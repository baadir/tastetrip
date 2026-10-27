from contextlib import closing
import json
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from app.server import create_app
from app.profiles import OPTIONS
from test_app import TRIP, PLAN

FAVORITE={'id':'12345678-1234-1234-1234-123456789012','name':'Synthetic place','type':'urn:entity:place'}
BOOK={'id':'22345678-1234-1234-1234-123456789012','name':'Synthetic book','type':'urn:entity:book'}

class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.app=create_app({'TESTING':True,'DATA_DIR':self.temp.name})
        self.client=self.app.test_client()
        self.headers={'X-TasteTrip':'1'}
        self.client.get('/api/me')

    def tearDown(self):
        self.temp.cleanup()

    def post(self,path,data,client=None):
        return (client or self.client).post('/api/'+path,json=data,headers=self.headers)

    def profile(self,client=None):
        return (client or self.client).get('/api/profile').json['profile']

    def change(self,changes,version=None,client=None):
        return (client or self.client).patch('/api/profile',json={'changes':changes,'profile_version':self.profile(client)['profile_version'] if version is None else version},headers=self.headers)

    def resolve(self,item,kind):
        with patch('app.providers.resolve_interests',return_value=[item]):
            return self.post('interests/search',{'query':item['name'],'kind':kind})

    def auth(self,name,register=True,client=None):
        return self.post('auth',{'username':name,'password':'synthetic-password-123','register':register},client)

    def test_versioned_guest_profile_and_session_cookie(self):
        first=self.change({'themes':['Kahve'],'persistence':'session'})
        self.assertEqual(first.status_code,200)
        self.assertEqual(self.profile()['themes'],['Kahve'])
        self.assertNotIn('Max-Age',next(c for c in first.headers.getlist('Set-Cookie') if c.startswith('tt_visitor=')))
        self.assertEqual(self.change({'themes':[]},version=0).status_code,409)
        self.assertEqual(self.profile()['themes'],['Kahve'])
        response=self.change({'persistence':'device'})
        self.assertTrue(any('Max-Age=15552000' in c for c in response.headers.getlist('Set-Cookie')))

    @patch('app.providers.qloo',return_value={'tags':[{'id':'urn:tag:genre:place:restaurant:thai','name':'Thai'}, {'id':'urn:tag:genre:media:thai','name':'Wrong domain'}]})
    @patch('app.providers.llm_json',return_value={'term':'Thai'})
    def test_dynamic_cuisine_is_real_and_domain_scoped(self,model,qloo):
        response=self.post('profile/cuisines',{'query':'Tayland mutfağı'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json['results']),1)
        thai=response.json['results'][0]['id']
        self.assertEqual(self.change({'cuisines':[thai]}).status_code,200)
        options=self.client.get('/api/profile').json['options']['cuisines']
        self.assertIn(thai,[x['id'] for x in options])
        self.assertEqual(self.change({'cuisines':['urn:tag:genre:media:thai']}).status_code,400)

    def test_account_switch_clears_previous_device_draft(self):
        self.auth('first')
        with patch('app.planner.generate',return_value=PLAN):
            self.post('plan',TRIP)
        self.auth('second')
        self.assertIsNone(self.client.get('/api/me').json['draft'])
        self.assertEqual(self.profile()['profile_version'],0)

    @patch('app.providers.media_candidates',side_effect=__import__('app.providers',fromlist=['ProviderError']).ProviderError('Upstream unavailable'))
    @patch('app.planner.generate',return_value=PLAN)
    def test_media_failure_keeps_master_version_and_draft(self,generate,media):
        self.resolve(BOOK,'book');self.post('plan',TRIP)
        response=self.post('recommend',{'kind':'book','stop_id':'museum','tastes':[BOOK],'remember_profile':True,'profile_version':0})
        self.assertEqual(response.status_code,503)
        self.assertEqual(self.profile()['profile_version'],0)
        self.assertEqual(self.client.get('/api/me').json['draft']['id'],'plan-1')

    def test_profile_csrf_applies_to_patch(self):
        self.assertEqual(self.client.patch('/api/profile',json={'changes':{}}).status_code,403)
        response=self.client.patch('/api/profile',json={},headers={**self.headers,'Origin':'https://foreign.example'})
        self.assertEqual(response.status_code,403)

    def test_fabricated_or_wrong_type_preferences_rejected(self):
        self.assertEqual(self.change({'favorites':[{'id':FAVORITE['id'],'name':'Forged'}]}).status_code,400)
        self.assertEqual(self.resolve(BOOK,'book').status_code,200)
        self.assertEqual(self.change({'content':{'movie':{'tastes':[BOOK]}}}).status_code,400)
        self.assertEqual(self.change({'cuisines':['invented']} ).status_code,400)
        self.assertEqual(self.change({'owner':'another-user'}).status_code,400)

    def test_server_canonical_labels_and_no_cross_device_guest_leak(self):
        self.resolve(FAVORITE,'place')
        response=self.change({'favorites':[{**FAVORITE,'name':'Forged label'}]})
        self.assertEqual(response.json['profile']['favorites'][0]['name'],FAVORITE['name'])
        other=self.app.test_client()
        self.assertEqual(self.profile(other)['favorites'],[])

    def test_account_import_is_explicit_versioned_and_field_scoped(self):
        self.change({'themes':['Kahve'],'budget':2})
        self.auth('traveler')
        self.assertEqual(self.profile()['themes'],[])
        data=self.client.get('/api/profile').json
        self.assertEqual(data['import_candidate']['themes'],['Kahve'])
        response=self.post('profile/import',{'fields':['themes'],'profile_version':0,'anonymous_version':1})
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.profile()['themes'],['Kahve'])
        self.assertEqual(self.profile()['budget'],4)
        self.assertIsNone(self.client.get('/api/profile').json['import_candidate'])
        second=self.app.test_client();self.auth('traveler',False,second)
        self.assertEqual(self.profile(second)['themes'],['Kahve'])

    def test_logout_does_not_expose_account_to_next_user(self):
        self.auth('first');self.change({'themes':['Kahve']})
        self.post('logout',{})
        self.assertEqual(self.profile()['themes'],[])
        self.auth('second')
        self.assertIsNone(self.client.get('/api/profile').json['import_candidate'])
        self.assertEqual(self.profile()['themes'],[])

    def test_concurrent_import_rejected(self):
        self.change({'themes':['Kahve']});self.auth('traveler')
        response=self.post('profile/import',{'fields':['themes'],'profile_version':0,'anonymous_version':99})
        self.assertEqual(response.status_code,409)
        self.assertEqual(self.profile()['themes'],[])

    @patch('app.planner.generate',return_value=PLAN)
    def test_plan_uses_current_master_and_trip_override(self,generate):
        self.resolve(FAVORITE,'place')
        self.change({'favorites':[FAVORITE],'dietary':[OPTIONS['dietary'][0]['id']],'budget':2})
        self.assertEqual(self.post('plan',{**TRIP,'budget':3}).status_code,200)
        sent=generate.call_args.args[0]
        self.assertEqual(sent['budget'],3)
        self.assertIn(FAVORITE['id'],sent['taste_context']['entities'])
        self.assertEqual(sent['taste_context']['required_tags'],[OPTIONS['dietary'][0]['id']])
        self.assertEqual(sent['profile_version'],1)
        self.assertEqual(self.profile()['budget'],2)

    @patch('app.providers.media_candidates',return_value=[])
    @patch('app.planner.generate',return_value=PLAN)
    def test_media_reads_saved_content_without_leaking_food_tags(self,generate,media):
        self.resolve(BOOK,'book')
        self.change({'dietary':[OPTIONS['dietary'][0]['id']], 'content':{'book':{'tastes':[BOOK],'language':'en'}}})
        self.post('plan',TRIP)
        self.assertEqual(self.post('recommend',{'kind':'book','stop_id':'museum'}).status_code,200)
        self.assertIn(BOOK['id'],media.call_args.args[1])
        self.assertNotIn(OPTIONS['dietary'][0]['id'],str(media.call_args))
        self.assertEqual(media.call_args.kwargs['take'],20)

    @patch('app.providers.media_candidates',return_value=[])
    @patch('app.planner.generate',return_value=PLAN)
    def test_one_off_recommendation_does_not_overwrite_master(self,generate,media):
        self.resolve(BOOK,'book');self.post('plan',TRIP)
        request={'kind':'book','stop_id':'museum','tastes':[BOOK],'language':'tr'}
        self.assertEqual(self.post('recommend',request).status_code,200)
        self.assertEqual(self.profile()['content'],{})
        self.assertEqual(self.post('recommend',{**request,'remember_profile':True,'profile_version':0}).status_code,200)
        self.assertEqual(self.profile()['content']['book']['language'],'tr')
        self.assertEqual(self.post('recommend',{**request,'remember_profile':True,'profile_version':0}).status_code,409)

    @patch('app.planner.generate',return_value=PLAN)
    def test_reset_does_not_remove_route(self,generate):
        self.change({'themes':['Kahve']});self.post('plan',TRIP)
        response=self.post('profile/reset',{'profile_version':1})
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.profile()['themes'],[])
        self.assertEqual(self.client.get('/api/me').json['draft']['id'],'plan-1')

    def test_legacy_media_preserved_for_review_not_sent_as_verified(self):
        me=self.client.get('/api/me');visitor=self.client.get_cookie('tt_visitor').value
        import hashlib
        with closing(sqlite3.connect(self.app.config['DATABASE'])) as db, db:
            db.execute('INSERT INTO media_preferences VALUES (?,?)',(hashlib.sha256(visitor.encode()).hexdigest(),json.dumps({'book':[BOOK]})))
        self.assertEqual(self.profile()['legacy_pending']['book'][0]['id'],BOOK['id'])
        self.assertEqual(self.profile()['content'],{})
        self.change({'themes':['Kahve']})
        self.assertEqual(self.profile()['legacy_pending']['book'][0]['id'],BOOK['id'])

