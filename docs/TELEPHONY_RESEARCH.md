# TasteTrip — Telefon altyapısı araştırması

Tarih: 21 Ekim 2026. Durum: Doküman temelli araştırma ve öneri; sağlayıcı seçilmedi, hesap açılmadı, gerçek arama/test yapılmadı.

## Kapsam

D-001 ve PRODUCT_REQUIREMENTS.md FR-04–FR-08: Restoranın gerçek numarasını arayan agent, web sitesinden iki tarafı canlı dinleme, konuşmacı ayrımlı Türkçe altyazı, doğrulanmış rezervasyon sonucu. İlk hedef ülke ve dil hâlâ açık. Fiziksel telefon/SIM cihazı gerekmez; PSTN erişimi olan bulut telefon servisi kullanılabilir.

## Seçenekler

| Yol | Görev | Fiyatın kapsamı | Değerlendirme |
| --- | --- | --- | --- |
| Vapi + Twilio + ElevenLabs sesi | Yönetilen agent, operatör ve TTS | Vapi $0.05/dk; STT, LLM, TTS ve telefon ayrıca | İlk prototip önerisi; live listen ve transcript olayları mevcut |
| ElevenAgents + Twilio | ElevenLabs yönetilen konuşma agentı | Creator $22/ay, 275 dk; ek dk $0.08; LLM ve telefon ayrıca | Ses/agent kurulumu kolay; ikinci kullanıcının aktif telefon görüşmesini dinlemesi ayrıca doğrulanmalı |
| Retell + operatör | Yönetilen telefon agentı | Yayınlanan AI aralığı $0.07–0.31/dk; model/ses/telefon seçimine göre değişir | Alternatif; canlı dinleyici akışı bu araştırmada doğrulanmadı |
| LiveKit Agents + SIP operatörü + STT/LLM/TTS | Oda ve medya mimarisi üzerinde kontrol | Agent oturumu liste örneği $0.01/dk; SIP/WebRTC/veri/AI/operatör ve plan ayrıca | Canlı dinleme için uygun mimari; daha fazla geliştirme işi |
| Doğrudan Twilio Media Streams + özel agent | Ham ses üzerinden kendi akışımız | Telefon + Media Streams $0.0044/dk + AI + sunucu | En fazla mühendislik; çift yönlü stream yalnız inbound ses verir, agent sesi kendi çıkışımızdan eşlenmeli |

Bu fiyatlar farklı kapsamlardadır; toplam fiyatmış gibi karşılaştırılmamalı. Tüm tutarlar USD; vergi ve kur dönüşümü dahil değil.

## Entegrasyon önerisi — Vapi tabanlı ilk prototip

1. Web sitesi rezervasyon özetini backend'e POST eder. Restoran telefonu istemciden güvenilir veri kabul edilmez; sunucu seçilen restoran kaydıyla eşleştirir.
2. Backend benzersiz girişim kimliği üretir; çift tıklama/yeniden istek ikinci arama başlatmaz. Tarih, restoran yerel saati, kişi sayısı, isim, izin verilen alternatifler ve görüşme dili agent bağlamına eklenir.
3. Backend Vapi POST /call ile assistantId, phoneNumberId ve customer.number gönderir. Twilio bağlantısı gerçek telefon şebekesini sağlar. Anahtarlar yalnız sunucudadır.
4. API'deki monitor.listenUrl canlı ses kaynağıdır. Yetkili kullanıcı için sunucu üzerinden erişim sınırlandırılır; PCM ses tarayıcıya uygun biçimde tamponlanıp oynatılır. İki tarafın gerçekten duyulduğu ve ses formatı kontrollü telefon testiyle doğrulanır.
5. Vapi transcript ve assistant.speechStarted olayları backend'e gelir; konuşmacı ve sıra kimliği korunarak çeviri katmanına, ardından SSE/WebSocket ile web sitesine gönderilir. Agentın taslak metni duyulmuş konuşma diye gösterilmez; kesilen sözler ve partial/final düzeltmeleri ele alınır.
6. Backend arama durumu ve rezervasyon sonucunu ayrı tutar. Telefonun açılması ya da HTTP başarısı rezervasyon onayı değildir. Restoranın açık kabulü ve son koşullar gerekir.
7. Arama süresi/yeniden deneme sınırı, webhook doğrulaması, dinleyici yetkisi ve hata durumları eklenir. Kontrol dışı alternatifte müşteriden karar alınır.

