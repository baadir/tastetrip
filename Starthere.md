# Buradan başla

**Önce [PROJECT_HISTORY.md](PROJECT_HISTORY.md) dosyasını oku, sonra aksiyon al.** Bu sıra her yeni oturumda, görevde ve bağlam yenilendiğinde geçerlidir.

## Çalışmaya başlamadan önce

1. `PROJECT_HISTORY.md` içindeki güncel durumu ve karar kayıtlarını oku.
2. Görevle ilgili kaynak belgeyi oku: ürün için `PRODUCT_REQUIREMENTS.md`, UX için `docs/ux/01-entry-and-login.md`, hackathon için `HACKATHON_REQUIREMENTS.md`.
3. Kesinleşmiş karar, geçici öneri, doğrulanmış bulgu ve açık soruyu birbirine karıştırma. Asistanın önerisini kullanıcı onayı gibi yorumlama.
4. Yapacağın değişikliğin önceki bir kararla çelişip çelişmediğini kontrol et. Çelişkiyi sessizce çözme veya eski kararı silme.
5. Kullanıcının yeni açık talimatı önceki kararı değiştiriyorsa uygula ve eski kararı referanslayan yeni bir tarihli karar kaydı ekle. Niyet belirsizse ilgili kararı değiştirmeden netleştir; bağımsız işleri sürdürebilirsin.

## Çalışma sonunda

- Kalıcı bir karar, bulgu, dış işlem veya durum değişikliği olduysa `PROJECT_HISTORY.md` dosyasına yeni kayıt ekle.
- Tarih, kayıt kimliği, durum, kaynak, gerekçe, etkilenen belgeler ve sonraki adımı belirt.
- Önceki kayıtları silme veya anlamını değiştirme. Düzeltmeyi yeni kayıtla yap; önceki kayda referans ver.
- Güncel durum özetini yeni kayda göre güncelleyebilirsin; eski kararların izi kayıt bölümünde korunmalı.
- Kaydedilmemiş form alanını kaydedilmiş, taslağı gönderilmiş, öneriyi onaylanmış veya yapılmamış testi başarılı olarak kaydetme.
- API anahtarı, parola veya başka sırları geçmiş dosyasına yazma. Yalnızca erişimin mevcut olup olmadığını kaydet.

## Şimdiki yön

28 Ekim H-075: Coolify Environment Variables listesine 12 boş API/model/ses alanı eklendi; toplam 19 runtime-only alan mevcut. Değerleri kullanıcı girecek; deploy başlatılmadı.

28 Ekim D-034/H-074: Proje github.com/baadir/tastetrip main dalına yüklendi. Coolify Tastetrip/production web kaynağı, HTTPS tastetrip.bahadirciftci.work domaini, Dockerfile/8080, kalıcı /app/data volume ve yedi sır olmayan runtime değişkeni kaydedildi. Deploy başlatılmadı; API sırları/LLM_MODEL ve tam ses servisleri yayın aşamasında tamamlanacak. docs/COOLIFY_TASTETRIP_PLAN.md güncel.

26 Ekim D-033/H-071: Deneyimin bütünü tek konuşma akışında; ayrı açılış/yan menü/form ekranları kaldırıldı. Uçuş ve rezervasyon bilgileri DeepSeek ile konuşmadan alınır; rota, tercih, içerik, güvenli giriş, listeler ve canlı görüşme aynı konuşmada karttır. 117 test; ayrı QA DB ile canlı rezervasyon taslağı/onay kapısı ve uçuş sonucu görüldü. docs/ux/10-complete-conversation.md güncel. Gerçek telefon/deploy yok.

26 Ekim D-032/H-070: Sohbet merkezli ana deneyim ve DeepSeek tercih çıkarımı uygulandı. Önce docs/ux/09-chat-first-journey.md oku. D-030 üç adımlı ana onboarding yüzeyi supersede; master profil, işlem anında giriş ve rezervasyon onayı korunur. 110 test; ayrı QA verisiyle canlı sohbet ve Qloo rota doğrulaması. Yerel 8080, üretim deploy yok.

