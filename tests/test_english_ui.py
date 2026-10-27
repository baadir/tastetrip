import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

from app import profiles
from app.server import create_app


class EnglishPresentationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app({'TESTING': True, 'DATA_DIR': self.temp.name})
        self.client = self.app.test_client()
        self.client.get('/api/me')

    def tearDown(self):
        self.temp.cleanup()

    def test_legacy_profile_keeps_preferences_and_native_language(self):
        old = profiles.empty()
        old.update(profile_version=3, themes=['Kahve'], pace='Sakin')
        old['locale'] = {'ui_language': 'tr', 'native_language': 'ja'}
        with closing(sqlite3.connect(self.app.config['DATABASE'])) as db:
            visitor = db.execute('SELECT id FROM visitors').fetchone()[0]
            db.execute('INSERT INTO taste_profiles VALUES (?,?,?)',
                       ('visitor:' + visitor, 3, json.dumps(old)))
            db.commit()
        profile = self.client.get('/api/profile').json['profile']
        self.assertEqual(profile['locale'], {'ui_language': 'en', 'native_language': 'ja'})
        self.assertEqual(profile['themes'], ['Kahve'])
        self.assertEqual(profile['pace'], 'Sakin')
        self.assertEqual(profile['profile_version'], 3)

    def test_validation_errors_are_english(self):
        response = self.client.patch('/api/profile', json={
            'profile_version': 0, 'changes': {'unknown': True}}, headers={'X-TasteTrip': '1'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Unknown profile field.')

    def test_chat_uses_resolved_message_language_without_changing_native_language(self):
        with patch('app.providers.llm_json', side_effect=[
                {'language': 'English'}, {'reply': 'You do not have an itinerary yet.'}]) as model:
            response = self.client.post('/api/chat', json={
                'message': 'Show my itinerary', 'revision': 0, 'turn_id': 'english_language_turn'},
                headers={'X-TasteTrip': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['thread']['language'], 'English')
        self.assertEqual(response.json['profile']['locale']['native_language'], 'tr')
        self.assertIn('REQUIRED REPLY LANGUAGE FOR THIS TURN: English', model.call_args.args[0])
        self.assertEqual(model.call_args.kwargs['latest_message'], 'Show my itinerary')

    def test_static_page_labels_have_no_turkish_copy(self):
        class Labels(HTMLParser):
            def __init__(self):
                super().__init__()
                self.labels = []

            def handle_data(self, value):
                self.labels.append(value)

            def handle_starttag(self, tag, attrs):
                self.labels.extend(value for name, value in attrs
                                   if name in ('aria-label', 'placeholder', 'title', 'alt') and value)

        for filename in ('index.html', 'voice-monitor.html'):
            parser = Labels()
            parser.feed((Path(__file__).resolve().parents[1] / 'app/static' / filename).read_text(encoding='utf-8'))
            self.assertNotRegex(' '.join(parser.labels), r'[çğıöşüÇĞİÖŞÜ]|\b(?:Esnek|Japon|Dinleniyor)\b')
