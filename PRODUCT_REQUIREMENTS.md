# Kişisel Seyahat Rotası ve Rezervasyon Asistanı

Tarih: 20 Ekim 2026  
Durum: Kullanıcının ürün fikrinden oluşturulan gereksinim ve kabul kriterleri  
Kapsam (21 Ekim 2026, D-008): Restoran, kafe, bar, otel ve gezilecek yer keşfi → çok günlük kişisel rota → kullanıcı seçimiyle gereken duraklara rezervasyon → canlı dinleme ve altyazı.

## 1. Ürün amacı

Seyahat eden müşterinin tercihlerini, tarihlerini ve seyahat koşullarını anlayarak restoran, kafe, bar, otel ve gezilecek yerlerden çok günlük kişisel rota oluşturan; müşterinin seçtiği ve rezervasyona uygun duraklarda rezervasyon girişimini yöneten bir uygulama geliştirmek. Qloo aday seçimi ve zevk ilişkileri için kullanılır; ulaşım süresi, rota sıralaması, bilet/oda müsaitliği ve rezervasyon için ayrı uygulama mantığı veya veri entegrasyonu gerekir.

21 Ekim kapsam değişikliği D-008 ile kayıtlıdır. Aşağıdaki restoran odaklı FR-01–FR-08 mevcut rezervasyon alt akışı olarak korunur; rota kapsamı FR-09–FR-11 ile genişletilir. İlk teknik teslim kapsamı henüz seçilmedi. Ayrıntılı akış: [Rota UX taslağı](docs/ux/06-trip-itinerary.md).

Müşteri, rezervasyon görüşmesini uygulamadan canlı dinleyebilir. Görüşme müşterinin ana dili dışında yapılıyorsa konuşma içeriği müşterinin ana dilinde canlı altyazıyla gösterilir. Agentın konuşma sesi ElevenLabs veya eşdeğer bir TTS servisiyle üretilir.

Bu belge ürün kabulünü tanımlar. Hackathon teslim koşulları ayrıca [HACKATHON_REQUIREMENTS.md](HACKATHON_REQUIREMENTS.md), Qloo yetenekleri [QLOO_CAPABILITIES.md](QLOO_CAPABILITIES.md) dosyasındadır.

## 2. Ana kullanıcı akışı

1. Müşteri seyahat konumunu, tarih/süreyi, ana dilini, tercihlerini ve günlük gezi koşullarını belirtir.
2. Sistem tercihleri Qloo’nun kullanabileceği girdilere dönüştürür.
3. Sistem uygun mekân adaylarından düzenlenebilir günlere ayrılmış rota sunar; bilinmeyen süre ve müsaitlikleri açık gösterir.
4. Müşteri durakları değiştirir, rezervasyon girişimi istediği durağı seçer ve koşullarını belirtir.
5. Sistem koşulları özetler; müşteri rezervasyon girişimini başlatır.
6. Sesli agent restoranı telefonla arar ve koşulları iletir.
7. Müşteri görüşmeyi canlı dinler; yabancı dildeki görüşmeyi ana dilinde altyazıyla takip eder.
8. Sistem doğrulanmış rezervasyon sonucunu müşteriye gösterir.

## 3. Fonksiyonel gereksinimler ve kabul kriterleri

### FR-01 — Müşteriyi ve seyahat bağlamını anlama

**Gereksinim:** Sistem müşterinin restoran tercihlerini Qloo destekli keşif için toplamalıdır.

- **AC-01.1:** Müşteri hedef şehir/bölgeyi ve ana dilini belirtebilir.
- **AC-01.2:** Müşteri sevdiği restoran, mutfak veya kültürel öğeler gibi tercih sinyallerini girebilir. Arayüz, kullanılan Qloo entegrasyonunun desteklediği girdilere göre tasarlanır.
- **AC-01.3:** Sistem serbest metin tercihlerini gerektiğinde geçerli Qloo entity/tag kimliklerine eşler; belirsiz eşleşmelerde müşteriden seçim ister.
- **AC-01.4:** Eşleşmeyen bir tercih desteklenen bir Qloo girdisiymiş gibi gönderilmez; müşteriye açıklama veya alternatif sunulur.
- **AC-01.5:** Müşteri bütçe ve beslenme gibi ek kısıtları belirtebilir. Qloo’nun desteklemediği kısıtlar uygulama tarafından ayrıca ele alınır.
- **AC-01.6:** Müşteri öneri almadan önce tercihlerini gözden geçirebilir ve değiştirebilir.

