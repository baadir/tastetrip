"""Local-only live monitor; no calls, recordings, or provider secrets in the browser."""
import asyncio
import contextlib
import hmac
import secrets
import time
from pathlib import Path
from aiohttp import WSMsgType, web

STATIC = Path(__file__).resolve().parent / "static"


def local_request(request):
    return (request.remote in ("127.0.0.1", "::1")
            and request.host in ("localhost:8081", "127.0.0.1:8081")
            and not any(h in request.headers for h in ("CF-Ray", "X-Forwarded-For", "Forwarded")))


class VoiceMonitor:
    def __init__(self, state, calls=None):
        self.state = state
        self.calls = calls
        self.start_tasks = set()
        self.tickets = {}
        self.listeners = set()

    def publish(self, event):
        for queue in tuple(self.listeners):
            if queue.full():
                while not queue.empty():
                    queue.get_nowait()
                queue.put_nowait({"type": "gap"})
            queue.put_nowait(event)

    def routes(self, app):
        async def page(request):
            if not local_request(request):
                raise web.HTTPForbidden()
            name = request.match_info.get("asset", "voice-monitor.html")
            if name not in ("voice-monitor.html", "voice-monitor.js", "voice-monitor.css"):
                raise web.HTTPNotFound()
            response = web.FileResponse(STATIC / name)
            response.headers.update({"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff", "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'"})
            return response

        async def session(request):
            if not local_request(request) or request.headers.get("Origin") != "http://" + request.host:
                raise web.HTTPForbidden()
            self.tickets = {k: expiry for k, expiry in self.tickets.items() if expiry > time.monotonic()}
            if len(self.tickets) >= 20:
                raise web.HTTPTooManyRequests()
            token = secrets.token_urlsafe(32)
            self.tickets[token] = time.monotonic() + 30
            return web.json_response({"token": token}, headers={"Cache-Control": "no-store"})

        async def call_status(request):
            if not local_request(request):
                raise web.HTTPForbidden()
            if not self.calls:
                return web.json_response({"status": "unavailable"})
            result=await asyncio.to_thread(self.calls.latest)
            if result.get('status') in ('completed','failed','busy','no-answer','canceled','rejected') and self.state.get('dial_owner')=='demo':self.state['dial_lease']=0
            return web.json_response(result, headers={"Cache-Control": "no-store"})

        async def call_start(request):
            if not local_request(request) or request.headers.get("Origin") != "http://" + request.host:
                raise web.HTTPForbidden()
            if not self.calls:
                raise web.HTTPServiceUnavailable()
            data = await request.json()
            if not isinstance(data, dict) or set(data) not in ({"attempt_id"}, {"attempt_id", "scenario"}) or not isinstance(data["attempt_id"], str):
                raise web.HTTPBadRequest()
            if self.state["active"] or self.state.get('dial_lease',0)>time.monotonic():
                return web.json_response({"error": "Bir görüşme zaten sürüyor."}, status=409)
            self.state['dial_lease']=time.monotonic()+240
            self.state['dial_owner']='demo'
            async def work():
                try:
                    return await asyncio.to_thread(self.calls.start, data["attempt_id"], data.get("scenario", "restaurant_demo"))
                except ValueError as error:
                    return {"error": str(error)}
            task = asyncio.create_task(work())
            self.start_tasks.add(task)
            task.add_done_callback(self.start_tasks.discard)
            result = await asyncio.shield(task)
            if 'error' in result or result.get('status') in ('completed','failed','busy','no-answer','canceled','rejected'):
                self.state['dial_lease']=0
            return web.json_response(result, status=409 if "error" in result else 200, headers={"Cache-Control": "no-store"})

        async def socket(request):
            if not local_request(request) or request.headers.get("Origin") != "http://" + request.host:
                raise web.HTTPForbidden()
            if len(self.listeners) >= 4:
                raise web.HTTPServiceUnavailable()
            ws = web.WebSocketResponse(max_msg_size=1024, heartbeat=15)
            await ws.prepare(request)
            try:
                auth = await ws.receive_json(timeout=5)
                token = auth.get("token", "")
                expiry = self.tickets.pop(token, 0) if isinstance(token, str) else 0
                if expiry <= time.monotonic():
                    await ws.close(code=1008)
                    return ws
            except Exception:
                await ws.close(code=1008)
                return ws
            queue = asyncio.Queue(maxsize=80)
            self.listeners.add(queue)
            async def sender():
                next_state = 0
                while not ws.closed:
                    if time.monotonic() >= next_state:
                        await ws.send_json({"type": "state", "data": {**self.state, "events": list(self.state["events"])}})
                        next_state = time.monotonic() + .7
                    try:
                        item = await asyncio.wait_for(queue.get(), .2)
                        await ws.send_json(item)
                    except asyncio.TimeoutError:
                        pass
            task = asyncio.create_task(sender())
            try:
                async for msg in ws:
                    if msg.type in (WSMsgType.CLOSE, WSMsgType.ERROR): break
            finally:
                self.listeners.discard(queue)
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError): await task
            return ws

        app.router.add_get("/monitor-call", call_status)
        app.router.add_post("/monitor-call", call_start)
        app.router.add_get("/monitor", page)
        app.router.add_get("/monitor-assets/{asset}", page)
        app.router.add_post("/monitor-session", session)
        app.router.add_get("/monitor-ws", socket)
