"""Durable, owner-scoped restaurant reservation requests; no provider POST in web threads."""
import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from pathlib import Path

import phonenumbers
from flask import g, jsonify, request
from .voice_languages import COUNTRY_LANGUAGE, COUNTRY_ZONE, model_for, supported, normalize_language

ACTIVE = ('queued','initiating','ringing','connected','unknown')
TERMINAL = ('ended','failed','busy','no_answer','canceled','rejected')


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def listen_token(secret, attempt, ttl=30):
    encoded=base64.urlsafe_b64encode(json.dumps({'attempt':attempt,'exp':int(time.time())+ttl,'nonce':secrets.token_hex(12)}).encode()).decode().rstrip('=')
    return encoded+'.'+hmac.new(secret.encode(),encoded.encode(),hashlib.sha256).hexdigest()


def verify_listen_token(secret, token, attempt):
    try:
        encoded,signature=token.split('.')
        if not secret or not hmac.compare_digest(signature,hmac.new(secret.encode(),encoded.encode(),hashlib.sha256).hexdigest()): return False
        data=json.loads(base64.urlsafe_b64decode(encoded+'='*(-len(encoded)%4)))
        return data['attempt']==attempt and time.time()<data['exp']<=time.time()+40
    except (ValueError,KeyError,TypeError): return False


