# Kurtaran Ev — Açık Konular

Site lokalde eksiksiz çalışıyor: 21 sayfa, ilan kataloğu, arama arayüzü ve yönetim paneli.
Aşağıdakiler canlıya çıkmadan önce tamamlanması gereken işler. Her maddede hangi dosyaya
dokunulacağı yazıyor.

Durum: **Lokal prototip hazır** · Son güncelleme: 15 Ağustos 2026

---

## 1. Instagram otomatik akışı

İlan kataloğu, arama arayüzü ve yönetim paneli hazır. 13 gerçek ilan (8 köpek, 5 kedi)
gönderi metinlerinden ayrıştırılıp sisteme aktarıldı. Eksik olan tek şey **otomatik**
çekim: Instagram, giriş yapmadan gönderi içeriği vermiyor (denendi — profil login
duvarına düşüyor, herkese açık JSON uçları kapalı).

- [ ] **@kurtaranev_kopekleri ve @kurtaranev_kedileri hesaplarını İşletme (Business)
      hesabına çevirin.** Ayarlar → Hesap türü ve araçlar.
- [ ] **Her iki hesabı bir Facebook Sayfası ile ilişkilendirin.** Graph API bunu şart koşuyor.
- [ ] **developers.facebook.com'da bir uygulama oluşturun**, Instagram Graph API ürününü ekleyin.
- [ ] **`instagram_basic` + `pages_show_list` izinlerini alın** (uygulama incelemesi gerekebilir).
- [ ] **Uzun ömürlü access token üretin** (kısa ömürlü jeton 1 saat, uzun ömürlü 60 gün).
- [ ] Jetonu tanımlayın:
      `export IG_ACCESS_TOKEN="..."` ya da `python3 tools/instagram_sync.py --ornek-config`
      ile oluşan `tools/instagram_config.json` dosyasına yazın.
- [ ] **Jeton yenileme** için 60 günde bir çalışan bir hatırlatma/otomasyon kurun.
      Komut hazır: `python3 tools/instagram_sync.py --jeton-yenile`
      (config'e `app_id` + `app_secret` yazılmalı; sync sırasında jeton 50 günü
      geçmişse uyarı da basılıyor). Örnek cron — ayda bir yenile, günde bir çek:
      ```
      0 6 1 * * cd /yol/kurtaran-ev-website && python3 tools/instagram_sync.py --jeton-yenile
      0 7 * * * cd /yol/kurtaran-ev-website && python3 tools/instagram_sync.py --limit 10
      ```
