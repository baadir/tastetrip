# UX skill incelemesi

Tarih: 20 Ekim 2026.

## Mevcut katalog

`ux-consultant-finance` yerel SKILL.md dosyası incelendi. Finansal dashboard ve portföy kararlarına odaklandığı için seyahat rezervasyon ürününün ana UX becerisi olarak seçilmedi. React ve teknik doğrulama becerileri ise kullanıcı yolculuğu ve etkileşim modeli seçiminin yerini tutmuyor.

## GitHub adayları

| Aday | İnceleme | Karar |
| --- | --- | --- |
| [magnus919/agent-skills — product-design-and-ux](https://github.com/magnus919/agent-skills/tree/main/product-design-and-ux) | SKILL.md tam okundu; bilgi mimarisi, durum modelleri, responsive davranış, AI kontrol sınırları ve test planı referansları okundu | Seçildi: henüz ekran çizmeye başlamadan davranış ve kullanıcı kontrolünü tanımlamak için uygun |
| [hueyexe/frontend-agent-skills — ux-usability-foundations](https://github.com/hueyexe/frontend-agent-skills/tree/main/ux-usability-foundations) | SKILL.md tam okundu; genel kullanılabilirlik, hata kurtarma, form ve gezinme odağı değerlendirildi | Güçlü alternatif; bu aşamada aynı kapsamı tekrar eden ikinci bir skill kurulmadı |
| [mdrmuhaimin/agentic-skills — mobile-ui-ux-designer](https://github.com/mdrmuhaimin/agentic-skills/tree/main/codex/mobile-ui-ux-designer) | GitHub arama özeti incelendi; tam içerik denetimi yapılmadı | Mobil ve görsel uygulama tarafı daha baskın; seçim için yeterli inceleme yapılmadığından kurulmadı |

Bu bir evrensel kalite sıralaması değil; mevcut işe uygunluk değerlendirmesidir. Popülerlik tek başına kalite kanıtı olarak kullanılmadı.

## Kurulum ve kaynak

- Kurulum: sistem `skill-installer` içindeki `install-skill-from-github.py` ile.
- Yerel yol: `.agents/skills/product-design-and-ux/`.
- 26 dosya: ana talimat, referanslar, şablonlar ve değerlendirme örnekleri. İndirilen dosya listesinde yürütülebilir kurulum betiği yok.
- Kaynak ref: `main`; kontrol sırasında upstream HEAD: `03a72d67c0fb3607ab3da0fc4a3758d544f9ac06`. Bu kayıt, her dosyanın hash bazında karşılaştırıldığı iddiası değildir.
- Upstream SKILL.md ve GitHub lisans metadatası MIT belirtiyor. Kök `LICENSE` dosyası bu kontrolde bulunamadı; bağımsız lisans metni üretilmedi. Yeniden dağıtım öncesi bu eksik netleştirilmeli.
- Upstream dosyaları değiştirilmedi. Projeye özgü kararlar ayrı UX belgelerinde tutuluyor.
- Skill’in komşu uzmanlıklara yönlendiren bağlantıları var; bu komşu skill’ler kurulmadı. İlk çalışma bunlara bağımlı bir erişilebilirlik uygunluğu veya model kalitesi iddiasında bulunmuyor.

Proje içi keşif için kök `AGENTS.md` eklendi. Skill sonraki turda kullanılabilir olacak; bu turda içeriği doğrudan okunarak ilk UX çalışmasına uygulandı.

## Uygulanan yöntem

1. Kullanıcının mevcut durumunu ve hedefini ayır.
2. Giriş ve hesap oluşturmayı ürün değerini görme anına göre değerlendir.
3. Akışı başarı kadar kesinti, geri dönme ve hata durumlarıyla tanımla.
4. Dar/geniş ekran, klavye, dokunma ve dil genişlemesinde davranışı belirt.
5. Tasarım önerisi, ürün gereksinimi ve gözlenmiş kullanıcı kanıtını ayrı tut.

İlk çıktı: [Giriş ve açılış stratejisi](01-entry-and-login.md).
