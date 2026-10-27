# Qloo — İlk canlı erişim ve veri doğrulaması

> Takip çalışması: 52 ek çağrıyla şehir, etiket, kategori ve kişisel sinyal deneyleri yapıldı. Güncel kanıt ve öneriler [API'ye dayalı UX raporunda](ux/04-api-backed-ux-recommendations.md). Aşağıdaki ilk kontrol kaydı değiştirilmeden korunmuştur.

Tarih: 21 Ekim 2026. Ortam: `https://hackathon.api.qloo.com`. Toplam 6 salt okunur GET çağrısı. API anahtarı bu dosyaya, proje dosyalarına veya geçmişe kaydedilmedi. Ham API yanıt dosyası oluşturulmadı; aşağıdaki içerik teknik doğrulama özetidir.

## Sonuç

- Kimlik doğrulaması başarılı: Tags ve Insights çağrıları HTTP 200 döndürdü.
- Mumbai + Italian restoran etiketiyle `take=3` sorgusu başarılı ve üç place sonucu döndürdü.
- Dönen sonuçlardan biri otel kaydıydı. Bu nedenle yalnızca mutfak etiketi ile `place` seçmek, yalnız bağımsız restoranlardan oluşan bir sonuç kümesini garanti etmiyor.
- Üç örnek kayıtta `properties.phone`, `properties.address` ve `properties.website` alanları doluydu.
- `take=1` ile ayrıca incelenen örnekte `external.google_place[]` altında `place_id` bulundu. Hazır Maps URL'si bu örnekte gösterilmedi; Place ID ile uygulama bağlantı oluşturabilir. Bu alan tüm kayıtlarda var sayılmaz.
- Tek örnekte saatler, görseller, fiyat seviyesi ve bazı açıklama alanları doluydu. `menu_url` alan adı şemada görünse de incelenen kayıtta dolu alanlar arasında değildi; menü linkini garanti edemeyiz.

## Keşfedilen tercih türleri

| Arama | Gözlenen sonuç | Teknik/UX yorumu |
| --- | --- | --- |
| Italian | Mekân/restoran mutfağına ilişkin genre etiketi; başka kategorilerde aynı isim de var | İsim tek başına yeterli değil; kategori ve kimlik doğrulanmalı |
| quiet | Ambience, noise level, neighborhood ve quiet dining gibi farklı anlamlarda mekân etiketleri | Sessiz iç mekân ile sessiz semt aynı tercih değildir |
| romantic | Mekân ambience etiketleri; ayrıca film/müzik sonuçları | Restoran filtresinde doğru namespace kullanılmalı |
| vegan | Vegan restoran türü, dietary option ve vegan options gibi farklı etiketler | Vegan restoran ile vegan seçenek sunan restoran ayrı seçimlerdir |

Bu, tam katalog değildir. Aramalar sınırlı sayıda sonuç döndürdü. Etiket bulunması, bütün şehirlerde o etiketle yeterli öneri çıkacağı veya gerçek işletmenin koşulu kesin sağlayacağı anlamına gelmez.

## Henüz yapılmayanlar

- Quiet/romantic/vegan etiketleriyle gerçek Insights sonuçlarının ve etiket etkisinin denenmesi.
- İstanbul/Roma ve diğer şehirlerle kapsam karşılaştırması.
- Restoran/otel ayrımını doğru yapan kategori filtresinin doğrulanması.
- Arama → entity seçimi → kişisel sinyal → öneri tam akışı.
- Alan doluluk oranı, telefon güncelliği, işletme kimliği ve müsaitlik doğrulaması.
- Çağrı kalitesi, gecikme, kota veya yük testi.

## UX'e etkisi — henüz karar değil

“Mutfak”, “ortam” ve “beslenme seçenekleri” için gerçek katalogya dayanan arayüz hazırlamak artık mümkün. Önce doğru etiket anlamlarını ve Insights davranışını sınamalıyız. Login zamanı, hazır seçenek listesi veya ikinci görsel yön otomatik olarak onaylanmış sayılmıyor.

## Tekrarlama yolu

Sunucu tarafında `X-Api-Key` header'ı kullan. Anahtarı URL'ye, frontend dosyasına, public repoya veya bu rapora koyma.

- `/v2/tags?filter.query=Italian&take=3`
- `/v2/tags?filter.query=quiet&take=8`
- `/v2/tags?filter.query=romantic&take=8`
- `/v2/tags?filter.query=vegan&take=8`
- `/v2/insights`: `filter.type=urn:entity:place`, `filter.location.query=Mumbai`, `filter.tags=urn:tag:genre:place:restaurant:italian`, `take=3` ve metadata için `take=1`.

Çıktılardan kullanıcıya ait veri veya Qloo ham payload'ını açık kaynak dosyalara aktarmadan, yalnız gerekli teknik doğrulama bulgularını kaydet.
