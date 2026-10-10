# -*- coding: utf-8 -*-
"""
"İlan modu" — canlı Wix sitesinden (kurtaranev.org) açılan yalın ilan sayfaları.

Yalnızca köpek/kedi kataloğu ve ilan detayı vardır; menü, alt bilgi ya da
prototipin diğer sayfalarına bağlantı yoktur. Üst şeritteki ✕ ilgili Wix
sahiplenme sayfasına döner, "Sahiplenme formu" Wix'in kullandığı Google
Formunu yeni sekmede açar.

Çıktı: site/ilanlar/ (TR) ve site/ilanlar/en/ (EN). Varlık yolları göreli
("../assets/…"); sayfalar ileride ilanlar.kurtaranev.org köküne taşınsa da
çalışır (kökün üstüne çıkan ../ kökte kalır).

Filtre ve ızgara bölümü tam sitedeki katalogdan birebir alınır
(pages.katalog / en.part4.katalog), iki yerde ayrı bakım gerekmez.
"""

from __future__ import annotations

import json
import re

import pages
from en import part4

# Canlı Wix sitesindeki sayfalar ve formlar (10.10.2026'da siteden okundu)
WIX = {
    "tr": {
        "kapat": {"kopek": "https://www.kurtaranev.org/kopek",
                  "kedi": "https://www.kurtaranev.org/kedi"},
        "form": {"kopek": "https://docs.google.com/forms/d/e/1FAIpQLSe0hUSZhEDcGFTGW6aIloQLaK3-xoV6OHq0TkETuLF_aRsZkA/viewform?usp=pp_url",
                 "kedi": "https://forms.gle/UzDyB6KMUQooRy4X7"},
        "varsayilan_kapat": "https://www.kurtaranev.org/sahiplendirme",
    },
    "en": {
        "kapat": {"kopek": "https://en.kurtaranev.org/kopek",
                  "kedi": "https://en.kurtaranev.org/kedi"},
        "form": {"kopek": "https://docs.google.com/forms/d/e/1FAIpQLSdUIcBuv3YeGyWFCpXXa6RkgcGrL06tz0GxlFnyQGwluMHXcQ/viewform?usp=pp_url",
                 "kedi": "https://forms.gle/UzDyB6KMUQooRy4X7"},
        "varsayilan_kapat": "https://en.kurtaranev.org/sahiplendirme",
    },
}

METIN = {
    "tr": {
        "kapat": "Siteye dön",
        "kapat_etiket": "Kapat ve Kurtaran Ev sitesine dön",
        "form_btn": "Sahiplenme formunu doldur",
        "baslik": {"kopek": "Yuva arayan köpekler", "kedi": "Yuva arayan kediler"},
        "eyebrow": {"kopek": "Kurtaran Ev · Köpekler", "kedi": "Kurtaran Ev · Kediler"},
        "lead": ("Instagram'da paylaştığımız güncel ilanlar burada. Yaşam alanlarımızda çok daha "
                 "fazla can yuva bekliyor; aradığınızı bulamazsanız sahiplenme formunu doldurun, "
                 "sizi uygun bir canla eşleştirmeye çalışalım."),
        "geri": "Tüm ilanlar",
        "bant": ("Sahiplendirme formumuzu doldurun ve formda ilgilendiğiniz canın adını belirtin. "
                 "Gönüllülerimiz WhatsApp üzerinden sizinle iletişime geçer."),
        "diger": "Diğer yuva arayanlar",
        "tumu": "Tümünü gör",
        "onceki": "Önceki", "sonraki": "Sonraki",
        "pager": "İlanlar arası geçiş",
        "ilan_title": "İlan | Kurtaran Ev",
    },
    "en": {
        "kapat": "Back to site",
        "kapat_etiket": "Close and return to the Kurtaran Ev website",
        "form_btn": "Fill in the adoption form",
        "baslik": {"kopek": "Dogs looking for a home", "kedi": "Cats looking for a home"},
        "eyebrow": {"kopek": "Kurtaran Ev · Dogs", "kedi": "Kurtaran Ev · Cats"},
        "lead": ("These are our current listings from Instagram. Many more animals are waiting "
                 "at our shelters; if you can't find what you're looking for, fill in the "
                 "adoption form and we'll try to match you with the right one."),
        "geri": "All listings",
        "bant": ("Fill in our adoption form and mention the name of the animal you are "
                 "interested in. Our volunteers will contact you on WhatsApp."),
        "diger": "Others looking for a home",
        "tumu": "See all",
        "onceki": "Previous", "sonraki": "Next",
        "pager": "Browse listings",
        "ilan_title": "Listing | Kurtaran Ev",
    },
}

LISTE = {"kopek": "kopekler.html", "kedi": "kediler.html"}


def _katalog_bolumu(html: str) -> str:
    """Tam sitedeki katalogdan yalnızca filtre + ızgara bölümünü alır."""
    m = re.search(r'<section class="section section--cream section--tight">\s*'
                  r'<div class="container" data-catalog=.*?</section>', html, re.S)
    if not m:
        raise SystemExit("ilanlar.py: katalog bölümü bulunamadı (pages.katalog değişmiş olabilir)")
    return m.group(0)


