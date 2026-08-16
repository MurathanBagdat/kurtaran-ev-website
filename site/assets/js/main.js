/* Kurtaran Ev — arayüz etkileşimleri */
(function () {
  'use strict';

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
      return '₺' + Number(value).toLocaleString('tr-TR');
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
            ? 'Seçtiğiniz tutarla başla'
            : format(value) + ' ile başla';
        }
      });
    });

    if (custom && label) {
      custom.addEventListener('input', function () {
        var value = parseInt(custom.value, 10);
        label.textContent = value > 0 ? format(value) + ' ile başla' : 'Seçtiğiniz tutarla başla';
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
          'Teşekkürler! Bu yerel prototipte form gönderimi henüz bağlı değil.';
      }
      form.reset();
    });
  });

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
