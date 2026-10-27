# Tastetrip — GitHub üzerinden Coolify dağıtım planı

27 Ekim 2026. Kullanıcı talimatı: mevcut projeyi `baadir/tastetrip` deposuna yükle, Coolify'da yeni Tastetrip projesini oluştur, `tastetrip.bahadirciftci.work` domainini ekle ve bu depodan dağıtımı planla. Canlıya çıkma ile konfigürasyon hazırlığı ayrı durumdur; gerçekleşen adımlar PROJECT_HISTORY içinde tutulur.

## Kaynak ve web uygulaması

- Depo: https://github.com/baadir/tastetrip.git · dal: `main` · public.
- Coolify: https://panel.bahadirciftci.work · proje: Tastetrip · ortam: production.
- Build Pack: Dockerfile · base directory `/` · Dockerfile `/Dockerfile`.
- Web hedefi: `https://tastetrip.bahadirciftci.work` · container port `8080`.
- Tek web instance; mevcut Dockerfile Gunicorn 1 worker/8 thread, non-root UID10001 ve `/health` kontrolü kullanır. Taban multiarch Python3.12-slim; gerçek CAX21/ARM64 build ayrıca doğrulanmalıdır.
- Kalıcı veri: container `/app/data`, Coolify named volume `wpsrxqjtiwj8w64igmghpk4x-tastetrip-data`. Boş volume'un UID10001 tarafından yazılabilirliği ilk açılışta doğrulanır. Yerel kullanıcı/sohbet veritabanı repoya veya sunucuya otomatik taşınmaz.

Sır olmayan runtime değişkenleri:

```dotenv
APP_ORIGIN=https://tastetrip.bahadirciftci.work
COOKIE_SECURE=true
DATA_DIR=/app/data
PORT=8080
QLOO_API_URL=https://hackathon.api.qloo.com
LLM_BASE_URL=https://api.deepseek.com
DISABLE_DEMO_CALLS=true
```

Qloo/DeepSeek/Aviasales anahtarları Coolify runtime environment alanına ayrı eklenmelidir; build arguments veya public/frontend değişkenleri değildir. Kullanılacak `LLM_MODEL` hesabın erişebildiği modelle açıkça ayarlanır; `.env.example` varsayılanı erişim kanıtı sayılmaz. Yerel `.env` GitHub'a yüklenmedi. Bu hazırlık anahtarların Coolify'a aktarıldığı anlamına gelmez.

## Sesli rezervasyonun tam üretim aşaması

Yalnız web container'ı canlı rezervasyon araması için yeterli değildir. Önceki kabul edilmiş üç servis yapısı korunur:

| Servis | Komut / giriş | Veri / bağlantı |
| --- | --- | --- |
| Web | Dockerfile varsayılan Gunicorn, 8080 | `/app/data`, HTTPS uygulama domaini |
| Voice gateway | `python -m app.voice_gateway`, 8081 | HTTPS/WSS için ayrı adres; `VOICE_GATEWAY_HOST=0.0.0.0`, `RESERVATION_WEB_URL=http://tastetrip:8080` |
| Reservation worker | `python -m app.reservation_worker` | Web ile aynı volume ve `VOICE_GATEWAY_INTERNAL_URL=http://voice-gateway:8081` |

Tam servisler `compose.yaml` mantığıyla **aynı Compose kaynağında** kurulmalı; bağımsız Coolify kaynaklarının prefiksli named volume'larının kendiliğinden aynı diski paylaşacağı varsayılmamalı. Mevcut compose yerel kullanım için `.env` okur ve web host8080 portunu publish eder; Coolify Compose aşamasında runtime env referansları ve proxy ağına göre üretim varyantı hazırlanır. Web-only Dockerfile kaynağıyla eşzamanlı ikinci web container'ı aynı veritabanını kullanacak şekilde açılmaz.

Gateway HTTPS/WSS hostname'i henüz kullanıcı tarafından belirlenmedi; yeni domain kendi kendine atanmaz. Web'in `VOICE_PUBLIC_URL` değeri gerçek gateway adresine çevrilmeden ve üç serviste aynı güçlü `VOICE_MONITOR_TOKEN` ile sağlayıcı runtime sırları tanımlanmadan ücretli çağrı hazır sayılmaz. Sabit şahsi test düğmeleri üretimde kapalı kalır. Demo numarası/Twilio test hedefi üretim ortamına taşınmaz.

