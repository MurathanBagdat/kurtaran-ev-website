/* Kurtaran Ev — tek ilan detay sayfası (ilan.html?id=...) */
(function () {
  'use strict';

  var kok = document.querySelector('[data-animal-detail]');
  if (!kok) return;

  var veri = (window.KE_DATA && window.KE_DATA.hayvanlar) || [];
  var id = new URLSearchParams(location.search).get('id');
  var h = veri.filter(function (a) { return a.id === id; })[0];

  var CINSIYET = { disi: 'Dişi', erkek: 'Erkek' };
  var BOYUT = { kucuk: 'Küçük', orta: 'Orta', buyuk: 'Büyük' };
  var DURUM = {
    'yuva-ariyor': 'Yuva arıyor', 'rezerve': 'Rezerve',
    'yuvalandi': 'Yuvalandı', 'taslak': 'Taslak'
  };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* Taslak ilanlar herkese açık değildir; doğrudan bağlantıyla da açılmamalı. */
  if (!h || h.durum === 'taslak') {
    kok.innerHTML =
      '<div class="empty-state">' +
        '<h1 class="animal-detail__name" style="font-size:2.2rem">İlan bulunamadı</h1>' +
        '<p>Bu ilan kaldırılmış, yuvasına kavuşmuş ya da bağlantı hatalı olabilir.</p>' +
        '<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">' +
        '<a class="btn" href="yuva-arayan-kopekler.html">Yuva arayan köpekler <span aria-hidden="true">→</span></a>' +
        '<a class="btn btn--sky" href="yuva-arayan-kediler.html">Yuva arayan kediler <span aria-hidden="true">→</span></a></div>' +
      '</div>';
    document.title = 'İlan bulunamadı | Kurtaran Ev';
    return;
  }

  document.title = h.isim + ' — yuva arıyor | Kurtaran Ev';
  var aciklama = document.querySelector('meta[name="description"]');
  if (aciklama) aciklama.setAttribute('content', (h.aciklama || '').slice(0, 155));

  function tahmin(alan) {
    return (h.tahmini || []).indexOf(alan) !== -1
      ? ' <span class="spec__est">(tahmini)</span>' : '';
  }

  function uclu(v) {
    if (v === true) return 'Evet';
    if (v === false) return 'Hayır';
    return null;
  }

  function spec(etiket, deger, ekBilgi) {
    var bos = deger == null || deger === '';
    return '<div class="spec">' +
      '<span class="spec__label">' + esc(etiket) + '</span>' +
      '<span class="spec__value' + (bos ? ' unknown' : '') + '">' +
        (bos ? 'Bilinmiyor' : esc(deger) + (ekBilgi || '')) +
      '</span></div>';
  }

  /* --- galeri ------------------------------------------------------------ */
  var fotograflar = h.fotograflar || [];
  var galeri;
  if (fotograflar.length) {
    galeri =
      '<div class="animal-gallery__main"><img id="ana-foto" src="' + esc(fotograflar[0]) +
        '" alt="' + esc(h.isim) + '"></div>' +
      (fotograflar.length > 1
        ? '<div class="animal-gallery__thumbs">' + fotograflar.map(function (f, i) {
            return '<button type="button" data-foto="' + esc(f) + '"' +
              (i === 0 ? ' class="is-active"' : '') +
              ' aria-label="Fotoğraf ' + (i + 1) + '"><img src="' + esc(f) + '" alt=""></button>';
          }).join('') + '</div>'
        : '');
  } else {
    galeri =
      '<div class="animal-gallery__main"><div class="animal-card__placeholder">' +
      '<svg viewBox="0 0 64 64" fill="currentColor" aria-hidden="true">' +
      '<ellipse cx="20" cy="20" rx="7" ry="9"/><ellipse cx="34" cy="15" rx="7" ry="9.5"/>' +
      '<ellipse cx="48" cy="21" rx="6.5" ry="8.5"/><ellipse cx="55" cy="35" rx="6" ry="7.5"/>' +
      '<path d="M34 30c8 0 15 6 15 13 0 6-5 9-11 9-3 0-5-1-8-1s-5 1-8 1c-6 0-11-3-11-9 0-7 7-13 15-13z"/>' +
      '</svg><span>Fotoğraf yakında</span></div></div>';
  }

  /* --- künye ------------------------------------------------------------- */
  var kilo = h.kiloKg == null ? null : String(h.kiloKg).replace('.', ',') + ' kg';
  var specler = [
    spec('Cinsiyet', h.cinsiyet ? CINSIYET[h.cinsiyet] : null),
    spec('Yaş', h.yasMetni, tahmin('yasAy')),
    spec('Cins / ırk', h.cins, tahmin('cins')),
    spec('Kilo', kilo, tahmin('kiloKg')),
    spec('Boyut', h.boyut ? BOYUT[h.boyut] : null, tahmin('boyut')),
    spec('Renk / desen', h.renk),
    spec('Kısırlaştırıldı', uclu(h.kisir)),
    spec('Aşıları tam', uclu(h.asili)),
    spec('Mikroçipli', uclu(h.cipli)),
    spec('Çocuklarla uyumlu', uclu(h.cocuklaUyum)),
    spec('Köpeklerle uyumlu', uclu(h.kopeklerleUyum)),
    spec('Kedilerle uyumlu', uclu(h.kedilerleUyum)),
    spec('Bulunduğu yer', h.konum),
    spec('Özel bakım', uclu(h.ozelBakim))
  ].join('');

  var rozetler = ['<span class="badge badge--' + h.durum + '">' + esc(DURUM[h.durum]) + '</span>'];
  if (h.ornek) rozetler.push('<span class="badge badge--ornek">Örnek kayıt</span>');

  var etiketler = (h.karakter || []).map(function (k) {
    return '<span class="tag">' + esc(k) + '</span>';
  }).join('');

  var kaynak = '';
  if (h.kaynak && h.kaynak.tip === 'instagram' && h.kaynak.baglanti) {
    kaynak = '<p class="animal-detail__source">Bu ilan <a href="' + esc(h.kaynak.baglanti) +
      '" target="_blank" rel="noopener">@' + esc(h.kaynak.hesap) + ' Instagram gönderisinden</a> alındı.</p>';
  } else if (h.ornek) {
    kaynak = '<p class="animal-detail__source">Bu bir örnek kayıttır; gerçek bir ilan değildir.</p>';
  }

  var listeSayfasi = h.tur === 'kedi' ? 'yuva-arayan-kediler.html' : 'yuva-arayan-kopekler.html';
  var listeAdi = h.tur === 'kedi' ? 'Yuva arayan kediler' : 'Yuva arayan köpekler';

  var cta = h.durum === 'yuvalandi'
    ? '<div class="callout callout--sky"><h2 class="callout__title">' + esc(h.isim) +
      ' yuvasına kavuştu 🎉</h2><p class="callout__text">Başka canlar hâlâ bekliyor.</p>' +
      '<div class="callout__actions"><a class="btn btn--white" href="' + listeSayfasi + '">' +
      esc(listeAdi) + ' <span aria-hidden="true">→</span></a></div></div>'
    : '<div class="callout"><h2 class="callout__title">' + esc(h.isim) +
      ' ile tanışmak ister misiniz?</h2>' +
      '<p class="callout__text">Önce sahiplenme sürecini okuyun, sonra bize yazın. ' +
      'Ekibimiz sizinle iletişime geçip ön görüşmeyi planlasın.</p>' +
      '<div class="callout__actions">' +
      '<a class="btn btn--white" href="iletisim.html?ilan=' + encodeURIComponent(h.id) +
      '">Tanışmak istiyorum <span aria-hidden="true">→</span></a>' +
      '<a class="link-arrow" href="sahiplenme-sureci.html">Sahiplenme süreci <span aria-hidden="true">→</span></a>' +
      '</div></div>';

  kok.innerHTML =
    '<div class="animal-gallery">' + galeri + '</div>' +
    '<div>' +
      '<div class="animal-detail__badges">' + rozetler.join('') + '</div>' +
      '<h1 class="animal-detail__name">' + esc(h.isim) + '</h1>' +
      (h.aciklama ? '<p class="animal-detail__lead">' + esc(h.aciklama) + '</p>' : '') +
      (etiketler ? '<div class="animal-card__tags" style="margin-bottom:1.6rem">' + etiketler + '</div>' : '') +
      '<div class="spec-grid">' + specler + '</div>' +
      (h.saglikNotu
        ? '<div class="callout callout--cream" style="box-shadow:none;margin-bottom:1.6rem">' +
          '<h2 class="callout__title" style="font-size:1.3rem">Sağlık notu</h2>' +
          '<p class="callout__text">' + esc(h.saglikNotu) + '</p></div>'
        : '') +
      cta + kaynak +
    '</div>';

  /* Ekmek kırıntısı ve geri bağlantısı */
  var geri = document.querySelector('[data-back-link]');
  if (geri) { geri.setAttribute('href', listeSayfasi); geri.textContent = listeAdi; }

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
