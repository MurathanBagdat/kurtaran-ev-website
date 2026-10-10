/*
 * ilanlar.kurtaranev.org — Cloudflare Pages (gelişmiş kip, _worker.js)
 *
 * Wix sitesinden açılan "ilan modu" sayfalarını GitHub Pages'teki kaynaktan
 * sunan süzgeçli bir kapı. Yalnızca izin listesindeki yollar geçer; tam
 * prototipin diğer sayfaları (bağış, koruyucu melek, admin…) bu adreste
 * yoktur → 404.
 *
 * İçerik GitHub Pages'ten okunduğu için günlük Instagram senkronu buraya
 * kendiliğinden yansır; bu dosya değişmedikçe yeniden yayın gerekmez.
 *
 * Yayın: wrangler pages deploy cloudflare/ilanlar --project-name kurtaranev-ilanlar --branch main
 */

const ORIGIN = 'https://murathanbagdat.github.io/kurtaran-ev-website';

const SAYFALAR = new Set(['kopekler.html', 'kediler.html', 'ilan.html']);
const VARLIKLAR = new Set([
  'assets/css/style.css',
  'assets/js/i18n.js',
  'assets/js/main.js',
  'assets/js/catalog.js',
  'assets/js/animal.js',
  'assets/data/animals.js',
  'assets/img/logo.png',
]);
const FOTO = /^assets\/img\/animals(-k)?\/[A-Za-z0-9._-]+\.(jpe?g|png|webp)$/;

const SURE = { sayfa: 300, veri: 300, foto: 86400 };   // sn — kenar + tarayıcı önbelleği

function bulunamadi(dil) {
  const en = dil === 'en';
  const geri = en ? 'https://en.kurtaranev.org/sahiplendirme' : 'https://www.kurtaranev.org/sahiplendirme';
  const html = `<!DOCTYPE html><html lang="${en ? 'en' : 'tr'}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>${en ? 'Page not found' : 'Sayfa bulunamadı'} | Kurtaran Ev</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#fffdf7;color:#183653;
display:grid;place-items:center;min-height:100vh;margin:0;text-align:center;padding:24px}
a{color:#183653;font-weight:700}</style></head><body><div>
<h1 style="font-family:Georgia,serif">${en ? 'Page not found' : 'Sayfa bulunamadı'}</h1>
<p><a href="/${en ? 'en/' : ''}kopekler.html">${en ? 'Dogs looking for a home' : 'Yuva arayan köpekler'}</a> ·
<a href="/${en ? 'en/' : ''}kediler.html">${en ? 'Cats looking for a home' : 'Yuva arayan kediler'}</a></p>
<p><a href="${geri}">${en ? 'Back to Kurtaran Ev' : 'Kurtaran Ev sitesine dön'}</a></p>
</div></body></html>`;
  return new Response(html, { status: 404, headers: { 'content-type': 'text/html; charset=utf-8' } });
}

export default {
  async fetch(request) {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method not allowed', { status: 405 });
    }
    const url = new URL(request.url);
    let yol = url.pathname.replace(/^\/+/, '');
    const dil = yol.startsWith('en/') || yol === 'en' ? 'en' : 'tr';

    if (yol === '' || yol === 'en' || yol === 'en/') {
      return Response.redirect(`${url.origin}/${dil === 'en' ? 'en/' : ''}kopekler.html`, 302);
    }
    if (/^(en\/)?(kopekler|kediler|ilan)\/?$/.test(yol)) yol = yol.replace(/\/$/, '') + '.html';

    let hedef = null;
    let sure = SURE.sayfa;
    const sayfa = yol.match(/^(en\/)?([a-z]+\.html)$/);
    if (sayfa && SAYFALAR.has(sayfa[2])) {
      hedef = `${ORIGIN}/ilanlar/${sayfa[1] || ''}${sayfa[2]}`;
    } else if (VARLIKLAR.has(yol)) {
      hedef = `${ORIGIN}/${yol}`;
      sure = SURE.veri;
    } else if (FOTO.test(yol)) {
      hedef = `${ORIGIN}/${yol}`;
      sure = SURE.foto;
    }
    if (!hedef) return bulunamadi(dil);

    const yanit = await fetch(hedef, { cf: { cacheEverything: true, cacheTtl: sure } });
    if (yanit.status === 404) return bulunamadi(dil);

    const basliklar = new Headers(yanit.headers);
    basliklar.set('cache-control', `public, max-age=${sure}`);
    for (const ad of ['x-github-request-id', 'x-fastly-request-id', 'x-served-by', 'x-proxy-cache',
                      'via', 'x-cache', 'x-cache-hits', 'x-timer', 'access-control-allow-origin']) {
      basliklar.delete(ad);
    }
    return new Response(yanit.body, { status: yanit.status, headers: basliklar });
  },
};
