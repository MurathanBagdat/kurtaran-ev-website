# -*- coding: utf-8 -*-
"""English page bodies — part 1: home, adopt, foster, before you adopt, adoption process."""

from pages import page_hero, crumb, IG_KOPEK, IG_KEDI, IG_ANA


# ===========================================================================
# HOME
# ===========================================================================
INDEX = """
<section class="hero">
  <div class="container hero__inner">
    <div class="hero__text">
      <p class="eyebrow">Four shelters in Istanbul</p>
      <h1 class="display display--hero hero__title">Every life deserves<br class="lb">
        to be safe<br class="lb"> and <em>loved</em>.</h1>
      <p class="lead hero__lead">We rescue, treat, rehabilitate and match animals with the right
        homes. Across our 4 shelters we are here every day for more than 1,500 cats and dogs —
        and for all the ones still to come.</p>
      <div class="hero__actions">
        <a class="btn" href="hikayemiz.html">Our mission <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="#yuva-arayanlar">See who’s looking for a home <span aria-hidden="true">↘</span></a>
      </div>
    </div>

    <div class="hero__media">
      <span class="hero__blob" aria-hidden="true"></span>
      <div class="arch">
        <img src="assets/img/hero-kucak.jpg" width="1536" height="2048"
             alt="A volunteer in a yellow bandana hugging a black-and-white dog on the grass.">
      </div>
      <p class="sticker sticker--hero">A little care, a little trust, a whole new life.</p>
    </div>
  </div>
</section>

<section class="stats" aria-label="Kurtaran Ev in numbers">
  <div class="stats__grid">
    <div class="stats__cell">
      <span class="stats__num">1,200</span>
      <span class="stats__label">dogs</span>
    </div>
    <div class="stats__cell">
      <span class="stats__num">600</span>
      <span class="stats__label">cats</span>
    </div>
    <div class="stats__cell">
      <span class="stats__num">4</span>
      <span class="stats__label">shelters</span>
    </div>
    <div class="stats__cell">
      <p class="stats__note">Rescue, treatment, rehabilitation and lifelong care — every one of
        them possible thanks to your support.</p>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="section__intro">
      <p class="eyebrow">There’s more than one way to help</p>
      <h2 class="display">How can you stand with us?</h2>
      <p class="body-lg">With your time, by opening your home, or with regular support,
        you can change the course of a life.</p>
    </div>

    <div class="paths">
      <a class="path-card path-card--green" href="yuva-arayan-kopekler.html">
        <span class="path-card__num">01</span>
        <h3 class="path-card__title">Adopt</h3>
        <p class="path-card__text">Not just a new friend — meet a new member of your family.</p>
        <span class="path-card__arrow" aria-hidden="true">↗</span>
      </a>
      <a class="path-card path-card--sky" href="gecici-yuva.html">
        <span class="path-card__num">02</span>
        <h3 class="path-card__title">Foster</h3>
        <p class="path-card__text">A short-term space in your home saves a new life in the field.</p>
        <span class="path-card__arrow" aria-hidden="true">↗</span>
      </a>
      <a class="path-card path-card--orange" href="koruyucu-melek.html">
        <span class="path-card__num">03</span>
        <h3 class="path-card__title">Become a Guardian Angel</h3>
        <p class="path-card__text">Keep care going with regular monthly support.</p>
        <span class="path-card__arrow" aria-hidden="true">↗</span>
      </a>
      <a class="path-card path-card--cream" href="gonullu-ol.html">
        <span class="path-card__num">04</span>
        <h3 class="path-card__title">Volunteer</h3>
        <p class="path-card__text">Bring your skills and your time wherever they’re needed most.</p>
        <span class="path-card__arrow" aria-hidden="true">↗</span>
      </a>
    </div>
  </div>
</section>

<section class="section section--warm" id="yuva-arayanlar">
  <div class="container adopt">
    <div>
      <p class="eyebrow">Looking for a home</p>
      <h2 class="display">Our adoption<br class="lb"> listings</h2>
      <p class="body-lg" style="margin:1.4rem 0 1.9rem; max-width:29rem;">Hundreds of animals in
        our shelters are waiting for a home — sadly, we can’t keep up with sharing every one of
        them. If you can’t find the friend you’re looking for here, or you’re not sure, fill in
        our adoption form and we’ll find the right match together.</p>
      <a class="link-arrow" href="sahiplen.html">Adoption form <span aria-hidden="true">→</span></a>
    </div>

    <div class="adopt__cards">
      <a class="adopt-card" href="yuva-arayan-kopekler.html">
        <img src="assets/img/kopek-portre.jpg" width="2302" height="1535"
             alt="A tan puppy looking at the camera.">
        <span class="adopt-card__caption">
          <span class="adopt-card__handle">Our dogs looking for a home</span>
          <span class="adopt-card__title">Meet the dogs</span>
        </span>
      </a>
      <a class="adopt-card adopt-card--cat" href="yuva-arayan-kediler.html">
        <img src="assets/img/kedi-yasam-alani.jpg" width="2048" height="1152"
             alt="The corridor of the cat shelter, with climbing shelves and beds along the wall.">
        <span class="adopt-card__caption">
          <span class="adopt-card__handle">Our cats looking for a home</span>
          <span class="adopt-card__title">Meet the cats</span>
        </span>
      </a>
    </div>
  </div>
</section>

<div class="split split--orange split--media-left">
  <div class="split__media">
    <img src="assets/img/bahce-kopekler.jpg" width="1200" height="1600"
         alt="Dogs gathered in the garden of the Hadımköy shelter.">
    <p class="sticker sticker--plain sticker--onmedia">Foster home = room for a new rescue</p>
  </div>
  <div class="split__body">
    <p class="eyebrow">Space in your home saves lives in the field</p>
    <h2 class="display">One kennel empties.<br class="lb"> A new life<br class="lb"> is rescued.</h2>
    <p class="body-md" style="max-width:30rem;">Fostering isn’t a trial adoption. It’s offering an
      animal a safe, short-term home while it gets ready for its forever family.</p>
    <ul class="checklist">
      <li>Kurtaran Ev support throughout</li>
      <li>The right match for the animal’s needs</li>
      <li>Clear responsibilities and follow-up</li>
    </ul>
    <div>
      <a class="btn btn--sky" href="gecici-yuva.html">Learn how it works and apply <span aria-hidden="true">→</span></a>
    </div>
  </div>
</div>

<div class="split split--navy split--media-left">
  <div class="split__media">
    <img src="assets/img/kopek-portre.jpg" width="2302" height="1535"
         alt="A dog resting its paw on a volunteer’s knee and looking at the camera.">
    <p class="sticker sticker--green sticker--onmedia">Be there every month.</p>
  </div>
  <div class="split__body">
    <p class="eyebrow">Regular support, sustainable care</p>
    <h2 class="display">Become a Guardian Angel.</h2>
    <p class="body-md" style="max-width:33rem;">Your regular support, starting from ₺3,000 a month,
      goes towards food, treatment, medicine and keeping our shelters running.</p>

    <div class="amounts" data-amounts data-amount-target="#melek-cta-label">
      <p class="amounts__label">Choose your monthly amount</p>
      <div class="amounts__options">
        <button class="amount is-active" type="button" data-amount="3000" aria-pressed="true">₺3,000</button>
        <button class="amount" type="button" data-amount="5000" aria-pressed="false">₺5,000</button>
        <button class="amount" type="button" data-amount="7500" aria-pressed="false">₺7,500</button>
        <button class="amount" type="button" data-amount="custom" aria-pressed="false">Other</button>
        <input class="amount-custom" type="number" min="100" step="100" hidden
               aria-label="Other amount (₺)" placeholder="₺ amount">
      </div>
    </div>

    <div>
      <a class="btn btn--yellow" href="koruyucu-melek.html">
        <span id="melek-cta-label">Start with ₺3,000</span> <span aria-hidden="true">→</span>
      </a>
    </div>
    <p class="amounts__note">You can change or cancel your support at any time.</p>
  </div>
</div>

<section class="section section--cream">
  <div class="container">
    <div class="section__head">
      <div>
        <p class="eyebrow">Stories and news from the field</p>
        <h2 class="display">The ones who make hope visible.</h2>
      </div>
      <a class="link-arrow" href="hikayeler.html">All stories <span aria-hidden="true">→</span></a>
    </div>

    <div class="stories">
      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-lucy.jpg" width="460" height="430"
               alt="A smiling woman holding Lucy on a yellow sofa.">
        </figure>
        <span class="story__tag">Happy ending</span>
        <h3 class="story__title">Lucy’s new life</h3>
        <p class="story__excerpt">While her cancer treatment was still ongoing, a family opened not
          just their home to her, but their whole hearts.</p>
        <a class="link-arrow link-arrow--sm" href="hikayeler.html">Read the story <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-mobil-klinik.png" width="1336" height="1194"
               alt="Promotional image for the Kurtaran Araç mobile clinic project.">
        </figure>
        <span class="story__tag">Project · Corporate partnership</span>
        <h3 class="story__title">Mobile clinic: Kurtaran Araç</h3>
        <p class="story__excerpt">With the support of Anadolu Sigorta, we bring treatment, neutering
          and check-ups to wherever they’re needed.</p>
        <a class="link-arrow link-arrow--sm" href="hikayeler.html">Read the story <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-kevok.jpg" width="1600" height="1332"
               alt="A man carrying his white dog Kevok in his arms on the beach.">
        </figure>
        <span class="story__tag">Happy ending</span>
        <h3 class="story__title">Kevok was finally seen</h3>
        <p class="story__excerpt">Overlooked for years because of his breed and age, Kevok met the
          person who truly saw him.</p>
        <a class="link-arrow link-arrow--sm" href="hikayeler.html">Read the story <span aria-hidden="true">↗</span></a>
      </article>
    </div>
  </div>
</section>

<section class="section section--sky section--tight">
  <div class="container areas">
    <div>
      <p class="eyebrow">Get to know Kurtaran Ev</p>
      <h2 class="display">Four shelters. One promise:<br class="lb"> no one gets<br class="lb"> left behind.</h2>
      <p class="body-lg" style="margin:1.4rem 0 2rem; max-width:30rem;">Our treatment,
        rehabilitation, adoption and lifelong-care work continues across four sites in Istanbul.</p>
      <a class="btn btn--ghost" href="yasam-alanlari.html">Explore our shelters <span aria-hidden="true">→</span></a>
    </div>

    <div class="areas__list">
      <div class="area-row">
        <span class="area-row__num">01</span>
        <h3 class="area-row__name">Hadımköy Shelter</h3>
        <p class="area-row__desc">Care and rehabilitation for dogs</p>
      </div>
      <div class="area-row">
        <span class="area-row__num">02</span>
        <h3 class="area-row__name">Cat Shelter</h3>
        <p class="area-row__desc">A safe living and care space for cats</p>
      </div>
      <div class="area-row">
        <span class="area-row__num">03</span>
        <h3 class="area-row__name">Beşiktaş Cat Adoption Centre</h3>
        <p class="area-row__desc">Meet-and-greets and adoptions</p>
      </div>
      <div class="area-row">
        <span class="area-row__num">04</span>
        <h3 class="area-row__name">Dumankaya Cat Treatment Centre</h3>
        <p class="area-row__desc">Treatment and recovery</p>
      </div>
    </div>
  </div>
</section>

<section class="newsletter">
  <div class="container newsletter__inner">
    <div>
      <p class="eyebrow">Follow our progress</p>
      <h2 class="display">Subscribe to our newsletter.</h2>
    </div>
    <form data-demo-form data-demo-message="Thank you! Newsletter sign-up isn’t connected yet in this local prototype.">
      <label class="newsletter__label" for="bulten-eposta">E-mail address</label>
      <div class="newsletter__form">
        <input id="bulten-eposta" type="email" name="email" placeholder="name@example.com" required>
        <button type="submit">Subscribe →</button>
      </div>
      <p class="form-status" role="status"></p>
    </form>
  </div>
</section>
"""


