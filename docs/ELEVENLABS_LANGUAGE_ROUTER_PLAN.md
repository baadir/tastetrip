# ElevenLabs dil bazlı TTS router planı

22 Ekim 2026. Kullanıcı kararı D-028; **plan**, çalışan router uygulaması değil. Ana ses Anna (D-027); yalnız model seçimi değişir.

## Seçim kuralı

1. Girdi `conversation_language`: restoran ülkesinden elde edilen, kullanıcı tarafından düzeltilebilir görüşme dili. Altyazı/native/UI dili seçim kaynağı değildir (D-016).
2. BCP47 kodu normalize edilir: `en-US`→`en`, `tr-TR`→`tr`; bölge/aksan bilgisi ayrı korunur. İsimlerden serbest LLM tahminiyle dil kodu uydurulmaz. Desteklenmeyen/ambiguous kodlar açık hata verir.
3. Dil Flash v2.5 destek kümesindeyse `eleven_flash_v2_5`.
4. Flash desteklemiyor, v3 destekliyorsa `eleven_v3`.
5. İkisinde de yoksa ücretli telefon araması başlamadan durdur; otomatik İngilizceye geçme. Kullanıcı desteklenen görüşme dili seçebilir.

Bu dil desteği fallback'idir;401/402/kota/ağ hatası geldiğinde körlemesine v3'e geçiş yapılmaz. Maliyet veya hata nedeniyle model/dil değişimi sessizce yapılmaz. Model seçimi mümkünse çağrı boyunca sabitlenir; personelin dil değişikliği isteğinde destek kontrolü tekrar yapılır ve kullanıcı bilgilendirilir.

## Canlı API'den doğrulanan destek matrisi

Resmî `GET /v1/models`22Ekim2026 kontrolü. Dil listesi kodda elle tahmin edilmez; sürümlü snapshot ve son başarılı güncelleme zamanı tutulacak. Başlangıç/periyodik yenileme önerisi24saat; çağrının sıcak yolunda keşif isteği yok. Güncelleme başarısızsa son doğrulanmış snapshot kullanılabilir; snapshot yoksa arama durdurulur. Otomatik keşif yeni modelleri politikaya eklemez, yalnız bu iki modelin dil desteğini günceller.

### eleven_v3

`af, ar, as, az, be, bg, bn, bs, ca, ceb, cs, cy, da, de, el, en, es, et, fa, fi, fil, fr, ga, gl, gu, ha, he, hi, hr, hu, hy, id, is, it, ja, jv, ka, kk, kn, ko, ky, lb, ln, lt, lv, mk, ml, mr, ms, ne, nl, no, ny, pa, pl, ps, pt, ro, ru, sd, sk, sl, so, sr, sv, sw, ta, te, th, tr, uk, ur, vi, zh`

### eleven_flash_v2_5

`ar, bg, cs, da, de, el, en, es, fi, fil, fr, hi, hr, hu, id, it, ja, ko, ms, nl, no, pl, pt, ro, ru, sk, sv, ta, tr, uk, vi, zh`


| Örnek | Seçilecek model |
| --- | --- |
| Türkçe, İngilizce, Arapça, Japonca | Flash v2.5 |
| Afrikaans | v3 |
| İkisinde de bulunmayan dil | Arama öncesi hata |

## Bütün ses akışına uygulanması

Planlanan `app/voice_routing.py` saf `resolve_tts(language, capabilities)` sonucu: normalized language, model_id, Anna voice_id, seçim nedeni, snapshot sürümü. Açılış, normal yanıt, dijital asistan açıklaması, sessizlik teyidi ve kapanış aynı seçimi kullanır. `voice_agent.py` sabit model_id yerine bu sonucu tüketir; sunucu istemciden keyfi model/voice ID kabul etmez. Genel Anna env alanı ana kaynak olacak; eski TR/EN alanları uyumluluk için korunabilir, farklı dil için Anna yerine başka sese sessiz geçiş yok.