class ProfileQueryTests(unittest.TestCase):
    @patch('app.providers.qloo',return_value={'entities':[]})
    def test_only_food_queries_receive_food_constraints(self,qloo):
        from app.providers import place_candidates
        context={'tags':['urn:tag:ambience:qloo:quiet'],'required_tags':[OPTIONS['dietary'][0]['id']],'excluded':[FAVORITE['id']]}
        place_candidates('Paris','restaurant',taste_context=context)
        query=qloo.call_args.args[1]
        self.assertEqual(query['operator.filter.tags'],'intersection')
        self.assertEqual(query['filter.exclude.entities'],FAVORITE['id'])
        place_candidates('Paris','museum',taste_context=context)
        self.assertNotIn('signal.interests.tags',qloo.call_args.args[1])
        self.assertNotIn(OPTIONS['dietary'][0]['id'],str(qloo.call_args.args[1]))

    @patch('app.providers.qloo')
    def test_provider_does_not_silently_return_noncompliant_food(self,qloo):
        from app.providers import place_candidates
        qloo.return_value={'entities':[{'entity_id':FAVORITE['id'],'name':'Fixture','properties':{'primary_genre':{'id':'urn:tag:category:place:restaurant'}},'tags':[]}]}
        self.assertEqual(place_candidates('Paris','restaurant',taste_context={'required_tags':[OPTIONS['dietary'][0]['id']]}),[])

if __name__=='__main__':
    unittest.main()
