import tempfile
import unittest
from contextlib import closing
from unittest.mock import patch
from app.server import create_app


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app({'TESTING': True, 'DATA_DIR': self.temp.name})
        self.client = self.app.test_client()
        self.headers = {'X-TasteTrip': '1'}

    def tearDown(self):
        self.temp.cleanup()

    def turn(self, output, text='Kahve severim', revision=0, tid='synthetic_turn_01'):
        with patch('app.providers.llm_json', return_value=output):
            return self.client.post('/api/chat', json={'message': text, 'turn_id':tid, 'revision':revision}, headers=self.headers)

    def test_explicit_preference_and_history_persist_together(self):
        result = self.turn({'reply':'Nasıl bir tempo seversin?', 'preferences':[
            {'scope':'profile','evidence':'Kahve severim','changes':{'themes':['Kahve']}}]})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['profile']['themes'], ['Kahve'])
        self.assertEqual(result.json['thread']['messages'][-1]['saved'], ['themes'])
        self.assertEqual(self.client.get('/api/chat').json['thread'], result.json['thread'])

    def test_scope_evidence_and_fabricated_ids_do_not_write(self):
        result = self.turn({'reply':'Bu seyahat için not aldım.', 'preferences':[
            {'scope':'trip','evidence':'Kahve','changes':{'themes':['Kahve']}},
            {'scope':'profile','evidence':'olmayan alıntı','changes':{'budget':1}},
            {'scope':'profile','evidence':'Kahve','changes':{'favorites':[{'id':'fake'}]}},
            {'scope':'profile','evidence':'Kahve','changes':{'content':{'book':{'tastes':[{'id':'fake'}]}}}}]})
        self.assertEqual(result.status_code,200)
        self.assertEqual(result.json['profile']['profile_version'],0)

    def test_retry_is_idempotent_and_collision_rejected(self):
        self.turn({'reply':'Merhaba'})
        with patch('app.providers.llm_json') as model:
            retry=self.turn({'reply':'Yeniden'})
            self.assertEqual(retry.json['thread']['revision'],1)
            self.assertEqual(len(retry.json['thread']['messages']),2)
        self.assertEqual(self.turn({'reply':'a'},text='başka metin').status_code,400)
        self.assertEqual(self.turn({'reply':'a'},tid='another_turn_id').status_code,409)

    def test_model_failure_leaves_profile_and_thread_unchanged(self):
        self.assertEqual(self.turn({'reply':None}).status_code,503)
        self.assertEqual(self.client.get('/api/chat').json['thread']['revision'],0)
        invalid=self.turn({'reply':'a','preferences':[{'scope':'profile','evidence':'Kahve','changes':{'themes':['invented']}}]})
        self.assertEqual(invalid.status_code,200)
        self.assertIn('I did not change your general profile',invalid.json['thread']['messages'][-1]['text'])
        self.assertEqual(self.client.get('/api/chat').json['profile']['profile_version'],0)

    def test_relaxed_pace_alias_is_saved_and_message_is_not_rejected(self):
        text='sabah erken kalkmayı sevmem daha relax bir tempo severim'
        result=self.turn({'reply':'Sakin bir tempo ile ilerleyelim.','preferences':[
            {'scope':'profile','evidence':text,'changes':{'pace':'Rahat'}}]},text=text)
        self.assertEqual(result.status_code,200)
        self.assertEqual(result.json['profile']['pace'],'Sakin')
        self.assertEqual(result.json['thread']['messages'][0]['text'],text)
        self.assertEqual(result.json['thread']['messages'][-1]['saved'],['pace'])

    def test_account_and_visitors_are_isolated(self):
        self.turn({'reply':'a'})
        other=self.app.test_client()
        self.assertEqual(other.get('/api/chat').json['thread']['messages'],[])
        self.client.post('/api/auth',json={'username':'chat-test','password':'synthetic-password-123','register':True},headers=self.headers)
        self.assertEqual(self.client.get('/api/chat').json['thread']['messages'],[])
        self.turn({'reply':'hesap'})
        self.client.post('/api/logout',json={},headers=self.headers)
        self.assertEqual(self.client.get('/api/chat').json['thread']['messages'],[])

    def test_clear_has_monotonic_revision(self):
        self.turn({'reply':'a'})
        result=self.client.post('/api/chat/clear',json={'revision':1},headers=self.headers)
        self.assertEqual(result.json['thread']['revision'],2)
        self.assertEqual(result.json['thread']['messages'],[])
        self.assertEqual(self.turn({'reply':'a'},revision=0,tid='new_turn_id').status_code,409)

    def test_plan_is_only_validated_preview_and_phone_action_ignored(self):
        result=self.turn({'reply':'Kontrol edelim','intent':'plan','trip':{'city':'Paris','start':'2099-01-01','days':2,'people':3},'actions':[{'type':'call'}]})
        self.assertEqual(result.json['thread']['messages'][-1]['actions'][0]['type'],'plan')
        self.assertIsNone(self.client.get('/api/me').json['draft'])
        self.assertEqual(self.turn({'reply':'a','intent':'call'},revision=1,tid='second_turn_id').json['thread']['messages'][-1]['actions'],[])

    def test_concurrent_profile_change_rejects_entire_turn(self):
        def model(*args,**kwargs):
            if args[0].startswith('Identify only the language'):
                return {'language': 'English'}
            from flask import g
            import json
            import sqlite3
            from app import profiles
            with closing(sqlite3.connect(self.app.config['DATABASE'])) as connection:
                value=profiles.empty();value['profile_version']=1
                connection.execute('INSERT INTO taste_profiles VALUES (?,?,?)',('visitor:'+g.visitor,1,json.dumps(value)))
                connection.commit()
            return {'reply':'a'}
        with patch('app.providers.llm_json',side_effect=model):
            result=self.client.post('/api/chat',json={'message':'merhaba','turn_id':'concurrent_turn','revision':0},headers=self.headers)
        self.assertEqual(result.status_code,409)
        self.assertEqual(self.client.get('/api/chat').json['thread']['messages'],[])

    def test_task_state_uses_server_route_and_never_model_approval(self):
        import copy
        from test_app import PLAN, TRIP
        plan=copy.deepcopy(PLAN)
        plan['days'][0]['stops'][0].update(phone='+12025550123',country_code='US',timezone='America/New_York')
        with patch('app.planner.generate',return_value=plan):
            self.client.post('/api/plan',json=TRIP,headers=self.headers)
        output={'reply':'Saat kaçta olsun?', 'intent':'reserve', 'task':'reserve',
                'reservation':{'booking_name':'Synthetic Guest','local_time':'19:00',
                               'approved':True,'phone_verified':True}}
        with patch('app.providers.llm_json',return_value=output) as model:
            result=self.client.post('/api/chat',json={'message':'Rezervasyon istiyorum','turn_id':'task_state_test',
                'revision':0,'task_mode':'reserve','stop_id':'food'},headers=self.headers)
        self.assertEqual(result.status_code,200)
        self.assertEqual(result.json['thread']['tasks']['reservation']['stop_id'],'food')
        self.assertNotIn('approved',result.json['thread']['tasks']['reservation'])
        self.assertNotIn('phone_verified',result.json['thread']['tasks']['reservation'])
        self.assertEqual(result.json['thread']['messages'][-1]['actions'][0]['type'],'reserve')
        self.assertIn('Food',model.call_args.args[1])
        import sqlite3
        with closing(sqlite3.connect(self.app.config['DATABASE'])) as connection:
            self.assertEqual(connection.execute('SELECT count(*) FROM reservation_attempts').fetchone()[0],0)

    def test_special_condition_requires_explicit_storage_phrase(self):
        result=self.turn({'reply':'Bu seyahatte dikkate alalım.','preferences':[
            {'scope':'profile','evidence':'Özel bir koşulum var','changes':{'special_requirements':'Synthetic condition'}}]},text='Özel bir koşulum var')
        self.assertEqual(result.json['profile']['special_requirements'],'')
        result=self.turn({'reply':'İnceleyebilirsin.','preferences':[
            {'scope':'profile','evidence':'Özel koşulumu kaydet','changes':{'special_requirements':'Synthetic condition'}}]},text='Özel koşulumu kaydet',revision=1,tid='special_condition_save')
        self.assertEqual(result.json['profile']['special_requirements'],'Synthetic condition')

    def test_new_session_rotates_identity_without_deleting_old_conversation(self):
        self.turn({'reply':'Previous conversation'})
        old_cookie=self.client.get_cookie('tt_visitor').value
        result=self.client.post('/api/session/new',json={},headers=self.headers)
        self.assertEqual(result.status_code,200)
        self.assertNotEqual(old_cookie,self.client.get_cookie('tt_visitor').value)
        self.assertEqual(self.client.get('/api/chat').json['thread']['messages'],[])
        self.assertIsNone(self.client.get('/api/me').json['user'])
        old=self.app.test_client()
        old.set_cookie('tt_visitor',old_cookie)
        self.assertEqual(len(old.get('/api/chat').json['thread']['messages']),2)
