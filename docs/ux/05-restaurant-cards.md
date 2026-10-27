# Restoran kartları

21 Ekim 2026 · P-004 · Tasarım önerisi; kullanıcı onayı veya gerçek uygulama değildir.

Kaynak: [Ürün baseline](../../PRODUCT_REQUIREMENTS.md), özellikle AC-02.1–02.7; [canlı API bulguları](04-api-backed-ux-recommendations.md); D-006 görsel ve akışkan UX yönü. Kullanıcı araştırması yapılmadı. Bu tur yeni API sorgusu yapılmadı.

## Önerilen bilgi seviyesi

Kartın görevi “Bunu değerlendirmek istiyor muyum?” sorusunu cevaplamak. Rezervasyon koşulları ayrı adımda toplanır.

| İlk görünüm | Kaynak / gösterim kuralı |
| --- | --- |
| Tek büyük restoran fotoğrafı | `properties.image/images`; bulunamazsa adı/mutfak bilgisi olan nötr görsel alanı, “Fotoğraf mevcut değil”. Başka restoran fotoğrafı kullanma. |
| Restoran adı | Entity adı; kimlik ve restoran kategorisi kontrolünden sonra göster. |
| Mutfak, semt/şehir | Geçerli tür etiketleri ve konum alanları; bilinmeyeni uydurma. |
| Göreli fiyat | `price_level`: ekonomik/orta/yüksek/çok yüksek. Eksikse “Fiyat bilgisi yok”. Kişi başı para tutarı çıkarma. |
| En fazla iki ayırt edici özellik | Sonuçta gerçekten mevcut, kullanıcı tercihleriyle ilgili etiketler. Yalnız arama sinyali gönderilmesi rozet için yeterli değil. |
| Tek cümle öneri gerekçesi | Gözlenen veri ve tercih eşleşmesi. Örneğin “Sakin ortam tercihinle örtüşen bir etiketi var.” Zayıf kanıtta “Seçtiğin şehir ve mutfak aramasından bir aday.” |
| Detaylar + Bu restoranı seç | Detay açma ve geri alınabilir yerel seçim. Kart seçmek telefon araması başlatmaz. |
| Müsaitlik notu | “Masa müsaitliği telefon görüşmesinde teyit edilir.” |

## Detay açılınca

Tam adres, telefonun varlığı/numarası, çalışma saatleri (restoranın yerel saatinde), harita, web sitesi, varsa menü ve gerekçenin veri dayanağı gösterilir. Bağlantılar yalnız alan varsa etkin olur; boş menü düğmesi gösterilmez. Google Place ID varsa doğru Google Maps bağlantısı oluşturulabilir; Qloo UUID kullanılmaz. Telefonun bulunması numaranın doğruluğunu veya rezervasyon kabul edildiğini kanıtlamaz; aramadan önce doğrulama gerekir.

`business_rating` ileride kaynak/ölçek doğrulanırsa ikincil bilgi olabilir; şimdilik ilk görünümden çıkarıldı. Kaynak doğrulanmadan “Google puanı” yazılmaz. Affinity yüzdesi, yürüyüş süresi ve gerçek zamanlı masa müsaitliği gösterilmez. Güncellik zamanı bilinmiyorsa “az önce doğrulandı” denmez. Beslenme etiketleri sertifika veya alerji güvenliği garantisi değildir.

## İki görsel alternatif

- **Fotoğraf odaklı:** Büyük üst fotoğraf, güçlü isim hiyerarşisi, iki özellik ve kısa gerekçe. İlk keşifte önerilen yaklaşım; başlangıçta üç aday sunma fikri ayrıca doğrulanmalı.
- **Kompakt karşılaştırma:** Fotoğraf solda, aynı karar bilgileri sağda. Daha fazla adayı tararken kullanılabilir. Dar alanda fotoğraf üste geçer; içerik sırası ve eylemler korunur.

İki alternatif de aynı kurgusal Terrazza Lume kaydını kullanır; gerçek işletme veya canlı Qloo sonucu değildir. Kullanılan fotoğraf önceki çalışmada üretilmiş temsili Akdeniz terasıdır; Roma veya bu işletmenin fotoğrafı sayılmaz. Üretimde gerçek kaydın fotoğrafı veya nötr fallback kullanılmalı. Karşılaştırma için kullanılan iki ayrı kartın seçim durumu prototipte bağımsızdır; gerçek listede seçilmiş tek restoran kimliği ortak tutulmalı.

