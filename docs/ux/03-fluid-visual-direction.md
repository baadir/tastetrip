# Görsel ve akışkan UX — ikinci yön

Tarih: 20 Ekim 2026. Durum: **tasarım önerisi / etkileşim simülasyonu**. D-006 kullanıcı geri bildirimiyle hazırlanmıştır; bu yön henüz kullanıcı tarafından beğenilmiş veya onaylanmış değildir.

## Değişimin nedeni

İlk taslak metin ağırlıklı bulundu. Kullanıcı daha görsel olarak çekici, akışkan ve geçişli bir deneyim istedi. Önceki taslak silinmedi; onun yerine yeni sürüm oluşturuldu. Ürün kapsamı, API bekleme ve açık UX kararları korunuyor.

## Görsel öneri

- Seyahat/yemek atmosferini taşıyan büyük editoryal görsel.
- Tekrarlanan açıklama blokları yerine her adımda tek temel karar.
- Sıcak vurgu rengi, serif başlık ve sade kontrol tipografisi; açık/koyu görünüme uyumlu ürün renkleri.
- Adım ilerledikçe aynı fotoğrafın kadrajı, çerçevesi ve kısa başlığı değişir; kullanıcının aynı yolculukta olduğu hissi korunur.
- İçerik geçişi: yaklaşık 420ms yatay hareket ve görünürlük değişimi. Giriş yüzeyi: yaklaşık 280ms dikey hareket. Sürekli dönen/dekoratif animasyon yok.
- `prefers-reduced-motion` durumunda animasyon ve CSS geçişleri kapatılır; bilgi ve eylemler aynı kalır.

Renk, font ve adım sırası **P-002 önerisidir**, kesin ürün kararı değildir.

## Akış ve davranış sözleşmesi

| Yüzey | Karar / eylem | Korunan bilgi ve geri dönüş | Tamamlanma kanıtı |
| --- | --- | --- | --- |
| Yerin | Şehir yaz veya örnek şehir seç; devam et | Şehir metni korunur; boşsa hata ve alan odağı | Planın adımı açılır; henüz gerçek arama yok |
| Planın | İsteğe bağlı tarih/saat ve kişi sayısı | Bilinmeyen değerler kendiliğinden atanmaz; geri gidilebilir | Bir sonraki adımda aynı girdiler bellekte |
| Zevkin | İsteğe bağlı serbest metin | Hazır Qloo tag listesi uydurulmaz; geri dönüşte metin durur | Özet tam olarak girilen metni gösterir; anlaşıldı/çözümlendi iddiası yok |
| Özetin | Bilgileri gözden geçir veya düzenle | Şehir, tarih/saat, kişi ve tercih görünür | Geçerli girdiler gösterilir; gerçek restoran sonuçları/API beklenir |
| Giriş | Yerel örnek oturum veya iptal | Aynı plan üzerinde kalır; native dialog focus/ESC davranışı | Oturum simülasyonu etiketi ve özete dönüş; gerçek arama/sunucu kaydı yok |
| Yolculuğum | Bu önizlemede oluşturulmuş plana dön | Yeni rezervasyon veya arama başlatılmaz | Mevcut plan özeti veya plan yok açıklaması |

Bu örnekte login keşif öncesinde zorunlu değil; planı saklama isteğinde sunuluyor. Bu, P-001'i kesinleştiren veya değiştiren bir karar değil; farklı erken giriş ve geri dönüş durumunu gösteren **P-002 önizlemesi**. Gerçek rezervasyondan önce login zorunluluğu hâlâ açık.

## Responsive davranış

Geniş alanda içerik solda, büyük atmosfer görseli sağda. Dar alanda görsel kısa bir üst bölüme dönüşür; alanlar ve düğmeler tek sütunda ilerler. Kişi kontrolü dışında sürükleme, hover veya kaydırma jesti zorunlu değil. Klavye odağı adım değişiminde geçerli adım düğmesine taşınır; önceki adımlara düğmelerle dönülür. Dialog yerel odak yönetimi kullanır. Mobil klavye ve ekran okuyucu testleri yapılmadı.

## Gerçek veri sınırı

- Qloo, LLM, kimlik veya telefon servisi yok; hiçbir restoran aranmaz.
- Örnek şehirler kapsama garantisi değil. Fotoğraf gerçek restoran kaydı veya öneri değil.
- Kullanıcının serbest metni anlamlandırılmıyor; özette olduğu gibi gösteriliyor.
- Veriler yalnızca önizleme belleğinde. Yenileme ve cihaz değişiminde saklama yok.
- Özet saatinin gerçek restoranın saat dilimiyle doğrulanması sonraki entegrasyon işidir.
- Restoran seçimi, gerçek rezervasyon, canlı ses ve çeviri ekranı bu revizyonun kapsamına alınmadı; ürün kapsamından çıkarılmış değiller.

## Görsel varlık ve üretim kaydı

- Yerel kaynak: `assets/dining-atmosphere-v2.png`.
- Hafif kopya: `assets/dining-atmosphere-v2.jpg`.
- Üretim: built-in ImageGen. Üretilen görsel görüntülenerek incelendi; figür/yer adı içermez.
- Görsel yalnızca bir atmosfer önerisidir; gerçek mekân veya Qloo sonucu gibi kullanılmaz.

Üretim prompt'u:

> Use case: photorealistic-natural. Asset type: editorial hero photograph for a travel restaurant concierge UX prototype. Create a cinematic premium travel editorial photograph of an intimate open-air restaurant terrace on the Mediterranean coast at golden hour, viewed from a seated guest perspective. Foreground beautiful round white linen dining table set for two with handmade ceramic plates, olives and a small pasta dish, one candle and glassware. Warm amber natural sunlight, soft olive tree shadows, terracotta and limestone architecture, sea and distant coastal buildings in background. Authentic understated luxury, no people in foreground, no dramatic oversaturated colors. Landscape composition, table in right half with beautiful architectural depth, usable image across full crop. No words, lettering, logos, borders, watermark or UI. This is an illustrative atmosphere image, not a named real restaurant.

## Kontrol kaydı

- Yerel tarayıcıda açılış görseli yüklendi ve geniş görünüm incelendi.
- Boş şehir doğrulaması çalıştı; hata metni ve alana odak görüldü.
- Roma → 24 Ekim 2026 / 19:30 → 2 kişi → serbest metin → özet geçişi yapıldı; değerler doğru gösterildi.
- Giriş dialogu iptali ve örnek oturumla dönüş kontrol edildi; aynı plan korundu.
- Geri dönüldüğünde tercih metni korunduğu arayüzde görüldü.
- 390px dar görünüm görsel olarak incelendi; 390px ve 320px'de kök scroll genişliği içerik genişliğine eşitti (yatay taşma ölçülmedi).
- Animasyon süreleri ve reduced-motion CSS yolu mevcut; OS reduced-motion, tüm browser çeşitleri, ekran okuyucu ve gerçek mobil klavye denemesi yapılmadı.
- Bu kayıt kullanılabilirlik araştırması, erişilebilirlik uygunluğu veya gerçek API testi sonucu değildir.

## Sonraki değerlendirme

Kullanıcı bu görsel yönü, bir karar/adım yaklaşımını ve geçiş hissini değerlendirecek. Login zamanı, son keşif modeli, gerçek tag seçenekleri, hedef ülkeler ve servis sağlayıcıları hâlâ açık. API gelince gerçek restoran içerikleriyle akış revize edilecek.
