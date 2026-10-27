# Qloo — Birlikte fikir geliştirme ve uygulama rehberi

20 Ekim 2026. Bu belge bizim çalışma önerimizdir; resmi isterler [HACKATHON_REQUIREMENTS.md](HACKATHON_REQUIREMENTS.md) dosyasındadır. Aşağıdaki fikirler araştırmayla doğrulanmış pazar fırsatları değil, sınanacak hipotezlerdir.

## Başlangıç yaklaşımımız

Önce tek bir insanın zorlandığı kararı seçelim. Ardından o kararda kültürel tercihin hangi bilgiyi sağladığını ve agentın hangi işi tamamlayacağını tarif edelim. Arayüzü ve teknoloji yığınını bu akış netleşince seçelim.

Fikir cümlesi:

> [Kullanıcı], [durum] sırasında [kararı] vermekte zorlanıyor. Bugün [geçici çözümü] kullanıyor. Agentımız [işi] tamamlıyor; Qloo [kararı değiştiren ilişkiyi] sağlıyor. Başarıyı [ölçülebilir sonuç] ile sınayacağız.

## 1. İlk görüşme: problem havuzu

İlk oturumda şu üç bilgiyi belirleyelim:

1. Yakından tanıdığın veya birkaç kullanıcıya ulaşabileceğin alan hangisi?
2. Tek başına mı, ekiple mi ilerleyeceğiz; günlük süre ve güçlü olduğun teknolojiler neler?
3. API anahtarı başvurusu yapıldı mı; demo için tercih ettiğin ülke/dil var mı?

Her problem için son yaşanmış bir örnek arayalım: ne yapılmaya çalışıldı, nerede takılındı, yanlış kararın maliyeti neydi? Mümkünse 3–5 kısa kullanıcı görüşmesi yapalım. Genel beğeni soruları yerine gerçek davranış soralım.

## 2. Üç fikir hipotezi

| Yön | Kullanıcı ve iş | Qloo için sınanacak katkı | Agentın tamamladığı iş | İlk risk |
| --- | --- | --- | --- | --- |
| Ortak zevk bulucu | Farklı tercihleri olan arkadaşlar birlikte bir akşam planlıyor | Kişi bazlı adaylardan ortak kabul görecek seçenekler çıkarma | Tercih toplar, adayları karşılaştırır, itiraza göre planı yeniler | Grup birleştirme mantığını bizim kurmamız ve hedef şehir kapsamı |
| Bağımsız etkinlik küratörü | Küçük bir mekân sahibi temalı etkinlik hazırlıyor | Sanatçı/film/marka gibi sinyallerden uyumlu adaylar çıkarma | Briefi çözer, program taslağı üretir, geri bildirimle düzenler | Gerçek müsaitlik, haklar ve bütçe Qloo dışında doğrulanmalı |
| Yeni şehirde keşif | Taşınan kişi kendi zevkine uygun yerleri bulmak istiyor | Tanıdığı kültürel öğelerden yeni yer adaylarına geçiş | Kısa keşif planı hazırlar, beğenilmeyen durağı değiştirir | Yerel veri kapsamı; saat ve ulaşım için ek kaynak ihtiyacı |

İlk deneme önerim ortak zevk bulucu: iki farklı profil ve bir itiraz üzerinden kararın nasıl değiştiğini kısa bir demoda gösterebiliriz. Bu tercih kesinleşmiş değil; ulaşabildiğin kullanıcı ve gerçek API sonuçları belirleyici olacak.

Qloo’nun grup uzlaşması, rezervasyon veya canlı müsaitlik sunduğunu varsaymıyoruz. Kendi karar mantığımızı ve gerekiyorsa ek veri kaynaklarını açıkça ayıracağız.

## 3. Fikir seçimi

Her adayı 1–5 puanlayalım. Bu ağırlıklar bizim seçim aracımızdır; resmi jüri ağırlıkları değildir.

| Ölçüt | Ağırlık | Aranacak kanıt |
| --- | --- | --- |
| Qloo’nun karar üzerindeki katkısı | %30 | Aynı senaryoda API katkısıyla değişen, yararlı sonuç |
| Gerçek problem ve kullanıcıya erişim | %25 | Yakın zamanda yaşanmış örnek ve görüşülebilen kişi |
| Kalan sürede bitirebilme | %20 | Tek ana akış, az bağımlılık, çalışan veri denemesi |
| Demoda anlaşılabilirlik | %15 | Birkaç dakikada görülen somut çıktı |
| Özgünlük | %10 | Kullanıcının mevcut çözümünden açık fark |

Puan = ağırlıklı ortalama. API erişimi/veri kapsamı doğrulanamayan veya Qloo çıkarılınca aynı kalan fikri yüksek puanına rağmen seçmeyelim.

## 4. Kodlamadan önce küçük veri deneyi

Her finalist için 60–90 dakikalık bir teknik deneme öneriyorum:

