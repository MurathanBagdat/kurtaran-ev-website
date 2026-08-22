#!/usr/bin/env python3
"""
Kurtaran Ev — statik site üreteci.

Ortak başlık/altbilgi tek yerde durur, sayfa gövdeleri pages.py içindedir.
Çalıştırma:  python3 tools/build.py
Çıktı:       site/*.html
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pages import PAGES  # noqa: E402


# ---------------------------------------------------------------------------
# Site haritası — JPEG'deki menü yapısından çıkarıldı
# ---------------------------------------------------------------------------
NAV = [
    {
        "label": "Yuva Ol",
        "groups": [
            {
                "label": "Yuva Arayanlar",
                "items": [
                    ("Yuva Arayan Köpekler", "yuva-arayan-kopekler.html", "Tüm köpek ilanları", False),
                    ("Yuva Arayan Kediler", "yuva-arayan-kediler.html", "Tüm kedi ilanları", False),
                    ("Sahiplen", "sahiplen.html", "Nasıl sahiplenilir?", False),
                    ("Geçici Yuva", "gecici-yuva.html", "Kısa süreli ev, uzun ömürlü etki", False),
                ],
            },
            {
                "label": None,
                "items": [
                    ("Sahiplenmeden Önce", "sahiplenmeden-once.html", "Ön hazırlık, beklentiler", False),
                    ("Sahiplenme Süreci", "sahiplenme-sureci.html", "Nasıl işliyor, neler gerekiyor", False),
                ],
            },
        ],
    },
    {
        "label": "Destek Ol",
        "groups": [
            {
                "label": None,
                "items": [
                    ("Bağış Yap", "bagis-yap.html", None, True),
                    ("Koruyucu Melek", "koruyucu-melek.html", None, True),
                    ("E-kartlar ve Sertifikalar", "e-kartlar.html", None, True),
                    ("Kurtaran Shop", "kurtaran-shop.html", None, True),
                ],
            },
            {
                "label": None,
                "items": [
                    ("Güncel İhtiyaçlar", "guncel-ihtiyaclar.html", "Sahadan gelen öncelikli listeler", False),
                ],
            },
        ],
    },
    {
        "label": "Katıl",
        "groups": [
            {
                "label": None,
                "items": [
                    ("Gönüllü Ol", "gonullu-ol.html", None, True),
                    ("Kurumsal İş Birliği", "kurumsal-is-birligi.html", None, True),
                ],
            },
        ],
    },
    {
        "label": "Hakkımızda",
        "groups": [
            {
                "label": None,
                "items": [
                    ("Hikayemiz ve Misyonumuz", "hikayemiz.html", None, False),
                    ("Etkimiz ve Çalışmalarımız", "etkimiz.html", None, False),
                    ("Yaşam Alanlarımızı Ziyaret", "yasam-alanlari.html", None, False),
                ],
            },
            {
                "label": "Blog Merkezi",
                "items": [
                    ("Haberler ve Hikayeler", "hikayeler.html", None, False),
                ],
            },
            {
                "label": None,
                "items": [
                    ("İletişim", "iletisim.html", None, False),
                ],
            },
        ],
    },
]

CARET = (
    '<svg class="nav__caret" viewBox="0 0 12 8" fill="none" aria-hidden="true">'
    '<path d="M1 1.5 6 6.5l5-5" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


def render_nav() -> str:
    out = []
    for index, item in enumerate(NAV):
        groups = []
        for group in item["groups"]:
            links = []
            if group["label"]:
                links.append(
                    f'<span class="dropdown__label">{group["label"]}</span>'
                )
            for title, href, desc, external in group["items"]:
                arrow = '<span class="dropdown__arrow" aria-hidden="true">↗</span>' if external else ""
                sub = f'<span class="dropdown__desc">{desc}</span>' if desc else ""
                links.append(
                    f'<a class="dropdown__link" href="{href}">'
                    f'<span><span class="dropdown__title">{title}</span>{sub}</span>'
                    f"{arrow}</a>"
                )
            groups.append(f'<div class="dropdown__group">{"".join(links)}</div>')

        menu_id = f"menu-{index + 1}"
        out.append(
            f'<li class="nav__item nav__item--has-menu">'
            f'<button class="nav__link" type="button" aria-expanded="false" '
            f'aria-controls="{menu_id}">{item["label"]}{CARET}</button>'
            f'<div class="dropdown" id="{menu_id}">{"".join(groups)}</div>'
            f"</li>"
        )
    return "".join(out)


HEADER = """  <div class="announce">
    <span><a href="https://maps.app.goo.gl/R77zL5Gg42f7ZfXY6" target="_blank" rel="noopener">Hadımköy ziyaret</a>: <b>11.00–17.00</b></span>
    <span class="sep" aria-hidden="true">·</span>
    <span><a href="https://maps.app.goo.gl/PutVz4WqqHoSv1bNA" target="_blank" rel="noopener">Beşiktaş ziyaret</a>: <b>10.00–16.00</b></span>
  </div>

  <header class="site-header">
    <div class="site-header__inner">
      <a class="brand" href="index.html">
        <img src="assets/img/logo.png" alt="" width="56" height="56">
        <span class="brand__name">Kurtaran Ev Derneği</span>
      </a>

      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="ana-menu">
        <span class="nav-toggle__bars" aria-hidden="true"><i></i><i></i><i></i></span>
        Menü
      </button>

      <nav aria-label="Ana menü">
        <ul class="nav" id="ana-menu">__NAV__</ul>
      </nav>

      <div class="lang">
        <button class="lang__toggle" type="button" aria-expanded="false" aria-label="Dil seçimi">
          TR
          <svg class="nav__caret" viewBox="0 0 12 8" fill="none" aria-hidden="true">
            <path d="M1 1.5 6 6.5l5-5" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div class="lang__menu">
          <button class="lang__option" type="button" aria-current="true">Türkçe <small>TR</small></button>
          <button class="lang__option" type="button" aria-disabled="true">English <small>yakında</small></button>
        </div>
      </div>

      <a class="btn header-cta" href="bagis-yap.html">Bağış Yap</a>
    </div>
  </header>