### FR-02 — Restoran önerilerini sunma

**Gereksinim:** Sistem müşteri tercihleri ve seyahat konumuna göre Qloo destekli restoran seçenekleri sunmalıdır.

- **AC-02.1:** Başarılı öneri akışında gerçek Qloo API sonucu kullanılır; test/sentetik veri varsa açıkça işaretlenir.
- **AC-02.2:** Her restoran kartında en az restoran adı, mevcut konum/adres bilgisi ve öneri gerekçesi gösterilir. Eksik bilgi uydurulmaz.
- **AC-02.3:** Gerekçe kullanılan tercih ve mevcut verilere dayanır; Qloo eşleşme skoru kesin beğeni olasılığı olarak sunulmaz.
- **AC-02.4:** Müşteri seçenekleri karşılaştırabilir ve bir restoran seçebilir.
- **AC-02.5:** Müşteri tercihlerini değiştirdiğinde öneriler yeni girdilerle yeniden üretilebilir.
- **AC-02.6:** Sonuç bulunamadığında veya API hata verdiğinde durum açıkça gösterilir; tercih/konum değiştirme veya yeniden deneme yolu sunulur.
- **AC-02.7:** Telefonla aranabilirlik öneri uygunluğundan ayrı gösterilir. Doğrulanmış telefon bilgisi olmayan restoran için rezervasyon araması başlatılmaz.

### FR-03 — Rezervasyon koşullarını toplama

**Gereksinim:** Sistem seçilen restoran için müşterinin talep ettiği rezervasyonu açıkça tanımlamalıdır.

- **AC-03.1:** Tarih, restoranın yerel saatine göre saat, kişi sayısı ve rezervasyon adı alınır.
- **AC-03.2:** Gerekli iletişim bilgileri ve özel istekler belirtilebilir. Gereksiz alanlar zorunlu tutulmaz.
- **AC-03.3:** Saatin restoranın yerel saat diliminde olduğu özet ekranında açıkça belirtilir.
- **AC-03.4:** Müşteri kabul edeceği alternatifleri belirtebilir; örneğin saat aralığı veya farklı oturma alanı.
- **AC-03.5:** Aramadan önce restoran, tarih, saat, kişi sayısı ve özel isteklerin özeti gösterilir. Müşteri bu özet üzerinden girişimi başlatır.
- **AC-03.6:** Eksik veya geçersiz zorunlu bilgi varsa arama başlamaz; düzeltilecek alan belirtilir.

### FR-04 — Restoranı telefonla arama

**Gereksinim:** Sesli agent seçilen restoranın telefonunu arayarak müşterinin koşullarında rezervasyon istemelidir.

- **AC-04.1:** Arama, seçilen restoranla eşleştiği doğrulanmış telefon numarasına yapılır. Numara kaynağı uygulama tarafında izlenebilir.
- **AC-04.2:** Agent rezervasyon isteyen kişinin yapay zekâ destekli dijital asistanı olduğunu ve kendisi adına aradığını görüşmenin başında anlaşılır biçimde belirtir; insan gibi kimlik sunmaz. Tanıtım kesilirse tamamlanmış sayılmaz ve sonraki yanıtta tekrarlanır. Restoranla desteklenen görüşme dilinde konuşur.
- **AC-04.3:** Agent tarih, saat, kişi sayısı, rezervasyon adı ve ilgili özel istekleri karşı tarafa iletir.
- **AC-04.4:** Agent restoranın yanıtlarına göre konuşmayı sürdürür ve gerekli rezervasyon sorularına mevcut müşteri bilgileriyle yanıt verir.
- **AC-04.5:** Agent yalnızca müşterinin önceden kabul ettiği alternatifler içinde karar verebilir. Bu sınırın dışındaki değişiklikte müşteriden yeni karar alınmadan rezervasyon tamamlanmaz.
- **AC-04.6:** Restoran özel bir isteği karşılayamıyorsa bu durum müşteriye aktarılır; istek sessizce yerine getirilmiş sayılmaz.
- **AC-04.7:** Yanıt yok, meşgul, görüşme kesildi ve rezervasyon reddedildi durumları başarılı rezervasyondan ayrı işlenir.

### FR-05 — Görüşmeyi müşteriye canlı dinletme

