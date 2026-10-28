# Production voice reservations — Coolify

28 October 2026. D-038/H-081. This extends the web-only deployment; it does not authorize an actual phone call.

## Persistent configuration

- Existing Coolify application: `wpsrxqjtiwj8w64igmghpk4x`, repository `baadir/tastetrip`, branch `main`.
- Build pack: Docker Compose; repository file `/compose.coolify.yaml`.
- Web: `https://tastetrip.bahadirciftci.work`, service `tastetrip`, internal port 8080.
- Gateway: `https://voice-tastetrip.bahadirciftci.work`, service `voice-gateway`, internal port 8081. DNS resolves via the existing wildcard. Coolify manages HTTPS routing and WebSocket upgrades.
- Worker: `reservation-worker`; no public port.
- Web and worker share Docker volume `wpsrxqjtiwj8w64igmghpk4x_tastetrip-data` at `/app/data`. The gateway accesses the web internal API by service name.
- Gateway must receive the production `APP_ORIGIN` as well as `RESERVATION_WEB_URL=http://tastetrip:8080`. Worker uses `VOICE_GATEWAY_INTERNAL_URL=http://voice-gateway:8081`.
- `VOICE_PUBLIC_URL` is the gateway HTTPS origin, not the old temporary tunnel. Anna voice ID is `XZXyuzPdidXaSa10PmVA`. The existing Flash/v3 language router is preserved.
- Provider keys and the shared monitor token remain Coolify runtime variables, never repository/build credentials. Demo calling stays disabled.

## Migration and backups

Coolify parser version 5 rewrites named Compose volume sources even when an external volume alias is supplied. The original standalone volume was therefore not assumed to remain mounted. Before migration, the outbox and active-call counts were zero, an SQLite backup was made, and the old web container was stopped for a consistent transfer. The database was copied through SQLite's backup API into the managed Compose volume; integrity check passed and the existing user and saved itinerary counts matched.

The first read-only-source backup attempt failed because SQLite needed journal/sidecar access; the old web service was immediately restarted. The retry after stopping it again succeeded with the source filesystem writable and the database connection read-only. No existing destination database was overwritten.

Preserved rollback material on the server:

- Original Docker volume `wpsrxqjtiwj8w64igmghpk4x-tastetrip-data`, including `backups/before-voice-20261028.sqlite3`.
- Root-only `/root/tastetrip-backup-20261028/coolify-resource-before-compose.json`, containing the pre-migration application/settings and encrypted environment metadata. Never upload this file.

Do not mount a second web process against another database and call it a shared deployment. Do not prune the original volume before backup/restore policy is established. A rollback after new production writes requires a current SQLite backup and explicit volume mapping; the pre-migration snapshot is not an automatic replacement for newer data.

## Non-dialing checks

Check all three container health states, HTTPS `/health` on both public origins, and `/api/reservations/options` for `worker_available=true`. Confirm a recent `reservation_worker_heartbeat` with ready=1 in the shared database. The worker checks public gateway reachability and authenticated internal readiness.

Twilio account authentication, ElevenLabs model/Anna voice metadata, and Deepgram's authenticated STT WebSocket can be checked without placing a call or uploading speech. An unsigned Twilio media WebSocket must return 403. The live-listening WebSocket must require the production Origin and a short-lived signed token; test connections may use a synthetic attempt without creating an outbound call.

The user must review a fresh reservation summary and explicitly approve a real call. Healthy configuration and provider authentication are not evidence of a completed conversation, availability, or a confirmed reservation.

## Verified deployment

Application code/config commit `a961bf9`; Coolify deployment `x146vgaks490vk2355az9f13` finished. All three services healthy. Production options report `worker_available=true`, all required call fields present with valid number/URL format, provider authentication checks passed, and an authorized synthetic live-listening WSS connection succeeded. Wrong-Origin and unsigned Twilio connections were rejected. After redeployment, the existing user and saved itinerary counts were unchanged. Zero outbound attempts were created. Actual phone conversation quality remains to be tested through explicit user approval.


## Deployment update — 28 October 2026 / H-083
Reservation popup commit 1f6963f deployed successfully through Coolify e108e5kfbekev7mh667pcjds. Web/gateway/worker healthy; public HTTPS health 200, worker available, versioned popup asset present. Existing one user and two saved plans preserved. No actual telephone call was made. This supersedes the earlier not-deployed status; earlier evidence remains historical.
