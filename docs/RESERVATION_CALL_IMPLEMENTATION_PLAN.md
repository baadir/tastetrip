# Rezervasyon araması entegrasyon planı

21 Ekim 2026. Planlama çıktısı; bu belgede önerilen servis seçimi veya sayısal limitler kullanıcı tarafından kabul edilmiş sayılmaz. Gerçek telefon araması, hesap oluşturma, numara satın alma veya deployment yapılmadı.

## Kesin kapsam ve yeni dil kararı

Kaynak: PRODUCT_REQUIREMENTS FR-03–FR-08, D-010 aksiyonda login, D-008 rotaya bağlı rezervasyon. Restoran seçimi telefon araması değildir. Giriş yapmış kullanıcı koşulları inceleyip açıkça “Aramayı başlat” der. Başlangıç uygulaması restoran masa rezervasyonu; otel/etkinlik oda-bilet işlem kanalları ayrı adaptörlerdir ve otomatik desteklenmiş sayılmaz.

D-016 kullanıcı kararı: görüşme dili restoranın ülkesine göre değişir; altyazı kullanıcının native/ana dilinde olur. `country_code`, `conversation_language`, `native_language` ve arayüz dili ayrı alanlardır. Ülke→dil eşlemesi varsayılandır, restoran personelinin dili için kanıt değildir. Çok dilli ülke/bilinmeyen ülke veya desteklenmeyen ses dili durumunda kullanıcıya açıklanır, seçim/düzeltme alınır. Restoran başka bir dil isterse desteklenen alternatifte geçiş yapılır ve kullanıcıya bildirilir; bilinmeyen dile körlemesine devam edilmez. Ülke bilinmeden şehir adından LLM ile kesin dil uydurulmaz. Ana dil kullanıcıdan alınır; browser veya UI dilinden kesin kabul edilmez. Ana dil ile görüşme dili aynıysa orijinal altyazı; farklıysa konuşmacı ayrımlı çeviri gösterilir.

## Güncel maliyet odaklı yön — D-018 / P-006

Kullanıcının 21 Ekim 2026 maliyet önceliğiyle ilk geliştirme önerisi: Twilio Media Streams + kendi CAX21 gateway/worker + Deepgram Nova-3 + DeepSeek + Amazon Polly Standard. Ayrıntılar ve fiyat varsayımları [VOICE_COST_COMPARISON.md](VOICE_COST_COMPARISON.md). Aşağıdaki Vapi hattı önceki P-005 önerisinin tarihsel kaydıdır; yeni yol için Vapi anahtarları istenmez. Gateway doğrudan Twilio medyasını işler; webhook/TwiML ve WebSocket doğrulaması Twilio yöntemleriyle uygulanır. Eski monitor ve Vapi kurulum maddeleri yeni hatta aynen uygulanmaz. Durum modeli, kullanıcı yetkisi ve özet kuralları korunur. Sağlayıcı kalite/latency testleri ve uygulama henüz yapılmadı.

## Önceki servis önerisi — P-005 (yerini P-006 aldı)

| Parça | Öneri / sorumluluk | Kabul kapısı |
| --- | --- | --- |
| Yer, kimlik ve telefon adayı | Mevcut Qloo entegrasyonu | Numara E.164 formatı, işletme eşleşmesi/kaynağı, ülke ve güncellik kontrolü; telefonun bulunması tek başına doğru hedef kanıtı değil |
| Görüşme orkestrasyonu | Vapi standart STT→LLM→TTS hattı | Outbound, tool sonuçları, transcript, gerçek çift taraflı dinleme testi |
| PSTN | Twilio numarası/bağlantısı | Hedef ülke/numara türü izinleri ve test numarası desteği |
| Konuşma sesi | ElevenLabs desteklenen voice/model | Seçilen dil ve telefon kalitesinde test; TTS tek başına arama yapmaz |
| Konuşma LLM’i | Vapi’nin desteklediği düşük gecikmeli model/adaptör | Mevcut DeepSeek rota modeli korunur; sesli agentta DeepSeek desteği ve gecikme ayrıca denenmeden varsayılmaz |
| Altyazı çevirisi | Sunucu tarafında mevcut DeepSeek adaptörüyle ilk deney | Final cümlelerin sırası, sayı/tarih/isim koruma ve gecikme ölçümü; gerekirse ayrı sağlayıcı |
| Canlı medya | Yetkili async voice-gateway | PCM formatı/kanallar/sample rate gerçek monitor akışından doğrulanır; iki taraf da duyulur |