**Gereksinim:** Müşteri rezervasyon görüşmesini gerçekleşirken uygulamadan dinleyebilmelidir.

- **AC-05.1:** Arama sürerken müşteri hem agentın hem restoran tarafının sesini canlı takip edebilir.
- **AC-05.2:** Arama durumu ekranda gösterilir: aranıyor, bağlı, görüşme sürüyor veya sona erdi.
- **AC-05.3:** Canlı ses bağlantısı koparsa müşteriye bildirilir; sessizlik normal görüşme akışı olarak gösterilmez.
- **AC-05.4:** Özelliğin kabul testinde sonradan oynatılan kayıt canlı yayın yerine kullanılamaz.

### FR-06 — Canlı altyazı ve çeviri

**Gereksinim:** Görüşme müşterinin ana dili dışında yürütülüyorsa içerik müşterinin ana dilinde canlı altyazı olarak sunulmalıdır.

- **AC-06.1:** Müşterinin ana dili ile görüşme dili ayrı bilgiler olarak tutulur. Farklı olduklarında çeviri altyazısı devreye girer.
- **AC-06.2:** Hem agentın hem restoranın sözleri konuşma tanıma/çeviri akışına dahil edilir.
- **AC-06.3:** Altyazıda konuşmacılar ayırt edilir; müşteri hangi sözün kime ait olduğunu anlayabilir.
- **AC-06.4:** Altyazı görüşme devam ederken parça parça güncellenir; yalnızca görüşme sonunda verilen metin yeterli değildir.
- **AC-06.5:** Tarih, saat ve kişi sayısı gibi rezervasyon ayrıntıları çeviride korunur. Belirsiz/anlaşılamayan ifade kesin bilgi olarak yazılmaz.
- **AC-06.6:** Çeviri veya konuşma tanıma bağlantısı kesilirse altyazının kesildiği açıkça gösterilir.

### FR-07 — TTS ile agent sesi

**Gereksinim:** Agentın telefon görüşmesindeki konuşması ElevenLabs veya eşdeğer bir TTS servisiyle üretilmelidir.

- **AC-07.1:** Agentın ürettiği metin TTS üzerinden sese çevrilerek telefon görüşmesine aktarılır.
- **AC-07.2:** Seçilen servis görüşme dilini destekler; desteklenmeyen dilde arama başlamadan müşteriye bilgi verilir.
- **AC-07.3:** TTS veya telefon bağlantısı hatasında sistem rezervasyonu tamamlanmış olarak işaretlemez.
- **AC-07.4:** Kabul testinde karşı tarafın beklenmedik yanıtına uygun yeni agent konuşması üretilebilir; yalnızca sabit bir ses kaydıyla akış taklit edilmez.

### FR-08 — Rezervasyon sonucunu doğrulama

**Gereksinim:** Sistem görüşme sonunda rezervasyonun gerçek durumunu ve ayrıntılarını müşteriye göstermelidir.

- **AC-08.1:** “Onaylandı” durumu yalnızca restoranın rezervasyonu açıkça kabul ettiği durumda kullanılır.
- **AC-08.2:** Onaylanan rezervasyonda restoran adı, yerel tarih/saat, kişi sayısı, rezervasyon adı ve kabul edilen özel istekler gösterilir.
- **AC-08.3:** Restoran bir rezervasyon numarası verirse sonuçta gösterilir; vermediyse numara üretilmez.
- **AC-08.4:** Onay yoksa sonuç “başarısız” veya “belirsiz” olarak gerekçesiyle gösterilir. Telefonun açılmış olması onay sayılmaz.
- **AC-08.5:** Yeniden deneme öncesinde önceki girişimin sonucu gösterilir. Belirsiz sonuçta olası mevcut rezervasyon kontrol edilmeden otomatik ikinci rezervasyon yapılmaz.

### FR-13 — Rezervasyon görüşmesinin özeti (D-017, 21 Ekim 2026)

**Gereksinim:** Görüşme sonrasında kullanıcıya ana dilinde, konuşmaya dayanan kısa bir özet gösterilir.