## Yayına alma sırası

1. Bu repodan Dockerfile web kaynağını ve domain/port/storage ayarlarını kaydet.
2. Qloo/DeepSeek/Aviasales runtime değişkenlerini tamamla; en az Qloo ve DeepSeek anahtar/model olmadan işlevsel asistan yayını iddiasında bulunma.
3. Cloudflare kayıtlarının yalnız çözülmesi yeterli değildir; origin'in bu sunucu olduğu, proxy TLS modu ve Coolify sertifikası yayına alma sırasında doğrulanır.
4. Deploy başlat; build logları, `/health`, HTTPS ve tarayıcıdaki ilk sohbet → gerçek öneri → giriş/kayıt adımlarını kontrol et. Yerel Docker daemon çalışmadığından bu hazırlıkta container build yapılmadı.
5. Rota/hesap oluştur, redeploy et ve volume'daki kayıtların korunduğunu doğrula. SQLite backup API ile yedek ve geri yükleme deneyi yap.
6. Ses için Compose varyantına kontrollü geçiş, aynı SQLite volume, WSS, worker heartbeat ve onay kapısını doğrula. Kullanıcı belirli hedef için açıkça başlatmadan gerçek telefon denemesi yapma.

Manuel Deploy, GitHub `main` dalını kaynak alır. Push sonrası otomatik dağıtım için GitHub App veya webhook ayrıca kurulup doğrulanmalıdır; public Git kaynağı oluşturmak tek başına çalışan webhook kanıtı değildir. Anahtarları tamamlamadan otomatik deploy açılması planlanmadı.

## Doğrulama sınırı

Mevcut 119 birim test geçti ve yükleme öncesi dosya listesi mevcut yerel API sırlarına karşı tarandı. `.env`, data, sanal ortam, ses ve ekran görüntüsü artifact'ları dışarıda tutuldu. Bu kontroller üretim build/ARM64, gerçek rezervasyon telefonu veya canlı domain sertifikası testi yerine geçmez.


## Coolify kaynak kaydı (27–28 Ekim hazırlığı)
- Proje: `dy0g44moqkbcxsshesm6k6xl` · production: `wugoylfk2w7x1jzujumrk9na`.
- Web uygulaması: `wpsrxqjtiwj8w64igmghpk4x`.
- Konfigürasyon: https://panel.bahadirciftci.work/project/dy0g44moqkbcxsshesm6k6xl/environment/wugoylfk2w7x1jzujumrk9na/application/wpsrxqjtiwj8w64igmghpk4x
- İlk kaynak push: `d4d4d52` (`main`). Son dokümantasyon commit'i GitHub main'de ayrıca görülebilir.
- Domain/Dockerfile/8080 ayarları ve prefiksli kalıcı volume oluşturuldu; Deploy başlatılmadı. Uygulama Exited durumunda; bu başlatılmamış kaynak için yayın başarısı değildir.

28 Ekim kayıt: Yukarıdaki yedi sır olmayan env alanı Coolify runtime-only olarak kaydedildi (buildtime kapalı). Sağlayıcı sırları ve LLM_MODEL henüz eklenmedi.


### 28 Ekim güncellemesi — H-075
Sağlayıcı anahtarları, LLM_MODEL ve ses bağlantısı için 12 boş giriş alanı eklendi; toplam 19 alan runtime-only olarak doğrulandı. Önceki kayıttaki eksik alanlar artık listede mevcut, fakat değerleri henüz girilmedi. Kullanıcı her ilgili satırın değerini girip Update ile kaydetmeli. Deploy başlatılmadı.


### 28 Ekim ilk yayın — H-076
Kullanıcı talimatıyla deployment xfb9j6404vtl2cawynbqcz1y başlatılıp tamamlandı. main/e55842e build başarılı; Running (healthy), HTTPS ana sayfa ve /health status=ok görüldü. Önceki deploy başlatılmadı kayıtları tarihsel durumu belirtir. Sağlayıcı işlevleri, redeploy veri kalıcılığı ve ses gateway/worker yayını henüz uçtan uca doğrulanmadı.
