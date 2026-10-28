# TasteTrip installation guide

TasteTrip was built from scratch for the Qloo Agentic Hackathon. This guide covers a local web setup, optional integrations, and the three-service production deployment.

## Requirements

- Git and Python 3.12 with virtual environment support.
- A Qloo API key for place and cultural discovery.
- An OpenAI-compatible LLM endpoint supporting `/chat/completions` and `response_format: json_object` for conversational planning. The current provider is DeepSeek; select a model available to your account.
- Optional Docker Engine with Docker Compose v2 for container deployment.
- Optional Aviasales/Travelpayouts access for flights.
- For calls: Twilio, Deepgram, ElevenLabs, an authorized caller number, and a public HTTPS gateway with WebSocket support.

No npm install or frontend compilation is required.

## 1. Clone and install

```bash
git clone https://github.com/baadir/tastetrip.git
cd tastetrip
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Windows PowerShell:

```powershell
.venv/Scripts/python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Do not overwrite an existing `.env`; merge missing fields instead. All commands below run from the repository root. On Windows, use `.venv/Scripts/python.exe` in place of `python` if the environment is not activated.

## 2. Configure core services

Edit `.env` locally. Never commit its values.

```dotenv
APP_ORIGIN=http://localhost:8080
COOKIE_SECURE=false
DATA_DIR=./data
PORT=8080
QLOO_API_URL=https://hackathon.api.qloo.com
QLOO_API_KEY=<your-qloo-key>
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=<model-enabled-for-your-account>
LLM_API_KEY=<your-provider-key>
```

The Qloo origin must match the server allowed by your API key. Choose an LLM model that supports the required JSON mode; do not assume the example model is available to every account. The server also validates generated data; JSON mode alone is not a validity guarantee.

`APP_ORIGIN` must match the exact browser origin, including scheme and port. With the setting above, use `http://localhost:8080`, rather than switching to `http://127.0.0.1:8080`. Use secure cookies for production HTTPS, and leave them disabled for local HTTP.

## 3. Start the web application

```bash
python -m app.server
```