Arama koşulu/attempt kaydında dil/model/voice/snapshot sürümü sabitlenir; istemci yalnız okunur dil ve seçilen modeli görür. Mevcut iki demo sabit tr/en olduğundan her ikisi Flash seçer. Router eklenmesi demo senaryolarını otomatik çok dilli hale getirmez; prompt, STT ve sabit teyit metinleri de görüşme diline uygun olmalıdır.

## Arama öncesi kabul kapısı

TTS dil desteği **uçtan uca telefon desteği değildir**. Deepgram STT dil/model desteği, Anna'nın seçilen modelde erişimi/kalitesi, DeepSeek'in görüşme dili ve bu dilde teyit metni de kontrol edilir. Afrikaans örneğinin WAV üretimi başarılı; mevcut Nova-3 telefon STT'sinde Afrikaans'ın çalıştığı doğrulanmadı. Bu kapı geçilmeden sırf v3 Afrikaans konuşabiliyor diye Afrikaans araması açılmaz.

Twilio çıkışı raw8kHz mono mu-law/base64 kalır. v3 için aynı streaming uç/ulaw8000/model ayarları gerçek kısa ses üretimiyle doğrulanacak; önceki v3 PCM WAV testi bu kapıyı karşılamaz. v3 gecikmesi ve söz kesme davranışı ölçülecek;10sn sessizlik kuralı provider gecikmesiyle yanlış kapanma oluşturmamalı. Bu kullanıcı sessizlik kararını değiştirmez; implementasyonda ölçüm ve ayrı provider-timeout durumu gerekir.

## Uygulama sırası ve testler

1. Sürümlü dil yetenek snapshotı + saf router; tr/en/ar/ja→Flash,af→v3,unsupported hata testleri. en-US normalizasyonu, bilinmeyen kod, bozuk/eksik snapshot ve provider hata sınıfları.
2. Çağrı öncesi STT/TTS/voice/temel metin yetenek doğrulaması; koşul kaydı ve seçimi bütün TTS noktalarına taşıma. İdempotency korunur; model değişikliği ikinci çağrı yaratmaz.
3. İki modelde Anna kısa ses üretimi, telephony formatı/mark/clear/sessizlik kontrolü. En az bir Flash dışı dilde STT+LLM hattı kanıtı olmadan üretim hazır sayma.
4. Yerel ön yüzde görüşme dili/model gösterimi ve desteklenmeyen dil açıklaması. Sonra izinli test numarasıyla kontrollü telefon testi; gerçek restoranı otomatik test etme.

## Maliyet ve durum

Flash API temel kredi tüketimi v3'ün yaklaşık yarısı; plan/sese göre çarpanlar ayrıca doğrulanır. Router seçimi dil ve maliyet gerekçesiyle izlenebilir olacak, token/ham konuşma loglanmayacak.

Bu tur kod, env, çalışan servis veya demo hedefi değiştirilmedi; arama yapılmadı. Yukarıdaki testler planlanan kabul kontrolleridir, çalıştırılmış testler değildir.

Kaynaklar:
- https://elevenlabs.io/docs/api-reference/text-to-speech/stream
- https://elevenlabs.io/docs/overview/models
- https://api.elevenlabs.io/v1/models (kimlik doğrulamalı dil metadata kaynağı; anahtar belgede yok)

## 22 Ekim — Ürün rezervasyon yolunda uygulama
Dil router'ı app/voice_languages.py, app/voice_models.json ve reservation worker/agent entegrasyonunda uygulandı. Flash destek kümesi, aksi halde v3; Nova-3 uygunluğu da kontrol edilir. Ürün görüşmesi için model, onaylı koşullarla sabitlenir ve worker canlı model listesiyle arama öncesi doğrular. Snapshot 22 Ekim tarihli; otomatik periyodik snapshot yenilemesi henüz yok. Önceki planın 24 saat yenileme önerisi tamamlandı sayılmaz. Eski sabit demo ses yolu Flash olarak korunur. Flash/TR ve v3/Afrikaans μ-law streaming küçük API örnekleri başarılı; tam telefon testi değildir. Güncel kapsam RESERVATION_IMPLEMENTATION.md.
