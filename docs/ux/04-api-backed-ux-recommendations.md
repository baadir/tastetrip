# Canlı Qloo deneylerinden UX önerileri

Tarih: 21 Ekim 2026. Durum: **kanıta dayanan tasarım önerileri; kullanıcı tarafından henüz onaylanmış kararlar değil**. Bu belgede yalnız Qloo deneyleri yapıldı; telefon, auth, TTS veya LLM entegrasyonu yapılmadı.

## 1. Deney kapsamı ve kanıt

Bu turda 52 salt okunur çağrı: 9 etiket araması, 19 sorguluk ilk matris, 7 kategori/sinyal deneyi, 9 takip deneyi, 5 tekrarlanabilirlik kontrolü ve 3 ek arama/bütçe/geçersiz şehir kontrolü. 51 çağrı HTTP 200, özellikle geçersiz şehirle yapılan negatif kontrol HTTP 400 döndürdü. Bu sayılar önceki turdaki 6 çağrıyı içermez.

İstanbul, Roma ve Mumbai; sorgu başına en fazla 10 sonuç. Tam katalog, nüfus temsili örneklem, veri güncelliği testi, memnuniyet araştırması veya üretim performans testi değil. Sonuçlar sayfa sınırına ulaştığından şehir toplam restoran sayıları çıkarılamaz.

Kaynak özetleri:

- `../validation/qloo-ux-matrix-2026-10-21.json`
- `../validation/qloo-ux-followup-2026-10-21.json`
- `../validation/qloo-ux-final-2026-10-21.json`
- `../validation/qloo-ux-repeatability-2026-10-21.json`
- Tekrarlanabilir araç: `../../scripts/qloo_ux_probe.py`; anahtar yalnız process environment içinden alınır.

JSON dosyaları anahtarsız, restoran kayıtlarını içermeyen sayım/karşılaştırma özetleridir. İlk çıktıdaki `primary_genre` nesnesi gereğinden geniş olduğundan yalnız kategori adı/sayısına küçültüldü. Matrisin konsol yazdırmasındaki Windows encoding hatası sorgulardan ve dosya yazımından sonraydı; düzeltildi. API çağrılarının başarısızlığı olarak sayılmadı.

## 2. Hangi girişleri gerçekten sunabiliriz?

| Kullanıcı dili | Teknik eşleme | Canlı deney | Önerilen UX davranışı |
| --- | --- | --- | --- |
| Gideceğim yer | `filter.location.query` | Istanbul/Rome/Mumbai sonuç verdi; uydurma şehir 400 | Şehir/bölge seçiminde ülkeyi netleştir; bulunamayan yeri yerinde düzelt; bütün planı sıfırlama |
| İtalyan mutfağı | `urn:tag:genre:place:restaurant:italian` | Üç şehirde kesişim filtresiyle 10'ar sonuç; istenen etiket 10/10 mevcut | Çoklu seçilebilir mutfak seçeneği; birden çok mutfakta OR mantığı ürün önerisi, bu tur ayrıca test edilmedi |
| Japon mutfağı | `urn:tag:genre:place:restaurant:japanese` | Roma'da 10 sonuç; etiket 10/10 | İlk desteklenen mutfaklardan biri olabilir |
| Türk mutfağı | `urn:tag:genre:place:restaurant:turkish` | Etiket aramasında var; bu tur Insights deneyi yapılmadı | Katalog adayı; her şehirde çalışıyor gibi sunma |
| Sakin bir ortam | `urn:tag:ambience:qloo:quiet` | Üç şehirde hard filtreyle 10'ar sonuç; etiket 10/10. Roma'da soft sinyal de sıralamayı değiştirdi | Varsayılan “tercihim”; istenirse “olmazsa olmaz” |
| Romantik bir ortam | `urn:tag:ambience:qloo:romantic` | Üç şehirde 10'ar sonuç ve etiket 10/10 | Atmosfer tercihi; kullanıcının rezervasyon özel isteğiyle aynı alan değil |
| Açık havada oturma | `urn:tag:service_options:place:outdoor_seating` | Roma'da 10 sonuç ve etiket 10/10 | Tercih seçilebilir; masa gerçekten açık havada mı telefonda sorulur |
| Vegan seçenek olsun | `urn:tag:dietary_option:qloo:vegan` | Üç şehirde 10'ar sonuç ve etiket 10/10 | Vegan seçenek arama; tamamen vegan işletme iddiası değil |
| Vegan restoran | `urn:tag:category:place:vegan_restaurant` | Mumbai'de 10 sonuç ve etiket 10/10 | Ayrı niyet; gerçek menü/uygunluk yine teyit edilir |
| Helal seçenek | `urn:tag:dietary_option:qloo:halal` | Roma'da 10 sonuç ve etiket 10/10 | Kaynağa dayalı aday bilgisi; sertifika veya kesin uygunluk garantisi diye yazma |
| Fiyat seviyesi | `filter.price_level.max` | Roma kategori + max=2: 10 sonucun fiyat değeri de 2 | “Ekonomik / Orta / Yüksek / Çok yüksek” gibi göreli seviyeler; kişi başı kesin para tutarı üretme |
| Sevdiğim restoran | Search → seçilmiş entity ID → `signal.interests.entities` | İsim araması 5 kimlik/adresli aday döndürdü; iki farklı gerçek restoran sinyaliyle öneriler değişti | Atlanabilir autocomplete; isim+şehir/adres ile kullanıcı doğru kaydı seçsin |

