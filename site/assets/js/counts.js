/* Ana sayfa ve Sahiplen sayfasındaki kartlarda canlı ilan sayısını gösterir. */
(function () {
  'use strict';
  var veri = (window.KE_DATA && window.KE_DATA.hayvanlar) || [];

  function say(tur) {
    return veri.filter(function (h) {
      return h.tur === tur && (h.durum === 'yuva-ariyor' || h.durum === 'rezerve');
    }).length;
  }

  document.querySelectorAll('[data-sayac]').forEach(function (el) {
    var tur = el.getAttribute('data-sayac');
    var n = say(tur);
    if (!n) return;                       // ilan yoksa varsayılan metin kalsın
    el.textContent = n + (tur === 'kedi' ? ' kedi' : ' köpek') + ' yuva arıyor';
  });
})();