Vapi seçimi henüz öneridir. GPT-Live özel yolunun mevcut dokümanındaki live-listen/voice kısıtları nedeniyle standart STT/LLM/TTS hattıyla başlanması önerilir; “Vapi destekliyor” demek her modelde aynı özellik var demek değildir. Alternatif LiveKit+SIP planı korunur; Vapi dinleme kapısı geçilmezse oraya dönülür. Şimdiki fiyat araştırması toplam gerçek arama maliyeti değildir; hedef ülke ve servis yapılandırmasıyla yeniden hesaplanır.

## Kullanıcı akışı

1. Rota kartı → Rezervasyon planla → gerekiyorsa giriş. Kullanıcıya ait plan/durak kimliği sunucuda çözülür.
2. Restoran adı/adresi, restoranın yerel tarihi/saati ve saat dilimi; kişi sayısı, rezervasyon adı, gerekiyorsa geri dönüş iletişimi, özel istekler, kabul edilebilir saat aralığı ve oturma alternatifleri toplanır.
3. Kullanıcının ana dili alınır/hatırlatılır; ülkeye göre seçilen görüşme dili düzenlenebilir biçimde gösterilir. Saat dilimi ülkenin tek saat dilimi olduğu varsayımıyla atanmaz; konumdan doğrulanır.
4. Özet ve numara kaynağı gösterilir; yalnız o özet/koşul sürümü için Aramayı başlat yetkisi alınır. Ses kaydı ile canlı dinleme ayrı konulardır; varsayılan öneri kalıcı ses kaydı kapalıdır, saklama kararı henüz verilmedi.
5. Aranıyor → bağlı. Kullanıcı “Canlı dinle” ile tarayıcı sesini açar; müşteri mikrofonu gerekmez. Agent ve restoran konuşmaları, orijinal metin + native dil çevirisi olarak ayrılır. Varsayılan müşteri yalnız dinleyicidir.
6. Agent, kullanıcı adına çalışan otomatik rezervasyon asistanı olduğunu ve görüşmenin müşteri tarafından canlı dinlenebildiğini anlaşılır biçimde belirtir; temsil yetkisinin dışına çıkmaz. Bilgilendirme metni hedef ülke/servis kurulumunda gözden geçirilir.
7. Restoran izin verilen saat/masa alternatifi sunarsa kapsam içinde ilerler. Kapsam dışı teklifte `needs_user_decision` kartı açılır: “20:30 yerine 21:15 uygun mu?” Kullanıcı yanıtı sunucudan doğrulanıp agent’a iletilir. Önerilen ilk davranış: yanıt gelmezse rezervasyonu kabul etmeden görüşmeyi kapatmak; timeout ve süre limiti ürün sahibiyle seçilecek.
8. Görüşme sonunda restoranın açık kabulü ve koşulların son okumasıyla sonuç çıkarılır. Onaylı sonuç gün/saat/kişi/ad/özel istekler ve verilen referansla rotaya bağlanır. Kaynak belirsizse “Sonuç belirsiz”; HTTP200 veya LLM özetinin “başarılı” demesi yeterli değil.

“Aramayı durdur” aramayı sonlandırır; daha önce verilmiş bir rezervasyonu iptal ettiğini iddia etmez. Yenileme veya tarayıcıdan ayrılma aramayı otomatik iptal etmez; geri gelince aynı girişim devam eder. Ses veya çeviri kesilmesi aramanın kesilmesinden ayrı görünür. Ana dil/görüşme dili değişince sıradaki altyazılar yeni dilde akar; eski kayıtlar sessizce yeniden yazılmaz.

## Sunucu yapısı ve Coolify

Mevcut Flask API/SQLite uygulaması korunur. Uzun ömürlü PCM/WebSocket bağlantıları 8 Gunicorn thread’ini tüketmemeli. Önerilen Compose genişlemesi:

- `web`: mevcut form/auth/rota + rezervasyon API’si ve webhook alıcısı.
- `voice-worker`: kalıcı outbox işlerini atomik claim ederek başlatır; sağlayıcı durum uzlaştırma ve altyazı çevirisini yürütür. Request thread’i içinde arama başlatıp bellek thread’ine emanet edilmez.
- `voice-gateway`: küçük async Python ASGI servis; monitor socket’ini sunucudan açar, yetkili kullanıcıya ses ve olay taşır. SQLite dosyasını doğrudan paylaşmak yerine web API’den kısa ömürlü, call-ID/scope/user bağlı token kontrolü yapar. Provider monitor/control URL ve anahtarları tarayıcıya gitmez.

