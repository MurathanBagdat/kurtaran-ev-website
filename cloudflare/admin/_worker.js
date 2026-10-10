/*
 * admin.kurtaranev.org — Cloudflare Pages (gelişmiş kip, _worker.js)
 *
 * Kurtaran Ev ekibinin ortak şifreyle girdiği yönetim paneli kapısı.
 *
 *  - Panel sayfası ve dosyaları GitHub Pages'ten aynı adresten sunulur.
 *  - /kapi/giris  : ortak şifre (ADMIN_SIFRE) doğruysa 12 saatlik imzalı oturum çerezi.
 *  - /kapi/gh/... : oturum açıksa isteği GitHub API'ye GITHUB_TOKEN ile iletir.
 *    YALNIZCA panelin kullandığı uçlara izin verilir ve her commit yalnızca
 *    ilan verisine (animals.json/js) ve ilan fotoğraflarına dokunabilir —
 *    workflow, kod ya da başka bir dosya panelden değiştirilemez.
 *
 * Gizli değişkenler (wrangler pages secret put … --project-name kurtaranev-admin):
 *   GITHUB_TOKEN       fine-grained PAT — yalnızca bu repo, Contents + Actions: Read and write
 *   ADMIN_SIFRE        ekibin ortak şifresi (değişince tüm oturumlar düşer)
 *   OTURUM_ANAHTARI    çerez imza anahtarı (rastgele)
 *
 * Yayın: wrangler pages deploy cloudflare/admin --project-name kurtaranev-admin --branch main
 */

const ORIGIN = 'https://murathanbagdat.github.io/kurtaran-ev-website';
const REPO = '/repos/MurathanBagdat/kurtaran-ev-website';
const DAL = 'main';
const OTURUM_SURE = 12 * 60 * 60;          // sn
const CEREZ = 'ke_oturum';

const DOSYALAR = new Set([
  'admin.html',
  'assets/css/admin.css',
  'assets/css/style.css',
  'assets/js/i18n.js',
  'assets/js/main.js',
  'assets/js/admin.js',
  'assets/js/admin-github.js',
  'assets/data/sema.json',
  'assets/img/logo.png',
]);
const FOTO = /^assets\/img\/animals(-k)?\/[A-Za-z0-9._-]+\.(jpe?g|png|webp)$/;

/* Commit'lerin dokunabileceği dosyalar */
const YAZILABILIR = /^site\/assets\/(data\/animals\.(json|js)|img\/animals\/[A-Za-z0-9._-]+\.(jpe?g|png|webp))$/;
const SHA = '[0-9a-f]{40}';

/* ---------------------------------------------------------------- yardımcılar */
const enc = new TextEncoder();

function b64url(buf) {
  let s = '';
  for (const b of new Uint8Array(buf)) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

async function hmac(anahtar, veri) {
  const k = await crypto.subtle.importKey('raw', enc.encode(anahtar), { name: 'HMAC', hash: 'SHA-256' },
    false, ['sign']);
  return b64url(await crypto.subtle.sign('HMAC', k, enc.encode(veri)));
}

/* Zamanlamaya duyarsız karşılaştırma (iki tarafın HMAC'i karşılaştırılır) */
async function esitMi(a, b, anahtar) {
  const [x, y] = await Promise.all([hmac(anahtar, a), hmac(anahtar, b)]);
  let fark = x.length ^ y.length;
  for (let i = 0; i < Math.min(x.length, y.length); i++) fark |= x.charCodeAt(i) ^ y.charCodeAt(i);
  return fark === 0;
}

/* İmza anahtarı şifreye bağlı: şifre değişince eski oturumlar geçersizleşir */
function imzaAnahtari(env) {
  return `${env.OTURUM_ANAHTARI}|${env.ADMIN_SIFRE}`;
}

async function oturumOlustur(env) {
  const bitis = Math.floor(Date.now() / 1000) + OTURUM_SURE;
  return `${bitis}.${await hmac(imzaAnahtari(env), `oturum:${bitis}`)}`;
}

async function oturumGecerli(request, env) {
  const cerez = (request.headers.get('cookie') || '')
    .split(/;\s*/).find((c) => c.startsWith(`${CEREZ}=`));
  if (!cerez) return false;
  const [bitis, imza] = cerez.slice(CEREZ.length + 1).split('.');
  if (!bitis || !imza || Number(bitis) < Date.now() / 1000) return false;
  return esitMi(imza, await hmac(imzaAnahtari(env), `oturum:${bitis}`), env.OTURUM_ANAHTARI);
}

function cerezBasligi(deger, sure) {
  return `${CEREZ}=${deger}; Path=/; Max-Age=${sure}; HttpOnly; Secure; SameSite=Strict`;
}

function json(govde, status = 200, ek = {}) {
  return new Response(JSON.stringify(govde), {
    status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...ek },
  });
}

/* Basit kaba kuvvet freni: IP başına 15 dk'da 10 hatalı deneme (isolate belleğinde) */
const hatalar = new Map();
function engelliMi(ip) {
  const k = hatalar.get(ip);
  return k && k.n >= 10 && Date.now() - k.t < 15 * 60 * 1000;
}
function hataYaz(ip) {
  const k = hatalar.get(ip);
  if (!k || Date.now() - k.t > 15 * 60 * 1000) hatalar.set(ip, { n: 1, t: Date.now() });
  else k.n += 1;
}

