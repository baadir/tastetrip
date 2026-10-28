# TasteTrip Concierge — Project History

Current update — D-039/H-082 (28 October 2026): reservation verification, paid-call approval and live call use a popup over chat; terminal call summary returns to chat. Implemented and tested locally; not deployed. See docs/ux/12-reservation-call-popup.md.

İlk kayıt: 20 Ekim 2026. Tarihler Europe/Istanbul bağlamındadır.

## Güncel durum

28 Ekim D-034/H-074: Proje github.com/baadir/tastetrip main dalına yüklendi. Coolify Tastetrip/production web kaynağı, HTTPS tastetrip.bahadirciftci.work domaini, Dockerfile/8080, kalıcı /app/data volume ve yedi sır olmayan runtime değişkeni kaydedildi. Deploy başlatılmadı; API sırları/LLM_MODEL ve tam ses servisleri yayın aşamasında tamamlanacak. docs/COOLIFY_TASTETRIP_PLAN.md güncel.

26 Ekim D-033/H-071: Deneyimin bütünü tek konuşma akışında; ayrı açılış/yan menü/form ekranları kaldırıldı. Uçuş ve rezervasyon bilgileri DeepSeek ile konuşmadan alınır; rota, tercih, içerik, güvenli giriş, listeler ve canlı görüşme aynı konuşmada karttır. 117 test; ayrı QA DB ile canlı rezervasyon taslağı/onay kapısı ve uçuş sonucu görüldü. docs/ux/10-complete-conversation.md güncel. Gerçek telefon/deploy yok.

26 Ekim D-032/H-070: Ana deneyim sohbet merkezli. DeepSeek açık genel tercihleri mevcut şema üzerinden atomik olarak kullanıcı/ziyaretçi profiline kaydeder; tek seyahat istekleri ayrı. 110 test ve ayrı QA DB ile canlı sohbet→Qloo rota/reload kontrolü var. docs/ux/09-chat-first-journey.md güncel. Rezervasyon/uşuş ayrıntı formları korunur; deploy yapılmadı.

22 Ekim D-031/H-069: Restoran rezervasyonu ürün akışına bağlandı; 102 test, sentetik UI/WS ve küçük canlı TTS/LLM kontrolleri var. Gerçek telefon/rezervasyon ve Coolify yayın testi yok. docs/RESERVATION_IMPLEMENTATION.md güncel kapsam ve sınırları tanımlar. Eski “rezervasyon bağlı değil” özetleri tarihsel.

22 Ekim D-030/H-068: Onboarding ve ortak zevk profili uygulandı; 71 test, canlı Qloo parametre kontrolleri ve tarayıcı kayıt/yenileme kanıtı var. Hesaba açık alan aktarımı, session/device tercihi ve ilgili kategori sorguları bağlı. Daha eski uygulama öncesi özetler tarihsel kalır; güncel kapsam README ve UX08 son bölümünde.

22 Ekim D-029/H-067: Onboarding ve ortak kullanıcı tercih profili yeni kapsam. docs/ux/08-onboarding-and-taste-profile.md akış, soru seti, veri modeli, kategoriye göre Qloo eşlemesi ve kabul planını içerir. Kalıcı ve tekrar kullanılan tercih verisi kullanıcı talebi; adım sırası henüz kabul edilmiş veya uygulanmış sayılmaz. Mevcut kodda bağımsız master profil yok. Aşağıdaki eski özetler tarihli yeni kayıtlarla birlikte okunmalıdır.

21 Ekim D-018/P-006/H-025: Aramada maliyet önceliği kullanıcı talimatı. Güncel teknik öneri Twilio + kendi gateway + Deepgram + DeepSeek + Polly Standard; docs/VOICE_COST_COMPARISON.md. Önceki Vapi önerisi P-005 tarihsel; arama henüz uygulanmadı.

21 Ekim uygulama güncellemesi (D-010–D-012/H-015): app/ ilk çalışan sürüm; DeepSeek+Qloo üretim/düzenleme ve Aviasales erişimi canlı doğrulandı. Login aksiyonda, cookie ile anonim hatırlama, hesapta rota kayıtları var. README ve docs/IMPLEMENTATION_STATUS.md önce okunmalı. Coolify/CAX21 Docker hedefi hazırlandı; deploy ve ARM64 runtime testi yapılmadı. Rezervasyon ve gerçek yol/saat entegrasyonu henüz yok.

21 Ekim D-009: THY Travel Agent kartları referans; rota anlarına kitap/film/podcast/müzik önerileri eklendi. docs/ux/07-thy-components-and-content.md kaynak incelemesini ve henüz uygulanmamış uyarlamayı açıklar.

21 Ekim 2026 D-008: Ürün restoran/kafe/bar/otel/gezilecek yerlerden çok günlük kişisel rota ve durak rezervasyonlarına genişledi. Yeni baseline PRODUCT_REQUIREMENTS.md FR-09–FR-11; UX taslağı docs/ux/06-trip-itinerary.md. Henüz uygulanmadı.

21 Ekim 2026 kart tasarımı güncellemesi: P-004 iki etkileşimli restoran kartı önerir; kullanıcı onayı beklenir. Ayrıntılar `docs/ux/05-restaurant-cards.md`; önceki kararlar korunur.

- **Aşama:** Ürün gereksinimleri ve erken UX çalışması; ilk taslak reddedildikten sonra ikinci görsel ve geçişli konsept hazırlandı. Gerçek uygulama ve servis entegrasyonları geliştirilmedi. Bkz. H-008 ve P-002.
- **API erişimi:** Kullanıcı anahtar e-postasını paylaştı; 21 Ekim 2026'da Tags ve Insights ile canlı erişim doğrulandı. Anahtar değeri proje dosyalarına kaydedilmedi. Bkz. H-009 ve `docs/QLOO_LIVE_VALIDATION.md`.
- **Hackathon:** Kullanıcının Register işlemi sonrası proje taslağı oluşturuldu. Son kontrolümüzde 3/5 adım tamamlanmıştı; nihai proje teslimi yapılmadı. Bkz. H-003.
- **Çalışma adı:** TasteTrip Concierge; asistanın seçtiği geçici taslak adı. Kullanıcı tarafından kesin marka kararı verilmedi.
- **UX:** Seyahat odaklı, akıllı asistan, desktop ve mobil responsive. İlk görsel taslak kullanıcı tarafından metin ağırlıklı bulundu ve reddedildi; görsel olarak çekici, akışkan ve geçişli bir yön isteniyor (D-006). Login zamanı ve chatbot/wizard/hibrit modeli kesinleşmedi.
- **Şimdiki iş:** 52 ek API deneyi tamamlandı; `docs/ux/04-api-backed-ux-recommendations.md` içindeki P-003 önerilerini kullanıcıyla değerlendir. Gerçek etiketler ve örnek metadata kanıtlandı; restoran kategorisi uygulamada ayrıca süzülmeli. Login, telefon ve dil kararları henüz kapanmadı.
- **Son kalıcı karar:** D-006 — metin ağırlıklı ilk taslağı görsel ve akışkan bir deneyimle yeniden ele al; D-005 geçmiş koruma kuralı devam ediyor.

Bu özet değişebilir. Aşağıdaki tarihli kayıtlar geçmişin izidir; silinmez. Yeni kullanıcı talimatı, eski kararın üzerine yeni bir karar kaydıyla işlenir.

## Kayıt düzeni

Durumlar:

- **KARAR:** Kullanıcının açık isteği/onayıyla belirlenmiş yön veya kapsam.
- **ÖNERİ:** Asistanın sunduğu, henüz kullanıcı tarafından kesinleştirilmemiş yaklaşım.
- **BULGU:** Doküman veya gözlenen arayüzle desteklenen bilgi; kapsam ve kontrol tarihi belirtilir.
- **DURUM:** Yapılan iş veya kullanıcının bildirdiği gelişme; kanıt sınırı belirtilir.
- **AÇIK:** Çözülmemiş soru/bağımlılık; karar gibi uygulanmaz.

Yeni kayıt şablonu:

```markdown
### D/H/P/O-XXX — Kısa başlık
- Tarih:
- Tür / durum:
- Kaynak / kanıt sınırı:
- Karar, bulgu veya olay:
- Gerekçe:
- Etkilenen belgeler:
- Önceki kayıtla ilişki: yeni / tamamlar / değiştirir / düzeltir [ID]
- Sonraki adım / çözülme koşulu:
```

Bir karar değiştiğinde önceki kaydı yeniden yazmak yerine yeni kayıtta “D-XXX kararını değiştirir” denir. Tarihsel kaydın durumunu değiştirmek yerine değişiklik ilişkisi yeni kayıtta tutulur. Özet ve ilgili çalışma belgeleri de yeni karara uyarlanır. Sıradan ifade düzeltmeleri dışında geçmişe müdahale yapılmaz; maddi hatalar düzeltme kaydıyla açıklanır.

## Tarihsel kayıtlar

### H-001 — Hackathon incelemesi ve kaynak belgeler
- Tarih: 20 Ekim 2026.
- Tür / durum: BULGU ve DURUM.
- Kaynak: Resmi Devpost sayfaları ve Qloo dokümanları; bağlantılar ilgili belgelerde.
- Olay: Hackathon koşulları ve çalışma rehberi kaydedildi. Demo URL'si ve public repo nihai teslimde isteniyor. API anahtarı için ayrı talep formu var; o form demo veya repo URL'si istemiyor.
- Belgeler: `HACKATHON_REQUIREMENTS.md`, `WORKING_GUIDE.md`, `QLOO_CAPABILITIES.md`.
- Sınır: Kurallar güncellenebilir; nihai teslim öncesi yeniden kontrol gerekir.

### D-001 — Ürün kapsamı: seyahatte restoran keşfi ve telefonla rezervasyon
- Tarih: 20 Ekim 2026.
- Tür / durum: KARAR — kullanıcı tarafından tanımlanan ürün fikri.
- Kaynak: Kullanıcının ürününü açıkladığı mesaj.
- Karar: Müşterinin Qloo'ya uygun tercih girdilerini al; restoran seçenekleri sun; müşteri restoranı seçsin; sistem müşterinin koşullarıyla restoranı telefonla arayıp rezervasyon istesin.
- Deneyim: Müşteri görüşmenin iki tarafını canlı dinleyebilsin; görüşme ana dilinden farklıysa ana dilinde canlı altyazı görsün. Ses için ElevenLabs gibi bir TTS servisi kullanılsın.
- Gerekçe: Tercihe uygun keşif ile dil engelini aşan rezervasyonu aynı akışta birleştirmek.
- Belge: `PRODUCT_REQUIREMENTS.md`.
- Sınır: ElevenLabs kesin sağlayıcı seçimi değil. Belgedeki ayrıntılı kabul kriterleri asistanın kapsam açılımıdır; tüm teknik/operasyonel öneriler ayrı kullanıcı onayı almış sayılmaz.
- Sonraki adım: API ve telefon yeteneklerini doğrulayıp tasarım/geliştirme kapsamını netleştirmek.

### H-002 — Qloo veri ve girdi modeli incelemesi
- Tarih: 20 Ekim 2026.
- Tür / durum: BULGU; canlı API testi yapılmadı.
- Kaynak: Qloo resmi dokümanları ve `qloo/docs-public` deposu; ilgili bağlantılar önceki belgelerde ve konuşmada.
- Bulgu: API alanına göre enum, sayı, entity/tag kimliği veya sınırlı arama metni bekliyor. Kullanıcının doğal dil isteğini uygulama bu girdilere dönüştürecek. Etiketler Tags/Tag Types uçlarından keşfediliyor.
- Belirsizlikler: Tam restoran tag kataloğu, “sakin/romantik” gibi etiketlerin varlığı, hedef şehirlerde veri yoğunluğu, telefon ve hazır Maps bağlantısı alanları doğrulanmadı.
- Sınır: Global kapsam açıklaması Hindistan'daki her restoranın bulunduğu veya her kaydın tam olduğu anlamına gelmiyor. Genel doküman ile hackathon ortamında farklar olabilir.
- Sonraki adım: Anahtar gelince desteklenen girdiler, şehir sonuçları ve gerçek metadata'yı test etmek.

