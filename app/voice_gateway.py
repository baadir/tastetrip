"""Isolated development Twilio -> Deepgram STT gateway. No outbound call endpoint."""
import asyncio
import base64
import contextlib
import hmac
import hashlib
import json
import os
import time
from collections import deque
from pathlib import Path
from urllib.parse import urlencode, urlsplit

from aiohttp import ClientSession, ClientTimeout, WSMsgType, web
from dotenv import load_dotenv
from twilio.request_validator import RequestValidator
from .voice_agent import VoiceAgent
from .voice_monitor import VoiceMonitor
from .voice_demo_calls import DemoCalls
from .reservation_bridge import ReservationBridge, reservation_scenario

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def valid_signature(request, origin, token):
    if not origin or not token:
        return False
    # Media Streams signs the public wss:// URL, not its HTTPS upgrade equivalent.
    # Use configured public origin, never untrusted Host / forwarded headers.
    url = origin.rstrip("/").replace("https://", "wss://", 1) + request.path_qs
    validator = RequestValidator(token)
    signature = request.headers.get("X-Twilio-Signature", "")
    # Twilio documents a trailing-slash variant for WebSocket handshake signatures.
    return any(validator.validate(candidate, {}, signature)
               for candidate in (url, url + "/" if not request.query_string and not url.endswith("/") else url))


