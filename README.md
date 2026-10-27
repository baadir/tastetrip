# TasteTrip

Qloo ile kişisel seyahat rotası; istek üzerine kültürel öneriler, hesapta kaydetme ve OpenAI uyumlu LLM ile durakları yeniden düzenleme. Python/Flask + SQLite + bağımlılıksız tarayıcı arayüzü. THY Travel Agent kart/rota yapıları ve uçuş adaptörü referans alınmıştır.

## Yerel geliştirme

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
Copy-Item .env.example .env  # yalnız .env henüz yoksa
# .env alanlarını doldur
.venv/Scripts/python -m app.server
```

http://localhost:8080 adresini aç. `.env` ve `data/` Git dışında tutulur. LLM sağlayıcısının `/chat/completions` ve `response_format: json_object` desteği olmalı; model adı açıkça LLM_MODEL ile seçilir. Model cevabı ayrıca sunucuda ID/gün/tekrar/sabit rezervasyon açısından doğrulanır. JSON mode tek başına yeterli sayılmaz.

Kullanıcı seçimi DeepSeek: `LLM_BASE_URL=https://api.deepseek.com`, `LLM_MODEL=deepseek-flash`. Model adı 21 Ekim 2026 tarihli [resmi başlangıç belgesinden](https://api-docs.deepseek.com/) doğrulandı; başka hesap/model kullanılırsa değiştirilebilir. Anahtarı `LLM_API_KEY` alanına gir. JSON output [resmi sözleşmeyle](https://api-docs.deepseek.com/guides/json_mode/) uyumludur. `.env` değiştirdikten sonra uygulamayı yeniden başlat; yapılandırma başlangıçta yüklenir.

```powershell
.venv/Scripts/python -m unittest discover -s tests -v
```

## Mevcut davranış

- Girişsiz keşif; HttpOnly anonim cookie üzerinden tercih ve taslak hatırlama. Cookie yalnız rastgele kimlik taşır. Kaydetme için gerçek kullanıcı adı/parola hesabı; SQLite’ta scrypt hash ve süreli hashlenmiş oturum token’ı.
- Qloo restoran/kafe/bar/otel/müze/park/özel yer adayları ve isim aramasından seçilmiş kültürel tercih sinyalleri. Eksik kategoriler görünür; şehirde tüm kategorilerin kapsandığı varsayılmaz.
- LLM bağlıysa bilinen adaylar günlere ayrılır. LLM yoksa açıkça etiketli Qloo aday taslağı gösterilir. Gerçek yol süresi, tarihli açılış ve rezervasyon müsaitliği entegrasyonu henüz yok; kesin uygulanabilir rota iddiası yok.
- Durak kartında adres ve Konumda gör. Varsa menü uygulama içi pencerede; kaynak site engellerse dış bağlantı mevcut.
- Öneri al yalnız kullanıcı tıklayınca sorgu yapar: kitap, film, podcast, sanatçı, dizi, oyun, marka ve destinasyon. Sanatçı çalınabilir playlist değildir; playback entegrasyonu yok.
- LLM ile mevcut durakları gün/sıra değiştirerek yeniden düzenleme. Yeni yer ekleme/çıkarma henüz desteklenmiyor; belirsiz istekte açıklama alınır. Düzenleme kaydedilmiş kopyayı otomatik değiştirmez.
- Kullanıcıya özel rota kayıtları ve yeniden açma. Başka hesabın rota kimliği erişim vermez. Çıkışta cihaz taslağı temizlenir.
- THY `flight_service.py` ile aynı Travelpayouts `/v1/prices/cheap` API adaptörü; şehir/havalimanı seçimi ve tam tarih filtresi. Önbellek fiyatlarıdır; canlı bilet/müsaitlik veya satın alma yok.

Restoran masa rezervasyonu; giriş, ayrıntı/özet onayı, kalıcı arama kuyruğu, Twilio/Anna görüşmesi, yetkili canlı dinleme, altyazı ve özet yoluna bağlandı. Ayrı voice-gateway ve reservation-worker gerekir; ilk sürüm ve doğrulama sınırları [rezervasyon belgesinde](docs/RESERVATION_IMPLEMENTATION.md). Müze/otel bileti, ödeme ve canlı alternatif teklif karar akışı henüz yok. Yeni ürün akışında bu tur gerçek telefon testi yapılmadı. Auth ilk sürümde yerel kullanıcı adı/parola; e-posta doğrulama, kurtarma ve OAuth henüz yok.

## Coolify / Hetzner CAX21

[Kurulum ve veri saklama](docs/COOLIFY_DEPLOYMENT.md). Dockerfile standart çok mimarili Python slim imajını kullanır; ARM64 sunucuda native build. Yerelde Docker mevcut değilse container/ARM64 çalıştırma doğrulaması yapılmış sayılmaz.

### İçerik dili
Kitap ve podcast önerilerinde dil seçimi vardır. Kitap dili Qloo kaydından; podcast dili Qloo iTunes kimliğine bağlı RSS yayıncı beyanından alınır. Dil eşleşmeyen/bilinmeyen kayıtlar seçili dile eklenmez. Filtre, aday havuzuyla sınırlıdır; her dilde envanter garantisi vermez. RSS metadata cache DATA_DIR içinde,7 gün; bilinmeyenler1 saat. defusedxml bağımlılığını requirements ile kur. Film dil seçimi henüz yok.

## 22 Ekim 2026 — Kullanıcı zevk profili entegrasyonu

