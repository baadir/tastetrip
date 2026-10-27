# Yerel telefon sesi denemesi

21 Ekim 2026. Bu servis STT geliştirme prototipidir; rezervasyon agentı, LLM yanıtı, canlı kullanıcı dinleyicisi veya özet üretimi değildir.

## Hazır yapı

- `app/voice_gateway.py`: ayrı aiohttp servisi, yalnız127.0.0.1:8081 üzerinde. Ana Flask uygulaması8080 tünele açılmadı.
- Cloudflare Quick Tunnel yalnız8081'e bağlı; geçici URL `.env` VOICE_PUBLIC_URL içinde. URL tünel yeniden başladığında değişir; `.env` güncellenip gateway yeniden başlatılmalı.
- Deepgram Nova-3, açık Türkçe `tr`, mulaw8000Hz mono. Dil ilk teknik test için sabit; ürünün ülke/native dil kararı değiştirilmedi.
- Twilio X-Twilio-Signature, yapılandırılmış HTTPS originden türetilen public WSS URL ile doğrulanır; Host/X-Forwarded-Host imza kaynağı yapılmaz. Başlangıç accountSid ve medya formatı kontrol edilir. Bir aktif stream,60sn üst sınır.
- Dışarıya açık arama başlatma ucu yok. Sağlayıcı anahtarları tarayıcıya verilmez. Ses kaydı yok. Son100 transcript olayı yalnız bellekte; yeni akışta ve process kapanınca silinir. Diskte transcript/ses arşivi yok.
- `/internal/transcript` Bearer VOICE_MONITOR_TOKEN gerektirir; token `.env` içinde. `/health` yalnız ok durumu verir. Erişim logları kapalı.

## Başlatma

```powershell
.venv/Scripts/python.exe -m app.voice_gateway
./data/tools/cloudflared-windows-amd64.exe tunnel --url http://127.0.0.1:8081 --no-autoupdate --logfile data/voice-tunnel.log
```

Cloudflared resmi cloudflare/cloudflared GitHub sürümü2026.10.3, data/tools altında (Git ignore). Sistem servisi kurulmadı. Terminal processleri kapanınca tünel/servis durur; üretim veya Coolify deploy değildir.

## Doğrulananlar

-27 unittest başarılı;5 yeni kontrol health, transcript tokenı, imzasız medya reddi, spoofed host reddi, yanlış Twilio hesabının Deepgram açılmadan reddi.
- Geçici public HTTPS `/health`200; yetkisiz transcript ve media403.
- Yerel test istemcisi Twilio imzasıyla public WSS handshake/start gönderdi; Deepgram bağlantısı açıldı, stop ile normal1000 kapandı. Bu gerçek Twilio çağrısı değildir; ses frame'i gönderilmedi.

## Sonraki test

İzinli telefon aramasına kısa Türkçe bilgilendirme sonrası `<Connect><Stream url="wss://.../twilio/media"/></Connect>` eklenerek gerçek medya gönderilecek. Hedef açıkça seçilmeli; arama POST'u otomatik tekrar edilmemeli ve çağrı süresi ayrıca sınırlandırılmalı. Bu hazırlıkta yeni telefon araması yapılmadı. Konuşmayı doğru yazıya çevirdiği ancak gerçek test ve kullanıcı teyidiyle söylenebilir.

Kaynaklar:
- https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/
- https://www.twilio.com/docs/voice/media-streams
- https://www.twilio.com/docs/voice/media-streams/websocket-messages
- https://developers.deepgram.com/reference/speech-to-text/listen-streaming


## 21 Ekim bağlantı hatası düzeltmesi — H-045

Önceki sentetik kontrol HTTPS imzasını ürettiği için gerçek Twilio WSS handshake davranışını temsil etmiyordu. İki telefon testindeki31920/imza reddi bununla uyumlu. Media Streams imzası public `wss://` URL ve belgelenmiş trailing-slash varyantına göre doğrulanacak şekilde düzeltildi. Host/forwarded header hiçbir zaman güvenilir origin yerine kullanılmaz; HTTPS imzası artık WSS uçta reddedilir.

30 test geçti. Telefon araması yapmadan public tünel üzerinden WSS imzalı25 adet20ms mu-law sessizlik frame'i gerçek Deepgram bağlantısına gönderildi;25 frame,0 imza reddi, normal1000 kapanış/ended görüldü. Bu0.5sn sentetik sessizlik testidir; Türkçe konuşma doğruluğunu veya gerçek Twilio'nun artık başarılı bağlandığını henüz kanıtlamaz. Yeni telefon araması yapılmadı.

Kaynak: https://github.com/openai/openai-agents-python/blob/main/examples/realtime/twilio/README.md (WSS imza URL açıklaması) ve Twilio security belgesi.


## Dilara + DeepSeek konuşma denemesi

`start.customParameters.mode=restaurant_demo` olan imzalı Twilio stream için `app/voice_agent.py` etkinleşir. Diğer streamler STT testi olarak kalır. Türkçe Dilara/Flashv2.5 ulaw8000 kullanılır; İngilizce Anna seçimi kaydedilmiş olsa da bu demo dil değiştirmez. DeepSeek mevcut env modelinde thinking disabled; tek kısa yanıt, sınırlı geçmiş/sıra ve provider timeout. Ayrı worker gerçek ürün outbox entegrasyonu değildir.