Open [http://localhost:8080](http://localhost:8080). You can explore before signing in. Create an account through **Sign up** when you want to save routes or prepare a reservation.

The Flask development server binds to loopback. Use the Docker/Gunicorn setup behind a reverse proxy for production. Restart processes after editing `.env`; environment variables already supplied to the process take precedence over dotenv values.

## Optional flight discovery

Add to `.env`:

```dotenv
AVIASALES_API_TOKEN=<your-api-token>
AVIASALES_PARTNER_ID=<your-partner-id>
```

Restart the web app. Use **Find flights** and supply the origin, destination, and travel dates. Results are cached price information; follow the source link to check the current offer.

## Voice reservations

### Credentials and endpoints

Add these fields to the same `.env` used by the web app, gateway, and worker:

```dotenv
TWILIO_ACCOUNT_SID=<your-account-sid>
TWILIO_AUTH_TOKEN=<your-auth-token>
TWILIO_FROM_NUMBER=<authorized-number-in-E164-format>
DEEPGRAM_API_KEY=<your-deepgram-key>
ELEVENLABS_API_KEY=<your-elevenlabs-key>
ELEVENLABS_VOICE_ID=XZXyuzPdidXaSa10PmVA
ELEVENLABS_VOICE_ID_TR=XZXyuzPdidXaSa10PmVA
ELEVENLABS_VOICE_ID_EN=XZXyuzPdidXaSa10PmVA
VOICE_PUBLIC_URL=https://voice.your-domain.example
VOICE_MONITOR_TOKEN=<one-long-random-shared-secret>
RESERVATION_WEB_URL=http://127.0.0.1:8080
VOICE_GATEWAY_INTERNAL_URL=http://127.0.0.1:8081
VOICE_GATEWAY_HOST=127.0.0.1
VOICE_GATEWAY_PORT=8081
RESERVATION_DAILY_LIMIT=10
DISABLE_DEMO_CALLS=true
```

`VOICE_MONITOR_TOKEN` must be identical across all three processes and remain private. Generate a fresh value, for example with `python -c "import secrets; print(secrets.token_urlsafe(48))"`, and put it directly in your local environment.

The included Anna voice ID requires access under your ElevenLabs account. Configure another accessible voice if needed. Ensure Twilio permits outbound calls to the destination and that your account/number is authorized; trial-account restrictions can still apply.

### Run all three processes

Keep each process running in a separate terminal with the same virtual environment and working directory:

```bash
# Terminal 1
python -m app.server
```

```bash
# Terminal 2
python -m app.voice_gateway
```

```bash
# Terminal 3
python -m app.reservation_worker
```

Expose the gateway's local port 8081 through an HTTPS reverse proxy or a development tunnel that supports WSS. Set `VOICE_PUBLIC_URL` to that public HTTPS origin, with no path. A localhost-only gateway cannot receive Twilio media. The gateway must also reach the internal web URL; the worker must reach both the internal gateway and its public health endpoint.

### Verify before dialing

1. Check the web `/health` endpoint and the gateway's public `/health` endpoint.
2. Check `GET /api/reservations/options`; `worker_available` should be `true` once the worker is ready.
3. Select a restaurant from a route, complete the booking details in chat, and review the popup.
4. Verify the business/phone match and restaurant-local date, time, and time zone from a current source.
5. Review the separate paid-call approval. Only then start an authorized call.

Opening the UI, generating an itinerary, or running health checks does not dial a restaurant. Use your own authorized number for initial testing. Closing the call window stops browser listening; **Stop the call** requests a phone stop. A stopped call does not cancel a reservation already made.

## Docker

Copy and configure `.env`, then start just the web service:

```bash
docker compose up --build -d tastetrip
docker compose logs --tail=100 tastetrip
```

Open `http://localhost:8080`. `compose.yaml` mounts `tastetrip-data` at `/app/data`. It can also start the gateway and worker with `docker compose up --build -d`, once their credentials and public routing are configured. Its gateway uses an internal exposed port, not a host-published port: attach an appropriate reverse proxy/network, or explicitly publish 8081 only for a local development proxy. Internal container addresses are service names, not host loopback.

## Coolify / production

1. Create a Coolify application connected to this repository and the desired branch.
2. Select Docker Compose and set the file path to **`/compose.coolify.yaml`**. This production file consumes runtime variables directly; do not upload `.env` to the repository.
3. Set the required Qloo, LLM, flight (optional), Twilio, Deepgram, ElevenLabs, voice ID, shared token, and `VOICE_PUBLIC_URL` variables in Coolify. Set `QLOO_API_URL` explicitly.
4. If deploying to your own domain, edit **both** web and gateway `APP_ORIGIN` entries in the Compose file to your web origin. The checked-in production values target the existing TasteTrip deployment.
5. Assign the web HTTPS domain to service `tastetrip` on internal port 8080. Assign a separate public HTTPS domain to `voice-gateway` on internal port 8081. Configure DNS and WebSocket forwarding. Set `VOICE_PUBLIC_URL` to the gateway domain, not the web domain.
6. Keep the worker private. Keep `/app/data` mounted from the **same persistent volume** in web and worker. Container-internal web/gateway URLs are supplied in the Compose file. Run one reservation worker instance.
7. Deploy and wait for all three health checks. Verify public health, `worker_available=true`, and persistence after a redeployment before conducting an approved call.

The image uses Python 3.12 slim and can be built natively on ARM64, including Hetzner CAX21. The web runs Gunicorn; the gateway and worker run their own Python entry points.

**Existing installations:** read the [production voice runbook](VOICE_PRODUCTION_RUNBOOK.md) before changing volumes or build packs. Coolify can rewrite volume names; verify the actual mount and take a current SQLite backup instead of assuming a named alias points to old data. The existing deployment's old migration backup is not a replacement for newer production writes.

## Data and backups

Local SQLite data is stored under `DATA_DIR`; Docker uses `/app/data`. Back up `tastetrip.sqlite3` with SQLite's backup API or a consistent stopped-service backup, including any required journal handling. Preserve the volume during redeployments; `docker compose down -v` removes it and can destroy application data.

Anonymous identity cookies contain a random identifier. Device remembering is opt-in; account profiles and saved itineraries are stored server-side. Transcripts and summaries currently have a 30-day retention window. Live audio is streamed rather than stored as an audio recording by the application. Provider-side policies remain separate.

## Tests and troubleshooting

```bash
python -m unittest discover -s tests -v
```

| Symptom | Check |
| --- | --- |
| Chat or route generation fails | LLM key, base URL, enabled model, JSON output support, and provider response |
| Qloo returns an error or few results | Key/server pairing, constraints, destination coverage, and supplied taste signals |
| Request source not accepted | Exact `APP_ORIGIN` versus the browser's scheme, host, and port |
| Phone configuration missing | All voice fields above, including voice ID, plus the core LLM fields |
| Worker unavailable | Shared database, running worker/gateway, shared token, internal URLs, and public gateway health |
| Twilio rejects a call | Account restrictions, caller number authorization, destination permissions, and provider error code |
| Live audio does not connect | HTTPS/WSS routing, web Origin, gateway reachability, and signed listener authorization |
| Menu cannot open inside the app | The source may forbid embedding; use the provided source link |
| Data disappears after deployment | Actual volume name/mount, `/app/data` ownership, and web/worker database alignment |

Check process/container logs without publishing credentials or private conversation content. The current product limits are listed in the [README](../README.md#verification-and-current-limits).
