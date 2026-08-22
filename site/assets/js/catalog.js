/* Kurtaran Ev — ilan kataloğu: arama, filtreleme, sıralama, listeleme.
   Veri kaynağı: assets/data/animals.js (window.KE_DATA)
   Not: veri JS dosyası olarak yükleniyor; böylece site yerel sunucu olmadan,
   dosyaya çift tıklayarak açıldığında da çalışıyor (fetch, file:// altında engelli). */
(function () {
  'use strict';

  var kok = document.querySelector('[data-catalog]');
  if (!kok) return;

  var TUR = kok.getAttribute('data-catalog');           // "kopek" | "kedi"
  var veri = (window.KE_DATA && window.KE_DATA.hayvanlar) || [];
  var EN = document.documentElement.lang === 'en';
  var I18N = window.KE_I18N;                             // assets/js/i18n.js
  var BASE = window.KE_BASE || '';                       // site/en/ altında "../"

  /* ---------------------------------------------------------------------
     Sözlükler
     --------------------------------------------------------------------- */
  var CINSIYET = I18N.cinsiyet;
  var DURUM = I18N.durum;
  var T = I18N.t;

  var PATI_SVG =
    '<svg viewBox="0 0 64 64" fill="currentColor" aria-hidden="true">' +
    '<ellipse cx="20" cy="20" rx="7" ry="9"/><ellipse cx="34" cy="15" rx="7" ry="9.5"/>' +
    '<ellipse cx="48" cy="21" rx="6.5" ry="8.5"/><ellipse cx="55" cy="35" rx="6" ry="7.5"/>' +
    '<path d="M34 30c8 0 15 6 15 13 0 6-5 9-11 9-3 0-5-1-8-1s-5 1-8 1c-6 0-11-3-11-9 0-7 7-13 15-13z"/>' +
    '</svg>';

  /* ---------------------------------------------------------------------
     Durum
     --------------------------------------------------------------------- */
  var VARSAYILAN = {
    q: '',
    durum: 'musait',        // müsait = yuva arıyor + rezerve
    cinsiyet: '',
    yas: '',
    boyut: '',
    sirala: 'yeni',
    kisir: false,
    asili: false,
    cocuk: false,
    kopek: false,
    kedi: false
  };
  var durum = Object.assign({}, VARSAYILAN);

  /* ---------------------------------------------------------------------
     Yardımcılar
     --------------------------------------------------------------------- */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* Türkçe duyarlı sadeleştirme — "Şeker" araması "seker" ile de bulunsun. */
  function sade(s) {
    return String(s || '')
      .replace(/I/g, 'ı').toLocaleLowerCase('tr')
      .replace(/[çğıöşü]/g, function (c) {
        return { 'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u' }[c];
      });
  }

  function tahminMi(hayvan, alan) {
    return (hayvan.tahmini || []).indexOf(alan) !== -1;
  }

  function kiloMetni(hayvan) {
    if (hayvan.kiloKg == null) return null;
    return String(hayvan.kiloKg).replace('.', EN ? '.' : ',') + ' kg';
  }

  /* ---------------------------------------------------------------------
     Filtreleme
     --------------------------------------------------------------------- */
  function uygunMu(h) {
    if (h.tur !== TUR) return false;
    if (h.durum === 'taslak') return false;          // taslaklar hiçbir zaman herkese açık değil

    if (durum.durum === 'musait' && h.durum !== 'yuva-ariyor' && h.durum !== 'rezerve') return false;
    if (durum.durum !== 'musait' && durum.durum !== '' && h.durum !== durum.durum) return false;

    if (durum.cinsiyet && h.cinsiyet !== durum.cinsiyet) return false;
    if (durum.yas && h.yasGrubu !== durum.yas) return false;
    if (durum.boyut && h.boyut !== durum.boyut) return false;

    /* Üç durumlu alanlar: kutucuk işaretliyse yalnızca kesin "evet" olanlar.
       Bilinmeyen (null) kayıtlar elenir — kullanıcı "kısırlaştırılmış" diye
       süzdüyse, emin olmadığımız bir hayvanı ona göstermek doğru olmaz. */
    if (durum.kisir && h.kisir !== true) return false;
    if (durum.asili && h.asili !== true) return false;
    if (durum.cocuk && h.cocuklaUyum !== true) return false;
    if (durum.kopek && h.kopeklerleUyum !== true) return false;
    if (durum.kedi && h.kedilerleUyum !== true) return false;

    if (durum.q) {
      var q = sade(durum.q);
      /* EN sayfada İngilizce arama dizini kullanılır; çevirisi olmayan
         alanlarda o dizin zaten Türkçesine düşüyor (animals.py > aramaEn). */
      var hedef = sade((EN && h.aramaEn) || h.arama || (h.isim + ' ' + (h.cins || '')));
      if (hedef.indexOf(q) === -1) return false;
    }
    return true;
  }

  function sirala(liste) {
    var kopya = liste.slice();
    if (durum.sirala === 'isim') {
      kopya.sort(function (a, b) { return (a.isim || '').localeCompare(b.isim || '', EN ? 'en' : 'tr'); });
    } else if (durum.sirala === 'yas-artan') {
      kopya.sort(function (a, b) {
        if (a.yasAy == null) return 1;               // bilinmeyen yaş sona
        if (b.yasAy == null) return -1;
        return a.yasAy - b.yasAy;
      });
    } else if (durum.sirala === 'yas-azalan') {
      kopya.sort(function (a, b) {
        if (a.yasAy == null) return 1;
        if (b.yasAy == null) return -1;
        return b.yasAy - a.yasAy;
      });
    } else {
      kopya.sort(function (a, b) { return (b.olusturma || '').localeCompare(a.olusturma || ''); });
    }
    /* Yuvalananlar her zaman en sonda dursun. */
    kopya.sort(function (a, b) {
      return (a.durum === 'yuvalandi' ? 1 : 0) - (b.durum === 'yuvalandi' ? 1 : 0);
    });
    return kopya;
  }

  /* ---------------------------------------------------------------------
     Kart üretimi
     --------------------------------------------------------------------- */
  function kartHTML(h) {
    var rozetler = ['<span class="badge badge--' + h.durum + '">' + esc(DURUM[h.durum] || h.durum) + '</span>'];
    if (h.ornek) rozetler.push('<span class="badge badge--ornek">' + T.ornekKayit + '</span>');

    var gorsel = (h.fotograflar && h.fotograflar[0])
      ? '<img src="' + esc(BASE + h.fotograflar[0]) + '" alt="' + esc(h.isim) + '" loading="lazy">'
      : '<div class="animal-card__placeholder">' + PATI_SVG + '<span>' + T.fotoYakinda + '</span></div>';

    var bilgiler = [];
    bilgiler.push(h.cinsiyet
      ? '<li>' + esc(CINSIYET[h.cinsiyet]) + '</li>'
      : '<li class="unknown">' + T.cinsiyetBilinmiyor + '</li>');
    var yas = I18N.yasMetni(h);
    if (yas) {
      bilgiler.push('<li>' + esc(yas) + (tahminMi(h, 'yasAy') ? ' <em>' + T.tahmini + '</em>' : '') + '</li>');
    } else {
      bilgiler.push('<li class="unknown">' + T.yasBilinmiyor + '</li>');
    }
    var kilo = kiloMetni(h);
    if (kilo) bilgiler.push('<li>' + esc(kilo) + (tahminMi(h, 'kiloKg') ? ' <em>' + T.tahmini + '</em>' : '') + '</li>');

    var etiketler = [];
    var cins = I18N.alan(h, 'cins');
    if (cins) etiketler.push('<span class="tag">' + esc(cins) + '</span>');
    (I18N.alan(h, 'karakter') || []).slice(0, 3).forEach(function (k) {
      etiketler.push('<span class="tag">' + esc(h.karakterEn && EN ? k : I18N.karakter(k)) + '</span>');
    });
    if (h.kisir === true) etiketler.push('<span class="tag">' + T.kisirEtiket + '</span>');
    if (h.ozelBakim === true) etiketler.push('<span class="tag">' + T.ozelBakimEtiket + '</span>');

    return '' +
      '<a class="animal-card" href="ilan.html?id=' + encodeURIComponent(h.id) + '">' +
        '<div class="animal-card__media">' + gorsel +
          '<div class="animal-card__badges">' + rozetler.join('') + '</div>' +
        '</div>' +
        '<div class="animal-card__body">' +
          '<h3 class="animal-card__name">' + esc(h.isim) + '</h3>' +
          '<ul class="animal-card__facts">' + bilgiler.join('') + '</ul>' +
          (etiketler.length ? '<div class="animal-card__tags">' + etiketler.join('') + '</div>' : '') +
          '<span class="animal-card__cta">' + T.ilaniGor + ' <span aria-hidden="true">→</span></span>' +
        '</div>' +
      '</a>';
  }

  /* ---------------------------------------------------------------------
     Çizim
     --------------------------------------------------------------------- */
  var izgara = kok.querySelector('[data-grid]');
  var sayac = kok.querySelector('[data-count]');
  var temizle = kok.querySelector('[data-clear]');

  function ciz() {
    var sonuc = sirala(veri.filter(uygunMu));

    if (sayac) {
      sayac.innerHTML = sonuc.length
        ? T.listeleniyor(sonuc.length, TUR)
        : T.sonucYok;
    }

    izgara.innerHTML = sonuc.length
      ? sonuc.map(kartHTML).join('')
      : '<div class="empty-state">' +
          '<h3>' + T.bosBaslik + '</h3>' +
          '<p>' + T.bosMetin + '</p>' +
          '<button class="btn" type="button" data-reset>' + T.filtreleriTemizle + '</button>' +
        '</div>';

    var sifirla = izgara.querySelector('[data-reset]');
    if (sifirla) sifirla.addEventListener('click', temizleFiltreler);

    if (temizle) temizle.hidden = !degistiMi();
    adresiGuncelle();
  }

  function degistiMi() {
    return Object.keys(VARSAYILAN).some(function (k) { return durum[k] !== VARSAYILAN[k]; });
  }

  function temizleFiltreler() {
    durum = Object.assign({}, VARSAYILAN);
    formuYaz();
    ciz();
  }

  /* ---------------------------------------------------------------------
     Form <-> durum
     --------------------------------------------------------------------- */
  function formuOku() {
    kok.querySelectorAll('[data-filter]').forEach(function (el) {
      var ad = el.getAttribute('data-filter');
      durum[ad] = el.type === 'checkbox' ? el.checked : el.value;
    });
  }

  function formuYaz() {
    kok.querySelectorAll('[data-filter]').forEach(function (el) {
      var ad = el.getAttribute('data-filter');
      if (el.type === 'checkbox') {
        el.checked = !!durum[ad];
        el.closest('.chip').classList.toggle('is-active', el.checked);
      } else {
        el.value = durum[ad];
      }
    });
  }

  /* Filtreleri adres çubuğuna yaz — böylece bir arama paylaşılabilir. */
  function adresiGuncelle() {
    if (!window.history || !window.history.replaceState) return;
    var p = new URLSearchParams();
    Object.keys(VARSAYILAN).forEach(function (k) {
      if (durum[k] !== VARSAYILAN[k] && durum[k] !== false && durum[k] !== '') {
        p.set(k, durum[k] === true ? '1' : durum[k]);
      }
    });
    var yeni = location.pathname + (p.toString() ? '?' + p.toString() : '');
    window.history.replaceState(null, '', yeni);
  }

  function adrestenOku() {
    var p = new URLSearchParams(location.search);
    Object.keys(VARSAYILAN).forEach(function (k) {
      if (!p.has(k)) return;
      var v = p.get(k);
      durum[k] = typeof VARSAYILAN[k] === 'boolean' ? (v === '1' || v === 'true') : v;
    });
  }

  /* ---------------------------------------------------------------------
     Bağlama
     --------------------------------------------------------------------- */
  var zamanlayici;
  kok.addEventListener('input', function (e) {
    if (!e.target.matches('[data-filter]')) return;
    formuOku();
    if (e.target.type === 'search') {
      clearTimeout(zamanlayici);
      zamanlayici = setTimeout(ciz, 180);
    } else {
      ciz();
    }
  });

  kok.addEventListener('change', function (e) {
    if (!e.target.matches('[data-filter]')) return;
    if (e.target.type === 'checkbox') {
      e.target.closest('.chip').classList.toggle('is-active', e.target.checked);
    }
    formuOku();
    ciz();
  });

  if (temizle) temizle.addEventListener('click', temizleFiltreler);

  /* Örnek kayıt uyarısı — yalnızca örnek kayıt varsa göster */
  var uyari = document.querySelector('[data-ornek-uyari]');
  if (uyari) uyari.hidden = !veri.some(function (h) { return h.ornek && h.tur === TUR; });

  /* İngilizce sayfada "açıklamalar Türkçe" notu — yalnızca çevirisi olmayan ilan varsa */
  var dilUyari = document.querySelector('[data-lang-uyari]');
  if (dilUyari) dilUyari.hidden = !veri.some(function (h) {
    return h.tur === TUR && h.durum !== 'taslak' && h.aciklama && !h.aciklamaEn;
  });

  adrestenOku();
  formuYaz();
  ciz();

  /* Ana sayfadaki kartların sayaçları için dışa aç */
  window.KE_SAY = function (tur) {
    return veri.filter(function (h) {
      return h.tur === tur && (h.durum === 'yuva-ariyor' || h.durum === 'rezerve');
    }).length;
  };
})();
