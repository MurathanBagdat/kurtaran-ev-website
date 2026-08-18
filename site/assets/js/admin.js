/* Kurtaran Ev — yönetim paneli.
   İki kipte çalışır:
   - yerel:  tools/server.py sunucusuyla konuşur (şifreyle giriş).
   - github: sunucu yoksa (ör. GitHub Pages) admin-github.js üzerinden
             doğrudan GitHub API'sine yazar (fine-grained jetonla giriş).
             Her kayıt bir commit olur; Actions siteyi yeniden yayınlar. */
(function () {
  'use strict';

  var kok = document.getElementById('admin');
  if (!kok) return;

  var JETON_ANAHTAR = 'ke_admin_jeton';
  var GH_ANAHTAR = 'ke_gh_jeton';
  var jeton = sessionStorage.getItem(JETON_ANAHTAR) || '';
  var mod = 'yerel';         // 'yerel' | 'github'
  var gh = null;             // KE_GH arka ucu (yalnızca github kipinde)
  var sema = null;
  var hayvanlar = [];
  var suanki = null;         // düzenlenen kayıt

  /* --------------------------------------------------------------------- */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function bildir(mesaj, hata) {
    var t = document.getElementById('toast');
    t.textContent = mesaj;
    t.classList.toggle('toast--hata', !!hata);
    t.hidden = false;
    clearTimeout(t._z);
    t._z = setTimeout(function () { t.hidden = true; }, hata ? 6000 : 3000);
  }

  function api(yol, secenekler) {
    secenekler = secenekler || {};
    var baslik = { 'Content-Type': 'application/json' };
    if (jeton) baslik.Authorization = 'Bearer ' + jeton;
    return fetch('/api/' + yol, {
      method: secenekler.method || 'GET',
      headers: baslik,
      body: secenekler.body ? JSON.stringify(secenekler.body) : undefined
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (govde) {
        if (!r.ok) throw new Error(govde.hata || ('Sunucu hatası (' + r.status + ')'));
        return govde;
      });
    });
  }

  /* --------------------------------------------------------------------- */
  /* Açılış: sunucu var mı?                                                 */
  /* --------------------------------------------------------------------- */
  function baslat() {
    fetch('/api/durum')
      .then(function (r) { if (!r.ok) throw new Error('yok'); return r.json(); })
      .then(function (d) {
        if (!d || !d.calisiyor) throw new Error('yok');
        return api('sema').then(function (s) { sema = s; });
      })
      .then(function () {
        if (jeton) {
          return api('hayvanlar')
            .then(function (d) { hayvanlar = d.hayvanlar; panelCiz(); })
            .catch(function () { jeton = ''; sessionStorage.removeItem(JETON_ANAHTAR); girisCiz(); });
        }
        girisCiz();
      })
      .catch(githubBaslat);
  }

  /* Yerel sunucu yok → GitHub kipi. Şema statik dosyadan gelir. */
  function githubBaslat() {
    if (!window.KE_GH) return cevrimdisiCiz();
    gh = window.KE_GH();
    fetch('assets/data/sema.json', { cache: 'no-store' })
      .then(function (r) { if (!r.ok) throw new Error('yok'); return r.json(); })
      .then(function (s) {
        sema = s;
        mod = 'github';
        var kayitli = localStorage.getItem(GH_ANAHTAR) || sessionStorage.getItem(GH_ANAHTAR);
        if (kayitli) {
          return gh.girisYap(kayitli)
            .then(function () { return gh.hayvanlarYukle(); })
            .then(function (liste) { hayvanlar = liste; panelCiz(); })
            .catch(function () {
              localStorage.removeItem(GH_ANAHTAR);
              sessionStorage.removeItem(GH_ANAHTAR);
              githubGirisCiz();
            });
        }
        githubGirisCiz();
      })
      .catch(cevrimdisiCiz);
  }

  function cevrimdisiCiz() {
    kok.innerHTML =
      '<div class="container admin">' +
        '<h1 class="admin__title">Yönetim paneli</h1>' +
        '<p class="admin__sub" style="margin-bottom:24px">Bu sayfa yerel sunucu üzerinden açılmalı.</p>' +
        '<div class="admin__offline">' +
          '<p><b>Sunucu çalışmıyor.</b> Panel, ilanları kaydedebilmek için ' +
          '<code>tools/server.py</code> sunucusuna ihtiyaç duyar. Terminalde proje klasöründe:</p>' +
          '<p style="margin:.9rem 0"><code>python3 tools/server.py</code></p>' +
          '<p>Sonra <code>http://127.0.0.1:8000/admin.html</code> adresini açın. ' +
          'Dosyaya çift tıklayarak açtığınızda (file://) tarayıcı sunucuya ulaşamaz.</p>' +
        '</div>' +
      '</div>';
  }

  /* --------------------------------------------------------------------- */
  /* Giriş                                                                  */
  /* --------------------------------------------------------------------- */
  function girisCiz() {
    kok.innerHTML =
      '<div class="container">' +
        '<form class="login" id="giris-form">' +
          '<h1>Yönetim paneli</h1>' +
          '<p>İlan eklemek, düzenlemek ve silmek için giriş yapın.</p>' +
          '<div class="field">' +
            '<label for="sifre">Şifre</label>' +
            '<input id="sifre" type="password" autocomplete="current-password" required autofocus>' +
          '</div>' +
          '<button class="btn" type="submit">Giriş yap <span aria-hidden="true">→</span></button>' +
          '<p class="form-status" role="status" id="giris-durum"></p>' +
        '</form>' +
      '</div>';

    document.getElementById('giris-form').addEventListener('submit', function (e) {
      e.preventDefault();
      var durum = document.getElementById('giris-durum');
      durum.textContent = 'Kontrol ediliyor…';
      api('giris', { method: 'POST', body: { sifre: document.getElementById('sifre').value } })
        .then(function (d) {
          jeton = d.jeton;
          sessionStorage.setItem(JETON_ANAHTAR, jeton);
          return api('hayvanlar');
        })
        .then(function (d) { hayvanlar = d.hayvanlar; panelCiz(); })
        .catch(function (err) { durum.textContent = err.message; });
    });
  }

  /* GitHub kipi girişi — şifre yerine fine-grained jeton. */
  function githubGirisCiz() {
    kok.innerHTML =
      '<div class="container">' +
        '<form class="login" id="giris-form">' +
          '<h1>Yönetim paneli</h1>' +
          '<p>Bu panel değişiklikleri doğrudan GitHub\'a kaydeder. ' +
            'Giriş için GitHub erişim jetonunuzu yapıştırın.</p>' +
          '<div class="field">' +
            '<label for="gh-jeton">GitHub jetonu</label>' +
            '<input id="gh-jeton" type="password" autocomplete="off" required autofocus ' +
              'placeholder="github_pat_…">' +
          '</div>' +
          '<div class="field">' +
            '<label style="font-weight:normal"><input type="checkbox" id="gh-hatirla" checked> ' +
              'Bu cihazda hatırla</label>' +
          '</div>' +
          '<button class="btn" type="submit">Giriş yap <span aria-hidden="true">→</span></button>' +
          '<p class="form-status" role="status" id="giris-durum"></p>' +
          '<details style="margin-top:1rem">' +
            '<summary>Jeton nasıl alınır?</summary>' +
            '<ol style="margin:.6rem 0 0 1.2rem;font-size:.9em;line-height:1.6">' +
              '<li><a href="https://github.com/settings/personal-access-tokens/new" target="_blank" rel="noopener">' +
                'github.com/settings/personal-access-tokens/new</a> adresini açın.</li>' +
              '<li><b>Repository access</b> → Only select repositories → ' +
                '<code>' + esc(gh.ayar.repo) + '</code> seçin.</li>' +
              '<li><b>Permissions</b> → Contents: <b>Read and write</b>' +
                ' · Actions: <b>Read and write</b> (Instagram senkronu için).</li>' +
              '<li>Jetonu oluşturup buraya yapıştırın.</li>' +
            '</ol>' +
          '</details>' +
        '</form>' +
      '</div>';

    document.getElementById('giris-form').addEventListener('submit', function (e) {
      e.preventDefault();
      var durum = document.getElementById('giris-durum');
      durum.textContent = 'Kontrol ediliyor…';
      var girilen = document.getElementById('gh-jeton').value;
      gh.girisYap(girilen)
        .then(function () {
          var depo = document.getElementById('gh-hatirla').checked ? localStorage : sessionStorage;
          depo.setItem(GH_ANAHTAR, girilen.trim());
          return gh.hayvanlarYukle();
        })
        .then(function (liste) { hayvanlar = liste; panelCiz(); })
        .catch(function (err) { durum.textContent = err.message; });
    });
  }

  /* --------------------------------------------------------------------- */
  /* Panel                                                                  */
  /* --------------------------------------------------------------------- */
  function say(kosul) { return hayvanlar.filter(kosul).length; }

  function panelCiz() {
    kok.innerHTML =
      '<div class="container admin">' +
        '<div class="admin__head">' +
          '<div>' +
            '<h1 class="admin__title">İlan yönetimi</h1>' +
            '<p class="admin__sub">Tüm kayıtlar — taslaklar dahil' +
              (mod === 'github' ? ' · GitHub üzerinden: kayıtlar 1-2 dk içinde yayına girer' : '') +
            '</p>' +
          '</div>' +
          '<div class="admin__stats">' +
            '<div><b>' + hayvanlar.length + '</b>toplam</div>' +
            '<div><b>' + say(function (a) { return a.durum === 'yuva-ariyor'; }) + '</b>yuva arıyor</div>' +
            '<div><b>' + say(function (a) { return a.durum === 'taslak'; }) + '</b>taslak</div>' +
            '<div><b>' + say(function (a) { return a.ornek; }) + '</b>örnek</div>' +
          '</div>' +
        '</div>' +

        '<div class="admin__tools">' +
          '<button class="btn btn--sm" type="button" id="yeni">+ Yeni ilan</button>' +
          '<button class="btn-mini" type="button" id="ig-sync">Instagram\'dan çek</button>' +
          '<button class="btn-mini" type="button" id="ornek-sil">Örnek kayıtları sil</button>' +
          '<select class="btn-mini" id="suz-durum" aria-label="Duruma göre süz">' +
            '<option value="">Tüm durumlar</option>' +
            Object.keys(sema.durumlar).map(function (k) {
              return '<option value="' + k + '">' + esc(sema.durumlar[k]) + '</option>';
            }).join('') +
          '</select>' +
          '<select class="btn-mini" id="suz-tur" aria-label="Türe göre süz">' +
            '<option value="">Tüm türler</option><option value="kopek">Köpek</option><option value="kedi">Kedi</option>' +
          '</select>' +
          '<span class="spacer"></span>' +
          '<a class="btn-mini" href="index.html">Siteye dön</a>' +
          '<button class="btn-mini" type="button" id="cikis">Çıkış</button>' +
        '</div>' +

        '<pre class="console" id="konsol" hidden></pre>' +
        '<div id="liste"></div>' +
      '</div>' +
      kipHTML() +
      '<div class="toast" id="toast" hidden role="status"></div>';

    document.getElementById('yeni').addEventListener('click', function () { kipAc(null); });
    document.getElementById('cikis').addEventListener('click', cikis);
    document.getElementById('ig-sync').addEventListener('click', instagramCek);
    document.getElementById('ornek-sil').addEventListener('click', ornekleriSil);
    document.getElementById('suz-durum').addEventListener('change', listeCiz);
    document.getElementById('suz-tur').addEventListener('change', listeCiz);
    kipBagla();

    /* Tıklama dinleyicisi kalıcı kapsayıcıya bağlanır; listeCiz() yalnızca
       içeriği yeniler, dinleyici hayatta kalır. */
    document.getElementById('liste').addEventListener('click', function (e) {
      var duzenle = e.target.closest('[data-duzenle]');
      var silBtn = e.target.closest('[data-sil]');
      if (duzenle) {
        var id = duzenle.getAttribute('data-duzenle');
        kipAc(hayvanlar.filter(function (a) { return a.id === id; })[0]);
      } else if (silBtn) {
        sil(silBtn.getAttribute('data-sil'));
      }
    });

    listeCiz();
  }

  function listeCiz() {
    var d = document.getElementById('suz-durum').value;
    var t = document.getElementById('suz-tur').value;
    var liste = hayvanlar.filter(function (a) {
      return (!d || a.durum === d) && (!t || a.tur === t);
    });

    if (!liste.length) {
      document.getElementById('liste').innerHTML =
        '<div class="empty-state"><h3>Kayıt yok</h3><p>Bu süzgeçle eşleşen ilan bulunamadı.</p></div>';
      return;
    }

    document.getElementById('liste').innerHTML =
      '<table class="admin-table"><thead><tr>' +
        '<th style="width:70px">Foto</th><th>İlan</th><th>Tür</th><th>Durum</th><th>Kaynak</th><th></th>' +
      '</tr></thead><tbody>' +
      liste.map(function (a) {
        var foto = (a.fotograflar && a.fotograflar[0])
          ? '<img class="admin-table__thumb" src="' + esc(a.fotograflar[0]) + '" alt="">'
          : '<div class="admin-table__thumb admin-table__thumb--empty">foto yok</div>';
        var kaynak = a.ornek ? 'Örnek'
          : (a.kaynak && a.kaynak.tip === 'instagram' ? '@' + esc(a.kaynak.hesap) : 'Elle');
        var ozet = [
          a.cinsiyet ? sema.alanlar.cinsiyet.secenekler[a.cinsiyet] : null,
          a.yasMetni, a.cins
        ].filter(Boolean).join(' · ') || 'bilgi yok';
        return '<tr>' +
          '<td>' + foto + '</td>' +
          '<td><div class="admin-table__name">' + esc(a.isim) + '</div>' +
              '<div class="admin-table__meta">' + esc(ozet) + '</div></td>' +
          '<td>' + (a.tur === 'kedi' ? 'Kedi' : 'Köpek') + '</td>' +
          '<td><span class="badge badge--' + a.durum + '">' + esc(sema.durumlar[a.durum]) + '</span></td>' +
          '<td class="admin-table__meta">' + kaynak + '</td>' +
          '<td><div class="admin-table__actions">' +
            '<button class="btn-mini" type="button" data-duzenle="' + esc(a.id) + '">Düzenle</button>' +
            '<button class="btn-mini btn-mini--danger" type="button" data-sil="' + esc(a.id) + '">Sil</button>' +
          '</div></td>' +
        '</tr>';
      }).join('') + '</tbody></table>';

  }

  /* --------------------------------------------------------------------- */
  /* Form — şemadan üretilir                                                */
  /* --------------------------------------------------------------------- */
  function kipHTML() {
    return '' +
      '<div class="modal" id="kip" hidden role="dialog" aria-modal="true" aria-labelledby="kip-baslik">' +
        '<div class="modal__panel">' +
          '<div class="modal__head">' +
            '<h2 class="modal__title" id="kip-baslik">İlan</h2>' +
            '<button class="modal__close" type="button" id="kip-kapat" aria-label="Kapat">×</button>' +
          '</div>' +
          '<form id="kip-form"><div class="modal__body" id="kip-govde"></div>' +
            '<div class="modal__foot">' +
              '<button class="btn" type="submit">Kaydet</button>' +
              '<button class="btn-mini" type="button" id="kip-iptal">İptal</button>' +
              '<span class="form-status" id="kip-durum" role="status"></span>' +
            '</div>' +
          '</form>' +
        '</div>' +
      '</div>';
  }

  function alanHTML(ad, tanim, deger, tahminiMi) {
    var id = 'f-' + ad;
    var ipucu = tanim.ipucu ? '<small>' + esc(tanim.ipucu) + '</small>' : '';
    var genislik = (tanim.tip === 'uzunmetin') ? ' span-3'
                 : (tanim.tip === 'etiketler') ? ' span-3' : '';
    var ic;

    if (tanim.tip === 'secim') {
      var bos = (ad === 'tur' || ad === 'durum') ? '' : '<option value="">— bilinmiyor —</option>';
      ic = '<select id="' + id + '" name="' + ad + '">' + bos +
        Object.keys(tanim.secenekler).map(function (k) {
          return '<option value="' + k + '"' + (deger === k ? ' selected' : '') + '>' +
            esc(tanim.secenekler[k]) + '</option>';
        }).join('') + '</select>';
    } else if (tanim.tip === 'uclu') {
      ic = '<div class="field-tri">' +
        [['', 'Bilinmiyor'], ['evet', 'Evet'], ['hayir', 'Hayır']].map(function (s) {
          var secili = (deger === true && s[0] === 'evet') ||
                       (deger === false && s[0] === 'hayir') ||
                       (deger == null && s[0] === '');
          return '<label><input type="radio" name="' + ad + '" value="' + s[0] + '"' +
            (secili ? ' checked' : '') + '>' + s[1] + '</label>';
        }).join('') + '</div>';
    } else if (tanim.tip === 'uzunmetin') {
      ic = '<textarea id="' + id + '" name="' + ad + '" rows="4">' + esc(deger || '') + '</textarea>';
    } else if (tanim.tip === 'etiketler') {
      ic = '<input id="' + id + '" name="' + ad + '" value="' + esc((deger || []).join(', ')) + '">';
    } else {
      var tip = (tanim.tip === 'sayi' || tanim.tip === 'ondalik') ? 'number' : 'text';
      var adim = tanim.tip === 'ondalik' ? ' step="0.1"' : '';
      ic = '<input id="' + id + '" type="' + tip + '"' + adim + ' name="' + ad + '" value="' +
        esc(deger == null ? '' : deger) + '">';
    }

    /* Tahmini işareti — yalnızca işaretlenebilir alanlarda */
    var tahmin = '';
    if (sema.tahminEdilebilir.indexOf(ad) !== -1) {
      tahmin = '<label class="est-toggle"><input type="checkbox" name="tahmini:' + ad + '"' +
        (tahminiMi ? ' checked' : '') + '> Bu değer tahmini</label>';
    }

    return '<div class="field' + genislik + '">' +
      '<label for="' + id + '">' + esc(tanim.etiket) + '</label>' + ic + ipucu + tahmin + '</div>';
  }

  function kipAc(kayit) {
    suanki = kayit ? JSON.parse(JSON.stringify(kayit)) : { tur: 'kopek', durum: 'taslak', fotograflar: [], tahmini: [] };
    document.getElementById('kip-baslik').textContent = kayit ? ('Düzenle: ' + kayit.isim) : 'Yeni ilan';

    var gruplar = {};
    Object.keys(sema.alanlar).forEach(function (ad) {
      var t = sema.alanlar[ad];
      (gruplar[t.grup] = gruplar[t.grup] || []).push(ad);
    });

    var GRUP_ADI = {
      temel: 'Temel bilgiler', fiziksel: 'Fiziksel özellikler',
      saglik: 'Sağlık', uyum: 'Uyum', icerik: 'İlan içeriği'
    };

    var html = Object.keys(gruplar).map(function (g) {
      return '<fieldset class="fieldset"><legend>' + esc(GRUP_ADI[g] || g) + '</legend>' +
        '<div class="fieldset__grid">' +
          gruplar[g].map(function (ad) {
            return alanHTML(ad, sema.alanlar[ad], suanki[ad],
              (suanki.tahmini || []).indexOf(ad) !== -1);
          }).join('') +
        '</div></fieldset>';
    }).join('');

    html += '<fieldset class="fieldset"><legend>Fotoğraflar</legend>' +
      '<div class="photos" id="fotolar"></div>' +
      '<input type="file" id="foto-girdi" accept="image/jpeg,image/png,image/webp" multiple hidden>' +
      '</fieldset>';

    document.getElementById('kip-govde').innerHTML = html;
    fotoCiz();
    document.getElementById('kip').hidden = false;
    document.getElementById('kip-durum').textContent = '';
    document.body.style.overflow = 'hidden';
  }

  function kipKapat() {
    document.getElementById('kip').hidden = true;
    document.body.style.overflow = '';
    suanki = null;
  }

  function fotoCiz() {
    var kap = document.getElementById('fotolar');
    kap.innerHTML = (suanki.fotograflar || []).map(function (f, i) {
      return '<div class="photo-item"><img src="' + esc(f) + '" alt="">' +
        '<button type="button" data-foto-sil="' + i + '" aria-label="Fotoğrafı kaldır">×</button></div>';
    }).join('') +
    '<button class="photo-add" type="button" id="foto-ekle">+<br>Fotoğraf</button>';

    kap.querySelectorAll('[data-foto-sil]').forEach(function (b) {
      b.addEventListener('click', function () {
        suanki.fotograflar.splice(Number(b.getAttribute('data-foto-sil')), 1);
        fotoCiz();
      });
    });
    document.getElementById('foto-ekle').addEventListener('click', function () {
      document.getElementById('foto-girdi').click();
    });
  }

  function kipBagla() {
    document.getElementById('kip-kapat').addEventListener('click', kipKapat);
    document.getElementById('kip-iptal').addEventListener('click', kipKapat);
    document.getElementById('kip').addEventListener('click', function (e) {
      if (e.target.id === 'kip') kipKapat();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !document.getElementById('kip').hidden) kipKapat();
    });

    document.getElementById('kip-govde').addEventListener('change', function (e) {
      if (e.target.id !== 'foto-girdi') return;
      var dosyalar = Array.prototype.slice.call(e.target.files);
      var durum = document.getElementById('kip-durum');
      durum.textContent = dosyalar.length + ' fotoğraf yükleniyor…';
      Promise.all(dosyalar.map(function (dosya) {
        return new Promise(function (coz, red) {
          var okuyucu = new FileReader();
          okuyucu.onload = function () {
            if (mod === 'github') {
              /* GitHub kipinde fotoğraf, kayıtla birlikte tek commit'te
                 yüklenir; o zamana dek data-URL olarak önizlenir. */
              coz(okuyucu.result);
              return;
            }
            api('fotograf', { method: 'POST', body: { veri: okuyucu.result, isim: suanki.isim || 'ilan' } })
              .then(function (d) { coz(d.yol); }).catch(red);
          };
          okuyucu.onerror = function () { red(new Error('Dosya okunamadı')); };
          okuyucu.readAsDataURL(dosya);
        });
      })).then(function (yollar) {
        suanki.fotograflar = (suanki.fotograflar || []).concat(yollar);
        fotoCiz();
        durum.textContent = '';
      }).catch(function (err) { durum.textContent = err.message; });
      e.target.value = '';
    });

    document.getElementById('kip-form').addEventListener('submit', function (e) {
      e.preventDefault();
      kaydet();
    });
  }

  function kaydet() {
    var form = document.getElementById('kip-form');
    var fd = new FormData(form);
    var govde = { id: suanki.id, fotograflar: suanki.fotograflar || [], tahmini: [] };

    Object.keys(sema.alanlar).forEach(function (ad) {
      var tanim = sema.alanlar[ad];
      var v = fd.get(ad);
      if (tanim.tip === 'uclu') {
        govde[ad] = v === 'evet' ? true : (v === 'hayir' ? false : null);
      } else if (tanim.tip === 'etiketler') {
        govde[ad] = String(v || '').split(',').map(function (s) { return s.trim(); }).filter(Boolean);
      } else {
        govde[ad] = v === '' ? null : v;
      }
      if (fd.get('tahmini:' + ad)) govde.tahmini.push(ad);
    });

    if (suanki.ornek) govde.ornek = true;
    if (suanki.kaynak) govde.kaynak = suanki.kaynak;
    if (suanki.olusturma) govde.olusturma = suanki.olusturma;

    var durum = document.getElementById('kip-durum');
    durum.textContent = 'Kaydediliyor…';
    var islem = (mod === 'github')
      ? gh.kaydet(govde, sema)
      : api('hayvanlar', { method: 'POST', body: govde })
          .then(function () { return api('hayvanlar'); })
          .then(function (d) { return d.hayvanlar; });
    islem
      .then(function (liste) {
        hayvanlar = liste;
        kipKapat();
        panelCiz();
        bildir(mod === 'github' ? 'İlan kaydedildi — site 1-2 dk içinde güncellenir.' : 'İlan kaydedildi.');
      })
      .catch(function (err) { durum.textContent = err.message; });
  }

  /* --------------------------------------------------------------------- */
  function sil(id) {
    var kayit = hayvanlar.filter(function (a) { return a.id === id; })[0];
    if (!confirm('"' + (kayit ? kayit.isim : id) + '" ilanı silinsin mi?\n\nBu işlem geri alınamaz.')) return;
    var islem = (mod === 'github')
      ? gh.sil(id)
      : fetch('/api/hayvanlar/' + encodeURIComponent(id), {
          method: 'DELETE', headers: { Authorization: 'Bearer ' + jeton }
        }).then(function (r) {
          if (!r.ok) throw new Error('Silinemedi');
          return api('hayvanlar');
        }).then(function (d) { return d.hayvanlar; });
    islem.then(function (liste) {
      hayvanlar = liste; panelCiz(); bildir('İlan silindi.');
    }).catch(function (err) { bildir(err.message, true); });
  }

  function ornekleriSil() {
    if (!confirm('Tüm örnek kayıtlar silinsin mi?')) return;
    var islem = (mod === 'github')
      ? gh.ornekleriSil()
      : api('ornekleri-sil', { method: 'POST', body: {} })
          .then(function (d) {
            return api('hayvanlar').then(function (h) {
              return { silinen: d.silinen, hayvanlar: h.hayvanlar };
            });
          });
    islem.then(function (r) {
      hayvanlar = r.hayvanlar; panelCiz();
      bildir(r.silinen + ' örnek kayıt silindi.');
    }).catch(function (err) { bildir(err.message, true); });
  }

  function instagramCek() {
    var konsol = document.getElementById('konsol');
    konsol.hidden = false;
    konsol.textContent = 'Instagram senkronu başlatıldı…\n';
    var islem = (mod === 'github')
      ? gh.instagramSync(function (mesaj) { konsol.textContent = mesaj + '\n'; })
      : api('instagram-sync', { method: 'POST', body: { limit: 5 } });
    islem
      .then(function (d) {
        konsol.textContent = d.cikti || '(çıktı yok)';
        return (mod === 'github')
          ? gh.hayvanlarYukle()
          : api('hayvanlar').then(function (h) { return h.hayvanlar; });
      })
      .then(function (liste) {
        hayvanlar = liste;
        listeCiz();
        bildir('Senkron tamamlandı — çıktıyı kontrol edin.');
      })
      .catch(function (err) {
        konsol.textContent += '\nHATA: ' + err.message;
        bildir(err.message, true);
      });
  }

  function cikis() {
    if (mod === 'github') {
      gh.cikis();
      localStorage.removeItem(GH_ANAHTAR);
      sessionStorage.removeItem(GH_ANAHTAR);
      githubGirisCiz();
      return;
    }
    api('cikis', { method: 'POST', body: {} }).catch(function () {});
    jeton = '';
    sessionStorage.removeItem(JETON_ANAHTAR);
    girisCiz();
  }

  baslat();
})();