- **AC-13.1:** Özet; talebi, restoran yanıtını, üzerinde anlaşılan veya reddedilen koşulları, özel istekleri ve açık kalan noktaları içerir. Referans gibi veriler uydurulmaz.
- **AC-13.2:** Doğrulanmış rezervasyon durumu özetten ayrı gösterilir. LLM özeti onay kanıtı yerine geçmez; kesinti/eksik transcript varsa belirsizlik görünürdür.
- **AC-13.3:** Tarih, yerel saat/saat dilimi, kişi sayısı ve rezervasyon adı konuşma kanıtı ve sonuç kaydıyla tutarlılık kontrolünden geçer; desteklenmeyen bilgi kesin ifade edilmez.
- **AC-13.4:** Özet hazırlanıyor, hazır, eksik veri ve hata durumları gösterilir. Özet hatasında mevcut rezervasyon sonucu korunur; yeniden özetleme telefon araması başlatmaz.
- **AC-13.5:** Özet rezervasyona bağlanır; yetkili kullanıcı sonradan açabilir. Saklama/silme politikası ayrıca belirlenir; bu gereksinim kalıcı ses kaydı izni değildir.

FR-13 kullanıcı kapsamına eklendi; henüz uygulanmadı. Önceki FR-01–FR-12 kabul kapsamına bu bölüm de dahildir.

## 4. Uçtan uca kabul senaryoları

| Senaryo | Beklenen sonuç |
| --- | --- |
| Müşteri tercih girer, restoran seçer, talep kabul edilir | Gerçek Qloo önerisi → telefon görüşmesi → canlı dinleme → doğrulanmış rezervasyon özeti |
| Türkçe ana dilli müşteri için İngilizce görüşme | Her iki konuşmacı canlı duyulur; konuşma Türkçe altyazıyla görüşme sırasında takip edilir |
| İstenen saat dolu; önceden kabul edilmiş alternatif var | Agent izin verilen alternatifi değerlendirir; kabul edilen son saat özette gösterilir |
| Restoran izin verilen kapsam dışında alternatif sunar | Müşteriden karar alınmadan değişmiş koşullarda rezervasyon tamamlanmaz |
| Restoran telefonu açmaz | Başarılı rezervasyon gösterilmez; arama sonucu ve yeniden deneme seçeneği sunulur |
| Telefon bilgisi yok | Öneri görüntülenebilir; arama başlatılamaz ve nedeni açıklanır |
| Restoranın son onayı duyulmadan görüşme kesilir | Rezervasyon belirsiz işaretlenir; otomatik ikinci rezervasyon yapılmaz |
| Canlı dinleme veya altyazı bağlantısı kesilir | İlgili kesinti müşteriye görünür; özellik çalışıyormuş gibi gösterilmez |

## 5. Teknik sorumluluk ayrımı

- **Qloo:** Tercih girdilerinden restoran adayları ve ilişkili içgörü üretmek.
- **Uygulama/agent:** Profil, restoran seçimi, rezervasyon koşulları, konuşma akışı ve sonuç durumunu yönetmek.
- **Telefon servisi:** Restoranın numarasını aramak ve çift yönlü görüşme sesini taşımak.
- **TTS:** Agentın sesini üretmek. Tek başına telefon araması veya rezervasyon yönetimi sağlaması varsayılmaz.
- **Konuşma tanıma ve çeviri:** Görüşme sesini metne ve müşterinin ana diline dönüştürmek.
- **Canlı yayın katmanı:** Görüşme sesini ve altyazıları müşterinin uygulamasına aktarmak.
- **İşletme verisi kaynağı:** Qloo yanıtında bulunmuyorsa doğrulanmış restoran telefonu gibi gerekli bilgileri tamamlamak.

Bu ayrım mimari taslaktır; servis sağlayıcıları henüz seçilmedi.

## 6. Uygulama öncesi netleştirilecek kararlar

Aşağıdaki noktalar kullanıcı tarafından henüz belirlenmedi; kesinleşmiş gereksinim olarak yorumlanmamalıdır.

- İlk sürümün hedef ülke/şehirleri, müşteri ana dilleri ve görüşme dilleri.
- Canlı ses ve altyazı için kabul edilebilir gecikme eşikleri; sayısal eşikler belirlenmeden performans kabulü tamamlanmış sayılmaz.
- Müşterinin görüşme sırasında müdahale etme, yeni alternatif onaylama veya aramayı durdurma yöntemi.
- Telefon numarası veri kaynağı ve hedef ülkelerdeki telefon servisinin kullanılabilirliği.
- Arama süresi, yeniden deneme sayısı ve maliyet sınırları.
- Görüşme kaydı tutulup tutulmayacağı; canlı dinleme ile kalıcı kayıt ayrı kararlardır.
- Restoran tarafına otomatik agent ve canlı dinleyici bilgisinin nasıl verileceği; hedef ülkedeki telefon, veri ve bilgilendirme koşullarının uygulamaya etkisi.
- Ödeme/depozito veya kart garantisi isteyen restoranların nasıl ele alınacağı; bu belge ödeme yetkisi tanımlamaz.

