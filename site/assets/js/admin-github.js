/* Kurtaran Ev — GitHub tabanlı yönetim arka ucu.
   Yerel sunucu (tools/server.py) yokken (ör. GitHub Pages) admin paneli bu
   dosya üzerinden doğrudan GitHub API'siyle konuşur: her kayıt repo'ya bir
   commit olur, GitHub Actions siteyi otomatik yeniden yayınlar.

   Gerekli jeton: fine-grained PAT — yalnızca bu repo, Contents: Read/Write
   (+ Instagram senkronu için Actions: Read/Write).

   tools/animals.py'deki normalize/save mantığının JS portunu içerir; şema
   assets/data/sema.json'dan gelir (animals.py her kayıtta yeniden üretir). */
(function () {
  'use strict';

  var API = 'https://api.github.com';

  /* ---------------------------------------------------------------------- */
  /* Yardımcılar                                                             */
  /* ---------------------------------------------------------------------- */
  function utf8ToB64(metin) {
    var b = new TextEncoder().encode(metin), ikili = '';
    for (var i = 0; i < b.length; i++) ikili += String.fromCharCode(b[i]);
    return btoa(ikili);
  }

  function b64ToUtf8(b64) {
    var ikili = atob(String(b64).replace(/\s/g, ''));
    var arr = new Uint8Array(ikili.length);
    for (var i = 0; i < ikili.length; i++) arr[i] = ikili.charCodeAt(i);
    return new TextDecoder().decode(arr);
  }

  function slugify(metin) {
    if (!metin) return 'isimsiz';
    var tr = { 'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
               'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U' };
    metin = String(metin).replace(/[çğıöşüÇĞİÖŞÜ]/g, function (c) { return tr[c]; });
    metin = metin.normalize('NFKD').replace(/[^\x00-\x7F]/g, '');
    metin = metin.replace(/[^a-zA-Z0-9]+/g, '-').replace(/^-+|-+$/g, '').toLowerCase();
    return metin || 'isimsiz';
  }

  function rastgeleHex(uzunluk) {
    var arr = new Uint8Array(Math.ceil(uzunluk / 2));
    crypto.getRandomValues(arr);
    return Array.prototype.map.call(arr, function (b) {
      return ('0' + b.toString(16)).slice(-2);
    }).join('').slice(0, uzunluk);
  }

  /* tools/animals.py now_iso() ile aynı biçim: 2026-08-16T20:04:28+00:00 */
  function nowIso() {
    return new Date().toISOString().replace(/\.\d{3}Z$/, '+00:00');
  }

  function yasMetni(ay) {
    if (ay == null) return null;
    if (ay < 1) return 'Yenidoğan';
    if (ay < 12) return ay + ' aylık';
    var yil = Math.floor(ay / 12), kalan = ay % 12;
    if (kalan === 0) return yil + ' yaşında';
    if (kalan >= 6) return yil + ',5 yaşında';
    return yil + ' yaşında';
  }

  function yasGrubu(ay) {
    if (ay == null) return null;
    if (ay < 12) return 'yavru';
    if (ay < 84) return 'yetiskin';
    return 'kidemli';
  }

  function boyutTahmini(tur, kilo) {
    if (kilo == null) return null;
    if (tur === 'kedi') return 'kucuk';
    if (kilo < 12) return 'kucuk';
    if (kilo < 25) return 'orta';
    return 'buyuk';
  }

  function toBool(v) {
    if (v == null || v === '' || v === 'bilinmiyor') return null;
    if (typeof v === 'boolean') return v;
    return ['true', 'evet', '1', 'var', 'yes'].indexOf(String(v).toLowerCase()) !== -1;
  }

  function toNum(v, ondalik) {
    if (v == null || v === '') return null;
    var n = parseFloat(String(v).replace(',', '.'));
    if (isNaN(n)) return null;
    return ondalik ? Math.round(n * 10) / 10 : Math.round(n);
  }

  /* tools/animals.py normalize() portu — (kayit, hatalar) döner. */
  function normalize(ham, sema) {
    var hatalar = [];
    var tur = String(ham.tur || 'kopek').trim();
    if (tur !== 'kopek' && tur !== 'kedi') {
      hatalar.push('Geçersiz tür: ' + tur);
      tur = 'kopek';
    }

    var kayit = { id: null, tur: tur };
    Object.keys(sema.alanlar).forEach(function (ad) {
      if (ad === 'tur') return;
      var tanim = sema.alanlar[ad];
      var deger = ham[ad];
      var tip = tanim.tip;
      if (tip === 'metin' || tip === 'uzunmetin') {
        deger = (deger == null || deger === '') ? null : (String(deger).trim() || null);
      } else if (tip === 'sayi') {
        deger = toNum(deger);
      } else if (tip === 'ondalik') {
        deger = toNum(deger, true);
      } else if (tip === 'uclu') {
        deger = toBool(deger);
      } else if (tip === 'secim') {
        deger = (deger in (tanim.secenekler || {})) ? deger : null;
      } else if (tip === 'etiketler') {
        if (typeof deger === 'string') {
          deger = deger.split(',').map(function (p) { return p.trim(); }).filter(Boolean);
        }
        deger = (deger || []).map(function (p) { return String(p).trim(); })
          .filter(Boolean).slice(0, 8);
      }
      kayit[ad] = deger;

      if ((tip === 'sayi' || tip === 'ondalik') && kayit[ad] != null &&
          (kayit[ad] < tanim.min || kayit[ad] > tanim.max)) {
        hatalar.push(tanim.etiket + ' aralık dışı: ' + kayit[ad]);
        kayit[ad] = null;
      }
    });

    if (!kayit.isim) kayit.isim = 'İsimsiz';
    kayit.durum = kayit.durum || 'taslak';
    kayit.fotograflar = (ham.fotograflar || []).map(String)
      .filter(function (f) { return f.trim(); }).slice(0, 12);
    kayit.tahmini = (ham.tahmini || []).filter(function (f) {
      return sema.tahminEdilebilir.indexOf(f) !== -1;
    });
    kayit.ornek = !!ham.ornek;
    kayit.kaynak = ham.kaynak || null;
    kayit.id = ham.id || (tur + '-' + slugify(kayit.isim) + '-' + rastgeleHex(6));
    kayit.olusturma = ham.olusturma || nowIso();
    kayit.guncelleme = nowIso();

    if (kayit.boyut == null) {
      var tahmin = boyutTahmini(tur, kayit.kiloKg);
      if (tahmin) {
        kayit.boyut = tahmin;
        if (kayit.tahmini.indexOf('boyut') === -1) kayit.tahmini.push('boyut');
      }
    }

    kayit.yasMetni = yasMetni(kayit.yasAy);
    kayit.yasGrubu = yasGrubu(kayit.yasAy);
    kayit.arama = [
      kayit.isim, kayit.cins, kayit.renk, kayit.konum, kayit.aciklama,
      kayit.saglikNotu, (kayit.karakter || []).join(' ')
    ].filter(Boolean).join(' ').toLowerCase();

    return { kayit: kayit, hatalar: hatalar };
  }

  /* ---------------------------------------------------------------------- */
  /* Arka uç                                                                 */
  /* ---------------------------------------------------------------------- */
  window.KE_GH = function () {
    var ayar = { sahip: 'MurathanBagdat', repo: 'kurtaran-ev-website', dal: 'main' };
    /* github.io üzerindeyse sahibi/repoyu adresten türet */
    if (/\.github\.io$/i.test(location.hostname)) {
      ayar.sahip = location.hostname.split('.')[0];
      var parcalar = location.pathname.split('/').filter(Boolean);
      if (parcalar.length > 1) ayar.repo = parcalar[0];
    }

    var jeton = '';
    var repoYol = '/repos/' + ayar.sahip + '/' + ayar.repo;
    var IZINLI_FOTO = { 'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp' };

    function gh(yol, secenekler) {
      secenekler = secenekler || {};
      return fetch(API + yol, {
        method: secenekler.method || 'GET',
        headers: {
          Authorization: 'Bearer ' + jeton,
          Accept: 'application/vnd.github+json',
          'X-GitHub-Api-Version': '2022-11-28'
        },
        body: secenekler.body ? JSON.stringify(secenekler.body) : undefined
      }).then(function (r) {
        if (r.status === 204) return {};
        return r.json().catch(function () { return {}; }).then(function (govde) {
          if (!r.ok) {
            var mesaj = govde.message || ('GitHub hatası (' + r.status + ')');
            if (r.status === 401) mesaj = 'Jeton geçersiz ya da süresi dolmuş.';
            if (r.status === 403 && /rate limit/i.test(mesaj)) mesaj = 'GitHub istek sınırına takıldı, biraz bekleyin.';
            if (r.status === 403 && /Resource not accessible/i.test(govde.message || '')) {
              mesaj = 'Jetonun bu işlem için yetkisi yok (Contents ve Actions izinlerini kontrol edin).';
            }
            var hata = new Error(mesaj);
            hata.kod = r.status;
            throw hata;
          }
          return govde;
        });
      });
    }

    /* Depodan dosya oku — içerik + sha. 1 MB üstünde blob API'sine düşer. */
    function dosyaOku(yol) {
      return gh(repoYol + '/contents/' + yol + '?ref=' + ayar.dal).then(function (d) {
        if (d.content) return { icerik: b64ToUtf8(d.content), sha: d.sha };
        return gh(repoYol + '/git/blobs/' + d.sha).then(function (blob) {
          return { icerik: b64ToUtf8(blob.content), sha: d.sha };
        });
      });
    }

    /* Birden çok dosyayı TEK commit'le yaz.
       dosyalar: [{yol, icerik}] (UTF-8 metin) ya da [{yol, base64}] (ikili). */
    function commitle(dosyalar, mesaj) {
      var refSha, agacSha;
      return gh(repoYol + '/git/ref/heads/' + ayar.dal)
        .then(function (ref) {
          refSha = ref.object.sha;
          return gh(repoYol + '/git/commits/' + refSha);
        })
        .then(function (c) {
          agacSha = c.tree.sha;
          return Promise.all(dosyalar.map(function (d) {
            if (d.base64) {
              return gh(repoYol + '/git/blobs', {
                method: 'POST', body: { content: d.base64, encoding: 'base64' }
              }).then(function (blob) {
                return { path: d.yol, mode: '100644', type: 'blob', sha: blob.sha };
              });
            }
            return { path: d.yol, mode: '100644', type: 'blob', content: d.icerik };
          }));
        })
        .then(function (girdiler) {
          return gh(repoYol + '/git/trees', {
            method: 'POST', body: { base_tree: agacSha, tree: girdiler }
          });
        })
        .then(function (agac) {
          return gh(repoYol + '/git/commits', {
            method: 'POST',
            body: { message: mesaj, tree: agac.sha, parents: [refSha] }
          });
        })
        .then(function (c) {
          return gh(repoYol + '/git/refs/heads/' + ayar.dal, {
            method: 'PATCH', body: { sha: c.sha }
          });
        });
    }

    function hayvanlarYukle() {
      return dosyaOku('site/assets/data/animals.json').then(function (d) {
        return (JSON.parse(d.icerik).hayvanlar) || [];
      });
    }

    /* tools/animals.py save() portu: JSON + JS'yi birlikte, tek commit'le yazar. */
    function tumKaydet(hayvanlar, ekDosyalar, mesaj) {
      hayvanlar = hayvanlar.slice().sort(function (a, b) {
        return String(b.olusturma || '').localeCompare(String(a.olusturma || ''));
      });
      var govde = { guncelleme: nowIso(), sayi: hayvanlar.length, hayvanlar: hayvanlar };
      var json = JSON.stringify(govde, null, 2) + '\n';
      var js = '/* Otomatik üretildi — bu dosyayı elle düzenlemeyin.\n' +
        '   Kaynak: assets/data/animals.json · Üreten: tools/animals.py */\n' +
        'window.KE_DATA = ' + JSON.stringify(govde, null, 2) + ';\n';
      var dosyalar = [
        { yol: 'site/assets/data/animals.json', icerik: json },
        { yol: 'site/assets/data/animals.js', icerik: js }
      ].concat(ekDosyalar || []);
      return commitle(dosyalar, mesaj).then(function () { return hayvanlar; });
    }

    /* data:-URL fotoğrafları commit'e girecek blob dosyalarına çevirir;
       kayıttaki yolları site içi göreli yola günceller. */
    function fotolariAyikla(kayitHam) {
      var dosyalar = [];
      kayitHam.fotograflar = (kayitHam.fotograflar || []).map(function (f) {
        var m = /^data:([\w/+.-]+);base64,(.+)$/s.exec(f);
        if (!m) return f;
        var uzanti = IZINLI_FOTO[m[1]];
        if (!uzanti) throw new Error('Desteklenmeyen görsel türü: ' + m[1] + '. JPEG, PNG veya WebP kullanın.');
        if (m[2].length * 0.75 > 8 * 1024 * 1024) throw new Error('Fotoğraf 8 MB\'tan büyük olamaz.');
        var ad = slugify(kayitHam.isim || 'foto') + '-' + rastgeleHex(8) + uzanti;
        dosyalar.push({ yol: 'site/assets/img/animals/' + ad, base64: m[2] });
        return 'assets/img/animals/' + ad;
      });
      return dosyalar;
    }

    return {
      ayar: ayar,

      girisYap: function (yeniJeton) {
        jeton = String(yeniJeton || '').trim();
        if (!jeton) return Promise.reject(new Error('Jeton boş olamaz.'));
        return gh(repoYol).then(function (repo) {
          if (repo.permissions && !repo.permissions.push) {
            throw new Error('Bu jetonun repoya yazma izni yok (Contents: Read and write gerekli).');
          }
          return repo;
        });
      },

      cikis: function () { jeton = ''; },

      hayvanlarYukle: hayvanlarYukle,

      kaydet: function (ham, sema) {
        var fotoDosyalar;
        try { fotoDosyalar = fotolariAyikla(ham); }
        catch (e) { return Promise.reject(e); }

        var sonuc = normalize(ham, sema);
        if (sonuc.hatalar.length) return Promise.reject(new Error(sonuc.hatalar.join('; ')));
        var kayit = sonuc.kayit;

        return hayvanlarYukle().then(function (hayvanlar) {
          var bulundu = false;
          for (var i = 0; i < hayvanlar.length; i++) {
            if (hayvanlar[i].id === kayit.id) {
              kayit.olusturma = hayvanlar[i].olusturma || kayit.olusturma;
              hayvanlar[i] = kayit;
              bulundu = true;
              break;
            }
          }
          if (!bulundu) hayvanlar.push(kayit);
          return tumKaydet(hayvanlar, fotoDosyalar,
            'Admin: ' + (bulundu ? 'ilan güncellendi' : 'yeni ilan') + ' — ' + kayit.isim);
        });
      },

      sil: function (id) {
        return hayvanlarYukle().then(function (hayvanlar) {
          var kalan = hayvanlar.filter(function (a) { return a.id !== id; });
          if (kalan.length === hayvanlar.length) throw new Error('Kayıt bulunamadı: ' + id);
          return tumKaydet(kalan, [], 'Admin: ilan silindi — ' + id);
        });
      },

      ornekleriSil: function () {
        return hayvanlarYukle().then(function (hayvanlar) {
          var kalan = hayvanlar.filter(function (a) { return !a.ornek; });
          var silinen = hayvanlar.length - kalan.length;
          if (!silinen) return { silinen: 0, hayvanlar: hayvanlar };
          return tumKaydet(kalan, [], 'Admin: ' + silinen + ' örnek kayıt silindi')
            .then(function (h) { return { silinen: silinen, hayvanlar: h }; });
        });
      },

      /* Instagram senkronu: GitHub Actions workflow'unu tetikler ve bitene
         dek durumu izler. onDurum(mesaj) ilerlemeyi bildirir. */
      instagramSync: function (onDurum) {
        var wfYol = repoYol + '/actions/workflows/instagram-sync.yml';
        var baslangic = Date.now() - 90 * 1000; // saat kayması payı

        function bekle(ms) { return new Promise(function (coz) { setTimeout(coz, ms); }); }

        function izle(deneme) {
          if (deneme > 60) throw new Error('Zaman aşımı — durumu Actions sayfasından izleyin.');
          return bekle(10000).then(function () {
            return gh(wfYol + '/runs?per_page=1');
          }).then(function (d) {
            var kosum = (d.workflow_runs || [])[0];
            if (!kosum || new Date(kosum.created_at).getTime() < baslangic) {
              onDurum('Çalıştırma kuyruğa alınıyor…');
              return izle(deneme + 1);
            }
            if (kosum.status !== 'completed') {
              onDurum('Senkron çalışıyor (' + kosum.status + ')… ' +
                'Ayrıntı: ' + kosum.html_url);
              return izle(deneme + 1);
            }
            return kosum;
          });
        }

        return gh(wfYol + '/dispatches', { method: 'POST', body: { ref: ayar.dal } })
          .then(function () {
            onDurum('Senkron GitHub Actions üzerinde başlatıldı…');
            return izle(0);
          })
          .then(function (kosum) {
            if (kosum.conclusion !== 'success') {
              throw new Error('Senkron başarısız bitti (' + kosum.conclusion + '). Ayrıntı: ' + kosum.html_url);
            }
            return { cikti: 'Senkron tamamlandı. Ayrıntılı rapor: ' + kosum.html_url };
          });
      }
    };
  };
})();
