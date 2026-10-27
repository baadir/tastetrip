# Qloo nedir, ne işe yarar?

> **21 Ekim 2026 güncellemesi:** Aşağıdaki ilk doküman temelli özet tarihsel olarak korunuyor. Artık ilk canlı erişim doğrulaması yapıldı; telefon, Google Place ID, Mumbai kapsamı ve etiketlerle ilgili güncel kanıt/sınırlar için [canlı doğrulama raporunu](docs/QLOO_LIVE_VALIDATION.md) oku. Bu örnekler tüm kayıtlar için garanti değil.

Kontrol tarihi: 20 Ekim 2026. Bu belge resmi dokümanlara dayanan teknik özettir; canlı API testi yapılmadı. Dokümantasyon sitesi bu kontrolde açılamadığı için Qloo’nun kendi [resmi dokümantasyon deposu](https://github.com/qloo/docs-public) kullanıldı.

## Temel fikir

Qloo, insanların kültürel tercihleri arasındaki ilişkileri uygulamalara sunan bir veri ve model katmanıdır. Film, müzik, kitap, marka ve mekân gibi farklı alanlar arasında tercih bağlantıları kurarak öneri üretmeye yardımcı olur. Qloo bunu kültürel zekâ ve kategoriler arası zevk modelleri olarak tanımlıyor. [Resmi ürün açıklaması](https://www.qloo.com/).

Örnek ürün senaryosu — gerçek API sonucu değildir:

> Kullanıcı birkaç sevdiği film ve sanatçıyı seçer. Uygulama bu tercihleri Qloo’ya sinyal olarak verir ve hedef şehirdeki mekân adaylarını ister. Kendi agentımız adayları zaman, bütçe ve kullanıcı geri bildirimiyle değerlendirerek bir plan oluşturur.

Burada tercih ilişkilerini Qloo sağlar; konuşmayı, planı, iş kurallarını ve gerekli ek entegrasyonları biz geliştiririz.

## Temel kavramlar

| Kavram | Anlamı |
| --- | --- |
| Entity | API’nin tanıdığı film, sanatçı, kitap, marka veya mekân gibi kayıt |
| Tag | Tür, tema veya ilgi alanını temsil eden etiket |
| Signal | Sonuçları yönlendirmek için verdiğimiz tercih, kitle veya konum bilgisi |
| Filter | Hangi sonuçların kabul edileceğini sınırlandıran koşul |
| Affinity | Girdi ile sonuç arasındaki ilişkinin gücünü anlatan skor |

Sinyal ile filtre arasındaki pratik ayrım: “Bu sanatçıları seviyorum” tercihi yönlendirir; “yalnızca bu şehirdeki mekânları getir” sonuç kümesini sınırlar. Kullanılabilir kombinasyon kategoriye bağlıdır. [API genel bakış](https://github.com/qloo/docs-public/blob/main/reference/api-overview.md), [Parametreler](https://github.com/qloo/docs-public/blob/main/reference/insights-api-deep-dive.md).

## Yetenek haritası

| Yetenek | Ne sağlar? | Uygulama fikri |
| --- | --- | --- |
| Tercihe göre öneri | Entity, etiket, kitle ve konum sinyalleriyle adaylar | Kişiye uygun keşif listesi |
| Entity arama | İsimden kayıt ve kimlik bulma; kimlikle kayıt arama | Kullanıcının seçtiği filmin doğru kaydını çözme |
| Etiket ve kitle arama | API’ye verilebilecek geçerli girdileri bulma | Serbest metni desteklenen girdilere dönüştürme |
| Konuma göre içgörü | Coğrafyaya göre öneri ve tercih analizi | Bir şehirde uygun mekân keşfi |
| Heatmap | Coğrafi yakınlık/ilgi verisini haritalama | Tercihlerin bölgesel dağılımını gösterme |
| Grup analizi ve karşılaştırma | Entity gruplarını analiz etme ve karşılaştırma | İki seçkiyi karşılaştırma |
| Trendler | Kategori trendleri ve entity bazında haftalık değişim | Yeni yükselen adayları izleme |

Bu tablo platformdaki belgelenmiş işlevleri gösterir; belirli anahtarın bütün kombinasyonlara eriştiğini kanıtlamaz. [API genel bakış](https://github.com/qloo/docs-public/blob/main/reference/api-overview.md).

### Zevk profilini açıklayıcı etiketlere dönüştürme

Taste Analysis, tercihlerle ilişkili tag içgörüleri üretir. Örneğin bir film seçkisinin ilişkili temalarını incelemek için kullanılabilir. Entity, tag, kitle ve konum sinyalleri uygun kombinasyonlarla birleştirilebilir. [Taste Analysis](https://github.com/qloo/docs-public/blob/main/reference/taste-analysis.md).

### Kitle ve demografik içgörüler

Bir entity veya tag ile ilişkili yaş ve cinsiyet gibi demografik dağılımlar/affinity bilgileri alınabilir. Bu, kitle düzeyindeki ilişkilere yöneliktir; belirli bir kullanıcının yaşını veya kimliğini kesin olarak öğrenme anlamına gelmez. [Demografik içgörüler](https://github.com/qloo/docs-public/blob/main/reference/demographics-use-case.md).

### Filtreleme ve açıklanabilirlik

Genel API referansında kategoriye bağlı olarak konum, etiket, hariç tutulan entity, çıkış yılı ve içerik derecelendirmesi gibi filtreler bulunuyor. `feature.explainability`, desteklendiğinde girdi entity’lerinin önerilere katkısını açıklayan metadata istiyor. Hesaplanamazsa uyarı gelebiliyor; bu özelliği kullanacağımız ortamda ayrıca denemeliyiz. [Insights referansı](https://github.com/qloo/docs-public/blob/main/reference/insights-api-deep-dive.md).

## Skorları nasıl okumalıyız?

Affinity, girdilerle sonuçlar arasındaki ilişkinin gücünü ifade eder. Bağlamı öneri, konum veya etiket analizi olabilir. Doküman, skorların sorgu bağlamına göre normalize edildiğini belirtiyor; farklı sorgulardaki ham skorları doğrudan karşılaştırmamalıyız. Küçük farklar büyük ürün kararlarına temel olmamalı.

Bizim arayüz yorumumuz: “%90 affinity” ifadesini “Bu kişinin bunu beğenme olasılığı %90” diye çevirmeyeceğiz. Böyle bir kişisel memnuniyet garantisi çıkarmak uygun değil. [Skor yorumlama rehberi](https://github.com/qloo/docs-public/blob/main/docs/interpreting-affinity-scores.md).

## LLM ve agent ile nasıl birleşir?

Önerilen görev paylaşımı — bizim mimari önerimiz:

| Bileşen | Sorumluluk |
| --- | --- |
| LLM | Kullanıcı isteğini anlama, eksik bilgiyi sorma, sonuçları anlaşılır anlatma |
| Qloo | Tercih sinyallerine göre aday ve ilişkili içgörü sağlama |
| Uygulama/agent | Araç çağırma, kısıt kontrolü, alternatif üretme, geri bildirimle yeniden planlama |
| Diğer servisler | Gerekirse müsaitlik, ulaşım, fiyat, rezervasyon gibi operasyonel veri/işlem |

Örnek akış:

1. Kullanıcı tercih ve hedefini söyler.
2. Uygulama doğru entity ve tag kimliklerini çözer.
3. Qloo’dan hedef kategoride adaylar istenir.
4. Uygulama sonuçları kendi kuralları ve gerekiyorsa ek verilerle değerlendirir.
5. Agent planı sunar; itiraza göre yeni adaylar isteyebilir.

Bu, tasarım örneğidir; kullanıcıya uygunluğunu gerçek sonuç ve kullanıcı denemesiyle doğrulayacağız.

## Neleri varsaymamalıyız?

Aşağıdakiler bizim uygulama sınırlarımızdır:

- Qloo’yu her soruyu yanıtlayan bir sohbet modeli veya genel internet arama motoru olarak kullanmayacağız.
- Tercih ilişkisini gerçek zamanlı stok, fiyat, açık olma veya rezervasyon garantisi saymayacağız. Dönen alanların kapsamını ve güncelliğini ayrıca doğrulayacağız.
- Grup analizi özelliğini otomatik “arkadaşlar arasında adil uzlaşma” algoritması saymayacağız; bu karar mantığını biz tasarlayacağız.
- Beğeni ilişkisini sağlık gereksinimine uygunluk veya güvenlik onayı gibi yorumlamayacağız.
- Her şehirde ve her kategoride aynı veri derinliği olduğunu varsaymayacağız.
- Demografik grup içgörüsünü tek bir kişi hakkındaki kesin bilgiye dönüştürmeyeceğiz.

## Hackathon için pratik not

Bu proje için mevcut [isterler dosyasındaki](HACKATHON_REQUIREMENTS.md) hackathon ortamını esas alacağız. Üretim API dokümanındaki her örneği doğrudan kopyalamak yerine ortam, yöntem, entity türü ve parametre desteğini doğrulayacağız. Genel referans ile hackathon rehberi arasında yöntem ve tür adları bakımından farklılıklar görülebiliyor.

İlk teknik deneyin hedefi: üç farklı profilin gerçekten farklı ve yararlı adaylar üretmesi; bulunamayan entity ve boş sonuç durumlarının anlaşılması. Bunun ardından hangi ürün fikrinin Qloo’dan en fazla faydalandığını seçebiliriz.

Kaynak: [Hackathon geliştirici rehberi](https://docs.qloo.com/reference/qloo-llm-hackathon-developer-guide) — önceki incelemede erişildi; bu kontrolde site açılamadı.