class ReservationStore:
    def __init__(self,path):
        self.path=str(path)
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        with self.db() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS reservation_worker_heartbeat(id INTEGER PRIMARY KEY,at REAL NOT NULL,ready INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS reservation_requests(id TEXT PRIMARY KEY,user_id TEXT NOT NULL,plan_id TEXT NOT NULL,revision INTEGER NOT NULL,stop_id TEXT NOT NULL,digest TEXT NOT NULL,body TEXT NOT NULL,created REAL NOT NULL,expires REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS reservation_attempts(id TEXT PRIMARY KEY,request_id TEXT NOT NULL,user_id TEXT NOT NULL,key TEXT NOT NULL,status TEXT NOT NULL,result TEXT NOT NULL DEFAULT 'pending',sid TEXT UNIQUE,created REAL NOT NULL,updated REAL NOT NULL,stop_requested INTEGER NOT NULL DEFAULT 0,error_code INTEGER,summary TEXT,summary_status TEXT NOT NULL DEFAULT 'pending',UNIQUE(user_id,key));
            CREATE TABLE IF NOT EXISTS reservation_outbox(attempt_id TEXT PRIMARY KEY,state TEXT NOT NULL,claimed REAL);
            CREATE TABLE IF NOT EXISTS reservation_events(seq INTEGER PRIMARY KEY AUTOINCREMENT,attempt_id TEXT NOT NULL,event_id TEXT NOT NULL,role TEXT NOT NULL,text TEXT NOT NULL,translation TEXT,translation_status TEXT NOT NULL DEFAULT 'pending',created REAL NOT NULL,UNIQUE(attempt_id,event_id));
            ''')
            db.execute('BEGIN IMMEDIATE')
            columns={r[1] for r in db.execute('PRAGMA table_info(reservation_attempts)')}
            for name in ('script','reference','confirmation_source'):
                if name not in columns:db.execute('ALTER TABLE reservation_attempts ADD COLUMN '+name+' TEXT')
            for name in ('transcript_revision','summary_revision'):
                if name not in columns:db.execute('ALTER TABLE reservation_attempts ADD COLUMN '+name+' INTEGER NOT NULL DEFAULT 0')
            event_columns={r[1] for r in db.execute('PRAGMA table_info(reservation_events)')}
            if 'kind' not in event_columns:db.execute("ALTER TABLE reservation_events ADD COLUMN kind TEXT NOT NULL DEFAULT 'utterance'")
            # Text is retained for 30 days; audio is never persisted.
            db.execute('DELETE FROM reservation_events WHERE created<?',(time.time()-30*86400,))
            db.execute("UPDATE reservation_attempts SET summary=NULL,script=NULL,summary_status='expired' WHERE created<?",(time.time()-30*86400,))

    @contextmanager
    def db(self):
        db=sqlite3.connect(self.path,timeout=15);db.row_factory=sqlite3.Row
        try:
            db.execute('PRAGMA busy_timeout=15000')
            with db: yield db
        finally: db.close()

    def request(self,id,user=None):
        with self.db() as db:
            row=db.execute('SELECT * FROM reservation_requests WHERE id=?'+(' AND user_id=?' if user else ''),(id,user) if user else (id,)).fetchone()
        return dict(row) if row else None

    def attempt(self,id,user=None):
        with self.db() as db:
            row=db.execute('SELECT * FROM reservation_attempts WHERE id=?'+(' AND user_id=?' if user else ''),(id,user) if user else (id,)).fetchone()
        return dict(row) if row else None

    def public(self,id,user):
        attempt=self.attempt(id,user)
        if not attempt: return None
        req=self.request(attempt['request_id'],user)
        with self.db() as db:
            events=[dict(r) for r in db.execute('SELECT seq,event_id,role,text,translation,translation_status,created FROM reservation_events WHERE attempt_id=? ORDER BY seq',(id,))]
        return {k:attempt[k] for k in ('id','request_id','status','result','created','updated','stop_requested','error_code','summary_status','reference','transcript_revision','summary_revision','confirmation_source')} | {'terms':json.loads(req['body']), 'digest':req['digest'], 'plan_id':req['plan_id'], 'stop_id':req['stop_id'], 'events':events,'summary':json.loads(attempt['summary']) if attempt['summary'] else None}

    def enqueue(self,req,user,key,retry_of=None):
        if not isinstance(key,str) or not re.fullmatch(r'[A-Za-z0-9_-]{16,80}',key): raise ValueError('The attempt key is invalid.')
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            previous=db.execute('SELECT * FROM reservation_attempts WHERE user_id=? AND key=?',(user,key)).fetchone()
            if previous:
                if previous['request_id']!=req['id']: raise ValueError('This attempt key belongs to another reservation.')
                return previous['id']
            old=db.execute("SELECT a.id,a.status,a.result FROM reservation_attempts a JOIN reservation_requests r ON r.id=a.request_id WHERE a.request_id=? OR (a.user_id=? AND ((r.plan_id=? AND r.stop_id=?) OR r.digest=?)) ORDER BY a.created DESC LIMIT 1",(req['id'],user,req['plan_id'],req['stop_id'],req['digest'])).fetchone()
            if old and not (old['id']==retry_of and old['status'] in TERMINAL and old['result'] in ('not_completed','declined')): raise ValueError('An attempt already exists for this stop. Review the existing result first; do not retry when the situation is unclear.')
            if db.execute("SELECT 1 FROM reservation_attempts WHERE status IN ('queued','initiating','ringing','connected','unknown') LIMIT 1").fetchone(): raise ValueError('An interview is in progress or its result is unclear. Check the current attempt first.')
            limit=max(1,min(1000,int(os.getenv('RESERVATION_DAILY_LIMIT','10'))))
            if db.execute('SELECT COUNT(*) FROM reservation_attempts WHERE user_id=? AND created>?',(user,time.time()-86400)).fetchone()[0]>=limit:raise ValueError('You have reached the daily call attempt limit.')
            id=secrets.token_urlsafe(24);now=time.time()
            db.execute("INSERT INTO reservation_attempts(id,request_id,user_id,key,status,created,updated) VALUES (?,?,?,?,'queued',?,?)",(id,req['id'],user,key,now,now))
            db.execute("INSERT INTO reservation_outbox VALUES (?,'pending',NULL)",(id,))
            return id

    def update(self,id,**fields):
        allowed={'status','result','sid','stop_requested','error_code','summary','summary_status','script','reference','confirmation_source'}
        if not fields or set(fields)-allowed: raise ValueError('Invalid attempt update')
        with self.db() as db:
            db.execute('UPDATE reservation_attempts SET '+','.join(k+'=?' for k in fields)+',updated=? WHERE id=?',(*fields.values(),time.time(),id))

    def event(self,id,event):
        if not isinstance(event,dict) or event.get('role') not in ('assistant','restaurant','system') or not isinstance(event.get('text'),str) or not 1<=len(event['text'])<=4000 or not re.fullmatch('[A-Za-z0-9_-]{8,80}',str(event.get('event_id',''))): raise ValueError('Invalid interview event.')
        with self.db() as db:
            kind=event.get('kind','utterance')
            if kind not in ('utterance','readback') or (kind=='readback' and event['role']!='assistant'):raise ValueError('Invalid conversation type.')
            db.execute('BEGIN IMMEDIATE')
            previous=db.execute("SELECT role,kind,text FROM reservation_events WHERE attempt_id=? AND role!='system' ORDER BY seq DESC LIMIT 1",(id,)).fetchone()
            added=db.execute('INSERT OR IGNORE INTO reservation_events(attempt_id,event_id,role,text,kind,created) VALUES (?,?,?,?,?,?)',(id,event['event_id'],event['role'],event['text'],kind,time.time()))
            if added.rowcount:
                db.execute("UPDATE reservation_attempts SET transcript_revision=transcript_revision+1,summary_status=CASE WHEN summary_status IN ('ready','failed','insufficient') THEN 'pending' ELSE summary_status END WHERE id=?",(id,))
                # A deterministic, narrow acceptance path: only after the exact app-generated readback
                # completed playback, followed immediately by an unambiguous staff confirmation.
                if event['role']=='restaurant' and previous and previous['role']=='assistant' and previous['kind']=='readback':
                    req=db.execute('SELECT r.body FROM reservation_requests r JOIN reservation_attempts a ON a.request_id=r.id WHERE a.id=?',(id,)).fetchone()
                    terms=json.loads(req['body'])
                    text=re.sub(r"[.!،,;:]",'',event['text'].strip().casefold()).strip()
                    affirmative={'en':{'confirmed','yes confirmed','your reservation is confirmed','the reservation is confirmed','yes the reservation is confirmed'},'tr':{'confirmed','I confirm','yes I confirm','your reservation is confirmed','I confirm the reservation'}}
                    # Exact numeric literals and name make the readback auditable; availability is never acceptance.
                    exact=all(str(terms[k]) in previous['text'] for k in ('local_date','local_time','people','booking_name'))
                    if exact and text in affirmative.get(terms['conversation_language'],set()):
                        db.execute("UPDATE reservation_attempts SET result='confirmed',confirmation_source='restaurant_exact_reply',updated=? WHERE id=? AND result IN ('pending','unknown')",(time.time(),id))
                elif event['role']=='restaurant':
                    current=db.execute('SELECT result,confirmation_source FROM reservation_attempts WHERE id=?',(id,)).fetchone()
                    if current['result']=='confirmed' and current['confirmation_source']=='restaurant_exact_reply':
                        closing=re.sub(r"[.!،,;:]",'',event['text'].strip().casefold()).strip()
                        harmless={'thank you','thanks','you are welcome',"you're welcome",'goodbye','bye','thanks','thank you',"you're welcome",'good day','see you'}
                        if closing not in harmless:
                            db.execute("UPDATE reservation_attempts SET result='unknown',confirmation_source=NULL,updated=? WHERE id=?",(time.time(),id))




def checked_terms(stop,trip,data,native):
    if stop.get('category') not in ('restaurant','cafe','bar') or not stop.get('phone'): raise ValueError('Phone-based table reservations are not supported for this stop.')
    country=data.get('country_code',stop.get('country_code') or '')
    if not isinstance(country,str) or not re.fullmatch('[A-Z]{2}',country) or country not in phonenumbers.SUPPORTED_REGIONS: raise ValueError("Specify the restaurant's country with a two-letter code; for example TR, IE or FR.")
    try:
        phone=phonenumbers.parse(stop['phone'],country)
        if not phonenumbers.is_valid_number(phone) or phone.country_code!=phonenumbers.country_code_for_region(country): raise ValueError()
        number=phonenumbers.format_number(phone,phonenumbers.PhoneNumberFormat.E164)
    except (phonenumbers.NumberParseException,ValueError): raise ValueError("The restaurant's phone number could not be verified; use the existing source link.") from None
    if data.get('phone_verified') is not True: raise ValueError('Verify and confirm the number and business match from the source link.')
    if data.get('timezone_verified') is not True: raise ValueError("Verify and confirm the restaurant's local time zone.")
    zone=data.get('timezone') or COUNTRY_ZONE.get(country)
    try:
        tz=ZoneInfo(zone)
        date_time=datetime.fromisoformat(str(data.get('local_date',''))+'T'+str(data.get('local_time','')))
        if date_time.tzinfo: raise ValueError()
        valid=[]
        for fold in (0,1):
            local=date_time.replace(tzinfo=tz,fold=fold)
            if local.astimezone(timezone.utc).astimezone(tz).replace(tzinfo=None)==date_time: valid.append(local)
        if not valid: raise ValueError('This local time does not exist during the time zone transition.')
        if len({v.utcoffset() for v in valid})>1: raise ValueError('This time occurs twice during the time zone transition; choose a different time.')
        when=valid[0]
        if when.timestamp()<=time.time(): raise ValueError("The reservation time must be in the future according to the restaurant's local time.")
    except (ZoneInfoNotFoundError,TypeError): raise ValueError("Select the restaurant's IANA time zone; for example Europe/Paris.") from None
    except ValueError as error: raise ValueError(str(error) if str(error) else 'Specify a valid date and time.') from None
    name=data.get('booking_name','');people=data.get('people');notes=data.get('notes','')
    if not isinstance(name,str) or not 2<=len(name.strip())<=100 or any(ord(x)<32 for x in name): raise ValueError('The reservation name must be 2–100 characters.')
    if type(people) is not int or not 1<=people<=20: raise ValueError('The number of people must be between 1 and 20.')
    if not isinstance(notes,str) or len(notes)>600: raise ValueError('Special requests must be at most 600 characters.')
    language=data.get('conversation_language') or COUNTRY_LANGUAGE.get(country,'')
    locale=language
    language=normalize_language(language)
    model=model_for(language)
    if not isinstance(native,str) or not re.fullmatch('[a-z]{2,3}(?:-[A-Z]{2})?',native): raise ValueError('Specify your native language.')
    return {'restaurant':stop['name'],'address':stop.get('address',''),'phone':number,'phone_source':'Qloo stop selected; user verified the business match','map_url':stop.get('map_url'),'website':stop.get('website'),'country_code':country,'timezone':zone,'conversation_language':language,'conversation_locale':locale,'native_language':native,'local_date':when.date().isoformat(),'local_time':when.strftime('%H:%M'),'utc':when.astimezone(timezone.utc).isoformat(),'people':people,'booking_name':name.strip(),'notes':notes.strip(),'model':model,'max_seconds':180,'alternatives':'Only the specified exact date/time and number of people; alternatives are not accepted.'}


def register(app,db,body,draft,profiles):
    store=ReservationStore(app.config['DATABASE']);app.extensions['reservations']=store
    def owned(id):
        return store.attempt(id,g.user['id']) if g.user else None
    def fail_login(): return jsonify(error='You must sign in to make a reservation.',code='login_required'),401
    def internal():
        secret=os.getenv('VOICE_MONITOR_TOKEN','')
        return bool(secret) and hmac.compare_digest(request.headers.get('Authorization',''),'Bearer '+secret)

    def worker_ready():
        with store.db() as connection:
            row=connection.execute('SELECT at,ready FROM reservation_worker_heartbeat WHERE id=1').fetchone()
        return bool(row and row['ready'] and row['at']>time.time()-45)

    @app.get('/api/reservations')
    def listing():
        if not g.user:return fail_login()
        with store.db() as connection:
            ids=[r['id'] for r in connection.execute('SELECT id FROM reservation_attempts WHERE user_id=? ORDER BY created DESC LIMIT 100',(g.user['id'],))]
        return jsonify(reservations=[store.public(id,g.user['id']) for id in ids])

    @app.get('/api/reservations/options')
    def options():
        return jsonify(languages=sorted(supported()),countries=sorted(phonenumbers.SUPPORTED_REGIONS),country_languages=COUNTRY_LANGUAGE,country_timezones=COUNTRY_ZONE,max_seconds=180,worker_available=worker_ready())

    @app.post('/api/reservations/prepare')
    def prepare():
        if not g.user:return fail_login()
        data=body();plan=draft()
        if data.get('plan_id')!=plan['id'] or data.get('revision')!=plan['revision']:return jsonify(error='The route changed. Start again from the current stop.'),409
        stop=next((s for d in plan['days'] for s in d['stops'] if s['id']==data.get('stop_id')),None)
        if not stop:raise ValueError('Select a valid stop within this route.')
        profile=profiles.load(db)
        terms=checked_terms(stop,plan['trip'],data,data.get('native_language',profile['locale']['native_language']))
        id=secrets.token_urlsafe(24);hash=digest(terms);now=time.time()
        with store.db() as connection:
            connection.execute('INSERT INTO reservation_requests VALUES (?,?,?,?,?,?,?,?,?)',(id,g.user['id'],plan['id'],plan['revision'],stop['id'],hash,json.dumps(terms),now,now+600))
            connection.execute('INSERT OR REPLACE INTO plans VALUES (?,?,?,?)',(plan['id'],g.user['id'],json.dumps(plan),now))
        return jsonify(request_id=id,digest=hash,terms=terms,expires=now+600)

    @app.post('/api/reservations/<id>/start')
    def start(id):
        if not g.user:return fail_login()
        data=body();req=store.request(id,g.user['id'])
        if not req:return jsonify(error='Reservation draft not found.'),404
        # Return the original attempt even after review expiry; never duplicate an uncertain POST.
        with store.db() as c:
            existing=c.execute('SELECT id,request_id FROM reservation_attempts WHERE user_id=? AND key=?',(g.user['id'],data.get('idempotency_key',''))).fetchone()
        if existing:
            if existing['request_id']!=id:raise ValueError('The attempt key belongs to another process.')
            return jsonify(reservation=store.public(existing['id'],g.user['id']))
        plan=draft()
        if req['expires']<time.time() or plan['id']!=req['plan_id'] or plan['revision']!=req['revision']:return jsonify(error='The summary or route changed. Review the details again.'),409
        if data.get('approved') is not True or not hmac.compare_digest(str(data.get('digest','')),req['digest']):raise ValueError('Confirm the current reservation summary.')
        if datetime.fromisoformat(json.loads(req['body'])['utc']).timestamp()<=time.time():raise ValueError('The reservation time is in the past.')
        missing=[k for k in ('TWILIO_ACCOUNT_SID','TWILIO_AUTH_TOKEN','TWILIO_FROM_NUMBER','VOICE_PUBLIC_URL','VOICE_MONITOR_TOKEN','DEEPGRAM_API_KEY','ELEVENLABS_API_KEY','ELEVENLABS_VOICE_ID','LLM_API_KEY','LLM_MODEL','LLM_BASE_URL') if not os.getenv(k)]
        if missing:return jsonify(error='Phone service configuration is missing; the call was not started.'),503
        if not re.fullmatch(r'https://[A-Za-z0-9.-]+(?::[0-9]+)?/?',os.getenv('VOICE_PUBLIC_URL','')) or not re.fullmatch(r'\+[1-9][0-9]{7,14}',os.getenv('TWILIO_FROM_NUMBER','')):return jsonify(error='Phone service HTTPS/number configuration is invalid.'),503
        if not worker_ready():return jsonify(error='Reservation worker or voice gateway is not ready; the call was not started.'),503
        id=store.enqueue(req,g.user['id'],data.get('idempotency_key'),data.get('retry_of'))
        return jsonify(reservation=store.public(id,g.user['id'])),202

    @app.get('/api/reservations/<id>')
    def status(id):
        if not g.user:return fail_login()
        value=store.public(id,g.user['id'])
        return jsonify(reservation=value) if value else (jsonify(error='Reservation not found.'),404)

    @app.post('/api/reservations/<id>/stop')
    def stop(id):
        if not g.user:return fail_login()
        attempt=owned(id)
        if not attempt:return jsonify(error='Reservation not found.'),404
        with store.db() as c:
            c.execute('BEGIN IMMEDIATE')
            row=c.execute('SELECT status FROM reservation_attempts WHERE id=?',(id,)).fetchone()
            if row['status']=='queued':
                c.execute("UPDATE reservation_attempts SET status='canceled',result='not_completed',stop_requested=1,updated=? WHERE id=?",(time.time(),id))
                c.execute("UPDATE reservation_outbox SET state='canceled' WHERE attempt_id=?",(id,))
            else:c.execute('UPDATE reservation_attempts SET stop_requested=1 WHERE id=?',(id,))
        return jsonify(reservation=store.public(id,g.user['id']),notice='Stopping the call does not cancel an existing table reservation.')

    @app.post('/api/reservations/<id>/listen-token')
    def listen(id):
        if not g.user:return fail_login()
        if not owned(id):return jsonify(error='Reservation not found.'),404
        secret=os.getenv('VOICE_MONITOR_TOKEN','');origin=os.getenv('VOICE_PUBLIC_URL','').rstrip('/')
        if not secret or not origin.startswith('https://'):return jsonify(error='Live voice connection is not configured.'),503
        return jsonify(token=listen_token(secret,id),url=origin.replace('https://','wss://',1)+'/reservations/listen/'+id)

    @app.post('/api/reservations/<id>/review-result')
    def review_result(id):
        if not g.user:return fail_login()
        attempt=owned(id)
        if not attempt:return jsonify(error='Reservation not found.'),404
        data=body();req=store.request(attempt['request_id'],g.user['id'])
        outcome=data.get('outcome','confirmed')
        if outcome not in ('confirmed','declined') or (attempt['result']=='confirmed' and outcome!='confirmed'):raise ValueError('A confirmed reservation cannot be canceled with this action.')
        if attempt['status'] not in TERMINAL or data.get('digest')!=req['digest'] or data.get('heard_acceptance') is not True:raise ValueError('Review the ended conversation and the final terms, and state the restaurant confirmation.')
        with store.db() as c:
            evidence=c.execute("SELECT seq,text FROM reservation_events WHERE attempt_id=? AND event_id=? AND role='restaurant'",(id,data.get('event_id'))).fetchone()
        if not evidence:raise ValueError("Select the conversation line containing the restaurant's acceptance.")
        reference=data.get('reference','')
        if not isinstance(reference,str) or len(reference)>80 or (reference and reference not in evidence['text']):raise ValueError('The reference number must appear verbatim in the selected restaurant statement; leave it blank if not provided.')
        store.update(id,result=outcome,reference=reference or None,confirmation_source='user_review')
        store.event(id,{'event_id':secrets.token_hex(16),'role':'system','text':'The user reviewed the selected restaurant statement and summary terms and confirmed the result: '+outcome+'. Evidence: '+data['event_id']})
        return jsonify(reservation=store.public(id,g.user['id']))

    @app.post('/api/reservations/<id>/summary/retry')
    def retry_summary(id):
        if not g.user:return fail_login()
        attempt=owned(id)
        if not attempt:return jsonify(error='Reservation not found.'),404
        if attempt['status'] not in TERMINAL:raise ValueError('Wait for the conversation to end for the summary.')
        store.update(id,summary_status='pending')
        return jsonify(ok=True)

    @app.route('/api/internal/reservations/<id>',methods=['GET','POST'])
    def internal_attempt(id):
        if not internal():return jsonify(error='Forbidden'),403
        attempt=store.attempt(id)
        if not attempt:return jsonify(error='Not found'),404
        if request.method=='GET':
            sid=request.args.get('sid','')
            if not re.fullmatch('CA[0-9a-fA-F]{32}',sid):return jsonify(error='Invalid call'),403
            with store.db() as c:
                c.execute('BEGIN IMMEDIATE')
                current=c.execute('SELECT sid,status FROM reservation_attempts WHERE id=?',(id,)).fetchone()
                if current['sid'] not in (None,sid) or current['status'] not in ('initiating','ringing','connected'):return jsonify(error='Call mismatch'),403
                c.execute("UPDATE reservation_attempts SET sid=?,status='connected',updated=? WHERE id=?",(sid,time.time(),id))
            return jsonify(terms=json.loads(store.request(attempt['request_id'])['body']),script=json.loads(attempt['script']) if attempt['script'] else None,stop_requested=bool(attempt['stop_requested']))
        data=request.get_json()
        if not isinstance(data,dict):raise ValueError('Event expected')
        if data.get('type')=='ended':
            # Stream closure alone cannot assert Twilio ended, or a reservation succeeded.
            store.event(id,{'event_id':data['event_id'],'role':'system','text':'The audio stream has ended; the phone status is also being checked.'+(' The transcript may have missing parts.' if data.get('transcript_complete') is False else '')})
        else:store.event(id,data)
        return jsonify(ok=True)