İlk sürüm tek web/worker instance ve mevcut kalıcı SQLite volume; yeni tablolar aynı transactional DB’de. Gateway ses buffer’ı sınırlı/bellekte, kalıcı ses arşivi yok. Coolify’de aynı HTTPS domain altında API/WS path routing; wss proxy timeout ve reconnect testleri. Healthcheck’ler servis bazında. CAX21 native ARM64 imajlar; ilk eşzamanlılık önerisi 1 aktif arama, gerçek ölçümle artırılır. Web worker/gateway restart’ı devam eden çağrıya ikinci telefon açmaz. Sonraki ölçek artışında ortak PostgreSQL/queue değerlendirilecek; şu an geçilmiş sayılmaz.

## API sözleşmesi taslağı — henüz kod değil

| Uç | Görev |
| --- | --- |
| `POST /api/reservations/prepare` | Login, plan/durak sahipliği, telefon/dil/saat doğrulama; ücretli arama yapmadan özet/draft sürümü |
| `POST /api/reservations/{id}/start` | Onaylanan digest/sürüm + idempotency key ile kalıcı attempt/outbox |
| `GET /api/reservations/{id}` | Arama + rezervasyon + dinleme/çeviri durumları |
| `POST /api/reservations/{id}/listen-token` | Sahiplik ve aktif aramaya bağlı kısa ömürlü yalnız dinleme erişimi |
| `WS /voice/{attempt_id}` | Gateway üzerinden ses ve sıralı altyazı olayları; ilk mesaj/token doğrulaması ve Origin kontrolü |
| `POST /api/reservations/{id}/decision` | Bekleyen teklif ID/sürümüne kapsamlı kullanıcı yanıtı; eski teklif reddedilir |
| `POST /api/reservations/{id}/stop` | İdempotent stop; sonlandırma sonucu teyit edilir |
| `POST /api/webhooks/voice` | Sağlayıcının belgelenen credential/signature yöntemiyle doğrulanan olay; tarayıcı cookie/CSRF uçlarından ayrı |

Webhook secret/imza alanları seçilen Vapi yapılandırmasından doğrulanacak; desteklenmeyen bir HMAC standardı varsayılmaz. Çağrı/call ID, webhook credential ve olay içerikleri uygulamanın beklediği girişimle eşleştirilir. Monitor URL’leri yalnız onaylı sağlayıcı uçlarına bağlanabilir; keyfi hedefe socket/proxy açılmaz.

## Durum modeli ve kayıtlar

`reservation_requests`: owner, plan_id/revision, stop_id/entity_id, doğrulanmış numara kaynağı, ülke/tz, görüşme/native dil, koşullar, onay digest’i, sürüm.

`call_attempts`: request_id, provider_call_id (unique), attempt UUID/idempotency key (unique), call_state, result_state, start/end/reason, limitler.

`call_events`: event/delivery kimliği veya deterministik dedup anahtarı, attempt, sıra/timestamp, konuşmacı, partial/final, translation revision. Yeniden gelen/out-of-order olay son durumu geriye taşımaz.

`reservation_outbox`: atomik claim, lease, işlem türü, retry/reconciliation durumu. İşlem durumunu yalnız bellekte tutma.

Arama: queued → initiating → ringing → connected → ended / failed / unknown. Rezervasyon: pending → needs_user_decision → confirmed / declined / unknown / not_completed. Dinleme ve çeviri ayrıca healthy/degraded/disconnected. “Confirmed” maddi koşulların işletmeden kabul kanıtına bağlanır; boş/ref uydurulmaz.

Create-call isteği sunucudan çıktıktan sonra yanıt kaybolursa provider’ın arama başlatmadığı varsayılmaz. Önce attempt metadata/provider kayıtlarıyla uzlaştırma; bulunamazsa unknown ve insan değerlendirmesi. Sağlayıcı idempotency desteği belgelenmeden otomatik yeniden POST yok. Aynı rezervasyon için tek aktif attempt ve kesinleşmiş onaydan sonra yeni rezervasyon engeli; yeni gerçek arama açık kullanıcı kararıdır.

