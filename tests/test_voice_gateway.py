import unittest
from aiohttp.test_utils import TestClient, TestServer
from twilio.request_validator import RequestValidator
from app.voice_gateway import create_gateway


class VoiceGatewayTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.origin = "https://voice.example.test"
        self.client = TestClient(TestServer(create_gateway({"VOICE_PUBLIC_URL": self.origin, "TWILIO_AUTH_TOKEN": "test-secret", "TWILIO_ACCOUNT_SID": "ACtest", "DEEPGRAM_API_KEY": "fake", "VOICE_MONITOR_TOKEN": "monitor-secret"})))
        await self.client.start_server()

    async def asyncTearDown(self):
        await self.client.close()

    async def test_health_has_no_configuration(self):
        r = await self.client.get("/health")
        self.assertEqual(await r.json(), {"ok": True})

    async def test_transcript_requires_token(self):
        self.assertEqual((await self.client.get("/internal/transcript")).status, 403)
        r = await self.client.get("/internal/transcript", headers={"Authorization": "Bearer monitor-secret"})
        self.assertEqual((await r.json())["events"], [])

    async def test_unsigned_media_rejected(self):
        self.assertEqual((await self.client.get("/twilio/media")).status, 403)

    async def test_host_spoof_does_not_override_signature_origin(self):
        signature = RequestValidator("test-secret").compute_signature("https://attacker.test/twilio/media", {})
        r = await self.client.get("/twilio/media", headers={"X-Twilio-Signature": signature, "X-Forwarded-Host": "attacker.test"})
        self.assertEqual(r.status, 403)

    async def test_signed_wrong_account_closes_before_deepgram(self):
        signature = RequestValidator("test-secret").compute_signature(self.origin.replace("https://", "wss://") + "/twilio/media", {})
        ws = await self.client.ws_connect("/twilio/media", headers={"X-Twilio-Signature": signature})
        await ws.send_json({"event": "start", "start": {"accountSid": "wrong"}})
        await ws.receive()
        self.assertEqual(ws.close_code, 1008)
        await ws.close()

    async def test_signed_trailing_slash_handshake(self):
        signature = RequestValidator("test-secret").compute_signature(self.origin.replace("https://", "wss://") + "/twilio/media/", {})
        ws = await self.client.ws_connect("/twilio/media", headers={"X-Twilio-Signature": signature})
        await ws.send_json({"event": "start", "start": {"accountSid": "wrong"}})
        await ws.receive()
        self.assertEqual(ws.close_code, 1008)
        await ws.close()

    async def test_https_signature_is_not_websocket_signature(self):
        signature = RequestValidator("test-secret").compute_signature(self.origin + "/twilio/media", {})
        r = await self.client.get("/twilio/media", headers={"X-Twilio-Signature": signature})
        self.assertEqual(r.status, 403)

    async def test_wss_signature_for_other_host_rejected(self):
        signature = RequestValidator("test-secret").compute_signature("wss://attacker.test/twilio/media", {})
        r = await self.client.get("/twilio/media", headers={"X-Twilio-Signature": signature, "Host": "attacker.test"})
        self.assertEqual(r.status, 403)
