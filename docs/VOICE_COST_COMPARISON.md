# Ekonomik rezervasyon araması altyapısı

Tarih: 21 Ekim 2026. Resmî fiyat sayfalarına dayalı plan; çalışan arama entegrasyonu veya ölçülmüş fatura değildir.

## Seçilen geliştirme yönü

Kullanıcının önceliği en düşük maliyet (D-018). Tekrarlanan servis giderini azaltmak için Vapi yerine mevcut CAX21 üzerinde kendi konuşma orkestrasyonumuz önerilir: Twilio Programmable Voice + bidirectional Media Streams → Deepgram Nova-3 streaming STT → mevcut DeepSeek → Amazon Polly Standard. Coolify üzerinde ayrı async voice-gateway ve kalıcı outbox worker kullanılacak. Bu sağlayıcı bileşimi teknik öneridir (P-006); dil/kalite/gecikme testi henüz yapılmadı.

Bu seçim incelenen yönetilen-agent yaklaşımına göre düşük işletim gideri hedefler; dünyadaki bütün operatörlerin en ucuzu olduğu kanıtlanmadı. Twilio ilk PSTN adaptörüdür; hedef ülke/numara türüne göre Telnyx veya yerel SIP tarifesi daha ucuz çıkabilir. Geliştirme ve bakım emeği dahil toplam sahip olma maliyeti farklıdır.

| Bileşen | Birim maliyet / yaklaşım |
| --- | --- |
| PSTN telefon | Twilio; ülke, numara türü ve arayan numara bölgesine bağlı |
| İki yönlü medya | Twilio Media Streams $0.0044/dakika |
| STT | Deepgram Nova-3 monolingual streaming: kampanya $0.0048/dakika; sayfada normal $0.0077/dakika |
| TTS | Amazon Polly Standard $4 / 1 milyon karakter; desteklenen dil/seste |
| Agent, native altyazı çevirisi ve özet | DeepSeek; gerçek giriş/çıkış token tüketimi üzerinden, dakika başına sabit ücret varsayılmaz |
| Orkestrasyon / dinleme | Mevcut CAX21 üzerinde kendi gateway/worker; ayrı Vapi lisans/dakika kalemi yok; sunucu kaynakları ve bakım ücretsiz sayılmaz |

Vapi hosting tek başına $0.05/dakika; telefon, STT, TTS ve LLM ayrıca. 1000 dakikada kaldırılan Vapi hosting kalemi $50 olur; kendi medya ve işletim giderleri düşülmeden net tasarruf diye sunulmaz. ElevenLabs ilk maliyet odaklı varsayılan değildir; Polly telefon kalitesinde yetersiz kalırsa yalnız ilgili dil için daha kaliteli ses değerlendirilir.

## Örnek hesap: Paris sabit hat

Varsayım: 3 dakika, agent toplam 1500 karakter üretir; tek STT akışı 3 dakika açıktır. Ücretsiz krediler hesaba katılmaz.

- Fransa sabit hat: 3 × $0.0187 = $0.0561.
- Media Streams: 3 × $0.0044 = $0.0132.
- STT: 3 × $0.0048 = $0.0144 (kampanya); normal tarifede $0.0231.
- Polly Standard: 1500 / 1 milyon × $4 = $0.006.
- Toplam: **$0.0897 kampanya / $0.0984 normal STT + DeepSeek tokenları**.

Yaklaşık $0.09–0.10 yalnız bu senaryonun değişken kalemleridir. Aylık telefon numarası, vergi, sunucu/bant genişliği, olası diğer sağlayıcı ücretleri ve faturalama yuvarlaması hariç. Bu tutar Türkiye, mobil hat veya her ülke için geçerli değildir. Fransa mobil tarifesindeki düşük EEA-origin fiyatını bütün aramalara uygulamamak gerekir. Türkiye tarifesi bu incelemede sayfa timeout nedeniyle yeniden doğrulanamadı; sayısal tahmin verilmedi.

## Ürün gereksinimlerinin korunması

- Restoran ülkesinden görüşme dili varsayılanı, kullanıcı ana dilinde altyazı ve görüşme sonrası özet korunur (D-016/D-017). Desteklenmeyen dilde sessizce başka dile geçilmez.
- Nova-3 için açık dil kodu seçilir; Türkçe ve Fransızca desteği belgelenmiş olsa da restoran gürültüsü/telefon hattı testi gerekir. Turn detection, endpointing, söz kesme ve TTS iptali kendi gateway sorumluluğumuzdur; Nova-3 Flux özelliklerini otomatik sağlamaz.
- Twilio bidirectional stream karşı uç inbound sesini taşır. Agent sesi kendi üretim hattından dinleyiciye de aktarılır; iki tarafın duyulması ve gerçekten çalınan sesle transcript hizası kontrollü testte doğrulanır. Mark/clear ile kesilen/çalınmayan ses yönetilir.
- Kullanıcı canlı sesi kendi yetkili WebSocket bağlantısıyla dinler; ayrıca telefonla konferansa bağlanmaz. Altyazı ve özet ek LLM tüketir.
- Mevcut idempotency, ayrı arama/rezervasyon durumları, explicit başlangıç onayı, bilinmeyen sonuç uzlaştırma ve özet yeniden denemesinin tekrar aramaması kuralları korunur.
- İlk teknik kapı: izinli test numarasında tek eşzamanlı arama, gecikme, iki taraf ses, dil ve maliyet ölçümü. Gerçek rezervasyon entegrasyonu henüz yazılmadı.

## Kaynaklar

21 Ekim 2026 kontrolü:
- https://www.twilio.com/en-us/voice/pricing/fr
- https://deepgram.com/pricing (streaming kampanyası geçici)
- https://developers.deepgram.com/docs/models-languages-overview
- https://aws.amazon.com/polly/pricing/
- https://docs.aws.amazon.com/polly/latest/dg/standard-voices.html
- https://vapi.ai/pricing
