import unittest
from datetime import date, timedelta
from app import chat_tasks, profiles

STOP = {'id':'known-stop','name':'Synthetic restaurant','category':'restaurant',
        'phone':'+12025550123','country_code':'US','timezone':'America/New_York'}
PLAN = {'trip':{'people':3},'days':[{'number':1,'date':str(date.today()+timedelta(days=3)), 'stops':[STOP]}]}

class ConversationalTaskTests(unittest.TestCase):
    def context(self, mode='reserve'):
        return chat_tasks.task_context({}, {'task_mode':mode,'stop_id':STOP['id']}, PLAN, profiles.empty())

    def test_reservation_collects_defaults_but_not_name_time_or_authority(self):
        tasks, stops = self.context()
        r = tasks['reservation']
        self.assertEqual(r['people'],3)
        self.assertEqual(r['timezone'],'America/New_York')
        self.assertNotIn('booking_name',r)
        self.assertNotIn('local_time',r)
        self.assertEqual(chat_tasks.resolve({'intent':'reserve'},tasks,stops)[1],[])
        tasks, actions = chat_tasks.resolve({'intent':'reserve','reservation':{'booking_name':'Synthetic Guest',
            'local_time':'19:00','phone_verified':True,'timezone_verified':True,'approved':True,'digest':'invented'}},tasks,stops)
        self.assertEqual(actions[0]['type'],'reserve')
        self.assertFalse(set(tasks['reservation']) & {'phone_verified','timezone_verified','approved','digest'})

    def test_unknown_stop_cannot_create_reservation_or_media_action(self):
        tasks,stops=self.context()
        tasks,actions=chat_tasks.resolve({'intent':'reserve','reservation':{'stop_id':'unknown','booking_name':'Guest','local_time':'19:00'}},tasks,stops)
        self.assertEqual(tasks['reservation']['stop_id'],'known-stop')
        self.assertEqual(actions,[])
        empty,stops=chat_tasks.task_context({}, {'task_mode':'reserve','stop_id':'unknown'}, PLAN, profiles.empty())
        self.assertNotEqual(empty['task'],'reserve')

    def test_flight_dates_and_types_are_checked(self):
        base={'task':'flights','flight':{},'reservation':{},'media':{}}
        output={'intent':'flights','flight':{'origin_query':'Istanbul','destination_query':'Paris','departure':'2099-01-01','return':None}}
        tasks,actions=chat_tasks.resolve(output,base,{})
        self.assertEqual(actions[0]['type'],'flights')
        self.assertEqual(chat_tasks.resolve({'intent':'flights','flight':{'departure':'2000-01-01'}},tasks,{})[1],[])
        self.assertEqual(chat_tasks.resolve({'intent':'flights','flight':{'return':'2098-01-01'}},tasks,{})[1],[])

    def test_media_is_scoped_to_selected_stop_without_invented_ids(self):
        tasks,stops=self.context('media')
        tasks,actions=chat_tasks.resolve({'intent':'media','media':{'kind':'podcast','query':'science','language':'en','tastes':[{'id':'fake'}]}},tasks,stops)
        self.assertEqual(actions[0]['draft']['stop_id'],'known-stop')
        self.assertNotIn('tastes',tasks['media'])
        self.assertEqual(chat_tasks.resolve({'intent':'media','media':{'kind':'invalid'}},tasks,stops)[1],[])

    def test_task_switch_preserves_drafts_and_no_phone_action_exists(self):
        tasks,stops=self.context()
        tasks,actions=chat_tasks.resolve({'task':'chat','intent':'call','reservation':{'booking_name':'Guest','local_time':'19:00'}},tasks,stops)
        self.assertEqual(actions,[])
        self.assertEqual(tasks['task'],'chat')
        self.assertEqual(tasks['reservation']['booking_name'],'Guest')
