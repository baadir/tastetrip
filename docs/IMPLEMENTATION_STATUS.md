# İlk çalışan sürüm — 21 Ekim 2026

Uygulama: `app/server.py`, `app/providers.py`, `app/planner.py`, `app/static/`. Ürün kabulünün tamamı bitmiş değildir. Kaynak bağlamı PRODUCT_REQUIREMENTS, PROJECT_HISTORY, UX 06/07.

## Uygulanan ve doğrulanan

- Responsive genel seyahat formu: şehir/ülke, tarih, gün, kişi, kategoriler, bütçe, tempo, ulaşım, konaklama, serbest istek; Qloo aramasıyla seçilmiş kültürel entity sinyalleri.
- Girişsiz keşif ve taslak düzenleme. Kaydetme/rezervasyon girişinde login kapısı. Rastgele anonim HttpOnly/SameSite cookie; tercihler ve taslak SQLite’ta. Aynı tarayıcı yenilendiğinde taslak geri geldi.
- Kullanıcı adı/parola auth, scrypt hash, süreli ve sunucuda hashlenmiş oturumlar; hesap bazında kayıtlı rota erişimi. Kaydet, listele, yeniden aç. Bağlantı sınırlarında auth kontrol edilir.
- Qloo mekânlarıyla günlük kartlar; gerçek fotoğraf/adres/Maps Place ID. Eksik metadata üretilmez. Model yalnız mevcut ID’leri sıralar.
- Kullanıcı tıklamasıyla kitap/film/podcast/sanatçı/dizi/oyun/marka/destinasyon önerileri. Otomatik içerik sorgusu yok. Qloo isim araması kültürel tercih seçimine bağlı.
- DeepSeek OpenAI uyumlu JSON adaptörü, bilinen ID/sayı/tekrar kontrolü; mevcut durakları günler arasında düzenleme, sürüm çakışması kontrolü; onaylı rezervasyonun gününü değiştirme engeli. Kayıtlı kopya ayrıca kaydetmeden değişmez.
- Travelpayouts şehir/havalimanı çözümleme + THY referanslı `/v1/prices/cheap` adaptörü, tam gidiş/dönüş tarihi ve tek yön/gidiş-dönüş ayrımı; varsa partner arama linki. Bilet satın alma yok.
- Coolify için native ARM64 uyumlu Dockerfile, non-root Gunicorn, healthcheck, `/app/data` kalıcı dizini ve Compose.

## Gerçek servis kontrolleri

- Paris kategori örneklerinde restoran, kafe, otel, müze, park ve gezilecek yerler döndü. İlk 8 bar adayında ana kategori süzgeci sonrası sonuç kalmadı; 20 adayda 3 bar döndü. Uygulama kategori başına en az 20 ham aday ister; tüm şehri kapsayan test değildir.
- 8 kültürel türün her biri bir restoran sinyaliyle 4’er sonuç verdi. Bu, kişiselleştirme kalitesi veya tüm entity ilişkilerinin doğrulaması değildir.
- Tarayıcıda Paris için DeepSeek+Qloo rota üretildi. İkinci gün Musée National Picasso-Paris kaydı ilk güne doğal dil talimatıyla taşındı, sürüm 1→2 oldu; iki gündeki diğer ID’ler korundu. İşletme/saati değiştiren dış işlem yapılmadı.
- Tarayıcıda kafe durağı → Öneri al → Kitap akışında gerçek Qloo kitapları geldi. Kaydet düğmesi giriş dialogunu açtı.
- Aviasales 20–23 Kasım 2026 IST→PAR tam tarihli gidiş-dönüş kontrolünde bir önbellek teklifi verdi; satın alma/gerçek müsaitlik doğrulanmadı. Fiyat zamana bağlıdır. Tek yön isteğinde gidiş-dönüş kaydı gösterilmesi engellendi.
- 320 px tarayıcı kontrolünde form ve kartlar yatay taşmadı (body clientWidth/scrollWidth=305). Dar tarih alanı ek tek sütun kuralıyla iyileştirildi. Tüm tarayıcı/erişilebilirlik kapsamı test edilmedi.
- 10 otomatik test: giriş anı/kaydetme/açma, hesap izolasyonu, cookie tercihleri, CSRF, hatalı girdiler, LLM eksikliğinde taslak koruma, sürüm uyuşmazlığı, bilinmeyen/tekrarlanan/eksiltilen ID, müze taşıma ve sabit rezervasyon engeli, güvenli URL ve Place ID, tam tarihli uçuş ayrımı, model JSON nesnesi kontrolü. Dış servisler bu testlerde fixture/mock; canlı denemeler yukarıda ayrı.
- Python compile, JS syntax ve `docker compose config -q` geçti. Docker daemon kapalı olduğundan imaj build/çalıştırma ve CAX21 native runtime doğrulanmadı. Sunucu deploy yapılmadı.