1. Üç farklı tercih profili ve hedef kategoriyi yaz.
2. Gerçek entity kimliklerini çöz; isim benzerliğiyle yanlış eşleşmeleri kontrol et.
3. Her profil için gerçek Insights sonucu al; kullanılan parametrelerin desteklendiğini doğrula.
4. Profil değişince sonucun yararlı biçimde değişip değişmediğini incele.
5. Boş sonuç, bulunamayan entity ve kapsam dışı şehir dene.
6. Kararı kaydet: devam / kapsam daralt / fikri ele.

Anahtar yokken ekran taslağı ve sentetik veriyle akışı hazırlayabiliriz; sentetik sonucu gerçek Qloo çıktısı diye sunmayacağız. Gerçek veri geçidi tamamlanmadan fikri teknik olarak doğrulanmış saymayacağız.

## 5. MVP sınırı

Tek kullanıcı türü, tek temel karar, tek ana akış; yalnızca gerekli birkaç araç çağrısı. Hesap sistemi, ödeme, sosyal ağ ve çok sayıda entegrasyonu ilk sürüme eklemeyelim.

Önerilen akış:

`Tercihler + kısıtlar → entity eşleştirme → Qloo adayları → kısıt kontrolü → karar/plan → kullanıcı itirazı → yeniden değerlendirme`

Agent, eksik bilgiyi sormalı ve hangi araca ihtiyaç olduğunu seçmeli. Sonuç açıklaması gerçekten gelen verilere dayanmalı. Qloo ilişkisinden türetilmeyen açıklamaları model yorumu olarak ayırmalı; uydurma gerekçe veya kesin beğeni vaadi üretmemeli.

Başlangıç mimarisi önerisi: tek web uygulaması ve sunucu tarafında API adaptörü. Anahtar sunucuda tutulur; zaman aşımı, sınırlı tekrar denemesi ve kullanıcıya anlaşılır hata mesajları eklenir. Framework kararını mevcut becerilerimize göre veririz.

## 6. Qloo katkısını kanıtlama

Aynı görev ve aynı modelle iki akış karşılaştıralım: yalnız LLM ve Qloo destekli agent. Her ikisine aynı kullanıcı tercihleri ve kısıtları verelim. Başlangıç için 10 sabit senaryo yeterli bir geliştirme seti olabilir; bu sayı istatistiksel kanıt iddiası taşımaz.

Kaydedilecekler:

- Kullanıcının kör karşılaştırmada seçtiği çıktı ve gerekçesi.
- Açık kısıt ihlalleri ve doğrulanamayan öneriler.
- Görevin tamamlanması, yanıt süresi ve çağrı maliyeti.
- Bir tercih değişince kararın nasıl değiştiği.

Sonuçları açık biçimde raporlayalım; birkaç örnekten genel üstünlük yüzdesi üretmeyelim. Eşleşme skorunu kullanıcı memnuniyeti olasılığı gibi sunmayalım.

## 7. Çalışma takvimi önerisi

| Tarih — Türkiye | Hedef ve bitiş koşulu |
| --- | --- |
| 20 Ekim | Anahtar başvurusu, kullanıcı/problem havuzu, üç fikir kartı |
| 21 Ekim | Görüşmeler, finalistler; anahtar geldiyse gerçek veri deneyi |
| 22 Ekim | Veriyle doğrulanmış tek fikir, MVP akışı; erişim gecikirse kapsamı yeniden değerlendir |
| 23–25 Ekim | İlk çalışan uçtan uca ürün ve erken hosting denemesi |
| 26–27 Ekim | Kullanıcı denemeleri, karşılaştırma, hata durumları |
| 28 Ekim | Ürün deneyimi, İngilizce README ve proje metni |
| 29 Ekim | Temiz ortamda kurulum, public demo, lisans ve submission kontrolü |
| 30 Ekim | Erken teslim; kalan zaman yalnızca kritik düzeltmeler |

Bu takvim günlük zamanımız belli olmadığı için taslaktır. Değerlendirme süresince demo erişimini ve API bütçesini koruyacağız. Anahtar kapanışı sonrası devam edeceksek ayrı erişim planı gerekecek; ayrıntılar [resmi rehberde](https://docs.qloo.com/reference/qloo-llm-hackathon-developer-guide).

## 8. Birlikte çalışma düzenimiz

Sen problem bağlamını, kullanıcı erişimini ve tercihlerini getir; ben bunları karşılaştırılabilir fikir kartlarına, API denemelerine, ürün akışına ve uygulama görevlerine dönüştüreyim. Her aşamada somut bir çıktı üzerinden karar verelim:

`Problem örnekleri → üç fikir kartı → veri deneyi → bir sayfalık ürün tanımı → çalışan akış → kullanıcı geri bildirimi → teslim`

Karar kaydı şablonu:

```markdown
### Tarih / karar
- Seçenekler:
- Gördüğümüz kanıt:
- Seçim ve nedeni:
- Doğrulanmamış varsayım:
- Bir sonraki deneme ve bitiş koşulu:
```

Bir sonraki oturumun çıktısı: üç kısa fikir kartı ve ilk veri deneyinin kapsamı. İlk cevaplayacağımız soru: **Hangi kullanıcı grubunun yaşadığı kararsızlığı yakından biliyorsun ve bu hafta o gruptan kime ulaşabiliriz?**