## 7. Tamamlanma tanımı

Fonksiyonel kabul için FR-01–FR-08 kriterleri, seçilen ülke/dil kapsamındaki uçtan uca senaryolarda gösterilmelidir. Teknik denemelerde kontrollü bir karşı taraf kullanılabilir; bu durum gerçek restoran rezervasyonu diye sunulmaz. Gerçek restoranla rezervasyon başarısı iddiası yalnızca gerçek ve doğrulanmış sonuçla yapılır.

Ürünün teslim edilebilir sayılması için açık kararlar arasındaki hedef kapsam ve performans eşikleri kesinleştirilmeli, seçilen servislerle ana akış doğrulanmalı ve hackathon teslim koşulları ayrıca tamamlanmalıdır.


## 8. D-008 — Rota kapsamı ek gereksinimleri (21 Ekim 2026)

### FR-09 — Çok kategorili kişisel keşif
- AC-09.1: Restoran, kafe, bar, otel ve gezilecek yer adayları Qloo ile bulunur; her kategorinin gerçek veri kapsamı ayrıca doğrulanır.
- AC-09.2: Her durakta kimlik, mevcut konum/adres, veri dayanağı ve “Konumda gör” bulunur; eksik alan üretilmez. Yanlış ana kategori ayıklanır.
- AC-09.3: Kullanıcı tarih, süre, tempo, ulaşım, bütçe ve tercihlerini düzenleyebilir; doğrulanmamış varsayımlar görünür olur. Otel önerisi ile mevcut konaklama noktası ayrılır.

### FR-10 — Çok günlük düzenlenebilir rota
- AC-10.1: İstenen günler yerel tarihlere ayrılır; konum, ziyaret süresi, ulaşım ve açılış bilgisi kullanılarak uygulanabilirlik kontrol edilir. Bilinmeyen süre/saatler açık gösterilir.
- AC-10.2: Sabit rezervasyonlar ve bilinen ziyaret/geçiş süreleri çakışmaz; doğrulanmış kapalı saatlere ziyaret planlanmaz.
- AC-10.3: Kullanıcı durak değiştirir, çıkarır veya sabitler; ilgili geçiş/saatler yeniden hesaplanır. Onaylı rezervasyonlar sessizce taşınmaz veya iptal edilmez.
- AC-10.4: Harita ve günlük çizelge aynı rota sürümünü gösterir; mobilde aynı içerik ve kontroller korunur. Rota oluşturma hatası kullanıcının girdilerini silmez.

### FR-11 — Durak bazlı rezervasyon
- AC-11.1: Rezervasyon gerekliliği ve işlem kanalının desteklenmesi ayrı gösterilir; telefon bulunması rezervasyon gerekliliğinin kanıtı değildir.
- AC-11.2: Kullanıcı her girişimin işletme, tarih, saat, kişi/oda/bilet, varsa ücret ve koşullarını gözden geçirip başlatır. Rota oluşturma toplu rezervasyon yetkisi vermez.
- AC-11.3: Restoran telefon rezervasyonu FR-03–FR-08 üzerinden canlı ses/altyazıyla çalışır. Otel ve gezilecek yer rezervasyonu uygun kanal entegrasyonu ve kategoriye özel doğrulama gerektirir; entegrasyon yoksa desteklenmiyor bilgisi ve mevcut resmi bağlantı gösterilir.
- AC-11.4: Her durağın onaylı/başarısız/belirsiz durumu ayrı korunur; rota hazır olması rezervasyonların tamamlandığı anlamına gelmez. Belirsiz sonuç tekrar öncesi sorgulanır.
- AC-11.5: Bir rezervasyon saati rotayla çakışırsa kullanıcıya düzenleme önerilir; mevcut rezervasyon yeni onay olmadan değiştirilmez. Bu kapsam ödeme veya depozito harcama yetkisi tanımlamaz.

Genişletilmiş ürün kabulü FR-01–FR-11 ve seçilecek kategori/şehir rezervasyon kanalları üzerinden değerlendirilecek. Bölüm 7’deki FR-01–FR-08 kabulü restoran rezervasyon alt akışını ifade eder. Bu ek kapsamında canlı rota veya yeni kategori doğrulaması henüz yapılmadı.


