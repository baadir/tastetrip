import asyncio
import unittest
from collections import deque
from app.voice_agent import VoiceAgent, DISCLOSURE


class Socket:
    def __init__(self): self.sent = []
    async def send_json(self, message): self.sent.append(message)


class AgentTests(unittest.IsolatedAsyncioTestCase):
    def agent(self):
        return VoiceAgent(None, Socket(), "MZtest", lambda k: "", {"events": deque(maxlen=100)})

    async def test_final_fragments_wait_for_speech_end(self):
        a = self.agent()
        await a.feed("Üç kişi", True, False)
        self.assertTrue(a.queue.empty())
        await a.feed("için yerimiz var", True, True)
        self.assertEqual(await a.queue.get(), "Üç kişi için yerimiz var")
        self.assertFalse(a.pending)

    async def test_interim_is_not_a_user_turn(self):
        a = self.agent()
        await a.feed("Merhaba", False, False)
        self.assertTrue(a.queue.empty())
        self.assertEqual(a.pending, [])

    async def test_interrupt_cancels_generation_and_clears_audio(self):
        a = self.agent()
        a.turn = asyncio.create_task(asyncio.sleep(10))
        a.speaking = True
        await a.feed("Bir saniye", False, False)
        self.assertTrue(a.turn.cancelled())
        self.assertEqual(a.ws.sent[-1]["event"], "clear")
        self.assertFalse(a.speaking)
        self.assertEqual(len(a.history), 1)

    async def test_mark_acknowledges_matching_playback_only(self):
        a = self.agent()
        future = asyncio.get_running_loop().create_future()
        a.marks["expected"] = future
        a.mark("other")
        self.assertFalse(future.done())
        a.mark("expected")
        self.assertTrue(future.result())

    async def test_interrupted_opening_disclosure_is_repeated_in_next_reply(self):
        class Reply:
            status = 200
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
            async def json(self):
                return {"choices": [{"message": {"content": "Yarın saat yedide üç kişilik masa uygun mu?"}}]}
        class Client:
            def post(self, *args, **kwargs): return Reply()
        a = self.agent()
        a.client = Client()
        a.turn = asyncio.create_task(asyncio.sleep(10))
        a.speaking = True
        await a.interrupt()
        reply = await a.reply("Alo, buyurun")
        self.assertTrue(reply.startswith(DISCLOSURE))
        self.assertFalse(a.introduced)
        a.introduced = True  # equivalent to a completed disclosure playback mark
        self.assertFalse((await a.reply("Yer var" )).startswith(DISCLOSURE))

    async def test_silence_closes_stream_and_records_reason(self):
        import time
        a=self.agent()
        closed=[]
        async def close(code): closed.append(code)
        a.ws.close=close
        a.silence.last=time.monotonic()-11
        await asyncio.wait_for(a.watch_silence(),1)
        self.assertEqual(closed,[1000])
        self.assertEqual(a.state["end_reason"],"remote_silence_10s")


class ProductAgentTests(unittest.IsolatedAsyncioTestCase):
    async def test_readback_uses_approved_template_not_model_supplied_details(self):
        import json
        from app.reservation_bridge import reservation_scenario
        class Reply:
            status=200
            async def __aenter__(self):return self
            async def __aexit__(self,*args):pass
            async def json(self):return {'choices':[{'message':{'content':json.dumps({'action':'readback','reply':'Invented date and party size'})}}]}
        class Client:
            def post(self,*args,**kwargs):return Reply()
        terms={'conversation_language':'en','booking_name':'Synthetic Guest','restaurant':'Synthetic Restaurant','local_date':'2027-01-02','local_time':'13:00','people':3,'model':'eleven_flash_v2_5'}
        scenario=reservation_scenario(terms)
        agent=VoiceAgent(Client(),Socket(),'MZtest',lambda k:'synthetic',{'events':deque(maxlen=100)},scenario=scenario)
        agent.introduced=True
        response=await agent.reply('We have a table for you.')
        self.assertEqual(response,scenario['readback'])
        self.assertNotIn('Invented',response)