Bu **21 Ekim 2026 tarihli test senaryosu**,22Ekim2026 19:00/3kişi için masa sorar. Tarih prompt içinde bu deneme için sabittir; sonraki gerçek rezervasyonlarda parametreli koşul sürümü gerekir. Rezervasyon adı verilmediğinde uydurmaz, ödeme yapmaz, gerçek rezervasyon kaydı üretmez.

Twilio media gönderiminde raw mu-law8kHz/base64; mark teyidi tamamlanmadan assistant metni tamamlanmış sayılmaz. Karşı tarafın en az2 kelimelik ara metni ses sırasında gelirse mevcut ses görevi iptal edilip clear gönderilir. Bu ilk söz kesme yaklaşımı gerçek görüşmede kalite/gecikme açısından değerlendirilmeli; tam duplex üretim kabul testi değildir.34 test: önceki30 + final fragment birleştirme, interim cevabı engelleme, iptal/clear, mark eşleştirmesi.

Yeni dosya diske ses veya transcript yazmaz; son olaylar geçici bellektedir. Görüşme sonrası native özet, kullanıcı canlı dinleyicisi, rota rezervasyon UI ve provider idempotent outbox henüz uygulanmadı.


## Yerel canlı dinleme ekranı

http://localhost:8081/monitor adresinde Canlı dinle seçilir. Bir telefon görüşmesi başlatmaz; sonraki streami dinler. Sesi kapat yalnız sesi, Dinlemeyi bitir yalnız tarayıcı bağlantısını kapatır. Görüşme ve dinleyici bağlantısı ayrı durumlardır. Bağlantı koparsa kullanıcı yeniden bağlanabilir; geçmiş ses yeniden çalınmaz. Mikrofon kullanılmaz. Metin otomatik ve hatalı olabilir; rezervasyon onayı değildir.

`voice_monitor.py` sadece loopback+yerel Host ve proxy header yokluğunda sayfa/ticket verir;30sn tek kullanımlık token WS ilk mesajında, local Origin kontrolü. Provider anahtarları ve uzun ömürlü monitor secret frontend'e gitmez.4 dinleyici;80 paket buffer; yavaş dinleyicide eski paketler atılır ve gap bildirilir. Kamuya açık tünel /monitor girişini reddeder; yalnız Twilio media imzalı uç erişilebilir. Bu yerel test ekranıdır, üretim kullanıcı/çağrı sahipliği yerine kullanılamaz.

Türkçe restoran sesi ve agenta gönderilen Dilara sesi tarayıcıda mu-law8kHz olarak çözülür; mark onaylı assistant metin gösterilir. Geçici/söz kesilmiş sesle telefon playback'inin tam eşleşmesi henüz ürün düzeyinde doğrulanmadı. Demo tarih/kişi bilgileri önceki test koşullarını gösterir, genel rezervasyon editörü değildir.39 test geçti; gerçek telefonla canlı dinleme ayrıca test edilmeli.


## Ön yüzden arama başlatma — H-055

Önce Canlı dinle, sonra Test aramasını başlat. Düğme yalnız env `TWILIO_TEST_TO_NUMBER` hedefine3dk sınırlı Dilara+DeepSeek demo çağrısı gönderir. Numara browser'a taşınmaz/değiştirilemez. `POST /monitor-call` sadece localhost+Origin kontrolüyle ve idempotent girişim kimliğiyle kabul edilir. `GET /monitor-call` sağlayıcı durumunu uzlaştırır. Arama hazırlık/çalıyor/görüşmede/tamamlandı/reddedildi/unknown ayrı gösterilir. Unknown yeni aramayı engeller; Twilio loglarıyla manuel uzlaştırma gerekir, kör retry yapılmaz. Sayfa yenilemek aramayı iptal etmez veya tekrarlamaz.

Girişimler `data/voice-demo.sqlite3` içinde provider SID/status ile kalıcıdır; hedef numara veya transcript içermez. İstek kopsa bile oluşturma görevi process yaşarken sürer; process çöküşünde starting/unknown bloklaması kalır. Bu yerel tek instance demo aracıdır; gerçek ürün için hesap sahipliği/izin/koşul sürümü/outbox entegrasyonu hâlâ gerekir.46 test geçti; düğmenin gerçek Twilio çağrısı kullanıcı tarafından henüz denenmedi.


## D-026 sessizlik kuralı

Karşı taraftan ses/metin yoksa4sn civarı kısa Türkçe/İngilizce teyit;10sn toplam sessizlikte stream kapanır, mevcut TwiML Hangup çalışır. Asistanın kendi normal konuşma süresi sayılmaz; teyit sorusu saati resetlemez. Inbound mu-law enerji aktivitesi ve tanınan metin resetler; gürültü veya bekleme müziği de ses sayılabilir.54 test geçti; gerçek aramayla yeni kural henüz denenmedi. Ön yüzde end_reason remote_silence_10s ayrı açıklanır; bu sonuç rezervasyon iptali değildir.
