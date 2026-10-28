# TasteTrip — Sign up / Sign in

28 Ekim 2026 · D-037/H-079. Kullanıcı ayrı kayıt butonu ve kayıt sürecinin gözden geçirilmesini istedi. D-033 tek sohbet, D-036 English UI ve işlem anında giriş korunur. Bu çalışma ürün/UX skill ile mevcut uygulama incelemesine dayanır; kullanıcı araştırması iddiası yoktur.

## Akış ve kabul koşulları

- Misafir üst barda ayrı Sign in ve vurgulu Sign up görür. Kayıt zorunlu açılış adımı değildir. Hesap açıkken Sign up gizlenir, Sign out görünür; çıkışta geri gelir.
- Sign up aynı sohbet içinde Create your account kartını açar; kullanıcı adı, parola ve parola tekrarı vardır. Eski Create new account checkbox kaldırıldı. Sign in kartı iki alan kullanır. İki kartın arasında geçiş kullanıcı adını ve bekleyen işi korur; parola alanları temizlenir.
- Kullanıcı adı 3–50 ASCII harf/rakam/nokta/alt çizgi/tire; server trim/lowercase ile normalleştirir. Parola 12–200 karakter; kayıt ekranında eşleşme kontrolü ve göster/gizle düğmesi vardır. Parolalar sohbet/LLM yerine yalnız auth uç noktasına gider. Yeni UI confirmation alanını gönderir; eski API istemcileriyle uyum korunur. Varsa uyuşmayan confirmation server tarafından da reddedilir. register alanı boolean olmalıdır.
- Başarılı kayıtta güvenli oturum açılır; kart kapanır, parola alanları temizlenir ve bekleyen rota kaydetme/listeler gibi işe dönülür. Profil aktarımı ayrı açık seçimdir. Kayıt başarılı olup sonraki veri yenilemesi başarısızsa kayıt yeniden başarısız diye gösterilmez: signed-in durumu ve tekrar deneme açıklanır.
- Parola uyuşmazlığı, hatalı kullanıcı adı/parola uzunluğu ve kullanılan ad hataları English olarak kart içinde görünür. İptal kayıt oluşturmaz; taslak/anonim tercihler korunur. Kart mobilde tek sütun, geniş ekranda kompakt alan grupları kullanır.

## Doğrulama ve sınır

126 unittest ve JavaScript sözdizimi kontrolleri geçti. Ayrı yerel QA DB/tarayıcıyla My trips → Sign in → Sign up, parola uyuşmazlığı, başarılı kayıt/otomatik giriş/bekleyen My trips dönüşü, çıkışta Sign up geri gelişi, duplicate username ve tekrar Sign in doğrulandı. Üretimde sentetik hesap açılmadı.

Kayıt username/password tabanlıdır; e-posta doğrulama ve parola kurtarma uygulanmadı. Parola kurtarmanın olmadığı kartta açıkça belirtilir. Gerçek ücretli telefon/rezervasyon başlatılmadı.
