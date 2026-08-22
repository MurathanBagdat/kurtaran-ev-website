/* Kurtaran Ev — arayüz metinleri (TR / EN).
   Dil <html lang="..."> özniteliğinden okunur; site/en/ altındaki sayfalar "en" der.
   İlan verisi (assets/data/animals.js) Türkçe tutulur; burada yalnızca arayüz
   sözlüğü ve veriden türetilebilen alanların (yaş, karakter) çevirisi vardır. */
(function () {
  'use strict';

  var EN = document.documentElement.lang === 'en';

  var TR = {
    cinsiyet: { disi: 'Dişi', erkek: 'Erkek' },
    boyut: { kucuk: 'Küçük', orta: 'Orta', buyuk: 'Büyük' },
    durum: { 'yuva-ariyor': 'Yuva arıyor', 'rezerve': 'Rezerve', 'yuvalandi': 'Yuvalandı', 'taslak': 'Taslak' },
    karakter: {},
    t: {
      ornekKayit: 'Örnek kayıt',
      fotoYakinda: 'Fotoğraf yakında',
      fotograf: 'Fotoğraf',
      cinsiyetBilinmiyor: 'Cinsiyet bilinmiyor',
      yasBilinmiyor: 'Yaş bilinmiyor',
      bilinmiyor: 'Bilinmiyor',
      tahmini: '(tahmini)',
      kisirEtiket: 'kısırlaştırıldı',
      ozelBakimEtiket: 'özel bakım',
      ilaniGor: 'İlanı gör',
      listeleniyor: function (n, tur) {
        return '<span>' + n + '</span> ' + (tur === 'kedi' ? 'kedi' : 'köpek') + ' listeleniyor';
      },
      sonucYok: 'Sonuç bulunamadı',
      bosBaslik: 'Bu filtrelerle eşleşen ilan yok',
      bosMetin: 'Filtreleri gevşetmeyi deneyin ya da tüm ilanlara göz atın.',
      filtreleriTemizle: 'Filtreleri temizle',
      sayac: function (n, tur) { return n + (tur === 'kedi' ? ' kedi' : ' köpek') + ' yuva arıyor'; },

      ilanYok: 'İlan bulunamadı',
      ilanYokMetin: 'Bu ilan kaldırılmış, yuvasına kavuşmuş ya da bağlantı hatalı olabilir.',
      kopekListesi: 'Yuva arayan köpekler',
      kediListesi: 'Yuva arayan kediler',
      basliEki: ' — yuva arıyor',
      evet: 'Evet',
      hayir: 'Hayır',
      sCinsiyet: 'Cinsiyet', sYas: 'Yaş', sCins: 'Cins / ırk', sKilo: 'Kilo', sBoyut: 'Boyut',
      sRenk: 'Renk / desen', sKisir: 'Kısırlaştırıldı', sAsili: 'Aşıları tam',
      sCocuk: 'Çocuklarla uyumlu', sKopek: 'Köpeklerle uyumlu', sKedi: 'Kedilerle uyumlu',
      sOzelBakim: 'Özel bakım',
      saglikNotu: 'Sağlık notu',
      aciklamaTurkce: '',
      kaynakInstagram: function (link) { return 'Bu ilan ' + link + ' Instagram gönderisinden alındı.'; },
      kaynakOrnek: 'Bu bir örnek kayıttır; gerçek bir ilan değildir.',
      yuvalandiBaslik: ' yuvasına kavuştu 🎉',
      yuvalandiMetin: 'Başka canlar hala bekliyor.',
      tanismak: function (isim) { return isim + ' ile tanışmak ister misiniz?'; },
      digerKopekler: 'Diğer yuva arayan köpekler',
      digerKediler: 'Diğer yuva arayan kediler',

      tutarSec: 'Seçtiğiniz tutarla başla',
      ileBasla: function (tutar) { return tutar + ' ile başla'; },
      formVarsayilan: 'Teşekkürler! Bu yerel prototipte form gönderimi henüz bağlı değil.',
      cumleSelam: 'Merhaba, ',
      cumleSahiplenme: ' için sahiplenme başvurusu yapmak istiyorum.',
      cumleGeciciYuva: ' için geçici yuva olmak istiyorum.',
      cumleKoruyucuMelek: ' için koruyucu melek olmak istiyorum.',
      cumleTanisma: ' ile tanışmak istiyorum.',
      cumleSon: ' Bilgi alabilir miyim?'
    },
    yasMetni: function (h) { return h.yasMetni || null; },
    sayi: 'tr-TR'
  };

  var EN_DICT = {
    cinsiyet: { disi: 'Female', erkek: 'Male' },
    boyut: { kucuk: 'Small', orta: 'Medium', buyuk: 'Large' },
    durum: { 'yuva-ariyor': 'Looking for a home', 'rezerve': 'Reserved', 'yuvalandi': 'Adopted', 'taslak': 'Draft' },
    /* Saha ekibinin kullandığı karakter etiketleri; eşleşmeyen etiket olduğu gibi kalır. */
    karakter: {
      'sevecen': 'affectionate', 'sosyal': 'social', 'oyuncu': 'playful', 'sakin': 'calm',
      'enerjik': 'energetic', 'hareketli': 'active', 'meraklı': 'curious', 'merakli': 'curious',
      'neşeli': 'cheerful', 'neseli': 'cheerful', 'uyumlu': 'easygoing', 'çekingen': 'shy',
      'cekingen': 'shy', 'ürkek': 'timid', 'urkek': 'timid', 'uysal': 'gentle', 'sadık': 'loyal',
      'sadik': 'loyal', 'bağımsız': 'independent', 'bagimsiz': 'independent', 'korkak': 'fearful',
      'cesur': 'brave', 'akıllı': 'clever', 'akilli': 'clever', 'nazik': 'gentle',
      'sevimli': 'sweet', 'tatlı': 'sweet', 'tatli': 'sweet', 'yavru': 'puppy-like'
    },
    t: {
      ornekKayit: 'Sample',
      fotoYakinda: 'Photo coming soon',
      fotograf: 'Photo',
      cinsiyetBilinmiyor: 'Sex unknown',
      yasBilinmiyor: 'Age unknown',
      bilinmiyor: 'Unknown',
      tahmini: '(approx.)',
      kisirEtiket: 'neutered',
      ozelBakimEtiket: 'special care',
      ilaniGor: 'View listing',
      listeleniyor: function (n, tur) {
        var ad = tur === 'kedi' ? (n === 1 ? 'cat' : 'cats') : (n === 1 ? 'dog' : 'dogs');
        return 'Showing <span>' + n + '</span> ' + ad;
      },
      sonucYok: 'No results',
      bosBaslik: 'No listings match these filters',
      bosMetin: 'Try loosening the filters or browse all listings.',
      filtreleriTemizle: 'Clear filters',
      sayac: function (n, tur) {
        var ad = tur === 'kedi' ? (n === 1 ? 'cat' : 'cats') : (n === 1 ? 'dog' : 'dogs');
        return n + ' ' + ad + ' looking for a home';
      },

      ilanYok: 'Listing not found',
      ilanYokMetin: 'This listing may have been removed, the animal may have found a home, or the link may be wrong.',
      kopekListesi: 'Dogs looking for a home',
      kediListesi: 'Cats looking for a home',
      basliEki: ' — looking for a home',
      evet: 'Yes',
      hayir: 'No',
      sCinsiyet: 'Sex', sYas: 'Age', sCins: 'Breed', sKilo: 'Weight', sBoyut: 'Size',
      sRenk: 'Colour / pattern', sKisir: 'Neutered', sAsili: 'Fully vaccinated',
      sCocuk: 'Good with children', sKopek: 'Good with dogs', sKedi: 'Good with cats',
      sOzelBakim: 'Special care',
      saglikNotu: 'Health note',
      aciklamaTurkce: 'This description was written in Turkish by our field team. Write to us and we’ll gladly tell you more in English.',
      kaynakInstagram: function (link) { return 'This listing was taken from an Instagram post by ' + link + '.'; },
      kaynakOrnek: 'This is a sample record, not a real listing.',
      yuvalandiBaslik: ' has found a home 🎉',
      yuvalandiMetin: 'Others are still waiting.',
      tanismak: function (isim) { return 'Would you like to meet ' + isim + '?'; },
      digerKopekler: 'Other dogs looking for a home',
      digerKediler: 'Other cats looking for a home',

      tutarSec: 'Start with your chosen amount',
      ileBasla: function (tutar) { return 'Start with ' + tutar; },
      formVarsayilan: 'Thank you! Form submission is not connected yet in this local prototype.',
      cumleSelam: 'Hello, ',
      cumleSahiplenme: ' — I would like to apply to adopt.',
      cumleGeciciYuva: ' — I would like to foster.',
      cumleKoruyucuMelek: ' — I would like to become a Guardian Angel.',
      cumleTanisma: ' — I would like to meet.',
      cumleSon: ' Could you send me more information?'
    },
    /* Yaş metni veride Türkçe ("2 yaşında", "5 aylık"); İngilizce için aydan üretilir. */
    yasMetni: function (h) {
      var ay = h.yasAy;
      if (ay == null) return h.yasMetni || null;
      if (ay < 12) return ay + (ay === 1 ? ' month old' : ' months old');
      var yil = Math.round(ay / 6) / 2;                 // 18 ay → 1.5
      return yil + (yil === 1 ? ' year old' : ' years old');
    },
    sayi: 'en-US'
  };

  var D = EN ? EN_DICT : TR;
  /* Veri kaydında İngilizce alan ("aciklamaEn" gibi) doluysa onu, yoksa Türkçesini döndürür. */
  D.alan = function (h, ad) {
    if (EN && h[ad + 'En'] != null && h[ad + 'En'] !== '' &&
        !(Array.isArray(h[ad + 'En']) && !h[ad + 'En'].length)) return h[ad + 'En'];
    return h[ad];
  };
  D.karakter = (function (map) {
    return function (k) {
      var anahtar = String(k || '').toLocaleLowerCase(EN ? 'en' : 'tr');
      return map[anahtar] || k;
    };
  })(D.karakter);

  window.KE_I18N = D;
})();
