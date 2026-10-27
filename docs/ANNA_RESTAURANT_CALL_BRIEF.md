# Anna ile planlanan restoran rezervasyonu araması

Kayıt tarihi: 21 Ekim 2026 (Europe/Istanbul).
Durum: Kullanıcının sonraki arama için verdiği bilgiler kaydedildi. Arama yapılmadı; rezervasyon oluşturulmadı.

## Kullanıcının verdiği bilgiler

- Restoran telefon numarası: **+18185570881**.
- Google Maps bağlantısı: https://maps.app.goo.gl/CWum5kNZRtR4kd6T7
- Rezervasyon adı: **Philip** (bu yazımla).
- Kişi sayısı: **3**.
- Görüşme sesi: **Anna — Conversational, Helpful**.
- ElevenLabs Voice ID: `XZXyuzPdidXaSa10PmVA`.
- Görüşme dili: İngilizce (D-021 Anna seçimi ve bu arama bağlamı).
- Açılışta Philip adına arayan yapay zekâ destekli dijital asistan olduğu açıkça belirtilir (D-022).

## Aramadan önce tamamlanacaklar

- Rezervasyon tarihi, restoranın yerel saati ve saat dilimi henüz bu arama için verilmedi. Önceki kişisel Dilara demosundaki22Ekim19:00 bu restorana otomatik taşınmaz.
- Restoran adı, Maps kaydı ile telefon eşleşmesi, çalışma saatleri ve rezervasyon kabulü henüz bağımsız doğrulanmadı. Yukarıdaki telefon ve bağlantı kullanıcı kaynaklıdır.
- Alternatif saatler, özel istekler, gerekli geri dönüş iletişimi ve konuşma/altyazı dili ayrıntıları henüz belirtilmedi.
- Mevcut yerel demo Türkçe/Dilara ve kişisel test numarasına bağlıdır. Anna/İngilizce, Philip ve bu restoranın koşullarıyla çalışan akışa henüz geçirilmedi.

## İşlem sınırı

Kullanıcı bu tur bilgilerin kaydedilmesini ve daha sonra arama yapılmasını istedi. Bu kayıt otomatik arama planlamaz; zamanlanmış görev kurulmadı. Mevcut `TWILIO_TEST_TO_NUMBER`, arama düğmesinin hedefi veya çalışan demo promptu değiştirilmedi. Gerçek restorana yapılacak arama için eksik koşullar tamamlanıp kullanıcı başlangıcıyla ilerlenir. Sonuç ancak restoranın açık kabulüyle onaylı sayılır.


## 21 Ekim güncellemesi — D-023 / H-057

Kullanıcı tarih/saat verdi: **yarın22Ekim2026 Perşembe13:00**, restoranın Burbank/Los Angeles yerel saati (`America/Los_Angeles`). Philip/3kişi/Anna/İngilizce korunur. Önceki tarih/saat eksik kaydı bu güncellemeyle tamamlandı; eski not tarihsel.

Telefon eşleşmesi resmî işletme kaynağında görüldü: https://beer.bjsrestaurants.com/Default.aspx?id=11522 (BJ's Burbank,107 South1st Street,8185570881). Yerel turizm kaynağı da aynı şubeyi gösteriyor: https://visitburbank.com/dining-and-nightlife/restaurants/bjs-restaurant-and-brew-house/ . Maps kısa bağlantısı web aracında açılamadı; Maps sayfasının içeriği doğrulanmış sayılmaz.

Ayrı Anna ile restoranı ara düğmesi eklendi; kişisel Türkçe test düğmesi korunur. Tetikleme canlı dinleme bağlantısından sonra kullanıcı tarafından yapılır. Anna kimliğini AI digital assistant olarak açıklar, doğru işletmeyi sorar;22Ekim1PM/3kişiyi değiştirmez. Kullanıcı talebi doğrultusunda restoran açık rezervasyon onayı verdikten sonra deney açıklaması ve özür; ayrıca gerçek masa tutulmaması için iptal ve açık iptal teyidi istenir. Bu davranış LLM promptunda tanımlı, henüz gerçek görüşmeyle doğrulanmadı; otomatik rezervasyon/iptal garantisi değildir. Ödeme/kapora veya eksik iletişim bilgisi uydurma yok. Görüşme sonlanırsa iptal belirsiz kalabilir ve telefon completed durumu rezervasyonun iptali sayılmaz.

48 test geçti. Anna metadata erişimi önceki turda doğrulandı; bu tur Anna ses üretimi veya gerçek restoran araması yapılmadı. Mevcut180sn çağrı sınırı ve SQLite idempotency/unknown bloklaması iki düğme için ortaktır.


## Aktif hedef değişikliği — D-024 (21 Ekim 2026)

Burbank kaydı tarihsel; aktif Anna düğmesi artık **Botanical / Dublin One Hotel, Dublin** için:
- Telefon: **+35315567170** (otel genel hattı; restoran masa rezervasyonlarına bağlanma istenir).
- Kullanıcı Maps bağlantısı: https://maps.app.goo.gl/Lr76mWnrGy6GiADi8
- Philip,3kişi, **22Ekim2026 13:00 Europe/Dublin**.
- İngilizce/Anna, AI kimlik açıklaması, deney sonrası özür ve test rezervasyonunu iptal ettirme/teyit isteme korunur.
- Resmî telefon/adres kaynağı: https://dublinonehotel.com/find-us/ . Maps kısa link içeriği doğrulanmadı.
- Arama henüz yapılmadı. Burbank numarası artık aktif düğmenin hedefi değildir.


## Aktif hedef değişikliği — D-025 (21 Ekim2026)

Kullanıcı yeni hedef verdi ve deneme istedi. Aktif düğme **The Goat Bar & Grill, Goatstown, Dublin**:
- +35312984145
- https://maps.app.goo.gl/mVNF9utFz7KEWRXE8
- Philip/3kişi/22Ekim2026 13:00 Europe/Dublin; Anna İngilizce.
- Telefon doğrulama kaynağı: https://www.claytonhotels.com/hotel-near/the-goat-bar-grill-dublin/
- Önceki Botanical hedefi tarihsel. Telefon rezervasyonu kabul edilmiyorsa doğru kanalı bir kez sorma ve tekrar etmeden kapatma talimatı eklendi. Deney açıklaması/özür ve iptal teyidi isteme kuralı korunur.