def ust_serit(lang: str, tur: str | None) -> str:
    t = METIN[lang]
    kapat = WIX[lang]["kapat"][tur] if tur else WIX[lang]["varsayilan_kapat"]
    baslik = t["baslik"][tur] if tur else ""
    return f"""  <header class="embed-bar">
    <div class="container embed-bar__inner">
      <span class="embed-bar__brand"><img src="assets/img/logo.png" alt="Kurtaran Ev" width="44" height="44">
        <span class="embed-bar__title" data-embed-title>{baslik}</span></span>
      <a class="embed-bar__close" href="{kapat}" data-kapat aria-label="{t['kapat_etiket']}">
        <span class="embed-bar__close-text">{t['kapat']}</span><span class="embed-bar__x" aria-hidden="true">✕</span></a>
    </div>
  </header>"""


def ayar_betigi(lang: str) -> str:
    """Sayfadaki JS'e (catalog.js / animal.js) ilan modunu bildirir."""
    ayar = {"liste": LISTE, "form": WIX[lang]["form"], "kapat": WIX[lang]["kapat"],
            "baslik": METIN[lang]["baslik"]}
    return f"<script>window.KE_GOMULU={json.dumps(ayar, ensure_ascii=False)};</script>\n"


def katalog_govde(lang: str, tur: str) -> str:
    t = METIN[lang]
    tam = pages.katalog(tur) if lang == "tr" else part4.katalog(tur)
    variant = " page-hero--sky" if tur == "kedi" else ""
    return f"""
<section class="page-hero page-hero--embed{variant}">
  <div class="container page-hero__inner page-hero__inner--single">
    <div>
      <p class="eyebrow">{t['eyebrow'][tur]}</p>
      <h1 class="display">{t['baslik'][tur]}</h1>
      <p class="page-hero__lead">{t['lead']}</p>
      <div class="page-hero__actions">
        <a class="btn" href="{WIX[lang]['form'][tur]}" target="_blank" rel="noopener">{t['form_btn']} <span aria-hidden="true">↗</span></a>
      </div>
    </div>
  </div>
</section>

{_katalog_bolumu(tam)}
"""


def detay_govde(lang: str) -> str:
    t = METIN[lang]
    return f"""
<section class="section section--cream" style="padding-top:40px;padding-bottom:56px">
  <div class="container">
    <div class="detail-top">
      <p class="breadcrumb"><a href="kopekler.html" data-back-link>{t['geri']}</a></p>

      <nav class="pager" aria-label="{t['pager']}" data-pager hidden>
        <a class="pager__link" href="#" data-pager-prev>
          <span class="pager__arrow" aria-hidden="true">←</span>
          <span class="pager__text"><span class="pager__label">{t['onceki']}</span><span class="pager__name"></span></span>
        </a>
        <span class="pager__count" data-pager-count></span>
        <a class="pager__link pager__link--next" href="#" data-pager-next>
          <span class="pager__text"><span class="pager__label">{t['sonraki']}</span><span class="pager__name"></span></span>
          <span class="pager__arrow" aria-hidden="true">→</span>
        </a>
      </nav>
    </div>

    <div class="animal-detail" data-animal-detail></div>
  </div>
</section>

<section class="section section--cream meet-band" data-meet-band hidden>
  <div class="container">
    <div class="callout meet-cta">
      <h2 class="callout__title" data-meet-title></h2>
      <p class="callout__text">{t['bant']}</p>
    </div>

    <p class="animal-detail__source meet-band__source" data-meet-source hidden></p>

    <div class="meet-band__cta">
      <a class="btn" href="{WIX[lang]['form']['kopek']}" data-form-link target="_blank" rel="noopener">{t['form_btn']} <span aria-hidden="true">↗</span></a>
    </div>
  </div>
</section>

<section class="section section--warm section--tight" data-others hidden>
  <div class="container">
    <div class="others__head">
      <h2 class="others__title" data-others-title>{t['diger']}</h2>
      <a class="link-arrow" href="kopekler.html" data-others-all>{t['tumu']} <span aria-hidden="true">→</span></a>
    </div>
    <div class="animal-grid" data-others-grid></div>
  </div>
</section>
"""


def sayfalar(lang: str) -> dict:
    """{dosya adı: {title, description, tur, body, js}}"""
    t = METIN[lang]
    tr = lang == "tr"
    return {
        "kopekler.html": {
            "title": f"{t['baslik']['kopek']} | Kurtaran Ev",
            "description": ("Sahiplendirilmeyi bekleyen köpeklerimiz." if tr
                            else "Dogs waiting for adoption at Kurtaran Ev."),
            "tur": "kopek", "body": katalog_govde(lang, "kopek"), "js": "assets/js/catalog.js",
        },
        "kediler.html": {
            "title": f"{t['baslik']['kedi']} | Kurtaran Ev",
            "description": ("Sahiplendirilmeyi bekleyen kedilerimiz." if tr
                            else "Cats waiting for adoption at Kurtaran Ev."),
            "tur": "kedi", "body": katalog_govde(lang, "kedi"), "js": "assets/js/catalog.js",
        },
        "ilan.html": {
            "title": t["ilan_title"],
            "description": ("Yuva arayan bir canın ilan detayı." if tr
                            else "Details of an animal looking for a home."),
            "tur": None, "body": detay_govde(lang), "js": "assets/js/animal.js",
        },
    }
