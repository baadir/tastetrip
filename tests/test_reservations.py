import copy
import json
import os
import tempfile
import time
import unittest
from datetime import date,timedelta
from unittest.mock import patch,Mock
from app.server import create_app
from app.reservations import checked_terms,listen_token,verify_listen_token
from app.reservation_worker import ReservationWorker
from app.reservation_bridge import reservation_scenario
from test_app import PLAN,TRIP

KEY='synthetic-idempotency-1234'
SYNTHETIC_SID='CA'+'a'*32
ENV={k:'synthetic-value' for k in ('TWILIO_ACCOUNT_SID','TWILIO_AUTH_TOKEN','VOICE_MONITOR_TOKEN','DEEPGRAM_API_KEY','ELEVENLABS_API_KEY','ELEVENLABS_VOICE_ID','LLM_API_KEY','LLM_MODEL','LLM_BASE_URL')}
ENV.update(TWILIO_FROM_NUMBER='+12025550124',VOICE_PUBLIC_URL='https://voice.example.test')

class ReservationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.app=create_app({'TESTING':True,'DATA_DIR':self.temp.name});self.client=self.app.test_client();self.headers={'X-TasteTrip':'1'}
        self.gateway=patch('app.reservation_worker.requests.post',return_value=Mock(ok=True));self.gateway.start()
        self.env=patch.dict(os.environ,ENV);self.env.start()
        self.post('auth',{'username':'synthetic-user','password':'synthetic-password-123','register':True})
        self.plan=copy.deepcopy(PLAN);self.food=self.plan['days'][0]['stops'][0]
        self.food.update(phone='+12025550123',country_code='US',address='Synthetic fixture address',map_url='https://example.test/map')
        with patch('app.planner.generate',return_value=self.plan):self.post('plan',TRIP)
        self.store=self.app.extensions['reservations']
        with self.store.db() as db:db.execute('INSERT OR REPLACE INTO reservation_worker_heartbeat VALUES (1,?,1)',(time.time(),))
        self.input={'plan_id':'plan-1','revision':1,'stop_id':'food','country_code':'US','timezone':'America/New_York','local_date':(date.today()+timedelta(days=35)).isoformat(),'local_time':'19:00','people':3,'booking_name':'Synthetic Guest','native_language':'tr','conversation_language':'en','phone_verified':True,'timezone_verified':True,'notes':''}

    def tearDown(self):self.gateway.stop();self.env.stop();self.temp.cleanup()
    def post(self,path,data,client=None):return (client or self.client).post('/api/'+path,json=data,headers=self.headers)
    def prepare(self,**changes):return self.post('reservations/prepare',{**self.input,**changes})
    def enqueue(self,**extra):
        req=self.prepare().json
        response=self.post('reservations/'+req['request_id']+'/start',{'digest':req['digest'],'approved':True,'idempotency_key':KEY,**extra})
        self.assertEqual(response.status_code,202,response.json)
        return req,response.json['reservation']
    def worker(self):return ReservationWorker(self.app.config['DATABASE'],lambda k:ENV.get(k,''))

    def test_prepare_has_no_call_and_uses_server_phone(self):
        with patch('requests.Session.post') as paid:
            response=self.prepare(phone='+442079460000')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['terms']['phone'],'+12025550123');paid.assert_not_called()
        self.assertEqual(self.client.get('/api/reservations').json['reservations'],[])
        self.assertEqual(self.client.get('/api/plans').json['plans'][0]['id'],'plan-1')

    def test_login_source_zone_and_category_gates(self):
        self.assertEqual(self.prepare(phone_verified=False).status_code,400)
        self.assertEqual(self.prepare(timezone_verified=False).status_code,400)
        self.assertEqual(self.prepare(stop_id='museum').status_code,400)
        self.assertEqual(self.prepare(timezone='Wrong/Zone').status_code,400)
        self.assertEqual(self.prepare(country_code='ZZ').status_code,400)
        self.assertEqual(self.prepare(conversation_language='xx').status_code,400)
        self.assertEqual(self.post('reservations/prepare',self.input,client=self.app.test_client()).status_code,401)

    def test_dst_missing_and_ambiguous_local_times_rejected(self):
        future=date.today().year+1
        # US DST: second Sunday in March, first Sunday in November.
        from datetime import datetime
        march=date(future,3,1);spring=march+timedelta(days=(6-march.weekday())%7+7)
        november=date(future,11,1);fall=november+timedelta(days=(6-november.weekday())%7)
        self.assertEqual(self.prepare(local_date=str(spring),local_time='02:30').status_code,400)
        self.assertEqual(self.prepare(local_date=str(fall),local_time='01:30').status_code,400)

    def test_review_digest_stale_route_and_worker_required(self):
        req=self.prepare().json
        base={'approved':True,'digest':req['digest'],'idempotency_key':KEY}
        self.assertEqual(self.post('reservations/'+req['request_id']+'/start',{**base,'digest':'wrong'}).status_code,400)
        self.assertEqual(self.post('reservations/'+req['request_id']+'/start',{**base,'approved':False}).status_code,400)
        with self.store.db() as db:db.execute('DELETE FROM reservation_worker_heartbeat')
        self.assertEqual(self.post('reservations/'+req['request_id']+'/start',base).status_code,503)
        self.assertEqual(self.prepare(revision=99).status_code,409)

    def test_start_duplicate_and_unknown_no_redial(self):
        req,attempt=self.enqueue()
        with patch('requests.Session.post') as paid:
            response=self.post('reservations/'+req['request_id']+'/start',{'digest':req['digest'],'approved':True,'idempotency_key':KEY})
        self.assertEqual(response.json['reservation']['id'],attempt['id']);paid.assert_not_called()
        self.store.update(attempt['id'],status='unknown')
        second=self.prepare().json
        self.assertEqual(self.post('reservations/'+second['request_id']+'/start',{'approved':True,'digest':second['digest'],'idempotency_key':'another-synthetic-key-12'}).status_code,400)

    def test_expired_review_cannot_dial_but_existing_attempt_remains_idempotent(self):
        req=self.prepare().json
        with self.store.db() as db:db.execute('UPDATE reservation_requests SET expires=? WHERE id=?',(time.time()-1,req['request_id']))
        response=self.post('reservations/'+req['request_id']+'/start',{'approved':True,'digest':req['digest'],'idempotency_key':KEY})
        self.assertEqual(response.status_code,409)
        req,a=self.enqueue()
        with self.store.db() as db:db.execute('UPDATE reservation_requests SET expires=? WHERE id=?',(time.time()-1,req['request_id']))
        duplicate=self.post('reservations/'+req['request_id']+'/start',{'approved':True,'digest':req['digest'],'idempotency_key':KEY})
        self.assertEqual(duplicate.json['reservation']['id'],a['id'])

    def test_owner_scoped_status_stop_summary_listen(self):
        req,attempt=self.enqueue();other=self.app.test_client()
        self.post('auth',{'username':'another-user','password':'synthetic-password-123','register':True},other)
        self.assertEqual(other.get('/api/reservations/'+attempt['id']).status_code,404)
        for action in ('stop','listen-token','summary/retry'):
            self.assertEqual(self.post('reservations/'+attempt['id']+'/'+action,{},other).status_code,404)

    def test_stop_before_dispatch_cancels_outbox(self):
        req,attempt=self.enqueue()
        result=self.post('reservations/'+attempt['id']+'/stop',{}).json['reservation']
        self.assertEqual(result['status'],'canceled')
        worker=self.worker()
        try:self.assertIsNone(worker.claim())
        finally:worker.pool.shutdown()

    def test_failed_retry_requires_explicit_previous_id(self):
        req,attempt=self.enqueue();self.store.update(attempt['id'],status='rejected',result='not_completed')
        next_req=self.prepare().json;data={'approved':True,'digest':next_req['digest'],'idempotency_key':'second-synthetic-key-12'}
        self.assertEqual(self.post('reservations/'+next_req['request_id']+'/start',data).status_code,400)
        self.assertEqual(self.post('reservations/'+next_req['request_id']+'/start',{**data,'retry_of':attempt['id']}).status_code,202)

    def test_summary_does_not_confirm_and_review_requires_restaurant_evidence(self):
        req,attempt=self.enqueue();self.store.update(attempt['id'],status='ended',result='unknown',summary=json.dumps({'text':'A generated claim is not proof'}),summary_status='ready')
        data={'digest':req['digest'],'heard_acceptance':True,'event_id':'assistant-123456'}
        self.store.event(attempt['id'],{'event_id':data['event_id'],'role':'assistant','text':'I think this is booked.'})
        self.assertEqual(self.post('reservations/'+attempt['id']+'/review-result',data).status_code,400)
        self.store.event(attempt['id'],{'event_id':'restaurant-123456','role':'restaurant','text':'Yes, the requested reservation is confirmed.'})
        response=self.post('reservations/'+attempt['id']+'/review-result',{**data,'event_id':'restaurant-123456'})
        self.assertEqual(response.json['reservation']['result'],'confirmed')
        self.assertEqual(self.client.get('/api/me').json['draft']['days'][0]['stops'][0]['reservation_status'],'confirmed')
        with patch('app.planner.llm_json',return_value={'days':[{'stop_ids':[]},{'stop_ids':['food','museum']}] }):
            self.assertEqual(self.post('revise',{'revision':1,'instruction':'Move food to second day'}).status_code,400)

    def test_internal_sid_binding_requires_secret_and_matching_call(self):
        req,attempt=self.enqueue();self.store.update(attempt['id'],status='initiating')
        url='/api/internal/reservations/'+attempt['id']+'?sid='+SYNTHETIC_SID
        self.assertEqual(self.client.get(url).status_code,403)
        response=self.client.get(url,headers={'Authorization':'Bearer '+ENV['VOICE_MONITOR_TOKEN']})
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.store.attempt(attempt['id'])['status'],'connected')
        mismatch=self.client.get(url.replace(SYNTHETIC_SID,'CA'+'b'*32),headers={'Authorization':'Bearer '+ENV['VOICE_MONITOR_TOKEN']})
        self.assertEqual(mismatch.status_code,403)

    def test_event_replay_is_deduplicated(self):
        req,a=self.enqueue();event={'event_id':'stable-event-id-123','role':'restaurant','text':'Hello'}
        self.store.event(a['id'],event);self.store.event(a['id'],event)
        self.assertEqual(len(self.store.public(a['id'],a.get('user_id') or self.client.get('/api/me').json['user']['id'])['events']),1)

    def test_worker_claim_and_timeout_never_automatically_post_again(self):
        req,a=self.enqueue();worker=self.worker()
        try:
            attempt=worker.claim();self.assertIsNone(worker.claim())
            model=Mock();model.raise_for_status.return_value=None;model.json.return_value=[{'model_id':'eleven_flash_v2_5','languages':[{'language_id':'en'}]}]
            with patch('app.reservation_worker.requests.get',return_value=model),patch('requests.Session.post',side_effect=__import__('requests').Timeout) as paid:
                worker.dispatch(attempt)
                self.assertEqual(paid.call_count,1)
            self.assertEqual(self.store.attempt(a['id'])['status'],'unknown');self.assertIsNone(worker.claim())
            restarted=self.worker()
            try:self.assertIsNone(restarted.claim())
            finally:restarted.pool.shutdown()
        finally:worker.pool.shutdown()

    def test_live_sid_binding_wins_over_late_create_response(self):
        req,a=self.enqueue();worker=self.worker()
        try:
            attempt=worker.claim();model=Mock();model.raise_for_status.return_value=None;model.json.return_value=[{'model_id':'eleven_flash_v2_5','languages':[{'language_id':'en'}]}]
            def created(*args,**kwargs):
                self.store.update(a['id'],status='connected',sid=SYNTHETIC_SID)
                response=Mock(status_code=201);response.json.return_value={'sid':SYNTHETIC_SID,'status':'queued'};return response
            with patch('app.reservation_worker.requests.get',return_value=model),patch('requests.Session.post',side_effect=created):worker.dispatch(attempt)
            self.assertEqual(self.store.attempt(a['id'])['status'],'connected')
        finally:worker.pool.shutdown()

    def test_stop_unknown_without_sid_does_not_claim_cancellation(self):
        req,a=self.enqueue();self.store.update(a['id'],status='unknown')
        response=self.post('reservations/'+a['id']+'/stop',{})
        self.assertEqual(response.json['reservation']['status'],'unknown')
        self.assertTrue(response.json['reservation']['stop_requested'])

    def test_v3_voice_script_is_prepared_before_the_phone_request(self):
        self.input['conversation_language']='af'
        req,a=self.enqueue();worker=self.worker()
        try:
            attempt=worker.claim();terms=json.loads(self.store.request(attempt['request_id'])['body'])
            model=Mock();model.raise_for_status.return_value=None;model.json.return_value=[{'model_id':'eleven_v3','languages':[{'language_id':'af'}]}]
            script={'opening':'AI '+terms['booking_name']+' '+terms['local_date']+' '+terms['local_time'], 'disclosure':'AI assistant', 'probe':'Can you hear me?', 'readback':'3 '+terms['booking_name']+' '+terms['local_date']+' '+terms['local_time']}
            response=Mock(status_code=201);response.json.return_value={'sid':SYNTHETIC_SID,'status':'queued'}
            with patch('app.reservation_worker.requests.get',return_value=model),patch('app.reservation_worker.providers.llm_json',return_value=script),patch('requests.Session.post',return_value=response) as paid:
                worker.dispatch(attempt)
            self.assertEqual(paid.call_count,1)
            self.assertIn(script['opening'],json.loads(self.store.attempt(a['id'])['script'])['opening'])
        finally:worker.pool.shutdown()

    def test_provider_reconciliation_cannot_overwrite_new_restaurant_confirmation(self):
        req,a=self.enqueue();self.store.update(a['id'],status='connected',sid=SYNTHETIC_SID)
        old=self.store.attempt(a['id']);worker=self.worker()
        def provider_response(*args,**kwargs):
            self.store.update(a['id'],result='confirmed',confirmation_source='restaurant_exact_reply')
            response=Mock(ok=True);response.json.return_value={'status':'completed'};return response
        try:
            with patch('requests.Session.get',side_effect=provider_response):worker.reconcile(old)
            self.assertEqual(self.store.attempt(a['id'])['status'],'ended')
            self.assertEqual(self.store.attempt(a['id'])['result'],'confirmed')
        finally:worker.pool.shutdown()

    def test_model_gate_prevents_phone_post(self):
        req,a=self.enqueue();worker=self.worker()
        try:
            attempt=worker.claim();model=Mock();model.raise_for_status.return_value=None;model.json.return_value=[]
            with patch('app.reservation_worker.requests.get',return_value=model),patch('requests.Session.post') as paid:worker.dispatch(attempt)
            paid.assert_not_called();self.assertEqual(self.store.attempt(a['id'])['status'],'failed')
        finally:worker.pool.shutdown()

    def test_late_transcript_invalidates_generated_summary(self):
        req,a=self.enqueue();self.store.update(a['id'],status='ended',result='unknown')
        self.store.event(a['id'],{'event_id':'first-event-1234','role':'restaurant','text':'First sentence'})
        worker=self.worker()
        try:
            def late_event(*args,**kwargs):
                self.store.event(a['id'],{'event_id':'late-event-1234','role':'restaurant','text':'Late final sentence'})
                return {'text':'Old summary','evidence_event_ids':['first-event-1234']}
            with patch('app.reservation_worker.providers.llm_json',side_effect=late_event):worker.summarize(self.store.attempt(a['id']))
            self.assertEqual(self.store.attempt(a['id'])['summary_status'],'pending')
            self.assertNotEqual(self.store.attempt(a['id'])['summary_status'],'ready')
        finally:worker.pool.shutdown()

    def test_automatic_confirmation_needs_exact_readback_and_unambiguous_staff_acceptance(self):
        req,a=self.enqueue();self.store.update(a['id'],status='connected')
        terms=json.loads(self.store.request(a['request_id'])['body'])
        readback=reservation_scenario(terms)['readback']
        self.store.event(a['id'],{'event_id':'readback-one-1234','role':'assistant','text':readback,'kind':'readback'})
        self.store.event(a['id'],{'event_id':'availability-1234','role':'restaurant','text':'Yes, we have availability.'})
        self.assertEqual(self.store.attempt(a['id'])['result'],'pending')
        self.store.event(a['id'],{'event_id':'readback-two-1234','role':'assistant','text':readback,'kind':'readback'})
        self.store.event(a['id'],{'event_id':'confirmation-1234','role':'restaurant','text':'Your reservation is confirmed.'})
        self.assertEqual(self.store.attempt(a['id'])['result'],'confirmed')
        self.store.event(a['id'],{'event_id':'correction-1234','role':'restaurant','text':'Sorry, actually we cannot accept that time.'})
        self.assertEqual(self.store.attempt(a['id'])['result'],'unknown')

    def test_staff_confirmation_without_readback_is_not_auto_accepted(self):
        req,a=self.enqueue()
        self.store.event(a['id'],{'event_id':'no-readback-1234','role':'restaurant','text':'Confirmed.'})
        self.assertEqual(self.store.attempt(a['id'])['result'],'pending')

    def test_reference_must_exist_in_selected_restaurant_text(self):
        req,a=self.enqueue();self.store.update(a['id'],status='ended',result='unknown')
        self.store.event(a['id'],{'event_id':'reference-event-1234','role':'restaurant','text':'Confirmed. Reference ABC123.'})
        data={'digest':req['digest'],'heard_acceptance':True,'event_id':'reference-event-1234','reference':'invented'}
        self.assertEqual(self.post('reservations/'+a['id']+'/review-result',data).status_code,400)
        data['reference']='ABC123'
        self.assertEqual(self.post('reservations/'+a['id']+'/review-result',data).json['reservation']['reference'],'ABC123')

    def test_summary_retry_never_enqueues_call(self):
        req,a=self.enqueue();self.store.update(a['id'],status='ended',result='unknown',summary_status='failed')
        self.assertEqual(self.post('reservations/'+a['id']+'/summary/retry',{}).status_code,200)
        with self.store.db() as db:self.assertEqual(db.execute('SELECT COUNT(*) FROM reservation_outbox').fetchone()[0],1)