Üç adımlı, atlanabilir onboarding ve Tercihlerim ekranı eklendi. Seyahat temaları, dil, mutfak/ortam tercihleri, zorunlu yemek/ortam koşulları, bütçe/tempo/ulaşım, aramayla doğrulanmış favoriler ve tekil kayıt dışlamaları ortak profilde tutulur. Kitap/podcast/film/sanatçı tercihleri mevcut Öneri al ekranından açık “genel tercihlerime kaydet” seçimiyle güncellenir. Yeni profil alanları seyahat verisinden ayrıdır.

- Profil API: `GET/PATCH /api/profile`, `POST /api/profile/reset`, `POST /api/profile/import`. `profile_version` ile değişiklik çakışmaları 409 verir; istemcinin verdiği kullanıcı kimliği kabul edilmez.
- Misafir profilinin hatırlama seçimi kapalı başlar: tanıma cookie'si oturumluk; açıkken 180 gün. Anonim master profil kayıtları son düzenlemeden 180 gün sonra servis başlangıcındaki temizlikte kaldırılır. Oturum cookie'sinin kapanması sunucudaki kaydın anında silinmesi anlamına gelmez; tarayıcının oturum geri yüklemesi cookie ömrünü uzatabilir.
- Hesap profili sunucuda saklanır ve aynı hesapla başka cihazda yüklenir. Girişte anonim profil otomatik aktarılmaz; alan bazında fark incelemesi sunulur. Çıkışta hesap profilinin sonraki kullanıcıya taşınması engellenir. Kayıtlı rotalar korunur.
- Eski medya seçimleri doğrulanmış profil gibi sessizce kabul edilmez; `legacy_pending` içinde korunur ve Tercihlerim son adımında yeniden eşleme mesajı gösterilir. Eski seyahat verileri kalıcı zevk tercihi olarak otomatik yükseltilmez.
- Her yeni rota ve içerik önerisi güncel master profili okur; yalnız ilgili sinyaller gönderilir. Yemek koşulları müze veya kitap sorgularına eklenmez. Zorunlu etiketler hem Qloo sorgusunda hem sonuçlarda denetlenir; sonuç yoksa kaldırılmaz.
- Arayüz şu an Türkçedir; ana dil ayrıca kaydedilir. Kitap/podcast dil doğrulaması korunur; bu çalışma canlı altyazı veya yeni film dili entegrasyonu eklemez. Serbest özel koşullar görünür teyit notudur; alerjen güvenliği veya sertifika kanıtı değildir.

Tasarım ve kabul planı: docs/ux/08-onboarding-and-taste-profile.md. Bu iş için yeni bağımlılık eklenmedi; mevcut SQLite volume ve Flask dağıtımı kullanılır.


## Restoran rezervasyonu (22 Ekim 2026)
Rota kartı → Rezervasyon planla → giriş → kesin koşullar ve işletme/yerel saat kontrolü → özet → Aramayı başlat. Bu aksiyon ayrı ücretli telefon aramasıdır; rota üretimi arama başlatmaz. Rezervasyonlarım üzerinden görüşme/sonuç yeniden açılır; Canlı dinle tarayıcı mikrofonu istemez. Telefon bitişi ve rezervasyon sonucu ayrıdır; dar kanıt zinciriyle otomatik kabul veya kullanıcı incelemesi gerekir. Belirsiz sonuç otomatik yeniden aranmaz. Prepare bağlamı korumak için rotayı hesaba kaydeder.

Yerelde web'e ek olarak iki süreç çalıştır:

```powershell
.venv/Scripts/python.exe -m app.voice_gateway
.venv/Scripts/python.exe -m app.reservation_worker
```

`.env.example` yeni servis ayarlarını içerir. `compose.yaml` Coolify için üç servis ve ortak kalıcı volume'u tanımlar. Varsayılan kullanıcı başına 10 girişim/gün, çağrı başına 180 saniye; ses kaydı yok, konuşma metni/özet 30 gün. Bu parasal toplam maliyet garantisi değildir. Ayrıntılar ve gerçek telefon testinin henüz yapılmadığı sınırlar [RESERVATION_IMPLEMENTATION.md](docs/RESERVATION_IMPLEMENTATION.md).

## 26 Ekim: Sohbet merkezli TasteTrip
Ana giriş artık konuşarak tercih öğrenir ve şehir/tarih/gün/kişi toplar. DeepSeek çıkarımları sunucu doğrulamasından sonra SQLite master profile kaydedilir; rota/içerik Qloo yolları aynı profili okur. Sohbet endpointleri GET/POST `/api/chat`, POST `/api/chat/clear`; mevcut LLM env ayarları kullanılır. Yeni bağımlılık yok. Güncel davranış ve sınırlar: docs/ux/09-chat-first-journey.md. Test: `.venv/Scripts/python.exe -m unittest discover -s tests -q`.

## D-033 / H-071 — Tam konuşma deneyimi (26 Ekim)
Açılış/yan menü ve ayrı yardımcı ekranlar yerini tek konuşma akışına bıraktı. Uçuş ve rezervasyon alanları konuşmayla toplanır; güvenli giriş, profil, sonuçlar ve açık arama onayı konuşma kartlarıdır. 117 test; güncel kapsam/sınırlar docs/ux/10-complete-conversation.md. Yeni bağımlılık yok, Coolify/CAX21 mimarisi değişmedi; deploy veya gerçek telefon yapılmadı.