# ===========================================================================
# ADOPT
# ===========================================================================
SAHIPLEN = page_hero(
    "Adopt · Adopt",
    "Meet the animals<br class=\"lb\"> looking for a home.",
    "We keep our adoption listings up to date on our cat and dog accounts. "
    "When you see an animal you’d like to meet, write to us — we’ll take it from there together.",
    actions='<a class="btn" href="yuva-arayan-kopekler.html">Dogs looking for a home <span aria-hidden="true">→</span></a>'
            '<a class="btn btn--sky" href="yuva-arayan-kediler.html">Cats looking for a home <span aria-hidden="true">→</span></a>'
            '<a class="link-arrow" href="sahiplenmeden-once.html">Before you adopt <span aria-hidden="true">↘</span></a>',
    figure='<img src="assets/img/kopek-portre.jpg" alt="A tan dog looking for a home looks at the camera.">',
    breadcrumb=crumb(("Home", "index.html"), ("Adopt", None), ("Adopt", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="section__head">
      <div>
        <p class="eyebrow">Current listings</p>
        <h2 class="display">Looking for a home today</h2>
      </div>
      <a class="link-arrow" href="__IG_ANA__" target="_blank" rel="noopener">Kurtaran Ev on Instagram <span aria-hidden="true">↗</span></a>
    </div>

    <div class="adopt__cards" style="grid-template-columns:repeat(2,minmax(0,400px));">
      <a class="adopt-card" href="yuva-arayan-kopekler.html">
        <img src="assets/img/kopek-portre.jpg" alt="Dogs looking for a home.">
        <span class="adopt-card__caption">
          <span class="adopt-card__handle">Dogs looking for a home</span>
          <span class="adopt-card__title">Meet the dogs</span>
          <span class="adopt-card__sub" data-sayac="kopek">Browse all listings</span>
        </span>
      </a>
      <a class="adopt-card adopt-card--cat" href="yuva-arayan-kediler.html">
        <img src="assets/img/kedi-yasam-alani.jpg" alt="Cats looking for a home.">
        <span class="adopt-card__caption">
          <span class="adopt-card__handle">Cats looking for a home</span>
          <span class="adopt-card__title">Meet the cats</span>
          <span class="adopt-card__sub" data-sayac="kedi">Browse all listings</span>
        </span>
      </a>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <p class="eyebrow">Who could you give a home to?</p>
    <h2 class="display" style="margin-bottom:2.6rem;">Every animal needs something different.</h2>
    <div class="tiles">
      <article class="tile tile--white">
        <span class="tile__kicker">Puppies and kittens</span>
        <h3 class="tile__title">Full of energy, eager to learn</h3>
        <p class="tile__text">We’re looking for homes that can set aside regular time in the first
          months for training, the vaccination schedule and socialisation.</p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">Adults</span>
        <h3 class="tile__title">Settled character, quick to adapt</h3>
        <p class="tile__text">Because we know their temperament, it’s much easier to find the
          match that best fits your home and your rhythm of life.</p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">Special care</span>
        <h3 class="tile__title">They ask for patience and win your heart</h3>
        <p class="tile__text">For elderly animals, those with chronic conditions or disabilities,
          we plan the treatment support together with you.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--cream section--tight">
  <div class="container">
    <div class="callout">
      <h2 class="callout__title">Is there an animal you’d like to meet?</h2>
      <p class="callout__text">Leave a comment under the listing or write to us directly.
        Our team will get in touch and arrange a first conversation.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="iletisim.html">Write to us <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="sahiplenme-sureci.html">How does the process work? <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
""".replace("__IG_KOPEK__", IG_KOPEK).replace("__IG_KEDI__", IG_KEDI).replace("__IG_ANA__", IG_ANA)


# ===========================================================================
# FOSTER
# ===========================================================================
GECICI_YUVA = page_hero(
    "Adopt · Foster",
    "One kennel empties.<br class=\"lb\"> A new life is rescued.",
    "Fostering isn’t a trial adoption. It’s offering an animal a safe, short-term home "
    "while it gets ready for its forever family.",
    actions='<a class="btn btn--sky" href="#basvuru">Apply to foster <span aria-hidden="true">→</span></a>',
    figure='<img src="assets/img/bahce-kopekler.jpg" alt="Dogs waiting in the shelter garden.">',
    breadcrumb=crumb(("Home", "index.html"), ("Adopt", None), ("Foster", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="section__intro">
      <p class="eyebrow">How does it work?</p>
      <h2 class="display">Fostering in four steps</h2>
    </div>
    <div class="steps">
      <div class="step">
        <span class="step__num">01</span>
        <div>
          <h3 class="step__title">Application and first chat</h3>
          <p class="step__text">Fill in the form; we’ll have a short conversation about your home
            set-up, your daily routine and any previous experience.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">02</span>
        <div>
          <h3 class="step__title">The right match</h3>
          <p class="step__text">We match the animal’s needs with the conditions in your home.
            It could be a puppy or kitten, an adult, or an animal going through treatment.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">03</span>
        <div>
          <h3 class="step__title">Support all the way through</h3>
          <p class="step__text">Food, medical follow-up and behaviour advice are on Kurtaran Ev.
            You provide a safe room and regular attention.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">04</span>
        <div>
          <h3 class="step__title">Sending them off to a forever home</h3>
          <p class="step__text">When a permanent home is found, we plan the handover together.
            The space you free up means another life can be rescued.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <article class="tile tile--sky">
        <span class="tile__kicker">Kurtaran Ev covers</span>
        <h3 class="tile__title">The cost of care isn’t on you</h3>
        <ul class="bullets">
          <li>Food, litter and basic care supplies</li>
          <li>Vaccinations, treatment and vet check-ups</li>
          <li>Carrier, lead and bed</li>
          <li>Advice on behavioural issues</li>
        </ul>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">What we ask of you</span>
        <h3 class="tile__title">A safe space and regular attention</h3>
        <ul class="bullets">
          <li>A home with secured windows and balconies</li>
          <li>Feeding and cleaning a few times a day</li>
          <li>Sharing photos and progress updates</li>
          <li>Help getting to check-up appointments</li>
        </ul>
      </article>
    </div>
  </div>
</section>

<section class="section section--cream section--tight" id="basvuru">
  <div class="container">
    <p class="eyebrow">Application</p>
    <h2 class="display" style="margin-bottom:2.2rem;">Is there room in your home?</h2>
    <form class="form-grid" data-demo-form
          data-demo-message="Your application hasn’t actually been received — form submission isn’t connected in this local prototype.">
      <div class="field"><label for="gy-ad">Full name</label><input id="gy-ad" name="ad" required></div>
      <div class="field"><label for="gy-eposta">E-mail</label><input id="gy-eposta" type="email" name="eposta" required></div>
      <div class="field"><label for="gy-telefon">Phone</label><input id="gy-telefon" type="tel" name="telefon"></div>
      <div class="field">
        <label for="gy-tur">Which animals could you foster?</label>
        <select id="gy-tur" name="tur">
          <option>Cats</option><option>Dogs</option><option>Either</option>
        </select>
      </div>
      <div class="field field--full">
        <label for="gy-not">Your home set-up and experience</label>
        <textarea id="gy-not" name="not" placeholder="Are there other animals at home? How much of the day are you in?"></textarea>
      </div>
      <div class="field field--full">
        <button class="btn btn--sky" type="submit">Send application <span aria-hidden="true">→</span></button>
        <p class="form-status" role="status"></p>
      </div>
    </form>
  </div>
</section>
"""


# ===========================================================================
# BEFORE YOU ADOPT
# ===========================================================================
SAHIPLENMEDEN_ONCE = page_hero(
    "Adopt · Before You Adopt",
    "Getting ready, and<br class=\"lb\"> realistic expectations.",
    "Adopting starts with preparation, not just a decision. Before you decide, there are a few "
    "things we’d like you to think through with us.",
    breadcrumb=crumb(("Home", "index.html"), ("Adopt", None), ("Before You Adopt", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="tiles">
      <article class="tile tile--warm">
        <span class="tile__kicker">Time</span>
        <h3 class="tile__title">A 10–15 year promise</h3>
        <p class="tile__text">Moving house, a new job, marriage, children… this animal needs a
          place in your life plans too.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Budget</span>
        <h3 class="tile__title">Ongoing costs</h3>
        <p class="tile__text">You’ll need a monthly budget for food, litter, vaccinations,
          parasite protection and unexpected treatment.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Home</span>
        <h3 class="tile__title">Safety measures</h3>
        <p class="tile__text">For cats, window and balcony netting is a must. For dogs, plan a
          safe walking routine.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Settling in</span>
        <h3 class="tile__title">The first weeks can be rough</h3>
        <p class="tile__text">Hiding, loss of appetite and toilet accidents are normal. Patience
          is the only thing that speeds things up.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Household</span>
        <h3 class="tile__title">Is everyone on board?</h3>
        <p class="tile__text">Everyone in the home — and any other animals, if you have them —
          needs to be part of this decision.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Expectations</span>
        <h3 class="tile__title">A rescued animal isn’t a ready-made pet</h3>
        <p class="tile__text">You’re meeting an animal with a past. Trust is built over time.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <p class="eyebrow">FAQ</p>
    <h2 class="display" style="margin-bottom:2.4rem;">Things people ask</h2>
    <div class="faq">
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false">Can I keep a dog in a flat?</button>
        <div class="faq__a"><p>Yes. What matters isn’t the size of the home but whether the dog’s
          daily need for exercise is met. If you can manage two or three walks a day, a flat
          is no problem.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false">Is it a good idea to adopt with children at home?</button>
        <div class="faq__a"><p>Yes, with the right match. For homes with children we recommend
          well-socialised animals with a patient temperament, and we talk through how to handle
          the first days together.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false">I already have another animal — will they get along?</button>
        <div class="faq__a"><p>Usually, yes. Introductions should be gradual: separate rooms,
          scent swapping and short supervised meetings. We guide you through the process.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false">Is there an adoption fee?</button>
        <div class="faq__a"><p>We don’t charge a fee for adoption. If you’d like, you can make a
          donation towards the other animals in our care.</p></div>
      </div>
    </div>

    <div class="callout callout--sky" style="margin-top:3rem;">
      <h2 class="callout__title">Feeling ready?</h2>
      <p class="callout__text">The next step is to read about the process. You’ll find which
        documents are needed and how the conversations go.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="sahiplenme-sureci.html">Go to the adoption process <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


# ===========================================================================
# ADOPTION PROCESS
# ===========================================================================
SAHIPLENME_SURECI = page_hero(
    "Adopt · Adoption Process",
    "How it works,<br class=\"lb\"> and what you’ll need.",
    "For us, adoption isn’t a handover — it’s a match. The steps below take two to three "
    "weeks on average.",
    breadcrumb=crumb(("Home", "index.html"), ("Adopt", None), ("Adoption Process", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="steps">
      <div class="step">
        <span class="step__num">01</span>
        <div>
          <h3 class="step__title">Look through the listings</h3>
          <p class="step__text">The listings on our adoption accounts give each animal’s age,
            temperament and health. Pick the one you think is right for you.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">02</span>
        <div>
          <h3 class="step__title">First conversation</h3>
          <p class="step__text">In a short phone call or face-to-face chat we talk about your
            routine, your expectations and the conditions in your home.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">03</span>
        <div>
          <h3 class="step__title">Meet-and-greet</h3>
          <p class="step__text">You meet at our shelter or at the animal’s foster home.
            There’s no rush; both sides should feel comfortable.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">04</span>
        <div>
          <h3 class="step__title">Preparing your home and the contract</h3>
          <p class="step__text">For cats, we check window and balcony netting. The adoption
            contract is signed and ID details are recorded.</p>
        </div>
      </div>
      <div class="step">
        <span class="step__num">05</span>
        <div>
          <h3 class="step__title">Moving in and follow-up</h3>
          <p class="step__text">We check in after the first week, the first month and the sixth
            month. If problems come up, our door is always open — returning the animal is
            also an option.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <div>
        <p class="eyebrow">What you’ll need</p>
        <h2 class="display" style="font-size:2.4rem; margin-bottom:1.4rem;">Bring with you</h2>
        <ul class="bullets bullets--lg">
          <li>Photo ID</li>
          <li>You must be 18 or over</li>
          <li>The agreement of everyone living in the home</li>
          <li>If adopting a cat, a photo of your window/balcony netting</li>
          <li>A carrier (if you can’t get one, we’ll provide it)</li>
        </ul>
      </div>
      <div class="callout callout--cream">
        <h2 class="callout__title">Why so thorough?</h2>
        <p class="callout__text">Every animal that comes back means trust that was built being
          broken again. Every question that slows the process raises the chances of a
          forever home.</p>
        <div class="callout__actions">
          <a class="btn" href="sahiplen.html">See who’s looking for a home <span aria-hidden="true">→</span></a>
        </div>
      </div>
    </div>
  </div>
</section>
"""
