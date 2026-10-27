# THY kart referansı ve yolculuk içerikleri

21 Ekim 2026. Kaynak proje salt okunur incelendi: `D:/LLM/THY Travel Agent`. Uygulama çalıştırılmadı; değerlendirme kaynak koduna dayanır. Kaynak projede değişiklik veya bileşen aktarımı yapılmadı. Kullanıcı kartları örnek alma izni verdi; aynı renk/marka ve tüm davranışlar onaylanmış sayılmaz.

## İncelenen bileşenler

| Kaynak (`frontend/src/` altında) | Gözlenen yapı | TasteTrip için uyarlama önerisi |
| --- | --- | --- |
| `components/widgets/TimelinePath.tsx` | Gün/tema, saatli dikey duraklar, fotoğraf, not ekleme/düzenleme/silme, görsel galeri | Günlük rota omurgası; sabit stop ID, yerel tarih/saat, ziyaret/geçiş süresi, rezervasyon durumu ve içerik önerisi ekle |
| `components/widgets/PlacesOrbit.tsx` | İsim, kategori etiketi, vibe, açıklama, Konumda gör eylemi; tek sütun kartlar | Mekân kartının hiyerarşisi; mevcut gerçek Qloo fotoğrafı ve adres kartıyla birleştir |
| `components/widgets/PlacesWidget.tsx` | 240 px yatay kayan mekân kartları, fiyat ve konum | Bir durağa alternatif seçme alanı; ana rota yalnız yatay kaydırmaya bağlı olmamalı |
| `components/widgets/ItineraryWidget.tsx` | Basit gün/aktivite/saat çizelgesi | Veri azsa sade görünüm; ana referans daha kapsamlı TimelinePath |
| `components/ui/MapModal.tsx` | Uygulama içinde iframe harita, kapatma ve dış harita bağlantısı | Ayrılmadan konum inceleme; isim araması yerine Qloo koordinatı/Place ID ile doğrulanan hedef kullan; yükleme hatasında dış bağlantıyı koru |
| `components/widgets/WidgetRenderer.tsx` | Widget türüne göre render, plan kaydetme/güncelleme; mevcut auth/chat/API/analytics bağımlılıkları | Ayrı rota/mekân/içerik kartları ortak planı render edebilir; THY backend ve auth bağımlılıklarını taşımadan adaptör kullan |
| `app/globals.css` | Yeşil vurgu, açık zemin, yuvarlak beyaz kartlar, gölge/glass stilleri | Form ve hiyerarşi referansı; TasteTrip’in mevcut görsel yönünü değiştirmek ayrı karar |

Koddan görülen uyarlama ihtiyaçları: MapModal için dialog semantiği, Escape/fokus yönetimi ve iframe başlığı eklenmeli; bazı küçük 10 px etiketler büyütülmeli; not eylemleri yalnız hover ile görünmemeli. TimelinePath optimistik not kaydı başarısızlığında geri alma/tekrar deneme gerekir. Bunlar tüm uygulamayı kapsayan hata veya erişilebilirlik denetimi değildir.

## Kullanıcının eklediği kapsam

Rota içindeki yolculuk, mola ve dinlenme anlarında kitap, film, podcast ve müzik listesi önerileri sunulacak (D-009). Yer ve içerik önerileri aynı zevk profilinden yararlanabilir; kategoriler arası eşleşme kalitesi henüz canlı test edilmedi.

Qloo dokümanında `book`, `movie`, `podcast`, `artist` türleri vardır. Ayrı playlist/track türü Insights enum listesinde görünmüyor. Dolayısıyla “Qloo’dan hazır şarkı listesi gelir” varsayılmaz: sanatçı önerisinden müzik listesine geçmek için parça/playlist sağlayıcısı ve eşleme gerekir. Podcast önerisi de bölüm süresi veya bölüm düzeyinde uygunluk garantisi değildir.

Kaynak: https://github.com/qloo/docs-public/blob/main/reference/insights-api-deep-dive.md (21 Ekim 2026 kontrolü).

## Önerilen yerleşim ve davranış

- Fiziksel duraklar ana zaman çizelgesinde kalır. İçerikler, ilgili durak veya geçiş altında açılabilen “Bu ana eşlik etsin” alanında bulunur; varsayılan bütün kategorilerle ekran doldurulmaz.
- Uzun ulaşım/bekleme: podcast veya film; kafe molası: kitap; otelde dinlenme: film; dinlenme/uygun yolculuk anı: müzik. Bunlar ürün örnekleridir; kullanıcı yürürken veya araç kullanırken ekran izleme önerilmez.
- İçerik kartı: gerçek başlık, yazar/sanatçı, kapak varsa, tür, dil ve süre yalnız doğrulanmışsa, kişisel öneri gerekçesi. “Seyahatime ekle”, “Değiştir”, mevcutsa sağlayıcıda aç. İçerik seçmek fiziksel rota süresini otomatik değiştirmez.
- Kitabı kısa molada bitirecekmiş gibi gösterme; “Bu molada okumaya başlayabilirsin”. Podcast için bölüm/süre bulunmadan “20 dakikaya tam uygun” deme. Film için dil, süre ve izlenebilirlik ayrıca doğrulanır.
- Kişinin içerik istememesi veya bağlantı/sağlayıcı eksikliği rotayı engellemez. Otomatik oynatma yok. Öneri, oynatma, çevrimdışı indirme ve satın alma ayrı yeteneklerdir; bu çalışmada oynatıcı entegrasyonu yok.
- Başarısız sağlayıcı bağlantısında seçim korunur ve “Bağlantı mevcut değil” açıklanır; uydurma sağlayıcı URL’si üretilmez. Medya içerikleri rezervasyon kontrolü taşımaz.

## Veri modeli ve sonraki doğrulama

Plan → gün → durak/geçiş → isteğe bağlı içerik önerileri. İçerikte sabit öneri ID’si, Qloo entity ID/türü, ilişkilendirilen stop veya segment ID, öneri gerekçesinin dayanağı, varsa kaynak URL ve doğrulama zamanı ayrı tutulmalı. Müzik listesi uygulama tarafından derlendiyse “derlenmiş liste” olarak belirtilmeli.

Sonraki çalışma: THY referanslı rota görünümünü TasteTrip’te tasarlamak, kitap/film/podcast/sanatçı için canlı yanıt alanlarını incelemek, müzik sağlayıcısı ve gömme/oynatma yöntemini seçmek. Bu belge kod aktarımı veya yeni görsel prototip üretildiği anlamına gelmez.
