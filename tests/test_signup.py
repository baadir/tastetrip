import sqlite3
import tempfile
import unittest
from contextlib import closing

from werkzeug.security import check_password_hash
from app.server import create_app


class SignupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app({'TESTING': True, 'DATA_DIR': self.temp.name})
        self.client = self.app.test_client()
        self.headers = {'X-TasteTrip': '1'}

    def tearDown(self):
        self.temp.cleanup()

    def signup(self, **changes):
        data = {'username': 'synthetic_traveler', 'password': 'synthetic-password-123',
                'password_confirmation': 'synthetic-password-123', 'register': True}
        return self.client.post('/api/auth', json={**data, **changes}, headers=self.headers)

    def test_confirmation_mismatch_does_not_create_user_or_session(self):
        response = self.signup(password_confirmation='different-password-123')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Passwords do not match', response.json['error'])
        self.assertIsNone(self.client.get('/api/me').json['user'])
        with closing(sqlite3.connect(self.app.config['DATABASE'])) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM users').fetchone()[0], 0)

    def test_signup_normalizes_username_hashes_password_and_signs_in(self):
        response = self.signup(username=' Synthetic_Traveler ')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['user']['username'], 'synthetic_traveler')
        self.assertEqual(self.client.get('/api/me').json['user']['id'], response.json['user']['id'])
        self.assertNotIn('password', response.json['user'])
        with closing(sqlite3.connect(self.app.config['DATABASE'])) as db:
            stored = db.execute('SELECT password FROM users').fetchone()[0]
            self.assertNotEqual(stored, 'synthetic-password-123')
            self.assertTrue(check_password_hash(stored, 'synthetic-password-123'))
        self.client.post('/api/logout', json={}, headers=self.headers)
        duplicate = self.signup(username='SYNTHETIC_TRAVELER')
        self.assertEqual(duplicate.status_code, 400)
        self.assertIn('not available', duplicate.json['error'])
        self.assertIsNone(self.client.get('/api/me').json['user'])

    def test_string_registration_flag_cannot_create_an_account(self):
        self.assertEqual(self.signup(register='false').status_code, 400)
        with closing(sqlite3.connect(self.app.config['DATABASE'])) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM users').fetchone()[0], 0)
