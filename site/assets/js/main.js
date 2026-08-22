/* Kurtaran Ev — arayüz etkileşimleri */
(function () {
  'use strict';
  var T = window.KE_I18N.t;                               // assets/js/i18n.js

  var isTouchLayout = function () {
    return window.matchMedia('(max-width: 980px)').matches;
  };

  /* ---------------------------------------------------------------------
     Ana menü: açılır paneller
     Masaüstünde hover CSS ile, tıklama/klavye ile de açılıp kapanır.
     --------------------------------------------------------------------- */
  var navItems = Array.prototype.slice.call(document.querySelectorAll('.nav__item--has-menu'));

  function closeAllMenus(except) {
    navItems.forEach(function (item) {
      if (item === except) return;
      item.classList.remove('is-open');
      var btn = item.querySelector('.nav__link');
      if (btn) btn.setAttribute('aria-expanded', 'false');
    });
  }

  navItems.forEach(function (item) {
    var toggle = item.querySelector('.nav__link');
    if (!toggle) return;

    toggle.addEventListener('click', function (event) {
      event.preventDefault();
      var willOpen = !item.classList.contains('is-open');
      closeAllMenus(item);
      item.classList.toggle('is-open', willOpen);
      toggle.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    });

    item.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        item.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });

    item.addEventListener('focusout', function (event) {
      if (isTouchLayout()) return;
      if (!item.contains(event.relatedTarget)) {
        item.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  });

  /* ---------------------------------------------------------------------
     Dil seçici
     --------------------------------------------------------------------- */
  var lang = document.querySelector('.lang');
  if (lang) {
    var langToggle = lang.querySelector('.lang__toggle');
    langToggle.addEventListener('click', function (event) {
      event.stopPropagation();
      var open = lang.classList.toggle('is-open');
      langToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    lang.querySelectorAll('.lang__option[aria-disabled="true"]').forEach(function (option) {
      option.addEventListener('click', function (event) {
        event.preventDefault();
      });
    });

    /* Sorgu dizesini ve çıpayı diğer dile taşı. Dil bağlantıları sayfa üretilirken
       yazıldığı için sabittir; /en/ilan.html?id=... üzerinden TR'ye geçince ?id
       düşüyor ve "İlan bulunamadı" çıkıyordu. Katalog filtreleri de böylece korunur
       (filtre değerleri dilden bağımsız anahtarlar). */
    var ek = window.location.search + window.location.hash;
    if (ek) {
      lang.querySelectorAll('.lang__option[href]').forEach(function (option) {
        var href = option.getAttribute('href');
        if (!href || href.charAt(0) === '#') return;      // EN sayfası yoksa href="#"
        option.setAttribute('href', href.replace(/[?#].*$/, '') + ek);
      });
    }
  }

  /* ---------------------------------------------------------------------
     Mobil menü
     --------------------------------------------------------------------- */
  var navToggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* Dışarı tıklayınca kapat */
  document.addEventListener('click', function (event) {
    if (!event.target.closest('.nav__item--has-menu')) closeAllMenus(null);
    if (lang && !event.target.closest('.lang')) {
      lang.classList.remove('is-open');
      var lt = lang.querySelector('.lang__toggle');
      if (lt) lt.setAttribute('aria-expanded', 'false');
    }
  });

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    closeAllMenus(null);
    if (lang) lang.classList.remove('is-open');
    if (nav && navToggle) {
      nav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });

  /* ---------------------------------------------------------------------
     Bağış tutarı seçici
     --------------------------------------------------------------------- */
  document.querySelectorAll('[data-amounts]').forEach(function (group) {
    var buttons = Array.prototype.slice.call(group.querySelectorAll('.amount'));
    var label = document.querySelector(group.getAttribute('data-amount-target') || '');
    var custom = group.querySelector('.amount-custom');

    function format(value) {
      return '₺' + Number(value).toLocaleString(window.KE_I18N.sayi);
    }

    buttons.forEach(function (button) {
      button.addEventListener('click', function () {
        buttons.forEach(function (b) {
          b.classList.remove('is-active');
          b.setAttribute('aria-pressed', 'false');
        });
        button.classList.add('is-active');
        button.setAttribute('aria-pressed', 'true');

        var value = button.getAttribute('data-amount');
        if (custom) custom.hidden = value !== 'custom';
        if (custom && value === 'custom') custom.focus();

        if (label) {
          label.textContent = value === 'custom'
            ? T.tutarSec
            : T.ileBasla(format(value));
        }
      });
    });

    if (custom && label) {
      custom.addEventListener('input', function () {
        var value = parseInt(custom.value, 10);
        label.textContent = value > 0 ? T.ileBasla(format(value)) : T.tutarSec;
      });
    }
  });

  /* ---------------------------------------------------------------------
     SSS akordiyonu
     --------------------------------------------------------------------- */
  document.querySelectorAll('.faq__q').forEach(function (question) {
    question.addEventListener('click', function () {
      var item = question.closest('.faq__item');
      var open = item.classList.toggle('is-open');
      question.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* ---------------------------------------------------------------------
     Formlar — yerel prototipte gönderim yok, geri bildirim veriyoruz
     --------------------------------------------------------------------- */
  document.querySelectorAll('form[data-demo-form]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var status = form.querySelector('.form-status');
      if (status) {
        status.textContent = form.getAttribute('data-demo-message') ||
          T.formVarsayilan;
      }
      form.reset();
    });
  });

  /* ---------------------------------------------------------------------
     İlan sayfasından gelen ziyaretçi: konu ve mesaj alanını hazırla
     (iletisim.html?ilan=...&ad=...&konu=...)
     --------------------------------------------------------------------- */
  var konuAlani = document.getElementById('il-konu');
  var mesajAlani = document.getElementById('il-mesaj');
  if (konuAlani || mesajAlani) {
    var sorgu = new URLSearchParams(location.search);
    var ilanAdi = sorgu.get('ad');
    var ilanKonu = sorgu.get('konu');

    if (konuAlani && ilanKonu) {
      var uygun = Array.prototype.slice.call(konuAlani.options).some(function (o) {
        return o.value === ilanKonu;
      });
      if (uygun) konuAlani.value = ilanKonu;
    }

    if (mesajAlani && ilanAdi && !mesajAlani.value) {
      var CUMLE = {
        'sahiplenme': T.cumleSahiplenme,
        'gecici-yuva': T.cumleGeciciYuva,
        'koruyucu-melek': T.cumleKoruyucuMelek
      };
      mesajAlani.value = T.cumleSelam + ilanAdi +
        (CUMLE[ilanKonu] || T.cumleTanisma) + T.cumleSon;
    }
  }

  /* ---------------------------------------------------------------------
     Aktif menü öğesini işaretle
     --------------------------------------------------------------------- */
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.dropdown__link, .nav__link[href]').forEach(function (link) {
    if (link.getAttribute('href') === here) {
      link.setAttribute('aria-current', 'page');
      var parent = link.closest('.nav__item');
      if (parent) {
        var top = parent.querySelector('.nav__link');
        if (top) top.setAttribute('aria-current', 'page');
      }
    }
  });
})();