/* ------------------------------------------------- GitHub vekili: izin listesi */
function izinliMi(method, yol, govde) {
  const r = (desen) => new RegExp(`^${REPO}${desen}$`).test(yol);
  if (method === 'GET') {
    return r('') || r('/contents/site/assets/data/animals\\.json') || r(`/git/blobs/${SHA}`) ||
      r(`/git/ref/heads/${DAL}`) || r(`/git/commits/${SHA}`) ||
      r('/actions/workflows/instagram-sync\\.yml/runs');
  }
  if (method === 'POST' && r('/git/blobs')) {
    return govde && govde.encoding === 'base64' && typeof govde.content === 'string';
  }
  if (method === 'POST' && r('/git/trees')) {
    return govde && typeof govde.base_tree === 'string' && Array.isArray(govde.tree) && govde.tree.length > 0 &&
      govde.tree.every((g) => g && typeof g.path === 'string' && YAZILABILIR.test(g.path) &&
        g.mode === '100644' && g.type === 'blob');
  }
  if (method === 'POST' && r('/git/commits')) {
    return govde && typeof govde.tree === 'string' && Array.isArray(govde.parents) && govde.parents.length === 1;
  }
  if (method === 'PATCH' && r(`/git/refs/heads/${DAL}`)) {
    return govde && typeof govde.sha === 'string' && govde.force !== true;
  }
  if (method === 'POST' && r('/actions/workflows/instagram-sync\\.yml/dispatches')) {
    return govde && govde.ref === DAL;
  }
  return false;
}

async function githubVekili(request, env, yol, arama) {
  const method = request.method;
  let govdeMetni = null;
  let govde = null;
  if (method !== 'GET') {
    if (request.headers.get('x-ke-kapi') !== '1') return json({ message: 'Geçersiz istek.' }, 403);
    govdeMetni = await request.text();
    if (govdeMetni.length > 14 * 1024 * 1024) return json({ message: 'İstek çok büyük.' }, 413);
    try { govde = JSON.parse(govdeMetni || '{}'); } catch { return json({ message: 'Geçersiz JSON.' }, 400); }
  }
  if (!izinliMi(method, yol, govde)) {
    return json({ message: 'Bu işleme panelden izin verilmiyor.' }, 403);
  }
  const yanit = await fetch(`https://api.github.com${yol}${arama}`, {
    method,
    headers: {
      Authorization: `Bearer ${env.GITHUB_TOKEN}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'kurtaranev-admin-kapi',
      ...(govdeMetni !== null ? { 'Content-Type': 'application/json' } : {}),
    },
    body: govdeMetni,
  });
  return new Response(yanit.body, {
    status: yanit.status,
    headers: { 'content-type': yanit.headers.get('content-type') || 'application/json', 'cache-control': 'no-store' },
  });
}

/* ------------------------------------------------------------------ giriş */
async function giris(request, env) {
  const ip = request.headers.get('cf-connecting-ip') || 'yok';
  if (engelliMi(ip)) return json({ hata: 'Çok fazla hatalı deneme. 15 dakika sonra tekrar deneyin.' }, 429);
  let sifre = '';
  try { sifre = String((await request.json()).sifre || ''); } catch { /* boş */ }
  if (!env.ADMIN_SIFRE || !env.OTURUM_ANAHTARI || !env.GITHUB_TOKEN) {
    return json({ hata: 'Panel henüz yapılandırılmadı (gizli değişkenler eksik).' }, 503);
  }
  if (!sifre || !(await esitMi(sifre, env.ADMIN_SIFRE, env.OTURUM_ANAHTARI))) {
    hataYaz(ip);
    await new Promise((c) => setTimeout(c, 800));
    return json({ hata: 'Şifre hatalı.' }, 401);
  }
  hatalar.delete(ip);
  return json({ tamam: true }, 200, { 'set-cookie': cerezBasligi(await oturumOlustur(env), OTURUM_SURE) });
}

/* ------------------------------------------------------------------ ana */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const yol = url.pathname.replace(/^\/+/, '');

    if (yol === '' || yol === 'admin') return Response.redirect(`${url.origin}/admin.html`, 302);

    if (yol === 'kapi/durum') {
      return json({ kapi: true, girisli: await oturumGecerli(request, env) });
    }
    if (yol === 'kapi/giris' && request.method === 'POST') return giris(request, env);
    if (yol === 'kapi/cikis' && request.method === 'POST') {
      return json({ tamam: true }, 200, { 'set-cookie': cerezBasligi('', 0) });
    }
    if (yol.startsWith('kapi/gh/')) {
      if (!(await oturumGecerli(request, env))) {
        return json({ message: 'Oturum süresi doldu, yeniden giriş yapın.' }, 401);
      }
      return githubVekili(request, env, `/${yol.slice('kapi/gh/'.length)}`, url.search);
    }

    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method not allowed', { status: 405 });
    }
    if (DOSYALAR.has(yol) || FOTO.test(yol)) {
      const foto = FOTO.test(yol);
      const yanit = await fetch(`${ORIGIN}/${yol}`,
        foto ? { cf: { cacheEverything: true, cacheTtl: 86400 } } : {});
      const basliklar = new Headers(yanit.headers);
      basliklar.set('cache-control', foto ? 'public, max-age=86400' : 'no-cache');
      basliklar.set('x-robots-tag', 'noindex, nofollow');
      basliklar.set('x-frame-options', 'DENY');
      return new Response(yanit.body, { status: yanit.status, headers: basliklar });
    }
    return new Response('Bulunamadı', { status: 404 });
  },
};