Bu tablo tam evrensel tag listesi değildir. “Italian” gibi aynı isimli müzik, mutfak ve amenity etiketleri var; görünür metni ID yerine API'ye göndermeyiz.

### Tercih / zorunluluk ayrımı

- **Tercihim:** Sıralamayı etkiler; her sonucun aynı etiketi taşıması beklenmez. UI, sadece sinyal gönderildi diye her karta o özellik rozetini eklemez.
- **Olmazsa olmaz:** Desteklenen etiket kesişim filtresine dönüşür. Kullanıcı izni olmadan gevşetilmez.
- Sonuç kalmazsa “Önce sakin ortam tercihini esnetelim mi?” gibi somut bir seçenek sunulur; zorunlu beslenme koşulu sessizce kaldırılmaz.
- Kullanıcının yazdığı tüm doğal dil özelliklerinin Qloo'da karşılığı olduğu varsayılmaz. Eşleşmeyen metin düzenlenebilir özel istek olarak kalır; bir filtre uygulanmış gibi gösterilmez.

## 3. Restoran ile diğer mekânları nasıl ayıracağız?

**Bulgumuz:** Ne `urn:tag:genre:place:restaurant` ne `urn:tag:category:place:restaurant` tek başına temiz bir restoran listesi garantiliyor. Otel, alışveriş merkezi ve topluluk merkezi gibi ana kategoriler dönebildi. Hotel etiketini hariç tutunca o etiket kalktı; fakat Hotel ana kategorili bir kayıt hâlâ dönebildi. Dolayısıyla etiket yokluğu tek başına kimlik/kategori doğrulaması değil.

Önerilen başlangıç pipeline'ı:

1. Qloo'da place ve restoran kategori filtresiyle adayları al.
2. Uygulamada `properties.primary_genre.id` alanını kontrol et. Restoran ailesi ana kategorilerini varsayılan keşifte tut; otel, AVM, hostel gibi kayıtları doğrudan rezervasyon hedefi olarak gösterme.
3. Cafe, bar, fast food gibi restoran ailesinin alt türlerini akşam yemeği bağlamına göre ayrıca değerlendir. Yalnız prefix kontrolü “masa rezervasyonu alır” demek değildir.
4. Yeterli kart için sayfalama/ek aday çekme gerekir; ilk 10 ham sonuç ilk 10 uygun restoran değildir. Bu teknik henüz uygulamaya eklenmedi.
5. Bir otelin içindeki gerçek restoran ayrı bir işletme kaydıyla doğrulanabiliyorsa ileride sunulabilir; otelin genel telefonu otomatik olarak restoran telefonu sayılmaz.

### Küçük şehir örneklemi

`category:place:restaurant` sorgusunun ilk 10 sonucu ve uygulama tarafındaki örnek ana-kategori süzgeci:

| Şehir | Ham sonuç | Restoran ailesinde ana kategori | Bu alt kümede telefon | Fotoğraf | Google Place ID |
| --- | --- | --- | --- | --- | --- |
| İstanbul | 10 | 7 | 6/7 | 7/7 | 7/7 |
| Roma | 10 | 8 | 7/8 | 8/8 | 8/8 |
| Mumbai | 10 | 8 | 7/8 | 8/8 | 8/8 |

Bu, şehir kalitesi sıralaması değildir. İlk demo keşif akışını bu üç şehirden birinde deneyebiliriz. Telefonla rezervasyon için şehir/dil seçimi ayrıca gerçek işletme ve telefon servisiyle denenmeli; yalnız Qloo verisinden İngilizce konuşulacağı sonucu çıkmaz.

## 4. Restoran kartını hangi bilgilerle dolduralım?

**Ana kart:** gerçek fotoğraf, ad, mahalle/adres özeti, mevcutsa göreli fiyat seviyesi, veriye dayalı 1–2 tercih etiketi. Ana eylem: “Bu restoranı seç”. İlk görünümde uzun açıklamalar yok; ayrıntılar açılabilir.

**Detay:** mevcutsa web sitesi, saatler, açıklama, telefon ve Google Maps yolu. Başlangıçtaki 30 ham şehir örneğinde fotoğraf/adres/Place ID 30/30, telefon 27/30; menü URL'si 0/30 idi. Bu yüzden menü bağlantısı zorunlu kart öğesi olmasın. Fiyatın veya saatin bulunmadığı kartta alan gizlenmeli ya da “Bilgi yok” denmeli; uydurulmamalı.

- Place ID ile Maps bağlantısı uygulamada oluşturulur; hazır URL döndü diye yazılmaz.
- Telefon dolu olması güncelliğini veya doğru restoran şubesine ait olduğunu kanıtlamaz. Aramadan önce işletme eşleşmesi gerekir.
- Telefon yoksa keşif kartı kalabilir; rezervasyon adımında “Telefon bilgisi yok, şu an senin adına arayamıyoruz” gösterilir. Alternatif: diğer restoranlar, mevcutsa web sitesi/harita.
- Qloo'nun business rating alanı kaynağı belli olmadan “Google puanı” diye etiketlenmez.
- Saat verisi canlı masa müsaitliği değildir. Aramadan önce “Müsaitlik restoranla teyit edilecek” yazılır; gerçek zamanlı boş masa rozeti verilmez.

## 5. Kişiselleştirme için ne kadar soru soralım?

İki farklı Mumbai restoran kimliği, Roma hedefli aynı filtreli sorguya ayrı ayrı verildi. Aynı seed iki kez sorgulandığında ilk 10 aynı sıradaydı. Farklı seed ile ilk 10'da 6 kayıt ortak kaldı, 4 kayıt değişti. Bu tek ve kısa tekrar; kalıcı deterministik davranış veya kullanıcı memnuniyeti kanıtı değil.

**Öneri:** “Sevdiğin bir restoran var mı?” sorusunu kısa ve atlanabilir yapalım. Bu girdi gerçekten sonuç değiştirebiliyor. Uzun müzik/film anketi şart değil. Favori restoranı olmayan kişi mutfak ve ortam tercihleriyle devam edebilsin. Sıralama farkı tek başına daha iyi öneri anlamına gelmediğinden gelecekte kullanıcı değerlendirmesi gerekir.

## 6. Önerilen UX akışı

```text
Şehir / bölge
  → Bu akşamdan beklentin: görsel kısa seçenekler + serbest anlatım
  → Mutfak / ortam / beslenme / bütçe: gerekenleri tamamla, diğerlerini atla
  → İstersen sevdiğin restoranı seç
  → Düzenlenebilir tercih özeti
  → Az sayıda fotoğraflı restoran kartı; diğer sonuçlar isteğe bağlı
  → Restoran seçimi
  → Rezervasyon koşulları: yerel tarih/saat, kişi, isim, özel istekler
  → Gerekliyse login, sonra aynı özete dönüş
  → Açık müşteri eylemiyle telefon araması
  → Canlı dinleme + ana dilde altyazı + doğrulanmış sonuç
```