## 9. D-009 — Seyahat anlarına bağlı kültürel içerikler

### FR-12 — Kitap, film, podcast ve müzik önerileri
- AC-12.1: Rota durağı veya yolculuk/mola anıyla ilişkili, kullanıcı zevklerine göre kitap, film, podcast ve müzik listesi önerileri sunulur. Qloo destekli türler gerçek entity kimlikleriyle eşlenir.
- AC-12.2: Başlık, yazar/sanatçı ve öneri gerekçesi mevcut veriye dayanır; kapak, süre, dil ve platform erişimi eksikse uydurulmaz. Podcast ile bölüm ve sanatçı ile parça/playlist ayrı modellenir.
- AC-12.3: Kullanıcı içerik ekler, değiştirir veya önerileri kapatır; fiziksel rota ve rezervasyonlar etkilenmez. Otomatik oynatma yapılmaz.
- AC-12.4: Müzik listesi için parça/playlist kaynağı ayrıca belirlenir; Qloo sanatçı önerisi hazır çalınabilir liste olarak sunulmaz. Sağlayıcıda açma yalnız gerçek bağlantıyla mümkündür.
- AC-12.5: Platform oynatma/indirme/erişim yeteneği doğrulanmadan içeride oynatım veya çevrimdışı kullanım vaat edilmez; içerik hatası ana rota akışını engellemez.

Kart/rota tasarımı için kullanıcı tarafından önerilen referans proje D:/LLM/THY Travel Agent. Kaynak incelemesi ve uyarlama önerileri docs/ux/07-thy-components-and-content.md içinde. Referansı kullanma izni tüm renk, marka, auth veya backend kodunu birebir aktarma kararı değildir. FR-12 kullanıcı kapsam ekidir; henüz uygulama veya canlı kategori testi değildir. Ürün kabulüne FR-12 de dahildir.


## 10. D-010–D-012 — İlk kodlama kararları
- Login keşifte istenmez; rota kaydetme ve rezervasyon girişimi gibi işlem anında gerekir. Anonim cihaz cookie’si kişisel oturum yerine geçmez; kullanıcı giriş yapınca kayıtlı rotalar hesaba ait olmalı.
- Cookie ile ziyaretçi tanınır; ilk uygulamada cookie yalnız anonim kimlik, tercih/taslak verisi sunucuda tutulur. Temizleme eylemi bulunmalı.
- THY Travel Agent uçuş servisi referans alınır; Travelpayouts/Aviasales fiyatları önbellek, tarih/tek yön/gidiş-dönüş doğrulamasıyla sunulur.
- Bekleme/mola önerileri kullanıcı tetiklemesiyle alınır; otomatik sorgu veya oynatma yok.
- Rotalar hesapta kaydedilebilir; doğal dille düzenleme kayıtlı kopyayı açık kaydetme olmadan değiştirmez. Model mekan kimliği veya rezervasyon onayı uyduramaz; belirsiz talimatta açıklama ister, çakışmada mevcut taslak korunur.
- LLM sağlayıcısı kullanıcı seçimi DeepSeek, OpenAI uyumlu API; hedef ortam Coolify/Hetzner CAX21 ARM64. Sağlayıcı anahtarları sunucu runtime environment içindedir.

İlk uygulanan davranış ve kalan ürün kabul işleri docs/IMPLEMENTATION_STATUS.md içinde kayıtlıdır. Bu ek FR-01–FR-12 tamamlandı anlamına gelmez.

### AC-12.6 — Öneri öncesi türe özel zevk
Kitap/film önerisinden önce sevilen eserlerin Qloo aramasıyla seçilebildiği, atlanabilir tercih adımı sunulur. Aynı adım desteklenen diğer içerik türlerine uyarlanır. Kitap ve film seçimleri ayrı hatırlanır; atlama varsa önerinin seyahat/genel tercih bağlamına dayandığı açıklanır.

### AC-12.7 — Podcast konu anahtar kelimeleri (D-013)
Podcast örneği zorunlu değildir; serbest konu metni LLM ile normalize edilip mevcut Qloo tag ID’lerine eşlenir ve seçime sunulur. Bulunmayan tag üretilmez. Anahtar kelime dili ile podcast yayın dili ayrılır; tüm diller veya belirli yayın dili garanti edilmez. Kitap/film eser adımı korunur.