- [ ] Çalıştığını doğrulayın: `python3 tools/instagram_sync.py --limit 5 --kuru`
- [ ] **Düzenli çalıştırma** ayarlayın (cron ya da hosting'in zamanlanmış görevi),
      örn. günde bir kez.
- [ ] `tools/instagram_config.json` dosyasını sürüm kontrolüne **eklemeyin** (jeton içerir).

> Jeton gelene kadar sistem elle içe aktarma ile çalışır:
> `python3 tools/instagram_sync.py --dosya tools/gonderiler.json`
>
> Ayrıca gönderi bağlantısıyla yarı otomatik çekim var (RapidAPI, jeton gerekmez):
> `python3 tools/instagram_sync.py --link "<gönderi-url>"` — caption + HD
> fotoğrafları indirir; denendi ve doğrulandı (Köfte gönderisi, 5 fotoğraf).
>
> **Köprü otomasyon (16 Ağustos 2026):** `--rapid` kipi, RapidAPI'daki
> "Instagram API - Fast & Reliable Data Scraper" servisiyle her iki hesabın
> son N gönderisini kendiliğinden çekiyor:
> `python3 tools/instagram_sync.py --rapid --limit 5`
> Denendi: 10 gönderi işlendi, mevcut ilanlar güncellendi, yeniler taslak düştü.
> Uyarılar: resmî API değil (ToS dışı, her an kırılabilir), ücretsiz katmanda
> sert hız limiti var (betik bekleyip yeniden dener). Uydurma gönderi
> kimlikleri gerçek kısa kodlarla eşlendi; yalnızca `ke-george` akışın ilk
> sayfasında olmadığı için eski kimliğinde kaldı — derin sayfalama eklenirse
> önce onun kimliği düzeltilmeli, yoksa mükerrer kayıt oluşur.
> Günlük köprü otomasyon için örnek cron:
> `0 7 * * * cd /yol/kurtaran-ev-website && python3 tools/instagram_sync.py --rapid --limit 5`
>
> **Onaysız yayın (16 Ağustos 2026, istek üzerine):** içe aktarılan ilanlar
> artık varsayılan olarak DOĞRUDAN "yuva-ariyor" durumuyla yayınlanıyor;
> panel onayı beklenmiyor. İhtiyatlı kip için `--taslak` bayrağı eklendi.
> Zaten kayıtlı gönderiler yeniden işlenmiyor (`--guncelle` ile zorlanabilir),
> bu sayede cron'da AI isteği yalnızca gerçekten yeni gönderiler için gidiyor.
>
> **AI ayrıştırma (16 Ağustos 2026):** Caption ayrıştırması artık varsayılan
> olarak OpenRouter/Gemini Flash ile yapılıyor (`tools/ai_parser.py`).
> Kural tabanlı ayrıştırıcı yedek olarak duruyor (`--klasik` ya da model
> hatasında otomatik). Kayıt hangi yöntemle üretildiyse `kaynak.ayristirici`
> alanında yazıyor ("ai" / "kural"). Fotoğraflar modele henüz gönderilmiyor —
> ileride görselden renk/boyut çıkarımı eklenebilir.

**Ayrıştırıcı iyileştirmeleri** (gerçek gönderilerde görülen eksikler):

- [x] Çoklu hayvan ilanları. `parse_all()` "ikisi erkek, biri dişi" gibi sayıları okuyup
      hayvan başına bir kayıt üretiyor; "Kutu kardeşler" 3 kayda açıldı (2 erkek, 1 dişi).
      Kayıtlar gönderi + sıra ikilisiyle eşleniyor, tekrar çekimde çoğalmıyor.
- [ ] Koruyucu Melek gönderileri: ayrıştırıcı artık bunları `icerik_turu() ==
      "koruyucu-melek"` olarak tanıyor ve sync net bir mesajla atlıyor. **Açık kalan:**
      sitede bunlara ayrı bir bölüm açılacaksa tasarlanması gerekiyor.
- [x] Sağlık notu ayrıştırması → `saglikNotu` alanına çıkıyor; ağır durumlar
      (kör, engelli, FIV vb.) `ozelBakim`'i de işaretliyor.
- [x] Bulunduğu yer → `konum` alanı (geçici yuva / yaşam alanı, Hadımköy/Beşiktaş tanınıyor).
- [ ] Yeni gönderi kalıpları çıktıkça `tools/test_parser.py` içine vaka ekleyin
      (çoklu hayvan, sağlık notu, konum ve içerik türü vakaları eklendi).

---

## 2. Yönetim paneli — canlıya çıkmadan önce

Panel şu an **yalnızca yerel** kullanım için güvenli. Canlıda olduğu gibi kullanılamaz.

- [ ] **Gerçek kimlik doğrulama.** Şu an tek bir şifre ve bellekte tutulan jeton var;
      sunucu yeniden başlayınca oturumlar düşüyor. Kullanıcı hesapları + oturum saklama gerekli.
- [ ] **Şifreyi değiştirin.** Varsayılan `kurtaranev`. → `export KE_ADMIN_SIFRE="..."`
- [ ] **HTTPS zorunlu** olmalı; jeton düz metin gidiyor.
- [ ] **Hız sınırı / kaba kuvvet koruması** (şu an sınırsız deneme yapılabilir).
- [ ] **CSRF koruması** — API çerez değil Bearer jeton kullanıyor, yine de gözden geçirilmeli.
- [ ] **Fotoğraf işleme:** yüklenen görseller olduğu gibi kaydediliyor. Boyutlandırma,
      WebP'ye çevirme ve EXIF temizliği eklenmeli.
- [ ] **Yedekleme.** Tüm veri tek bir `animals.json` dosyasında. Düzenli yedek alın;
      ilan sayısı büyürse gerçek bir veritabanına (SQLite/Postgres) taşıyın.
- [ ] **Değişiklik günlüğü** — kim neyi ne zaman değiştirdi?
- [ ] `admin.html` sayfasını `robots.txt` ile arama motorlarına kapatın.

---

## 3. Bağış ve ödeme altyapısı

Sitenin en kritik eksiği. Şu an bağış akışlarının hiçbiri gerçek bir tahsilata bağlı değil.

- [ ] **Ödeme sağlayıcısı seçilecek** (iyzico, PayTR, Stripe vb.) ve dernek adına hesap açılacak.
- [ ] **Tek seferlik bağış akışı** bağlanacak.
      → `tools/pages.py` içinde `BAGIS_YAP`
- [ ] **Düzenli (abonelik) bağış akışı** bağlanacak — Koruyucu Melek için otomatik aylık çekim.
      → `tools/pages.py` içinde `KORUYUCU_MELEK`, `#melek-form` bölümü
- [ ] **Bağış tutarı seçici** şu an yalnızca düğme metnini değiştiriyor; seçilen tutar ödeme
      sayfasına taşınacak.
      → `site/assets/js/main.js`, `data-amounts` bloğu
- [ ] **Banka hesap bilgileri (IBAN)** eklenecek. Şu an "Hesap bilgileri için
      iletisim@kurtaranev.org" yazıyor — gerçek bilgiyle değiştirilecek.
      → `tools/pages.py` içinde `BAGIS_YAP`, "Banka havalesi / EFT" kutusu
- [ ] **Bağış makbuzu / dekont** süreci netleştirilecek (otomatik e-posta gönderilecek mi?).
- [ ] **Bağış tutarlarındaki karşılıklar doğrulanacak.** ₺500 bir haftalık mama, ₺1.500 aşı,
      ₺3.000 kısırlaştırma, ₺7.500 acil tedavi — bunlar örnek rakamlar, dernekten teyit alınmalı.
      → `tools/pages.py` içinde `BAGIS_YAP`, "Somut karşılıklar" bölümü

---

## 4. Formlar

Beş form var; hepsi şu an ekranda "gönderildi sayılmaz" uyarısı veriyor, hiçbir yere veri gitmiyor.

- [ ] **Form servisi seçilecek** (Formspree, Netlify Forms, Google Forms ya da kendi API'niz).
- [ ] Bağlanacak formlar:
  - [ ] Geçici yuva başvurusu → `gecici-yuva.html`
  - [ ] Gönüllü başvurusu → `gonullu-ol.html`
  - [ ] İletişim formu → `iletisim.html`
  - [ ] Koruyucu Melek kaydı → `koruyucu-melek.html`
  - [ ] Bülten aboneliği → `index.html` (alt kısım)
- [ ] **Bülten için e-posta servisi** ayrıca gerekli (Mailchimp, Brevo vb.).
- [ ] **KVKK aydınlatma metni ve onay kutusu** her forma eklenecek. Kişisel veri toplandığı
      için yasal olarak zorunlu.
- [ ] Başvuruların hangi e-posta adresine düşeceği belirlenecek.

> Formların ortak davranışı `site/assets/js/main.js` içindeki `data-demo-form` bloğunda.
> Gerçek servise bağlanınca bu blok kaldırılacak.

---

## 5. İçerik eksikleri

- [ ] **Blog yazı detay sayfaları.** `hikayeler.html` şu an yalnızca liste; kartlardaki
      "Hikâyeyi oku" bağlantıları `#` işaret ediyor. Altı yazı için detay sayfası gerekiyor:
      Lucy, Kurtaran Araç, Kevok, kış hazırlığı, kedi yaşam alanı, ilk hafta rehberi.
- [ ] **Yaşam alanlarının açık adresleri.** Ziyaret saatleri `tasarim/prototip-ana-sayfa.pdf`'ten alındı ama adresler yok;
      şu an "randevu sırasında paylaşıyoruz" deniyor. Adresler eklenecekse harita da düşünülebilir.
      → `tools/pages.py` içinde `YASAM_ALANLARI`
- [ ] **İlan fotoğrafları.** Mevcut 13 fotoğraf Instagram ekran görüntülerinden kırpıldı;
      üzerlerinde isim yazısı ve #hashtag rozetleri var. Orijinal fotoğraflar varsa
      onlarla değiştirin — `site/assets/img/animals/`.
- [ ] **Kurtaran Shop ürünleri.** Dört ürün ve fiyatları tamamen örnek içerik.
      Gerçek ürünler, görseller ve fiyatlar gelecek; mağaza altyapısı bağlanacak.
      → `tools/pages.py` içinde `KURTARAN_SHOP`
- [ ] **Güncel ihtiyaç listesi.** Sahadan gelen gerçek listeyle değiştirilecek ve düzenli
      güncellenmesi için bir yöntem belirlenecek (kim, ne sıklıkla güncelleyecek?).
      → `tools/pages.py` içinde `GUNCEL_IHTIYACLAR`
- [ ] **E-kart görselleri.** Şu an yalnızca üç kart türü metinle anlatılıyor, görsel yok.
      → `tools/pages.py` içinde `E_KARTLAR`
- [ ] **Kurumsal iş birliği örnekleri.** Yalnızca Kurtaran Araç var; başka referanslar
      eklenebilir. Anadolu Sigorta logosu kullanılacaksa izin alınmalı.
- [ ] **Dernek künyesi** eklenecek: resmi dernek adı, vergi/dernek kütük numarası, adres.
      Genelde alt bilgide durur.
- [ ] **Görsel alt metinleri (alt)** derneğin bildiği gerçek isimlerle iyileştirilebilir
      (örn. hangi köpek hangi fotoğrafta).

---

## 6. İngilizce sürüm

- [ ] Dil seçici arayüzü hazır, EN şu an **"yakında"** olarak pasif.
      → `tools/build.py` içinde `HEADER`, `.lang__menu` bloğu
- [ ] Karar verilecek: `/en/` klasörü mü, ayrı dosya adları mı?
- [ ] 21 sayfanın metinleri çevrilecek (ilan verisi dahil: karakter etiketleri, ilan metinleri).
- [ ] `<html lang="tr">` çevrilen sayfalarda `en` olacak, sayfalar arası `hreflang`
      bağlantıları eklenecek.

> Not: `tools/pages.py` yapısı ikinci bir dil eklemeye uygun — sözlük ikiye çıkarılıp
> `build.py` iki kez çalıştırılabilir.

---

## 7. Yayına alma

- [ ] **Alan adı** (kurtaranev.org görünüşe göre kullanımda — e-posta adresi oradan) ve
      DNS ayarları.
- [ ] **Hosting.** Site tamamen statik olduğu için Netlify, Vercel veya GitHub Pages
      ücretsiz ve yeterli. `site/` klasörünü yüklemek yeterli.
- [ ] **HTTPS sertifikası** (yukarıdaki servislerde otomatik gelir).
- [ ] **Görsel optimizasyonu.** Görseller PDF'ten orijinal boyutlarıyla çıkarıldı,
      toplam 3,9 MB. WebP'ye çevrilip küçültülürse sayfa belirgin şekilde hızlanır.
      → `site/assets/img/`
- [ ] **favicon** şu an logo PNG'si; ayrı bir favicon seti hazırlanabilir.
- [ ] **Open Graph / sosyal medya paylaşım görselleri** eklenecek — şu an bir bağlantı
      WhatsApp veya Instagram'da paylaşıldığında önizleme görseli çıkmıyor.
- [ ] **sitemap.xml** ve **robots.txt** eklenecek. İlan sayfaları (`ilan.html?id=...`)
      istemci tarafında üretiliyor; arama motorlarında görünmeleri isteniyorsa her ilan
      için statik sayfa üretilmeli (`build.py`'ye eklenebilir) ya da sunucu tarafı render gerekir.
- [ ] **Analitik** kurulacak (Google Analytics, Plausible vb.) — KVKK/çerez uyarısı gerekebilir.
- [ ] **404 sayfası** hazırlanacak.

---

## 8. Küçük notlar

- [ ] Menüde ↗ ile işaretli maddeler (Sahiplen, Geçici Yuva, Bağış Yap, Koruyucu Melek,
      E-kartlar, Kurtaran Shop, Gönüllü Ol, Kurumsal İş Birliği) tasarımda dış bağlantı
      gibi duruyordu. Site lokalde eksiksiz gezilebilsin diye **iç sayfalara** bağlandı.
      Bir kısmı gerçekten dış sisteme gidecekse (örn. bağış platformu, shop) bağlantılar
      güncellenecek. → `tools/build.py` içinde `NAV`
- [ ] Duyuru şeridindeki ziyaret saatleri (Hadımköy 12.00–17.00, Beşiktaş 10.00–16.00)
      PDF'ten alındı; güncel mi teyit edilecek. → `tools/build.py` içinde `HEADER`
- [ ] Alt bilgideki telif yılı sabit "2026" yazıyor; otomatikleştirilebilir.
- [ ] Erişilebilirlik son kontrolü: klavye ile gezinme ve ekran okuyucu testi yapıldı mı?
- [ ] Gerçek cihazlarda (iPhone, Android) test edilecek — şu an yalnızca tarayıcıda
      farklı genişliklerde doğrulandı.

---

## Tamamlananlar

- [x] PDF prototipinin ana sayfa olarak birebir uygulanması
- [x] JPEG'deki site haritasının menüye dönüştürülmesi (4 açılır menü + TR + Bağış Yap)
- [x] 17 sayfanın oluşturulması
- [x] Tasarım sistemi (renkler, tipografi, bileşenler) → `site/assets/css/style.css`
- [x] PDF'ten görsel ve logo çıkarımı
- [x] Mobil/tablet uyumu (390 px'e kadar test edildi)
- [x] Açılır menüler, mobil menü, bağış tutarı seçici, SSS akordiyonu
- [x] Kırık bağlantı ve yatay taşma kontrolü
- [x] İlan kataloğu: kedi/köpek sayfaları, arama, 9 filtre, sıralama, paylaşılabilir URL
- [x] İlan detay sayfası (galeri, künye tablosu, "bilinmiyor"/"tahmini" gösterimi)
- [x] Hayvan veri modeli — hiçbir alan zorunlu değil, tahmini değerler işaretli
- [x] Yönetim paneli: ekleme, düzenleme, silme, fotoğraf yükleme (şemadan üretilen form)
- [x] Yerel sunucu + admin API (`tools/server.py`)
- [x] Instagram caption ayrıştırıcısı + regresyon testleri
- [x] Instagram pipeline'ı (Graph API kipi + elle içe aktarma kipi)
- [x] 13 gerçek ilanın aktarılması (8 köpek, 5 kedi)