Her tercihi ayrı zorunlu sayfaya dönüştürmek yerine tek ana soruya odaklanan, atlanabilir alt seçimler öneriyorum. İkinci görsel yöndeki akışkan geçişler ve büyük görseller korunabilir. API çağrıları küçük bir örnekte 0,52–10,28 saniye sürdü; bu yüzden “anında” iddiası yerine durum metni, iptal/geri dönüş ve korunmuş girdiler gerekir. Bu üretim SLA'sı veya gerçek kullanıcı bekleme ölçümü değil.

Rezervasyon tarihi, kişi sayısı ve ana dil Qloo keşfi için zorunlu değil. Tarih/kişi ilk başta isteğe bağlı kalabilir; restoran seçildikten sonra rezervasyon için tamamlanır. Ana dil çevrilmiş altyazı için gerekir; kullanıcının tercih ettiği dil düzenlenebilir olmalı.

## 7. API'nin çözmediği açık konulara öneriler

| Açık konu | Öneri | Kanıt sınırı / çözülme koşulu |
| --- | --- | --- |
| O-001 Login | Keşif misafir erişimine açık; aramadan önce giriş; giriş sonrası özet, ayrı arama eylemi | Qloo kullanıcı hesabı gerektirmiyor; login yeri ürün önerisi. Auth prototipi/kullanıcı değerlendirmesi gerekir |
| O-002 Chatbot mı wizard mı? | Hibrit: doğal dil + görünür düzenlenebilir seçimler ve sonuç kartları | Yapılandırılmış API girdileri bu tasarımı uygulanabilir kılıyor; tek başına kullanılabilirlik kanıtı değil |
| O-003 Şehir/dil | Keşif prototipinde İstanbul/Roma/Mumbai; gerçek arama demosunda tek şehir ve tek doğrulanmış dil çifti | Üç şehirde veri var; işletmenin dili ve telefon servisi test edilmedi |
| O-004 Etiket/metadata | Yukarıdaki küçük desteklenen katalogla başla; alan eksikliklerini tasarıma dahil et | Büyük ölçüde ilk örnekler doğrulandı; tam katalog ve güncellik açık |
| O-005 Sağlayıcı/gecikme | Telefon+STT+TTS+çeviri için kontrollü uçtan uca ses deneyi | Qloo bu kararı çözmez; sağlayıcı henüz seçilmedi |
| O-006 Canlı müdahale | Dinlemeyi kapatma ile telefon görüşmesini bitirme ayrı kontroller. Onay dışı alternatifte karar kartı; yanıt yoksa anlaşılmamış koşulla rezervasyon yapma | Telefonun bekleme/iptal davranışı teknik deney gerektiriyor; çağrı bitirmek var olan rezervasyonu iptal etmek değildir |
| O-007 Kalıcılık | Keşif taslağı ve işlem durumunu ayrı tut; dönüşte mevcut arama durumunu doğrula, tekrar başlatma | Saklama süresi/kişisel veri sınırları ve gerçek backend henüz tanımlanmadı |

Bu belge önerileri doldurur; bunları kullanıcı onayı alınmış nihai karar olarak işaretlemez. Eksik telefon/çeviri/auth kanıtını Qloo testiyle kapatılmış göstermeyiz.

## 8. Bir sonraki somut tasarım işi

P-003 önerisi: ikinci görsel taslağa gerçek katalogdan **mutfak, ortam, beslenme ve bütçe** seçimleri; **sevilen restoran autocomplete** ve **fotoğraflı sonuç kartı** sözleşmesi eklemek. Kullanıcıya “tercih” ile “zorunluluk” ayrımını göstermek. İlk iterasyonda yalnızca yukarıda denenmiş eşlemeleri desteklemek; yeni eşleme eklemeden test etmek.

Gerçek restoran fotoğrafları veya Qloo payload'ı statik/public prototipe gömülmedi. Sonraki gerçek entegrasyon API anahtarını yalnız sunucuda tutmalı; API verisini public repoda ham fixture olarak yayımlamamalı.
