# Qloo Agentic Hackathon — İsterler

Kontrol: 20 Ekim 2026. Aşağıdakiler kaynakların kısa çalışma özetidir; resmi kuralların yerine geçmez.

## Ürün ve teslim

- [ ] Qloo API kullanan çalışan bir uygulama: agentic araç, agent framework uygulaması veya mevcut agente entegrasyon.
- [ ] Kültürel tercih bilgisi ürünün kararlarını anlamlı biçimde iyileştiriyor.
- [ ] Dışarıda yayımlanmış, uçtan uca denenebilir demo URL’si.
- [ ] GitHub/GitLab/Bitbucket üzerinde public repo; kaynaklar, varlıklar ve çalıştırma talimatları.
- [ ] Repo tarafından tanınan, About bölümünde görünen açık kaynak lisansı.
- [ ] Özellikleri ve Qloo katkısını açıklayan proje metni.
- Video zorunlu değil; yalnızca yerelde çalışan demo yeterli değil.

Kaynak: [Genel sayfa](https://qloo.devpost.com/).

## Takvim — Europe/Istanbul

| Olay | Türkiye saati |
| --- | --- |
| Son teslim | 31 Ekim 2026, 06:45 |
| Değerlendirme | 2 Kasım 20:00 – 17 Kasım 07:45 |
| Sonuçlar, yaklaşık | 23 Kasım 23:00 |

Son teslimin orijinali: 30 Ekim 2026, 23:45 EDT. Takvim, açılışı 09:30 EDT; kurallar 09:00 Eastern olarak gösteriyor. Kasım başındaki EST etiketi de saat değişimine dikkat gerektiriyor; değerlendirme başlangıcını kurallardaki Eastern Time üzerinden çevirdik. Son teslim öncesi yeniden kontrol edilmeli.

Kaynaklar: [Takvim](https://qloo.devpost.com/details/dates), [Kurallar §1](https://qloo.devpost.com/rules).

## Katılım ve diğer koşullar

- [ ] Devpost kaydı ve süresi içinde submission.
- [ ] İkamet ülkesinde reşit katılımcılar; birey, ekip veya kuruluş kabul ediliyor. Ekipte yetkili temsilci gerekiyor.
- [ ] Yasaklı bölgeler ve organizatör/jüri bağlantılı çıkar çatışması istisnaları kontrol edilmeli. Türkiye açıkça yasaklı listede değil; bu tek başına uygunluk garantisi değil.
- [ ] İngilizce teslim veya tüm materyallerin İngilizce çevirisi.
- [ ] Jüriye değerlendirme sonuna kadar ücretsiz, kısıtsız test erişimi.
- [ ] Özgün çalışma; üçüncü taraf içerik/API/lisans hakları sağlanmalı.
- [ ] Eski projede yarışma dönemindeki önemli değişiklikler açıklanmalı. §4’te mevcut projelerle ilgili cümle bozuk; bu yolu seçersek yazılı netleştirme gerekli.
- Birden çok başvuru birbirinden esaslı biçimde farklı olmalı.
- Süre bitince submission değişikliği genel olarak kapalı.
- Haklar geliştiricide kalıyor; değerlendirme ve tanıtım izinleri mevcut. Ödül doğrulaması, form ve vergi yükümlülükleri var.
- Çelişkide resmi kurallar üstün. Test bölümünde özel siteye giriş bilgisi kabul edilirken genel sayfa özel erişimi dışlıyor; tercihimiz giriş engeli olmayan public demo.

Kaynak: [Kurallar §3–8, §11](https://qloo.devpost.com/rules).

## Jüri ve ödül

Ön eleme tema/API uygunluğu; ardından eşit ağırlıklı dört ölçüt: teknik uygulama, tasarım, potansiyel etki, fikir kalitesi. Eşitlikte ölçüt sırası kullanılıyor. [Kurallar §6](https://qloo.devpost.com/rules).

Ödüller: 15.000 / 6.000 / 4.000 USD. Ayrıca ana sayfada Jason Calacanis’in favorisine 25.000 USD yatırım duyurusu var; bunu garanti nakit ödül veya açıklanmış yatırım şartları olarak değerlendirmiyoruz. [Duyuru](https://qloo.devpost.com/).

## Teknik başlangıç

- Anahtar başvurusu fikir kesinleşmeden yapılabiliyor; manuel onay birkaç iş günü sürebilir.
- Base URL: `https://hackathon.api.qloo.com`; header: `X-Api-Key`.
- `/search` ile entity, `/v2/tags` ile tag kimliği bul; `GET /v2/insights` çağrısında kullan.
- `filter.type` gerekli; desteklenen parametreleri kategoriye göre doğrula. Search türleriyle Insights türleri aynı değil.
- `/recommendations`, `/recs` kullanılmıyor. Geçersiz parametreler sessizce yok sayılabiliyor; HTTP 200 tek başına doğruluk kanıtı değil.
- Bölgesel veri eksikliği mümkün; hedef şehir ve kategoriyi erken dene.
- Anahtarlar değerlendirme boyunca aktif; sonrasında kapanıyor. Kota artışı Discord üzerinden istenebiliyor; sayısal limit belirtilmiyor.
- Özel sunucu cache’i mümkün; Qloo yanıtlarını public repoya koyma.

Kaynak ve anahtar formu: [Geliştirici rehberi](https://docs.qloo.com/reference/qloo-llm-hackathon-developer-guide).

Başlangıç kaynakları: [Resmi kit](https://github.com/qloo/qloo-hackathon-kit), [Kaynaklar ve Discord](https://qloo.devpost.com/resources).