def create_gateway(config=None):
    settings = dict(config or {})
    def value(key):
        return settings.get(key, os.getenv(key, ""))
    origin = value("VOICE_PUBLIC_URL").rstrip("/")
    if origin and (urlsplit(origin).scheme != "https" or urlsplit(origin).path not in ("", "/")):
        raise ValueError("VOICE_PUBLIC_URL must be an HTTPS origin")
    app = web.Application(client_max_size=16384)
    state = {"handshake_rejections": 0, "active": False, "status": "idle", "events": deque(maxlen=100), "frames": 0}

    bridge = ReservationBridge(value, state)
    bridge.routes(app)
    calls = None if settings.get("DISABLE_DEMO_CALLS") or value("DISABLE_DEMO_CALLS") == "true" else DemoCalls(value, ROOT / "data" / "voice-demo.sqlite3")
    monitor = VoiceMonitor(state, calls)
    monitor.routes(app)

    async def health(request):
        return web.json_response({"ok": True})

    async def transcript(request):
        secret = value("VOICE_MONITOR_TOKEN")
        supplied = request.headers.get("Authorization", "")
        if not secret or not hmac.compare_digest(supplied, "Bearer " + secret):
            raise web.HTTPForbidden()
        return web.json_response({**state, "events": list(state["events"])}, headers={"Cache-Control": "no-store"})

    async def media(request):
        if not valid_signature(request, origin, value("TWILIO_AUTH_TOKEN")):
            state["handshake_rejections"] += 1
            raise web.HTTPForbidden()
        if not value("DEEPGRAM_API_KEY"):
            raise web.HTTPServiceUnavailable()
        if state["active"]:
            raise web.HTTPServiceUnavailable()
        state.update(active=True, status="connecting", frames=0, agent_error=None, end_reason=None)
        state["events"].clear()
        monitor.publish({"type": "reset"})
        ws = web.WebSocketResponse(max_msg_size=16384, heartbeat=15)
        dg = None
        reader = None
        agent = None
        finish_product = None
        try:
            await ws.prepare(request)
            # Twilio must identify the expected account before a paid STT connection opens.
            start = None
            async with asyncio.timeout(10):
                async for msg in ws:
                    if msg.type != WSMsgType.TEXT:
                        break
                    data = json.loads(msg.data)
                    if data.get("event") == "start":
                        start = data["start"]
                        break
            if not start or start.get("accountSid") != value("TWILIO_ACCOUNT_SID"):
                await ws.close(code=1008)
                return ws
            fmt = start.get("mediaFormat", {})
            if fmt.get("encoding") != "audio/x-mulaw" or fmt.get("sampleRate") != 8000 or fmt.get("channels") != 1:
                await ws.close(code=1008)
                return ws
            scenario = start.get("customParameters", {}).get("mode", "")
            language = "en" if scenario == "anna_restaurant" else "tr"
            params = urlencode({"model": "nova-3", "language": language, "encoding": "mulaw", "sample_rate": 8000, "channels": 1, "interim_results": "true", "punctuate": "true", "endpointing": 300})
            async with ClientSession(timeout=ClientTimeout(total=None, sock_connect=10)) as client:
                publish = monitor.publish
                agent_scenario = scenario
                if scenario == "reservation":
                    terms, publish, finish_product = await bridge.session(client, start.get("customParameters", {}).get("attempt", ""), start.get("callSid", ""))
                    agent_scenario = reservation_scenario(terms)
                    params = urlencode({"model": "nova-3", "language": terms["conversation_language"], "encoding": "mulaw", "sample_rate": 8000, "channels": 1, "interim_results": "true", "punctuate": "true", "endpointing": 300})
                dg = await client.ws_connect("wss://api.deepgram.com/v1/listen?" + params, headers={"Authorization": "Token " + value("DEEPGRAM_API_KEY")}, heartbeat=5, max_msg_size=262144)
                state["status"] = "listening"
                agent_mode = scenario in ("restaurant_demo", "anna_restaurant", "reservation")
                state["scenario"] = scenario
                if agent_mode:
                    agent = VoiceAgent(client, ws, start["streamSid"], value, state, publish, scenario=agent_scenario)
                    await agent.start()
                async def receive_results():
                    async for message in dg:
                        if message.type != WSMsgType.TEXT:
                            break
                        event = json.loads(message.data)
                        if event.get("type") == "Error":
                            state["status"] = "stt_error"
                            await ws.close(code=1011)
                            return
                        if event.get("type") == "Results":
                            alternatives = event.get("channel", {}).get("alternatives", [])
                            text = alternatives[0].get("transcript", "") if alternatives else ""
                            if text:
                                state["events"].append({"role": "restaurant", "text": text[:4000], "final": bool(event.get("is_final")), "at": time.time()})
                            if scenario == "reservation" and text and event.get("is_final"):
                                publish({"type": "transcript", "event_id": hashlib.sha256(json.dumps([start.get("callSid"), event.get("start"), event.get("duration"), text]).encode()).hexdigest(), "role": "restaurant", "text": text, "final": True})
                            if agent:
                                await agent.feed(text, bool(event.get("is_final")), bool(event.get("speech_final")))
                reader = asyncio.create_task(receive_results())
                try:
                    async with asyncio.timeout(180 if agent_mode else 60):
                        async for message in ws:
                            if message.type != WSMsgType.TEXT:
                                break
                            event = json.loads(message.data)
                            if event.get("event") == "mark" and agent:
                                agent.mark(event.get("mark", {}).get("name"))
                            if event.get("event") == "stop":
                                await dg.send_json({"type": "CloseStream"})
                                with contextlib.suppress(asyncio.TimeoutError):
                                    await asyncio.wait_for(asyncio.shield(reader), 3)
                                break
                            if event.get("event") == "media" and event.get("media", {}).get("track", "inbound") == "inbound":
                                audio = base64.b64decode(event["media"]["payload"], validate=True)
                                if len(audio) > 8192:
                                    raise ValueError("oversized media")
                                publish({"type": "audio", "role": "restaurant", "payload": event["media"]["payload"]})
                                if agent:
                                    agent.hear_audio(audio)
                                await dg.send_bytes(audio)
                                state["frames"] += 1
                finally:
                    if agent:
                        await agent.close()
                    if finish_product:
                        await finish_product()
                        finish_product = None
                    reader.cancel()
                    with contextlib.suppress(asyncio.CancelledError):
                        await reader
        except Exception:
            state["status"] = "stream_error"
            # No audio, transcripts, credentials or provider exceptions in public logs.
            if ws.prepared:
                await ws.close(code=1011)
        finally:
            if finish_product:
                # ClientSession may already be closed; finish is best effort and never makes a new call.
                with contextlib.suppress(Exception): await finish_product()
            if locals().get("scenario") == "reservation":
                state["events"].clear()
                bridge.active_attempt = None
            if state["status"] not in ("stream_error", "stt_error"):
                state["status"] = "ended"
            state["active"] = False
            state["dial_lease"] = 0
            state["dial_owner"] = None
        return ws

    app.router.add_get("/health", health)
    app.router.add_get("/internal/transcript", transcript)
    app.router.add_get("/twilio/media", media)
    return app


if __name__ == "__main__":
    web.run_app(create_gateway(), host=os.getenv("VOICE_GATEWAY_HOST", "127.0.0.1"), port=int(os.getenv("VOICE_GATEWAY_PORT", "8081")), access_log=None)
