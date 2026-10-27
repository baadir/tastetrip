import unittest
from app.voice_silence import SilenceGuard, has_voice

class SilenceTests(unittest.TestCase):
    def test_probe_once_then_ten_second_hangup(self):
        g=SilenceGuard(0)
        self.assertIsNone(g.tick(3.9))
        self.assertEqual(g.tick(4),"check")
        self.assertIsNone(g.tick(8))
        self.assertEqual(g.tick(10),"hangup")
    def test_incoming_voice_resets_timer_and_probe(self):
        g=SilenceGuard(0);g.tick(4);g.heard(9)
        self.assertIsNone(g.tick(10))
        self.assertEqual(g.tick(13),"check")
    def test_own_normal_speech_not_counted_as_remote_silence(self):
        g=SilenceGuard(0)
        self.assertIsNone(g.tick(20,True))
        self.assertIsNone(g.tick(23))
        self.assertEqual(g.tick(24),"check")
    def test_mulaw_silence_vs_speech_activity(self):
        self.assertFalse(has_voice(b'\xff'*160))
        self.assertFalse(has_voice(b'\x7f'*160))
        self.assertTrue(has_voice(b'\x80'*160))
        self.assertFalse(has_voice(b''))
