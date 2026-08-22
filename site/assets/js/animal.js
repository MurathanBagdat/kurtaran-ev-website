/* Kurtaran Ev — tek ilan detay sayfası (ilan.html?id=...) */
(function () {
  'use strict';

  var kok = document.querySelector('[data-animal-detail]');
  if (!kok) return;

  var veri = (window.KE_DATA && window.KE_DATA.hayvanlar) || [];
  var EN = document.documentElement.lang === 'en';
  var I18N = window.KE_I18N;                             // assets/js/i18n.js
  var T = I18N.t;
  var BASE = window.KE_BASE || '';                       // site/en/ altında "../"
  var id = new URLSearchParams(location.search).get('id');
  var h = veri.filter(function (a) { return a.id === id; })[0];

  var PATI_SVG =
    '<svg viewBox="0 0 64 64" fill="currentColor" aria-hidden="true">' +
    '<ellipse cx="20" cy="20" rx="7" ry="9"/><ellipse cx="34" cy="15" rx="7" ry="9.5"/>' +
    '<ellipse cx="48" cy="21" rx="6.5" ry="8.5"/><ellipse cx="55" cy="35" rx="6" ry="7.5"/>' +
    '<path d="M34 30c8 0 15 6 15 13 0 6-5 9-11 9-3 0-5-1-8-1s-5 1-8 1c-6 0-11-3-11-9 0-7 7-13 15-13z"/>' +
    '</svg>';

  var CINSIYET = I18N.cinsiyet;
  var BOYUT = I18N.boyut;
  var DURUM = I18N.durum;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* Taslak ilanlar herkese açık değildir; doğrudan bağlantıyla da açılmamalı. */
  if (!h || h.durum === 'taslak') {
    kok.innerHTML =
      '<div class="empty-state">' +
        '<h1 class="animal-detail__name" style="font-size:2.2rem">' + T.ilanYok + '</h1>' +
        '<p>' + T.ilanYokMetin + '</p>' +
        '<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">' +
        '<a class="btn" href="yuva-arayan-kopekler.html">' + T.kopekListesi + ' <span aria-hidden="true">→</span></a>' +
        '<a class="btn btn--sky" href="yuva-arayan-kediler.html">' + T.kediListesi + ' <span aria-hidden="true">→</span></a></div>' +
      '</div>';
    document.title = T.ilanYok + ' | Kurtaran Ev';
    return;
  }

  document.title = h.isim + T.basliEki + ' | Kurtaran Ev';
  var metaAciklama = document.querySelector('meta[name="description"]');
  if (metaAciklama) metaAciklama.setAttribute('content', (I18N.alan(h, 'aciklama') || '').slice(0, 155));

  function tahmin(alan) {
    return (h.tahmini || []).indexOf(alan) !== -1
      ? ' <span class="spec__est">' + T.tahmini + '</span>' : '';
  }

  function uclu(v) {
    if (v === true) return T.evet;
    if (v === false) return T.hayir;
    return null;
  }

  function spec(etiket, deger, ekBilgi) {
    var bos = deger == null || deger === '';
    return '<div class="spec">' +
      '<span class="spec__label">' + esc(etiket) + '</span>' +
      '<span class="spec__value' + (bos ? ' unknown' : '') + '">' +
        (bos ? T.bilinmiyor : esc(deger) + (ekBilgi || '')) +
      '</span></div>';
  }

  /* --- galeri ------------------------------------------------------------ */
  var fotograflar = h.fotograflar || [];
  var galeri;
  if (fotograflar.length) {
    galeri =
      '<div class="animal-gallery__main"><img id="ana-foto" src="' + esc(BASE + fotograflar[0]) +
        '" alt="' + esc(h.isim) + '"></div>' +
      (fotograflar.length > 1
        ? '<div class="animal-gallery__thumbs">' + fotograflar.map(function (f, i) {
            return '<button type="button" data-foto="' + esc(BASE + f) + '"' +
              (i === 0 ? ' class="is-active"' : '') +
              ' aria-label="' + T.fotograf + ' ' + (i + 1) + '"><img src="' + esc(BASE + f) + '" alt=""></button>';
          }).join('') + '</div>'
        : '');
  } else {
    galeri =
      '<div class="animal-gallery__main"><div class="animal-card__placeholder">' +
      PATI_SVG + '<span>' + T.fotoYakinda + '</span></div></div>';
  }

  /* --- künye ------------------------------------------------------------- */
  var kilo = h.kiloKg == null ? null : String(h.kiloKg).replace('.', EN ? '.' : ',') + ' kg';
  var specler = [
    spec(T.sCinsiyet, h.cinsiyet ? CINSIYET[h.cinsiyet] : null),
    spec(T.sYas, I18N.yasMetni(h), tahmin('yasAy')),
    spec(T.sCins, I18N.alan(h, 'cins'), tahmin('cins')),
    spec(T.sKilo, kilo, tahmin('kiloKg')),
    spec(T.sBoyut, h.boyut ? BOYUT[h.boyut] : null, tahmin('boyut')),
    spec(T.sRenk, I18N.alan(h, 'renk')),
    spec(T.sKisir, uclu(h.kisir)),
    spec(T.sAsili, uclu(h.asili)),
    spec(T.sCocuk, uclu(h.cocuklaUyum)),
    spec(T.sKopek, uclu(h.kopeklerleUyum)),
    spec(T.sKedi, uclu(h.kedilerleUyum)),
    spec(T.sOzelBakim, uclu(h.ozelBakim))
  ].join('');

  var rozetler = ['<span class="badge badge--' + h.durum + '">' + esc(DURUM[h.durum]) + '</span>'];
  if (h.ornek) rozetler.push('<span class="badge badge--ornek">' + T.ornekKayit + '</span>');

  var karakterler = I18N.alan(h, 'karakter') || [];
  var etiketler = karakterler.map(function (k) {
    return '<span class="tag">' + esc(h.karakterEn && EN ? k : I18N.karakter(k)) + '</span>';
  }).join('');

  /* Açıklama: İngilizce alan varsa o; yoksa Türkçesi + kısa not. */
  var aciklama = I18N.alan(h, 'aciklama');
  var aciklamaTr = EN && !!aciklama && !h.aciklamaEn;

  var kaynakIc = '';
  if (h.kaynak && h.kaynak.tip === 'instagram' && h.kaynak.baglanti) {
    /* Yalnızca hesap adı bağlantı olsun; "gönderisinden" altı çizili görünmesin. */
    kaynakIc = T.kaynakInstagram('<a href="' + esc(h.kaynak.baglanti) +
      '" target="_blank" rel="noopener">@' + esc(h.kaynak.hesap) + '</a>');
  } else if (h.ornek) {
    kaynakIc = T.kaynakOrnek;
  }

  var listeSayfasi = h.tur === 'kedi' ? 'yuva-arayan-kediler.html' : 'yuva-arayan-kopekler.html';
  var listeAdi = h.tur === 'kedi' ? T.kediListesi : T.kopekListesi;

  /* İletişim sayfasına ilan bilgisini ve niyeti taşıyan bağlantı */
  function iletisimBaglantisi(konu) {
    return 'iletisim.html?ilan=' + encodeURIComponent(h.id) +
      '&ad=' + encodeURIComponent(h.isim) +
      (konu ? '&konu=' + encodeURIComponent(konu) : '') + '#kanallar';
  }

  /* Yuva arayan canlarda çağrı bloğu ve kaynak notu sayfanın altındaki yatay banttadır;
     sağ sütunda yalnızca yuvalanma müjdesi kalır. */
  var bant = document.querySelector('[data-meet-band]');
  var bantAktif = !!bant && h.durum !== 'yuvalandi';

  var cta = h.durum === 'yuvalandi'
    ? '<div class="callout callout--sky"><h2 class="callout__title">' + esc(h.isim) +
      T.yuvalandiBaslik + '</h2><p class="callout__text">' + T.yuvalandiMetin + '</p>' +
      '<div class="callout__actions"><a class="btn btn--white" href="' + listeSayfasi + '">' +
      esc(listeAdi) + ' <span aria-hidden="true">→</span></a></div></div>'
    : '';

  kok.innerHTML =
    '<div class="animal-gallery">' + galeri + '</div>' +
    '<div>' +
      '<div class="animal-detail__badges">' + rozetler.join('') + '</div>' +
      '<h1 class="animal-detail__name">' + esc(h.isim) + '</h1>' +
      (aciklama ? '<p class="animal-detail__lead"' + (aciklamaTr ? ' lang="tr"' : '') + '>' + esc(aciklama) + '</p>' +
        (aciklamaTr ? '<p class="animal-detail__note">' + T.aciklamaTurkce + '</p>' : '') : '') +
      (etiketler ? '<div class="animal-card__tags" style="margin-bottom:1.6rem">' + etiketler + '</div>' : '') +
      '<div class="spec-grid">' + specler + '</div>' +
      (h.saglikNotu
        ? '<div class="callout callout--cream" style="box-shadow:none;margin-bottom:1.6rem">' +
          '<h2 class="callout__title" style="font-size:1.3rem">' + T.saglikNotu + '</h2>' +
          '<p class="callout__text"' + (EN && !h.saglikNotuEn ? ' lang="tr"' : '') + '>' + esc(I18N.alan(h, 'saglikNotu')) + '</p></div>'
        : '') +
      cta +
      (!bantAktif && kaynakIc ? '<p class="animal-detail__source">' + kaynakIc + '</p>' : '') +
    '</div>';

  /* Ekmek kırıntısı ve geri bağlantısı */
  var geri = document.querySelector('[data-back-link]');
  if (geri) { geri.setAttribute('href', listeSayfasi); geri.textContent = listeAdi; }

  /* Sayfanın altındaki yatay çağrı bandı — yuvalanmış canlarda gösterilmez */
  if (bantAktif) {
    var bantBaslik = bant.querySelector('[data-meet-title]');
    if (bantBaslik) bantBaslik.textContent = T.tanismak(h.isim);

    /* Seçenekler ilanı iletişim formuna taşısın */
    bant.querySelectorAll('[data-meet-option]').forEach(function (baglanti) {
      baglanti.setAttribute('href', iletisimBaglantisi(baglanti.getAttribute('data-meet-option')));
    });

    var bantKaynak = bant.querySelector('[data-meet-source]');
    if (bantKaynak && kaynakIc) { bantKaynak.innerHTML = kaynakIc; bantKaynak.hidden = false; }

    bant.hidden = false;
  }

  /* ---------------------------------------------------------------------
     İlanlar arası geçiş
     Aynı türün herkese açık ilanları, katalogdaki varsayılan sırayla:
     önce yeni eklenenler, yuvalananlar en sonda.
     --------------------------------------------------------------------- */
  var kardesler = veri
    .filter(function (a) { return a.tur === h.tur && a.durum !== 'taslak'; })
    .sort(function (a, b) { return (b.olusturma || '').localeCompare(a.olusturma || ''); })
    .sort(function (a, b) {
      return (a.durum === 'yuvalandi' ? 1 : 0) - (b.durum === 'yuvalandi' ? 1 : 0);
    });

  var sira = kardesler.map(function (a) { return a.id; }).indexOf(h.id);

  function ilanBaglantisi(a) { return 'ilan.html?id=' + encodeURIComponent(a.id); }

  /* --- önceki / sonraki --- */
  var pager = document.querySelector('[data-pager]');
  if (pager && sira !== -1 && kardesler.length > 1) {
    /* Uçlarda başa/sona sarılır; böylece ok her zaman bir yere götürür. */
    var onceki = kardesler[(sira - 1 + kardesler.length) % kardesler.length];
    var sonraki = kardesler[(sira + 1) % kardesler.length];

    [['[data-pager-prev]', onceki], ['[data-pager-next]', sonraki]].forEach(function (c) {
      var el = pager.querySelector(c[0]);
      if (!el) return;
      el.setAttribute('href', ilanBaglantisi(c[1]));
      el.setAttribute('title', c[1].isim);
      var ad = el.querySelector('.pager__name');
      if (ad) ad.textContent = c[1].isim;
    });

    var sayac = pager.querySelector('[data-pager-count]');
    if (sayac) sayac.textContent = (sira + 1) + ' / ' + kardesler.length;
    pager.hidden = false;
  }

  /* --- "Diğer yuva arayanlar" kart şeridi --- */
  var digerBolum = document.querySelector('[data-others]');
  var digerIzgara = digerBolum && digerBolum.querySelector('[data-others-grid]');
  if (digerIzgara && kardesler.length > 1) {
    /* Bu ilandan sonraki üç can; liste bitince başa döner. */
    var digerleri = [];
    for (var i = 1; i < kardesler.length && digerleri.length < 3; i++) {
      digerleri.push(kardesler[(Math.max(sira, 0) + i) % kardesler.length]);
    }

    digerIzgara.innerHTML = digerleri.map(function (a) {
      var gorsel = (a.fotograflar && a.fotograflar[0])
        ? '<img src="' + esc(BASE + a.fotograflar[0]) + '" alt="' + esc(a.isim) + '" loading="lazy">'
        : '<div class="animal-card__placeholder">' + PATI_SVG + '<span>' + T.fotoYakinda + '</span></div>';

      var yasA = I18N.yasMetni(a);
      var bilgiler = [
        a.cinsiyet ? '<li>' + esc(CINSIYET[a.cinsiyet]) + '</li>'
          : '<li class="unknown">' + T.cinsiyetBilinmiyor + '</li>',
        yasA ? '<li>' + esc(yasA) + '</li>'
          : '<li class="unknown">' + T.yasBilinmiyor + '</li>'
      ].join('');

      return '<a class="animal-card" href="' + ilanBaglantisi(a) + '">' +
        '<div class="animal-card__media">' + gorsel +
          '<div class="animal-card__badges"><span class="badge badge--' + a.durum + '">' +
          esc(DURUM[a.durum] || a.durum) + '</span></div>' +
        '</div>' +
        '<div class="animal-card__body">' +
          '<h3 class="animal-card__name">' + esc(a.isim) + '</h3>' +
          '<ul class="animal-card__facts">' + bilgiler + '</ul>' +
          '<span class="animal-card__cta">' + T.ilaniGor + ' <span aria-hidden="true">→</span></span>' +
        '</div></a>';
    }).join('');

    var digerBaslik = digerBolum.querySelector('[data-others-title]');
    if (digerBaslik) {
      digerBaslik.textContent = h.tur === 'kedi' ? T.digerKediler : T.digerKopekler;
    }
    var digerTumu = digerBolum.querySelector('[data-others-all]');
    if (digerTumu) digerTumu.setAttribute('href', listeSayfasi);

    digerBolum.hidden = false;
  }

  /* Galeri geçişi */
  var thumbs = kok.querySelector('.animal-gallery__thumbs');
  if (thumbs) {
    thumbs.addEventListener('click', function (e) {
      var dugme = e.target.closest('[data-foto]');
      if (!dugme) return;
      kok.querySelector('#ana-foto').src = dugme.getAttribute('data-foto');
      thumbs.querySelectorAll('button').forEach(function (b) { b.classList.remove('is-active'); });
      dugme.classList.add('is-active');
    });
  }
})();
