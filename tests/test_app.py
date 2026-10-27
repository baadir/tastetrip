from contextlib import closing
import copy
import os
import json
import sqlite3
import tempfile
import unittest
from datetime import date, timedelta
from unittest.mock import patch

from app.planner import revise, validate_assignment, validate_trip
from app.server import create_app


TRIP = {'city': 'Paris, France', 'start': (date.today() + timedelta(days=30)).isoformat(),
        'days': 2, 'people': 2, 'categories': ['museum', 'restaurant']}
PLAN = {'id': 'plan-1', 'revision': 1, 'trip': validate_trip(TRIP), 'mode': 'fixture', 'warnings': [],
        'notice': 'Test fixture', 'days': [
            {'number': 1, 'date': TRIP['start'], 'stops': [{'id': 'food', 'name': 'Food', 'category': 'restaurant'}]},
            {'number': 2, 'date': TRIP['start'], 'stops': [{'id': 'museum', 'name': 'Museum', 'category': 'museum'}]}]}


class PlanningTests(unittest.TestCase):
    def test_reject_fabricated_or_dropped_venues(self):
        pool = {'a': {}, 'b': {}}
        for assignment in ([{'stop_ids': ['fake']}, {'stop_ids': []}],
                           [{'stop_ids': ['a']}, {'stop_ids': ['a']}],
                           [{'stop_ids': ['a']}, {'stop_ids': []}]):
            with self.assertRaises(ValueError):
                validate_assignment({'days': assignment}, pool, 2, require_all=True)

    @patch('app.planner.llm_json', return_value={'days': [{'stop_ids': ['museum', 'food']}, {'stop_ids': []}]})
    def test_museum_move_preserves_all_venue_facts(self, _model):
        before = copy.deepcopy(PLAN)
        updated = revise(before, '2. gündeki müzeyi 1. güne al')
        self.assertEqual([s['id'] for s in updated['days'][0]['stops']], ['museum', 'food'])
        self.assertEqual(updated['revision'], 2)
        self.assertEqual(before, PLAN)

    @patch('app.planner.llm_json', return_value={'days': [{'stop_ids': ['museum', 'food']}, {'stop_ids': []}]})
    def test_confirmed_booking_cannot_move(self, _model):
        plan = copy.deepcopy(PLAN)
        plan['days'][1]['stops'][0]['reservation_status'] = 'confirmed'
        with self.assertRaises(ValueError):
            revise(plan, 'Müzeyi ilk güne al')


class APITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app({'TESTING': True, 'DATA_DIR': self.temp.name})
        self.client = self.app.test_client()
        self.headers = {'X-TasteTrip': '1'}
        self.client.get('/api/me')
        # Synthetic Qloo search/tag catalogue fixtures: recommendation inputs must be resolved.
        with closing(sqlite3.connect(self.app.config['DATABASE'])) as db, db:
            for kind in ('movie', 'book', 'podcast'):
                for id, name in [('012EF80C-B187-4ECB-9C3D-9CA5228B503C', 'Fixture '+kind),
                                 ('urn:tag:genre:media:science', 'Science')]:
                    db.execute('INSERT OR REPLACE INTO taste_catalog VALUES (?,?,?)',
                               (id, kind, json.dumps({'id': id, 'name': name, 'kind': kind})))


    def tearDown(self):
        self.temp.cleanup()

    def post(self, path, data, client=None):
        return (client or self.client).post('/api/' + path, json=data, headers=self.headers)

    def register(self, client, name):
        return self.post('auth', {'username': name, 'password': 'fictional-pass-1234', 'register': True}, client)

    @patch('app.planner.generate', return_value=PLAN)
    def test_action_login_save_reload_and_isolation(self, _generate):
        self.assertEqual(self.post('plan', TRIP).status_code, 200)
        self.assertEqual(self.post('plans/save', {}).status_code, 401)
        self.assertEqual(self.register(self.client, 'traveler').status_code, 200)
        self.assertEqual(self.post('plans/save', {}).status_code, 200)
        self.assertEqual(len(self.client.get('/api/plans').json['plans']), 1)
        other = self.app.test_client()
        other.get('/api/me')
        self.assertEqual(self.register(other, 'another').status_code, 200)
        self.assertEqual(other.get('/api/plans').json['plans'], [])
        self.assertEqual(self.post('plans/open', {'id': 'plan-1'}, other).status_code, 404)
        self.post('logout', {})
        self.assertIsNone(self.client.get('/api/me').json['draft'])
        self.assertEqual(self.post('auth', {'username': 'traveler', 'password': 'fictional-pass-1234'}).status_code, 200)
        self.assertEqual(self.post('plans/open', {'id': 'plan-1'}).json['plan']['id'], 'plan-1')

    def test_cookie_remembers_preferences_without_auth(self):
        response = self.client.get('/api/me')
        cookies = response.headers.getlist('Set-Cookie')
        self.assertTrue(any('HttpOnly' in c and 'SameSite=Lax' in c for c in cookies))
        self.assertEqual(self.post('preferences', TRIP).status_code, 200)
        me = self.client.get('/api/me').json
        self.assertIsNone(me['user'])
        self.assertEqual(me['preferences']['city'], TRIP['city'])
        self.post('forget', {})
        self.assertEqual(self.client.get('/api/me').json['preferences'], {})

    def test_csrf_and_invalid_inputs(self):
        self.assertEqual(self.client.post('/api/plan', json=TRIP).status_code, 403)
        self.assertEqual(self.client.post('/api/plan', json=TRIP,
                         headers={**self.headers, 'Origin': 'https://evil.example'}).status_code, 403)
        self.assertEqual(self.post('plan', {**TRIP, 'days': 400}).status_code, 400)
        self.assertEqual(self.post('flights', {'origin': 'IST', 'destination': 'IST', 'departure': TRIP['start']}).status_code, 400)

    @patch('app.planner.generate', return_value=PLAN)
    @patch('app.providers.media_candidates', return_value=[])
    def test_media_taste_is_explicit_typed_and_remembered(self, media, _generate):
        self.post('plan', TRIP)
        self.assertEqual(self.post('recommend', {'stop_id': 'museum', 'kind': 'movie'}).status_code, 400)
        taste = {'id': '012EF80C-B187-4ECB-9C3D-9CA5228B503C', 'name': 'Fixture movie'}
        self.assertEqual(self.post('recommend', {'stop_id': 'museum', 'kind': 'movie', 'tastes': [taste], 'remember_profile': True, 'profile_version': 0}).status_code, 200)
        self.assertEqual(media.call_args.args[1][0], taste['id'])
        self.assertEqual(self.client.get('/api/me').json['media_preferences']['movie'], [taste])
        self.assertNotIn('book', self.client.get('/api/me').json['media_preferences'])
        self.assertEqual(self.post('recommend', {'stop_id': 'museum', 'kind': 'book', 'skip_taste': True}).status_code, 200)
        self.post('forget', {})
        self.assertEqual(self.client.get('/api/me').json['media_preferences'], {})

    @patch('app.planner.generate', return_value=PLAN)
    @patch('app.providers.media_candidates', return_value=[])
    def test_podcast_topics_are_tags_not_entity_seeds(self, media, _generate):
        self.post('plan', TRIP)
        topic = {'id': 'urn:tag:genre:media:science', 'name': 'Science'}
        result = self.post('recommend', {'stop_id': 'museum', 'kind': 'podcast', 'tastes': [topic]})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(media.call_args.args[2], [topic['id']])
        self.assertNotIn(topic['id'], media.call_args.args[1])
        self.assertEqual(self.post('recommend', {'stop_id': 'museum', 'kind': 'movie', 'tastes': [topic]}).status_code, 400)

    @patch('app.planner.generate', return_value=PLAN)
    @patch('app.providers.media_candidates', return_value=[{'id': 'a', 'language': 'en'}, {'id': 'b', 'language': None}])
    def test_book_language_is_applied_and_invalid_language_rejected(self, media, _generate):
        self.post('plan', TRIP)
        query = {'stop_id': 'museum', 'kind': 'book', 'skip_taste': True, 'language': 'tr', 'remember_profile': True, 'profile_version': 0}
        response = self.post('recommend', query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['results'], [])
        self.assertEqual(response.json['language_status']['unknown'], 1)
        self.assertEqual(media.call_args.kwargs['take'], 20)
        self.assertEqual(self.client.get('/api/me').json['media_preferences']['_book_language'], 'tr')
        self.assertEqual(self.post('recommend', {**query, 'language': 'zz'}).status_code, 400)

    @patch('app.planner.generate', return_value=PLAN)
    @patch('app.providers.media_candidates', return_value=[])
    def test_book_keywords_use_tags_and_preserve_entity_preferences(self, media, _generate):
        self.post('plan', TRIP)
        topic = {'id': 'urn:tag:genre:media:science', 'name': 'Science'}
        favorite = {'id': '012EF80C-B187-4ECB-9C3D-9CA5228B503C', 'name': 'Fixture book'}
        result = self.post('recommend', {'stop_id': 'museum', 'kind': 'book', 'tastes': [topic, favorite]})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(media.call_args.args[2], [topic['id']])
        self.assertIn(favorite['id'], media.call_args.args[1])
        self.assertNotIn(topic['id'], media.call_args.args[1])

    @patch('app.planner.generate', return_value=PLAN)
    def test_no_automatic_media_queries_and_revision_recovery(self, _generate):
        with patch('app.providers.media_candidates') as media:
            self.post('plan', TRIP)
            self.client.get('/api/me')
            media.assert_not_called()
        with patch.dict(os.environ, {'LLM_API_KEY': '', 'LLM_MODEL': ''}):
            result = self.post('revise', {'revision': 1, 'instruction': 'Müzeyi ilk güne al'})
        self.assertEqual(result.status_code, 503)
        self.assertEqual(self.client.get('/api/me').json['draft']['revision'], 1)
        self.assertEqual(self.post('revise', {'revision': 99, 'instruction': 'Müzeyi taşı'}).status_code, 409)


if __name__ == '__main__':
    unittest.main()
