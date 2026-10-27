import unittest
from aiohttp.test_utils import TestClient, TestServer
from app.voice_gateway import create_gateway

class MonitorTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client=TestClient(TestServer(create_gateway({"VOICE_PUBLIC_URL":"https://voice.example.test"})))
        await self.client.start_server()
        self.headers={"Host":"localhost:8081", "Origin":"http://localhost:8081"}
    async def asyncTearDown(self): await self.client.close()
    async def test_public_host_cannot_read_monitor_or_create_ticket(self):
        self.assertEqual((await self.client.get("/monitor")).status,403)
        self.assertEqual((await self.client.post("/monitor-session")).status,403)
    async def test_proxy_cannot_access_local_monitor(self):
        r=await self.client.get("/monitor",headers={**self.headers,"CF-Ray":"proxy-test"})
        self.assertEqual(r.status,403)
    async def test_local_page_and_assets(self):
        self.assertEqual((await self.client.get("/monitor",headers=self.headers)).status,200)
        self.assertEqual((await self.client.get("/monitor-assets/.env",headers=self.headers)).status,404)
    async def test_ticket_one_use_and_state_snapshot(self):
        r=await self.client.post("/monitor-session",headers=self.headers)
        token=(await r.json())["token"]
        ws=await self.client.ws_connect("/monitor-ws",headers=self.headers)
        await ws.send_json({"token":token})
        m=await ws.receive_json();self.assertEqual(m["type"],"state")
        self.assertNotIn("token",m["data"])
        await ws.close()
        ws=await self.client.ws_connect("/monitor-ws",headers=self.headers)
        await ws.send_json({"token":token});await ws.receive();self.assertEqual(ws.close_code,1008)
        await ws.close()

    async def test_remote_cannot_trigger_call(self):
        r=await self.client.post("/monitor-call",json={"attempt_id":"test-attempt-0001"})
        self.assertEqual(r.status,403)
    async def test_other_origin_cannot_trigger_call(self):
        r=await self.client.post("/monitor-call",headers={"Host":"localhost:8081","Origin":"https://attacker.test"},json={"attempt_id":"test-attempt-0001"})
        self.assertEqual(r.status,403)
