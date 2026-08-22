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
from pages_en import PAGES_EN  # noqa: E402


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


# ---------------------------------------------------------------------------
# İngilizce menü — NAV ile aynı yapı, aynı dosya adları (site/en/ altında)
# ---------------------------------------------------------------------------
NAV_EN = [
    {
        "label": "Adopt",
        "groups": [
            {
                "label": "Looking for a home",
                "items": [
                    ("Dogs Looking for a Home", "yuva-arayan-kopekler.html", "All dog listings", False),
                    ("Cats Looking for a Home", "yuva-arayan-kediler.html", "All cat listings", False),
                    ("Adopt", "sahiplen.html", "How adoption works", False),
                    ("Foster", "gecici-yuva.html", "A short-term home, a lasting impact", False),
                ],
            },
            {
                "label": None,
                "items": [
                    ("Before You Adopt", "sahiplenmeden-once.html", "Preparation and expectations", False),
                    ("Adoption Process", "sahiplenme-sureci.html", "How it works, what's needed", False),
                ],
            },
        ],
    },
    {
        "label": "Support",
        "groups": [
            {
                "label": None,
                "items": [
                    ("Donate", "bagis-yap.html", None, True),
                    ("Guardian Angel", "koruyucu-melek.html", None, True),
                    ("E-cards & Certificates", "e-kartlar.html", None, True),
                    ("Kurtaran Shop", "kurtaran-shop.html", None, True),
                ],
            },
            {
                "label": None,
                "items": [
                    ("Current Needs", "guncel-ihtiyaclar.html", "Priority lists from the field", False),
                ],
            },
        ],
    },
    {
        "label": "Get Involved",
        "groups": [
            {
                "label": None,
                "items": [
                    ("Volunteer", "gonullu-ol.html", None, True),
                    ("Corporate Partnerships", "kurumsal-is-birligi.html", None, True),
                ],
            },
        ],
    },
    {
        "label": "About",
        "groups": [
            {
                "label": None,
                "items": [
                    ("Our Story & Mission", "hikayemiz.html", None, False),
                    ("Our Impact & Work", "etkimiz.html", None, False),
                    ("Visit Our Shelters", "yasam-alanlari.html", None, False),
                ],
            },
            {
                "label": "Blog",
                "items": [
                    ("News & Stories", "hikayeler.html", None, False),
                ],
            },
            {
                "label": None,
                "items": [
                    ("Contact", "iletisim.html", None, False),
                ],
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Yerel ayarlar — başlık/altbilgi metinleri. %ANAHTAR% yer tutucuları
# aşağıdaki şablonlarda değiştirilir.
# ---------------------------------------------------------------------------
LOCALES = {
    "tr": {
        "nav": NAV,
        "out": "",                      # site/
        "base": "",                     # varlık yolu öneki
        "skip": "İçeriğe geç",
        "hadimkoy": "Hadımköy ziyaret",
        "besiktas": "Beşiktaş ziyaret",
        "menu": "Menü",
        "nav_label": "Ana menü",
        "lang_label": "Dil seçimi",
        "lang_code": "TR",
        "cta": "Bağış Yap",
        "tagline": "Satın Alma Sahiplen",
        "f_act": "Harekete geç",
        "f_dogs": "Yuva arayan köpekler",
        "f_cats": "Yuva arayan kediler",
        "f_adopt": "Sahiplen",
        "f_foster": "Geçici yuva ol",
        "f_angel": "Koruyucu Melek ol",
        "f_donate": "Bağış yap",
        "f_org": "Kurtaran Ev",
        "f_about": "Hakkımızda",
        "f_stories": "Hikayeler",
        "f_shelters": "Yaşam alanlarımız",
        "f_contact": "İletişim",
        "f_social": "Sosyal",
        "f_ig_dogs": "Instagram · Köpekler",
        "f_ig_cats": "Instagram · Kediler",
        "f_contact_h": "İletişim",
        "f_hours_h": "Hadımköy ziyaret: 11.00–17.00",
        "f_hours_b": "Beşiktaş ziyaret: 10.00–16.00",
    },
    "en": {
        "nav": NAV_EN,
        "out": "en",                    # site/en/
        "base": "../",
        "skip": "Skip to content",
        "hadimkoy": "Hadımköy visits",
        "besiktas": "Beşiktaş visits",
        "menu": "Menu",
        "nav_label": "Main menu",
        "lang_label": "Language",
        "lang_code": "EN",
        "cta": "Donate",
        "tagline": "Don't Shop, Adopt",
        "f_act": "Take action",
        "f_dogs": "Dogs looking for a home",
        "f_cats": "Cats looking for a home",
        "f_adopt": "Adopt",
        "f_foster": "Foster",
        "f_angel": "Become a Guardian Angel",
        "f_donate": "Donate",
        "f_org": "Kurtaran Ev",
        "f_about": "About us",
        "f_stories": "Stories",
        "f_shelters": "Our shelters",
        "f_contact": "Contact",
        "f_social": "Social",
        "f_ig_dogs": "Instagram · Dogs",
        "f_ig_cats": "Instagram · Cats",
        "f_contact_h": "Contact",
        "f_hours_h": "Hadımköy visits: 11.00–17.00",
        "f_hours_b": "Beşiktaş visits: 10.00–16.00",
    },
}

HEADER = """  <div class="announce">
    <span><a href="https://maps.app.goo.gl/R77zL5Gg42f7ZfXY6" target="_blank" rel="noopener">%hadimkoy%</a>: <b>11.00–17.00</b></span>
    <span class="sep" aria-hidden="true">·</span>
    <span><a href="https://maps.app.goo.gl/PutVz4WqqHoSv1bNA" target="_blank" rel="noopener">%besiktas%</a>: <b>10.00–16.00</b></span>
  </div>

  <header class="site-header">
    <div class="site-header__inner">
      <a class="brand" href="index.html">
        <img src="%base%assets/img/logo.png" alt="" width="56" height="56">
        <span class="brand__name">Kurtaran Ev Derneği</span>
      </a>

      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="ana-menu">
        <span class="nav-toggle__bars" aria-hidden="true"><i></i><i></i><i></i></span>
        %menu%
      </button>

      <nav aria-label="%nav_label%">
        <ul class="nav" id="ana-menu">__NAV__</ul>
      </nav>

      <div class="lang">
        <button class="lang__toggle" type="button" aria-expanded="false" aria-label="%lang_label%">
          %lang_code%
          <svg class="nav__caret" viewBox="0 0 12 8" fill="none" aria-hidden="true">
            <path d="M1 1.5 6 6.5l5-5" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div class="lang__menu">
          <a class="lang__option" href="%tr_url%" hreflang="tr" lang="tr"%tr_current%>Türkçe <small>TR</small></a>
          <a class="lang__option" href="%en_url%" hreflang="en" lang="en"%en_current%>English <small>EN</small></a>
        </div>
      </div>

      <a class="btn header-cta" href="bagis-yap.html">%cta%</a>
    </div>
  </header>
"""

FOOTER = """  <footer class="site-footer">
    <div class="container">
      <div class="site-footer__brand">
        <img src="%base%assets/img/logo.png" alt="" width="80" height="80">
        <div>
          <div class="site-footer__name">Kurtaran Ev Derneği</div>
          <p class="site-footer__tagline">%tagline%</p>
        </div>
      </div>

      <div class="site-footer__cols">
        <div>
          <h2 class="site-footer__heading">%f_act%</h2>
          <ul>
            <li><a href="yuva-arayan-kopekler.html">%f_dogs%</a></li>
            <li><a href="yuva-arayan-kediler.html">%f_cats%</a></li>
            <li><a href="sahiplen.html">%f_adopt%</a></li>
            <li><a href="gecici-yuva.html">%f_foster%</a></li>
            <li><a href="koruyucu-melek.html">%f_angel%</a></li>
            <li><a href="bagis-yap.html">%f_donate%</a></li>
          </ul>
        </div>
        <div>
          <h2 class="site-footer__heading">%f_org%</h2>
          <ul>
            <li><a href="hikayemiz.html">%f_about%</a></li>
            <li><a href="hikayeler.html">%f_stories%</a></li>
            <li><a href="yasam-alanlari.html">%f_shelters%</a></li>
            <li><a href="iletisim.html">%f_contact%</a></li>
          </ul>
        </div>
        <div>
          <h2 class="site-footer__heading">%f_social%</h2>
          <ul>
            <li><a href="https://www.instagram.com/kurtaranev/" target="_blank" rel="noopener">Instagram</a></li>
            <li><a href="https://www.instagram.com/kurtaranev_kopekleri/" target="_blank" rel="noopener">%f_ig_dogs%</a></li>
            <li><a href="https://www.instagram.com/kurtaranev_kedileri/" target="_blank" rel="noopener">%f_ig_cats%</a></li>
          </ul>
        </div>
        <div>
          <h2 class="site-footer__heading">%f_contact_h%</h2>
          <ul>
            <li><a href="mailto:iletisim@kurtaranev.org">iletisim@kurtaranev.org</a></li>
            <li><a href="https://maps.app.goo.gl/R77zL5Gg42f7ZfXY6" target="_blank" rel="noopener">%f_hours_h%</a></li>
            <li><a href="https://maps.app.goo.gl/PutVz4WqqHoSv1bNA" target="_blank" rel="noopener">%f_hours_b%</a></li>
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
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{alternates}<link rel="icon" href="{base}assets/img/logo.png" type="image/png">
<link rel="stylesheet" href="{base}assets/css/style.css">
{extra_css}</head>
<body>
<a class="visually-hidden" href="#icerik">{skip}</a>

{header}
<main id="icerik">
{body}
</main>

{footer}
{data}<script src="{base}assets/js/i18n.js"></script>
<script src="{base}assets/js/main.js"></script>
{extra_js}</body>
</html>
"""


def fill(template: str, values: dict) -> str:
    for key, val in values.items():
        template = template.replace(f"%{key}%", str(val))
    return template


def rebase_assets(html: str, base: str) -> str:
    """Gövdedeki göreli varlık yollarını alt klasörden çalışacak hale getirir."""
    if not base:
        return html
    return html.replace('src="assets/', f'src="{base}assets/').replace('href="assets/', f'href="{base}assets/')


def build_locale(lang: str, pages: dict) -> int:
    loc = LOCALES[lang]
    out_dir = OUT / loc["out"] if loc["out"] else OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    nav = render_nav_from(loc["nav"])

    for filename, page in pages.items():
        bare = page.get("yalin")
        has_en = filename in PAGES_EN
        if lang == "tr":
            tr_url, en_url = filename, (f"en/{filename}" if has_en else "#")
        else:
            tr_url, en_url = f"../{filename}", filename

        values = dict(loc)
        values.update({
            "tr_url": tr_url,
            "en_url": en_url,
            "tr_current": ' aria-current="true"' if lang == "tr" else "",
            "en_current": ' aria-current="true"' if lang == "en" else "",
        })
        if lang == "tr" and not has_en:
            values["en_current"] = ' aria-disabled="true"'

        header = fill(HEADER, values).replace("__NAV__", nav)
        footer = fill(FOOTER, values)

        extra_css = "".join(
            f'<link rel="stylesheet" href="{loc["base"]}{yol}">\n' for yol in page.get("css", [])
        )
        extra_js = "".join(
            f'<script src="{loc["base"]}{yol}"></script>\n' for yol in page.get("js", [])
        )
        # Katalog sayfaları ilan verisini JS dosyası olarak yükler; böylece site
        # yerel sunucu olmadan, dosyaya çift tıklanarak da çalışır.
        data = ""
        if page.get("veri"):
            data = (f'<script>window.KE_BASE="{loc["base"]}";</script>\n'
                    f'<script src="{loc["base"]}assets/data/animals.js"></script>\n')

        alternates = ""
        if has_en and not bare:
            site = "https://murathanbagdat.github.io/kurtaran-ev-website/"
            alternates = (
                f'<link rel="alternate" hreflang="tr" href="{site}{filename}">\n'
                f'<link rel="alternate" hreflang="en" href="{site}en/{filename}">\n'
            )

        html = SHELL.format(
            lang=lang,
            base=loc["base"],
            skip=loc["skip"],
            title=page["title"],
            description=page["description"],
            alternates=alternates,
            header="" if bare else header,
            footer="" if bare else footer,
            body=rebase_assets(page["body"].strip("\n"), loc["base"]),
            extra_css=extra_css,
            extra_js=extra_js,
            data=data,
        )
        (out_dir / filename).write_text(html, encoding="utf-8")
        rel = f"{loc['out']}/{filename}" if loc["out"] else filename
        print(f"  ✓ site/{rel}")
    return len(pages)


def render_nav_from(nav_items) -> str:
    global NAV
    saved, NAV = NAV, nav_items
    try:
        return render_nav()
    finally:
        NAV = saved


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    n = build_locale("tr", PAGES)
    n += build_locale("en", PAGES_EN)
    print(f"\n{n} sayfa üretildi → {OUT}")


if __name__ == "__main__":
    build()
