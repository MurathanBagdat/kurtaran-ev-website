# Kurtaran Ev — Web Sitesi

Sahipsiz kedi ve köpekleri kurtaran, tedavi eden ve yuvalandıran Kurtaran Ev Derneği için
web sitesi. Şu an **lokalde** çalışır.

Site 21 sayfadan oluşuyor: PDF prototipinin birebir uygulandığı ana sayfa, 16 içerik
sayfası ve sahiplendirme ilanları için arama arayüzü (kedi/köpek katalogları, ilan
detayı ve yönetim paneli).

- **Tasarım dili:** `tasarim/prototip-ana-sayfa.pdf` — ana sayfa bu PDF'in birebir karşılığıdır.
- **Site haritası:** `tasarim/site-haritasi.jpg` — menü yapısı bu görselden çıkarıldı.

---

## Siteyi açma

**Hızlı bakış:** `site/index.html` dosyasına çift tıklayın. Katalog ve arama dahil
her şey çalışır; yalnızca yönetim paneli çalışmaz.

**Tam kurulum (önerilen):**

```bash
python3 tools/server.py
```

Ardından `http://127.0.0.1:8000` — yönetim paneli için `/admin.html`.

---

## Klasör yapısı

```
Kurtaran Ev Websitesi/
├── site/                          ← yayına çıkacak klasör (statik)
│   ├── index.html                 ← ana sayfa (PDF prototipinin birebir karşılığı)
│   ├── yuva-arayan-kopekler.html  ← ilan kataloğu + arama/filtre
│   ├── yuva-arayan-kediler.html   ← ilan kataloğu + arama/filtre
│   ├── ilan.html                  ← tek ilan detayı (?id=...)
│   ├── admin.html                 ← yönetim paneli (yerel sunucu gerekir)
│   ├── … 16 içerik sayfası daha
│   └── assets/
│       ├── css/style.css          ← tasarım sistemi
│       ├── css/admin.css          ← yalnızca yönetim paneli
│       ├── js/catalog.js          ← arama, filtre, sıralama
│       ├── js/animal.js           ← ilan detayı
│       ├── js/admin.js            ← yönetim paneli
│       ├── js/counts.js           ← ana sayfadaki canlı ilan sayaçları
│       ├── data/animals.json      ← TEK DOĞRULUK KAYNAĞI (ilan verisi)
│       ├── data/animals.js        ← animals.json'dan üretilir (tarayıcı okur)
│       └── img/animals/           ← ilan fotoğrafları
├── tools/
│   ├── build.py                   ← sayfaları üretir
│   ├── pages.py                   ← sayfa içerikleri
│   ├── animals.py                 ← veri modeli + depo
│   ├── caption_parser.py          ← Instagram metni → yapılandırılmış veri
│   ├── instagram_sync.py          ← Instagram çekme pipeline'ı
│   ├── server.py                  ← yerel sunucu + admin API
│   ├── seed.py                    ← örnek kayıt üretici/temizleyici
│   ├── test_parser.py             ← ayrıştırıcı regresyon testleri
│   └── gonderiler.json            ← elle içe aktarma dosyası
├── tasarim/                       ← kaynak tasarım dosyaları (PDF + site haritası)
└── README.md · to-do.md
```

---

## İlan kataloğu

Sahiplendirilmeyi bekleyen kedi ve köpekler artık Instagram'a yönlendirilmiyor;
sitenin kendi katalog sayfalarında listeleniyor.

**Arama ve filtreler:** metin araması (Türkçe duyarlı — "seker" yazınca "Şeker" bulunur),
durum, cinsiyet, yaş grubu, boyut, kısırlaştırma, aşı, çocuk/köpek/kedi uyumu ve sıralama.
Seçilen filtreler adres çubuğuna yazılır; bir arama sonucu bağlantı olarak paylaşılabilir.

**Veri modeli — hiçbir alan zorunlu değil.** Çoğu kurtarılmış hayvanın cinsi ya da
kilosu bilinmiyor. Bilinmeyen alanlar `null` kalır ve arayüzde *"Bilinmiyor"* olarak
gösterilir. Tahmin edilen değerler `tahmini` listesinde işaretlenir ve
*"3,5 yaşında (tahmini)"* biçiminde görünür.

Durumlar: `taslak` (yayında değil) · `yuva-ariyor` · `rezerve` · `yuvalandi`.
Taslak ilanlar herkese açık sayfalarda hiçbir zaman görünmez — doğrudan bağlantıyla bile.

---

## Yerel sunucu ve yönetim paneli

```bash
python3 tools/server.py
```