## Açık uygulama işleri

1. Harita üzerinde çok duraklı rota ve gerçek yol süreleri, tarihli açılış/kapanış kontrolü; şu an sıralı günlük **taslak**, kesin saatli uygulanabilir program değil. LLM başlangıç prompt’u tempoya göre 3–5 durak/azami 2 müze önerir; düzenlemede kullanıcının tüm durakları koruma isteği önceliklidir.
2. Telefon rezervasyon servisleri, canlı ses/çeviri, otel/müze rezervasyon kanalları. UI desteklenmediğini açık söyler; arama yapılmaz.
3. LLM ile yeni durak ekleme/çıkarma, tam talimat başarı değerlendirmesi ve daha zengin diff/onay akışı. İlk sürüm mevcut ID’lerin gün/sıra düzenlemesine odaklıdır.
4. Müziği gerçek parça/playlist’e bağlama, playback/çevrimdışı erişim ve medya kartlarını rota kaydına ekleme.
5. Auth kurtarma/doğrulama/OAuth; üretim abuse/bütçe limitleri, eski kayıt temizleme ve otomatik yedek/geri yükleme doğrulaması. İlk sürüm tek instance SQLite’tır.

LLM ve uçuş anahtarları kullanıcı tarafından yerel `.env` dosyasına girildi; varlıkları kontrol edildi, içerikleri log/belgelere yazılmadı. Aynı alanlar Coolify runtime environment’a aktarılmalı. `.env` değişikliği için restart gerekir.

Son tarayıcı kontrolünde uçuş havalimanı seçimi ve fiyat sorgusu da tamamlandı; gidiş-dönüş teklif ve partner arama bağlantısı görüldü. Son kod değişikliklerinden sonra 10 test, syntax ve Compose config tekrar geçti. Uygulama yeni yapılandırmayla yeniden başlatıldı.

## H-017 — Türe özel zevk toplama
Kitap/film ve diğer içerik türlerinde ayrı sevilen eser seçimi eklendi. Qloo araması tür filtresiyle gösterilir; seçilen 1–5 entity öneri sinyalidir. Tercih yoksa otomatik kişiselleştirme iddiası yerine açık atlama gerekir. Seçimler öneri isteğiyle sunucuda hatırlanır; türler birbirinden ayrıdır. 11 test geçti.

## H-018 — Podcast konu girişi
Podcast için eser yerine keyword → DeepSeek normalizasyonu → Qloo tag seçimi → konu filtreli öneri var. Türkçe bilim/uzay örneği canlı doğrulandı; her dil ve yayın dili garantisi yok. Kitap/film önceki eser seçimini korur. Toplam 12 test geçti.

## H-021 — Kitap ve podcast dil filtresi
Dil seçimi uygulandı: kitapta Qloo language/ISBN, podcast’te iTunes→RSS channel language. Seçili dilde en fazla20 adaydan ilk4 eşleşme; bilinmeyenler hariç, dil otomatik esnetilmez. Metadata kaynağı kartta gösterilir. Ayrı dil tercihleri anonim cookie kimliğiyle hatırlanır. RSS public-IP pinleme/redirect/timeout/boyut ve defused XML kontrolleriyle sunucuda alınır; kalıcı SQLite cache7 gün/negatif1 saat. İlk canlı kontroller İngilizce için başarılı; Türkçe kapsam garantisi yok.20 test geçti. Film filtresi yok; önceki H-019/H-020 sonuçlarının podcast uygulama-eksikliği kısmı bu ekle güncellenir, doğrudan Qloo dil filtresi bulgusu değişmez.