## Durum ve etkileşim sözleşmesi

- Detaylar aynı kart içinde açılır; `aria-expanded` güncellenir, klavye odağı tetikleyicide kalır. Kapatmak veya kart düzenini değiştirmek seçim girdilerini silmez.
- Seç düğmesi “Seçildi” olur; tekrar basmak seçimi kaldırır. Yerel durum canlı bölgede duyurulur. Gerçek üründe sonraki hedef tarih/saat/kişi/özel istek adımıdır; listeye dönünce filtre, kart ve kaydırma konumu korunmalı. Bu adım prototipte yalnız açıklama olarak simüle edilir.
- Telefon eksikse kart keşifte kalır. Eksiklik görünür biçimde belirtilmeli; başka restoran seçme yolu sunulmalı. Arama başlatılamaz. Prototipin tasarım kontrolünde “Telefon bilgisi eksik” seçeneği bu detay/seçim durumunu gösterir; canlı telefon doğrulaması yapmaz.
- Veri yüklenirken sabit tahmini tamamlanma süresi verme. Liste hatası veya boş sonuçta mevcut tercihler korunur; yeniden dene/tercihi düzenle sunulur. Zorunlu koşullar sessizce kaldırılmaz. Bunlar kart önizlemesinde uygulanmadı.
- 320 px ve üstünde içerik sarılır; ana eylem gerektiğinde ayrı satıra iner. Uzun isimler kesilmeden büyür. Dokunma hedefleri en az 44 px yükseklikte; hover gerektiren içerik yok. Hareket azaltma tercihi fotoğraf geçişini kapatır.
- Arama ve rezervasyon dış etkisi yalnız sonraki ürün akışının açık başlatma noktasında olur. Bu tasarım login zamanını veya sağlayıcı seçimini kesinleştirmez.

## Kontrol ve açık konular

Yerel tarayıcı önizlemesinde görsel yüklenmesi, detay açılması, seçim durumu ve alternatif geçişi doğrulandı. Kompakt kart 320 px viewport altında kontrol edildi: bileşen clientWidth=288 ve scrollWidth=288; yatay taşma gözlenmedi. Bu kontroller kullanıcı testi, tüm tarayıcı/ekran okuyucu uyumu veya üretim entegrasyonu doğrulaması değildir. Telefon eksik tasarım kontrolü kodda mevcut; bu tur host kontrolü üzerinden çalıştırılmadı. Varsayılan görünüm koyu tema ile görsel incelendi; açık tema ayrıca incelenmedi.

Ürün sahibiyle sonraki değerlendirme: ilk keşifte fotoğraf odaklı kart uygun mu, fiyat/öneri gerekçesi yeterince anlaşılır mı, kullanıcı seçim ile rezervasyonun tamamlanmasını ayırabiliyor mu? Kullanıcı kabulünden önce P-004 öneri olarak kalır. Veri kaynağı/freshness ve bağlantı güvenilirliği uygulama entegrasyonunda ayrıca doğrulanacak.

Yerel önizleme: [restaurant-cards-preview.html](restaurant-cards-preview.html). Uygulama veya yayına alınmış site değildir.


## 21 Ekim güncellemesi — Gerçek veri ve konum

D-007 kullanıcının açık talimatıdır: yeni gerçek veri kartında tam adres ve “Konumda gör” eylemi ilk görünümde bulunur; haritayı yalnız detayda sunan önceki P-004 önerisinin bu kısmını değiştirir. Önceki sentetik alternatifler tarihsel taslak olarak korunur.

[Gerçek restoran kartı](restaurant-card-live.html): Qloo’dan yeni çağrıyla alınan Pizza By The Bay, Mumbai kaydı. Fotoğraf doğrudan Qloo URL’sinden, Google Maps bağlantısı external.google_place.place_id alanından kullanıldı. API snapshot’ı 21 Ekim 2026 tarihli; işletme bilgisi/müsaitlik bağımsız teyit edilmedi. Fiyat seviyesi 3 göreli “Yüksek” etiketiyle gösterilir. Fotoğrafın tarayıcıda yüklendiği doğrulandı (420 px doğal genişlik). Harita href’i doğrulandı; hedef Maps sayfası kontrol edilmedi. Bu yerel prototip gerçek rezervasyon başlatmaz.
