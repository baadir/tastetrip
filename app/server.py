import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import threading
import time
from datetime import date
from contextlib import closing
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from . import planner, providers, profiles, reservations, chat

load_dotenv(Path(__file__).resolve().parent.parent / '.env')


def create_app(test_config=None):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.update(DATA_DIR=os.getenv('DATA_DIR', './data'), MAX_CONTENT_LENGTH=64 * 1024,
                      COOKIE_SECURE=os.getenv('COOKIE_SECURE', 'false').lower() == 'true')
    if test_config:
        app.config.update(test_config)
    Path(app.config['DATA_DIR']).mkdir(parents=True, exist_ok=True)
    app.config['DATABASE'] = str(Path(app.config['DATA_DIR']) / 'tastetrip.sqlite3')

    def db():
        if 'db' not in g:
            g.db = sqlite3.connect(app.config['DATABASE'], timeout=15)
            g.db.row_factory = sqlite3.Row
            g.db.execute('PRAGMA busy_timeout=15000')
        return g.db

    with closing(sqlite3.connect(app.config['DATABASE'])) as connection:
        connection.executescript('''
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS visitors(id TEXT PRIMARY KEY, prefs TEXT NOT NULL DEFAULT '{}', seen REAL);
        CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, username TEXT UNIQUE, password TEXT);
        CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, user_id TEXT NOT NULL, expires REAL);
        CREATE TABLE IF NOT EXISTS drafts(visitor_id TEXT PRIMARY KEY, body TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS media_preferences(visitor_id TEXT PRIMARY KEY, body TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS plans(id TEXT NOT NULL, user_id TEXT NOT NULL, body TEXT NOT NULL,
          updated REAL NOT NULL, PRIMARY KEY(id,user_id));
        ''')
        profiles.init_db(connection)
        chat.init_db(connection)
        connection.commit()

    @app.teardown_appcontext
    def close_db(_error):
        connection = g.pop('db', None)
        if connection:
            connection.close()

    def digest(token):
        return hashlib.sha256(token.encode()).hexdigest()

    throttle_lock = threading.Lock()
    buckets = {}

    def limit(key, count, window=60):
        now = time.time()
        with throttle_lock:
            recent = [t for t in buckets.get(key, []) if t > now - window]
            if len(recent) >= count:
                return False
            buckets[key] = recent + [now]
            if len(buckets) > 5000:
                for k in list(buckets):
                    if not buckets[k] or buckets[k][-1] < now - 900:
                        buckets.pop(k, None)
        return True

    @app.before_request
    def context():
        if request.path.startswith('/api/internal/reservations/'):
            return
        if request.path == '/health' or request.path.startswith('/static/'):
            return
        if request.method in ('POST', 'PATCH', 'DELETE'):
            allowed = os.getenv('APP_ORIGIN', 'http://localhost:8080').rstrip('/')
            origin = request.headers.get('Origin')
            if origin and origin != allowed:
                return jsonify(error='Request source not accepted.'), 403
            if request.headers.get('X-TasteTrip') != '1' or not request.is_json:
                return jsonify(error='Invalid application request.'), 403
            if not limit(('request', request.remote_addr), 80):
                return jsonify(error='Too many requests. Try again in a minute.'), 429
        token = request.cookies.get('tt_visitor', '')
        if not re.fullmatch(r'[A-Za-z0-9_-]{43}', token):
            token = secrets.token_urlsafe(32)
        g.visitor_token, g.visitor = token, digest(token)
        db().execute('INSERT OR IGNORE INTO visitors(id,seen) VALUES (?,?)', (g.visitor, time.time()))
        db().commit()
        session = request.cookies.get('tt_session', '')
        row = db().execute('SELECT users.id,users.username FROM sessions JOIN users ON users.id=sessions.user_id '
                           'WHERE token=? AND expires>?', (digest(session), time.time())).fetchone()
        g.user = dict(row) if row else None

    @app.after_request
    def headers(response):
        if hasattr(g, 'visitor_token'):
            profile = profiles.load(db)
            response.set_cookie('tt_visitor', g.visitor_token, max_age=None if profile['persistence'] == 'session' else 180 * 86400,
                                httponly=True, secure=app.config['COOKIE_SECURE'], samesite='Lax')
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        voice_origin = os.getenv('VOICE_PUBLIC_URL', '').rstrip('/')
        voice_source = (' ' + voice_origin.replace('https://', 'wss://', 1)) if re.fullmatch(r'https://[A-Za-z0-9.-]+(?::[0-9]+)?', voice_origin) else ''
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' https: data:; "
            "connect-src 'self'" + voice_source + "; frame-src https:; object-src 'none'; base-uri 'self'; frame-ancestors 'none'")
        if request.path.startswith('/api/'):
            response.headers['Cache-Control'] = 'no-store'
        return response

    @app.errorhandler(ValueError)
    def bad_input(error):
        return jsonify(error=str(error)[:600] or 'Check the information entered.'), 400

    @app.errorhandler(providers.ProviderError)
    def upstream_error(error):
        return jsonify(error=str(error)), 503

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify(error='Request too large.'), 413

    @app.errorhandler(500)
    def failure(_error):
        return jsonify(error='Operation could not be completed. Your current route was preserved.'), 500

    def body():
        value = request.get_json()
        if not isinstance(value, dict):
            raise ValueError('JSON object expected.')
        return value

    profiles.register(app, db, body)
    chat.register(app, db, body, limit)

    def draft():
        row = db().execute('SELECT body FROM drafts WHERE visitor_id=?', (g.visitor,)).fetchone()
        if not row:
            raise ValueError('First create a route or open your saved route.')
        return decorate_reservations(json.loads(row['body']))

    def decorate_reservations(plan):
        if g.user:
            with app.extensions['reservations'].db() as connection:
                rows = connection.execute("SELECT r.stop_id,a.id,a.result FROM reservation_attempts a JOIN reservation_requests r ON r.id=a.request_id WHERE a.user_id=? AND r.plan_id=? ORDER BY a.created", (g.user['id'],plan['id'])).fetchall()
            by_stop = {r['stop_id']:r for r in rows}
            for day in plan['days']:
                for stop in day['stops']:
                    if stop['id'] in by_stop:
                        stop['reservation_status'] = by_stop[stop['id']]['result']
                        stop['reservation_id'] = by_stop[stop['id']]['id']
        return plan

    def store_draft(plan):
        db().execute('INSERT OR REPLACE INTO drafts VALUES (?,?)', (g.visitor, json.dumps(plan)))
        db().commit()
        return plan

    reservations.register(app, db, body, draft, profiles)

    def auth_needed():
        return jsonify(error='You must log in for this action.', code='login_required'), 401

    @app.get('/health')
    def health():
        db().execute('SELECT 1')
        return jsonify(status='ok')

    @app.get('/')
    def index():
        return app.send_static_file('index.html')

    @app.get('/api/me')
    def me():
        prefs = json.loads(db().execute('SELECT prefs FROM visitors WHERE id=?', (g.visitor,)).fetchone()['prefs'])
        row = db().execute('SELECT body FROM drafts WHERE visitor_id=?', (g.visitor,)).fetchone()
        media = db().execute('SELECT body FROM media_preferences WHERE visitor_id=?', (g.visitor,)).fetchone()
        profile = profiles.load(db)
        return jsonify(user=g.user, preferences=prefs, profile=profile,
                       media_preferences=profiles.media_preferences(profile),
                       legacy_media_preferences=json.loads(media['body']) if media else {},
                       draft=decorate_reservations(json.loads(row['body'])) if row else None,
                       configured={'qloo': bool(os.getenv('QLOO_API_KEY')),
                                   'llm': bool(os.getenv('LLM_API_KEY') and os.getenv('LLM_MODEL')),
                                   'flights': bool(os.getenv('AVIASALES_API_TOKEN'))})

    @app.post('/api/preferences')
    def preferences():
        trip = planner.validate_trip(body())
        db().execute('UPDATE visitors SET prefs=? WHERE id=?', (json.dumps(trip), g.visitor))
        db().commit()
        return jsonify(ok=True)

    @app.post('/api/auth')
    def auth():
        if not limit(('auth', request.remote_addr), 12, 900):
            return jsonify(error='Too many login attempts. Try again later.'), 429
        data = body()
        username, password = str(data.get('username', '')).strip().lower(), data.get('password', '')
        if not re.fullmatch(r'[a-z0-9_.-]{3,50}', username) or not isinstance(password, str) or not 12 <= len(password) <= 200:
            raise ValueError('Username must be 3–50 lowercase letters/numbers; password must be at least 12 characters.')
        row = db().execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
        if data.get('register'):
            if row:
                raise ValueError('This username is not available.')
            user = {'id': secrets.token_urlsafe(16), 'username': username}
            try:
                db().execute('INSERT INTO users VALUES (?,?,?)',
                             (user['id'], username, generate_password_hash(password, method='scrypt')))
            except sqlite3.IntegrityError:
                raise ValueError('This username is not available.') from None
        else:
            if not row or not check_password_hash(row['password'], password):
                return jsonify(error='Username or password incorrect.'), 401
            user = {'id': row['id'], 'username': username}
        if g.user and g.user['id'] != user['id']:
            db().execute('DELETE FROM drafts WHERE visitor_id=?', (g.visitor,))
            db().execute('UPDATE visitors SET prefs=? WHERE id=?', ('{}', g.visitor))
            db().execute('DELETE FROM media_preferences WHERE visitor_id=?', (g.visitor,))
            db().execute('DELETE FROM taste_profiles WHERE owner=?', ('visitor:' + g.visitor,))
        session = secrets.token_urlsafe(32)
        old = request.cookies.get('tt_session', '')
        db().execute('DELETE FROM sessions WHERE token=? OR expires<?', (digest(old), time.time()))
        db().execute('INSERT INTO sessions VALUES (?,?,?)', (digest(session), user['id'], time.time() + 30 * 86400))
        db().commit()
        response = jsonify(user=user)
        response.set_cookie('tt_session', session, max_age=30 * 86400, httponly=True,
                            secure=app.config['COOKIE_SECURE'], samesite='Lax')
        return response

    @app.post('/api/logout')
    def logout():
        db().execute('DELETE FROM sessions WHERE token=?', (digest(request.cookies.get('tt_session', '')),))
        # Clear the device draft so an account route is not exposed after sign-out.
        db().execute('DELETE FROM drafts WHERE visitor_id=?', (g.visitor,))
        db().execute('UPDATE visitors SET prefs=? WHERE id=?', ('{}', g.visitor))
        db().execute('DELETE FROM media_preferences WHERE visitor_id=?', (g.visitor,))
        db().execute('DELETE FROM taste_profiles WHERE owner=?', ('visitor:' + g.visitor,))
        db().commit()
        g.user = None
        g.visitor_token = secrets.token_urlsafe(32)
        g.visitor = digest(g.visitor_token)
        response = jsonify(ok=True)
        response.delete_cookie('tt_session', secure=app.config['COOKIE_SECURE'], samesite='Lax')
        return response

    @app.post('/api/forget')
    def forget():
        db().execute('DELETE FROM taste_profiles WHERE owner=?', ('visitor:' + g.visitor,))
        db().execute('DELETE FROM drafts WHERE visitor_id=?', (g.visitor,))
        db().execute('DELETE FROM chat_threads WHERE owner=?', ('visitor:' + g.visitor,))
        db().execute('UPDATE visitors SET prefs=? WHERE id=?', ('{}', g.visitor))
        db().execute('DELETE FROM media_preferences WHERE visitor_id=?', (g.visitor,))
        db().commit()
        return jsonify(ok=True)

    @app.post('/api/session/new')
    def new_session():
        body()
        db().execute('DELETE FROM sessions WHERE token=?', (digest(request.cookies.get('tt_session', '')),))
        db().commit()
        # Rotate identity without deleting the old profile, conversation, or route draft.
        g.user = None
        g.visitor_token = secrets.token_urlsafe(32)
        g.visitor = digest(g.visitor_token)
        db().execute('INSERT INTO visitors(id,seen) VALUES (?,?)', (g.visitor, time.time()))
        db().commit()
        response = jsonify(ok=True)
        response.delete_cookie('tt_session', secure=app.config['COOKIE_SECURE'], samesite='Lax')
        return response

    @app.post('/api/interests/search')
    def interests():
        data = body()
        query = str(data.get('query', '')).strip()
        if not 2 <= len(query) <= 100:
            raise ValueError('Search for an artist, book, film, or place with at least two characters.')
        kind = data.get('kind')
        if kind and kind not in ('book', 'movie', 'podcast', 'artist', 'tv_show', 'videogame', 'brand', 'destination', 'place'):
            raise ValueError('Invalid content type.')
        results = providers.resolve_interests(query, kind)
        profiles.catalog(db, results, kind)
        return jsonify(results=results)

    @app.post('/api/plan')
    def plan():
        if not limit(('plan', g.visitor), 5, 300):
            return jsonify(error='You have reached the route creation limit. Try again in a few minutes.'), 429
        data = body()
        profile = profiles.load(db)
        resolved = {**{'budget': profile['budget'], 'pace': profile['pace'], 'transport': profile['transport']}, **data}
        trip = planner.validate_trip(resolved)
        context = profiles.context(profile, 'place')
        if profile['profile_version']:
            trip['taste_context'] = context
            trip['profile_version'] = profile['profile_version']
            trip['travel_themes'] = profile['themes']
            trip['special_requirements'] = profile['special_requirements']
        db().execute('UPDATE visitors SET prefs=? WHERE id=?', (json.dumps(trip), g.visitor))
        db().commit()
        return jsonify(plan=store_draft(planner.generate(trip)))

    @app.post('/api/revise')
    def revise():
        data, old = body(), draft()
        if data.get('revision') != old['revision']:
            return jsonify(error='The draft was changed in another operation. Refresh the page.'), 409
        old = json.loads(json.dumps(old))
        profile = profiles.load(db)
        old['trip']['taste_context'] = profiles.context(profile, 'place')
        old['trip']['profile_version'] = profile['profile_version']
        old['trip']['travel_themes'] = profile['themes']
        updated = planner.revise(old, data.get('instruction'))
        if 'clarification' in updated:
            return jsonify(**updated)
        # Recheck after the slow model call; concurrent revisions may have finished.
        connection = db()
        connection.execute('BEGIN IMMEDIATE')
        current = json.loads(connection.execute('SELECT body FROM drafts WHERE visitor_id=?', (g.visitor,)).fetchone()['body'])
        if current['id'] != old['id'] or current['revision'] != old['revision']:
            connection.rollback()
            return jsonify(error='The draft changed; load the new version and try again.'), 409
        return jsonify(plan=store_draft(updated))

    @app.post('/api/recommend')
    def recommend():
        data, current = body(), draft()
        valid = {s['id'] for d in current['days'] for s in d['stops']}
        stop_id = data.get('stop_id')
        if stop_id not in valid:
            raise ValueError('Select a valid stop.')
        kind = data.get('kind')
        if kind not in ('book', 'movie', 'podcast', 'artist', 'tv_show', 'videogame', 'brand', 'destination'):
            raise ValueError('Invalid content type.')
        profile = profiles.load(db)
        saved_content = profile['content'].get(kind, {})
        language = data.get('language', saved_content.get('language', 'any'))
        from .content_languages import LANGUAGES, filter_content_language
        if language != 'any' and (kind not in ('book', 'podcast') or language not in LANGUAGES):
            raise ValueError('Select a valid language for this content.')
        tastes = data.get('tastes', saved_content.get('tastes', []))
        if not isinstance(tastes, list) or len(tastes) > 5 or any(
                not isinstance(t, dict) or not re.fullmatch(
                    (r'urn:tag:[A-Za-z0-9_:-]{1,180}' if kind == 'podcast' else
                     r'(?:urn:tag:[A-Za-z0-9_:-]{1,180}|[A-Fa-f0-9-]{36})' if kind == 'book' else
                     r'[A-Fa-f0-9-]{36}'), str(t.get('id', '')))
                or not isinstance(t.get('name'), str) or not 1 <= len(t['name']) <= 250 for t in tastes):
            raise ValueError('You can select at most 5 valid works.')
        if not tastes and data.get('skip_taste') is not True:
            raise ValueError('First select a work you like or continue with “Skip for now”.')
        tastes = list({t['id']: {'id': t['id'], 'name': t['name']} for t in tastes}.values())
        # Persistent preferences change only on explicit opt-in; recommendations otherwise read the master.
        if tastes:
            profiles.checked_items(db, tastes, kind)
        if data.get('remember_profile') is True and data.get('profile_version') != profile['profile_version']:
            return jsonify(error='The profile changed. Keep your selections and reload.', code='profile_conflict'), 409
        context = profiles.context(profile, kind)
        effective = tastes if 'tastes' in data or data.get('skip_taste') is True else saved_content.get('tastes', [])
        topics = [t['id'] for t in effective if t['id'].startswith('urn:tag:')]
        explicit_entities = [t['id'] for t in effective if not t['id'].startswith('urn:tag:')]
        # An explicit empty selection overrides this content's saved seeds, not unrelated favorites.
        general = [t['id'] for t in profile['favorites'] if profiles.UUID.fullmatch(t['id'])]
        seeds = list(dict.fromkeys(explicit_entities + general + current['trip']['interests'] + [stop_id]))[:8]
        extra = {'excluded': context['excluded']} if context['excluded'] else {}
        if kind in ('book', 'podcast') and language != 'any':
            results = providers.media_candidates(kind, seeds, topics, take=20, **extra)
            results, language_status = filter_content_language(results, kind, language, app.config['DATA_DIR'])
        else:
            results = providers.media_candidates(kind, seeds, topics, **extra) if kind in ('book', 'podcast') else providers.media_candidates(kind, seeds, **extra)
            language_status = None
            if kind == 'podcast':
                from .content_languages import enrich_podcast_links
                results = enrich_podcast_links(results, app.config['DATA_DIR'])
        if data.get('remember_profile') is True:
            if data.get('profile_version') != profile['profile_version']:
                return jsonify(error='The profile changed. Keep your selections and reload.', code='profile_conflict'), 409
            entry = {'tastes': tastes, 'language': language, 'query': data.get('query', '')}
            value = profiles.validate(db, {'content': {kind: entry}}, profile)
            saved = profiles.save(db, value, profile['profile_version'])
            if saved is None:
                return jsonify(error='The profile changed. Reload.', code='profile_conflict'), 409
            profile = saved
        return jsonify(results=results, tastes=tastes, profile=profile, language_status=language_status,
                       basis=('Your selected topics and travel context' if topics else 'Your selected works and travel context') if tastes else 'Travel context and your general preferences, if any')

    @app.post('/api/podcast/topics')
    @app.post('/api/content/topics')
    def podcast_topics():
        data = body()
        text = str(data.get('query', '')).strip()
        if not 2 <= len(text) <= 300:
            raise ValueError('Write the topic you want to listen to with 2–300 characters.')
        if not limit(('topics', g.visitor), 12, 300):
            return jsonify(error='Too many topic searches. Try again a little later.'), 429
        kind = data.get('kind', 'podcast')
        result = providers.content_topics(text, kind)
        profiles.catalog(db, result['topics'], kind)
        return jsonify(**result)

    @app.get('/api/plans')
    def saved():
        if not g.user:
            return auth_needed()
        rows = db().execute('SELECT body FROM plans WHERE user_id=? ORDER BY updated DESC', (g.user['id'],)).fetchall()
        return jsonify(plans=[decorate_reservations(json.loads(r['body'])) for r in rows])

    @app.post('/api/plans/save')
    def save():
        if not g.user:
            return auth_needed()
        current = draft()
        db().execute('INSERT OR REPLACE INTO plans VALUES (?,?,?,?)',
                     (current['id'], g.user['id'], json.dumps(current), time.time()))
        db().commit()
        return jsonify(ok=True, id=current['id'])

    @app.post('/api/plans/open')
    def open_plan():
        if not g.user:
            return auth_needed()
        row = db().execute('SELECT body FROM plans WHERE id=? AND user_id=?',
                           (body().get('id'), g.user['id'])).fetchone()
        if not row:
            return jsonify(error='Route not found.'), 404
        return jsonify(plan=store_draft(decorate_reservations(json.loads(row['body']))))

    @app.post('/api/airports')
    def airports():
        term = str(body().get('query', '')).strip()
        if not 2 <= len(term) <= 100:
            raise ValueError('Search city or airport.')
        return jsonify(results=providers.airport_search(term))

    @app.post('/api/flights')
    def flight_search():
        data = body()
        origin, destination = str(data.get('origin', '')).upper(), str(data.get('destination', '')).upper()
        if not re.fullmatch('[A-Z]{3}', origin) or not re.fullmatch('[A-Z]{3}', destination) or origin == destination:
            raise ValueError('Select different departure and arrival airports.')
        departure = date.fromisoformat(data.get('departure', '')).isoformat()
        returning = data.get('return')
        if departure < date.today().isoformat():
            raise ValueError('Flights cannot be searched for a past date.')
        if returning:
            returning = date.fromisoformat(returning).isoformat()
            if returning < departure:
                raise ValueError('Return date cannot be before departure.')
        return jsonify(results=providers.flights(origin, destination, departure, returning),
                       search_url=providers.flight_search_url(origin, destination, departure, returning),
                       notice='These are Travelpayouts cached prices; not a final price or availability. No purchase is made.')

    return app


if __name__ == '__main__':
    create_app().run(host='127.0.0.1', port=int(os.getenv('PORT', '8080')), threaded=True)