### H-003 — Devpost proje taslağı
- Tarih: 20 Ekim 2026.
- Tür / durum: DURUM — tarayıcı arayüzünde gözlendi.
- Olay: Kullanıcı Devpost'a giriş yaptı ve hackathon Register işlemini yaptı. Proje adı, elevator pitch ve İngilizce proje hikâyesi kaydedildi; arayüz 3/5 adım ve DRAFT gösterdi.
- Ad: `TasteTrip Concierge` — geçici çalışma adı.
- Taslak: [Devpost yönetim sayfası](https://devpost.com/submit-to/31054-qloo-agentic-hackathon/manage/submissions/1248249-tastetrip-concierge/project_details/edit).
- Eksikler: Çalışan demo ve public repo URL'leri yok. Additional info başlangıç alanları yazıldı; son bölüm kaydedilmedi. Nihai submission yapılmadı.
- Belge: `DEVPOST_APPLICATION_DRAFT.md` ilk hazırlık kopyasıdır; giriş öncesi durum bölümü tarihsel kalmıştır. Güncel dış işlem durumu için bu kayıt esas alınır.
- Sonraki adım: Ürün çalışır hale gelince bağlantıları ve gerçek uygulama/test bilgilerini tamamlamak.

### H-004 — API anahtarı talep formu
- Tarih: 20 Ekim 2026.
- Tür / durum: DURUM — form içeriği tarayıcıda görüldü; tamamlanması kullanıcı tarafından bildirildi.
- Olay: Kullanıcının doldurduğu formdaki eksik Project Idea alanı İngilizce tamamlandı. Asistan sözleşme kutularını işaretlemedi ve Gönder'e basmadı. Sonraki mesajda kullanıcı “form dolduruldu” dedi; konuşma anahtar bekleme durumuna geçti.
- Kanıt sınırı: Gönderim başarı ekranı veya anahtar e-postası asistan tarafından görülmedi. Bu nedenle “talep onaylandı” ya da “anahtar mevcut” olarak kaydedilmez.
- Kişisel bilgiler: Forma girilen kimlik/iletişim bilgileri bu loga kopyalanmaz.
- Sonraki adım: Kullanıcı anahtarın geldiğini bildirince sır değeri loga yazılmadan erişimi doğrulamak.

### D-002 — Seyahat odaklı, responsive akıllı asistan
- Tarih: 20 Ekim 2026.
- Tür / durum: KARAR — kullanıcı talebi.
- Karar: Ürün seyahat odaklı bir UX sunacak; akıllı asistan gibi çalışacak; desktop ve mobilde responsive olacak.
- Açık bırakılan konu: Chatbot, adımlı asistan veya hibrit etkileşim modeli UX çalışmasında belirlenecek.
- Gerekçe: Kullanıcının seyahat bağlamını ve farklı cihaz kullanımını merkeze almak.
- Belgeler: `docs/ux/01-entry-and-login.md`, `PRODUCT_REQUIREMENTS.md`.
- Sonraki adım: Etkileşim modeli ve responsive ekran davranışlarını taslakta karşılaştırmak.

### H-005 — UX skill projeye eklendi
- Tarih: 20 Ekim 2026.
- Tür / durum: DURUM.
- Kaynak: Kullanıcının uygun UX skill bulup projeye dahil etme isteği.
- Olay: Mevcut finans odaklı skill uygun bulunmadı. GitHub adayları incelendi; `magnus919/agent-skills` içinden `product-design-and-ux` kuruldu.
- Yol: `.agents/skills/product-design-and-ux/SKILL.md`.
- Belgeler: `docs/ux/SKILL_REVIEW.md`, `AGENTS.md`.
- Sınır: Skill bir yöntem kaynağıdır; kullanıcı araştırması veya ürün kararının kanıtı değildir. Kaynak/lisans inceleme sınırları inceleme belgesinde kayıtlı.

### D-003 — UX'te önce kullanıcı durumu, login ve açılış
- Tarih: 20 Ekim 2026.
- Tür / durum: KARAR — kullanıcı yönlendirmesi.
- Karar: UX çalışması önce kullanıcının mevcut durumunu, login'in yerini ve uygulama açılış sayfasını ele alacak.
- Belge: `docs/ux/01-entry-and-login.md`.
- Gerekçe: Ana yolculuğa geçmeden giriş bağlamını anlamak.
- Sonraki adım: İlk ziyaret, geri dönüş, aktif işlem ve girişten dönüş durumlarını taslaklaştırmak.

### P-001 — Misafir keşif, arama öncesi login ve hibrit asistan
- Tarih: 20 Ekim 2026.
- Tür / durum: ÖNERİ — kullanıcı onayı yok; kesin karar değildir.
- Kaynak: Asistanın ilk UX değerlendirmesi.
- Öneriler: Keşfi girişsiz başlat; restoran ve koşullar seçilince telefon aramasından önce login iste. Giriş otomatik arama başlatmasın. Doğal dil ile seçenekli akışı birlikte sun. İlk ekranda uzun tercih anketi zorunlu olmasın.
- Açılış durumları: Yeni ziyaretçi için hedef/istek alanı, geri dönene devam kartı, aktif aramaya canlı görüşme girişi, yaklaşan rezervasyona özet.
- Belge: `docs/ux/01-entry-and-login.md`.
- Sınır: Kullanıcı login sorusuna açık onay vermedi; API girdilerine ilişkin sorularla devam etti. Dolayısıyla bu yaklaşımı kabul edilmiş mimari/UX kararı olarak uygulama.
- Sonraki adım: D-004 uyarınca taslak olarak koru; API sonrası gerçek girdi ve veriyle yeniden değerlendir.

### D-004 — API bekleme ve geçici UX taslağı
- Tarih: 20 Ekim 2026.
- Tür / durum: KARAR — kullanıcının son talimatı.
- Karar: API anahtarı beklenecek. Anahtar gelene kadar UX'te geldiğimiz nokta çizilebilir ve belgelenebilir. API'ye bağlı nihai UX seçimleri, katalog ve veri kapsamı görüldükten sonra son rötuşlarla netleştirilecek.
- Gerekçe: Hazır seçenekleri veya veri yeteneklerini gerçek API karşılığı görülmeden kesinleştirmemek.
- İlişki: D-003'ü tamamlar; P-001'i onaylamaz veya reddetmez, geçici öneri olarak korur.
- Sonraki adım: Düşük detaylı UX taslakları yapılabilir; canlı API doğrulaması veya kesin tag listesi iddiası yapılmaz.

### D-005 — Önce geçmişi oku, kararları silmeden ilerle
- Tarih: 20 Ekim 2026.
- Tür / durum: KARAR — kullanıcının son talimatı.
- Karar: Proje geçmişi kalıcı bağlam olarak tutulacak. `Starthere.md` önce geçmişi okumayı, sonra aksiyon almayı isteyecek. Alınan kararlar sessizce ezilmeyecek.
- Uygulama: Bu log oluşturuldu; `Starthere.md` ve kök `AGENTS.md` okuma sırasını belirtir. Karar değişiklikleri eski kaydı silmeden yeni kayıtla izlenir.
- Gerekçe: Yeni oturum ve bağlam kaybında önceki kararların korunması.
- Belgeler: `Starthere.md`, `PROJECT_HISTORY.md`, `AGENTS.md`.
- Sonraki adım: Her kalıcı gelişmede loga yeni kayıt ekle; değişiklik varsa güncel özeti de eşleştir.

### H-006 — İlk görsel ve etkileşimli UX taslağı
- Tarih: 20 Ekim 2026.
- Tür / durum: DURUM ve ÖNERİ; ürün kararı onayı değil.
- Kaynak: Kullanıcının “UX'e başla” talimatı; D-002, D-003 ve D-004 kapsamı.
- Olay: İlk ziyaret, geri dönen kullanıcı ve rezervasyon öncesi giriş/özete dönüş ekranları hazırlandı. Doğal dil ve seçeneklerle ilerleme yolları aynı ilk ekranda denetlenebilir hale getirildi.
- Karar ilişkisi: P-001 görselleştirildi; onaylanmış sayılmadı. D-004'teki API bekleme kararı korunuyor.
- Belgeler: `docs/ux/02-entry-prototype.md`; yerel kontrol kopyası `docs/ux/entry-preview.html`. Sohbet içi çizim kaynağı: `C:/Users/ciftc/.codex/visualizations/2026/10/20/01a15995-d9f1-79a3-9b9f-8c124c6ce728/tastetrip-entry.html`.
- Kontrol: Yerel tarayıcıda boş şehir hatası, seçenekli yol, giriş simülasyonu ve özete dönüş denendi; 390px görsel inceleme ve 320/390px kök yatay taşma kontrolü yapıldı.
- Sınır: Sahte restoran ve rezervasyon bilgisi; gerçek hesap, API, telefon veya kalıcı saklama yok. Araştırma veya erişilebilirlik uygunluğu sonucu değil.
- Sonraki adım: Açılış yoğunluğu ve etkileşim yolu üzerine kullanıcı geri bildirimi; API sonrası gerçek seçeneklerle revizyon.

### D-006 — İlk görsel taslak reddedildi; görsel ve geçişli UX yönü
- Tarih: 20 Ekim 2026.
- Tür / durum: KARAR ve kullanıcı geri bildirimi.
- Kaynak: Kullanıcı “Beğenmedim”, “Düz metin yapmışız sadece”, “daha akışkan, geçişli bir ux” dedi; skill kullanımını ve bugüne kadarki kararların loglanmasını tekrar istedi.
- Karar: H-006'daki ilk taslak onaylanmış tasarım değildir. Görsellerin belirgin rol oynadığı, daha çekici ve adımlar arasında süreklilik sağlayan yeni bir UX hazırlanacak. UX skill yöntemi uygulanacak.
- İlişki: H-006'nın görsel yönünü reddeder; önceki kayıt ve dosyaları silmez. D-001 ürün kapsamı, D-002 responsive beklentisi ve D-004 API sonrası kesinleştirme kararı değişmez. P-001'deki login ve hibrit model hâlâ onay bekleyen öneridir.
- Sonraki adım: Yeni görsel yön ve etkileşimli geçiş prototipi; geri bildirim ve doğrulama sınırlarını ayrıca kaydet.

### H-007 — Konuşma geçmişi ve karar bütünlüğü kontrolü
- Tarih: 20 Ekim 2026.
- Tür / durum: DURUM.
- Olay: Mevcut konuşmadaki kullanıcı kararları D-001–D-006 ile eşleştirildi: ürün fonksiyonları; seyahat/mobile-desktop; önce state/login/açılış; API beklerken taslak ve sonrasında kesinleştirme; geçmiş koruma; yeni görsel yön. Skill kurulumu, Devpost taslağı ve API formu olayları H-001–H-006'da korunuyor.
- Bulgular: Qloo'nun ML tercih motoru ile bizim konuşma/rezervasyon agentımızın ayrı sorumlulukları olduğu açıklanmıştı. Bu teknik bilgi yeni bir kullanıcı UX kararı değildir. API girdilerinin formatları dokümandan biliniyor; tam tag listesi ve gerçek restoran metadata'sı canlı doğrulama bekliyor.
- Korunan açıklıklar: Çalışma adı ve sağlayıcılar kesinleşmedi; girişsiz keşif ve rezervasyon öncesi login kullanıcı tarafından onaylanmadı. API formunun gönderim ekranı görülmedi. Proje geliştirildi veya hackathon'a nihai teslim yapıldı diye kaydedilmedi.
- Sonraki adım: Yeni kararları açık kullanıcı talimatına dayandır; tasarım yorumlarını ÖNERİ olarak ekle.

### P-002 — Fotoğraf odaklı, tek karar/adım concierge önerisi
- Tarih: 20 Ekim 2026.
- Tür / durum: ÖNERİ — kullanıcı onayı yok.
- Kaynak: D-006 görsel çekicilik ve akışkanlık talebine asistanın tasarım yorumu.
- Öneri: Büyük seyahat/yemek atmosfer fotoğrafı, sıcak vurgu rengi ve Yerin → Planın → Zevkin → Özetin akışı. Adımlar arasında hareketli geçiş ve aynı görselde kadraj/çerçeve sürekliliği. Dar ekranda kısa görsel ve tek sütun.
- Login: Erken giriş veya planı saklama isteğinde simülasyon sunulur. Bu, gerçek rezervasyon öncesi login kararını çözmez; P-001 ve O-001 açık kalır.
- İlişki: H-006'nın beğenilmeyen görsel yönüne alternatif üretir. D-004/API bekleme ve diğer onaylı kararlar korunur.
- Belge: `docs/ux/03-fluid-visual-direction.md`.
- Sonraki adım: Kullanıcının görsel yön ve geçiş akışı değerlendirmesi; API sonrası gerçek seçeneklerle revizyon.

### H-008 — İkinci görsel taslak, varlık ve kontrol kaydı
- Tarih: 20 Ekim 2026.
- Tür / durum: DURUM.
- Olay: D-006 ve P-002 için etkileşimli yeni konsept hazırlandı; ilk sürüm dosyaları korunuyor. ImageGen ile atmosfer fotoğrafı üretildi, incelendi ve `docs/ux/assets/dining-atmosphere-v2.png` ile JPG kopyası projeye alındı. Üretim prompt'u görsel yön belgesinde kayıtlı.
- Dosyalar: `docs/ux/entry-preview-v2.html` yerel kontrol kopyası; sohbet kaynağı `C:/Users/ciftc/.codex/visualizations/2026/10/20/01a15995-d9f1-79a3-9b9f-8c124c6ce728/tastetrip-flow-v2.html`.
- Kontrol: Şehir hatası, dört adım, özet değerleri, geri dönüşte tercih korunması, giriş iptali/örnek oturum dönüşü tarayıcıda denendi. 390px görünüm incelendi; 320/390px kök yatay taşma ölçülmedi.
- Sınır: Gerçek API, hesap, telefon, veri kalıcılığı veya tercih çözümleme yok. Fotoğraf gerçek restoran kaydı değil. Tasarım henüz kullanıcı tarafından değerlendirilmedi.
- Sonraki adım: İlk ekran ve geçiş hissine ilişkin geri bildirim almak.

### H-009 — API anahtarı geldi; ilk canlı doğrulama başarılı
- Tarih: 21 Ekim 2026.
- Tür / durum: Kullanıcı bildirimi ve canlı doğrulanmış BULGU.
- Kaynak: Kullanıcının paylaştığı Qloo anahtar e-postası; hackathon sunucusuna yapılan 6 salt okunur GET çağrısı.
- Olay: Tags ve Insights çağrıları HTTP 200 ile başarılı. Italian/quiet/romantic/vegan aramalarında gerçek etiketler bulundu. Mumbai/Italian sorgusu 3 place döndürdü; örneklerde telefon, adres ve website doluydu. Ek metadata incelemesinde Google Place ID bulundu.
- Sınır: Mutfak etiketli sonuçlardan biri otel kaydıydı; restoran kategorisi filtresi ayrıca doğrulanmalı. Quiet/romantic/vegan ile Insights davranışı ve tam tag kataloğu henüz test edilmedi. Alan güncelliği veya her şehirde veri varlığı garanti edilmez.
- İlişki: H-004'te anahtarın beklenmesi durumu sona erdi; D-004'ün bekleme koşulu karşılandı. Eski kayıt tarihsel olarak korunur. UX kararları kullanıcı onayı olmadan kesinleşmez.
- Güvenlik: Anahtar değeri, ham payload veya tam restoran kayıtları proje dosyalarına yazılmadı; yalnız teknik bulgu özeti kaydedildi.
- Belge: `docs/QLOO_LIVE_VALIDATION.md`.
- Sonraki adım: Semantik etiket/kategori ve tercih sinyali deneyi; ardından API'ye dayanan UX düzenlemesi.

### H-010 — UX açıkları için 52 ek canlı API deneyi
- Tarih: 21 Ekim 2026.
- Tür / durum: BULGU ve DURUM.
- Kaynak: Kullanıcının “API denemeleri yaparak UX'de açık kalan alanları doldur, önerileri ver” isteği.
- Olay: 9 etiket keşfi; 19 filtre/şehir matrisi; 7 kategori/sinyal kontrolü; 9 ek kategori/tercih deneyi; 5 seed tekrarı; 3 ek search/bütçe/geçersiz şehir deneyi. 51 HTTP 200; geçersiz şehir negatif kontrolünde beklenen HTTP 400. Önceki 6 çağrı bu sayıya dahil değil.
- Bulgular: İstanbul/Roma/Mumbai'de quiet, romantic, vegan seçenek ve Italian filtreleriyle 10'ar sonuç ve ilgili tag üyeliği gözlendi. Roma'da outdoor, halal ve Japanese filtreleri çalıştı. Bütçe max=2 denemesinde 10 fiyat seviyesi de 2 çıktı. İsim araması 5 ID/adresli aday döndürdü.
- Kategori sınırı: Restoran etiketi otel/AVM gibi ana kategorileri engellemiyor; Hotel etiketini dışlamak bile yeterli değil. Ana kategori kontrolü sonrası üç şehirdeki category sorgusunun ilk 10'undan 7/8/8 restoran ailesi kaydı kaldı; telefon bunlarda 6/7, 7/8, 7/8 doluydu.
- Kişiselleştirme: İki farklı gerçek restoran seed'iyle hedef Roma'da ilk 10'un 4 kaydı değişti; aynı seed'in kısa aralıkla tekrarında sıra aynıydı. Kalıcı determinizm veya memnuniyet kanıtı değil. İlk followup seed'i karışık place listesinden seçildiği için bu çıkarımın dayanağı son, ana-kategorisi kontrol edilmiş seed deneyidir.
- Belgeler: `docs/ux/04-api-backed-ux-recommendations.md`, `docs/validation/qloo-ux-*-2026-10-21.json`, `scripts/qloo_ux_probe.py`.
- Veri sınırı: Anahtar ve ham restoran payload'ı yazılmadı. Özetlerdeki gereğinden geniş primary_genre nesneleri kategori adı/sayılarıyla küçültüldü; konsol encoding hatası düzeltildi. Kaydedilenler teknik sayım/karşılaştırma özetidir.
- Sonraki adım: P-003'teki UX önerilerini değerlendirmek; gerçek telefon/auth/çeviri deneyleri ayrıca gerekli.

### P-003 — Gerçek katalogya dayalı hibrit keşif ve kart önerileri
- Tarih: 21 Ekim 2026.
- Tür / durum: ÖNERİ — kullanıcı tarafından onaylanmış karar değil.
- Öneri: Şehir + isteğe bağlı mutfak/ortam/beslenme/bütçe seçimleri; tercihler ve zorunluluklar ayrı. Sevilen restoran autocomplete atlanabilir. Fotoğraflı, az sayıda karşılaştırılabilir kart; fiyat/telefon gibi eksikler açık. Menü URL'si zorunlu kart öğesi değil. API sonrası adaylarda ana kategori temizliği yapılmalı.
- Login/akış: Girişsiz keşif ve aramadan önce login önerisi korunuyor; doğal dil ile düzenlenebilir yapılandırılmış seçimler birlikte öneriliyor. Bunlar kullanıcı araştırması sonucu veya kesin karar değil.
- İlişki: P-001/P-002'yi canlı kanıtla geliştirir; D-006 görsel/akışkan yön ve D-005 geçmiş koruma kuralını değiştirmez.
- Açık konular: Telefon sağlayıcısı, işletmenin konuştuğu dil, canlı müdahale, veri saklama ve auth yöntemi Qloo testleriyle kapanmaz.
- Sonraki adım: Ürün sahibinin değerlendirmesinden sonra görsel taslağa önerilen seçim ve sonuç kartı akışını taşımak.

## Açık sorular — karar değildir

- **O-001:** Login zamanı ve hesap yöntemi; sahibi ürün sahibi, API sonrası UX karar oturumunda netleşecek.
- **O-002:** Chatbot/wizard/hibrit modeli; sahibi ürün sahibi, ilk UX taslağı ve API deneyiyle netleşecek.
- **O-003:** İlk ülke/şehir ve desteklenen dil çifti; sahibi ürün sahibi, veri kapsamı ve telefon deneyi sonrası seçilecek.
- **O-004:** İlk mutfak/ortam/beslenme etiketleri ve telefon/Place ID metadata'sı canlı doğrulandı (H-010). Tam katalog, işletme kimliği/güncellik, çoklu şart kombinasyonları ve gerçek arama uygunluğu hâlâ açık.
- **O-005:** Telefon/TTS/çeviri sağlayıcıları, gecikme ve maliyet hedefleri; uygulama tasarımında netleşecek.
- **O-006:** Canlı görüşmede müdahale, aramayı durdurma, bekleme süresi ve onay dışı alternatif yönetimi; UX ve teknik deney birlikte çözmeli.
- **O-007:** Kalıcı kayıt, taslak saklama ve veri silme davranışları; gerçek kullanıcı verisi işlenmeden önce netleşmeli.

## Belge haritası

| Belge | Rol |
| --- | --- |
| `Starthere.md` | Her işe giriş noktası ve bağlam koruma prosedürü |
| `PROJECT_HISTORY.md` | Güncel durum ve tarihli karar/olay izi |
| `PRODUCT_REQUIREMENTS.md` | Ürün kapsamı ve kabul kriterleri taslağı |
| `docs/ux/01-entry-and-login.md` | İlk UX tartışması, state ve giriş önerileri |
| `docs/ux/02-entry-prototype.md` | İlk taslak ve kontroller; görsel yönü D-006 ile reddedildi |
| `docs/ux/03-fluid-visual-direction.md` | İkinci görsel/akışkan yön, davranış, varlık prompt'u ve kontrol sınırları |
| `docs/ux/04-api-backed-ux-recommendations.md` | 52 ek API deneyi, gerçek input/kart önerileri ve açık konuların çözüm sınırları |
| `docs/ux/SKILL_REVIEW.md` | UX skill seçimi ve kaynak bilgileri |
| `QLOO_CAPABILITIES.md` | Doküman temelli API yetenek özeti; canlı test değil |
| `HACKATHON_REQUIREMENTS.md` | Yarışma isterleri ve kaynaklar |
| `DEVPOST_APPLICATION_DRAFT.md` | İlk İngilizce başvuru metni; dış işlem durumu için logu oku |
| `WORKING_GUIDE.md` | İlk genel çalışma/fikir geliştirme rehberi; eski fikirler güncel ürün kararının yerine geçmez |

### H-010 — Telefon altyapısı ve maliyet araştırması
- Tarih: 21 Ekim 2026.
- Tür / durum: BULGU ve ÖNERİ; sağlayıcı seçimi/onayı değildir.
- Kaynak / kanıt sınırı: Twilio, Vapi, ElevenLabs, Retell ve LiveKit resmi fiyat/doküman sayfaları; canlı telefon, gecikme veya ses kalitesi testi yapılmadı.
- Bulgu: Telefon şebekesi, konuşma agentı ve web canlı dinleme/çeviri ayrı sorumluluklardır. Vapi live listen ve transcript olayları, LiveKit SIP oda katılımcıları ve yalnız dinleme izinleri belgelenmiştir. Twilio Türkiye sabit/mobil ve Hindistan/ABD tarifeleri farklıdır.
- Öneri: İlk teknik prototip için Vapi + Twilio + ElevenLabs sesi; daha fazla medya kontrolü için LiveKit + SIP alternatifi. Öneriler kabul edilmiş karar değildir.
- Gerekçe: D-001 canlı iki taraflı dinleme ve ana dilde altyazı gereksinimlerini sağlayıcı seçiminin merkezine almak.
- Etkilenen belgeler: docs/TELEPHONY_RESEARCH.md oluşturuldu; ürün baseline değiştirilmedi.
- Önceki kayıtla ilişki: D-001 ve O-005'i tamamlar; açık sağlayıcı/ülke kararlarını çözmez.
- Sonraki adım: Hedef ülke/dil ve kontrollü numarayla prototip; iki taraf sesi, çeviri ve gerçek maliyet ölçümü. Hesap açılmadı veya arama yapılmadı.


### P-004 — Restoran kartı bilgi hiyerarşisi ve iki görünüm
- Tarih: 21 Ekim 2026.
- Tür / durum: ÖNERİ; kullanıcı kabulü veya uygulama kararı değildir.
- Kaynak: Kullanıcının restoran kartı tasarlama isteği; D-006 görsel yön; P-003 ve “UX açıkları için 52 ek canlı API deneyi” başlıklı H-010; PRODUCT_REQUIREMENTS AC-02.1–02.7.
- Öneri: İlk keşifte büyük fotoğraf, isim, mutfak, semt, göreli fiyat, en fazla iki özellik ve tek cümle gerekçe. Adres/telefon/saatler/varsa harita-site-menü detayda. Kompakt alternatif karşılaştırma için sunuldu.
- Kontrol sınırı: “Bu restoranı seç” geri alınabilir seçimdir; arama veya rezervasyon sonucu değildir. Müsaitlik görüşmede teyit edilir; telefon eksikliği açık gösterilir.
- Etkilenen belgeler: docs/ux/05-restaurant-cards.md; mevcut ürün baseline ve login kararları değiştirilmedi.
- Sonraki adım: Ürün sahibinin görsel ve bilgi yoğunluğu değerlendirmesi; kabul edilirse gerçek veriyle sonuç akışına entegrasyon.

### H-011 — Restoran kartı etkileşimli taslak ve yerel kontrol
- Tarih: 21 Ekim 2026.
- Tür / durum: DOĞRULANMIŞ yerel taslak üretimi; canlı uygulama veya kullanıcı testi değil.
- İşlem: Fotoğraf odaklı ve kompakt karşılaştırma alternatifleri oluşturuldu; docs/ux/restaurant-cards-preview.html yerel önizlemesi kaydedildi.
- Veri sınırı: Restoran adı/bilgiler sentetik, fotoğraf önceki üretilmiş temsili varlık; gerçek restoran fotoğrafı veya yeni API sonucu değil. Sır veya API anahtarı eklenmedi.
- Kontrol: Tarayıcıda fotoğraf, detay açma, seçim mesajı ve varyant geçişi doğrulandı. Kompakt kart 320 px viewport altında clientWidth=288, scrollWidth=288; yatay taşma gözlenmedi. Koyu tema incelendi; açık tema, ekran okuyucu ve host telefon eksik kontrolü çalıştırılmadı.
- Sonraki adım: P-004 değerlendirmesi; kabulden sonra eksik veri durumları ve gerçek API entegrasyonuyla doğrulama.


### D-007 — Gerçek restoran verisi ve görünür konum eylemi
- Tarih: 21 Ekim 2026.
- Tür / durum: Kullanıcının açık talimatı.
- Karar: Yeni kart gerçek Qloo kaydıyla hazırlanmalı; konum/adres görünür olmalı ve “Konumda gör” düğmesi mutlaka bulunmalı.
- İlişki: P-004 içindeki haritayı yalnız detayda sunma önerisini bu kart için değiştirir; eski taslaklar tarihsel olarak korunur. Diğer görsel kararlar otomatik onaylanmış değildir.
- Etkilenen belgeler: docs/ux/restaurant-card-live.html ve docs/ux/05-restaurant-cards.md.

### H-012 — Gerçek API kaydıyla restoran kartı
- Tarih: 21 Ekim 2026.
- Tür / durum: DOĞRULANMIŞ API yanıtı ve yerel tasarım önizlemesi.
- İşlem: Mumbai + İtalyan restoranı filtresiyle /v2/insights salt okunur çağrısı yapıldı (take=3). Pizza By The Bay kaydının adı, adresi, fotoğraf URL’si, telefon/site, fiyat seviyesi 3 ve Google Place ID alanları kartta kullanıldı. Ham yanıt ve anahtar dosyaya kaydedilmedi; yalnız gösterim için gereken alanlar yerel HTML’de bulunur.
- Doğrulama: Tarayıcıda gerçek fotoğraf naturalWidth=420 ile yüklendi. Görünür adres ve Place ID içeren Google Maps bağlantısı DOM’da doğrulandı; Google Maps hedef sayfası bu tur açılmadı. İşletmenin güncelliği veya müsaitliği teyit edilmedi.
- Sınır: Yayına alma, telefon araması veya rezervasyon yapılmadı. Kart statik API snapshot’ıdır; canlı otomatik yenilenmez. Fotoğraf uzak Qloo URL’sinden doğrudan yüklenir, indirilmedi.
- Sonraki adım: Kullanıcının görsel değerlendirmesi; ardından seçilen restoranı rezervasyon koşulları adımına bağlama.


### H-013 — İstenen gerçek JSON yanıtı
- Tarih: 21 Ekim 2026.
- Durum: DOĞRULANMIŞ; Mumbai/İtalyan/take=1 sorgusu yeniden çalıştırıldı. Kullanıcının JSON çıktısını görme talebi için tam yanıt docs/validation/qloo-pizza-by-the-bay-response.json dosyasına kaydedildi. İki salt okunur çağrı yapıldı; ilk konsol çıktısı uzunluğu nedeniyle kesildi, ikinci yanıt tam dosyaya yazıldı. Anahtar veya istek başlıkları kaydedilmedi. Önceki H-012’de ham yanıt saklanmamış olması tarihsel olarak korunur; bu yeni dosya kullanıcının sonraki talebi kapsamındadır.


### D-008 — Çok günlük seyahat rotası ve çok kategorili rezervasyon
- Tarih: 21 Ekim 2026.
- Tür / durum: KULLANICI KARARI; yeni kapsam açık talimatla benimsendi, uygulanmış özellik değil.
- Kaynak: Kullanıcının restoran/kafe/bar/otel/gezilecek özel alanlardan Paris için iki günlük rota ve gereken duraklarda rezervasyon talebi. Paris ve tarih örnektir; gerçek seyahat veya rezervasyon talimatı değildir.
- Değişiklik: D-001 restoran odaklı ürün kapsamını genişletir; eski kayıt korunur. Telefonla rezervasyon, canlı dinleme/çeviri ve D-007 konum eylemi korunur.
- Sınır: Qloo zevk tabanlı aday üretimi; yol süresi, günlük sıralama, tarihli saat/müsaitlik ve rezervasyon ayrı sorumluluklar. Diğer kategoriler Paris’te bu tur canlı test edilmedi. Yeni arayüz veya telefon/ödeme işlemi yapılmadı.
- Etkilenen belgeler: PRODUCT_REQUIREMENTS.md başlık/amaç/akış ve FR-09–FR-11 eklendi; docs/ux/06-trip-itinerary.md oluşturuldu; Starthere ve güncel özet güncellendi. Harici Devpost taslağı değiştirilmedi.
- Öneri statüsü: Gün çizelgesi+harita, durak sabitleme, ilk MVP’de restoran telefon rezervasyonuna öncelik öneridir; kullanıcı kararı değildir.
- Sonraki adım: Paris’te beş kategori veri deneyi ve rota veri sağlayıcısını inceleme; ardından günlük rota ekranını tasarlama. İlk sürüm kapsamı ürün sahibince seçilecek.


### D-009 — THY kart referansı ve rota içi içerik önerileri
- Tarih: 21 Ekim 2026.
- Tür / durum: KULLANICI TALİMATI; kapsam eklendi, uygulanmadı.
- Kaynak: D:/LLM/THY Travel Agent kartlarını inceleyip baz alma izni; seyahat anlarında kitap, film, podcast ve müzik listesi önerileri ekleme talebi.
- İlişki: D-008 çok günlük rota kapsamını içeriklerle tamamlar; D-006 görsel yön ve D-007 konum eylemi korunur. Kaynak projedeki renk/marka ve tüm davranışlar otomatik kabul edilmiş sayılmaz.
- Etkilenen belgeler: PRODUCT_REQUIREMENTS.md FR-12, docs/ux/07-thy-components-and-content.md, Starthere ve güncel özet.
- Sonraki adım: Referans bileşen yapısını rota tasarımına uyarlamak; içerik kategorilerini gerçek API ile test etmek.

### H-014 — THY Travel Agent kaynak kodu incelemesi
- Tarih: 21 Ekim 2026.
- Tür / durum: DOĞRULANMIŞ kaynak incelemesi; runtime testi değil.
- İncelenen: frontend/src/components/widgets altındaki PlacesWidget, PlacesOrbit, TimelinePath, ItineraryWidget ve WidgetRenderer; ui/MapModal; app/globals.css ve frontend/package.json.
- Bulgu: Gün/saat/durak çizelgesi, fotoğraf ve kullanıcı notları; mekân kartı ve uygulama içi harita yapıları mevcut. Kaynak proje Next/React/Tailwind bağımlı; renderer auth/chat/backend/analytics bağları taşıyor. Dosyalar salt okunur incelendi; kaynak projede değişiklik ve bileşen aktarımı yapılmadı.
- API sınırı: Resmi Insights enum listesinde book/movie/podcast/artist var; playlist/track ayrı tür görünmüyor. Müzik listesi için ek sağlayıcı/eşleme gerekiyor; canlı içerik sorgusu yapılmadı.
- Öneri: Ana yapı TimelinePath, mekân kartı PlacesOrbit; medya kartları ilgili mola/geçiş altında isteğe bağlı. Erişilebilirlik, kimlik ve işlem durumları uyarlamada geliştirilecek.
- Sonraki adım: Referanslı görsel rota prototipi ve kategori deneyleri; uygulama çalıştırıldığı iddia edilmedi.


### D-010 — Aksiyon anında giriş, hatırlama ve düzenlenebilir kayıtlı rotalar
- Tarih: 21 Ekim 2026.
- Tür / durum: KULLANICI KARARI ve kodlama talimatı.
- Kapsam: Genel seyahat girdileri, THY referanslı uçuş API, kişisel rota, kullanıcı tetiklemeli bekleme/mola önerileri, rota kaydetme ve LLM ile yeniden düzenleme. Login keşif başlangıcında değil; kaydetme/rezervasyon gibi işlem anında. Tekrarlı ziyaret tanıma cookie tabanlı.
- İlişki: P-001/P-003 login zamanının öneri olan kısmını kesinleştirir; O-001 zamanlaması kapanır, auth yönteminin üretim kapsamı ayrı. D-008/D-009 korunur. Cookie kişisel hesap kimliğinin kanıtı değildir.
- Uygulama tercihi: Cookie’de rastgele anonim ID; tercih ve taslak sunucuda. İlk auth kullanıcı adı/parola; bu, kullanıcı tarafından seçilmiş OAuth sağlayıcısı gibi sunulmaz.
- Etkilenen: PRODUCT_REQUIREMENTS, Starthere, README, app/ ve docs/IMPLEMENTATION_STATUS.md.

### D-011 — Coolify / Hetzner CAX21 hedefi
- Tarih: 21 Ekim 2026.
- Tür / durum: Kullanıcının deployment hedefi; deploy yetkisi/işlemi olarak yorumlanmadı.
- Teknik uygulama: ARM64 uyumlu Python slim Dockerfile, Flask/Gunicorn, tek SQLite instance, kalıcı /app/data, runtime secrets, sağlık kontrolü ve Compose. Uygulama non-root.
- Sınır: Docker daemon yerelde kapalı; container/ARM64 build ve sunucu deployment doğrulanmadı.
- Kaynak: Coolify resmi uygulama/healthcheck belgeleri ve Hetzner ARM64 duyurusu; docs/COOLIFY_DEPLOYMENT.md.

### D-012 — DeepSeek ve servis anahtarlarının kullanıcı yapılandırması
- Tarih: 21 Ekim 2026.
- Tür / durum: KULLANICI SEÇİMİ ve doğrulanmış yapılandırma.
- Karar: OpenAI uyumlu API üzerinden DeepSeek. Resmi belgede güncel model deepseek-flash ve base URL api.deepseek.com doğrulandı; yapılandırılabilir bırakıldı.
- Kullanıcı DeepSeek ve Aviasales anahtarlarını .env içine girdiğini bildirdi; gerekli alanların doluluğu kontrol edildi ve gerçek çağrılarla erişim doğrulandı. Anahtarlar loga veya istemciye yazılmadı.

### H-015 — İlk çalışan uygulama ve canlı servis doğrulaması
- Tarih: 21 Ekim 2026.
- Durum: Kodlandı ve yerelde çalıştırıldı; ürün kabulünün tamamı veya deploy değildir.
- Uygulanan: Genel seyahat formu, Qloo gerçek yer kartları, günlük rota taslağı, DeepSeek ile üretim ve gün/sıra düzenleme, cookie hatırlama, aksiyonda login, kullanıcıya özel SQLite rota kayıtları, kullanıcı tetiklemeli 8 tür Qloo içerik önerisi, THY referanslı Travelpayouts uçuş adaptörü. Önceki HTML taslaklar tarihsel korunur.
- Canlı kanıt: Tarayıcıda Paris rotası DeepSeek+Qloo ile oluştu. Musée National Picasso-Paris ikinci günden ilk güne taşındı ve sürüm 2 oldu; diğer duraklar korundu. Kitap önerisi kullanıcı tıklamasıyla geldi. API kontrolünde 8 kültürel tür 4’er sonuç; Paris barları 20 adayla süzüldüğünde 3 sonuç. Tam tarihli IST/PAR gidiş-dönüş uçuş kontrolünde 1 önbellek teklifi; satın alma yapılmadı.
- Kontrol: 10 test geçti; hesap izolasyonu/kaydet-aç/cookie/CSRF/model ID doğrulama/sabit rezervasyon/tarihli uçuş gibi davranışlar fixture ile test edildi. JS/Python syntax ve Compose config geçti. Mobil 320 px taşma kontrolü yapıldı. Gerçek model deneyi test-fixture sonuçlarından ayrı.
- Açık: Gerçek yol süreleri ve tarihli açılışlar, rezervasyon telefon/canlı ses/çeviri, yeni yer ekleme/çıkarma, playlist oynatımı, üretim auth/backup kapsamı. Docker daemon kapalı, ARM64 container çalıştırılmadı. İlk gün ekranı bir rota taslağıdır, kesin program iddiası yok.
- Etkilenen: app/, tests/, Dockerfile, compose.yaml, requirements.txt, .env.example, README, docs/IMPLEMENTATION_STATUS.md, docs/COOLIFY_DEPLOYMENT.md. Anahtarlar yalnız Git dışında yerel .env.
- Sonraki adım: Kullanıcının ilk uygulamayı değerlendirmesi, gerçek rota uygulanabilirlik/harita ve rezervasyon entegrasyonları, Coolify’da build ve volume/restart smoke testi.


### H-016 — Kullanıcı anahtarlarından sonra canlı uçtan uca kontrol
- Tarih: 21 Ekim 2026.
- Durum: DOĞRULANMIŞ. Kullanıcı anahtarları girdiğini bildirdi; doluluk kontrolü ve restart sonrası DeepSeek rota üretimi/düzenlemesi ile Aviasales fiyatı canlı çalıştı. Tarayıcıda uçuş havalimanları seçildi ve tam tarihli gidiş-dönüş teklifi/partner bağlantısı görüldü. Anahtar içerikleri kaydedilmedi.
- Değişiklik: Tek yön isteğine dönüşlü fiyat sızmasını engelleyen tarih/tür filtresi ve uçuşta dönüş tarihi gösterimi; Qloo search types alanı ve tekrarlanan entity ID normalizasyonu düzeltildi. LLM çıktısının JSON nesnesi olması zorunlu.
- Test: Son sürüm 10 otomatik test, Python/JS syntax, Compose config geçti; Docker runtime/deploy yok. Başlangıç rota prompt’una tempo ve müze yoğunluğu yönergesi eklendi; bu kalite garantisi değildir.
- Açıklar: docs/IMPLEMENTATION_STATUS.md içindeki yol/saat/rezervasyon/medya/üretim işleri sürer. Uygulama http://localhost:8080 üzerinde açık bırakıldı.


### H-017 — Kitap/film için türe özel zevk toplama düzeltmesi
- Tarih: 21 Ekim 2026.
- Kaynak: Kullanıcının kitap ve film için kişisel içgörü sorulmadığı geri bildirimi. Önceki H-015 öneri alanı yalnız mekân/genel sinyallere dayanıyordu; bu eksik korunarak kaydedildi.
- Değişiklik: Öneri dialoguna seçili türe göre “Sevdiğin kitaplar/filmler neler?” adımı; Qloo isim aramasından türüne uyan 1–5 eser seçimi, kaldırma, “Zevkime göre öner” ve açık “Şimdilik atla” yolu eklendi. Seçilen entity ID’leri öneri sinyallerinin başında gönderilir. Film/kitap tercihleri ayrı, anonim ziyaretçi kimliğiyle sunucuda hatırlanır; cihaz temizleme bunları da siler. Atlamak eski tercihleri silmez. Yeni giriş engeli yok.
- Kanıt: 11 test geçti; yeni test eser olmadan örtük sorguyu engellemeyi, seçilen ID’nin sağlayıcıya iletilmesini, türler arası ayrımı, tekrar okumayı ve temizlemeyi kapsıyor. Tarayıcıda kitap/film soru adımları görüldü; film adıyla Qloo arama deneyi yapıldı. Kullanıcı adına sevilen eser uydurulmadı veya test tercihi kaydedilmedi.
- Sınır: Süre/dil/platform ve ayrıntılı tür tercihleri henüz toplanmıyor. Tercihlerin öneri kalitesine etkisi kullanıcı araştırmasıyla ölçülmedi.
- Etkilenen: app/server.py, providers.py, static/index.html/app.js/style.css, tests/test_app.py ve uygulama durumu. Önceki kararlar değiştirilmedi.


### D-013 / H-018 — Podcast için anahtar kelimeyle konu seçimi
- Tarih: 21 Ekim 2026.
- Kaynak / durum: Kullanıcı podcast örneği yerine keyword istedi; uygulandı. Kitap/film eser seçimi korunur; H-017 podcast eser adımı bu talimatla değişti.
- Canlı bulgu: Qloo /v2/tags podcast parent filtresinde bilim/tarih Türkçe sorguları boş, science/history sorguları etiket döndürdü. Bu örnekler tüm diller için destek veya destek yokluğu ispatı değildir.
- Uygulama: Podcast alanı “Ne hakkında dinlemek istersin?” oldu. DeepSeek serbest metni en fazla 3 İngilizce konuya normalize eder; Qloo’dan gerçekten bulunan tag ID’leri kullanıcı seçimine sunulur. Seçilen konular filter.tags union ile podcast sorgusuna gider; entity sinyalleriyle karıştırılmaz. Aynı isimli etiketler arayüzde tekilleştirilir.
- Canlı kontrol: “bilim ve uzay” → science/space normalizasyonu ve gerçek Qloo konu eşleşmeleri; science etiketiyle 4 podcast yanıtı. Bu test konu kalitesinin veya podcast konuşma dilinin doğrulaması değildir. Keyword dili ile içerik dili ayrı; podcast dil filtresi uygulanmadı.
- Test: 12 otomatik test geçti; yeni test konu ID’lerinin entity yerine tag parametresine iletilmesini ve film alanında tag kabul edilmemesini doğrular. Tarayıcıda podcast konu alanı ve açıklaması görüldü.
- Sınır: Her dil garanti edilmez; çeviri/eşleşme başarısızsa kullanıcı farklı kelime deneyebilir. Giriş metni sağlayıcıya DeepSeek iletilir. Kaynak anahtarları kaydedilmedi.
- Etkilenen: app/providers.py, app/server.py, static/index.html/app.js, tests/test_app.py, PRODUCT_REQUIREMENTS ve IMPLEMENTATION_STATUS. Yeni konu seçimi öneri anında hatırlanır; otomatik öneri yok.


### H-019 — Podcast ve film dil filtresi incelemesi
- Tarih: 21 Ekim 2026. Kullanıcı language seçeneğini sordu. Mevcut uygulamada dil seçimi yok; kod değiştirilmedi.
- Kaynak: Qloo resmi insights-api-deep-dive, parameters ve available-parameters-by-entity-type belgelerinde language parametresi bulunamadı. Canlı üçer film/podcast örneğinin properties alanlarında dil anahtarı yoktu. Turkish etiket aramasında film için turkish_cinema/turkish_culture gibi konu etiketleri, podcast için boş liste döndü. Bu örnekler tüm katalogda dil metadata bulunmadığının kanıtı değildir.
- Sonuç: Standart yayın dili filtresi bu erişimle doğrulanamadı. Kültür/ülke etiketi yayın dili, dublaj veya altyazı kanıtı değildir. Güvenilir dil seçimi için kategoriye uygun ek metadata sağlayıcısı/erişim entegrasyonu gerekir; henüz eklenmedi.
- Deney sınırı: İlk sinyalsiz Insights kontrolü servis hatası verdi; kayıtlı restoran entity sinyaliyle tekrar edilen sorgular sonuç verdi. Anahtarlar kaydedilmedi.


### H-020 — Podcast yayın dili için kontrollü API matrisi ve RSS deneyi
- Tarih: 21 Ekim 2026. Kullanıcının API denemesi isteği üzerine araştırma; yeni dil seçimi henüz uygulanmadı.
- Deney: 14 çağrılık script matrisi (temel/tekrar, 8 olası dil parametresi, 4 tag araması), ek 1 Qloo metadata çağrısı. Dil parametreleri tr/en ve geçersiz zz dahil HTTP200 ile aynı5 ID/sırayı verdi. Bu, dil filtresinin çalıştığını doğrulamaz; anlık temel tekrar aynıydı. Dillerin açıklama çevirilerinde bulunması yayın dili değildir.
- Ek kanıt: Qloo iTunes kimliklerinden 2 Lookup +2 RSS isteği. Berner Phone ve Giggly Squad RSS channel/language=en verdi; 4 dış HTTP200. Türkçe envanter veya her bölüm dili doğrulanmadı.
- Sonuç/öneri: Qloo aday üretimi + iTunes/RSS metadata dil doğrulama ve uygulama filtresi mümkün görünüyor; ayrı uygulama/üretim URL güvenliği/önbellek ve Türkçe kapsama testi gerekir. Dil bilinmiyorsa garanti verilmez. H-019’un sınırı korunur; doğrudan API dil filtresi bu erişimde doğrulanamadı.
- Etkilenen: scripts/qloo_podcast_language_probe.py, docs/validation/qloo-podcast-language-2026-10-21.json, docs/QLOO_PODCAST_LANGUAGE_VALIDATION.md. Anahtar, ham yanıt veya ses dosyası saklanmadı. Uygulama kodu değiştirilmedi.


### D-014 / H-021 — Podcast ve kitap dil seçimi uygulandı
- Tarih: 21 Ekim 2026. Kullanıcı RSS tabanlı podcast dil filtresini onayladı ve kitaplara dil seçimi eklenmesini istedi. H-020’deki öneri bu kapsamda uygulandı; film dil filtresi eklenmedi.
- Uygulama: Podcast/kitap için bağımsız hatırlanan dil seçimi; Dil fark etmez +13 dil kodu. Dil seçilince Qloo’dan en fazla20 aday, uygulamada metadata filtresi ve ilk4 eşleşme gösterilir. Bilinmeyen ve başka dildeki içerik eklenmez; aday/eşleşme/bilinmeyen sayıları görünür, koşul otomatik gevşetilmez.
- Kaynak ayrımı: Podcast Qloo iTunes ID → Apple Lookup → RSS channel/language (yayıncı beyanı); kitap properties.language + varsa ISBN (Qloo kitap kaydı, çeviri/baskı garantisi değil). Kitap örneklerinde language=English ve ISBN alanları canlı görüldü. Açıklama çeviri dili kullanılmadı.
- RSS katmanı: Sunucu tarafında public IP doğrulama ve DNS sonucu pinleme, redirect kontrolü/HTTPS downgrade engeli, standart portlar, süre/boyut sınırı, güvenli streaming XML. Dil bulunduğunda akış erken kesilir; ses indirilmez. Olumlu cache7 gün, bilinmeyen1 saat; cache DATA_DIR altında SQLite, kullanıcıya RSS URL proxy açılmadı.
- Canlı kanıt: Altışar kitap ve podcast adayı İngilizce olarak doğrulandı; tarayıcıda her kategoride20 adayın20’si İngilizce eşleşti ve4 sonuç dil/kaynak etiketiyle gösterildi. Türkçe seçenek var ancak Türkçe katalog kapsamı doğrulanmadı; iki örnek Türkçe başlık araması beklenen kitap/podcast kaydını bulmadı. Bu bütün Türkçe katalog boş demek değildir.
- Test:20 test geçti; yeni kontroller dil kodları/bölge varyantı, RSS dilinin açıklamadan ayrılması, entity expansion reddi, private IP/port/şema engeli, cache, bilinmeyen/diğer dili dışlama, server dil parametresi ve hatalı kod reddi. JS/Python syntax geçti. Dış entegrasyon testleri ve fixture testleri ayrı.
- Etkilenen: app/content_languages.py, providers.py/server.py/static/index.html/app.js, requirements.txt(defusedxml), tests, README ve IMPLEMENTATION_STATUS. Çalışan yerel sunucu yenilendi. Coolify redeploy henüz yapılmadı.


### H-022 — Podcast erişim bağlantıları doğrulaması
- Tarih: 21 Ekim 2026. Kullanıcı API doğrudan podcast bağlantısını sordu.
- Canlı bulgu: İki Qloo podcast kaydında link yerine external.itunes[].id mevcut; properties.channel yalnız ad. Apple Lookup ile her iki kayıtta collectionViewUrl/trackViewUrl (Apple Podcasts sayfası) ve feedUrl (RSS) alındı. Örnekler Berner Phone ve Giggly Squad. Bu, tüm podcast kayıtlarının link içerdiği garantisi veya bölüm ses oynatma doğrulaması değildir.
- Uygulama sınırı: Şu an iTunes metadata katmanı yalnız dil bilgisini taşıyor; Apple Podcasts URL kart yanıtına taşınmıyor. Kullanıcıya önerilecek erişim eylemi gerçek lookup URL’siyle Apple Podcasts’te aç; Spotify linki veya doğrudan bölüm sesi uydurulmaz. Bu tur kod değiştirilmedi.


### D-015 / H-023 — Kitap keyword ve Apple Podcasts erişimi
- Tarih: 21 Ekim 2026. Kullanıcının açık talimatı uygulandı.
- Kitap: Konu/anahtar kelime modu eklendi; sevilen kitap seçimi ayrı mod olarak korundu. Türkçe konu metni DeepSeek ile normalize edilir, yalnız book parent’ında bulunan Qloo tag ID’leri seçilir. Eser ID ve konu tag’leri ayrı entity/filter sinyalleriyle gönderilir; dil filtresi korunur.
- Podcast: Apple Lookup collectionViewUrl/trackViewUrl, yalnız HTTPS podcasts.apple.com adresi doğrulanarak kart yanıtına taşınır. “Apple Podcasts’te aç” bağlantısı dil fark etmez halinde de zenginleştirilir; RSS okunamasa da bulunan Apple sayfası korunur. Bağlantı yoksa açıklama gösterilir; bölüm sesi/Spotify bağlantısı uydurulmaz. Eski dil cache satırları yeni URL alanı için yenilenir.
- Canlı kanıt: Kitap için “bilim ve tarih” science/history ve iki gerçek book etiketiyle eşleşti. Berner Phone/Giggly Squad için gerçek Apple Podcasts URL’leri alındı. Tarayıcıda kitap keyword/eser seçimi görüldü; podcast bağlantı akışı çalıştırıldı.
- Test:22 test geçti; kitapta karma eser/konu ID’lerinin doğru parametrelere ayrılması ve RSS hatasında Apple linkinin korunması yeni testlerle doğrulandı. JS syntax geçti.
- Etkilenen: providers.py, content_languages.py, server.py, static/index.html/app.js, tests, ürün gereksinimleri ve uygulama durumu. Yerel sunucu yenilendi; deploy yapılmadı.


### D-016 — Görüşme dili restoran ülkesinden, altyazı kullanıcı ana dilinden
- Tarih: 21 Ekim 2026. Kullanıcının açık yanıtı.
- Karar: Hedef görüşme dili restoranın ülkesine göre değişecek; altyazı kullanıcının native dilinde olacak. Sabit İngilizce→Türkçe MVP kararı alınmadı.
- Uygulama sınırı: Ülke varsayılan sağlar, personelin dilini kanıtlamaz; çok dilli/bilinmeyen ülke ve desteklenmeyen dil için görünür düzeltme/fallback gerekir. Ana dil, UI dili ve görüşme dili ayrı tutulur. Bu maddelerin ayrıntı UX politikası plan önerisidir.
- İlişki: FR-06/D-001 korunur; O-003 dil/ülke desteğinin gerçek servis matrisi hâlâ açık.

### P-005 / H-024 — Rezervasyon araması entegrasyon planı
- Tarih: 21 Ekim 2026. Kullanıcı arama entegrasyonunu planlamayı istedi; plan tamamlandı, arama kodu/servis kurulumu yapılmadı.
- Öneri: Vapi standart STT/LLM/TTS + Twilio + ElevenLabs sesi, ayrı async voice-gateway ve kalıcı outbox worker; DeepSeek rota modeli korunur, sesli model uyumu/latency ayrıca test edilir. Sağlayıcılar onaylanmış karar değildir.
- Kaynak: Vapi call-features/server-url/events/GPT-Live compatibility ve ElevenLabs Twilio outbound resmi sayfaları yenilendi. Standart canlı dinleme dokümante, GPT-Live’de kısıtlar var; iki taraf gerçek ses ve altyazı testi henüz yok.
- Plan: Aksiyonda login/koşul özeti, idempotent arama girişimi, ayrı arama/rezervasyon durumları, kullanıcı alternatif kararı, unknown sonucun uzlaştırılması, sahiplik ve webhook doğrulaması, Coolify CAX21 gateway/worker, aşamalı kontrollü testler. Doküman varlığı çalışan entegrasyon sayılmadı.
- Etkilenen: docs/RESERVATION_CALL_IMPLEMENTATION_PLAN.md, PRODUCT_REQUIREMENTS dil notu ve Starthere güncel işaretçisi. Önceki telefon araştırması korunur.
- Sonraki adım: Sağlayıcı/ülke-limit-saklama kararları ve önce simülasyon adaptörlü rezervasyon çekirdeği. Gerçek arama, numara satın alma, hesap veya deploy yapılmadı.


### D-017 — Görüşme sonrası rezervasyon konuşması özeti
- Tarih: 21 Ekim 2026. Kullanıcının açık kapsam ekleme talimatı.
- Karar: Görüşme sonrasında native dilde kısa özet; talep, restoran cevabı, anlaşılan/değişen koşullar, özel istekler ve açık noktalar. Doğrulanmış rezervasyon durumu özetten ayrı tutulur. Konuşma eksikse belirsizlik görünür olur.
- Plan: Final transcript ve sonuç kaydıyla tutarlılık; kanıt event referansları, ayrı özet sürümü/durumu, sahiplik kontrollü sonuç erişimi ve arama yapmadan özet yeniden denemesi. Saklama süresi açık; ses kaydı izni verilmiş sayılmaz.
- Etkilenen: PRODUCT_REQUIREMENTS FR-13/AC-13.1–13.5, docs/RESERVATION_CALL_IMPLEMENTATION_PLAN.md sonuç ekranı/veri/API/kabul senaryoları. Starthere güncel yönüne eklendi.
- Durum: Plana/gereksinimlere eklendi; çalışan telefon veya özet üretim kodu henüz yok. Yeni test çalıştırılmadı; belirtilen kabul senaryoları planlanan testlerdir.


### D-018 / P-006 / H-025 — Aramada maliyet önceliği ve doğrudan ses hattı
- Tarih: 21 Ekim 2026. Kullanıcı en ucuz altyapıyı seçmemizi istedi; maliyet önceliği kabul edilmiş karar, belirli servislerin kalite uygunluğu henüz doğrulanmış değil.
- P-006: Mevcut CAX21 üzerinde orkestrasyon + Twilio Media Streams + Deepgram Nova-3 + DeepSeek + Polly Standard. P-005 Vapi/ElevenLabs başlangıç önerisinin yerine maliyet odaklı teknik yön; önceki kayıt korunur. Bütün ülkeler için en ucuz PSTN sağlayıcısı olduğu iddia edilmez.
- H-025: Resmî fiyatlar araştırıldı. Vapi hosting $0.05/dakika; Deepgram canlı monolingual Nova-3 kampanya $0.0048, normal $0.0077/dakika; Polly Standard $4/milyon karakter. Fransa sabit hat 3 dakika/1500 karakter örneği medya dahil $0.0897–0.0984 + LLM; numara/vergi/sunucu hariç. Türkiye tarife sayfası yeniden doğrulanamadı. Fiyat kaynakları ve varsayımlar ayrı belgede.
- Etkilenen: docs/VOICE_COST_COMPARISON.md, arama entegrasyon planı güncel yönü, Starthere. Dil/altyazı/özet kararları korunur.
- Durum: Belgelendirme; hesap açma, numara satın alma, gerçek arama, kod entegrasyonu, ses kalite testi veya deploy yapılmadı. Sonraki adım doğrudan hattın simülasyon çekirdeği ve kontrollü testidir.

### H-026 — Twilio onboarding ekranı
- Tarih: 21 Ekim 2026. Kullanıcı hesabını oluşturduğunu ve şahsi test hedef numarası bulunduğunu bildirdi. Tarayıcıda giriş yapılmış Twilio onboarding ekranı doğrulandı; numara satın alma, bakiye veya hedef numara doğrulaması kontrol edilmedi.
- Ekran: Voice seçili; Conversational AI ve With code henüz seçili değil. Öneri: Voice + Conversational AI + With code; nonprofit/government seçeneği işaretlenmez. Bu tur form değiştirilmedi veya gönderilmedi; seçimler öneridir. Kişisel numara ve hesap kimliği kaydedilmedi.


### H-027 — Twilio Trial ve test araması ekranı
- Tarih: 21 Ekim 2026. Tarayıcıda Trial hesabı, kalan 30 gün ve 75 ücretsiz dakika göstergeleri görüldü. Make a voice call kurulum paneli açıldı; To alanında Türkiye, From alanında ABD numarası hazır görünüyor. Numara değerleri kaydedilmedi; sahiplik/ülke izinleri ve başarılı arama henüz doğrulanmadı.
- Varsayılan Quick tests / Speech Recognition seçili. Start call düğmesine basılmadı; gerçek telefon araması veya satın alma yapılmadı. Bu panel Twilio demo testi, uygulamamızın agent entegrasyonu değil.


### H-028 — Kullanıcının Twilio demo araması başarılı bildirimi
- Tarih: 21 Ekim 2026. Kullanıcı test aramasının başarılı olduğunu, kendi telefonunun arandığını bildirdi. Kaynak kullanıcı beyanı; çağrı logu bağımsız incelenmedi.
- Kapsam: Twilio konsol demo bağlantısı; uygulamamızdan outbound API, çift yönlü medya, konuşma tanıma doğruluğu, agent veya rezervasyon başarısı kanıtlanmış sayılmaz. Kişisel numara/sır kaydedilmedi.
- Sonraki adım: Mevcut yerel env şablonunda Twilio ayarlarının hazırlanması ve uygulama tarafından kontrollü arama entegrasyonu. Ek gerçek arama otomatik başlatılmaz.


### H-029 — Twilio env alanları hazırlandı
- Tarih: 21 Ekim 2026. Kullanıcı alanların env dosyasında olmadığını bildirdi. .env ve .env.example içine eksik TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER alanları boş olarak eklendi; mevcut değerler korunur. Sırlar çıktıya veya geçmişe yazılmadı.
- Yapılandırma şablonu değişikliği; uygulamanın bu alanları kullanması veya gerçek arama entegrasyonu henüz uygulanmadı. Gerçek arama yapılmadı.

### H-030 — Twilio env ve salt okunur hesap kontrolü
- Tarih: 21 Ekim 2026. Kullanıcı env girişini tamamladığını bildirdi. Twilio kimlik doğrulaması başarılı; hesap durumu: active. FROM numarası hesap numaraları içinde bulunamadı; demo numarası/API kullanım yetkisi ayrıca kontrol edilmeli.
- Sadece yapılandırma varlığı ve salt okunur hesap/numara API kontrolü; değerler kaydedilmedi. Yeni arama veya satın alma yapılmadı.

### H-031 — Twilio numara yönetimi tarayıcı kontrolü
- Tarih: 21 Ekim 2026. Communications > Numbers & senders > Overview ekranında tahsis edilmiş numara listesi görülmedi; ek numara satın alımı için Upgrade metni var. Verified Caller IDs bağlantısı Upgrade penceresine yönlendirdi. Hesaba ait FROM numarası bu kontrolde bulunamadı; demo numarasının genel API kullanımı kanıtlanmadı.
- Önceki trial yeterliliği önerisi demo ile sınırlı kalıyor; uygulama outbound kurulumu için trial yetkisi ayrıca doğrulanmalı. Upgrade başlatılmadı, ödeme veya numara satın alma yapılmadı.


### H-032 — Twilio numara fiyatı araştırması
- Tarih: 21 Ekim 2026. Resmî ABD Voice fiyat sayfası yerel numara için aylık USD1.15 başlangıç fiyatı gösteriyor; arama ücretleri ayrı. Kaynak: https://www.twilio.com/en-us/voice/pricing/us ve https://help.twilio.com/articles/223182908 (ilk aylık ücret tahsiste peşin).
- Tarayıcıda Upgrade formu sadece inceleme için açıldı; adım1 hesap/vergi adresi gerekiyor. Bilgi girilmedi, Next/ödeme yapılmadı; hesaba özel minimum yükleme tutarı henüz doğrulanamadı. USD20 iddiası bu hesap için kesinleştirilmedi. Numara satın alınmadı.


### H-033 — Twilio promo araştırması
- Tarih: 21 Ekim 2026. Açık web ve resmî Twilio kaynaklarında bu hesaba uygulanabilir güncel genel promo kod doğrulanamadı; kod uygulanmadı ve ödeme yapılmadı. Startup FAQ ek startup kredisi sunulmadığını belirtiyor: https://www.twilio.com/en-us/solutions/startups . Eski APJ kredi sayfası arama sonucunda var fakat açıldığında404; aktif teklif sayılmadı. Impact Access sosyal fayda kuruluşlarına özgü; bu projenin uygunluğu varsayılmadı.


### H-034 — Numara satın alma girişimi ve zorunlu profil
- Tarih: 21 Ekim 2026. Kullanıcı USD20 yüklediğini ve numara satın almayı istediğini belirtti; konsolda Active ve USD20 bakiye doğrulandı. Listeden Voice destekli aylık USD1.15 ABD yerel numara seçilip Next ile ilerletildi; satın alma gerçekleşmedi.
- Twilio onaylı primary compliance profile zorunluluğu gösterdi. Individual Profile seçimiyle kimlik doğrulama iframe adımına gidildi; Verify your identity iframe içeriği boş göründü. Kimlik bilgisi girilmedi, Complete gönderilmedi, ücret kesimi doğrulanmadı. Numara henüz tahsis edilmedi; kullanıcı doğrulaması gerekli.


### H-035 — Twilio arayan numarası satın alındı
- Tarih: 21 Ekim 2026. Önceki kullanıcı satın alma yetkisiyle aylık USD1.15 ABD yerel Voice numarası alındı; konsolda hesaba eklendi mesajı görüldü. Satın alma özetinde ilk USD1.15 hemen, ardından aylık USD1.15 + kullanım ücreti bildirildi; bakiye başlığı henüz yenilenmediğinden kalan bakiye iddia edilmedi.
- Voice kanalı seçildi; compliance profile Complete görünüyor. SHAKEN/STIR, Voice Integrity, Branded Calling ve CNAM kaydı başlatılmadı. Ek hizmet satın alınmadı.
- Yerel .env TWILIO_FROM_NUMBER satın alınan numarayla güncellendi; anahtarlar değiştirilmedi. Numara değeri geçmişe yazılmadı. Gerçek uygulama araması henüz yapılmadı.

### H-036 — Yerel Twilio smoke araması reddedildi
- Tarih: 21 Ekim 2026. Kullanıcının ok yanıtıyla önceki konsol testindeki şahsi hedefe tek API araması denendi. Sahip olunan Voice FROM doğrulaması geçti; create isteği HTTP400/Twilio21215 ile reddedildi. Otomatik yeniden deneme yapılmadı; çağrı kabul edildi veya mesaj duyuldu diye kaydedilmedi.
- scripts/twilio_call_smoke.py eklendi: açık --call gerektirir; kısa Türkçe Polly.Filiz TwiML,30sn üst sınır, kayıt kapalı, POST tekrar yok. Henüz web arayüzü/agent entegrasyonu değil.


### D-019 / H-037 — Tüm coğrafi arama izinleri
- Tarih: 21 Ekim 2026. Kullanıcı her yere arama izni verilmesini açıkça istedi. Twilio Voice > Settings > Geo permissions altında Low risk ve High risk sekmelerinde Afrika, Asya, Avrupa, Kuzey Amerika, Okyanusya ve Güney Amerika toplu izinleri açıldı. Her iki sekmede6/6 kıta anahtarı checked ve Settings Updated görüldü.
- Kapsam: Ekranda sunulan hedef izinleri; operatör/servis özel kısıtlarını kaldırdığı veya tüm numaralara ulaşılabildiği iddia edilmez. Ayar Programmable Voice ve Elastic SIP Trunking için tüm Twilio bölgelerine uygulanıyor. Bu tur yeni test araması yapılmadı. Önceki21215 sonucu geçmişte korunur.


### H-038 — Açık talimatla telefon testi
- Tarih: 21 Ekim 2026. Kullanıcı arama yap dedi. Tek outbound API isteği kabul edildi; son durum completed. Kullanıcının mesajı duyduğu henüz teyit edilmedi.
- Önceki şahsi test hedefi, yerel Twilio ayarları, kısa Türkçe mesaj, maksimum30sn, kayıt kapalı. Otomatik yeniden arama yapılmadı; sır/numara/çağrı kimliği kaydedilmedi.

### H-039 — Telefon ses testi kullanıcı teyidi
- Tarih: 21 Ekim 2026. Kullanıcı Türkçe test sesini duyduğunu doğruladı; H-038 API completed (10sn) sonucuna dinleyici teyidi eklendi. Bu yalnız outbound bağlantı/TTS smoke testi; çift yönlü agent, STT, canlı dinleme ve rezervasyon henüz yok.
- Sonraki servis hazırlığı için .env ve .env.example içine eksikse boş DEEPGRAM_API_KEY alanı eklendi; mevcut değerler korunur. Deepgram hesabı veya ücretli satın alma yapılmadı.

### H-040 — Deepgram env erişim kontrolü
- Tarih: 21 Ekim 2026. Kullanıcı anahtarı eklediğini bildirdi. Deepgram kimlik doğrulaması başarılı (HTTP200). Resmî GET /v1/auth/token ile salt okunur kontrol; yanıt/sırlar çıktıya yazılmadı.
- Bu kontrol Türkçe Nova-3 transkripsiyon veya telefon ses akışı testi değildir. Yeni arama yapılmadı. Sonraki adım Twilio Media Streams için herkese açık HTTPS/WSS gateway hazırlığı; telefon sesini tarayıcıya verme ve agent hâlâ uygulanmadı.

### H-041 — Yerel ses gateway ve geçici tünel
- Tarih: 21 Ekim 2026. Kullanıcı Coolify deploy olmadığını belirtti ve geçici tünel önerisini ok ile kabul etti. app/voice_gateway.py ayrı8081 aiohttp STT prototipi ve resmi Cloudflared2026.10.3 Quick Tunnel hazırlandı/başlatıldı. Ana8080 uygulaması dışarı açılmadı.
- .env VOICE_PUBLIC_URL ve özel VOICE_MONITOR_TOKEN yapılandırıldı; örnek env boş alanlarla güncellendi. aiohttp/twilio sürümleri requirements içinde sabitlendi. Ses/transcript diske yazılmaz; bellekte100 olay, tek stream ve60sn sınır, Twilio imzası+account/format doğrulaması, tokenlı transcript erişimi.
- Kanıt:27 test geçti; public health200, yetkisiz uçlar403. İmzalı sentetik WSS start/stop ile Deepgram bağlantısı normal kapandı;0 ses frame. Gerçek telefon transkripsiyonu, agent veya canlı dinleme testi sayılmaz. Yeni arama yapılmadı.
- Etkilenen: gateway,5 yeni test, requirements, env şablonu, docs/LOCAL_VOICE_TEST.md. Geçici URL/sırlar geçmişe yazılmadı. Sonraki adım izinli gerçek telefon sesi transkripsiyonu.

### H-042 — Gerçek telefon STT denemesi
- Tarih: 21 Ekim 2026. Kullanıcı ok deneyelim dedi; şahsi test hedefine bir arama gönderildi,55sn üst sınır, kayıt kapalı. Son çağrı durumu completed; gateway ended; ses frame 0; final metin segmenti 0.
- Transcript içeriği/kişisel numara/sırlar geçmişe yazılmadı. Metin doğruluğu kullanıcıyla değerlendirilecek; LLM/rezervasyon agentı yok. Otomatik tekrar arama yapılmadı.

### H-043 — STT testinde erken kapanma incelemesi
- Tarih: 21 Ekim 2026. Kullanıcı konuşmaya fırsat olmadan kapanmayı bildirdi. Twilio son çağrı notification kodu31920 (WebSocket handshake) görüldü; H-042 sıfırframe bulgusuyla uyumlu. Kesin kök neden gerçek aramayla henüz yeniden doğrulanmadı.
- Twilio resmî security dokümanındaki WebSocket trailing-slash imza varyantı için doğrulama düzeltmesi ve regression testi eklendi; yapılandırılmış origin/imza zorunluluğu korunur. İmza reddi sayacı eklendi; sır yazılmaz.28 test geçti. Gateway yenilendi; tekrar arama yapılmadı.
- Kaynak: https://www.twilio.com/docs/usage/security . Sonraki kontrollü gerçek test hâlâ gerekli; sorun çözüldü diye kaydedilmedi.


### H-044 — Düzeltme sonrası açık talimatla STT araması
- Tarih: 21 Ekim 2026. Kullanıcının ara talimatıyla tek test. Son API durum completed; gateway idle; frame 0; final segment 0; imza reddi 1; Twilio diagnostic ['31920'].
-55sn sınır/kayıt kapalı; tekrar arama yok. Transcript içeriği ve özel kimlikler kaydedilmedi. Kullanıcı doğruluk teyidi henüz yok.

### H-045 — WSS imza URL şeması düzeltmesi
- Tarih: 21 Ekim 2026. Kullanıcı gerekli düzenlemeyi istedi. H-044 tekrarında gateway imza reddi1 ve Twilio31920 görüldüğünden valid_signature incelendi: HTTPS şeması kullanıyordu; Media Streams public WSS URL imzası gerektiriyor. HTTPS yerine WSS+trailing-slash doğrulaması uygulandı; imza/host kontrolleri kapatılmadı. Önceki sentetik HTTPS testi bu farkı kaçırmıştı.
- Kanıt:30 test geçti; yeni HTTPS/WSS ayrımı ve başka WSS host reddi testleri var. Gateway yenilendi. Public tünel üzerinden gerçek Deepgram bağlantısına25 mu-law20ms sessizlik frame gönderildi;25 frame/0 imza reddi/ended/WS1000 görüldü. Bu gerçek Twilio veya konuşma doğruluğu testi değil.
- Yeni telefon araması yapılmadı. app/voice_gateway.py, tests/test_voice_gateway.py ve docs/LOCAL_VOICE_TEST.md güncellendi. Sonraki adım kullanıcıyla tek kontrollü telefon testi.

### H-046 — WSS düzeltmesi sonrası telefon STT testi
- Tarih: 21 Ekim 2026. Kullanıcı başlat dedi; tek şahsi test araması/55sn üst sınır/kayıt kapalı. Son çağrı durum completed; gateway ended; frame 607; final segment 3.
- Transcript içeriği veya kişisel numara/sırlar geçmişe yazılmadı. Kullanıcı doğruluk teyidi bekleniyor. Otomatik yeniden arama yok.

### D-020 / H-047 — ElevenLabs Dilara ses seçimi
- Tarih: 21 Ekim 2026. Kullanıcı ElevenLabs Dilara https://elevenlabs.io/voices/D2dHiTSPRx6l2bhKGmyJ ile ilerlemeyi açıkça seçti. P-006 Polly Standard başlangıç TTS önerisinin yerine Dilara hedefi; Twilio/Deepgram/DeepSeek yönü korunur. Ses/model erişimi, ücret ve telefon kalitesi henüz doğrulanmadı; çalışan TTS henüz değiştirilmedi.
- Tarayıcıda Developers > API Keys > Create Key formu açıldı, TasteTrip Voice adı hazırlandı; anahtar üretilmedi. Kullanıcıya TTS erişimi ve Voices Read önerilecek. .env/.env.example ELEVENLABS_API_KEY boş alanı ve seçilen ELEVENLABS_VOICE_ID eklendi; sır kaydedilmedi.

### H-048 — ElevenLabs env ve ses metadata kontrolü
- Tarih: 21 Ekim 2026. Kullanıcı anahtarı env dosyasına eklediğini bildirdi. Ses metadata kontrolü HTTP400; durum voice_not_found.
- Salt okunur GET voice kontrolü; sır/yanıt bütünü yazılmadı. TTS üretim izni, kredi/plan uygunluğu ve gerçek ses üretimi bu kontrolle kanıtlanmaz. Yeni arama yapılmadı.

- H-048 ek doğrulama: Authenticated GET /v2/voices search=Dilara HTTP200;0 eşleşme. Anahtar Voices Read erişimi çalışıyor; seçilen ses hesap kütüphanesinde bulunamadı. Kullanıcıya Dilara sesini My Voices listesine ekleme adımı önerildi; plan yükseltmesi veya başka ses seçimi yapılmadı.


### H-049 — Dilara kütüphaneye ekleme sonrası kontrol
- Tarih: 21 Ekim 2026. Kullanıcı sesi eklediğini bildirdi. Seçili ses metadata HTTP200. Ses adı Dilara - Warm, Natural, Conversational. Salt okunur API kontrolü; TTS üretimi veya telefon araması yapılmadı.

### D-021 / H-050 — İngilizce Anna, Türkçe Dilara
- Tarih: 21 Ekim 2026. Kullanıcı İngilizce için Anna VoiceID XZXyuzPdidXaSa10PmVA eklediğini belirtti; İngilizce ses seçimi olarak kabul edildi. D-020 Türkçe Dilara korunur; başka dillerin sesi henüz seçilmedi.
- API bulgusu: Anna metadata HTTP200; ad: Anna - Conversational, Helpful. .env ve .env.example ELEVENLABS_VOICE_ID_TR/EN alanları hazırlandı; mevcut genel voice alanı korunur. Bu yapılandırma henüz çalışan dil bazlı TTS seçimi değildir. Ses üretimi/telefon testi yapılmadı; anahtar kaydedilmedi.

### H-051 — ElevenLabs121K kredi kapasite tahmini
- Tarih: 21 Ekim 2026. Kullanıcı Creator için121K kredi gördüğünü bildirdi; satın alma yapılmış sayılmadı. Resmî TTS sayfası yaklaşık1000kredi/üretilen ses dakikası ve Flashv2.5 API yarım kredi/karakter belirtiyor. Kaynak: https://elevenlabs.io/text-to-speech ve https://help.elevenlabs.io/hc/en-us/articles/21811236079505-How-do-I-find-the-model-ID . Ses bazlı credit modifier hariç.\n-121K kredi: standart yaklaşık121dk, Flash API yaklaşık242dk asistan sesi;3dk görüşmede asistan payı yüzde50 varsayımıyla yaklaşık80/160 arama. Bu ölçülmüş kapasite değil; Twilio/STT/LLM giderleri ve tekrar üretimler ayrı, Dilara modifier ayrıca doğrulanmalı.


### H-052 — Dilara + DeepSeek rezervasyon simülasyonu
- Tarih: 21 Ekim 2026. Kullanıcı Creator aboneliği aldığını bildirdi; Dilara TTS üretimi HTTP200 doğrulandı. Önceki arama talebi ve yeni koşulla22Ekim2026 19:00/3kişi senaryosu kuruldu; gerçek rezervasyon değil.
- app/voice_agent.py eklendi: DeepSeek thinking disabled, kısa yanıt, ElevenLabs Flashv2.5 ulaw8000, mark ile oynatma teyidi, söz kesmede clear, sınırlı sıra/geçmiş,180sn demo.34 test geçti; DeepSeek canlı yanıtı ve Dilara sesi ayrı doğrulandı.
- Tek telefon araması yapıldı. Son durum completed; frame 3673; final segment 9; tamamlanan assistant yanıtı 4; agent error None. Transcript içeriği, numara veya sır kaydedilmedi. Kullanıcı deneyim teyidi bekleniyor; otomatik tekrar arama yok.

- H-052 sonuç yorumu:73sn,3673 inbound frame,4 oynatımı tamamlanan assistant yanıtı; provider hata görünmedi. Restoran rolü uygunluk ve geçici tutma belirtti; müşteri adı senaryoda eksik olduğundan kesin rezervasyon sonucu çıkarılamaz. Agent isim netleşince ileteceğini söyledi; otomatik geri arama/takip özelliği yok, bu ifade uygulanmış kabiliyet sayılmaz. Gerçek ürün öncesi müşteri adı toplama ve takip vaadini sınırlama gerekli.


### D-022 / H-053 — Dijital asistan kimliğinin açık belirtilmesi
- Tarih: 21 Ekim 2026. Kullanıcı doğallığı yetersiz buldu; restoran çalışanının yanıltılmış hissetmemesi için arayanın rezervasyon isteyen kişinin dijital asistanı olduğunu söylemesini istedi. D-020/21 ses seçimleri korunur.
- Prompt ve deterministik ilk yanıt ön eki: yapay zekâ destekli dijital asistan ve müşteri adına arama açıklaması. Oynatma mark teyidi gelmeden tanıtım tamamlandı sayılmaz; kesilince sonraki yanıtta tekrar eklenir. Yapılmamış geri arama/takip vaadi de promptta yasaklandı. PRODUCT_REQUIREMENTS AC04.2 güncellendi;35 test aşamasında geçti. Yeni gerçek arama yapılmadı.

### H-054 — Yerel canlı dinleme ekranı
- Tarih: 21 Ekim 2026. Kullanıcı tarayıcıdan sesli takip ekranı istedi. product-design-and-ux skill task state ve AI belirsizlik referansları kullanıldı; tasarım kullanıcı araştırmasıyla doğrulanmış sayılmaz.
- localhost8081/monitor: Canlı dinle/sessize al/dinlemeyi bitir, ayrı bağlantı-görüşme durumu ve konuşmacı ayrımlı metin. Telefon başlatma/bitirme düğmesi yok; dinlemeyi kapatma telefon çağrısını bitirmez. Mikrofon izni istenmez. Türkçe yerel demo ekranı, ürün hesabına sahiplik entegrasyonu değil.
- Yerel Host+loopback ve proxy reddi;30sn tek kullanımlık dinleyici tokenı,WS Origin kontrolü,4 dinleyici, sınırlı paket kuyruğu, provider sırları tarayıcıya verilmez. İki ses kanalı WebAudio mu-law çözümleyiciyle oynatılır; asistan sesi gönderilen ses kopyasıdır, tam telefon playback eşzamanlılığı garanti değil. Clear ile bekleyen asistan sesi kesilir.
-39 test geçti. Tarayıcıda Canlı bağlı/Yeni görüşme bekleniyor durumu görüldü. Gerçek restoran görüşmesiyle dinleme henüz denenmedi; sentetik kontrol ayrıca kaydedilecek. Ekran sekmesi kullanıcıya açıldı.

- H-054 ek kanıt: Gerçek telefon araması olmadan public imzalı WSS/Deepgram/ElevenLabs sentetik başlangıçla dinleyiciye25 restoran sessizlik paketi ve87 Dilara ses paketi ulaştı. Twilio benzeri istemci mark teyidi verdi. Bu gerçek telefon dinleme kalitesi testi değildir.

### H-055 — Ön yüzden kontrollü test araması başlatma
- Tarih: 21 Ekim 2026. Kullanıcı canlı dinleme ön yüzünden arama tetiklemeyi istedi. Yerel monitor ekranına Test aramasını başlat ve arama durumları eklendi. Önce canlı dinleme açık olmalı; yalnız env içindeki izinli şahsi test hedefi aranır. Kullanıcı hedef numarayı istemci isteğiyle değiştiremez; ücretli/en fazla3dk ve demo koşulları görünür.
- app/voice_demo_calls.py: SQLite kalıcı girişim/idempotency, transaction ile tek aktif arama, starting kaydı POST öncesi, kayıp yanıt unknown ve yeni arama engeli, sağlayıcı status GET uzlaştırması. Süre180sn/kayıt kapalı, ağ POST tekrar yok. Yerel Host/Origin/proxy engeli devam eder. Bu genel rezervasyon/login/outbox entegrasyonu değildir.
-46 test geçti;7 yeni test duplicate, aktif guard, restart sonrası unknown, terminalden sonra açık yeni girişim, sabit hedef/süre, uzaktan ve yanlış Origin tetikleme reddi. Windows SQLite handle kapanması düzeltildi.
- Gateway yenilendi; tarayıcıda Canlı bağlı/Aramaya hazır ve etkin düğme doğrulandı. Gerçek ücretli arama düğmesine basılmadı. .env test hedefi eklendi; sır ve numara geçmişe yazılmadı. docs/LOCAL_VOICE_TEST.md ve Starthere güncellendi.

### H-056 — Anna ile sonraki restoran aramasının bilgileri kaydedildi
- Tarih: 21 Ekim 2026. Kullanıcı daha sonra Anna ile, verdiği restoran telefonu/Maps bağlantısı üzerinden Philip adına3kişilik rezervasyon görüşmesi yapılacağını söyledi ve bilgilerin kaydını istedi. Ayrıntılar docs/ANNA_RESTAURANT_CALL_BRIEF.md içinde kullanıcı kaynaklı olarak saklandı.
- Bu arama için tarih/saat/tz verilmedi; önceki Dilara demo zamanı taşınmadı. Restoran/telefon eşleşmesi bağımsız doğrulanmadı. Mevcut demo hedefi/env/çalışan prompt değiştirilmedi; arama, rezervasyon veya zamanlanmış görev oluşturulmadı. D-021 Anna ve D-022 açık dijital asistan kimliği korunur.

### D-023 / H-057 — Anna restoran senaryosu tarihi ve ayrı tetikleme
- Tarih:21Ekim2026. Kullanıcı yarın1PM, ayrı düğme ve canlı dinleme; onaydan sonra deney açıklaması/özür istedi. H-056 eksik tarih22Ekim2026 13:00 Los Angeles yerel saati olarak tamamlandı. Philip/3kişi/Anna İngilizce korunur.
- Telefon resmî BJ’s Burbank kaynağıyla eşleşti; Maps kısa link içeriği açılamadı. Ayrıntılı kaynaklar briefte. app/voice_scenarios.py ve profil bazlı agent/STT/VoiceID/düğme eklendi. İki sabit hedef ayrı, serbest numara isteği yok. Ortak tekaktif/idempotency koruması sürer.
- Onaydan sonra açıklama/özür yanında test rezervasyonunu iptal ettirme ve teyit isteme prompta eklendi; gerçek masa tutulması hedeflenmez. Prompt davranışı gerçek görüşmede doğrulanmadı; completed iptal/rezervasyon kanıtı sayılmaz.
-48 test geçti; Anna hedef/mode ve bilinmeyen profil reddi yeni kontroller. Gateway aktif görüşme yokken yenilendi. Tarayıcıda ayrı Anna düğmesi ve Canlı bağlı görüldü. Gerçek restoran araması yapılmadı.

### H-058 — Ön yüzde Twilio reddi incelemesi ve hata kaydı
- Tarih:21Ekim2026. Kullanıcı reddedildi mesajını bildirdi. Yerel DB son3girişim rejected/sid yok; provider Calls son kayıtlarında bu girişimlere karşılık yeni çağrı yok. Monitor Alerts yalnız eski31920 olaylarını gösterdi. FROM hesabın numaraları içinde doğrulandı. Kesin yeni red nedeni eski kayıttan çıkarılamadı; tahminle ülke/ödeme hatası denmedi.
- Önceki kod HTTP/code ayrıntısını saklamıyordu. DB migration ile error_code/http_status eklendi,4xx cevap kodu kalıcı ve ön yüze taşınıyor. Provider serbest mesajı/numaralar/sırlar saklanmıyor. Eski reddin kodu geriye dönük üretilemedi.
-49 test geçti; provider400/code21215 kalıcı kaydı ve UI yanıtına taşınması test edildi. Yeni gerçek arama veya satın alma yapılmadı. Bir sonraki kullanıcı tetiklemesinde kesin kod görülebilecek.


### H-059 — BJ’s aramasında21216 engeli
- Tarih:21Ekim2026. Kullanıcı şahsi hedefin arandığını fakat BJ’s reddi sürdüğünü bildirdi. Yerel kayıt son3reddedilen girişim HTTP400/error21216; çağrı oluşturulmadan engellenmiş. Son kişisel deneme201/busy; kullanıcının ulaşım bildirimiyle bağımsız kaynaklar ayrılır.
- Resmî21216 dokümanı +1 hedeflerde onaylı Primary Customer Profile gereksinimini ve8Ekim2025 sonrası ABD/Kanada dışı hesaplarda Business Primary Customer Profile şartını belirtiyor. Önceki Individual profilin bu şartı karşıladığı varsayılmaz. Kesin hesap profil incelemesi yapılmadı; risk/regülasyon ihtimalleri de aynı kodda olabilir.
- Kaynak https://www.twilio.com/docs/api/errors/21216 . UI21216 için açıklayıcı mesaj eklendi. Yeni arama, profil başvurusu veya servis satın alımı yapılmadı; sır yazılmadı.

### D-024 / H-060 — Anna restoran hedefi Dublin olarak değiştirildi
- Tarih:21Ekim2026. Kullanıcı BJ’s yerine Dublin telefonunu/Maps linkini verdi ve ön yüzü güncellemeyi istedi. D-023 Burbank aktif hedefinin yerine Dublin Botanical/Dublin One hedefi; eski kayıt korunur. Philip/3kişi/22Ekim13:00 bu kez Europe/Dublin yerel saati, Anna İngilizce ve deney sonrası özür/iptal teyidi talebi korunur.
- Telefon https://dublinonehotel.com/find-us/ resmî kaynakta otel genel hattı olarak doğrulandı. Restoran yönlendirmesi isteme prompta eklendi; oda rezervasyonu değil. Maps içeriği bağımsız doğrulanmış sayılmaz.
- app/voice_scenarios.py, monitor ön yüzü, sabit hedef testi ve arama briefi güncellendi. Bu tur arama yapılmadı; yeni ülkeye erişimin çalışacağı henüz doğrulanmadı.

### H-061 — Dublin Anna görüşmesi incelemesi
- Tarih:21Ekim2026. Kullanıcı görüşmeyi canlı takip edebildiğini bildirdi. Son kayıt Twilio completed/157sn, diagnostic yok, gateway ended/7844frame/agent_error yok;6 mark-tamamlanan assistant yanıtı görüldü. Ücret henüz API price alanında yok; maliyet çıkarılmadı.
- Geçici final transcript: otel IVR karşılama ardından resepsiyon; Anna dijital asistan kimliğiyle Botanical masa rezervasyonlarına yönlendirme istedi. Personel bu hattan rezervasyon yapamadıklarını ve OpenTable web sitesi gerektiğini belirtti. Anna teşekkür edip bitireceğini söyledi. Rezervasyon onayı veya iptal yok;3kişi/13:00 talebi rezervasyon görüşmesine dönüşmedi.\n- Bulgular: Yanıtta kimlik tanıtımı tekrarları ve olumsuz yönlendirmeden sonra benzer soruların3kez sürmesi gereksiz uzatıyor; IVR/bekleme ayrımı ve kanal desteklenmiyor sonlandırması iyileştirme önerisi, henüz uygulanmadı. Otomatik metindeki personel adı/otel adı hatalı olabilir. Ham transcript/kişisel kimlikler kalıcı dosyaya kopyalanmadı; yalnız sonuç özeti. Yeni arama yapılmadı.


### D-025 / H-062 — The Goat hedefi ve arama denemesi
- Tarih:21Ekim2026. Kullanıcı yeni Dublin telefonu/Maps bağlantısını ekleyip deneme istedi. D-024 aktif Botanical hedefi The Goat Bar and Grill,Goatstown olarak değiştirildi; önceki hedef geçmişte korunur. Philip/3kişi/22Ekim13:00 Europe/Dublin ve Anna İngilizce koşulları aynı. Kaynak https://www.claytonhotels.com/hotel-near/the-goat-bar-grill-dublin/ telefon eşleşmesi. Kullanıcı Maps linki https://maps.app.goo.gl/mVNF9utFz7KEWRXE8 .
- Ön yüz/senaryo/sabit hedef testi güncellendi;49 test geçti. Canlı dinleme açılarak UI düğmesinden tek arama başlatıldı. Son durum completed; frame 4042; final segment 4; agent_error None. Ayrıntı sonuç ayrıca yorumlanacak; ham metin veya kişisel kimlikler kaydedilmedi.

- H-062 sonuç incelemesi: Son transcriptte karşı taraf3kez hello dedi; Anna tek tam oynatılmış kimlik/işletme teyit sorusu verdi. Rezervasyon talebine/onayına geçilmedi; rezervasyon veya iptal yapılmış sayılamaz. API süre 82sn. Yeni tekrar arama yapılmadı. Ses/yanıt gecikmesi ve söz kesme döngüsü iyileştirme ihtiyacı görüldü; kesin gecikme nedeni henüz ölçülmedi.

### D-026 / H-063 — Sessizlikte teyit ve10sn kapatma
- Tarih:21Ekim2026. Belirsiz ilk ifadeden sonra kullanıcı açıkça Beni duyabiliyor musunuz/Orada mısınız teyidi ve10sn üzerinde karşı ses yoksa telefonu kapatma istedi.
- app/voice_silence.py:4sn uygulama varsayılanında bir teyit,10sn sessizlikte WS kapatma (mevcut TwiML devamındaki Hangup ile çağrı sonlanır). Kendi normal konuşması sayaçtan hariç; teyit sorusu sayacı uzatmaz. Inbound mu-law RMS ses aktivitesi ve STT metni sayacı yeniler; sessizlik paketleri yenilemez. Gürültü/müzik aktivite sayılabilir; bu konuşmacı-anlama/VAD kalitesi garantisi değil.
- Türkçe/İngilizce kısa teyitler; ek LLM isteği yok. Cevap gelince bekleyen teyit iptal/clear. Monitor kapanma nedenini açık gösterir. Sessizlikle bitiş rezervasyon iptal edildi anlamına gelmez; belirsiz sonuç ayrı kontrol edilmeli.
-54 test geçti: zaman eşiği/tek teyit/ses sonrası reset/kendi sesi/mu-law sessizlik ve gerçek WS close çağrısı kontrolü. Gateway aktif görüşme yokken yenilendi; yeni telefon araması yapılmadı.

### H-064 — Anna Türkçe WAV örneği
- Tarih:22Ekim2026. Kullanıcı küçük Türkçe Anna örneğini WAV istedi. Anna VoiceID ve eleven_flash_v2_5/language_code tr ile API üretimi başarılı. PCM24kHz16bit mono çıktı WAV kapsayıcısına yazıldı, wave ile format/süre kontrol edildi. artifacts/audio/anna-turkce-ornek.wav ve metin dosyası saklandı; telefon araması veya aktif ses tercihi değişikliği yapılmadı. Dinleyici doğallık değerlendirmesi henüz yok.

### D-027 — Ana ses Anna
- Tarih:22Ekim2026. Kullanıcı Anna ana sesimiz olsun dedi. D-020 Türkçe Dilara/D-021 İngilizce Anna ayrımının yerine Anna ana ses seçimi; önceki kayıtlar korunur. .env ve örnek genel/TR/EN VoiceID alanları Anna olarak güncellendi, Türkçe demo kimliği ve ön yüz adı Anna oldu. Telefon modeli Flashv2.5 değişmedi; Afrikaans örneği için yalnız çıktı üretiminde v3 seçildi. Çalışan process env yüklemesi ancak servis yenilenince uygulanır. Telefon araması yapılmadı.

### H-065 — Anna beş dilli tek WAV örneği
- Tarih:22Ekim2026. Kullanıcı aynı metni sırayla Türkçe/İngilizce/Arapça/Japonca ve bir Afrika dilinde istedi. Afrikaans seçildi; API models üzerinden v3 beş dili, Flashv2.5 yalnız ilk4ünü desteklediği doğrulandı. Tüm bölümler aynı Anna+eleven_v3 ile üretildi.
- artifacts/audio/anna-bes-dil.wav:75.6sn,24kHz16bit mono, bölümler arasında1sn sessizlik. Her bölüm ayrı WAV ve çeviri/model/süre manifesti artifacts/audio/anna-multilingual altında. WAV formatı/süre kontrol edildi; anadil konuşuru kalite değerlendirmesi yapılmadı.54 test geçti; yeni telefon araması yok.

### D-028 / H-066 — Dil bazlı Flash/v3 router planı
- Tarih:22Ekim2026. Kullanıcı Flashv2.5 destekliyorsaFlash, desteklemiyorsa v3 ile arama yönlendirmesi planlamamızı istedi. Anna ana ses korunur. İkisinde de desteklenmeyen dil arama öncesi açık hata. Native altyazı dili değil görüşme dili esas alınır.
- docs/ELEVENLABS_LANGUAGE_ROUTER_PLAN.md oluşturuldu; canlı GET models dil listeleri kontrol edildi. STT/LLM/sabit metin ve telefon ses formatı uygunluğu ayrı kabul kapısı. Afrikaans v3 WAV kanıtı tam telefon dili desteği sayılmaz.
- Uygulama sırası, normalizasyon/snapshot politikası, tüm TTS noktaları, hata ayrımı, maliyet ve planlanan testler belgelendi. Kod/env/servis değişmedi; yeni test veya telefon araması yapılmadı. Planlanmış router çalışıyor diye kaydedilmedi.

### D-029 — Onboarding ve master kullanıcı tercihleri
- Tarih: 22 Ekim 2026. Kaynak: Kullanıcı, Qloo kişiselleştirmesi için onboarding ve kullanıcıya özel kalıcı tercih bölümü planlanmasını; akış diyagramı, soru seti ve tercihlerden sonraki API kullanımında sürekli yararlanılmasını istedi.
- Kabul edilen kapsam: Ortak tercih verisi, onboarding ve önerilerde tekrar kullanım. D-010 işlem anında login ve D-009 kullanıcı tetiklemeli içerik önerisi korunur. Onboarding ekran sırası veya soru sayısı bu talimatla kesinleşmiş sayılmaz.
- PRODUCT_REQUIREMENTS.md FR-14 eklendi; docs/ux/08-onboarding-and-taste-profile.md planı kaydedildi. Yeni profil/endpoint/UI kodu uygulanmadı.

### H-067 — Mevcut tercih yapısı ve onboarding planı
- Tarih: 22 Ekim 2026. Doğrulanmış kod bulgusu: app/server.py ziyaretçi prefs/medya tercihleri ve seyahat taslağını ayrı saklıyor; /api/preferences seyahat şemasına bağlı. app/planner.py ve app/providers.py mevcut entity sinyalleri, kategori/konum/fiyat ve medya konu filtrelerini kullanıyor; bütün kategorilere ortak hesap profili çözümleyicisi yok.
- Önceki canlı Qloo deneyleri ve resmî qloo/docs-public Insights referansı incelendi. Yeni API çağrısı veya onboarding kullanılabilirlik testi yapılmadı. Yeni parametrelerin hackathon sunucusundaki desteği ayrıca doğrulanacak; dokümantasyon desteği canlı doğrulama diye yazılmadı.
- Tasarım önerisi: kısa, atlanabilir tanışma; yemek/seyahat zevki ve isteğe bağlı favori araması; medya detayları ilk Öneri al sırasında. Master profil ile seyahate özel bağlam ayrı, kullanıcı onaysız çıkarım/kalıcı overwrite yok. Sorular, Mermaid akışları, sahiplik/dil/hata durumları ve planlanan kabul kontrolleri UX08 içinde. Henüz benimsenmiş ekran kararı değildir.
- Starthere güncel yönü ve history özeti güncellendi; önceki kayıtlar korundu. Sonraki adım önerilen akışın değerlendirilmesi ve profil veri katmanının geliştirilmesi. Sır veya kişisel tercih verisi kaydedilmedi.


### D-030 — Onboarding planını uygulama talimatı
- Tarih: 22 Ekim 2026. Kaynak: Kullanıcının “plana göre entegrasyonları tamamla” talimatı. D-029/H-067 önerisi üç adımlı, atlanabilir onboarding ve ortak profil yönüyle geliştirmeye alındı. Giriş aksiyonda ve kullanıcı tetiklemeli içerik önerisi korunur.
- Uygulama tercihleri: misafir için hatırlama başlangıçta kapalı/oturum cookie'si; açıkken 180 gün. Sunucudaki anonim master kayıtları son düzenlemeden 180 gün sonra servis başlangıcında temizlenir; oturum cookie'si sunucu kaydının anında silinmesi değildir. Hesap profili kalıcıdır ve cihazdan aktarım açık alan seçimiyle yapılır. Otomatik çıkarım ve rota komutuyla profil değiştirme yok.
- Önceki tasarımın tüm ileri özellikleri tamamlandı sayılmaz: tür başına tek içerik dili, Türkçe arayüz; üretim rezervasyon/altyazı bağlantısı mevcut ayrı arama çalışmasının kapsamındadır. Bu iş canlı telefon araması yapmadı.

### H-068 — Ortak profil, onboarding ve Qloo entegrasyonunun doğrulaması
- Tarih: 22 Ekim 2026. app/profiles.py sürümlü SQLite profil, sunucu kataloğundan kimlik doğrulama, GET/PATCH profil, sıfırlama ve alan bazlı hesap aktarımı ekler. Profil sürüm çakışmaları 409; PATCH aynı Origin/JSON/header kontrollerine tabidir. Hesap/cihaz sahipliği ayrıdır; çıkış ve doğrudan hesap değişiminde cihaz taslağı ayrılır.
- app/server.py, planner.py ve providers.py güncel profili rota/içerik önerilerine bağlar. Tercih ve zorunlu koşullar ayrı; mutfak koşulları müze/kitap sorgularına geçmez. Zorunlu yemek etiketleri sonuçlarda da kontrol edilir; dışlanan belirli kayıtlar sorgu ve sonuçta ayıklanır. Rota revizyonu profili değiştirmez ve var olan yerleri yeniden doğruladığını iddia etmez. Yeni öneri cache'i yok, güncel sürüm okunur.
- app/static/profile.js ve index/style: üç adım, görsel seçimler/özet, favori/tekil dışlama araması, gerçek katalogdan ek mutfak araması, rota gerekmeden içerik tercih düzenleyicisi, açık hatırlama ve hesap fark/aktarım ekranı. İçerik önerisinde kalıcılık yalnız açık checkbox ile. Eski medya verileri legacy_pending olarak korunur; doğrulanmış sinyal diye otomatik taşınmaz.
- 71 unittest geçti; Python compileall ve iki JS dosyasının node --check kontrolü başarılı. Yeni testler sahiplik/hesap değişimi, stale sürüm, CSRF/PATCH, kimlik uydurma, kategori ayrımı, dinamik mutfak, içerik kayıt opt-in, upstream hata koruması ve legacy verinin korunmasını kapsar. Test SQLite handle'ları Windows'ta açık kalmayacak şekilde kapatıldı.
- Hedef Qloo sunucusunda 10 salt okunur çağrı: 8 etiket sinyali, vegan intersection ve entity dışlama; hepsi başarılı. Küçük Roma örneğidir, kalite/evrensel envanter kanıtı değildir. docs/validation/qloo-profile-contract-2026-10-22.json yalnız sayım/koşul kanıtlarını tutar; script tekrar üretilebilir, anahtar kaydedilmedi.
- Ayrı yerel QA verisiyle tarayıcı onboarding adımları, gerçek Qloo favori araması/seçimi, kaydetme ve yenilemede geri yükleme görüldü. Ana kullanıcı profiline sentetik tercih yazılmadı. Dar ana uygulama görünümünde onboarding görseli artifacts/ux/onboarding-2026-10-22.png. UI testi ilk yüklemede script hazır olma yarışını ve adım düğmesi etiketini ortaya çıkardı; DOMContentLoaded ve durum korumasıyla düzeltildi.
- Canlı profil+rota kontrolünde tarayıcıdaki ilk iki istek 503 verdi; bu iki hatanın kesin upstream nedeni kaydedilmedi. Ardından HTTP üzerinden iki ayrı canlı profil/rota isteği 200 ve ikişer gün döndürdü; biri tarayıcıda oluşturulan aynı zevk profiliyle. Tekrarlar kullanıcıya otomatik arama/rezervasyon etkisi oluşturmadı. Bu kayıt başarısız denemeleri başarı olarak saymaz.
- README, UX08, IMPLEMENTATION_STATUS ve başlangıç/güncel özetler güncellendi. Flask 8080 son kodla yenilendi; ayrı QA servisi kapatıldı. Coolify/ARM64 deploy veya gerçek telefon araması yapılmadı.


### D-031 — Rezervasyon yapısını uygulamaya ekleme
- Tarih: 22 Ekim 2026. Kaynak: Kullanıcı “Rezervasyon yapısını da ekleyelim” dedi. D-008/D-010 ve FR-03–FR-08/FR-11/FR-13 kapsamında rota kartından giriş, koşul inceleme, açık arama başlatma, takip ve sonuç yapısı geliştirildi. Ücretli gerçek restoran araması bu talimatla otomatik tetiklenmedi.
- İlk uygulama masa rezervasyonu restaurant/cafe/bar; diğer kategori kanalları, ödeme/depozito ve canlı alternatif teklif karar kartı henüz yok. Önceki geniş ürün kabul hedefleri silinmedi veya tamamlandı sayılmadı. Kesin koşullar ilk uygulama sınırıdır; alternatif isteğini kaldıran kalıcı ürün kararı değildir.
- Anna ana ses ve D-016 dil ayrımı korunur. D-028 router ürün ses yoluna uygulandı; eski sabit deney senaryoları ayrı kaldı. Ürün promptu test rezervasyonu/otomatik iptal istemez; eski gerçek restoran testinin koşulları yeni kullanıcı rezervasyonuna taşınmadı.

### H-069 — Rezervasyon çekirdeği, ses köprüsü ve doğrulama
- Tarih: 22 Ekim 2026. app/reservations.py sahiplikli prepare/start/status/stop/listen/sonuç/özet API'leri, immutable onay özeti, 10dk inceleme süresi, rota sürümü/digest, E.164/ülke/yerel saat/DST doğrulaması ve atomik girişim/outbox ekler. Prepare hesabın rota kopyasını korur. Start web thread'inde provider POST yapmaz. Aynı anahtar aynı girişim; belirsiz sonuç otomatik yeniden aranmaz. Bilinen ret/başarısızlık sonrası açık eski girişim referansıyla yeni deneme mümkün.
- app/reservation_worker.py kalıcı claim, tek create-call POST, SID GET uzlaştırması, stop, native çeviri ve sürümlü özeti yürütür. Yanıt kaybında unknown; ileride başlayan/eski worker POST'u tekrar etmez. Provider durum uzlaştırması yeni restoran onayını ezmez. Geç transcript eski özeti geçersiz kılar; özet tekrar denemesi yeni telefon oluşturmaz.
- app/reservation_bridge.py ve gateway; user/attempt kapsamlı 30sn tek kullanımlı token, Origin kontrolü, sınırlı dinleyici/buffer, iki taraf μ-law ses fanout ve final event dedup getirir. Ürün ve yerel demo dispatch'i gateway lease'iyle ayrılır. Ses dosyası/DB arşivi yok; metin/özet/script 30 gün, worker saatlik temizlik. Son koşul/sonuç kaydı temizlikle iptal edilmez.
- Sonuç kanıtı: uygulamanın kesin koşul readback'i tamamlanmış playback'ten sonra kaydedilir. Hemen sonraki açık TR/EN restoran cümlesi dar tüm-cümle kuralına uyarsa restaurant_exact_reply onayı; uygunluk/soru/çelişki onay değildir. Sonraki belirsiz düzeltme unknown yapar. Diğer ifade/dillerde kullanıcı konuşma satırını inceleyip kabul/ret teyidi yapabilir (user_review). LLM özeti tek başına confirmed yazamaz. Onaylı durak rota üzerinde görünür/korunur; stop gerçek masa rezervasyonunu iptal etmez.
- Dil router: canlı ElevenLabs models snapshot'ı app/voice_models.json, Nova-3 belgedeki dil kesişimi, base dil normalizasyonu, Flash destekliyorsa Flash yoksa v3. Worker seçilen modelin dil desteğini arama öncesi yeniden kontrol eder. TR/EN dışı açılış/teyit metinleri aramadan önce hazırlanır ve literal koşullar doğrulanır. Tüm dillerde gerçek telefon kalitesi denenmiş değildir. Snapshot periyodik otomatik yenilemesi yok; eski demo TTS yolu Flash olarak kaldı.
- Arayüz: tarih/saat/kişi/ad/ülke/saat dilimi/dil/istek formu; telefon/işletme ve saat dilimi kontrolü, ayrı ücretli arama özeti/onayı, Rezervasyonlarım, Canlı dinle/sessize al/durdur, orijinal/çeviri satırları, özet ve belirsiz sonuç incelemesi. Rota kartında durum ve takip bağlantısı. Logout/session değişiminde dinleme/kişisel görünüm temizlenir.
- 102 unittest geçti. Yeni kontroller; auth/sahiplik/CSRF, stale/expired onay, idempotency/restart/timeout, outbox stop, model kapısı, v3 ön hazırlığı, WSS attempt/Origin/replay ve sentetik iki yön ses, değişmez readback, yanlış/erken onay ve düzeltme, provider/sonuç yarışı, özet sürümü ve kaynak referansı. Python compileall ve üç JS node --check başarılı. Testler gerçek arama başlatmadı.
- Canlı küçük API kontrolleri: Flash/TR ulaw_8000 11146 byte ve v3/Afrikaans 8960 byte HTTP200; canlı DeepSeek yapılandırılmış readback aksiyonu onaylı şablonu kullandı, kısa native çeviride 3/19:00 korundu. docs/validation/reservation-voice-contract-2026-10-22.json ve reservation-agent-contract-2026-10-22.json yalnız metrik içerir; sır/ses kaydı yok. Bu, telefon uçtan uca veya tüm diller için kalite testi değildir.
- Tarayıcıda ayrı sentetik ve araması kapalı QA servisiyle form→özet→onay kapısı görüldü; artifacts/ux/reservation-review-2026-10-22.png. Ana uygulamada Rezervasyonlarım ve doğru türde rezervasyon kartı doğrulandı. Ürün DB'sinde son kontrolde 0 attempt; gerçek restoran aranmadı ve sentetik rezervasyon ana DB'ye yazılmadı. QA servisi kapatıldı.
- Eski geçici ses URL'si DNS çözülmedi; aynı 8081 gateway için Cloudflare Quick Tunnel yenilendi, yalnız VOICE_PUBLIC_URL env alanı güncellendi. Yeni public /health HTTP200 ve worker heartbeat/ready doğrulandı. Gateway anahtarı veya API sırları geçmişe yazılmadı. Dış health erişilemiyorsa yeni ücretli çağrı dispatch edilmez.
- compose.yaml üç servis/shared web-worker volume, gateway dahili web API'si, ayrı healthcheck ve üretimde demo kapalı ayarları içerir. phonenumbers 9.0.41/tzdata 2026.5 universal wheel eklendi. Docker/ARM64/Coolify deploy yapılmadı. Güncel web8080/gateway8081/worker yerelde yenilendi; gerçek telefon pilotu ayrıca kullanıcı tarafından belirli hedef/koşul için başlatılmalı.
- Etkilenen: README, RESERVATION_IMPLEMENTATION, rezervasyon planı, dil router planı, COOLIFY_DEPLOYMENT, IMPLEMENTATION_STATUS, PRODUCT_REQUIREMENTS uygulama kaydı ve başlangıç/güncel özetler. Önceki karar/kayıtlar korundu.


### D-032 — Sohbet merkezli deneyim ve açık tercihlerden otomatik profil kaydı
- Tarih: 26 Ekim 2026. Kaynak: Kullanıcı deneyimin tamamen chatbot merkezli olmasını, girişte tercih öğrenen journey ve DeepSeek ile kullanıcı adına veritabanı kaydı istedi.
- D-030'un üç adımlı ana onboarding UI kararı bu talimatla supersede edildi; tarihsel kayıt korundu. D-029 master profil, D-010 işlem anında giriş, cihaz/hesap ayrımı ve kullanıcı tetiklemeli içerik önerisi korunur.
- Açık genel beğeniler sohbet içinde otomatik çıkarılıp doğrulanarak kaydedilir; D-030'daki genel otomatik çıkarım yasağı yalnız bu açık ifade işleme kapsamıyla değişti. Modelin örtük/spekülatif çıkarımları kabul edilmiş tercih sayılmaz. Tek seyahat istekleri ayrı kalır; gerçek Qloo kimliği model tarafından uydurulamaz. Rezervasyon araması açık koşul incelemesi ve onay gerektirir.
- Journey ve sınırlar docs/ux/09-chat-first-journey.md. Soru sırası/etkileşim ayrıntıları kullanıcı araştırmasıyla doğrulanmış değildir.

### H-070 — Chat onboarding uygulaması ve doğrulama
- Tarih: 26 Ekim 2026. app/chat.py sahiplikli SQLite chat_threads, sürümlü/idempotent mesaj kaydı, DeepSeek JSON çıkarımı, son kullanıcı ifadesinden alıntı kontrolü, mevcut profil şeması doğrulaması ve atomik profil+sohbet transaction ekler. Profil veya sohbet eşzamanlı değişirse 409 ve yarım kayıt yok. Aynı mesaj kimliği son 100 mesaj içinde tekrar yazılmaz. 20 mesaj/5dk sahip başına sınır vardır.
- Yeni ana yüzey app/static/chat.js/chat.css: fotoğraflı sohbet, örnek yanıtlar, tek soru yolculuğu, görünür kayıt makbuzu, profil özeti ve tek sayfalık inceleme/düzeltme, açık hatırlama, sohbet temizleme. Eski büyük seyahat formu ana deneyimden çıkarıldı. Şehir/tarih/gün/kişi sohbetten toplanır; doğrulanmış rota oluşturma kartı mevcut Qloo+DeepSeek yoluna bağlanır. Rota düzenleme komutu önce aksiyon kartı olur; mevcut planner doğrulamaları korunur.
- Favori/konu/mutfak eşleşmesi gerçek Qloo araması ve açık seçimle kaydedilir. Filtrelenmemiş metin ID gibi gönderilmez. Ana dil/içerik dili ve seyahat bağlamı master profilden ayrıdır. Hassas özel koşullar otomatik çıkarımla yazılmaz; editörde açık giriş mümkündür. Metnin anlamsal olarak doğru yorumlanması model bağımlıdır; alıntı doğrulaması tek başına anlam doğruluğu garantisi değildir.
- Sohbet son 100 mesajı tutar, son 16 mesaj model bağlamına girer. 30 gün etkin olmayan thread servis başlangıcında temizlenir (mesaj başına tam 30 günlük TTL iddiası yok). Cookie kimlik taşır; cihazda hatırlama varsayılan kapalıdır. Hesaba girişte anonim sohbet otomatik taşınmaz; profil açık alan aktarımı mevcut davranışını korur. Kimlik değişiminde eski yanıtın yeni hesaba çizilmesini önleyen UI nesil kontrolü vardır.
- 110 unittest geçti (8 yeni sohbet testi): kayıt/reload, kaynak/kapsam, uydurma ID, model hatası, idempotency/çakışma, hesap/ziyaretçi ayrımı, temizleme sürümü ve telefon aksiyonunu reddetme. Python compileall ve app/profile/chat JS sözdizimi kontrolleri geçti. Gerçek telefon başlatılmadı.
- Ayrı data/chat-ui-qa verisiyle tarayıcıda canlı DeepSeek: kahve/müze/sakin tercihleri kaydedildi, sonraki yalnız-seyahate hızlı tempo isteği master sakin tercihini değiştirmedi. Yenilemede sohbet/profil geri geldi. Sohbet aksiyonuyla canlı Qloo + LLM, Paris için iki günlük rota ve gerçek görsel/harita/rezervasyon/Öneri al kartları döndü. Ana kullanıcı profiline sentetik tercihler yazılmadı. Küçük örnek tüm dil/cümle kalitesi kanıtı değildir.
- Ürün rezervasyon onay/dinleme, kullanıcı tetiklemeli medya önerileri, kayıtlı rotalar ve Aviasales ayrıntı yüzeyi korundu. Rezervasyon ve uçuş ayrıntıları hâlâ yardımcı form/kart yüzeyleridir; tamamı doğal dille doldurulan araçlar diye sunulmaz. Coolify/ARM64 deploy, gerçek rezervasyon telefonu ve formal erişilebilirlik/kullanılabilirlik çalışması yapılmadı.

- H-070 son kontrol: Ana web 8080 son kodla yeniden başlatıldı; mevcut hesap profili ve eski rota korundu, açılış mesajı mevcut ilgi alanlarını tanıdı. Dar görünümde clientWidth/scrollWidth 375/375; yatay taşma görülmedi. Geçici viewport sıfırlandı. Görsel artifacts/ux/chat-first-2026-10-26.png. Ayrı QA servisi ve sekmesi kapatıldı; ana uygulama tarayıcıda açık bırakıldı. Son küçük iyileştirmeler sonrası 8 sohbet testi ve JS sözdizimi kontrolleri tekrar geçti.


### D-033 — Deneyimin tamamı tek bir konuşma akışı
- Tarih: 26 Ekim 2026. Kaynak: Kullanıcı, D-032/H-070 uygulamasından sonra “deneyimin tamamını bir chat deneyimine değiştir” talimatını tekrarladı. D-032'de kalan yardımcı form/ayrı yüzey sınırı kaldırıldı; yalnız ana onboarding değil, bütün akış konuşma içinde ilerler.
- Ayrı açılış/yan menü/rota/listeler/tercih ekranı ve modal pencereler ana deneyimden çıkarıldı. Bilgi toplama konuşmadadır; gerçek katalog seçimi, güvenli kimlik bilgisi ve consequential onaylar konuşma içi kart/checkbox/buton olarak kalır. Şifre normal mesaj veya LLM girdisi değildir.
- D-010 giriş aksiyonda, D-029 ortak profil, açık medya kaydı, Qloo kimlik doğrulaması ve D-031 ücretli aramanın ayrı açık onayı korunur. “Tam sohbet” talimatı LLM'e otomatik telefon/ödeme yetkisi vermez. Önceki kayıtlar silinmedi.

### H-071 — Bütünleşik konuşma uygulaması ve kontroller
- Tarih: 26 Ekim 2026. app/chat_tasks.py yapılandırılmış uçuş/rezervasyon/medya görev taslaklarını ayırır; app/chat.py gerçek sunucu rotasını bağlama verir ve taslakları chat_threads.tasks içinde kalıcılaştırır. LLM bilinmeyen durak, telefon, verified/approved/digest veya keyfi araç alanı yazamaz; rezervasyon koşulları yalnız inceleme aksiyonu üretir. Hazırlama/start mevcut ürün API'sinde kalır, paralel arama yolu yok.
- app/static/full-chat.js/css tek tam-yükseklik konuşma, altta mesaj alanı, konuşma içi fotoğraflı rota, gün/harita/menü, tercih özeti/tek alan kaldırma, uçuş havalimanı/fiyat, içerik eşleşme/öneri, rota kaydı/listeler, güvenli auth/alan bazlı aktarım ve rezervasyon kontrol/ücretli onay/canlı takip kartlarını bağlar. Ayrı uzun tercih ve rezervasyon bilgi toplama formları gösterilmez. Rezervasyonun ad/saat/kişi/not bilgisi konuşmayla toplanır, yerel saat/telefon kontrolü ve açık arama onayı kartta kalır.
- Profil özel koşulu yalnız son mesajda açık kayıt/hatırlama ifadesiyle çıkarılabilir; tek seyahat notu ayrı kalır. Native/konuşma/içerik dili ayrımı ve kitapta konu/sevilen eser seçimi korunur. Yeni sohbet mevcut metni temizlemeyi açık kartta onaylatır; rota/profil/rezervasyonu veya sürmekteki telefonu iptal etmez. Görünür ses bağlantısı kapatılabilir.
- Kimlik değişiminde konuşma kartları ayrılır, kalıcı DOM bileşenlerinin bağlantıları korunur. LLM ve yeni asenkron uçuş/medya/listeler için eski kimliğe ait yanıtın yeni konuşmaya çizilmesini önleyen nesil kontrolleri eklendi. Giriş öncesi bekleyen aksiyon, kimlik değişimi bildiriminden sonra devam eder.
- 117 unittest geçti (15 chat/task testi dahil); Python compileall, app/chat/full-chat JS sözdizimi kontrolleri başarılı. Yeni kontroller gerçek server rota bağlamı, görev taslağı devamı, bilinmeyen durak, onay bayrağı reddi, uçuş tarihleri, medya ID'si ve açık özel koşul kaydıdır. Testler telefon oluşturmadı.
- scripts/chat_ui_preview.py ayrı data/full-chat-ui-qa DB ve sentetik rota kullanır; Twilio hesap/token alanları boş. Tarayıcıda sentetik hesapla konuşma içi giriş → rezervasyon sorusu → 19:00/ad/3 kişi/dil bilgilerinin mesajla verilmesi → telefon/saat kontrol kartı → immutable ücretli onay özeti görüldü. Aramayı başlat tıklanmadı; örnek checkbox işaretleri yalnız sentetik QA senaryosudur, gerçek işletme doğrulaması sayılmaz.
- Aynı QA konuşmasında uçuş isteğine geçildi; canlı DeepSeek İstanbul–Paris/15Kasım/tek yön taslağı çıkardı, gerçek autocomplete seçeneklerinden IST/CDG seçilip Aviasales API sonucu konuşmada gösterildi. Tam tarihte önbellek fiyatı bulunamadı; uçuş var/yok veya kesin fiyat iddiası yapılmadı. Tarayıcı seçim durumunun geçici busy etiketiyle yanlış işaretlenmesi görüldü ve düğme referansına göre seçimle düzeltildi.
- Podcast için aynı konuşmada bilim konusu/İngilizce dili/tek mola kapsamı çıkarıldı; gerçek Qloo Science konu eşleşmesi ve dil bilgisi konuşma içi kartta görüldü. Bu, tüm ifadeler/diller için model başarısı veya kullanıcı araştırması değildir.
- Ana DB'de restart öncesi 0 aktif ürün araması görüldü. Ana web8080 son backend ile yenilendi; mevcut hesap/sohbet/rota korundu. Dar görünümde clientWidth/scrollWidth 390/390, mesaj alanının altı 844px viewport içinde 796.8px; yatay sayfa taşması görülmedi. Geçici viewport sıfırlandı. artifacts/ux/full-chat-2026-10-26.png ve full-chat-mobile-2026-10-26.png kaydedildi.
- Geçici araç seçimleri/fiyat ve içerik sonuç kartlarının bütünü kalıcı sohbet arşivi değildir; sayfa yenilemesinde havalimanı/konu seçimi tekrar yapılabilir. Kalıcı profil/rota/rezervasyon ve konuşma görev taslakları sunucudan yüklenir. Bu sınır dokümanda belirtilir. Gerçek telefon, üretim Coolify/ARM64 ve formal erişilebilirlik/kullanılabilirlik testi yapılmadı.
- Etkilenen: docs/ux/10-complete-conversation.md, PRODUCT_REQUIREMENTS, README, IMPLEMENTATION_STATUS, Starthere ve bu geçmiş. D-032'nin fotoğraflı açılış/yardımcı yüzey anlatımı tarihsel olarak korunur.

- H-071 son içerik kontrolü: Sentetik QA durak kimliğiyle /api/recommend iki denemede 503 verdi; bu denemeler başarılı içerik önerisi sayılmadı. İkinci hata, seçimleri koruyan ve tekrar deneme/düzeltme yolunu açıklayan kalıcı konuşma kartında görüldü. Kesin upstream hata nedeni bu kayıtta kanıtlanmış sayılmaz.
- Gerçek UUID Qloo durak sinyaliyle ayrı salt okunur kontrol: 4 podcast adayı, 4 İngilizce dil eşleşmesi, 4 Apple Podcasts bağlantısı; bilinmeyen dil 0. Bu kontrol ana profil/rota/rezervasyonu değiştirmedi; yalnız QA içerik dil önbelleğine yazdı. Podcast UI konu seçiminde aria-pressed doğru seçili görüldü. Son 15 chat/task testi ve JS sözdizimi kontrolleri tekrar geçti.

- H-071 kapanış: Ayrı QA web servisi ve sekmesi kapatıldı. Ana 8080 sekmesi son frontend ile yenilendi; gönderilmemiş giriş metni varsa korunacak şekilde işlem yapıldı. Ana kullanıcı adına telefon veya yeni rezervasyon başlatılmadı.


### H-072 — Sıfır misafir oturumu
- Tarih: 26 Ekim 2026. Kaynak: Kullanıcı “sıfır bir session başlat” istedi. POST /api/session/new ve konuşma üstünde Sıfır oturum kontrolü eklendi; mevcut giriş session'ı kapatılır ve ziyaretçi cookie kimliği yenilenir. Önceki profil, sohbet, kayıtlı rota ve eski anonim taslak silinmez. Eski anonim cookie'ye erişim yoksa o anonim kayda UI üzerinden geri dönüş garanti değildir; hesap kayıtları yeniden girişle erişilebilir.
- Tarayıcıdan aksiyon uygulandı: Giriş yap düğmesi, ilk tanışma mesajı, boş sohbet ve rotasız başlangıç görüldü. artifacts/ux/fresh-session-2026-10-26.png. Web8080 yenilendi; bu işlem telefon başlatmadı.
- 11 chat testi geçti; yeni test kimlik rotasyonu, yeni oturum boşluğu ve eski cookie kapsamındaki sohbetin korunmasını doğrular. JS sözdizimi geçti. Sır/cookie değeri geçmişe yazılmadı.


### H-073 — Serbest tempo ifadesinde mesaj gönderimi düzeltildi
- Tarih: 26 Ekim 2026. Kaynak: Kullanıcı mesaj kutusundaki metnin Gönder ile sohbete gitmediğini bildirdi. Tarayıcıda profil enum doğrulama hatası görüldü; ayrı canlı DeepSeek kontrolü pace=Rahat çıktısını doğruladı. Sunucu Sakin/Dengeli/Yoğun beklediği için tüm tur 400 oluyordu.
- app/chat.py promptuna kesin enum sözleşmesi eklendi; rahat/relax/slow vb. bilinen tempo eşanlamlıları canonical değerlere çevrilir. Diğer geçersiz model tercih çıktısında profil korunur, kullanıcı mesajı ve açıklayıcı yanıt kaydedilir; geçerli kullanıcı metni sırf model enum hatası yüzünden reddedilmez.
- app/static/chat.js gönderilen mesajı yanıt beklenirken hemen konuşmada gösterir. Hata halinde metin/pending kimliği korunur; kimlik değişiminde eski bekleyen mesaj temizlenir. Başarısız mesaj başarı gibi işaretlenmez.
- Kullanıcının kutudaki metni yenilemede korundu, Gönder üzerinden gerçekten gönderildi. Tarayıcıda anında Gönderiliyor durumu, ardından asistan yanıtı ve Tempo kayıt makbuzu görüldü; giriş alanı temizlendi. Ana profil yalnız kullanıcının gönderilmesini istediği açık tercih doğrultusunda değişti; sentetik tercih eklenmedi. artifacts/ux/chat-send-fixed-2026-10-26.png.
- 119 unittest geçti; 17 chat/task testi içinde yeni rahat tempo regresyonu ve geçersiz model tercihinde profil koruması var. JS sözdizimi geçti. Web8080 son kodla yeniden başlatıldı; telefon veya deploy yapılmadı.


### D-034 — GitHub deposu ve Coolify proje/domain hazırlığı
- Tarih: 27 Ekim 2026 kullanıcı talimatı; hazırlık 28 Ekim'e geçti. Kaynak: Mevcut projeyi https://github.com/baadir/tastetrip.git deposuna yükleme, Coolify'da yeni Tastetrip projesi, tastetrip.bahadirciftci.work domaini ve bu depodan deployment planı.
- Kabul edilen hedef aynı Coolify/CAX21 yönüdür; yeni platforma geçiş değil. Uygulama kaynağı GitHub main ve mevcut Dockerfile'dır. Üç servisli tam rezervasyon yapısı korunur; web-only konfigürasyon tam sesli rezervasyon yayını sayılmaz. Kullanıcı bu turda belirli bir telefon araması istemedi.

### H-074 — Kaynak yükleme, Coolify konfigürasyonu ve dağıtım planı
- Tarih: 27–28 Ekim 2026. Yerel klasör başlangıçta Git deposu değildi; GitHub baadir/tastetrip boş ve PUBLIC olarak doğrulandı. main oluşturuldu, origin bağlandı, 129 dosyalı ilk commit d4d4d52 başarıyla push edildi. Mevcut GitHub geçmişi ezilmedi/force push yapılmadı. Dosya sistemi ownership kaydı olmadığı için Git güvenli dizin ayarı yalnız komut bazında verildi; global koruma değiştirilmedi.
- .gitignore artifacts, log ve SQLite dosyaları için genişletildi. .env, data, .venv, ses/görsel artifact'lar dışarıda. Stage dosyaları mevcut yerel anahtar/token değerleri ve yaygın key kalıplarına karşı tarandı; 0 eşleşme. Kişisel yerel DB/hesap/sohbet kayıtları ve API sırları GitHub'a yüklenmedi. Repository görünürlüğü public olarak korundu.
- Coolify'da Tastetrip projesi dy0g44moqkbcxsshesm6k6xl ve production ortamı wugoylfk2w7x1jzujumrk9na oluşturuldu. Yeni web uygulaması wpsrxqjtiwj8w64igmghpk4x, public Git kaynağı https://github.com/baadir/tastetrip, main, Dockerfile, base /, /Dockerfile ve port8080 olarak kaydedildi. HTTPS domain https://tastetrip.bahadirciftci.work. Mevcut başka proje veya domain ayarına müdahale edilmedi.
- Named volume wpsrxqjtiwj8w64igmghpk4x-tastetrip-data → /app/data oluşturuldu; Source Path boş, Docker volume. Gerçek build sonrası UID10001 yazma ve redeploy kalıcılığı henüz test edilmedi.
- Yedi sır olmayan değişken Coolify'da runtime-only kaydedildi: APP_ORIGIN, COOKIE_SECURE, DATA_DIR, PORT, DISABLE_DEMO_CALLS, LLM_BASE_URL, QLOO_API_URL. 7 buildtime checkbox false, 7 runtime true görüldü. Qloo/DeepSeek/Aviasales/Twilio/Deepgram/ElevenLabs sırları aktarılmadı; LLM_MODEL ve gizli runtime alanları yayın öncesi tamamlanmalı.
- UI genel konfigürasyon ilk fill girişlerini kaydetmedi; gerçek klavye olaylarıyla alanlar yeniden girildi ve kalıcılık kontrol edildi. Bu ilk girişler kayıt başarısı sayılmadı. Chrome CDP navigasyon zaman aşımı, mevcut browser/tab üzerinden toparlandı; başka otomasyon mekanizmasına geçilmedi.
- Mevcut 119 unittest geçti. Yerel Docker daemon kapalı olduğu için container build yapılmadı. DNS sorgusunda domain Cloudflare A/AAAA edge adreslerine çözülüyor; bu, origin eşleşmesi veya TLS sertifikası doğrulaması sayılmaz. Deploy düğmesi tıklanmadı, uygulama Exited ve henüz canlı değil. GitHub App/webhook kurulumu yapılmadı; otomatik push→deploy doğrulanmış değildir.
- docs/COOLIFY_TASTETRIP_PLAN.md web yayın adımları, runtime sırları, DNS/TLS, volume/redeploy/yedek, tek Compose içinde paylaşılan veri ve gateway/worker geçiş planını kaydeder. Ek gateway domaini kullanıcı adına atanmadı. Docker/ARM64 çalışma ve gerçek telefon testi sonraki yayın kontrolüdür.
- Coolify: https://panel.bahadirciftci.work/project/dy0g44moqkbcxsshesm6k6xl/environment/wugoylfk2w7x1jzujumrk9na/application/wpsrxqjtiwj8w64igmghpk4x . Kaynak: https://github.com/baadir/tastetrip . Sır/tam env içeriği geçmişe yazılmadı.


### H-075 — Coolify API giriş alanları hazırlandı
- Tarih: 28 Ekim 2026. Kullanıcı environment listesinde API alanlarını göremediğini bildirdi. H-074 sırasında yalnız yedi genel değişken vardı.
- Mevcut Tastetrip web kaynağına 12 boş alan kaydedildi: QLOO_API_KEY, LLM_API_KEY, LLM_MODEL, AVIASALES_API_TOKEN, AVIASALES_PARTNER_ID, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, DEEPGRAM_API_KEY, ELEVENLABS_API_KEY, VOICE_MONITOR_TOKEN, VOICE_PUBLIC_URL.
- UI üzerinden toplam 19 isim ve tüm alanlarda buildtime kapalı/runtime açık doğrulandı. Yeni alanların değerleri boştur; kullanıcı dolduracak. Yerel sırlar aktarılmadı. Deploy veya telefon araması yapılmadı. Ekran kanıtı: artifacts/deployment/coolify-api-fields-2026-10-28.png.
- Sonraki adım: Kullanıcı gerekli sağlayıcı değerlerini ve desteklenen LLM_MODEL değerini girip Update ile kaydetmeli; sonrasında yayın kontrolleri yapılabilir. Ses alanlarının bulunması gateway/worker kurulumunun tamamlandığı anlamına gelmez.


### H-076 — İlk Coolify web deploymentı tamamlandı
- Tarih: 28 Ekim 2026 yerel oturum; Coolify logları UTC 27 Ekim 21:13–21:14 gösteriyor. Kullanıcı deployment başlatılmasını açıkça istedi. Deploy UI üzerinden başlatıldı: xfb9j6404vtl2cawynbqcz1y, kaynak main/e55842e2727c077cd910fa5380068405341f56e0.
- Docker image build tamamlandı, yeni container ilk healthcheck denemesinde başarılı oldu; rolling update tamamlandı ve UI Deployment is Finished / Running (healthy) gösterdi.
- HTTPS https://tastetrip.bahadirciftci.work/ tarayıcıda sertifika uyarısı olmadan sohbet arayüzünü açtı. /health yanıtı status=ok doğrulandı. Kanıtlar artifacts/deployment/tastetrip-live-2026-10-28.png ve coolify-deployed-2026-10-28.png.
- API anahtar değerleri okunmadı/aktarılmadı; canlı sağlayıcı sohbet/rota/uçuş, kayıt-redeploy kalıcılığı ve gateway/worker telefon akışı bu turda test edilmedi. Web yayını doğrulandı; tüm ürün entegrasyonları doğrulanmış sayılmaz. Gerçek telefon araması yapılmadı.


### D-035 / H-077 — İngilizce karşılama, mesaj dilinde sohbet
- Tarih: 28 Ekim 2026. Kullanıcı girişte tamamen İngilizce karşılanmayı, sonrasında yazdığı dilde yanıt almayı istedi. Önceki Türkçe açılış bu kararla değişir; tam sohbet deneyimi D-033 korunur.
- İlk ve geri dönen ziyaretçi karşılaması, görünür açılış kısa yolları, öneri mesajları, composer/erişilebilir etiketler ve açıklama İngilizce yapıldı. DeepSeek reply dili son mesajı ve açık dil isteğini izler; belirsiz kısa mesaj önceki konuşma dilini korur, başlangıç varsayılanı İngilizcedir. Ana dil/altyazı alanı mesaj dilinden tahmin edilmez. Canonical profil enumları değiştirilmedi.
- Ayrı geçici DB ile gerçek DeepSeek testinde İngilizce → Türkçe → Fransızca üç tur 200 ve beklenen dilde yanıt verdi. İlk denemede Türkçe prompt etkisi görüldü, ana prompt İngilizce düzenlendikten sonra tekrar doğrulandı. 119 unittest ve iki JS sözdizimi kontrolü geçti. Kayıtlı eski mesajlar çevrilmez; yardımcı işlem kartlarının tam yerelleştirilmesi bu değişiklikte yapılmadı.

- H-077 yayın doğrulaması: 27c393e ardından tarayıcı statik JS önbelleği için e6ddb04 sürüm parametresi düzeltmesi push/deploy edildi. Coolify son deployment Finished; canlı başlık, İngilizce header/kısa yollar/composer/açıklama doğrulandı. Eski kullanıcı konuşması ve mevcut Dublin rotası redeploy sonrası korundu; test için kullanıcı geçmişi sıfırlanmadı. artifacts/deployment/tastetrip-english-entry-2026-10-28.png.


### D-036 / H-078 — Uygulamanın tüm sabit metinleri İngilizce
- Tarih: 28 Ekim 2026. Kullanıcı ekrandaki Türkçe yanıt/aksiyon/hata kartını göstererek uygulamada Türkçe kalmamasını istedi. D-035/H-077 içindeki yalnız karşılama çevirisi kapsamı genişletilir; önceki kayıt korunur. İngilizce uygulama UI ve kullanıcının mesaj dilindeki asistan yanıtı birlikte sürer. Kullanıcının kendi yazdığı mesajlar, geçmiş konuşma, yer/eser adları ve restoran dilindeki konuşma/ana dil altyazısı otomatik silinmez veya çevrilmez.
- Sohbet aksiyonları, profil/kayıt/giriş kartları, uçuş/rota/medya/rezervasyon alanları, canlı izleme UI, erişilebilir etiketler ve API doğrulama/hata metinleri İngilizceye çevrildi. Intl ülke/dil adları English. Statik JS sürüm parametreleri güncellendi. Eski rota sistem notice/mode metinleri görünümde çevrilir.
- Tercih enum/theme değerleri kalıcı uyumluluk için korunur; görünümde English label kullanılır. Eski locale.ui_language=tr okunurken en sunulur; profile_version/ana dil/beğeni değiştirilmez. Eski istemci tr yazımı uyumlu kabul edilip en normalize edilir.
- Canlı DeepSeek testinde önceki Türkçe/Fransızca geçmişin İngilizce kısa komutu etkilediği yeniden üretildi. Son mesajı ayrı user rolünde geçirmek tek başına yetmedi. Her tur küçük bir dil sınıflandırma çağrısı eklendi; doğrulanan dil o tur sistem sözleşmesine açıkça yazılır ve yalnız chat thread dil durumudur, master native dili değildir. İlave bir LLM isteği maliyet/gecikmesi vardır. Gerçek API: EN→TR→EN→FR→EN beş tur doğru yanıt dili ve 200.
- 123 unittest geçti; dört yeni test eski profil/ana dil koruması, English API hata metni, dil yönlendirme ve HTML/erişilebilir metin taraması içerir. Tüm statik JS sözdizimi başarılı. Ayrı DB/8084 tarayıcı testinde Show my itinerary → aksiyon → English hata kartı/toast, English profil/tempo/ulaşım ve güvenli giriş kartı görüldü. Gerçek telefon yapılmadı; API anahtarları değiştirilmedi. Yayın doğrulaması aşağıya eklenecek.

- H-078 yayın doğrulaması: e28b404237a7d95ff864433b42a7c99109d85966 GitHub main push edildi ve Coolify zpgwg0n9kadp58gw0ixdinen build kaynağı bu SHA olarak doğrulandı; Deployment is Finished. Canlı ayrı tarayıcı oturumunda Show my itinerary → English yanıt → English aksiyon → English hata kartı ve toast doğrulandı. Kanıt: artifacts/deployment/tastetrip-all-english-live-2026-10-28.png. Coolify Running bağlantısının commit etiketi eski SHA gösteriyordu; sürüm kanıtı import logu ve canlı değişen UI davranışıdır.
- Yerel 8080 Python sunucusu hedef PID doğrulanarak yeniden başlatıldı; mevcut veri klasörü korundu. Test oturumları ayrı artifacts/localization/qa-data DB kullandı. Üretimde yalnız sentetik rota sorgusu yapıldı, profil beğenisi/hesap/rezervasyon/telefon oluşturulmadı.

- H-078 son tarama: yerel ses test modülündeki dört kullanıcıya yansıyabilen doğrulama hatası da İngilizceye çevrildi; Türkçe gerçek telefon senaryosu/ses metinleri çok dilli özellik olarak korundu.

- H-078 son yayın: aa82c57 Coolify vu7immpfme41js9tru63xb9l üzerinden Finished doğrulandı; ses testi hataları için 8 ilgili test geçti. Tam ürün UI düzeltmesi ve önceki canlı hata kartı kanıtı geçerlidir.


### D-037 / H-079 — Ayrı Sign up ve kayıt akışı incelemesi
- Tarih: 28 Ekim 2026. Kullanıcı ayrı kayıt butonu ve kayıt sürecinin gözden geçirilmesini istedi. Önceki checkbox içindeki kayıt seçimi, ayrı Sign in/Sign up kart modlarıyla değiştirildi. Tek sohbet ve işlem anında giriş kararı korunur.
- Username/parola/parola tekrarı, açık kurallar, göster/gizle, iki mod arasında geçiş, kayıt sonrası otomatik giriş ve bekleyen işe dönüş uygulandı. Hesap açıkken Sign up gizlenir, çıkışta geri gelir. Sonraki veri yenilemesi başarısızsa başarılı kayıt yanlışlıkla başarısız gösterilmez. Parola/confirmation sohbet veya LLM verisi değildir.
- Server register boolean doğrulaması ve varsa confirmation eşleşmesi eklendi; eski API kayıt istemcileri korunur. Kullanıcı adı kuralları ve parola uzunluğu hataları ayrıldı. Ana dil/profil aktarımı/rezervasyon onayı değişmedi.
- 126 unittest geçti (3 yeni kayıt testi), statik JS sözdizimi başarılı. Ayrı artifacts/localization/qa-data DB üzerinde tarayıcıyla mismatch, signup, auto login, bekleyen My trips dönüşü, logout, duplicate, Sign in geçişi doğrulandı. Sentetik hesap yalnız yerel QA ortamındadır; prod hesap/telefon/rezervasyon oluşturulmadı.
- docs/ux/11-signup-and-signin.md akışı, doğrulama sınırını ve mevcut parola kurtarma/e-posta doğrulama eksikliğini kaydeder. Yayın sonucu aşağıya eklenecek.

- H-079 yayın: 389d185 Coolify x6q4rn2bijpz1z44a5tonm5q Finished ve canlı Sign up/kayıt alanları doğrulandı. Canlı ilk yükleme sırasında anonim kimlik yanıtı açık kayıt kartını kapatabildi; ilk owner değerinin visitor olarak başlatılmasıyla gereksiz kimlik değişimi temizliği kaldırıldı. Son düzeltme JS sürüm v3 ile yayınlanacak.

- H-079 son yayın: fb14370, Coolify u84bnfwc2q64ss1lxqy8277m Finished. Canlı sayfa yenilendiğinde Sign up ilk tıklamada açık kaldı; Sign in / Sign up ayrı kontrolleri ve username/password/confirmation alanları görüldü. artifacts/deployment/tastetrip-signup-live-2026-10-28.png. Yerel 8080 sunucusu da yeni Python koduyla yeniden başlatıldı; QA 8084 kapatıldı.


### H-080 — SSH ile üretim telefon yapılandırması teşhisi
- Tarih: 28 Ekim 2026. Kullanıcı açık sekmede call yapılandırma uyarısını bildirdi ve root@46.62.143.154 SSH log incelemesine açıkça izin verdi. SSH mevcut kimlikle başarılı; anahtar/parola değerleri yazdırılmadı. Açık 127.0.0.1:8082 sekmesi browser güvenlik politikası nedeniyle okunamadı; bu kısıt aşılmadı ve konuşma içeriği başka yoldan alınmadı. Yerel 8082 dinleyicisi gözlenmedi.
- Sunucuda TasteTrip yalnız fb14370 web container olarak healthy çalışıyor; aynı kaynak için durmuş container dahil başka servis yok. Paylaşılan /app/data volume mevcut. Gateway/rezervasyon worker containerı yok; reservation_worker_heartbeat tablosunda kayıt yok, worker_ready=false. Bu H-074/H-076 web-only yayın sınırıyla uyumlu.
- Web runtime ortamında Twilio SID/token/from, VOICE_PUBLIC_URL, VOICE_MONITOR_TOKEN, Deepgram, ElevenLabs key ve LLM key/model/base alanları dolu; yalnız var/yok kontrolü yapıldı, değerler doğrulanmadı. ELEVENLABS_VOICE_ID yok; VOICE_GATEWAY_INTERNAL_URL ve RESERVATION_WEB_URL yok. Arama start yolu önce missing configuration nedeniyle 503 verir; voice ID eklenmesi tek başına workersız yapıyı çalıştırmaz.
- VOICE_PUBLIC_URL eski trycloudflare geçici tünel adresidir. Web container içinden /health bağlantısı ConnectionError verdi. HTTPS biçimi geçerli olması erişilebilir gateway kanıtı değildir. Kalıcı gateway HTTPS/WSS adresi ve üç servisli dağıtım hâlâ tamamlanmalı.
- Son 12 saat loglarının maskelenmiş incelemesinde bir reservation start isteği 503 bulundu. Bu, bildirilen uyarıyla uyumludur; okunamayan sekmedeki konuşmayla aynı girişim olduğu kesinleştirilmedi. API anahtarı sağlayıcı yetkileri/bakiye/dil desteği test edilmedi. Gerçek arama, prod veri değişikliği veya servis yeniden başlatma yapılmadı.


### D-038 / H-081 — Üretim gateway ve rezervasyon worker dağıtımı
- Tarih: 28 Ekim 2026. Kullanıcı H-080 teşhisindeki aksiyonların tamamlanmasını açıkça istedi. Mevcut Coolify kaynağı aynı GitHub main deposuyla Docker Compose /compose.coolify.yaml yapısına geçirildi; yeni bağımsız web kaynağı oluşturulmadı. Gateway için uygulama tercihi voice-tastetrip.bahadirciftci.work; mevcut wildcard DNS çözülmesi doğrulandı. Önceki belgelerde adres belirlenmemiş durumu bu kurulumla güncellendi.
- Anna public voice ID, kalıcı VOICE_PUBLIC_URL ve servis içi adres alanları Coolify runtime ayarlarına eklendi. Mevcut sağlayıcı sırları okunup yazdırılmadı, repo/build içine konmadı; runtime varlıkları kullanıldı. Demo calls kapalı kaldı.
- Root-only Coolify kaynak/ayar/encrypted-env metadata yedeği ve SQLite backup alındı. pending outbox=0 ve active attempts=0 doğrulandı. Parser v5 external aliası bile yeniden isimlendirdiği için eski volume kullanılacak varsayımı yapılmadı; ortak yeni managed volumea SQLite backup API ile kontrollü aktarım yapıldı. Eski volume ve yedek korundu. İlk readonly kaynak denemesi sidecar erişimi nedeniyle başarısız oldu, eski web hemen açıldı; tekrar durdurup kaynak filesystem rw/veritabanı ro bağlantısıyla retry başarılı. Boş olmayan hedef ezilmedi. Integrity ok, bir kullanıcı ve bir kayıtlı rota korundu.
- İlk Compose deployment uc074tq4txepxs2rr8l6jahx Finished: web/gateway/worker healthy. Public web ve gateway HTTPS health 200; API options worker_available=true, DB heartbeat hazır ve 1 saniye yaşında. Twilio account GET 200; ElevenLabs models/Anna metadata 200, Flash ve v3 mevcut; Deepgram Nova-3 STT WebSocket kimlik doğrulaması başarılı, ses gönderilmedi. İmzasız public Twilio WSS 403. Gerçek telefon oluşturulmadı.
- Gateway canlı dinleme origin kontrolü için APP_ORIGIN eksikliği Compose son kontrolünde görüldü; prod origin eklendi, aktif arama yokken ikinci dağıtım x146vgaks490vk2355az9f13 başlatıldı. Son kontrol sonucu aşağıya eklenecek.
- 126 test geçti. docs/VOICE_PRODUCTION_RUNBOOK.md volume/parser sınırı, yedek/geri dönüş ve arama yapmadan kontrolleri kaydeder.

- H-081 son dağıtım: a961bf9 / x146vgaks490vk2355az9f13 Finished; web/gateway/worker healthy. Prod Origin ile kısa ömürlü imzalı sentetik dinleme tokenı kullanılarak public WSS bağlantısı ve connection/active=false cevabı doğrulandı; yanlış Origin 403. Bu test DBde girişim/rezervasyon yaratmadı.
- Son web kontrolleri: missing call configuration boş; from number E.164 ve public URL biçimi geçerli; worker_available=true. Yeniden dağıtım sonrasında bir kullanıcı/bir kayıtlı rota korunuyor; reservation_attempts toplamı 0. Sağlayıcı auth/model/voice/STT bağlantıları test edildi, gerçek telefon/TTS ses üretimi veya restoran görüşmesi yapılmadı. Browser yerel sekme kısıtı aşılmadı; doğrulamalar bağımsız sunucu servis/health/WSS kontrolleridir.



### D-039 / H-082 — Reservation approval and live call popup
- Date: 28 October 2026. Source: explicit user request. Adopted decision: reservation verification, separate paid-call approval, live audio/captions and stop controls open in a native modal over chat. This supersedes the reservation/live-call portion of D-033; preference collection, booking details and the rest of the product remain conversational. Earlier records are preserved.
- Implemented in reservation-modal.js/css with the existing reservation API and native dialog. Phone/business and restaurant-local-time checkboxes remain explicit; the model cannot approve them. Closing/Escape disconnects listening, not the phone call; an active-call reopen button is available. No new call endpoint or authorization bypass was added.
- Polling continues while an active call window is closed, and while the terminal call summary is pending/working. On terminal status the followed call closes the modal, returns focus to the composer and creates one chat summary card. Ready/failed/insufficient/expired summary states and reopening the transcript/outcome review are supported. Unchanged polls do not rebuild the summary card. Unknown call status remains unresolved, not terminal. Owner/attempt guards prevent stale polling responses from replacing another active record.
- Verified: 126 Python tests passed; changed JS syntax and git diff whitespace checks passed. Independent loopback fixture scripts/call_popup_ui_preview.py uses separate artifacts/call-popup-qa data, empty provider credentials, simulated reservation endpoints and no telephone calls. Browser confirmed unchecked verification rejection, separate unchecked paid-call approval/disabled start, simulated live transcript popup, close/reopen, terminal automatic close/composer focus, pending-to-ready update in one summary card, and reopening a finished record without immediate close; Escape closes it. Screenshots: artifacts/ux/call-popup-approval.png, call-popup-live.png, call-popup-summary.png. Browser viewport override did not take effect (still 1280px); narrow mobile sizing is CSS-defined but was not verified in a real narrow viewport.
- Boundary: no actual phone call, provider media test or deployment was performed for this change. Original 8082 conversation was not accessed. Backend durable records remain available through My reservations; transient summary cards follow the existing chat-card lifecycle.
- Affected documents: PRODUCT_REQUIREMENTS.md, docs/ux/10-complete-conversation.md, docs/ux/12-reservation-call-popup.md, docs/RESERVATION_IMPLEMENTATION.md, Starthere.md. Next: deploy when requested; validate a real authorized call and narrow mobile viewport separately.


### H-083 — Reservation popup deployed to Coolify
- Date: 28 October 2026. Source: user explicitly requested deployment. Commit 1f6963f pushed to GitHub main; Coolify deployment e108e5kfbekev7mh667pcjds finished.
- Before deployment active/unresolved calls=0, users=1 and saved plans=2. After deployment all three services (web, voice-gateway, reservation-worker) are healthy; users=1 and saved plans=2 remain, active calls=0.
- External web/gateway HTTPS health=200; reservation options worker_available=true; production HTML includes the versioned popup script and the script responds 200 with the summary logic. A server-origin urllib request returned 403; independent requests from the development machine returned 200 for all checks. No security setting was changed to bypass that result.
- No real telephone call or new reservation was created. Browser interaction was not needed for this deployment; the user's local 8082 conversation was not accessed. Synthetic UI evidence remains H-082; full live-call media behavior was not retested.
- Current state: D-039 popup implementation is deployed at https://tastetrip.bahadirciftci.work. Earlier local-only entries remain historical. A page refresh loads the versioned assets.