class VoicePolicyTests(unittest.TestCase):
    def test_listener_token_is_attempt_bound_and_expires(self):
        token=listen_token('secret','attempt-1')
        self.assertTrue(verify_listen_token('secret',token,'attempt-1'))
        self.assertFalse(verify_listen_token('secret',token,'attempt-2'))
        self.assertFalse(verify_listen_token('wrong',token,'attempt-1'))
        with patch('app.reservations.time.time',return_value=time.time()+40):self.assertFalse(verify_listen_token('secret',token,'attempt-1'))

    def test_router_selects_flash_and_v3_with_stt_gate(self):
        from app.voice_languages import model_for
        self.assertEqual(model_for('tr'),'eleven_flash_v2_5')
        self.assertEqual(model_for('en-US'),'eleven_flash_v2_5')
        self.assertEqual(model_for('af'),'eleven_v3')
        with self.assertRaises(ValueError):model_for('xx')

    def test_real_scenario_has_no_test_cancellation_prompt(self):
        terms={'conversation_language':'en','booking_name':'Synthetic Guest','restaurant':'Synthetic Restaurant','local_date':'2027-01-02','local_time':'13:00','people':3,'model':'eleven_flash_v2_5'}
        scenario=reservation_scenario(terms)
        self.assertIn('Synthetic Guest',scenario['opening'])
        self.assertNotIn('experimental test',scenario['system'])
        self.assertIn('REAL restaurant',scenario['system'])
        self.assertIn('exactly',scenario['system'])

if __name__=='__main__':unittest.main()