Örnek uygulama uçları (öneri, mevcut kod değil): POST /api/reservation-calls; POST /api/webhooks/voice; GET /api/reservation-calls/:id/events; yetkili canlı ses bağlantısı; POST /api/reservation-calls/:id/stop.

LiveKit alternatifi: SIP katılımcısı restoranı odaya bağlar, agent ayrı katılımcıdır, web kullanıcısı canSubscribe=true/canPublish=false token ile iki ses kanalını dinler. Altyazı yine ayrıca çevrilip iletilir. Sürekli medya bağlantısı için yönetilen servis veya uzun süre çalışan worker gerekir.

## Telefon tarifeleri ve hesap

Twilio Programmable Voice yayınlanan dakika tarifeleri:

| Hedef | USD/dk | 3 dk telefon bedeli |
| --- | ---: | ---: |
| ABD yerel | 0.0140 | 0.0420 |
| Hindistan sabit | 0.0699 | 0.2097 |
| Hindistan mobil | 0.0496 | 0.1488 |
| Türkiye sabit | 0.0701 | 0.2103 |
| Türkiye mobil | 0.2875 | 0.8625 |

Bunlar yalnız telefon bedelleri; SIP trunk tarife teklifi yerine kullanılmaz. Hedef numara öneki, rota ve faturalama yuvarlaması nihai tutarı etkiler. Yerel numara satın alma uygunluğu, o ülkeye arama yapabilmekten ayrı konudur.

Örnek Vapi bütçe varsayımı: platform $0.05 + STT/LLM/TTS için ölçülmemiş $0.05–0.15 = telefon öncesi $0.10–0.20/dk. Bu AI aralığı sağlayıcı fiyat teklifi değildir. 3 dakikalık görüşmede ABD toplamı yaklaşık $0.34–0.64, Hindistan sabit $0.51–0.81, Türkiye sabit $0.51–0.81, Türkiye mobil $1.16–1.46 olur. 1.000 görüşmede aynı rakamların 1.000 katı. Buna ayrıca çeviri, canlı yayın/proxy, hosting, numara kirası, vergi ve başarısız/tekrar aramalar eklenir.

Başarılı rezervasyon maliyeti = bütün girişimlerin toplam maliyeti / doğrulanmış rezervasyon adedi. Görüşme maliyeti başarı maliyeti değildir.

## Doğrulama gerektirenler

- İlk ülke, arama dili ve numara türü; operatörün hesap/ülke izinleri, uygun caller ID ve numara koşulları.
- Trial hesapların doğrulanmamış restoran numaralarını arama sınırlamaları; ücretli hesap gereksinimi.
- İki tarafın canlı sesi, mobil tarayıcı oynatması, konuşmacı ayrımı, Türkçe çeviri gecikmesi.
- Söz kesme, gürültü, bekletme müziği, IVR/DTMF, hat kopması ve alternatif saatler.
- Agent/aktif dinleyici bilgilendirmesi ve hedef ülkenin geçerli koşulları. Kalıcı kayıt ayrı ürün kararı; araştırma kayıt tutulmasını onaylamaz.

## Resmi kaynaklar

- https://vapi.ai/pricing
- https://docs.vapi.ai/calls/call-features
- https://docs.vapi.ai/server-url/events
- https://elevenlabs.io/pricing/agents
- https://elevenlabs.io/docs/eleven-agents/api-reference/twilio/outbound-call
- https://www.retellai.com/pricing
- https://livekit.com/pricing
- https://docs.livekit.io/telephony/making-calls/outbound-calls/
- https://docs.livekit.io/frontends/reference/tokens-grants/
- https://www.twilio.com/docs/voice/media-streams
- https://www.twilio.com/en-us/voice/pricing/us
- https://www.twilio.com/en-us/voice/pricing/in
- https://www.twilio.com/en-us/voice/pricing/tr
- https://www.twilio.com/docs/voice/api/dialing-permissions-resources
- https://help.twilio.com/hc/en-us/articles/360036052753-Twilio-Free-Trial-Limitations
