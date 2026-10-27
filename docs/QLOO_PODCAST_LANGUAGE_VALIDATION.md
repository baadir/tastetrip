# Podcast yayın dili — canlı API deneyi

21 Ekim 2026. Amaç: Qloo ile podcast önerisini yayın diline göre filtreleyebilmek. Uygulama davranışı değiştirilmedi; araştırma ve salt okunur deney yapıldı.

## Deneyler

Aynı restoran entity sinyali, podcast türü ve take=5 ile temel sorgu ve son tekrar dahil 10 Insights çağrısı; 4 podcast etiket araması. Sonrasında 2 podcast’in dış kimliğini almak için 1 Insights çağrısı. Toplam 15 Qloo çağrısı. İki podcast için iTunes Lookup + RSS olmak üzere 4 ek salt okunur HTTP isteği.

| Deneme | Sonuç | Yorum |
| --- | --- | --- |
| Filtresiz temel sorgu / tekrar | HTTP 200, aynı 5 ID ve sıra | Kıyas için anlık kontrol; genel deterministiklik kanıtı değil |
| `language=tr/en/zz` | HTTP 200, temel sorguyla aynı 5 ID ve sıra | Dil filtresi uygulandığına kanıt yok; geçersiz kod da aynı |
| `filter.language=tr/en/zz` | Aynı | Bu isimde parametrenin çalıştığı doğrulanamadı |
| `filter.languages=tr`, `filter.language_code=tr` | Aynı | Kabul edildi diye desteklenen filtre sayılamaz |
| Podcast tag araması `Turkish`, `English` | Boş | Tam katalogda dil bilgisi yok demek değil |
| `language`, `Turkish language` tag araması | Language / Language Learning vb. konu etiketleri | Dil öğrenme konusu, yayının konuşma dili değildir |
| Metadata içindeki `languages` | `short_descriptions[].languages` de/es/fr/en | Açıklama çevirisinin dili; yayın dili diye kullanılamaz |

Kaynak kodu: `scripts/qloo_podcast_language_probe.py`. Anahtarı `.env` içinden alır; anahtarı, istek başlıklarını veya ham yanıtı saklamaz. Karşılaştırma özeti: `docs/validation/qloo-podcast-language-2026-10-21.json`. Son 1 Insights ve 4 dış istek ek doğrulamadır; scriptin 14-call matrisinden ayrıdır.

## Alternatif gerçekten çalıştı mı?

Qloo `external.itunes[].id` alanından iTunes Lookup ile `feedUrl` alındı; RSS XML `channel/language` okundu:

| Qloo podcast’i | iTunes ID | Lookup | RSS | Bildirilen yayın dili |
| --- | --- | --- | --- | --- |
| Berner Phone | 1442257788 | 200 | 200 | `en` |
| Giggly Squad | 1536352412 | 200 | 200 | `en` |

Bu, iki örnekte dil metadata’sına erişilebildiğini gösterir. RSS yayıncının beyanıdır; her bölümün dili, tüm katalog kapsamı, güncellik veya Türkçe sonuç bulunması garanti edilmez. Medya dosyası indirilmedi/dinlenmedi. Bu iki İngilizce kayıt Türkçe podcast envanteri testinin yerine geçmez.

## Ürün için öneri — henüz uygulanmadı

Qloo’dan konu ve zevkle ilişkili daha geniş aday havuzu → iTunes kimliğiyle RSS bulma → yayın dili metadata’sını doğrulama/önbellekleme → seçilen `tr` / `en` vb. kodla filtreleme. `tr-TR` gibi varyantlar temel `tr` ile eşlenebilir. Dil bulunamayanlar Türkçe diye sunulmaz; ayrı “Dil doğrulanamadı” durumunda tutulur. Yeterli aday kalmazsa koşul sessizce esnetilmez. Türkçe aday bulma kapsamı ayrıca denenmeli; gerekirse dil bazlı podcast kataloğu keşfi ve Qloo sıralaması birlikte tasarlanmalı.

Üretim RSS entegrasyonunda dış URL doğrulaması, özel ağlara erişim engeli, redirect/timeout/boyut sınırları ve güvenli XML işleme gerekir. Bu deney scripti kullanıcıdan URL alan bir servis değildir; dış besleme proxy’si uygulamaya açılmadı.

Resmi şema ve belgelerde de bir yayın dili filtresi doğrulanamadı: https://github.com/qloo/docs-public . Dil filtresi yoktur şeklinde evrensel bir API garantisi yerine bu hackathon erişiminde **doğrulanamadı** sonucu kullanılmalı.
