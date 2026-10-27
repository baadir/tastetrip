import asyncio
import json
import unittest
from collections import deque
from aiohttp import web,WSMsgType
from aiohttp.test_utils import TestClient,TestServer
from app.reservation_bridge import ReservationBridge
from app.reservations import listen_token

class Reply:
    status=200
    def __init__(self,data=None):self.data=data or {}
    async def __aenter__(self):return self
    async def __aexit__(self,*args):return False
    async def json(self):return self.data
    async def read(self):return b''
class FakeInternalClient:
    def __init__(self):self.events=[]
    def get(self,*args,**kwargs):return Reply({'terms':{'conversation_language':'en'}})
    def post(self,*args,**kwargs):self.events.append(kwargs['json']);return Reply()

class ReservationBridgeTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.settings={'VOICE_MONITOR_TOKEN':'test-secret','APP_ORIGIN':'https://app.example.test'}
        self.state={'active':False}
        self.bridge=ReservationBridge(lambda k:self.settings.get(k,'present'),self.state)
        app=web.Application();self.bridge.routes(app);self.client=TestClient(TestServer(app));await self.client.start_server()
    async def asyncTearDown(self):await self.client.close()
    async def connect(self,attempt='synthetic-attempt-id-123',token=None):
        ws=await self.client.ws_connect('/reservations/listen/'+attempt,headers={'Origin':'https://app.example.test'})
        await ws.send_json({'token':token or listen_token('test-secret',attempt)})
        return ws

    async def test_ready_and_dial_lease_require_shared_secret(self):
        self.assertEqual((await self.client.get('/internal/reservations/ready')).status,403)
        headers={'Authorization':'Bearer test-secret'}
        claim=await self.client.post('/internal/reservations/claim',json={'attempt':'synthetic-attempt-id-123'},headers=headers)
        self.assertEqual(claim.status,200)
        self.assertFalse((await (await self.client.get('/internal/reservations/ready',headers=headers)).json())['ready'])
        self.assertEqual((await self.client.post('/internal/reservations/claim',json={'attempt':'other-attempt-id-123'},headers=headers)).status,409)
        await self.client.post('/internal/reservations/release',json={'attempt':'synthetic-attempt-id-123'},headers=headers)
        self.assertTrue((await (await self.client.get('/internal/reservations/ready',headers=headers)).json())['ready'])

    async def test_audio_is_attempt_scoped_and_transcript_persists_once(self):
        attempt='synthetic-attempt-id-123';ws=await self.connect(attempt)
        self.assertEqual((await ws.receive_json())['type'],'connection')
        client=FakeInternalClient();terms,publish,finish=await self.bridge.session(client,attempt,'CAtest')
        publish({'type':'audio','role':'restaurant','payload':'////'})
        self.assertEqual((await ws.receive_json())['payload'],'////')
        publish({'type':'audio','role':'assistant','payload':'aaaa'})
        self.assertEqual((await ws.receive_json())['role'],'assistant')
        publish({'type':'transcript','role':'restaurant','text':'Synthetic fixture','final':True})
        self.assertEqual((await ws.receive_json())['type'],'transcript')
        await finish()
        texts=[e for e in client.events if e.get('role')=='restaurant']
        self.assertEqual(len(texts),1);self.assertNotIn('payload',json.dumps(client.events))
        await ws.close()

    async def test_wrong_attempt_and_replayed_token_are_denied(self):
        token=listen_token('test-secret','synthetic-attempt-id-123')
        wrong=await self.connect('other-attempt-id-123',token)
        self.assertEqual((await wrong.receive()).type,WSMsgType.CLOSE)
        valid=await self.connect(token=token);await valid.receive_json()
        replay=await self.connect(token=token)
        self.assertEqual((await replay.receive()).type,WSMsgType.CLOSE)
        await valid.close()

    async def test_wrong_origin_cannot_listen(self):
        from aiohttp import WSServerHandshakeError
        with self.assertRaises(WSServerHandshakeError):
            await self.client.ws_connect('/reservations/listen/synthetic-attempt-id-123',headers={'Origin':'https://foreign.example'})

if __name__=='__main__':unittest.main()