Onaylı rezervasyon saatini rota sabit durağına bağla. Rota yeniden oluşturulursa rezervasyon korunur; değişiklik/iptal ayrı akış ve yeni yetki gerektirir. Bir durağın reddi diğer onaylı durakları bozmaz.

## Görüşme sonrası kullanıcı özeti — D-017

Kullanıcı talimatı (21 Ekim 2026): rezervasyon görüşmesi bittikten sonra konuşmanın özeti kullanıcıya gösterilecek. Bu gereksinim plana eklenmiştir; telefon entegrasyonu ve özet üretimi henüz uygulanmadı.

Sonuç ekranı önce doğrulanmış rezervasyon durumunu, ardından kullanıcının ana dilinde kısa görüşme özetini gösterir:

- Restoran, yerel tarih/saat ve saat dilimi, kişi sayısı, rezervasyon adı; işletmenin verdiği referans varsa referans.
- Kullanıcının ne istediği ve restoranın ne yanıtladığı; görüşmede değişen saat/masa gibi koşullar ve kullanıcının bunları kabul edip etmediği.
- Kabul edilen, reddedilen ve teyit edilemeyen özel istekler ayrı; sessizlik kabul olarak yorumlanmaz.
- Açık kalan noktalar ve gerekiyorsa sonraki adım. Arama kesilmişse veya son teyit alınamamışsa bu sınırlama özetin içinde görünür olur.

Özet, konuşmacı kimliği ve final transcript olaylarına dayanarak sunucuda LLM ile üretilir. Kullanıcıya gösterilen çıktı ana dilde olur; çeviride belirsiz sayı/isim/tarih kesinleştirilmez. Her maddi koşul destekleyen transcript event/sıra kimliğine bağlanır. Koşullar backend’in doğrulanmış rezervasyon kaydıyla karşılaştırılır; çelişki varsa özet onay durumunu değiştirmez, teyit ihtiyacı gösterilir. Modelin “rezervasyon yapıldı” cümlesi tek başına `confirmed` yazamaz.

Özet ayrı durum taşır: hazırlanıyor / hazır / eksik konuşma verisi / oluşturulamadı. Özet başarısız olduğunda doğrulanmış sonuç alanları gösterilmeye devam eder; yalnız özet yeniden denenir, ikinci telefon araması başlatılmaz. Sonradan gelen final olaylarla özet yeni sürüm alabilir; görüşme/veri kesintisi ve güncelleme kullanıcıya görünür olur.

Veri modeli: `call_summaries` tablosunda attempt_id, transcript_revision, native_language, structured_facts, summary_text, evidence_event_ids, status, generated_at ve summary_revision. Kullanıcı sahipliği sonuç/özet okumasında da kontrol edilir. Özet, rezervasyon ayrıntıları altında kaydedilebilir ve sonraki ziyaretlerde aynı hesaptan açılabilir; transcript/özet saklama ve silme süreleri veri saklama kararıyla birlikte belirlenir. Özet gereksinimi kalıcı ses kaydı izni vermez.

API planına `GET /api/reservations/{id}/summary` ve yalnız yeniden üretim için `POST /api/reservations/{id}/summary/retry` eklenir. Worker arama bittikten sonra final transcript’i uzlaştırır ve özet işini idempotent biçimde üretir. UI kısa özeti varsayılan, mevcutsa konuşma detayını isteğe bağlı açar; uydurma tam transcript göstermez.

Kabul senaryoları: başarılı görüşme doğru koşullarla özetlenir; ret veya belirsizlik başarıya dönüştürülmez; karşılanamayan özel istek görünürdür; özet hatası rezervasyonu silmez; özet tekrar denemesi arama oluşturmaz; başka kullanıcı özete erişemez; ana dil çevirisinde yerel saat ve kişi sayısı korunur. Bunlar planlanan testlerdir, çalıştırılmış sonuçlar değildir.

## Agent yetki sınırı

Özel istek ve restoranın konuşması güvenilmeyen veridir; sistem talimatını değiştirmez. Agent yalnız rezervasyon görevi ve mevcut kullanıcı koşullarıyla konuşur. Kart bilgisi/ödeme/depozito sözleşmesi, ek ücret veya koşul dışı taahhüt vermez; kullanıcı kararına döner. `record_reservation_result`, `request_user_decision`, `end_call` gibi dar araçlar; backend koşul/kimlik/sürüm kontrol eder. Kapsam dışı ödeme kabulü agent kararıyla yapılmaz. Sesli LLM’nin serbest metin özeti tek başına rezervasyon durumunu commit etmez.