### AC-12.8 — Kitap ve podcast dil seçimi (D-014)
Kitap ve podcast için bağımsız içerik dili seçilir ve hatırlanır. Kitapta Qloo kayıt dili, podcast’te iTunes/RSS yayıncı dil metadata’sı kullanılır. Dil kaynağı gösterilir; bilinmeyenler seçilen dile dahil edilmez, yetersiz sonuçta koşul sessizce kaldırılmaz. Dil fark etmez seçeneği açık kullanıcı kontrolüdür. Kitabın farklı çeviri/baskıları ve podcast bölümlerinin tümünün aynı dilde olması garanti edilmez. Film için bu özellik uygulanmış sayılmaz.

### AC-12.9 — Kitap konusu ve podcast erişimi (D-015)
Kitap önerisi konu/keyword veya sevilen eser üzerinden kişiselleştirilebilir; kitap tag ve entity sinyalleri karıştırılmaz. Podcast kartı doğrulanmış Apple Lookup bağlantısını “Apple Podcasts’te aç” ile sunar; dil filtresi olmasa da erişim yolu alınır. Bağlantı yoksa uydurulmaz; RSS dil hatası mevcut Apple sayfasını gizlemez.

### D-016 — Telefon görüşmesi dil politikası
Görüşme dili restoranın ülkesine göre varsayılan seçilir; altyazı kullanıcının açıkça belirttiği native diline göre sunulur. Ülke, işletmenin konuştuğu dilin kesin kanıtı değildir: çok dilli/bilinmeyen ülke ve desteklenmeyen dil için görünür düzeltme/geri dönüş gerekir. UI dili, ana dil ve görüşme dili ayrı tutulur. Entegrasyon taslağı docs/RESERVATION_CALL_IMPLEMENTATION_PLAN.md; sağlayıcı seçimi veya çalışan arama değildir.

## 11. D-029 — Onboarding ve ortak kullanıcı tercih profili

### FR-14 — Kalıcı, düzenlenebilir tercih verisi

Kullanıcı onboarding ile zevklerini tanımlar; bu kayıt bütün öneri yollarında ortak kaynak olarak kullanılır. Ayrıntılı UX ve teknik model önerisi docs/ux/08-onboarding-and-taste-profile.md içindedir; bu gereksinim uygulanmış özellik değildir.

- AC-14.1: Kalıcı zevk profili; seyahat hedef/tarih/kişi ve tek seferlik isteklerden ayrılır. Kullanıcı Tercihlerim üzerinden gözden geçirir, değiştirir ve sıfırlar.
- AC-14.2: Yer/eser/konu seçimleri gerçek Qloo entity veya tag kimliklerine eşlenir; belirsiz eşleşme kullanıcıya seçtirilir, eşleşmeyen metin gerçek sinyal olarak gönderilmez.
- AC-14.3: Her öneri isteği ortak profilin güncel sürümünü çözer ve ilgili kategori alt kümesini kullanır. Tercihler ile zorunlu koşullar ayrılır; sonuç bulunamadığında koşullar sessizce gevşetilmez.
- AC-14.4: Misafir başlangıcı ve işlem anında giriş korunur. Hatırlama kapsamı görünürdür; profil sunucuda, tanıma kimliği cookie üzerinde tutulur. Hesaba aktarım ve mevcut profille çakışmalar açık kullanıcı incelemesiyle çözülür; hesaplar karışmaz.
- AC-14.5: Ana dil, arayüz dili, içerik dilleri ve görüşme dili ayrıdır. Kitap/podcast/film/müzik tercihleri ilgili alanda tekrar kullanılabilir; doğrulanmamış dil/playlist yeteneği vaat edilmez.
- AC-14.6: Bir rota düzenleme komutu veya kart seçimi master profili kendiliğinden değiştirmez. Tek seferlik ve kalıcı değişiklik kullanıcıya ayrıştırılır; profil değişikliği gerçek rezervasyonu değiştirme yetkisi değildir.
- AC-14.7: Eksik/atlanmış profil öneri akışını kilitlemez. Eşleştirme veya kayıt hatasında girdiler korunur; kayıt onayı olmadan başarı gösterilmez. Önbellek profil sürümüyle geçersizleşir.


