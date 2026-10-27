"""Persistent single-call guard for the local, fixed-target voice demo."""
from contextlib import contextmanager
import re
import sqlite3
import time
from pathlib import Path
from xml.sax.saxutils import quoteattr
import requests
from .voice_scenarios import ANNA

TERMINAL = {"completed", "failed", "busy", "no-answer", "canceled", "rejected"}


class DemoCalls:
    def __init__(self, value, path):
        self.value = value
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self.db() as db:
            db.execute("CREATE TABLE IF NOT EXISTS calls (id TEXT PRIMARY KEY, sid TEXT, status TEXT NOT NULL, created REAL NOT NULL)")
            columns = {row[1] for row in db.execute("PRAGMA table_info(calls)")}
            for column in ("error_code", "http_status"):
                if column not in columns:
                    db.execute("ALTER TABLE calls ADD COLUMN " + column + " INTEGER")

    @contextmanager
    def db(self):
        connection = sqlite3.connect(self.path, timeout=10)
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def session(self):
        s = requests.Session()
        s.auth = (self.value("TWILIO_ACCOUNT_SID"), self.value("TWILIO_AUTH_TOKEN"))
        return s

    def base(self):
        return "https://api.twilio.com/2010-04-01/Accounts/" + self.value("TWILIO_ACCOUNT_SID")

    def public(self, row):
        return {"attempt_id": row[0], "status": row[2], "created": row[3], "error_code": row[4] if len(row)>4 else None, "http_status": row[5] if len(row)>5 else None} if row else {"status": "idle"}

    def latest(self):
        with self.db() as db:
            row = db.execute("SELECT * FROM calls ORDER BY created DESC LIMIT 1").fetchone()
        if row and row[1] and row[2] not in TERMINAL:
            try:
                r = self.session().get(self.base() + "/Calls/" + row[1] + ".json", timeout=8)
                if r.ok:
                    status = r.json().get("status")
                    if status in TERMINAL | {"queued", "ringing", "in-progress"}:
                        with self.db() as db: db.execute("UPDATE calls SET status=? WHERE id=?", (status, row[0]))
                        row = (row[0], row[1], status, row[3], *row[4:])
            except requests.RequestException: pass
        return self.public(row)

    def start(self, key, scenario="restaurant_demo"):
        if scenario not in ("restaurant_demo", ANNA["id"]):
            raise ValueError("Bilinmeyen arama senaryosu.")
        if not re.fullmatch(r"[A-Za-z0-9_-]{16,80}", key):
            raise ValueError("Geçersiz arama girişimi.")
        target = ANNA["target"] if scenario == ANNA["id"] else self.value("TWILIO_TEST_TO_NUMBER")
        caller = self.value("TWILIO_FROM_NUMBER")
        origin = self.value("VOICE_PUBLIC_URL").rstrip("/")
        if not all(re.fullmatch(r"\+[1-9][0-9]{7,14}", x or "") for x in (target, caller)) or target == caller or not origin.startswith("https://"):
            raise ValueError("Test numarası veya ses bağlantısı yapılandırılmamış.")
        if not all(self.value(k) for k in ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "DEEPGRAM_API_KEY", "ELEVENLABS_API_KEY", ("ELEVENLABS_VOICE_ID_EN" if scenario == ANNA["id"] else "ELEVENLABS_VOICE_ID_TR"), "LLM_API_KEY", "LLM_MODEL", "LLM_BASE_URL")):
            raise ValueError("Konuşma servislerinin yapılandırması eksik.")
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM calls WHERE id=?", (key,)).fetchone()
            if row: return self.public(row)
            active = db.execute("SELECT * FROM calls ORDER BY created DESC LIMIT 1").fetchone()
            if active and active[2] not in TERMINAL:
                raise ValueError("Bir arama sürüyor veya önceki sonucun kontrolü gerekiyor.")
            db.execute("INSERT INTO calls (id,sid,status,created) VALUES (?,NULL,'starting',?)", (key, time.time()))
        # Commit the attempt BEFORE sending the single non-retried provider POST.
        twiml = '<Response><Connect><Stream url=' + quoteattr(origin.replace("https://", "wss://", 1) + '/twilio/media') + '><Parameter name="mode" value="' + scenario + '"/></Stream></Connect><Hangup/></Response>'
        sid, status = None, "unknown"
        error_code, http_status = None, None
        try:
            r = self.session().post(self.base() + "/Calls.json", data={"To": target, "From": caller, "Twiml": twiml, "Timeout": 20, "TimeLimit": 180, "Record": "false"}, timeout=25)
            http_status = r.status_code
            if r.status_code == 201:
                data = r.json()
                sid, status = data["sid"], data.get("status", "queued")
            elif 400 <= r.status_code < 500:
                status = "rejected"
                payload = r.json()
                code = payload.get("code")
                error_code = code if isinstance(code, int) else None
        except (requests.RequestException, ValueError, KeyError): pass
        with self.db() as db:
            db.execute("UPDATE calls SET sid=?,status=?,error_code=?,http_status=? WHERE id=?", (sid, status, error_code, http_status, key))
            row = db.execute("SELECT * FROM calls WHERE id=?", (key,)).fetchone()
        return self.public(row)