## Uygulama sırası ve teslim kapıları

1. **Rezervasyon çekirdeği:** form, prepare/start/stop sözleşmeleri, DB/outbox, idempotency ve sahiplik. Fake adapter açık “simülasyon” işaretli; arama yok. Çift tık, restart ve stale-plan testleri.
2. **Kontrollü gerçek telefon:** Vapi/Twilio kurulumu, desteklenen hedef numara allowlist’i, küçük süre/bütçe limiti; bize ait/izinli karşı uçla konuşma. Ülkeye göre dil seçimi ve native dil alınır. Önce provider anahtar/numara yetkileri gerekir; gerçek restorana otomatik test araması yapılmaz.
3. **Canlı dinleme + altyazı:** iki taraf ses, kullanıcı tıklamasıyla playback, partial/final ve kesilen konuşma, sıralı çeviri, WS yeniden bağlanma ve yetkisiz kullanıcı testi. Doküman varlığı test yerine geçmez. Konuşma/çeviri gecikmesi ölçülür; sayısal kabul eşiği ürün sahibiyle belirlenir.
4. **Rezervasyon ve kullanıcı kararı:** kabul/ret, saat dolu, izinli ve izinsiz alternatif, webhook tekrar/sıra bozukluğu, telefon açılmaması, bağlantı kaybı sonrası unknown. Agent sonucu ve koşulları son kez karşı tarafa okur.
5. **Coolify kontrollü pilot:** HTTPS webhook/gateway, volume/backup/restart, çağrı limiti ve maliyet görünürlüğü. Gerçek restoran araması ancak doğru hedef/koşul için kullanıcının uygulamadaki başlatma kararıyla.

## Entegrasyondan önce gereken bilgiler

Ürün sahibi: ilk hedef ülke kümesi, kullanıcı ana dil alanı, çok dilli ülkelerde default/override politikası; max süre, eşzamanlı arama, günlük bütçe ve kullanıcı yanıt timeout’u; ses/transcript saklama tercihi. Sağlayıcı seçimi hâlâ öneridir.

Servis kurulumu: Vapi private key/assistant/phone-number ID ve webhook credential; Twilio PSTN bağlantısı; ElevenLabs voice/dil modeli. Bunlar Coolify runtime secrets olur; bu plan anahtar istemek veya mevcut anahtarları dışarı göndermek değildir. Rota DeepSeek anahtarı sesli model seçimini otomatik belirlemez. Bu aşamada yalnız plan tamamlandı; uygulama/voice test sonucu yok.

## Resmi teknik kaynaklar

- [Vapi Live Call Control / Listen](https://docs.vapi.ai/calls/call-features)
- [Vapi Server Events](https://docs.vapi.ai/server-url/events)
- [Vapi GPT-Live compatibility](https://docs.vapi.ai/gpt-live/configuration) — live monitor ve ses sağlayıcı kısıtlarını standart hatla karıştırma.
- [ElevenLabs Twilio outbound](https://elevenlabs.io/docs/conversational-ai/guides/twilio/outbound-calling) — alternatif agent yolu; ek müşteri canlı dinleyici kapsamı ayrıca doğrulanmalı.

Kaynaklar 21 Ekim 2026 tarihinde kontrol edildi. Önceki fiyat/sağlayıcı araştırması docs/TELEPHONY_RESEARCH.md içinde tarihsel korunur.

## D-031 / H-069 — 22 Ekim uygulama güncellemesi
Ürün restoran rezervasyonu çekirdeği, durable worker, dinleme/altyazı/özet köprüsü ve rota ekranları eklendi. Güncel kaynak docs/RESERVATION_IMPLEMENTATION.md. Bu belgenin eski Vapi/Polly önerileri tarihsel; güncel hat Twilio/Deepgram/DeepSeek/ElevenLabs Anna. İlk sürüm sabit koşullarla arar; alternatif teklif karar kartı henüz yok. Dar otomatik kabul kanıtı veya kullanıcı incelemesi olmadan confirmed yazılmaz. Bu tur gerçek arama veya deploy yapılmadı; bütün kabul kriterleri kapandı sayılmaz.