- Site: `http://127.0.0.1:8000`
- Yönetim paneli: `http://127.0.0.1:8000/admin.html`
- Varsayılan şifre: `kurtaranev` — değiştirmek için `export KE_ADMIN_SIFRE="..."`

Sunucu yalnızca `127.0.0.1` adresine bağlanır, dışarıdan erişilemez.

Panelden yapılabilenler: ilan ekleme, düzenleme, silme, fotoğraf yükleme,
Instagram senkronu çalıştırma, örnek kayıtları temizleme. Form alanları
`tools/animals.py` içindeki şemadan üretilir; oraya yeni bir alan eklemek
panelde de otomatik olarak görünür.

Katalog sayfaları sunucu olmadan da çalışır (veri `animals.js` olarak yükleniyor),
ama **yönetim paneli sunucu ister** — kayıt yazabilmesi gerekiyor.

---

## Instagram pipeline'ı

**Önemli:** Instagram, giriş yapmadan gönderi metni ve fotoğraflarını paylaşmıyor.
Denendi ve doğrulandı: profil sayfası login duvarına düşüyor, herkese açık JSON
uçları da kapatılmış. Bu yüzden **otomatik** akış resmî Instagram Graph API'sine
bağlı. Kurulum adımları `to-do.md` içinde.

İki çalışma kipi var:

```bash
# 1) Otomatik — Graph API jetonu gerektirir
export IG_ACCESS_TOKEN="..."
python3 tools/instagram_sync.py --limit 5

# 2) Elle içe aktarma — jeton olmadan bugün çalışır
python3 tools/instagram_sync.py --dosya tools/gonderiler.json

# 2b) Gönderi bağlantısıyla — jeton olmadan, RapidAPI anahtarıyla çalışır
#     Caption + HD fotoğrafları çeker; bağlantıyı Instagram'dan "Bağlantıyı
#     kopyala" ile alın. Anahtar: instagram_config.json > rapidapi_key.
python3 tools/instagram_sync.py --link "https://www.instagram.com/kurtaranev_kopekleri/p/XXXX/"

# 2c) Son gönderileri OTOMATİK çek — jeton olmadan, RapidAPI scraper ile.
#     Her iki hesabın en yeni N gönderisini listeler ve işler. Resmî API
#     değildir (Instagram kullanım koşulları dışı, her an kırılabilir);
#     Graph API kurulana kadar köprü çözümdür.
python3 tools/instagram_sync.py --rapid --limit 5

# ne olacağını görmek için (hiçbir şey yazmaz)
python3 tools/instagram_sync.py --dosya tools/gonderiler.json --kuru

# uzun ömürlü jetonu tazele (60 günlük ömrü sıfırlar; app_id + app_secret ister)
python3 tools/instagram_sync.py --jeton-yenile
```

Pipeline ne yapıyor?

1. Gönderiyi çeker, **sahiplendirme ilanı mı** diye bakar. Koruyucu Melek çağrıları,
   teşekkür ve kampanya gönderileri elenir.
2. Metinden isim, yaş, cinsiyet, kilo, cins, boyut, kısırlaştırma, aşı,
   çocuk/köpek/kedi uyumu, sağlık notu ve bulunduğu yeri (geçici yuva /
   yaşam alanı) çıkarır. Kardeş gönderileri ("ikisi erkek, biri dişi")
   hayvan başına ayrı kayda açılır.
   Ayrıştırmayı varsayılan olarak **yapay zekâ** yapar (`tools/ai_parser.py`,
   OpenRouter üzerinden `google/gemini-3.6-flash`; yalnızca metin gönderilir,
   fotoğraflar gönderilmez). Modele "metinde yazmayanı doldurma" talimatı
   verilir; bilinmeyen alanlar boş kalır. Anahtar yoksa ya da `--klasik`
   verilirse `caption_parser.py`'deki kural tabanlı ayrıştırıcı devreye girer;
   model hata verirse de aynı yedeğe düşülür. Anahtar:
   `instagram_config.json > openrouter_key`.
3. Fotoğrafları indirir.
4. Kaydı yazar. Varsayılan olarak ilan **doğrudan yayınlanır** ("Yuva arıyor");
   `--taslak` bayrağıyla çalıştırılırsa kayıt taslak düşer ve yönetici panelden
   onaylayana kadar sitede görünmez (hatalı ayrıştırmaya karşı ihtiyatlı kip).
5. Aynı gönderi tekrar çekilirse yöneticinin elle düzelttiği alanların üzerine yazmaz;
   yalnızca boş kalan alanları doldurur.

Ayrıştırıcıyı tek başına deneyebilirsiniz:

```bash
python3 tools/caption_parser.py "PAMUK yuva arıyor, 2 yaşında dişi, 18 kg"
python3 tools/test_parser.py          # regresyon testleri
```

---

## Site haritası (JPEG'den)

| Ana menü | Alt sayfalar |
|---|---|
| **Yuva Ol** | Yuva Arayanlar → **Yuva Arayan Köpekler**, **Yuva Arayan Kediler**, Sahiplen, Geçici Yuva · Sahiplenmeden Önce · Sahiplenme Süreci |
| **Destek Ol** | Bağış Yap · Koruyucu Melek · E-kartlar ve Sertifikalar · Kurtaran Shop · Güncel İhtiyaçlar |
| **Katıl** | Gönüllü Ol · Kurumsal İş Birliği |
| **Hakkımızda** | Hikâyemiz ve Misyonumuz · Etkimiz ve Çalışmalarımız · Yaşam Alanlarımızı Ziyaret · Blog Merkezi → Haberler ve Hikâyeler · İletişim |

Ayrıca başlıkta TR/EN dil seçici ve turuncu **Bağış Yap** düğmesi bulunur.

---

## İçerik düzenleme

Başlık ve alt bilgi 21 sayfada ortaktır; bu yüzden sayfalar bir betikle üretilir.

1. Menüyü değiştirmek için: `tools/build.py` içindeki `NAV` listesi
2. Başlık/alt bilgi HTML'i için: `tools/build.py` içindeki `HEADER` ve `FOOTER`
3. Bir sayfanın içeriği için: `tools/pages.py`
4. Sonra:

```bash
python3 tools/build.py
```

`site/` altındaki HTML dosyaları yeniden yazılır. **HTML dosyalarını doğrudan düzenlerseniz
bir sonraki `build.py` çalıştırmasında değişiklikleriniz kaybolur.**

Yalnızca görünüm değişiklikleri (renk, boşluk, yazı tipi) için `site/assets/css/style.css`
dosyasını düzenlemek yeterlidir; betiği çalıştırmanıza gerek yoktur.

**İlan verisi ayrıdır:** ilanlar `build.py` ile değil, yönetim paneli ya da
`instagram_sync.py` ile yönetilir. `animals.json` elle düzenlenirse ardından
`python3 tools/animals.py` çalıştırın — tarayıcının okuduğu `animals.js` tazelenir.

---

## Tasarım sistemi

PDF'ten örneklenen değerler `style.css` dosyasının başındaki `:root` bloğunda:

| Token | Değer | Kullanım |
|---|---|---|
| `--cream` | `#fffdf7` | Sayfa zemini |
| `--cream-warm` | `#fff8ea` | Vurgulu bölüm zemini |
| `--navy` | `#183653` | Metin, kenarlık, sert gölge |
| `--green` | `#0b7a53` | Sayı şeridi, vurgular |
| `--green-dark` | `#07573f` | Alt bilgi |
| `--orange` | `#ff6b4a` | Birincil düğme, vurgu |
| `--yellow` | `#ffd44d` | Duyuru şeridi, bülten |
| `--sky` | `#8fd5ef` | Yaşam alanları bölümü |

**Tipografi:** Başlıklar Georgia, gövde metni sistem yazı tipi (macOS'ta SF Pro).
PDF de aynı ikiliyi kullanıyor, bu yüzden web fontu yüklenmiyor — sayfa anında açılıyor.

**Ölçüler:** Tasarım 1440 px genişlik referansıyla hazırlandı. İçerik kolonu 1268 px,
başlık kolonu 1368 px. Sayfa 390 px'e kadar sorunsuz küçülür.

---

## Yayına alırken yapılması gerekenler

Site şu an tamamen statik ve lokalde eksiksiz çalışıyor. Canlıya çıkmadan önce
bağlanması gereken işlerin tam listesi ayrı bir dosyada:

**→ [`to-do.md`](to-do.md)**

Başlıca eksikler: ödeme altyapısı, form gönderimi, blog yazı sayfaları,
İngilizce sürüm ve hosting kurulumu.

---

## Notlar

- Menüdeki ↗ işaretli maddeler PDF/JPEG'de dış bağlantı olarak işaretlenmişti. Sitenin
  lokalde eksiksiz gezilebilmesi için bunlar iç sayfalara bağlandı; yalnızca Instagram
  hesapları gerçek dış bağlantı olarak kaldı.
- `site/assets/img/` içindeki tüm görseller PDF'in içinden orijinal çözünürlükleriyle çıkarıldı.
- Site JavaScript olmadan da okunur; JS yalnızca menü, bağış seçici ve SSS akordiyonu içindir.
