# -*- coding: utf-8 -*-
"""English: listing catalogue and single-listing page."""

from pages import crumb, IG_KOPEK, IG_KEDI


def katalog(tur: str) -> str:
    kedi = tur == "kedi"
    baslik = "Cats looking for a home" if kedi else "Dogs looking for a home"
    eyebrow = "Adopt · Cats" if kedi else "Adopt · Dogs"
    lead = (
        "Every cat waiting for adoption is here. Filter by age, sex and compatibility, "
        "then open the listing of the one you'd like to meet."
        if kedi else
        "Every dog waiting for adoption is here. Filter by age, size and compatibility, "
        "then open the listing of the one you'd like to meet."
    )
    ig = IG_KEDI if kedi else IG_KOPEK
    hesap = "@kurtaranev_kedileri" if kedi else "@kurtaranev_kopekleri"
    variant = " page-hero--sky" if kedi else ""

    # Size filter only makes sense for dogs
    boyut_filtresi = "" if kedi else """
        <div class="filter">
          <label for="f-boyut">Size</label>
          <select id="f-boyut" data-filter="boyut">
            <option value="">All</option>
            <option value="kucuk">Small</option>
            <option value="orta">Medium</option>
            <option value="buyuk">Large</option>
          </select>
        </div>"""

    return f"""
<section class="page-hero{variant}">
  <div class="container page-hero__inner page-hero__inner--single">
    <div>
      {crumb(("Home", "index.html"), ("Adopt", None), (baslik, None))}
      <p class="eyebrow">{eyebrow}</p>
      <h1 class="display">{baslik}</h1>
      <p class="page-hero__lead">{lead}</p>
      <div class="page-hero__actions">
        <a class="link-arrow" href="sahiplenme-sureci.html">Adoption process <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="{ig}" target="_blank" rel="noopener">{hesap} <span aria-hidden="true">↗</span></a>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream section--tight">
  <div class="container" data-catalog="{tur}">

    <div class="notice" data-ornek-uyari hidden>
      <span class="notice__icon" aria-hidden="true">⚠</span>
      <span><b>This page contains sample records.</b>
        Listings with a “SAMPLE” badge are not real; they were added to try out the interface.
        They can be removed with one click from the admin panel.</span>
    </div>

    <div class="notice notice--lang" data-lang-uyari hidden>
      <span class="notice__icon" aria-hidden="true">ⓘ</span>
      <span>Listing descriptions are written in Turkish by our field team; the details,
        filters and labels below are in English.</span>
    </div>

    <form class="filters" role="search" aria-label="Listing filters" onsubmit="return false">
      <div class="filter filters__search">
        <label for="f-q">Search</label>
        <input id="f-q" type="search" data-filter="q" placeholder="Name, breed, colour, character…">
      </div>

      <div class="filters__row">
        <div class="filter">
          <label for="f-durum">Status</label>
          <select id="f-durum" data-filter="durum">
            <option value="musait">Available</option>
            <option value="yuva-ariyor">Looking for a home</option>
            <option value="rezerve">Reserved</option>
            <option value="yuvalandi">Adopted</option>
            <option value="">All</option>
          </select>
        </div>
        <div class="filter">
          <label for="f-cinsiyet">Sex</label>
          <select id="f-cinsiyet" data-filter="cinsiyet">
            <option value="">All</option>
            <option value="disi">Female</option>
            <option value="erkek">Male</option>
          </select>
        </div>
        <div class="filter">
          <label for="f-yas">Age</label>
          <select id="f-yas" data-filter="yas">
            <option value="">All</option>
            <option value="yavru">Young (0–1 yr)</option>
            <option value="yetiskin">Adult (1–7 yrs)</option>
            <option value="kidemli">Senior (7+ yrs)</option>
          </select>
        </div>{boyut_filtresi}
        <div class="filter">
          <label for="f-sirala">Sort</label>
          <select id="f-sirala" data-filter="sirala">
            <option value="yeni">Newest first</option>
            <option value="isim">By name</option>
            <option value="yas-artan">Age: youngest first</option>
            <option value="yas-azalan">Age: oldest first</option>
          </select>
        </div>
      </div>

      <div class="filters__toggles">
        <label class="chip"><input type="checkbox" data-filter="kisir"> Neutered</label>
        <label class="chip"><input type="checkbox" data-filter="asili"> Fully vaccinated</label>
        <label class="chip"><input type="checkbox" data-filter="cocuk"> Good with children</label>
        <label class="chip"><input type="checkbox" data-filter="kopek"> Good with dogs</label>
        <label class="chip"><input type="checkbox" data-filter="kedi"> Good with cats</label>
        <button class="filters__clear" type="button" data-clear hidden>Clear filters</button>
      </div>
    </form>

    <div class="results-bar">
      <p class="results-bar__count" data-count role="status"></p>
      <p class="body-sm">Fields we don't have information for are shown as “unknown”.</p>
    </div>

    <div class="animal-grid" data-grid></div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="callout">
      <h2 class="callout__title">Didn't find what you were looking for?</h2>
      <p class="callout__text">New listings are added all the time. Tell us what you're looking for
        and we'll let you know when a suitable animal arrives.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="iletisim.html">Write to us <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="gecici-yuva.html">Become a foster home <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


ILAN_DETAY = """
<section class="section section--cream" style="padding-top:56px;padding-bottom:56px">
  <div class="container">
    <div class="detail-top">
      <p class="breadcrumb">
        <a href="index.html">Home</a><span aria-hidden="true">/</span>
        <a href="yuva-arayan-kopekler.html" data-back-link>Looking for a home</a>
      </p>

      <nav class="pager" aria-label="Browse listings" data-pager hidden>
        <a class="pager__link" href="#" data-pager-prev>
          <span class="pager__arrow" aria-hidden="true">←</span>
          <span class="pager__text"><span class="pager__label">Previous</span><span class="pager__name"></span></span>
        </a>
        <span class="pager__count" data-pager-count></span>
        <a class="pager__link pager__link--next" href="#" data-pager-next>
          <span class="pager__text"><span class="pager__label">Next</span><span class="pager__name"></span></span>
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
      <h2 class="callout__title" data-meet-title>Would you like to meet?</h2>
      <p class="callout__text">Read the
        <a class="meet-cta__process" href="sahiplenme-sureci.html">adoption process</a>
        first, then write to us. Our team will get in touch to arrange an initial conversation.</p>

      <div class="meet-cta__options">
        <a class="btn btn--white btn--sm" href="sahiplen.html" data-meet-option="sahiplenme">Adopt <span aria-hidden="true">→</span></a>
        <a class="btn btn--white btn--sm" href="gecici-yuva.html" data-meet-option="gecici-yuva">Foster <span aria-hidden="true">→</span></a>
        <a class="btn btn--white btn--sm" href="koruyucu-melek.html" data-meet-option="koruyucu-melek">Become a Guardian Angel <span aria-hidden="true">→</span></a>
      </div>
    </div>

    <p class="animal-detail__source meet-band__source" data-meet-source hidden></p>

    <div class="meet-band__cta">
      <a class="btn" href="iletisim.html">I'd like to meet <span aria-hidden="true">→</span></a>
    </div>
  </div>
</section>

<section class="section section--warm section--tight" data-others hidden>
  <div class="container">
    <div class="others__head">
      <h2 class="others__title" data-others-title>Others looking for a home</h2>
      <a class="link-arrow" href="yuva-arayan-kopekler.html" data-others-all>See all <span aria-hidden="true">→</span></a>
    </div>
    <div class="animal-grid" data-others-grid></div>
  </div>
</section>
"""
