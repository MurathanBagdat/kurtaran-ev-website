# -*- coding: utf-8 -*-
"""Sayfa gövdeleri. Tasarım dili: Kurtaran_Ev_Website_Prototype.pdf"""

IG_KOPEK = "https://www.instagram.com/kurtaranev_kopekleri/"
IG_KEDI = "https://www.instagram.com/kurtaranev_kedileri/"
IG_ANA = "https://www.instagram.com/kurtaranev/"


def page_hero(eyebrow, title, lead, actions="", figure="", variant="", breadcrumb=""):
    """İç sayfaların üst bloğu."""
    single = "" if figure else " page-hero__inner--single"
    fig = f'<figure class="page-hero__figure">{figure}</figure>' if figure else ""
    return f"""
<section class="page-hero{variant}">
  <div class="container page-hero__inner{single}">
    <div>
      {breadcrumb}
      <p class="eyebrow">{eyebrow}</p>
      <h1 class="display">{title}</h1>
      <p class="page-hero__lead">{lead}</p>
      {f'<div class="page-hero__actions">{actions}</div>' if actions else ''}
    </div>
    {fig}
  </div>
</section>
"""


def crumb(*parts):
    links = []
    for label, href in parts:
        links.append(f'<a href="{href}">{label}</a>' if href else f"<span>{label}</span>")
    return '<p class="breadcrumb">' + '<span aria-hidden="true">/</span>'.join(links) + "</p>"


# ===========================================================================
# ANA SAYFA — PDF prototipinin birebir karşılığı
# ===========================================================================
INDEX = """
<section class="hero">
  <div class="container hero__inner">
    <div class="hero__text">
      <p class="eyebrow">İstanbul’da dört yaşam alanı</p>
      <h1 class="display display--hero hero__title">Her can, güvende<br class="lb">
        ve <em>sevildiği</em> bir<br class="lb"> hayatı hak eder.</h1>
      <p class="lead hero__lead">Kurtarıyor, tedavi ediyor, rehabilite ediyor ve doğru yuvalarla
        buluşturuyoruz. 4 yaşam alanımızda 1500'den fazla kedi ve köpek için ve daha fazlası için
        her gün buradayız.</p>
      <div class="hero__actions">
        <a class="btn" href="hikayemiz.html">Misyonumuz <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="#yuva-arayanlar">Yuva arayanları gör <span aria-hidden="true">↘</span></a>
      </div>
    </div>

    <div class="hero__media">
      <span class="hero__blob" aria-hidden="true"></span>
      <div class="arch">
        <img src="assets/img/hero-kucak.jpg" width="1536" height="2048"
             alt="Sarı bandanalı bir gönüllü, siyah beyaz bir köpeği çimenlikte kucaklıyor.">
      </div>
      <p class="sticker sticker--hero">Biraz ilgi, biraz güven, bambaşka bir hayat.</p>
    </div>
  </div>
</section>

<section class="stats" aria-label="Rakamlarla Kurtaran Ev">
  <div class="stats__grid">
    <div class="stats__cell">
      <span class="stats__num">1.200</span>
      <span class="stats__label">köpek</span>
    </div>
    <div class="stats__cell">
      <span class="stats__num">600</span>
      <span class="stats__label">kedi</span>
    </div>
    <div class="stats__cell">
      <span class="stats__num">4</span>
      <span class="stats__label">yaşam alanı</span>
    </div>
    <div class="stats__cell">
      <p class="stats__note">Kurtarma, tedavi, rehabilitasyon ve yaşam boyu bakım—her biri
        sizin desteğinizle mümkün.</p>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="section__intro">
      <p class="eyebrow">İyiliğin tek bir yolu yok</p>
      <h2 class="display">Siz nasıl yanımızda olursunuz?</h2>
      <p class="body-lg">Zamanınızla, evinizi açarak ya da düzenli destek vererek
        bir hayatın yönünü değiştirebilirsiniz.</p>
    </div>

    <div class="paths">
      <a class="path-card path-card--green" href="yuva-arayan-kopekler.html">
        <span class="path-card__num">01</span>
        <h3 class="path-card__title">Sahiplen</h3>
        <p class="path-card__text">Yeni bir dost değil, ailenizin yeni bir üyesiyle tanışın.</p>
        <span class="path-card__arrow" aria-hidden="true">↗</span>
      </a>
      <a class="path-card path-card--sky" href="gecici-yuva.html">
        <span class="path-card__num">02</span>
        <h3 class="path-card__title">Geçici yuva ol</h3>
        <p class="path-card__text">Evinizde açılan kısa süreli yer, sahada yeni bir hayat kurtarır.</p>
        <span class="path-card__arrow" aria-hidden="true">↗</span>
      </a>
      <a class="path-card path-card--orange" href="koruyucu-melek.html">
        <span class="path-card__num">03</span>
        <h3 class="path-card__title">Koruyucu Melek ol</h3>
        <p class="path-card__text">Aylık düzenli destekle bakımın devamlılığını sağlayın.</p>
        <span class="path-card__arrow" aria-hidden="true">↗</span>
      </a>
      <a class="path-card path-card--cream" href="gonullu-ol.html">
        <span class="path-card__num">04</span>
        <h3 class="path-card__title">Gönüllü ol</h3>
        <p class="path-card__text">İhtiyaç duyulan yerde beceriniz ve zamanınızla yanımızda olun.</p>
        <span class="path-card__arrow" aria-hidden="true">↗</span>
      </a>
    </div>
  </div>
</section>

<section class="section section--warm" id="yuva-arayanlar">
  <div class="container adopt">
    <div>
      <p class="eyebrow">Yuva arayanlar</p>
      <h2 class="display">Yuva<br class="lb"> İlanlarımız</h2>
      <p class="body-lg" style="margin:1.4rem 0 1.9rem; max-width:29rem;">Yaşam alanlarımızda yuva
        bekleyen yüzlerce can var; ne yazık ki her birini tek tek paylaşmaya yetişemiyoruz.
        Aradığınız dostu burada bulamıyorsanız ya da emin değilseniz sahiplendirme formumuzu
        doldurun, doğru eşleşmeyi birlikte bulalım.</p>
      <a class="link-arrow" href="sahiplen.html">Sahiplenme Formu <span aria-hidden="true">→</span></a>
    </div>

    <div class="adopt__cards">
      <a class="adopt-card" href="yuva-arayan-kopekler.html">
        <img src="assets/img/kopek-portre.jpg" width="2302" height="1535"
             alt="Kameraya bakan sarı bir köpek yavrusu.">
        <span class="adopt-card__caption">
          <span class="adopt-card__handle">Yuva arayan köpeklerimiz</span>
          <span class="adopt-card__title">Köpeklerle tanış</span>
        </span>
      </a>
      <a class="adopt-card adopt-card--cat" href="yuva-arayan-kediler.html">
        <img src="assets/img/kedi-yasam-alani.jpg" width="2048" height="1152"
             alt="Kedi yaşam alanının koridoru; duvarda tırmanma rafları ve yataklar.">
        <span class="adopt-card__caption">
          <span class="adopt-card__handle">Yuva arayan kedilerimiz</span>
          <span class="adopt-card__title">Kedilerle tanış</span>
        </span>
      </a>
    </div>
  </div>
</section>

<div class="split split--orange split--media-left">
  <div class="split__media">
    <img src="assets/img/bahce-kopekler.jpg" width="1200" height="1600"
         alt="Hadımköy yaşam alanının bahçesinde toplanmış köpekler.">
    <p class="sticker sticker--plain sticker--onmedia">Geçici yuva = yeni kurtarma alanı</p>
  </div>
  <div class="split__body">
    <p class="eyebrow">Evinizde açılan yer, sahada hayat kurtarır</p>
    <h2 class="display">Bir kafes boşalır.<br class="lb"> Yeni bir can<br class="lb"> kurtarılır.</h2>
    <p class="body-md" style="max-width:30rem;">Geçici yuvalık bir sahiplenme denemesi değildir.
      Bir hayvan kalıcı yuvasına hazırlanırken ona güvenli, kısa süreli bir ev sunmaktır.</p>
    <ul class="checklist">
      <li>Süreç boyunca Kurtaran Ev desteği</li>
      <li>Hayvanın ihtiyaçlarına göre doğru eşleştirme</li>
      <li>Açık sorumluluklar ve takip</li>
    </ul>
    <div>
      <a class="btn btn--sky" href="gecici-yuva.html">Süreci öğren ve başvur <span aria-hidden="true">→</span></a>
    </div>
  </div>
</div>

<div class="split split--navy split--media-left">
  <div class="split__media">
    <img src="assets/img/kopek-portre.jpg" width="2302" height="1535"
         alt="Elini bir gönüllünün dizine koymuş, kameraya bakan köpek.">
    <p class="sticker sticker--green sticker--onmedia">Her ay yanında ol.</p>
  </div>
  <div class="split__body">
    <p class="eyebrow">Düzenli destek, sürdürülebilir bakım</p>
    <h2 class="display">Koruyucu Meleği olun.</h2>
    <p class="body-md" style="max-width:33rem;">Aylık ₺3.000’den başlayan düzenli desteğiniz;
      mama, tedavi, ilaç ve yaşam alanlarının devamlılığına katkı sağlar.</p>

    <div class="amounts" data-amounts data-amount-target="#melek-cta-label">
      <p class="amounts__label">Aylık destek tutarınızı seçin</p>
      <div class="amounts__options">
        <button class="amount is-active" type="button" data-amount="3000" aria-pressed="true">₺3.000</button>
        <button class="amount" type="button" data-amount="5000" aria-pressed="false">₺5.000</button>
        <button class="amount" type="button" data-amount="7500" aria-pressed="false">₺7.500</button>
        <button class="amount" type="button" data-amount="custom" aria-pressed="false">Diğer</button>
        <input class="amount-custom" type="number" min="100" step="100" hidden
               aria-label="Diğer tutar (₺)" placeholder="₺ tutar">
      </div>
    </div>

    <div>
      <a class="btn btn--yellow" href="koruyucu-melek.html">
        <span id="melek-cta-label">₺3.000 ile başla</span> <span aria-hidden="true">→</span>
      </a>
    </div>
    <p class="amounts__note">Desteğinizi dilediğiniz zaman değiştirebilir veya sonlandırabilirsiniz.</p>
  </div>
</div>

<section class="section section--cream">
  <div class="container">
    <div class="section__head">
      <div>
        <p class="eyebrow">Hikayeler ve sahadan haberler</p>
        <h2 class="display">Umudu görünür kılanlar.</h2>
      </div>
      <a class="link-arrow" href="hikayeler.html">Tüm hikayeler <span aria-hidden="true">→</span></a>
    </div>

    <div class="stories">
      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-lucy.jpg" width="460" height="430"
               alt="Sarı koltukta Lucy’yi kucağına almış gülümseyen bir kadın.">
        </figure>
        <span class="story__tag">Mutluluk hikayesi</span>
        <h3 class="story__title">Lucy’nin yeni hayatı</h3>
        <p class="story__excerpt">Kanser tedavisi devam ederken bir aile ona yalnızca evini değil,
          bütün kalbini açtı.</p>
        <a class="link-arrow link-arrow--sm" href="hikayeler.html">Hikayeyi oku <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-mobil-klinik.png" width="1336" height="1194"
               alt="Kurtaran Araç mobil klinik projesinin tanıtım görseli.">
        </figure>
        <span class="story__tag">Proje · Kurumsal iş birliği</span>
        <h3 class="story__title">Mobil Klinik: Kurtaran Araç</h3>
        <p class="story__excerpt">Anadolu Sigorta’nın desteğiyle tedavi, kısırlaştırma ve kontrolleri
          ihtiyaç olan yere taşıyoruz.</p>
        <a class="link-arrow link-arrow--sm" href="hikayeler.html">Hikayeyi oku <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-kevok.jpg" width="1600" height="1332"
               alt="Sahilde beyaz köpeği Kevok’u kucağında taşıyan bir adam.">
        </figure>
        <span class="story__tag">Mutluluk hikayesi</span>
        <h3 class="story__title">Kevok sonunda görüldü</h3>
        <p class="story__excerpt">Irkı ve yaşı yüzünden yıllarca gözden kaçan Kevok, onu gerçekten
          gören insanla tanıştı.</p>
        <a class="link-arrow link-arrow--sm" href="hikayeler.html">Hikayeyi oku <span aria-hidden="true">↗</span></a>
      </article>
    </div>
  </div>
</section>

<section class="section section--sky section--tight">
  <div class="container areas">
    <div>
      <p class="eyebrow">Kurtaran Ev’i tanıyın</p>
      <h2 class="display">Dört alan. Tek söz:<br class="lb"> hiçbirini geride<br class="lb"> bırakmamak.</h2>
      <p class="body-lg" style="margin:1.4rem 0 2rem; max-width:30rem;">Tedavi, rehabilitasyon,
        sahiplendirme ve yaşam boyu bakım çalışmalarımız İstanbul’daki dört farklı alanda devam ediyor.</p>
      <a class="btn btn--ghost" href="yasam-alanlari.html">Yaşam alanlarını keşfet <span aria-hidden="true">→</span></a>
    </div>

    <div class="areas__list">
      <div class="area-row">
        <span class="area-row__num">01</span>
        <h3 class="area-row__name">Hadımköy Yaşam Alanı</h3>
        <p class="area-row__desc">Köpeklerin bakım ve rehabilitasyonu</p>
      </div>
      <div class="area-row">
        <span class="area-row__num">02</span>
        <h3 class="area-row__name">Kedi Yaşam Alanı</h3>
        <p class="area-row__desc">Kedilerin güvenli yaşam ve bakım alanı</p>
      </div>
      <div class="area-row">
        <span class="area-row__num">03</span>
        <h3 class="area-row__name">Beşiktaş Kedi Sahiplendirme Alanı</h3>
        <p class="area-row__desc">Tanışma ve sahiplendirme</p>
      </div>
      <div class="area-row">
        <span class="area-row__num">04</span>
        <h3 class="area-row__name">Dumankaya Kedi Tedavi Alanı</h3>
        <p class="area-row__desc">Tedavi ve iyileşme</p>
      </div>
    </div>
  </div>
</section>

<section class="newsletter">
  <div class="container newsletter__inner">
    <div>
      <p class="eyebrow">Gelişmeleri takip edin</p>
      <h2 class="display">Bültenimize abone olun.</h2>
    </div>
    <form data-demo-form data-demo-message="Teşekkürler! Bültene kayıt bu yerel prototipte henüz bağlı değil.">
      <label class="newsletter__label" for="bulten-eposta">E-posta adresi</label>
      <div class="newsletter__form">
        <input id="bulten-eposta" type="email" name="email" placeholder="ornek@email.com" required>
        <button type="submit">Abone ol →</button>
      </div>
      <p class="form-status" role="status"></p>
    </form>
  </div>
</section>
""".replace("__IG_KOPEK__", IG_KOPEK).replace("__IG_KEDI__", IG_KEDI)