"""

FOOTER = """  <footer class="site-footer">
    <div class="container">
      <div class="site-footer__brand">
        <img src="assets/img/logo.png" alt="" width="80" height="80">
        <div>
          <div class="site-footer__name">Kurtaran Ev Derneği</div>
          <p class="site-footer__tagline">Satın Alma Sahiplen</p>
        </div>
      </div>

      <div class="site-footer__cols">
        <div>
          <h2 class="site-footer__heading">Harekete geç</h2>
          <ul>
            <li><a href="yuva-arayan-kopekler.html">Yuva arayan köpekler</a></li>
            <li><a href="yuva-arayan-kediler.html">Yuva arayan kediler</a></li>
            <li><a href="sahiplen.html">Sahiplen</a></li>
            <li><a href="gecici-yuva.html">Geçici yuva ol</a></li>
            <li><a href="koruyucu-melek.html">Koruyucu Melek ol</a></li>
            <li><a href="bagis-yap.html">Bağış yap</a></li>
          </ul>
        </div>
        <div>
          <h2 class="site-footer__heading">Kurtaran Ev</h2>
          <ul>
            <li><a href="hikayemiz.html">Hakkımızda</a></li>
            <li><a href="hikayeler.html">Hikayeler</a></li>
            <li><a href="yasam-alanlari.html">Yaşam alanlarımız</a></li>
            <li><a href="iletisim.html">İletişim</a></li>
          </ul>
        </div>
        <div>
          <h2 class="site-footer__heading">Sosyal</h2>
          <ul>
            <li><a href="https://www.instagram.com/kurtaranev/" target="_blank" rel="noopener">Instagram</a></li>
            <li><a href="https://www.instagram.com/kurtaranev_kopekleri/" target="_blank" rel="noopener">Instagram · Köpekler</a></li>
            <li><a href="https://www.instagram.com/kurtaranev_kedileri/" target="_blank" rel="noopener">Instagram · Kediler</a></li>
          </ul>
        </div>
        <div>
          <h2 class="site-footer__heading">İletişim</h2>
          <ul>
            <li><a href="mailto:iletisim@kurtaranev.org">iletisim@kurtaranev.org</a></li>
            <li><a href="https://maps.app.goo.gl/R77zL5Gg42f7ZfXY6" target="_blank" rel="noopener">Hadımköy ziyaret: 11.00–17.00</a></li>
            <li><a href="https://maps.app.goo.gl/PutVz4WqqHoSv1bNA" target="_blank" rel="noopener">Beşiktaş ziyaret: 10.00–16.00</a></li>
          </ul>
        </div>
      </div>

      <div class="site-footer__bottom">
        <span>© 2026 Kurtaran Ev Derneği</span>
        <a href="mailto:iletisim@kurtaranev.org">iletisim@kurtaranev.org</a>
      </div>
    </div>
  </footer>
"""

SHELL = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="assets/img/logo.png" type="image/png">
<link rel="stylesheet" href="assets/css/style.css">
{extra_css}</head>
<body>
<a class="visually-hidden" href="#icerik">İçeriğe geç</a>

{header}
<main id="icerik">
{body}
</main>

{footer}
{data}<script src="assets/js/main.js"></script>
{extra_js}</body>
</html>
"""


def build() -> None:
    header = HEADER.replace("__NAV__", render_nav())
    OUT.mkdir(parents=True, exist_ok=True)

    for filename, page in PAGES.items():
        extra_css = "".join(
            f'<link rel="stylesheet" href="{yol}">\n' for yol in page.get("css", [])
        )
        extra_js = "".join(
            f'<script src="{yol}"></script>\n' for yol in page.get("js", [])
        )
        # Katalog sayfaları ilan verisini JS dosyası olarak yükler; böylece site
        # yerel sunucu olmadan, dosyaya çift tıklanarak da çalışır.
        data = '<script src="assets/data/animals.js"></script>\n' if page.get("veri") else ""
        bare = page.get("yalin")

        html = SHELL.format(
            title=page["title"],
            description=page["description"],
            header="" if bare else header,
            footer="" if bare else FOOTER,
            body=page["body"].strip("\n"),
            extra_css=extra_css,
            extra_js=extra_js,
            data=data,
        )
        (OUT / filename).write_text(html, encoding="utf-8")
        print(f"  ✓ site/{filename}")

    print(f"\n{len(PAGES)} sayfa üretildi → {OUT}")


if __name__ == "__main__":
    build()