22 Ekim D-031/H-069: Ürün restoran rezervasyonu yapısı eklendi. Önce docs/RESERVATION_IMPLEMENTATION.md oku: giriş/özet/onay, kalıcı outbox-worker, Anna/Flash-v3, yetkili canlı ses, ana dil altyazı/özet ve kanıtlı sonuç. İlk sürüm kesin koşullar; alternatif karar kartı/otel-müze kanalı yok. 102 test geçti; gerçek ürün telefon araması yapılmadı. Web8080/gateway8081/worker ve yenilenmiş geçici tünel yerelde hazır; Coolify deploy yok.

22 Ekim D-030/H-068: D-029 onboarding planı uygulamaya bağlandı. app/profiles.py ve /static/profile.js ortak sürümlü profil, üç adım, Tercihlerim, kategoriye göre Qloo, açık içerik kaydı ve hesap aktarımı içerir. 71 test geçti; 10 canlı Qloo kontrat kontrolü başarılı. Tarayıcıda onboarding/kayıt/yenileme doğrulandı. docs/ux/08-onboarding-and-taste-profile.md son uygulama kaydı ve README güncel kapsamı açıklar. Yerel 8080 yenilendi; Coolify deploy yapılmadı.

22 Ekim D-029/H-067: Tercih onboarding'i ve bütün önerilerde ortak master profil istendi. docs/ux/08-onboarding-and-taste-profile.md akış/sorular/model/Qloo eşleme planı hazır; ekran sırası ve şema öneri, henüz kodlanmadı. D-010 işlem anında giriş ve kullanıcının tetiklediği içerik önerisi korunur. Yeni ürün baseline FR-14.

D-028: Dil bazlı Flashv2.5→v3 router kullanıcı kararı; docs/ELEVENLABS_LANGUAGE_ROUTER_PLAN.md planı hazır, henüz uygulanmadı. Anna korunur; görüşme dili ve uçtan uca STT/TTS uygunluk kontrolü gerekir.

D-027 (22Ekim): Ana ses tüm desteklenen diller için Anna seçildi; Türkçe Dilara eski kararı supersede edildi. Env genel/TR/EN Anna; telefon modeli Flashv2.5 korunur. Beş dilli örnek Afrikaans desteği nedeniyle yalnız artifact üretiminde Eleven v3 kullanır.

D-025: Aktif Anna hedefi artık The Goat Bar & Grill,Goatstown,Dublin. Philip,3kişi,22Ekim13:00 Dublin yerel saati. docs/ANNA_RESTAURANT_CALL_BRIEF.md son bölümünü oku. Önceki Botanical/Burbank hedefleri tarihsel.

D-024/H-060: Aktif Anna restoran düğmesi artık Botanical/Dublin One Hotel (Dublin) hedefli; Burbank hedefi tarihsel. Philip,3kişi,22Ekim13:00 Dublin yerel saati. Güncel briefin son bölümünü oku; Dublin araması henüz yapılmadı.

D-023/H-057: Anna restoran düğmesi hazır: BJ’s Burbank,Philip,3kişi,22Ekim2026 13:00 Los Angeles yerel saati. Onaydan sonra deney/özür ve test rezervasyonunu iptal/teyit isteme. Gerçek restorana henüz arama yok; docs/ANNA_RESTAURANT_CALL_BRIEF.md son güncellemeyi oku.

H-056: Sonraki Anna/İngilizce restoran araması için docs/ANNA_RESTAURANT_CALL_BRIEF.md kaydı var: Philip,3kişi; tarih/saat henüz yok. Gerçek arama yapılmadı ve mevcut demo hedefi değiştirilmedi.

H-055: Yerel monitor ekranından sabit şahsi test numarasını arama düğmesi eklendi;46 test geçti. Önce Canlı dinle, sonra Test aramasını başlat. SQLite idempotency/unknown bloklaması var; genel ürün arama yetkilendirmesi değil. Gerçek düğme çağrısı henüz denenmedi.

D-022/H-053: Açılışta müşteri adına arayan yapay zekâ destekli dijital asistan açıklaması zorunlu; kesilirse tekrar. H-054: http://localhost:8081/monitor yerel ses/metin takip ekranı;39 test ve sentetik iki taraf paket aktarımı doğrulandı. Gerçek telefonla canlı dinleme testi henüz yok; docs/LOCAL_VOICE_TEST.md son bölümünü oku.

21 Ekim: app/voice_agent.py ile Dilara+DeepSeek Türkçe restoran simülasyonu hazırlandı; docs/LOCAL_VOICE_TEST.md son bölümünü oku. Tarihli demo22Ekim19:00/3kişi,180sn sınır; gerçek ürün rezervasyon akışı değil. İngilizce Anna seçimi D-021 kapsamında kaydedildi.

