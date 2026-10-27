# Coolify / Hetzner CAX21 kurulumu

21 Ekim 2026. Kullanıcı hedefi Coolify üzerindeki CAX21. Sunucuya bağlanılmadı veya deploy yapılmadı.

## Dockerfile yöntemi

1. Repoyu Coolify’a bağla, build pack **Dockerfile**, Dockerfile `/Dockerfile`, uygulama portu **8080** seç.
2. HTTPS domain ata. `APP_ORIGIN=https://senin-domainin` (sonunda slash gerekmez) ve `COOKIE_SECURE=true` runtime değişkenlerini ayarla. Origin tarayıcıdaki adresle tam aynı olmalı.
3. `.env.example` alanlarını Coolify runtime environment olarak gir. QLOO_API_KEY, LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, AVIASALES_API_TOKEN ve gerekiyorsa AVIASALES_PARTNER_ID. Anahtarları build argument veya public değişken yapma. Docker imajına .env kopyalanmaz.
4. **Kalıcı storage destination `/app/data`**, uygulama UID 10001 yazma izniyle bağla. SQLite kullanıcılar/oturumlar/tercihler/taslaklar/rotalar burada. Redeploy’da volume korunmalı.
5. Port 8080, `/health` HTTP 200 beklenir. Dockerfile HEALTHCHECK sağlar. Dış API anahtarı eksikliği healthcheck’i bozmaz; arayüz bağlantı durumunu gösterir.
6. Container non-root çalışır. Gunicorn 1 worker/8 thread; tek SQLite yazıcısı ve tek uygulama instance’ı. Yatay replikasyon için önce DB/session/rate-limit katmanını ortak servise taşı.

Python 3.12 slim multiarch tabanı kullanılıyor; amd64 sabitlenmedi, native binary veya x86-only paket yok. CAX serisi ARM64’tür. İlk CAX21 build ve restart sonrası kalıcı rota/giriş kontrolü sunucuda ayrıca yapılmalı.

## Compose seçeneği

Yerelde `.env` ile `docker compose up --build` kullanılabilir. Repo compose dosyası 8080 host portunu publish eder; Coolify Dockerfile yöntemi önerilir. Coolify Compose kullanılırsa proxy/domain ve port yayınlama yapılandırmasını o kaynak üzerinden düzenle.

## Yedek ve operasyon

SQLite WAL modunda. Çalışırken yalnız ana .sqlite3 dosyasını kopyalamak yeterli değildir; Python sqlite3 backup API veya SQLite online backup kullan. Volume için günlük yedek/saklama ve geri yükleme deneyi kur. Şu an otomatik yedek işi tanımlanmadı.

Ziyaretçi cookie’si 180 gün, giriş cookie’si 30 gün. Cookie tanıması bu tarayıcıya aittir; cihazlar arası kimlik girişle gelir. Tercihler sunucuda saklanır; cihaz tercihlerini temizle kontrolü var. Rate limit tek süreç belleğinde; restart’ta sıfırlanır. Üretimde trafik limitleri, hesap kurtarma, eski kayıt temizleme ve kullanım maliyeti sınırları ayrıca tamamlanmalı.

## İlk smoke kontrolü

- `/health` → 200; statik arayüz yüklenir.
- Giriş yapmadan rota üret; Qloo sonuçlarını gör, önerileri yalnız tıklayınca al.
- Kaydet → giriş kapısı → hesap aç → rota listede görünür.
- Çıkış/giriş → kaydedilmiş rotayı aç.
- LLM bağlıyken ikinci gün müzesini ilk güne taşı; ID’ler korunur, sürüm artar.
- Redeploy → aynı hesap ve kayıtlar korunur.

Kaynaklar: [Coolify uygulamalar](https://coolify.io/docs/applications/), [healthchecks](https://coolify.io/docs/applications/configuration/health-checks), [Hetzner ARM64](https://www.hetzner.com/pressroom/arm64-cloud/), [OpenAI uyumlu chat sözleşmesi için resmi referans](https://developers.openai.com/api/reference/resources/chat).

## Restoran rezervasyonu servisleri (22 Ekim 2026)
Güncel compose.yaml üç servis çalıştırır: tastetrip (web), voice-gateway (8081), reservation-worker (port yok). Web ve worker aynı tastetrip-data volume'unu paylaşır. Gateway için ayrı HTTPS/WSS domain tanımlayın; APP_ORIGIN web domain'i, VOICE_PUBLIC_URL gateway domain'i olsun. İç bağlantılar RESERVATION_WEB_URL=http://tastetrip:8080 ve VOICE_GATEWAY_INTERNAL_URL=http://voice-gateway:8081. Üç serviste aynı VOICE_MONITOR_TOKEN ve ilgili sağlayıcı runtime secrets gereklidir; sırları repoya koymayın. Üretim Compose sabit numaralı demo düğmelerini kapatır. Ayrıntı/ilk sürüm sınırları RESERVATION_IMPLEMENTATION.md. Bu dosya güncellemesi yayın veya ARM64 çalışma testi değildir.