## H-023 — Kitap konusu ve podcast bağlantıları
Kitapta keyword ve sevilen kitap modları birlikte var; book konu etiketleri entity sinyallerinden ayrı gönderilir. Apple Lookup linkleri cache/yanıt üzerinden podcast kartlarına taşınır; Dil fark etmez seçeneğinde de alınır. RSS hatası Apple linkini silmez. Türkçe kitap konu eşleşmesi ve iki Apple podcast URL’si canlı doğrulandı;22 test geçti.

## H-068 — Onboarding ve ortak kullanıcı profili (22 Ekim 2026)
Üç adımlı atlanabilir onboarding, Tercihlerim, sürümlü hesap/ziyaretçi profili, dinamik gerçek mutfak/yer/eser seçimi, içerik tercih düzenleyicisi ve açık hesap aktarımı eklendi. Rota ve içerik önerileri güncel merkezi profili kullanır; tek seferlik seçimler profili otomatik değiştirmez. Eski medya tercihleri yeniden doğrulama için korunur. 71 test geçti; 10 canlı Qloo kontrat kontrolü ve tarayıcı kayıt/yenileme kontrolü başarılı. Canlı rota denemelerinde önce iki 503, ardından iki 200 görüldü; sebebi kesinleştirilmemiş hatalar saklanmadı diye yok sayılmaz. Ayrıntılar README ve UX08 son bölümünde. Coolify/ARM64 deploy yapılmadı; bu kayıt rezervasyon ürün akışının tamamlandığı anlamına gelmez.

## H-069 — Restoran rezervasyonu entegrasyonu (22 Ekim 2026)
Rota kartı→login→koşullar/yerel saat/işletme kontrolü→özet/onay→durable outbox/worker→Twilio/Anna→dinleme/altyazı/özet ve sonuç yapısı bağlı. TR/EN dar readback+staff kabul kanıtı veya kullanıcı incelemesi; LLM özeti onay yazmaz. Unknown otomatik aranmaz, stop masayı iptal etmez. Onaylı rota durağı korunur. 102 test geçti; küçük canlı TTS/LLM ve sentetik tarayıcı/WS kontrolleri var. Gerçek ürün telefon görüşmesi, alternatif karar kartı ve Coolify/ARM64 testi henüz yok. Ayrıntı docs/RESERVATION_IMPLEMENTATION.md; eski uygulama-eksikliği kayıtları tarihsel olarak korunur.

## 26 Ekim 2026 — Sohbet merkezli ana yüzey
D-032/H-070: DeepSeek konuşmadan açık genel tercihleri çıkarır; şema/kaynak doğrulama ve atomik SQLite kaydıyla mevcut master profile bağlanır. Seyahat taslağı ayrıdır. Sohbetten rota oluşturma/düzenleme aksiyonları, Qloo eşleşme seçimi, kayıt makbuzu ve tek sayfalık tercih inceleme eklendi. 110 test; ayrı QA DB ile canlı DeepSeek ve Qloo rota/reload kontrolü. 375px içerik genişliğinde yatay taşma görülmedi. Rezervasyon/uşuş yardımcı formları korunur; deploy yok. Güncel sözleşme docs/ux/09-chat-first-journey.md.

## D-033 / H-071 — Tam konuşma deneyimi (26 Ekim)
Açılış/yan menü ve ayrı yardımcı ekranlar yerini tek konuşma akışına bıraktı. Uçuş ve rezervasyon alanları konuşmayla toplanır; güvenli giriş, profil, sonuçlar ve açık arama onayı konuşma kartlarıdır. 117 test; güncel kapsam/sınırlar docs/ux/10-complete-conversation.md. Yeni bağımlılık yok, Coolify/CAX21 mimarisi değişmedi; deploy veya gerçek telefon yapılmadı.
