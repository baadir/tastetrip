import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import requests
from app.voice_demo_calls import DemoCalls

class DemoCallTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        values={"TWILIO_TEST_TO_NUMBER":"+12025550101","TWILIO_FROM_NUMBER":"+12025550102","VOICE_PUBLIC_URL":"https://voice.example.test"}
        self.calls=DemoCalls(lambda key:values.get(key,"configured"),Path(self.temp.name)/"calls.sqlite")
        self.session=Mock();self.calls.session=lambda:self.session
        self.session.post.return_value=Mock(status_code=201,json=lambda:{"sid":"CAtest","status":"queued"})
    def test_same_attempt_does_not_call_twice(self):
        first=self.calls.start("test-attempt-0001")
        second=self.calls.start("test-attempt-0001")
        self.assertEqual(first,second);self.session.post.assert_called_once()
    def test_other_attempt_blocked_while_active(self):
        self.calls.start("test-attempt-0001")
        with self.assertRaises(ValueError):self.calls.start("test-attempt-0002")
        self.session.post.assert_called_once()
    def test_lost_response_persists_unknown_across_restart(self):
        self.session.post.side_effect=requests.Timeout()
        self.assertEqual(self.calls.start("test-attempt-0001")["status"],"unknown")
        again=DemoCalls(self.calls.value,self.calls.path)
        with self.assertRaises(ValueError):again.start("test-attempt-0002")
    def test_terminal_status_allows_next_explicit_attempt(self):
        self.calls.start("test-attempt-0001")
        self.session.get.return_value=Mock(ok=True,json=lambda:{"status":"completed"})
        self.assertEqual(self.calls.latest()["status"],"completed")
        self.calls.start("test-attempt-0002");self.assertEqual(self.session.post.call_count,2)
    def test_only_configured_target_and_bounded_demo_sent(self):
        result=self.calls.start("test-attempt-0001")
        data=self.session.post.call_args.kwargs["data"]
        self.assertEqual(data["To"],"+12025550101")
        self.assertEqual(data["TimeLimit"],180)
        self.assertEqual(data["Record"],"false")
        self.assertIn('restaurant_demo',data["Twiml"])
        self.assertNotIn("sid",result)

    def test_anna_scenario_has_separate_fixed_target_and_stream_mode(self):
        self.calls.start("anna-attempt-0001", "anna_restaurant")
        data=self.session.post.call_args.kwargs["data"]
        self.assertEqual(data["To"], "+35312984145")
        self.assertIn('value="anna_restaurant"',data["Twiml"])
    def test_unknown_scenario_never_calls_provider(self):
        with self.assertRaises(ValueError):self.calls.start("test-attempt-0001", "other")
        self.session.post.assert_not_called()

    def test_provider_rejection_code_is_saved_and_exposed_without_credentials(self):
        self.session.post.return_value=Mock(status_code=400,json=lambda:{"code":21215,"message":"sensitive provider details"})
        result=self.calls.start("test-attempt-0001")
        self.assertEqual(result["error_code"],21215)
        self.assertEqual(result["http_status"],400)
        self.assertEqual(self.calls.latest()["error_code"],21215)
        self.assertNotIn("message",result)