D-020: Kullanıcı ElevenLabs Dilara sesini seçti; P-006 Polly varsayılan önerisinin yerine hedef TTS. ELEVENLABS_VOICE_ID env şablonunda; entegrasyon/erişim henüz doğrulanmadı. H-047 API anahtarı formu hazır.

H-041: Yerel ayrı8081 ses gateway ve geçici Cloudflare tüneli hazır; docs/LOCAL_VOICE_TEST.md oku. Henüz gerçek telefon STT testi/konuşan agent değil. H-038/039 outbound Türkçe mesaj bağlantısı kullanıcı tarafından duyuldu; Coolify deploy yok.

D-018/P-006: Aramada maliyet önceliği. Güncel teknik yön Twilio Media Streams + kendi CAX21 gateway/worker + Deepgram + DeepSeek + Polly Standard; önce docs/VOICE_COST_COMPARISON.md oku. Önceki Vapi/ElevenLabs P-005 önerisinin yerini aldı; servis kalite testi ve arama uygulaması henüz yok.

D-017: Görüşme sonrasında native dilde konuşma özeti de kapsamda; PRODUCT_REQUIREMENTS FR-13 ve rezervasyon araması planını oku. Özet ile doğrulanmış rezervasyon sonucu ayrı. Henüz uygulanmadı.

Rezervasyon araması için güncel plan docs/RESERVATION_CALL_IMPLEMENTATION_PLAN.md (P-005/H-024). D-016: görüşme dili restoran ülkesine göre varsayılan, altyazı kullanıcının native dilinde. Vapi/Twilio/ElevenLabs hâlâ öneri; gerçek arama yapılmadı.

D-010–D-012/H-015: Kod artık app/ altında; ilk çalışan genel seyahat uygulaması, DeepSeek+Qloo rota üretimi/düzenleme ve Aviasales entegrasyonu mevcut. Login kaydetme/rezervasyon gibi işlem anında; anonim cookie ile tercihler/taslak hatırlanır. Güncel uygulama sınırları için README.md ve docs/IMPLEMENTATION_STATUS.md, Coolify/CAX21 için docs/COOLIFY_DEPLOYMENT.md oku. Yerel adres http://localhost:8080; deploy yapılmadı. .env içeriğini çıktıya yazma.

D-009: Rota içi kitap/film/podcast/müzik önerileri de kapsamda. THY Travel Agent kart ve rota bileşenleri referans alınıyor; docs/ux/07-thy-components-and-content.md dosyasını oku. Kod aktarımı/oynatıcı henüz yok.

D-008 (21 Ekim 2026): Güncel kapsam çok günlük kişisel seyahat rotasıdır; restoran, kafe, bar, otel ve gezilecek yerler ile durak bazlı rezervasyon içerir. PRODUCT_REQUIREMENTS.md ve docs/ux/06-trip-itinerary.md günceldir. Restoran taslakları bu genişleyen akışın alt parçalarıdır; rota henüz uygulanmadı.

API anahtarı geldi; ilk kontrolden sonra 52 ek çağrıyla girdi/kategori/metadata ve tercih etkisi incelendi. Güncel UX kanıtı için `docs/ux/04-api-backed-ux-recommendations.md`, ilk kontrol için `docs/QLOO_LIVE_VALIDATION.md` dosyasını oku. Anahtar proje dosyalarında bulunmaz. İlk metin ağırlıklı taslak kullanıcı tarafından reddedildi; daha görsel, akışkan ve geçişli bir yön istendi (D-006). İkinci görsel yön `docs/ux/03-fluid-visual-direction.md` içindedir ve henüz kullanıcı onayı değildir. P-003, gerçek kataloğa dayalı sonraki UX önerisidir; login ve telefon/dil kararları kendiliğinden kesinleşmiş sayılmaz. Ayrıntılar ve karar kimlikleri `PROJECT_HISTORY.md` içindedir.

Bu dosyalar çalışma bağlamıdır; gerçek uygulama veya API doğrulaması yerine geçmez. Bu talimat, dosyaları okuyan sonraki çalışmalar için bağlam koruma mekanizmasıdır; otomatik bir arka plan izleyicisi kurulmamıştır.