# ===========================================================================
# YUVA OL
# ===========================================================================
SAHIPLEN = page_hero(
    "Yuva Ol · Sahiplen",
    "Yuva arayanlarla<br class=\"lb\"> tanışın.",
    "Sahiplendirme ilanlarımızı kedi ve köpek hesaplarımızda güncel tutuyoruz. "
    "Tanışmak istediğiniz canı gördüğünüzde bize yazın; gerisini birlikte yürütelim.",
    actions='<a class="btn" href="yuva-arayan-kopekler.html">Yuva arayan köpekler <span aria-hidden="true">→</span></a>'
            '<a class="btn btn--sky" href="yuva-arayan-kediler.html">Yuva arayan kediler <span aria-hidden="true">→</span></a>'
            '<a class="link-arrow" href="sahiplenmeden-once.html">Sahiplenmeden önce <span aria-hidden="true">↘</span></a>',
    figure='<img src="assets/img/kopek-portre.jpg" alt="Yuva arayan sarı bir köpek kameraya bakıyor.">',
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Yuva Ol", None), ("Sahiplen", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="section__head">
      <div>
        <p class="eyebrow">Güncel ilanlar</p>
        <h2 class="display">Bugün yuva arayanlar</h2>
      </div>
      <a class="link-arrow" href="__IG_ANA__" target="_blank" rel="noopener">Kurtaran Ev Instagram <span aria-hidden="true">↗</span></a>
    </div>

    <div class="adopt__cards" style="grid-template-columns:repeat(2,minmax(0,400px));">
      <a class="adopt-card" href="yuva-arayan-kopekler.html">
        <img src="assets/img/kopek-portre.jpg" alt="Yuva arayan köpekler.">
        <span class="adopt-card__caption">
          <span class="adopt-card__handle">Yuva arayan köpekler</span>
          <span class="adopt-card__title">Köpeklerle tanış</span>
          <span class="adopt-card__sub" data-sayac="kopek">Tüm ilanlara göz at</span>
        </span>
      </a>
      <a class="adopt-card adopt-card--cat" href="yuva-arayan-kediler.html">
        <img src="assets/img/kedi-yasam-alani.jpg" alt="Yuva arayan kediler.">
        <span class="adopt-card__caption">
          <span class="adopt-card__handle">Yuva arayan kediler</span>
          <span class="adopt-card__title">Kedilerle tanış</span>
          <span class="adopt-card__sub" data-sayac="kedi">Tüm ilanlara göz at</span>
        </span>
      </a>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <p class="eyebrow">Kime yuva olabilirsiniz?</p>
    <h2 class="display" style="margin-bottom:2.6rem;">Her canın ihtiyacı farklı.</h2>
    <div class="tiles">
      <article class="tile tile--white">
        <span class="tile__kicker">Yavrular</span>
        <h3 class="tile__title">Enerjisi yüksek, öğrenmeye aç</h3>
        <p class="tile__text">Eğitim, aşı takvimi ve sosyalleşme için ilk aylarda düzenli
          zaman ayırabilecek yuvalar arıyoruz.</p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">Yetişkinler</span>
        <h3 class="tile__title">Karakteri belli, uyumu hızlı</h3>
        <p class="tile__text">Mizacını bildiğimiz için evinize ve yaşam ritminize en uygun
          eşleştirmeyi yapmak çok daha kolay.</p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">Özel bakım</span>
        <h3 class="tile__title">Sabır isteyen, kalpten bağlayan</h3>
        <p class="tile__text">Yaşlı, kronik hastalığı olan ya da engelli canlar için tedavi
          desteğini birlikte planlıyoruz.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--cream section--tight">
  <div class="container">
    <div class="callout">
      <h2 class="callout__title">Tanışmak istediğiniz bir can mı var?</h2>
      <p class="callout__text">İlanın altına yorum bırakın ya da doğrudan bize yazın.
        Ekibimiz sizinle iletişime geçip ön görüşmeyi planlasın.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="iletisim.html">Bize yazın <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="sahiplenme-sureci.html">Süreç nasıl işliyor? <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
""".replace("__IG_KOPEK__", IG_KOPEK).replace("__IG_KEDI__", IG_KEDI).replace("__IG_ANA__", IG_ANA)


GECICI_YUVA = page_hero(
    "Yuva Ol · Geçici Yuva",
    "Bir kafes boşalır.<br class=\"lb\"> Yeni bir can kurtarılır.",
    "Geçici yuvalık bir sahiplenme denemesi değildir. Bir hayvan kalıcı yuvasına hazırlanırken "
    "ona güvenli, kısa süreli bir ev sunmaktır.",
    actions='<a class="btn btn--sky" href="#basvuru">Geçici yuva başvurusu <span aria-hidden="true">→</span></a>',
    figure='<img src="assets/img/bahce-kopekler.jpg" alt="Yaşam alanının bahçesinde bekleyen köpekler.">',
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Yuva Ol", None), ("Geçici Yuva", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="section__intro">
      <p class="eyebrow">Nasıl işliyor?</p>
      <h2 class="display">Dört adımda geçici yuva</h2>
    </div>
    <div class="steps">
      <div class="step">
        <span class="step__num">01</span>
        <div>
          <h3 class="step__title">Başvuru ve tanışma</h3>
          <p class="step__text">Formu doldurun; ev düzeniniz, yaşam ritminiz ve daha önceki
            deneyimleriniz üzerine kısa bir görüşme yapalım.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">02</span>
        <div>
          <h3 class="step__title">Doğru eşleştirme</h3>
          <p class="step__text">Hayvanın ihtiyaçlarıyla evinizin koşullarını eşleştiriyoruz.
            Yavru, yetişkin ya da tedavi sürecindeki bir can olabilir.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">03</span>
        <div>
          <h3 class="step__title">Süreç boyunca destek</h3>
          <p class="step__text">Mama, tıbbi takip ve davranış danışmanlığı Kurtaran Ev’de.
            Siz güvenli bir oda ve düzenli ilgi sağlıyorsunuz.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">04</span>
        <div>
          <h3 class="step__title">Kalıcı yuvaya uğurlama</h3>
          <p class="step__text">Kalıcı yuvası bulunduğunda geçişi birlikte planlıyoruz.
            Sizin bıraktığınız yer, kurtarılacak yeni bir can demek.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <article class="tile tile--sky">
        <span class="tile__kicker">Kurtaran Ev karşılar</span>
        <h3 class="tile__title">Bakımın masrafı size kalmaz</h3>
        <ul class="bullets">
          <li>Mama, kum ve temel bakım malzemesi</li>
          <li>Aşı, tedavi ve veteriner kontrolleri</li>
          <li>Taşıma kafesi, tasma ve yatak</li>
          <li>Davranış sorunlarında danışmanlık</li>
        </ul>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">Sizden beklediğimiz</span>
        <h3 class="tile__title">Güvenli bir alan ve düzenli ilgi</h3>
        <ul class="bullets">
          <li>Pencere ve balkon güvenliği alınmış bir ev</li>
          <li>Günde birkaç kez beslenme ve temizlik</li>
          <li>Fotoğraf ve gelişim paylaşımı</li>
          <li>Kontrol randevularına ulaşım desteği</li>
        </ul>
      </article>
    </div>
  </div>
</section>

<section class="section section--cream section--tight" id="basvuru">
  <div class="container">
    <p class="eyebrow">Başvuru</p>
    <h2 class="display" style="margin-bottom:2.2rem;">Evinizde bir yer var mı?</h2>
    <form class="form-grid" data-demo-form
          data-demo-message="Başvurunuz alındı sayılmaz — bu yerel prototipte form gönderimi bağlı değil.">
      <div class="field"><label for="gy-ad">Ad soyad</label><input id="gy-ad" name="ad" required></div>
      <div class="field"><label for="gy-eposta">E-posta</label><input id="gy-eposta" type="email" name="eposta" required></div>
      <div class="field"><label for="gy-telefon">Telefon</label><input id="gy-telefon" type="tel" name="telefon"></div>
      <div class="field">
        <label for="gy-tur">Hangi canlara yuva olabilirsiniz?</label>
        <select id="gy-tur" name="tur">
          <option>Kedi</option><option>Köpek</option><option>Fark etmez</option>
        </select>
      </div>
      <div class="field field--full">
        <label for="gy-not">Ev düzeniniz ve deneyiminiz</label>
        <textarea id="gy-not" name="not" placeholder="Evde başka hayvan var mı, gün içinde ne kadar süre evdesiniz?"></textarea>
      </div>
      <div class="field field--full">
        <button class="btn btn--sky" type="submit">Başvuruyu gönder <span aria-hidden="true">→</span></button>
        <p class="form-status" role="status"></p>
      </div>
    </form>
  </div>
</section>
"""


SAHIPLENMEDEN_ONCE = page_hero(
    "Yuva Ol · Sahiplenmeden Önce",
    "Ön hazırlık ve<br class=\"lb\"> gerçekçi beklentiler.",
    "Sahiplenmek bir kararla değil, bir hazırlıkla başlar. Karar vermeden önce birlikte "
    "düşünmenizi istediğimiz birkaç başlık var.",
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Yuva Ol", None), ("Sahiplenmeden Önce", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="tiles">
      <article class="tile tile--warm">
        <span class="tile__kicker">Zaman</span>
        <h3 class="tile__title">10–15 yıllık bir söz</h3>
        <p class="tile__text">Taşınma, iş değişikliği, evlilik, çocuk… Hayat planınızda bu canın
          da bir yeri olmalı.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Bütçe</span>
        <h3 class="tile__title">Düzenli giderler</h3>
        <p class="tile__text">Mama, kum, aşı, parazit koruması ve beklenmedik tedaviler için
          aylık bir bütçe ayırmanız gerekir.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Ev</span>
        <h3 class="tile__title">Güvenlik önlemleri</h3>
        <p class="tile__text">Kediler için pencere ve balkon teli şart. Köpekler için güvenli
          bir yürüyüş rutini planlayın.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Uyum</span>
        <h3 class="tile__title">İlk haftalar sancılı olabilir</h3>
        <p class="tile__text">Saklanma, iştahsızlık, tuvalet kazaları normaldir. Sabır süreci
          hızlandıran tek şeydir.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Ev halkı</span>
        <h3 class="tile__title">Herkes hemfikir mi?</h3>
        <p class="tile__text">Evdeki tüm bireylerin —ve varsa diğer hayvanların— bu karara
          dahil olması gerekir.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Beklenti</span>
        <h3 class="tile__title">Kurtarılmış bir can, hazır bir evcil hayvan değildir</h3>
        <p class="tile__text">Geçmişi olan bir canla tanışıyorsunuz. Güven zamanla kuruluyor.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <p class="eyebrow">Sık sorulanlar</p>
    <h2 class="display" style="margin-bottom:2.4rem;">Merak edilenler</h2>
    <div class="faq">
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false">Apartmanda köpek beslenir mi?</button>
        <div class="faq__a"><p>Beslenir. Belirleyici olan evin metrekaresi değil, köpeğin günlük
          hareket ihtiyacının karşılanması. Günde iki ila üç yürüyüş planlayabiliyorsanız
          apartman dairesi sorun değildir.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false">Evde çocuk varken sahiplenmek doğru mu?</button>
        <div class="faq__a"><p>Evet, doğru eşleştirme yapıldığında. Çocuklu evler için sosyalleşmiş,
          sabırlı mizaçlı canları öneriyoruz ve ilk günlerde nasıl davranılacağını birlikte konuşuyoruz.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false">Evimde başka bir hayvan var, uyum sağlar mı?</button>
        <div class="faq__a"><p>Çoğunlukla sağlar. Tanıştırma kademeli yapılmalı: ayrı odalar, koku
          değişimi ve kısa süreli gözetimli buluşmalar. Bu süreçte size yol gösteriyoruz.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false">Sahiplenme ücretli mi?</button>
        <div class="faq__a"><p>Sahiplendirme karşılığında ücret talep etmiyoruz. Dilerseniz bakımda olan
          diğer canlar için bağış yapabilirsiniz.</p></div>
      </div>
    </div>

    <div class="callout callout--sky" style="margin-top:3rem;">
      <h2 class="callout__title">Hazır hissediyor musunuz?</h2>
      <p class="callout__text">Sıradaki adım süreci okumak. Hangi belgelerin gerektiğini ve
        görüşmelerin nasıl ilerlediğini orada bulacaksınız.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="sahiplenme-sureci.html">Sahiplenme sürecine geç <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


SAHIPLENME_SURECI = page_hero(
    "Yuva Ol · Sahiplenme Süreci",
    "Nasıl işliyor,<br class=\"lb\"> neler gerekiyor?",
    "Sahiplendirme bizim için bir teslimat değil, bir eşleştirme. Aşağıdaki adımlar ortalama "
    "iki ila üç hafta sürüyor.",
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Yuva Ol", None), ("Sahiplenme Süreci", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="steps">
      <div class="step">
        <span class="step__num">01</span>
        <div>
          <h3 class="step__title">İlanı inceleyin</h3>
          <p class="step__text">Sahiplendirme hesaplarımızdaki ilanlarda her canın yaşı, mizacı ve
            sağlık durumu yazıyor. Size uygun olduğunu düşündüğünüz canı seçin.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">02</span>
        <div>
          <h3 class="step__title">Ön görüşme</h3>
          <p class="step__text">Kısa bir telefon ya da yüz yüze görüşmede yaşam düzeninizi,
            beklentilerinizi ve evin koşullarını konuşuyoruz.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">03</span>
        <div>
          <h3 class="step__title">Tanışma ziyareti</h3>
          <p class="step__text">Yaşam alanımızda ya da geçici yuvasında tanışıyorsunuz.
            Aceleye gerek yok; iki taraf da rahat hissetmeli.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">04</span>
        <div>
          <h3 class="step__title">Ev hazırlığı ve sözleşme</h3>
          <p class="step__text">Kedilerde pencere–balkon teli kontrolü yapılır. Sahiplendirme
            sözleşmesi imzalanır, kimlik bilgileri kayda alınır.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">05</span>
        <div>
          <h3 class="step__title">Eve geçiş ve takip</h3>
          <p class="step__text">İlk hafta, birinci ay ve altıncı ayda görüşüyoruz. Sorun çıkarsa
            kapımız her zaman açık — geri dönüş de bir seçenektir.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <div>
        <p class="eyebrow">Gerekenler</p>
        <h2 class="display" style="font-size:2.4rem; margin-bottom:1.4rem;">Yanınızda getirin</h2>
        <ul class="bullets bullets--lg">
          <li>Kimlik belgesi</li>
          <li>18 yaşını doldurmuş olmak</li>
          <li>Evde yaşayan herkesin onayı</li>
          <li>Kedi sahipleniyorsanız pencere/balkon teli fotoğrafı</li>
          <li>Taşıma kafesi (temin edemezseniz biz sağlarız)</li>
        </ul>
      </div>
      <div class="callout callout--cream">
        <h2 class="callout__title">Neden bu kadar ayrıntılı?</h2>
        <p class="callout__text">Geri dönen her hayvan, kazanılmış güvenin yeniden kırılması demek.
          Süreci yavaşlatan her soru, kalıcı bir yuvanın ihtimalini artırıyor.</p>
        <div class="callout__actions">
          <a class="btn" href="sahiplen.html">Yuva arayanları gör <span aria-hidden="true">→</span></a>
        </div>
      </div>
    </div>
  </div>
</section>
"""


# ===========================================================================
# DESTEK OL
# ===========================================================================
BAGIS_YAP = page_hero(
    "Destek Ol · Bağış Yap",
    "Desteğiniz bir<br class=\"lb\"> günü değil, bir<br class=\"lb\"> ömrü değiştirir.",
    "Her bağış doğrudan mamaya, tedaviye, ilaca ve yaşam alanlarının giderlerine gidiyor. "
    "Tek seferlik ya da düzenli — ikisi de bizim için çok kıymetli.",
    actions='<a class="btn" href="#bagis-yontemleri">Bağış yöntemleri <span aria-hidden="true">→</span></a>'
            '<a class="link-arrow" href="koruyucu-melek.html">Düzenli destek ver <span aria-hidden="true">↘</span></a>',
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Destek Ol", None), ("Bağış Yap", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">Bağışınız nereye gidiyor?</p>
    <h2 class="display" style="margin-bottom:2.6rem;">Somut karşılıklar</h2>
    <div class="tiles tiles--4">
      <article class="tile tile--yellow">
        <span class="tile__kicker">₺500</span>
        <h3 class="tile__title">Bir haftalık mama</h3>
        <p class="tile__text">Bir köpeğin bir haftalık kuru mama ihtiyacını karşılar.</p>
      </article>
      <article class="tile tile--sky">
        <span class="tile__kicker">₺1.500</span>
        <h3 class="tile__title">Aşı ve parazit koruması</h3>
        <p class="tile__text">Bir canın yıllık karma aşı ve iç–dış parazit korumasını kapsar.</p>
      </article>
      <article class="tile tile--orange">
        <span class="tile__kicker">₺3.000</span>
        <h3 class="tile__title">Kısırlaştırma</h3>
        <p class="tile__text">Bir kısırlaştırma operasyonu ve sonrası bakım masrafı.</p>
      </article>
      <article class="tile tile--green">
        <span class="tile__kicker">₺7.500+</span>
        <h3 class="tile__title">Acil tedavi</h3>
        <p class="tile__text">Kırık, kaza ya da ileri düzey tedavi gerektiren vakalar için.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight" id="bagis-yontemleri">
  <div class="container">
    <p class="eyebrow">Nasıl bağış yapabilirsiniz?</p>
    <h2 class="display" style="margin-bottom:2.4rem;">Üç yol</h2>
    <div class="tiles">
      <article class="tile tile--white">
        <span class="tile__kicker">01</span>
        <h3 class="tile__title">Banka havalesi / EFT</h3>
        <p class="tile__text">Dernek hesabımıza doğrudan gönderim yapabilirsiniz. Açıklama kısmına
          adınızı yazmanız makbuz için yeterli.</p>
        <p class="tile__meta">Hesap bilgileri için: <a href="mailto:iletisim@kurtaranev.org">iletisim@kurtaranev.org</a></p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">02</span>
        <h3 class="tile__title">Düzenli bağış</h3>
        <p class="tile__text">Koruyucu Melek olarak her ay otomatik destek verin; bakımın
          sürekliliğini planlamamızı sağlar.</p>
        <p class="tile__meta"><a href="koruyucu-melek.html">Koruyucu Melek ol →</a></p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">03</span>
        <h3 class="tile__title">Ayni bağış</h3>
        <p class="tile__text">Mama, kum, ilaç, battaniye ve temizlik malzemesi. Öncelikli
          ihtiyaç listesini güncel tutuyoruz.</p>
        <p class="tile__meta"><a href="https://www.amazon.com.tr/kurtaranev" target="_blank" rel="noopener">Amazon ihtiyaç listesi ↗</a> · <a href="guncel-ihtiyaclar.html">Güncel ihtiyaçlar →</a></p>
      </article>
    </div>

    <div class="callout" style="margin-top:3rem;">
      <h2 class="callout__title">Bağışınızı anlamlı bir hediyeye dönüştürün</h2>
      <p class="callout__text">Doğum günü, yıl dönümü ya da bir teşekkür için sevdiklerinize
        Kurtaran Ev e-kartı gönderin.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="e-kartlar.html">E-kartlar ve sertifikalar <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


KORUYUCU_MELEK = """
<section class="page-hero page-hero--navy">
  <div class="container page-hero__inner">
    <div>
      __CRUMB__
      <p class="eyebrow">Destek Ol · Koruyucu Melek</p>
      <h1 class="display">Koruyucu Meleği olun.</h1>
      <p class="page-hero__lead">Aylık ₺3.000’den başlayan düzenli desteğiniz; mama, tedavi, ilaç ve
        yaşam alanlarının devamlılığına katkı sağlar.</p>

      <div class="amounts" data-amounts data-amount-target="#melek-sayfa-cta">
        <p class="amounts__label">Aylık destek tutarınızı seçin</p>
        <div class="amounts__options">
          <button class="amount is-active" type="button" data-amount="3000" aria-pressed="true">₺3.000</button>
          <button class="amount" type="button" data-amount="5000" aria-pressed="false">₺5.000</button>
          <button class="amount" type="button" data-amount="7500" aria-pressed="false">₺7.500</button>
          <button class="amount" type="button" data-amount="custom" aria-pressed="false">Diğer</button>
          <input class="amount-custom" type="number" min="100" step="100" hidden
                 aria-label="Diğer tutar (₺)" placeholder="₺ tutar">
        </div>
      </div>

      <div>
        <a class="btn btn--yellow" href="#melek-form">
          <span id="melek-sayfa-cta">₺3.000 ile başla</span> <span aria-hidden="true">→</span>
        </a>
      </div>
      <p class="amounts__note">Desteğinizi dilediğiniz zaman değiştirebilir veya sonlandırabilirsiniz.</p>
    </div>

    <figure class="page-hero__figure" style="border-color:var(--white); box-shadow:6px 6px 0 var(--yellow);">
      <img src="assets/img/kopek-portre.jpg" alt="Elini uzatmış, kameraya bakan köpek.">
    </figure>
  </div>
</section>

<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">Neden düzenli destek?</p>
    <h2 class="display" style="margin-bottom:2.4rem;">Süreklilik, kurtarmanın en zor kısmı</h2>
    <div class="tiles">
      <article class="tile tile--warm">
        <span class="tile__kicker">Planlanabilirlik</span>
        <h3 class="tile__title">Her ay ne kadar mama alacağımızı biliriz</h3>
        <p class="tile__text">Düzenli gelir, tedarikte pazarlık gücü ve stok planlaması demek.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Kesintisiz tedavi</span>
        <h3 class="tile__title">Uzun süreli tedaviler yarım kalmaz</h3>
        <p class="tile__text">Kronik hastalıklarda aylara yayılan ilaç ve kontrol maliyeti karşılanır.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Kapasite</span>
        <h3 class="tile__title">Yeni kurtarmalara alan açılır</h3>
        <p class="tile__text">Mevcut bakım güvence altındayken sahadan yeni can alabiliriz.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight" id="melek-form">
  <div class="container">
    <p class="eyebrow">Başlayalım</p>
    <h2 class="display" style="margin-bottom:2.2rem;">Koruyucu Melek kaydı</h2>
    <form class="form-grid" data-demo-form
          data-demo-message="Kaydınız alınmadı — bu yerel prototipte ödeme altyapısı bağlı değil.">
      <div class="field"><label for="km-ad">Ad soyad</label><input id="km-ad" name="ad" required></div>
      <div class="field"><label for="km-eposta">E-posta</label><input id="km-eposta" type="email" name="eposta" required></div>
      <div class="field"><label for="km-telefon">Telefon</label><input id="km-telefon" type="tel" name="telefon"></div>
      <div class="field">
        <label for="km-tutar">Aylık tutar (₺)</label>
        <input id="km-tutar" type="number" name="tutar" value="3000" min="100" step="100">
      </div>
      <div class="field field--full">
        <label for="km-not">Eklemek istediğiniz bir not</label>
        <textarea id="km-not" name="not" placeholder="Desteğinizin belirli bir alana yönlenmesini ister misiniz?"></textarea>
      </div>
      <div class="field field--full">
        <button class="btn btn--yellow" type="submit">Kaydı tamamla <span aria-hidden="true">→</span></button>
        <p class="form-status" role="status"></p>
        <p class="form-note">Ödeme altyapısı canlıya çıkışta bağlanacaktır.</p>
      </div>
    </form>
  </div>
</section>
""".replace("__CRUMB__", crumb(("Ana sayfa", "index.html"), ("Destek Ol", None), ("Koruyucu Melek", None)))


E_KARTLAR = page_hero(
    "Destek Ol · E-kartlar ve Sertifikalar",
    "Hediyeniz bir<br class=\"lb\"> cana dokunsun.",
    "Doğum günü, yıl dönümü, teşekkür ya da anma… Bağışınızı kişiye özel bir e-kart ya da "
    "dijital sertifikaya dönüştürüyoruz.",
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Destek Ol", None), ("E-kartlar ve Sertifikalar", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="tiles">
      <article class="tile tile--yellow">
        <span class="tile__kicker">E-kart</span>
        <h3 class="tile__title">Kutlama kartı</h3>
        <p class="tile__text">Seçtiğiniz görsel ve mesajınızla, belirlediğiniz tarihte
          alıcının e-posta kutusuna düşer.</p>
        <p class="tile__meta">₺500’den başlayan bağışlarla</p>
      </article>
      <article class="tile tile--sky">
        <span class="tile__kicker">Sertifika</span>
        <h3 class="tile__title">Koruyucu Melek sertifikası</h3>
        <p class="tile__text">Bir canın aylık bakımını sevdiğiniz birinin adına üstlenin;
          sertifikayı adına düzenleyelim.</p>
        <p class="tile__meta">₺3.000’den başlayan düzenli destekle</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Anma</span>
        <h3 class="tile__title">Anısına bağış</h3>
        <p class="tile__text">Kaybettiğiniz bir dostun anısına yapılan bağışlar için özel
          tasarlanmış kart.</p>
        <p class="tile__meta">Tutarı siz belirlersiniz</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <p class="eyebrow">Nasıl gönderilir?</p>
    <h2 class="display" style="margin-bottom:2rem;">Üç adım</h2>
    <div class="steps">
      <div class="step"><span class="step__num">01</span><div>
        <h3 class="step__title">Bağışınızı yapın</h3>
        <p class="step__text">Tutarı ve bağış yöntemini seçin.</p></div></div>
      <div class="step"><span class="step__num">02</span><div>
        <h3 class="step__title">Kart bilgilerini iletin</h3>
        <p class="step__text">Alıcının adı, e-posta adresi, mesajınız ve gönderim tarihi.</p></div></div>
      <div class="step"><span class="step__num">03</span><div>
        <h3 class="step__title">Biz gönderelim</h3>
        <p class="step__text">Kartınız belirlediğiniz tarihte, sizin adınıza iletilir.</p></div></div>
    </div>

    <div class="callout" style="margin-top:3rem;">
      <h2 class="callout__title">E-kart talebi</h2>
      <p class="callout__text">Şimdilik e-kart taleplerini e-posta ile alıyoruz.
        Alıcı bilgisi ve mesajınızı bize yazmanız yeterli.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="mailto:iletisim@kurtaranev.org?subject=E-kart%20talebi">
          E-posta gönder <span aria-hidden="true">↗</span></a>
        <a class="link-arrow" href="bagis-yap.html">Önce bağış yap <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


KURTARAN_SHOP = page_hero(
    "Destek Ol · Kurtaran Shop",
    "Aldığınız her ürün<br class=\"lb\"> bir cana gidiyor.",
    "Kurtaran Shop’tan yaptığınız alışverişin geliri doğrudan mama, tedavi ve yaşam alanı "
    "giderlerine aktarılıyor.",
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Destek Ol", None), ("Kurtaran Shop", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">Vitrin</p>
    <h2 class="display" style="margin-bottom:2.6rem;">Öne çıkanlar</h2>
    <div class="tiles tiles--4">
      <article class="tile tile--white">
        <span class="tile__kicker">Tekstil</span>
        <h3 class="tile__title">“Her can güvende” tişört</h3>
        <p class="tile__text">Organik pamuk, unisex kalıp.</p>
        <p class="tile__meta">₺750</p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">Aksesuar</span>
        <h3 class="tile__title">Bez çanta</h3>
        <p class="tile__text">Kurtaran Ev illüstrasyonlu, geniş hacim.</p>
        <p class="tile__meta">₺350</p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">Ev</span>
        <h3 class="tile__title">Kupa</h3>
        <p class="tile__text">Sabah kahveniz bir iyilik hikayesiyle.</p>
        <p class="tile__meta">₺400</p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">Kırtasiye</span>
        <h3 class="tile__title">Sticker seti</h3>
        <p class="tile__text">Yaşam alanlarımızın maskotları.</p>
        <p class="tile__meta">₺150</p>
      </article>
    </div>
    <p class="form-note">Ürün ve fiyatlar örnek içeriktir; mağaza altyapısı canlıya çıkışta bağlanacaktır.</p>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="callout callout--sky">
      <h2 class="callout__title">Kurumsal siparişler</h2>
      <p class="callout__text">Şirketinizin yılbaşı hediyesi ya da etkinlik seti için toplu sipariş
        verebilirsiniz. Gelirin tamamı sahadaki çalışmalara aktarılır.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="kurumsal-is-birligi.html">Kurumsal iş birliği <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="mailto:iletisim@kurtaranev.org?subject=Kurtaran%20Shop%20toplu%20sipariş">
          Teklif iste <span aria-hidden="true">↗</span></a>
      </div>
    </div>
  </div>
</section>
"""


GUNCEL_IHTIYACLAR = page_hero(
    "Destek Ol · Güncel İhtiyaçlar",
    "Bu hafta en çok<br class=\"lb\"> neye ihtiyacımız var?",
    "Sahadan gelen listeyi düzenli olarak güncelliyoruz. Ayni bağışlarınızı yaşam alanlarımıza "
    "ulaştırabilir ya da kargo ile gönderebilirsiniz.",
    variant=" page-hero--sky",
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Destek Ol", None), ("Güncel İhtiyaçlar", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <article class="tile tile--warm">
        <span class="tile__kicker">Acil</span>
        <h3 class="tile__title">Köpek yaşam alanı</h3>
        <ul class="bullets">
          <li>Yetişkin kuru köpek maması</li>
          <li>İç ve dış parazit damlası</li>
          <li>Battaniye ve yatak</li>
          <li>Dezenfektan ve çamaşır suyu</li>
        </ul>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Acil</span>
        <h3 class="tile__title">Kedi yaşam alanı</h3>
        <ul class="bullets">
          <li>Topaklanan kedi kumu</li>
          <li>Yavru kedi maması ve süt tozu</li>
          <li>Yaş mama (tedavi süreçleri için)</li>
          <li>Kağıt havlu</li>
        </ul>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Sürekli</span>
        <h3 class="tile__title">Tıbbi malzeme</h3>
        <ul class="bullets">
          <li>Serum ve enjektör</li>
          <li>Sargı bezi, steril gazlı bez</li>
          <li>Elizabeth yakalığı</li>
        </ul>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Sürekli</span>
        <h3 class="tile__title">Lojistik</h3>
        <ul class="bullets">
          <li>Taşıma kafesi</li>
          <li>Tasma ve göğüs tasması</li>
          <li>Araçla nakil desteği</li>
        </ul>
      </article>
    </div>

    <div class="callout" style="margin-top:3rem;">
      <h2 class="callout__title">Nereye gönderebilirim?</h2>
      <p class="callout__text">Amazon ihtiyaç listemizden seçtiğiniz ürünler doğrudan yaşam
        alanlarımıza gönderilir. Ayni bağışlarınızı ziyaret saatleri içinde kendiniz de
        bırakabilirsiniz; kargo göndereceksiniz bize önceden yazın, adres paylaşalım.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="https://www.amazon.com.tr/kurtaranev" target="_blank" rel="noopener">Amazon ihtiyaç listesi <span aria-hidden="true">↗</span></a>
        <a class="link-arrow" href="yasam-alanlari.html">Yaşam alanları ve saatler <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="iletisim.html">İletişime geç <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


# ===========================================================================
# KATIL
# ===========================================================================
GONULLU_OL = page_hero(
    "Katıl · Gönüllü Ol",
    "İhtiyaç duyulan<br class=\"lb\"> yerde, sizin<br class=\"lb\"> becerinizle.",
    "Sahada yürüyüş yaptırmaktan sosyal medya içeriği üretmeye, veterinere ulaşım desteğinden "
    "etkinlik organizasyonuna kadar pek çok alanda gönüllüye ihtiyacımız var.",
    actions='<a class="btn" href="#gonullu-form">Gönüllü başvurusu <span aria-hidden="true">→</span></a>',
    figure='<img src="assets/img/hero-kucak.jpg" alt="Bir gönüllü köpekle vakit geçiriyor.">',
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Katıl", None), ("Gönüllü Ol", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">Gönüllülük alanları</p>
    <h2 class="display" style="margin-bottom:2.6rem;">Nasıl katkı verebilirsiniz?</h2>
    <div class="tiles">
      <article class="tile tile--warm">
        <span class="tile__kicker">Sahada</span>
        <h3 class="tile__title">Bakım ve sosyalleşme</h3>
        <p class="tile__text">Yürüyüş, tımar, oyun ve temizlik desteği. Haftada birkaç saat bile
          büyük fark yaratıyor.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Ulaşım</span>
        <h3 class="tile__title">Nakil desteği</h3>
        <p class="tile__text">Veteriner randevuları ve sahiplendirme teslimleri için aracıyla
          destek verebilecek gönüllüler.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Dijital</span>
        <h3 class="tile__title">İçerik ve iletişim</h3>
        <p class="tile__text">Fotoğraf, video, metin yazarlığı, sosyal medya yönetimi ve
          çeviri desteği.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Uzmanlık</span>
        <h3 class="tile__title">Veteriner ve davranış</h3>
        <p class="tile__text">Veteriner hekimler, veteriner teknisyenleri ve davranış
          uzmanları için gönüllü program.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Etkinlik</span>
        <h3 class="tile__title">Stant ve organizasyon</h3>
        <p class="tile__text">Sahiplendirme günleri, bağış etkinlikleri ve okul ziyaretlerinde
          ekibe katılın.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Ofis</span>
        <h3 class="tile__title">Kayıt ve takip</h3>
        <p class="tile__text">Sahiplendirme kayıtları, bağış takibi ve raporlama gibi
          arka plan işleri.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight" id="gonullu-form">
  <div class="container">
    <p class="eyebrow">Başvuru</p>
    <h2 class="display" style="margin-bottom:2.2rem;">Bize kendinizden bahsedin</h2>
    <form class="form-grid" data-demo-form
          data-demo-message="Başvurunuz kaydedilmedi — bu yerel prototipte form gönderimi bağlı değil.">
      <div class="field"><label for="go-ad">Ad soyad</label><input id="go-ad" name="ad" required></div>
      <div class="field"><label for="go-eposta">E-posta</label><input id="go-eposta" type="email" name="eposta" required></div>
      <div class="field">
        <label for="go-alan">İlgilendiğiniz alan</label>
        <select id="go-alan" name="alan">
          <option>Sahada bakım ve sosyalleşme</option>
          <option>Nakil desteği</option>
          <option>İçerik ve iletişim</option>
          <option>Veteriner / davranış</option>
          <option>Etkinlik</option>
          <option>Ofis ve kayıt</option>
        </select>
      </div>
      <div class="field">
        <label for="go-sure">Haftada ayırabileceğiniz süre</label>
        <select id="go-sure" name="sure">
          <option>1–3 saat</option><option>4–8 saat</option><option>8 saatten fazla</option>
        </select>
      </div>
      <div class="field field--full">
        <label for="go-not">Deneyiminiz ve eklemek istedikleriniz</label>
        <textarea id="go-not" name="not"></textarea>
      </div>
      <div class="field field--full">
        <button class="btn" type="submit">Başvuruyu gönder <span aria-hidden="true">→</span></button>
        <p class="form-status" role="status"></p>
      </div>
    </form>
  </div>
</section>
"""


KURUMSAL = page_hero(
    "Katıl · Kurumsal İş Birliği",
    "Şirketinizin gücü,<br class=\"lb\"> sahada karşılık<br class=\"lb\"> buluyor.",
    "Mobil klinik projemiz gibi kalıcı etki yaratan çalışmalar, kurumsal iş birlikleriyle "
    "hayata geçiyor. Birlikte ne yapabileceğimizi konuşalım.",
    actions='<a class="btn" href="mailto:iletisim@kurtaranev.org?subject=Kurumsal%20iş%20birliği">'
            'İş birliği için yazın <span aria-hidden="true">↗</span></a>',
    figure='<img src="assets/img/hikaye-mobil-klinik.png" alt="Kurtaran Araç mobil klinik projesi tanıtımı.">',
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Katıl", None), ("Kurumsal İş Birliği", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">İş birliği modelleri</p>
    <h2 class="display" style="margin-bottom:2.6rem;">Dört başlık</h2>
    <div class="tiles tiles--2">
      <article class="tile tile--sky">
        <span class="tile__kicker">01</span>
        <h3 class="tile__title">Proje sponsorluğu</h3>
        <p class="tile__text">Mobil klinik, kısırlaştırma kampanyası ya da yaşam alanı yenileme
          gibi tanımlı bir projenin sponsoru olun. Süreci ve sonucu raporlayalım.</p>
      </article>
      <article class="tile tile--sky">
        <span class="tile__kicker">02</span>
        <h3 class="tile__title">Kurumsal Koruyucu Melek</h3>
        <p class="tile__text">Şirket adına aylık düzenli destek; belirli sayıda canın bakımını
          adınıza üstlenin.</p>
      </article>
      <article class="tile tile--sky">
        <span class="tile__kicker">03</span>
        <h3 class="tile__title">Çalışan gönüllülüğü</h3>
        <p class="tile__text">Ekipler için saha günleri düzenliyoruz: bakım, temizlik, oyun ve
          yürüyüş. Takım ruhu için de iyi geliyor.</p>
      </article>
      <article class="tile tile--sky">
        <span class="tile__kicker">04</span>
        <h3 class="tile__title">Ayni ve lojistik destek</h3>
        <p class="tile__text">Mama, ilaç, inşaat malzemesi, nakliye ve depolama desteği de en az
          nakit kadar değerli.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <div>
        <p class="eyebrow">Örnek</p>
        <h2 class="display" style="font-size:2.4rem; margin-bottom:1.2rem;">Kurtaran Araç</h2>
        <p class="body-lg" style="margin-bottom:1rem;">Anadolu Sigorta’nın desteğiyle hayata geçirdiğimiz
          mobil klinik; yerinde tedavi, kısırlaştırma ve kontrol sağlamak amacıyla gönüllü veteriner
          hekimleri sahaya taşıyor.</p>
        <p class="body-lg">Özellikle afet bölgelerinde, orta seviyede donanıma sahip bir mobil klinik
          büyük fayda sağlıyor.</p>
        <p style="margin-top:1.6rem;"><a class="link-arrow" href="hikayeler.html">Projeyi oku <span aria-hidden="true">→</span></a></p>
      </div>
      <figure class="page-hero__figure" style="aspect-ratio:1336/1194;">
        <img src="assets/img/hikaye-mobil-klinik.png" alt="Kurtaran Araç mobil klinik sunum görseli.">
      </figure>
    </div>
  </div>
</section>
"""


# ===========================================================================
# HAKKIMIZDA
# ===========================================================================
HIKAYEMIZ = page_hero(
    "Hakkımızda · Hikayemiz ve Misyonumuz",
    "Her can, güvende<br class=\"lb\"> ve sevildiği bir<br class=\"lb\"> hayatı hak eder.",
    "Kurtaran Ev; sahipsiz kedi ve köpekleri kurtaran, tedavi eden, rehabilite eden ve "
    "kalıcı yuvalara ulaştıran bir dernektir.",
    figure='<img src="assets/img/hero-kucak.jpg" alt="Bir gönüllü ve kurtarılan bir köpek.">',
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Hakkımızda", None), ("Hikayemiz ve Misyonumuz", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="prose">
      <h2>Nasıl başladı?</h2>
      <p>Bir sokak köpeğine yapılan küçük bir müdahale, zamanla düzenli bir bakım ağına dönüştü.
        Önce birkaç can, sonra bir bahçe, sonra ayrı ayrı yaşam alanları… Bugün İstanbul’un dört
        farklı noktasında yaklaşık 1.200 köpek ve 600 kediyle ilgileniyoruz.</p>

      <h2>Ne yapıyoruz?</h2>
      <p>Çalışmalarımız dört başlıkta ilerliyor: <strong>kurtarma</strong>, <strong>tedavi</strong>,
        <strong>rehabilitasyon</strong> ve <strong>yaşam boyu bakım</strong>. Sahiplendirme bu zincirin
        yalnızca bir halkası; sahiplenilemeyen canların da ömürlerinin sonuna kadar güvende olmasını
        sağlamak asıl sorumluluğumuz.</p>

      <h2>Neye inanıyoruz?</h2>
      <ul>
        <li>Hiçbir can, yaşı ya da ırkı yüzünden geride bırakılmaz.</li>
        <li>Sahiplendirme bir teslimat değil, bir eşleştirmedir.</li>
        <li>Kısırlaştırma, kalıcı çözümün merkezindedir.</li>
        <li>Şeffaflık, bağışçıya borcumuzdur.</li>
      </ul>
    </div>

    <div class="callout callout--cream" style="margin-top:3rem;">
      <h2 class="callout__title">Misyonumuz</h2>
      <p class="callout__text">Sahipsiz hayvanların yaşamlarını güvence altına almak; onları
        iyileştirip doğru yuvalarla buluşturmak ve toplumda sorumlu sahiplenme kültürünü büyütmek.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="etkimiz.html">Etkimizi görün <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="yasam-alanlari.html">Yaşam alanlarımız <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


ETKIMIZ = page_hero(
    "Hakkımızda · Etkimiz ve Çalışmalarımız",
    "Rakamlar,<br class=\"lb\"> sahadaki karşılığı.",
    "Bakımını üstlendiğimiz can sayısı, yürüttüğümüz projeler ve önümüzdeki dönem hedeflerimiz.",
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Hakkımızda", None), ("Etkimiz ve Çalışmalarımız", None)),
) + """
<section class="stats" aria-label="Rakamlarla Kurtaran Ev">
  <div class="stats__grid">
    <div class="stats__cell"><span class="stats__num">1.200</span><span class="stats__label">köpek</span></div>
    <div class="stats__cell"><span class="stats__num">600</span><span class="stats__label">kedi</span></div>
    <div class="stats__cell"><span class="stats__num">4</span><span class="stats__label">yaşam alanı</span></div>
    <div class="stats__cell">
      <p class="stats__note">Kurtarma, tedavi, rehabilitasyon ve yaşam boyu bakım—her biri
        sizin desteğinizle mümkün.</p>
    </div>
  </div>
</section>

<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">Çalışma alanlarımız</p>
    <h2 class="display" style="margin-bottom:2.6rem;">Neyi, nasıl yapıyoruz?</h2>
    <div class="tiles">
      <article class="tile tile--warm">
        <span class="tile__kicker">01</span>
        <h3 class="tile__title">Kurtarma ve acil müdahale</h3>
        <p class="tile__text">İhbar üzerine sahaya çıkıyor, yaralı ve risk altındaki canları
          güvenli alana alıyoruz.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">02</span>
        <h3 class="tile__title">Tedavi ve kısırlaştırma</h3>
        <p class="tile__text">Anlaşmalı klinikler ve gönüllü veteriner hekimlerle tedavi,
          aşı ve kısırlaştırma süreçlerini yürütüyoruz.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">03</span>
        <h3 class="tile__title">Rehabilitasyon</h3>
        <p class="tile__text">Travma yaşamış canlar için sosyalleşme ve davranış çalışmaları
          yapıyoruz.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">04</span>
        <h3 class="tile__title">Sahiplendirme</h3>
        <p class="tile__text">Ön görüşme, tanışma, sözleşme ve sahiplendirme sonrası takip
          ile kalıcı yuvalar kuruyoruz.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">05</span>
        <h3 class="tile__title">Yaşam boyu bakım</h3>
        <p class="tile__text">Sahiplendirilemeyen canlar için ömür boyu barınma, beslenme ve
          tıbbi bakım.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">06</span>
        <h3 class="tile__title">Mobil klinik</h3>
        <p class="tile__text">Kurtaran Araç ile tedaviyi ihtiyacın olduğu yere taşıyoruz.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <div>
        <p class="eyebrow">Önümüzdeki dönem</p>
        <h2 class="display" style="font-size:2.4rem; margin-bottom:1.4rem;">Hedeflerimiz</h2>
        <ul class="bullets bullets--lg">
          <li>Kedi yaşam alanında kapasite ve karantina bölümünün genişletilmesi</li>
          <li>Mobil klinikle mahalle bazlı kısırlaştırma programı</li>
          <li>Geçici yuva ağının iki katına çıkarılması</li>
          <li>Sahiplendirme sonrası takip sisteminin dijitalleştirilmesi</li>
        </ul>
      </div>
      <div class="callout">
        <h2 class="callout__title">Bu hedefler destekle mümkün</h2>
        <p class="callout__text">Düzenli bağış, yaptığımız işi planlanabilir kılıyor.
          Aylık desteğinizle kapasitemizi büyütebiliriz.</p>
        <div class="callout__actions">
          <a class="btn btn--white" href="koruyucu-melek.html">Koruyucu Melek ol <span aria-hidden="true">→</span></a>
        </div>
      </div>
    </div>
  </div>
</section>
"""


YASAM_ALANLARI = page_hero(
    "Hakkımızda · Yaşam Alanlarımızı Ziyaret",
    "Dört alan. Tek söz:<br class=\"lb\"> hiçbirini geride<br class=\"lb\"> bırakmamak.",
    "Tedavi, rehabilitasyon, sahiplendirme ve yaşam boyu bakım çalışmalarımız İstanbul’daki "
    "dört farklı alanda devam ediyor. Ziyaret etmek için beklemiyoruz — geliyorsanız haber verin yeter.",
    variant=" page-hero--sky",
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Hakkımızda", None), ("Yaşam Alanlarımızı Ziyaret", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <article class="tile tile--warm">
        <span class="tile__kicker">01</span>
        <h3 class="tile__title">Hadımköy Yaşam Alanı</h3>
        <p class="tile__text">Köpeklerin bakım ve rehabilitasyonu. Yürüyüş, oyun ve
          sosyalleşme çalışmalarının merkezi.</p>
        <dl class="info-list" style="margin-top:.6rem;">
          <div class="info-row"><dt>Ziyaret saatleri</dt><dd>11.00–17.00</dd></div>
          <div class="info-row"><dt>Randevu</dt><dd>Gerekli değil, haber vermeniz yeterli</dd></div>
          <div class="info-row"><dt>Konum</dt>
            <dd><a href="https://maps.app.goo.gl/R77zL5Gg42f7ZfXY6" target="_blank" rel="noopener">Haritada gör ↗</a></dd></div>
        </dl>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">02</span>
        <h3 class="tile__title">Kedi Yaşam Alanı</h3>
        <p class="tile__text">Kedilerin güvenli yaşam ve bakım alanı. Tırmanma rafları,
          ayrı karantina bölümü ve dinlenme odaları.</p>
        <dl class="info-list" style="margin-top:.6rem;">
          <div class="info-row"><dt>Ziyaret</dt><dd>Randevu ile</dd></div>
          <div class="info-row"><dt>Not</dt><dd>Karantina bölümü ziyarete kapalıdır</dd></div>
        </dl>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">03</span>
        <h3 class="tile__title">Beşiktaş Kedi Sahiplendirme Alanı</h3>
        <p class="tile__text">Tanışma ve sahiplendirme. Yuva arayan kedilerle sakin bir
          ortamda vakit geçirebilirsiniz.</p>
        <dl class="info-list" style="margin-top:.6rem;">
          <div class="info-row"><dt>Ziyaret saatleri</dt><dd>10.00–16.00</dd></div>
          <div class="info-row"><dt>Randevu</dt><dd>Hafta sonu için önerilir</dd></div>
          <div class="info-row"><dt>Konum</dt>
            <dd><a href="https://maps.app.goo.gl/PutVz4WqqHoSv1bNA" target="_blank" rel="noopener">Haritada gör ↗</a></dd></div>
        </dl>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">04</span>
        <h3 class="tile__title">Dumankaya Kedi Tedavi Alanı</h3>
        <p class="tile__text">Tedavi ve iyileşme. Operasyon sonrası bakım ve kronik
          hastalıkların takibi burada yapılıyor.</p>
        <dl class="info-list" style="margin-top:.6rem;">
          <div class="info-row"><dt>Ziyaret</dt><dd>Yalnızca randevu ile</dd></div>
          <div class="info-row"><dt>Not</dt><dd>Tedavi süreci nedeniyle sınırlı ziyaret</dd></div>
        </dl>
      </article>
    </div>

    <div class="callout" style="margin-top:3rem;">
      <h2 class="callout__title">Ziyaret etmeden önce</h2>
      <p class="callout__text">Açık adres ve ulaşım bilgisini randevu sırasında paylaşıyoruz.
        Yanınızda mama ya da kum getirecekseniz önceden söyleyin, güncel ihtiyaca göre yönlendirelim.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="iletisim.html">Randevu al <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="guncel-ihtiyaclar.html">Güncel ihtiyaçlar <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


HIKAYELER = page_hero(
    "Blog Merkezi · Haberler ve Hikayeler",
    "Umudu görünür<br class=\"lb\"> kılanlar.",
    "Mutluluk hikayeleri, saha notları ve projelerimizden haberler.",
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Hakkımızda", None), ("Haberler ve Hikayeler", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="stories">
      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-lucy.jpg" alt="Sarı koltukta Lucy’yi kucaklayan bir kadın.">
        </figure>
        <span class="story__tag">Mutluluk hikayesi</span>
        <h2 class="story__title">Lucy’nin yeni hayatı</h2>
        <p class="story__excerpt">Kanser tedavisi devam ederken bir aile ona yalnızca evini değil,
          bütün kalbini açtı. Lucy artık tedavisini kendi evinde sürdürüyor.</p>
        <a class="link-arrow link-arrow--sm" href="#">Hikayeyi oku <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-mobil-klinik.png" alt="Kurtaran Araç mobil klinik tanıtımı.">
        </figure>
        <span class="story__tag">Proje · Kurumsal iş birliği</span>
        <h2 class="story__title">Mobil Klinik: Kurtaran Araç</h2>
        <p class="story__excerpt">Anadolu Sigorta’nın desteğiyle tedavi, kısırlaştırma ve kontrolleri
          ihtiyaç olan yere taşıyoruz. Özellikle afet bölgelerinde büyük fark yaratıyor.</p>
        <a class="link-arrow link-arrow--sm" href="#">Hikayeyi oku <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-kevok.jpg" alt="Sahilde Kevok’u kucaklayan bir adam.">
        </figure>
        <span class="story__tag">Mutluluk hikayesi</span>
        <h2 class="story__title">Kevok sonunda görüldü</h2>
        <p class="story__excerpt">Irkı ve yaşı yüzünden yıllarca gözden kaçan Kevok, onu gerçekten
          gören insanla tanıştı. Artık her sabah sahilde yürüyor.</p>
        <a class="link-arrow link-arrow--sm" href="#">Hikayeyi oku <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/bahce-kopekler.jpg" alt="Yaşam alanının bahçesindeki köpekler.">
        </figure>
        <span class="story__tag">Sahadan</span>
        <h2 class="story__title">Kış hazırlığı tamamlandı</h2>
        <p class="story__excerpt">Hadımköy’deki kulübelerin yalıtımı yenilendi, bahçe zemini
          düzenlendi. Gönüllülerimize teşekkürler.</p>
        <a class="link-arrow link-arrow--sm" href="#">Hikayeyi oku <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/kedi-yasam-alani.jpg" alt="Kedi yaşam alanının koridoru.">
        </figure>
        <span class="story__tag">Sahadan</span>
        <h2 class="story__title">Kedi yaşam alanında yeni bölüm</h2>
        <p class="story__excerpt">Yavru kediler için ayrı bir sosyalleşme odası açtık.
          İlk misafirler çoktan yerleşti.</p>
        <a class="link-arrow link-arrow--sm" href="#">Hikayeyi oku <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/kopek-portre.jpg" alt="Kameraya bakan sarı köpek.">
        </figure>
        <span class="story__tag">Rehber</span>
        <h2 class="story__title">İlk hafta rehberi</h2>
        <p class="story__excerpt">Sahiplendiğiniz canla geçireceğiniz ilk yedi gün için pratik
          öneriler: beslenme, tuvalet alışkanlığı ve güven kurma.</p>
        <a class="link-arrow link-arrow--sm" href="#">Hikayeyi oku <span aria-hidden="true">↗</span></a>
      </article>
    </div>
    <p class="form-note">Yazı detay sayfaları içerik girildikçe eklenecektir.</p>
  </div>
</section>
"""


ILETISIM = page_hero(
    "Hakkımızda · İletişim",
    "Bize ulaşın.",
    "Sahiplenme, geçici yuva, bağış ya da gönüllülük — hangi konuda olursa olsun yazın, "
    "en kısa sürede dönüş yapalım.",
    breadcrumb=crumb(("Ana sayfa", "index.html"), ("Hakkımızda", None), ("İletişim", None)),
) + """
<section class="section section--cream section--tight" id="kanallar">
  <div class="container">
    <div class="tiles tiles--2">
      <div>
        <p class="eyebrow">Doğrudan iletişim</p>
        <h2 class="display" style="font-size:2.4rem; margin-bottom:1.6rem;">Kanallar</h2>
        <dl class="info-list">
          <div class="info-row"><dt>E-posta</dt>
            <dd><a href="mailto:iletisim@kurtaranev.org">iletisim@kurtaranev.org</a></dd></div>
          <div class="info-row"><dt>Instagram</dt>
            <dd><a href="__IG_ANA__" target="_blank" rel="noopener">@kurtaranev</a></dd></div>
          <div class="info-row"><dt>Yuva arayan köpekler</dt>
            <dd><a href="__IG_KOPEK__" target="_blank" rel="noopener">@kurtaranev_kopekleri</a></dd></div>
          <div class="info-row"><dt>Yuva arayan kediler</dt>
            <dd><a href="__IG_KEDI__" target="_blank" rel="noopener">@kurtaranev_kedileri</a></dd></div>
          <div class="info-row"><dt>Hadımköy ziyaret</dt>
            <dd>11.00–17.00 · <a href="https://maps.app.goo.gl/R77zL5Gg42f7ZfXY6" target="_blank" rel="noopener">Haritada gör ↗</a></dd></div>
          <div class="info-row"><dt>Beşiktaş ziyaret</dt>
            <dd>10.00–16.00 · <a href="https://maps.app.goo.gl/PutVz4WqqHoSv1bNA" target="_blank" rel="noopener">Haritada gör ↗</a></dd></div>
        </dl>
      </div>

      <div>
        <p class="eyebrow">Mesaj bırakın</p>
        <h2 class="display" style="font-size:2.4rem; margin-bottom:1.6rem;">Form</h2>
        <form class="form-grid" style="grid-template-columns:1fr;" data-demo-form
              data-demo-message="Mesajınız gönderilmedi — bu yerel prototipte form altyapısı bağlı değil.">
          <div class="field"><label for="il-ad">Ad soyad</label><input id="il-ad" name="ad" required></div>
          <div class="field"><label for="il-eposta">E-posta</label><input id="il-eposta" type="email" name="eposta" required></div>
          <div class="field">
            <label for="il-konu">Konu</label>
            <select id="il-konu" name="konu">
              <option value="sahiplenme">Sahiplenme</option>
              <option value="gecici-yuva">Geçici yuva</option>
              <option value="koruyucu-melek">Koruyucu melek</option>
              <option value="bagis">Bağış</option>
              <option value="gonulluluk">Gönüllülük</option>
              <option value="kurumsal">Kurumsal iş birliği</option>
              <option value="diger">Diğer</option>
            </select>
          </div>
          <div class="field"><label for="il-mesaj">Mesajınız</label><textarea id="il-mesaj" name="mesaj" required></textarea></div>
          <div class="field">
            <button class="btn" type="submit">Gönder <span aria-hidden="true">→</span></button>
            <p class="form-status" role="status"></p>
          </div>
        </form>
      </div>
    </div>
  </div>
</section>
""".replace("__IG_ANA__", IG_ANA).replace("__IG_KOPEK__", IG_KOPEK).replace("__IG_KEDI__", IG_KEDI)


# ===========================================================================
# İLAN KATALOĞU
# ===========================================================================
def katalog(tur: str) -> str:
    kedi = tur == "kedi"
    baslik = "Yuva arayan kediler" if kedi else "Yuva arayan köpekler"
    eyebrow = "Yuva Ol · Kediler" if kedi else "Yuva Ol · Köpekler"
    lead = (
        "Sahiplendirilmeyi bekleyen kedilerimizin tamamı burada. Yaşa, cinsiyete ve "
        "uyum durumuna göre süzebilir, ilgilendiğiniz canın ilanını açabilirsiniz."
        if kedi else
        "Sahiplendirilmeyi bekleyen köpeklerimizin tamamı burada. Yaşa, boyuta ve "
        "uyum durumuna göre süzebilir, ilgilendiğiniz canın ilanını açabilirsiniz."
    )
    ig = IG_KEDI if kedi else IG_KOPEK
    hesap = "@kurtaranev_kedileri" if kedi else "@kurtaranev_kopekleri"
    variant = " page-hero--sky" if kedi else ""

    # Boyut süzgeci köpeklerde anlamlı; kedilerde gizli
    boyut_filtresi = "" if kedi else """
        <div class="filter">
          <label for="f-boyut">Boyut</label>
          <select id="f-boyut" data-filter="boyut">
            <option value="">Hepsi</option>
            <option value="kucuk">Küçük</option>
            <option value="orta">Orta</option>
            <option value="buyuk">Büyük</option>
          </select>
        </div>"""

    return f"""
<section class="page-hero{variant}">
  <div class="container page-hero__inner page-hero__inner--single">
    <div>
      {crumb(("Ana sayfa", "index.html"), ("Yuva Ol", None), (baslik, None))}
      <p class="eyebrow">{eyebrow}</p>
      <h1 class="display">{baslik}</h1>
      <p class="page-hero__lead">{lead}</p>
      <div class="page-hero__actions">
        <a class="link-arrow" href="sahiplenme-sureci.html">Sahiplenme süreci <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="{ig}" target="_blank" rel="noopener">{hesap} <span aria-hidden="true">↗</span></a>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream section--tight">
  <div class="container" data-catalog="{tur}">

    <div class="notice" data-ornek-uyari hidden>
      <span class="notice__icon" aria-hidden="true">⚠</span>
      <span><b>Bu sayfada örnek kayıtlar var.</b>
        “ÖRNEK KAYIT” rozetli ilanlar gerçek değildir; arayüzü denemek için eklenmiştir.
        Yönetim panelinden tek tıkla temizlenebilirler.</span>
    </div>

    <form class="filters" role="search" aria-label="İlan filtreleri" onsubmit="return false">
      <div class="filter filters__search">
        <label for="f-q">Ara</label>
        <input id="f-q" type="search" data-filter="q" placeholder="İsim, cins, renk, karakter…">
      </div>

      <div class="filters__row">
        <div class="filter">
          <label for="f-durum">Durum</label>
          <select id="f-durum" data-filter="durum">
            <option value="musait">Müsait olanlar</option>
            <option value="yuva-ariyor">Yuva arıyor</option>
            <option value="rezerve">Rezerve</option>
            <option value="yuvalandi">Yuvalandı</option>
            <option value="">Hepsi</option>
          </select>
        </div>
        <div class="filter">
          <label for="f-cinsiyet">Cinsiyet</label>
          <select id="f-cinsiyet" data-filter="cinsiyet">
            <option value="">Hepsi</option>
            <option value="disi">Dişi</option>
            <option value="erkek">Erkek</option>
          </select>
        </div>
        <div class="filter">
          <label for="f-yas">Yaş</label>
          <select id="f-yas" data-filter="yas">
            <option value="">Hepsi</option>
            <option value="yavru">Yavru (0–1 yaş)</option>
            <option value="yetiskin">Yetişkin (1–7 yaş)</option>
            <option value="kidemli">Kıdemli (7+ yaş)</option>
          </select>
        </div>{boyut_filtresi}
        <div class="filter">
          <label for="f-sirala">Sırala</label>
          <select id="f-sirala" data-filter="sirala">
            <option value="yeni">Önce yeni eklenen</option>
            <option value="isim">İsme göre</option>
            <option value="yas-artan">Yaş: küçükten büyüğe</option>
            <option value="yas-azalan">Yaş: büyükten küçüğe</option>
          </select>
        </div>
      </div>

      <div class="filters__toggles">
        <label class="chip"><input type="checkbox" data-filter="kisir"> Kısırlaştırıldı</label>
        <label class="chip"><input type="checkbox" data-filter="asili"> Aşıları tam</label>
        <label class="chip"><input type="checkbox" data-filter="cocuk"> Çocuklarla uyumlu</label>
        <label class="chip"><input type="checkbox" data-filter="kopek"> Köpeklerle uyumlu</label>
        <label class="chip"><input type="checkbox" data-filter="kedi"> Kedilerle uyumlu</label>
        <button class="filters__clear" type="button" data-clear hidden>Filtreleri temizle</button>
      </div>
    </form>

    <div class="results-bar">
      <p class="results-bar__count" data-count role="status"></p>
      <p class="body-sm">Bilgisi olmayan alanlar “bilinmiyor” olarak gösterilir.</p>
    </div>

    <div class="animal-grid" data-grid></div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="callout">
      <h2 class="callout__title">Aradığınızı bulamadınız mı?</h2>
      <p class="callout__text">Yeni ilanlar sürekli ekleniyor. Ne aradığınızı bize yazın,
        uygun bir can geldiğinde haber verelim.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="iletisim.html">Bize yazın <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="gecici-yuva.html">Geçici yuva ol <span aria-hidden="true">→</span></a>
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
        <a href="index.html">Ana sayfa</a><span aria-hidden="true">/</span>
        <a href="yuva-arayan-kopekler.html" data-back-link>Yuva arayanlar</a>
      </p>

      <nav class="pager" aria-label="İlanlar arası geçiş" data-pager hidden>
        <a class="pager__link" href="#" data-pager-prev>
          <span class="pager__arrow" aria-hidden="true">←</span>
          <span class="pager__text"><span class="pager__label">Önceki</span><span class="pager__name"></span></span>
        </a>
        <span class="pager__count" data-pager-count></span>
        <a class="pager__link pager__link--next" href="#" data-pager-next>
          <span class="pager__text"><span class="pager__label">Sonraki</span><span class="pager__name"></span></span>
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
      <h2 class="callout__title" data-meet-title>Tanışmak ister misiniz?</h2>
      <p class="callout__text">Önce
        <a class="meet-cta__process" href="sahiplenme-sureci.html">sahiplenme sürecini</a>
        okuyun, sonra bize yazın. Ekibimiz sizinle iletişime geçip ön görüşmeyi planlasın.</p>

      <div class="meet-cta__options">
        <a class="btn btn--white btn--sm" href="sahiplen.html" data-meet-option="sahiplenme">Sahiplen <span aria-hidden="true">→</span></a>
        <a class="btn btn--white btn--sm" href="gecici-yuva.html" data-meet-option="gecici-yuva">Geçici yuva ol <span aria-hidden="true">→</span></a>
        <a class="btn btn--white btn--sm" href="koruyucu-melek.html" data-meet-option="koruyucu-melek">Koruyucu melek ol <span aria-hidden="true">→</span></a>
      </div>
    </div>

    <p class="animal-detail__source meet-band__source" data-meet-source hidden></p>

    <div class="meet-band__cta">
      <a class="btn" href="iletisim.html">Tanışmak istiyorum <span aria-hidden="true">→</span></a>
    </div>
  </div>
</section>

<section class="section section--warm section--tight" data-others hidden>
  <div class="container">
    <div class="others__head">
      <h2 class="others__title" data-others-title>Diğer yuva arayanlar</h2>
      <a class="link-arrow" href="yuva-arayan-kopekler.html" data-others-all>Tümünü gör <span aria-hidden="true">→</span></a>
    </div>
    <div class="animal-grid" data-others-grid></div>
  </div>
</section>
"""


ADMIN = """
<div id="admin"></div>
"""


# ===========================================================================
PAGES = {
    "index.html": {
        "title": "Kurtaran Ev | Her can için güvenli bir hayat",
        "description": "Kurtaran Ev Derneği; İstanbul’daki dört yaşam alanında yaklaşık 1.200 köpek ve "
                       "600 kediyi kurtarıyor, tedavi ediyor ve yuvalandırıyor.",
        "body": INDEX,
        "veri": True,
        "js": ["assets/js/counts.js"],
    },
    "sahiplen.html": {
        "title": "Sahiplen | Kurtaran Ev",
        "description": "Yuva arayan kedi ve köpeklerimizle tanışın; sahiplenme sürecini öğrenin.",
        "body": SAHIPLEN,
        "veri": True,
        "js": ["assets/js/counts.js"],
    },
    "gecici-yuva.html": {
        "title": "Geçici Yuva | Kurtaran Ev",
        "description": "Geçici yuva olun; bir kafes boşalsın, yeni bir can kurtarılsın.",
        "body": GECICI_YUVA,
    },
    "sahiplenmeden-once.html": {
        "title": "Sahiplenmeden Önce | Kurtaran Ev",
        "description": "Sahiplenmeden önce bilmeniz gerekenler: ön hazırlık, bütçe, ev güvenliği ve beklentiler.",
        "body": SAHIPLENMEDEN_ONCE,
    },
    "sahiplenme-sureci.html": {
        "title": "Sahiplenme Süreci | Kurtaran Ev",
        "description": "Sahiplenme süreci nasıl işliyor, hangi belgeler gerekiyor?",
        "body": SAHIPLENME_SURECI,
    },
    "bagis-yap.html": {
        "title": "Bağış Yap | Kurtaran Ev",
        "description": "Bağışınız doğrudan mamaya, tedaviye ve yaşam alanlarının giderlerine gidiyor.",
        "body": BAGIS_YAP,
    },
    "koruyucu-melek.html": {
        "title": "Koruyucu Melek | Kurtaran Ev",
        "description": "Aylık düzenli destekle bakımın devamlılığını sağlayın.",
        "body": KORUYUCU_MELEK,
    },
    "e-kartlar.html": {
        "title": "E-kartlar ve Sertifikalar | Kurtaran Ev",
        "description": "Bağışınızı kişiye özel bir e-karta ya da sertifikaya dönüştürün.",
        "body": E_KARTLAR,
    },
    "kurtaran-shop.html": {
        "title": "Kurtaran Shop | Kurtaran Ev",
        "description": "Kurtaran Shop’tan alışverişinizin geliri doğrudan sahaya aktarılıyor.",
        "body": KURTARAN_SHOP,
    },
    "guncel-ihtiyaclar.html": {
        "title": "Güncel İhtiyaçlar | Kurtaran Ev",
        "description": "Yaşam alanlarımızın bu haftaki öncelikli mama, kum ve tıbbi malzeme ihtiyaçları.",
        "body": GUNCEL_IHTIYACLAR,
    },
    "gonullu-ol.html": {
        "title": "Gönüllü Ol | Kurtaran Ev",
        "description": "Sahada, dijitalde ya da ofiste; becerinizle Kurtaran Ev’e katkı verin.",
        "body": GONULLU_OL,
    },
    "kurumsal-is-birligi.html": {
        "title": "Kurumsal İş Birliği | Kurtaran Ev",
        "description": "Proje sponsorluğu, kurumsal Koruyucu Melek ve çalışan gönüllülüğü modelleri.",
        "body": KURUMSAL,
    },
    "hikayemiz.html": {
        "title": "Hikayemiz ve Misyonumuz | Kurtaran Ev",
        "description": "Kurtaran Ev nasıl başladı, neye inanıyor, ne yapıyor?",
        "body": HIKAYEMIZ,
    },
    "etkimiz.html": {
        "title": "Etkimiz ve Çalışmalarımız | Kurtaran Ev",
        "description": "Rakamlarla Kurtaran Ev; çalışma alanlarımız ve önümüzdeki dönem hedeflerimiz.",
        "body": ETKIMIZ,
    },
    "yasam-alanlari.html": {
        "title": "Yaşam Alanlarımızı Ziyaret | Kurtaran Ev",
        "description": "Hadımköy, Kedi Yaşam Alanı, Beşiktaş ve Dumankaya: dört yaşam alanı, ziyaret bilgileri.",
        "body": YASAM_ALANLARI,
    },
    "hikayeler.html": {
        "title": "Haberler ve Hikayeler | Kurtaran Ev",
        "description": "Mutluluk hikayeleri, saha notları ve projelerimizden haberler.",
        "body": HIKAYELER,
    },
    "iletisim.html": {
        "title": "İletişim | Kurtaran Ev",
        "description": "Sahiplenme, bağış, gönüllülük ve iş birliği için Kurtaran Ev’e ulaşın.",
        "body": ILETISIM,
    },

    # --- ilan kataloğu -----------------------------------------------------
    "yuva-arayan-kopekler.html": {
        "title": "Yuva Arayan Köpekler | Kurtaran Ev",
        "description": "Sahiplendirilmeyi bekleyen köpeklerimizi yaşa, boyuta ve uyum durumuna "
                       "göre süzerek inceleyin.",
        "body": katalog("kopek"),
        "veri": True,
        "js": ["assets/js/catalog.js"],
    },
    "yuva-arayan-kediler.html": {
        "title": "Yuva Arayan Kediler | Kurtaran Ev",
        "description": "Sahiplendirilmeyi bekleyen kedilerimizi yaşa, cinsiyete ve uyum durumuna "
                       "göre süzerek inceleyin.",
        "body": katalog("kedi"),
        "veri": True,
        "js": ["assets/js/catalog.js"],
    },
    "ilan.html": {
        "title": "İlan | Kurtaran Ev",
        "description": "Yuva arayan bir canın ilan detayı.",
        "body": ILAN_DETAY,
        "veri": True,
        "js": ["assets/js/animal.js"],
    },
    "admin.html": {
        "title": "Yönetim Paneli | Kurtaran Ev",
        "description": "Kurtaran Ev ilan yönetimi.",
        "body": ADMIN,
        "css": ["assets/css/admin.css"],
        "js": ["assets/js/admin.js"],
        "yalin": True,
    },
}
