"""One explicitly requested outbound smoke call; no recording or automatic retries."""
import argparse
import re
from pathlib import Path
import requests
from dotenv import dotenv_values


def start_call(to):
    config = dotenv_values(Path(__file__).resolve().parents[1] / ".env")
    sid, token, caller = (config.get(k, "") for k in ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM_NUMBER"))
    if not re.fullmatch(r"AC[0-9a-fA-F]{32}", sid or "") or not token:
        raise ValueError("Missing/invalid Twilio credentials")
    if not all(re.fullmatch(r"\+[1-9][0-9]{7,14}", n or "") for n in (to, caller)) or to == caller:
        raise ValueError("Invalid or identical caller/target numbers")
    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}"
    session = requests.Session()
    session.auth = (sid, token)
    owned = session.get(url + "/IncomingPhoneNumbers.json", params={"PhoneNumber": caller}, timeout=20)
    owned.raise_for_status()
    if not any(n.get("phone_number") == caller and n.get("capabilities", {}).get("voice") for n in owned.json().get("incoming_phone_numbers", [])):
        raise ValueError("Configured caller is not an owned voice number")
    twiml = '<Response><Say voice="Polly.Filiz" language="tr-TR">Merhaba. Bu, Taste Trip uygulamasının telefon bağlantısı testidir. Bu mesajı duyuyorsanız arama bağlantısı çalışıyor. Teşekkürler.</Say><Hangup/></Response>'
    # Never retry POST: a lost response can still mean a live call exists.
    response = session.post(url + "/Calls.json", data={"To": to, "From": caller, "Twiml": twiml, "Timeout": 20, "TimeLimit": 30, "Record": "false"}, timeout=25)
    if response.status_code != 201:
        try: code = response.json().get("code")
        except ValueError: code = None
        raise RuntimeError(f"Call not accepted: HTTP {response.status_code}, Twilio code {code}")
    data = response.json()
    return session, url, data["sid"], data.get("status")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--to", required=True)
    parser.add_argument("--call", action="store_true", help="Explicitly place one paid call")
    args = parser.parse_args()
    if not args.call:
        parser.error("No call placed; --call is required")
    try:
        _, _, _, status = start_call(args.to)
        print("Call accepted; status:", status)
    except (ValueError, RuntimeError):
        raise SystemExit("Call failed validation or provider rejected it; do not retry blindly.")
    except requests.RequestException:
        raise SystemExit("Network/response error; call outcome may be unknown. Check Twilio logs before retrying.")
