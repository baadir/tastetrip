# Kişisel rota ve rezervasyon akışı

21 Ekim 2026 · D-008 kapsamı kullanıcı talimatıdır; aşağıdaki arayüz ve teknik teslim önerileri henüz onaylanmadı. Product-design-and-ux yaklaşımı kullanıldı. Araştırma veya uygulanmış özellik iddiası yoktur.

## Kapsam ve kanıt sınırı

Restoran, kafe, bar, otel ve gezilecek özel yerler aynı seyahat planında yer alır. “Özel” için müze, galeri, park, manzara noktası veya mimari mekân örnekleri adaydır; kesin kategori listesi ve Paris kapsaması canlı katalog deneyiyle belirlenecek. Önceki restoran deneyleri tüm kategorilerin kalitesini doğrulamaz.

Qloo yer adaylarını ve zevk ilişkilerini sağlar. Resmi kaynak: https://github.com/qloo/docs-public/blob/main/reference/insights-api-deep-dive.md . Qloo önerisini uygulanabilir günlük programa dönüştürmek uygulamanın sorumluluğudur. Harita/ulaşım süreleri için sağlayıcı seçilmedi; yürüyüş, toplu taşıma veya araç süreleri uydurulmaz. Oda/bilet/masa müsaitliği ayrıca doğrulanır.

## Önerilen deneyim

1. Kullanıcı “Paris’e şu tarihte gidiyorum, iki günlük rota oluştur” der. Tarih belirsizse netleştirilir. Gün sayısı ile gece sayısı eşit varsayılmaz.
2. Kısa düzenlenebilir özet: tarih, günlük başlangıç/bitiş aralığı, kişi sayısı, bütçe, ilgi alanları, tempo, ulaşım biçimi. Otel belliyse başlangıç noktası; değilse otel önerisi isteğe bağlı. Eksik tercihler varsayım olarak görünür ve değiştirilebilir.
3. Qloo adayları kategori/kimlik kontrolünden geçer; günlere ve bölgelere dağıtılır. Süre, saatler ve geçiş bilgisi doğrulandıkça zaman çizelgesi oluşturulur. Bilinmeyenler işaretlenir; kesin uygun rota iddiası yapılmaz.
4. Desktop: günlük zaman çizelgesi yanında gerçek harita. Mobil: gün seçimi ve dikey durak akışı; harita ayrı görünüm. İki görünüm aynı plan/seçim durumunu paylaşır. Bu düzen öneridir, yeni görsel henüz üretilmedi.
5. Durakta gerçek fotoğraf/konum, tercih gerekçesi, ziyaret süresi tahmini etiketi, varsa açılış bilgisi ve “Konumda gör”. “Değiştir” benzer kategoride alternatifler sunar; “Bu durağı sabitle” sonraki düzenlemelerde korur.
6. Rezervasyon uygunluğu bilinen durakta “Rezervasyon planla”. Gereklilik, önerilir, gerekmez veya bilinmiyor ayrı durumlar; yalnız telefon numarası var diye “rezervasyon gerekir” denmez.
7. Kullanıcı rezervasyon özetini başlatır. Restoran telefon akışındaki canlı dinleme/çeviri korunur. Otel/bilet için tarih, ücret/iptal/depozito ve işlem kanalı ayrıca belirlenmeli. Entegrasyon yoksa desteklenmediği açık ve resmi site alternatifi görünür olur; işlem tamamlandı denmez.
8. Başarılı rezervasyon planın sabit saatli durağı olur. Çakışma varsa alternatif plan sunulur; mevcut rezervasyon otomatik iptal edilmez. Bir durak başarısızsa diğerlerinin başarısı korunur.

## Durumlar ve geri dönüş

Taslak → oluşturuluyor → kısmi/tam rota → düzenlenmiş rota. Rezervasyon her durakta ayrı: planlanmadı / inceleme / başlatıldı / onaylı / başarısız / belirsiz. “Rota hazır” bütün rezervasyonlar onaylandı anlamına gelmez. Bağlantı kopunca plan korunur, işlem kimliğiyle rezervasyon durumu sorgulanmadan yeniden rezervasyon denenmez. Yeni rota sürümü onaylı rezervasyonlara bağlı kalır; değişiklik, iptal veya ödeme için yeni kullanıcı kararı gerekir.

## Kabul ve doğrulama kapısı

- İki günlük istek iki yerel tarih/gün altında duraklar üretmeli; bilinen ziyaret/ulaşım süreleri ve sabit rezervasyonlar çakışmamalı.
- Kapalı olduğu doğrulanan durak ilgili saate yerleştirilmemeli; saat verisi eksikse teyit gerekir gösterilmeli. Özel gün kapanışları ayrıca doğrulanmalı.
- Durağı değiştirmek yalnız etkilenen geçiş ve saatleri yeniden hesaplamalı; sabitlenen ve onaylı rezervasyonları sessizce taşımamalı.
- Desteklenmeyen rezervasyonlar ve kısmi sonuçlar görünür olmalı; rota kabulü toplu rezervasyon izni sayılmamalı.
- Harita ve çizelge seçimi aynı durağa odaklanmalı; dar alanda içerik sırası ve eylemler korunmalı; hareket azaltma ve klavye kullanımı desteklenmeli.
- Paris kategori örnekleri, gerçek yol süreleri, tarihli açılışlar ve rezervasyon uçtan uca testi henüz yapılmadı. Sonraki teknik deney bunları ölçmeli.

Ürün sahibi ilk sürümün şehir/kategori ve işlem kapsamını seçecek; mühendislik öncesinde rota veri sağlayıcısı, rezervasyon kanalları, maliyet ve iptal/ödeme sınırları netleşecek. İlk teslim için tüm kategori önerileri + restoran telefon rezervasyonu ile başlamak bir MVP önerisidir; kabul edilmiş daraltma değildir.