## 12. D-031 / H-069 — Restoran rezervasyonu ilk uygulama kaydı
22 Ekim 2026: Rota kartından giriş/rezervasyon formu, onaylı immutable özet ve arama kuyruğu; ayrı worker/gateway ile Anna telefon görüşmesi, yetkili canlı ses, native altyazı/özet ve kanıtlı sonuç yolu eklendi. Otomatik kabul dar TR/EN readback+restoran kanıt kuralıyla; belirsiz/diğer ifadelerde kullanıcı incelemesiyle. Telefonun tamamlanması veya LLM özeti confirmed sayılmaz. Onaylı durak rota düzenlemesinde korunur. Güncel gerçek kapsam docs/RESERVATION_IMPLEMENTATION.md.

Bu kayıt bütün FR-03–FR-08/FR-11/FR-13 kabulü değildir: canlı alternatif teklif/yeni karar, diğer rezervasyon kanalları, gerçek restoran telefon uçtan uca testi ve üretim yayını henüz yok. Önceki geniş ürün hedefleri korunur. Kullanıcıya otomatik test araması veya rezervasyon oluşturulmadı.


## 13. D-032 — Sohbet merkezli seyahat asistanı (26 Ekim 2026)
### FR-15 — Konuşarak tanışma, profil kaydı ve planlama
- AC-15.1: Kullanıcı serbest sohbetle başlar; tanışmayı atlayıp doğrudan seyahat planlayabilir. Ana onboarding üç adımlı form değildir.
- AC-15.2: DeepSeek açık genel tercihleri yapılandırır; sunucu şema/kaynak/sürüm doğrulamasıyla kullanıcı veya ziyaretçi profiline kaydeder. Başarı yalnız DB commit sonrasında görünür. Kullanıcı inceleyip düzeltir veya sıfırlar.
- AC-15.3: Tek seyahat istekleri master profilden ayrıdır. Qloo kimliği yalnız gerçek katalogdan seçilir. Belirsizlikte soru sorulur; model keyfi işlem veya telefon başlatamaz.
- AC-15.4: Sohbet yenilemede geri gelir; sahip değişimi hesapları karıştırmaz. Hata giriş metnini korur; tekrar gönderim tekilleştirilir; çakışma görünürdür.
- AC-15.5: Sohbet rota üretme ve düzenleme aksiyonlarını mevcut API'lere bağlar. Fotoğraflı/haritalı kartlar, açık Öneri al, kaydetme ve rezervasyonun açık onay kapısı korunur.
Ayrıntılı kapsam ve doğrulama: docs/ux/09-chat-first-journey.md ve H-070. DeepSeek anlamsal çıkarımı bütün cümlelerde garanti edilmez; uçuş/rezervasyon ayrıntı yüzeyleri yardımcı formlarla çalışır.


## 14. D-033 — Bütün işlemler konuşma içinde
- AC-15.6: Ana deneyim tek kaydırılan konuşma ve sürekli mesaj alanıdır; ayrı rota/tercih/uçuş/rezervasyon sayfası veya modal zorunlu değildir.
- AC-15.7: Uçuş kalkış/varış/tarih ve rezervasyon ad/tarih/saat/kişi/not bilgileri konuşmadan yapılandırılmış taslağa çevrilir. Belirsiz katalog eşleşmesi kullanıcıya aynı konuşmada seçtirilir.
- AC-15.8: Profil inceleme/düzeltme, listeleme, kayıt, içerik önerisi, aktarım ve canlı görüşme takip kontrolleri konuşma içi kartlardır. Kitap konusu/sevilen eser ve podcast dil seçenekleri korunur.
- AC-15.9: Kimlik bilgileri yalnız güvenli kartla auth API'sine gider; LLM sohbetine eklenmez. Kaynak/yerel saat kontrolü ve ayrı ücretli arama onayı modelce verilemez.
Güncel sözleşme: docs/ux/10-complete-conversation.md. Önceki yardımcı form sınırı H-070 tarihsel kaydıdır.


### 28 Ekim 2026 — D-035: Karşılama ve sohbet dili
İlk ekran ve karşılama İngilizcedir. Asistan son kullanıcı mesajının dilinde yanıt verir; açık dil değişikliği isteği önceliklidir. Belirsiz kısa mesajlarda önceki konuşma dili, ilk temasta İngilizce kullanılır. Mesaj dili native/altyazı tercihini otomatik değiştirmez. Eski konuşmalar yeniden çevrilmez. Yardımcı işlem kartlarının tam yerelleştirmesi ayrıca ele alınacaktır.
