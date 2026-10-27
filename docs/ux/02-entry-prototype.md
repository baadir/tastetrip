# Giriş UX taslağı — ilk görsel çalışma

Tarih: 20 Ekim 2026. Durum: öneri ve etkileşim simülasyonu; kullanıcı onayı veya çalışan ürün değil.

## Kapsam ve izlenebilirlik

D-002 seyahat ve responsive deneyim, D-003 açılış/login odağı, D-004 API öncesi geçici taslak izni bu çalışmanın dayanağıdır. P-001'deki misafir keşif ve arama öncesi login yaklaşımı görselleştirildi; kesinleşmiş karar olarak değiştirilmedi.

Üç ekran:

1. **İlk ziyaret:** şehir + isteğe bağlı doğal dil. “Seçeneklerle ilerle” tarih ve kişi sayısını açar; girilmiş metin kaybolmaz. Şehir yoksa hata ve ilgili alana odak. Gönderimde API sonucunu taklit etmek yerine bağlantının henüz olmadığını belirten özet.
2. **Geri dönen kullanıcı:** örnek yarım keşif kartı; devam ve yeni keşif yolları. Devam eden gerçek arama veya rezervasyon varmış iddiası yok.
3. **Rezervasyondan önce giriş:** sentetik rezervasyon özeti, giriş simülasyonu ve aynı özete geri dönüş. Giriş telefon araması başlatmaz. Arama düğmesi yalnızca simülasyon açıklaması üretir.

## Etkileşim ve veri sınırı

- Gerçek Qloo, LLM, kimlik, telefon, TTS veya çeviri servisi bağlı değil.
- Kullanıcıdan parola, ödeme bilgisi veya gerçek rezervasyon kişisel verisi istenmez.
- Şehir metni ve istek bu önizlemenin belleğinde tutulur; sayfa yenileme veya cihazlar arası saklama uygulanmadı.
- Restoran, tarih ve saat örnektir. Mumbai veri kapsamı veya müsaitlik kanıtı değildir.
- İlk ekran başlığında seyahat bağlamı, sağ panelde keşif/seçim/canlı takip sırası gösterilir.
- Hesap ve stil seçenekleri ürün kararı değil; görsel inceleme içindir.

## Responsive ve erişim davranışı

Geniş alanda görev ve süreç anlatımı iki sütun; dar alanda tek sütun. Alanlar etiketli ve doğal klavye sırasında. Hata bölgesi `role=alert`, sonuç bölgesi `aria-live=polite`. Giriş önizlemesi aynı sayfada bir bölümdür; diyalog gibi gösterilip eksik focus-trap uygulanmadı. Girişe geçiş ve geri dönüşte ilgili düğmeye odak taşınır.

## Yapılan kontroller

- Yerel tarayıcı önizlemesi açıldı.
- Boş şehirde hata ve alana odak doğrulandı. İlk sürümde sandbox form gönderimi çalışmadığından ana eylem düğmesinin yerel etkileşimi düzeltildi ve yeniden denendi.
- Şehir girip özet gösterme, erken giriş simülasyonu, geri dönüş kartı ve rezervasyon öncesi girişten özete dönüş kontrol edildi.
- 390px görünümde ilk ekran görsel olarak incelendi. 390px ve 320px tarayıcı genişliklerinde kök içerikte yatay taşma ölçülmedi.
- Mobil klavye, ekran okuyucu, gerçek auth yönlendirmesi, bağlantı kopması, servis gecikmesi, canlı ses veya çeviri test edilmedi. Erişilebilirlik uygunluğu iddiası yok.

## Sonraki inceleme

Önce ilk ekranın bilgi miktarı ve doğal dil/seçenekli yol dengesi üzerine geri bildirim al. Sonra geri dönen kullanıcı durumlarını ve login zamanını tartış. API geldikten sonra gerçek tercih seçenekleri, restoran metadata'sı ve desteklenen şehirlerle revize et. Prototip davranışı tek başına ürün kararı sayılmaz.
