# -*- coding: utf-8 -*-
"""English page bodies — part 2: Support and Get Involved pages."""

from pages import page_hero, crumb, IG_KOPEK, IG_KEDI, IG_ANA  # noqa: F401


# ===========================================================================
# SUPPORT
# ===========================================================================
BAGIS_YAP = page_hero(
    "Support · Donate",
    "Your support<br class=\"lb\"> changes a life,<br class=\"lb\"> not just a day.",
    "Every donation goes straight to food, treatment, medicine and the running costs of our "
    "shelters. One-off or monthly — both mean the world to us.",
    actions='<a class="btn" href="#bagis-yontemleri">Ways to give <span aria-hidden="true">→</span></a>'
            '<a class="link-arrow" href="koruyucu-melek.html">Give monthly <span aria-hidden="true">↘</span></a>',
    breadcrumb=crumb(("Home", "index.html"), ("Support", None), ("Donate", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">Where does your donation go?</p>
    <h2 class="display" style="margin-bottom:2.6rem;">What it pays for</h2>
    <div class="tiles tiles--4">
      <article class="tile tile--yellow">
        <span class="tile__kicker">₺500</span>
        <h3 class="tile__title">A week of food</h3>
        <p class="tile__text">Covers a week's worth of dry food for one dog.</p>
      </article>
      <article class="tile tile--sky">
        <span class="tile__kicker">₺1.500</span>
        <h3 class="tile__title">Vaccines and parasite protection</h3>
        <p class="tile__text">A full year of combined vaccines plus internal and external parasite protection for one animal.</p>
      </article>
      <article class="tile tile--orange">
        <span class="tile__kicker">₺3.000</span>
        <h3 class="tile__title">Spay / neuter</h3>
        <p class="tile__text">One spay or neuter operation and the aftercare that follows.</p>
      </article>
      <article class="tile tile--green">
        <span class="tile__kicker">₺7.500+</span>
        <h3 class="tile__title">Emergency treatment</h3>
        <p class="tile__text">For fractures, accidents and cases that need advanced care.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight" id="bagis-yontemleri">
  <div class="container">
    <p class="eyebrow">How can you give?</p>
    <h2 class="display" style="margin-bottom:2.4rem;">Three ways</h2>
    <div class="tiles">
      <article class="tile tile--white">
        <span class="tile__kicker">01</span>
        <h3 class="tile__title">Bank transfer</h3>
        <p class="tile__text">Send directly to the association's bank account. Writing your name in
          the reference field is all we need for your receipt.</p>
        <p class="tile__meta">For account details: <a href="mailto:iletisim@kurtaranev.org">iletisim@kurtaranev.org</a></p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">02</span>
        <h3 class="tile__title">Monthly giving</h3>
        <p class="tile__text">Become a Guardian Angel and give automatically every month; it lets us
          plan care that doesn't stop.</p>
        <p class="tile__meta"><a href="koruyucu-melek.html">Become a Guardian Angel →</a></p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">03</span>
        <h3 class="tile__title">In-kind donation</h3>
        <p class="tile__text">Food, litter, medicine, blankets and cleaning supplies. We keep the
          priority list up to date.</p>
        <p class="tile__meta"><a href="https://www.amazon.com.tr/kurtaranev" target="_blank" rel="noopener">Amazon wish list ↗</a> · <a href="guncel-ihtiyaclar.html">Current needs →</a></p>
      </article>
    </div>

    <div class="callout" style="margin-top:3rem;">
      <h2 class="callout__title">Turn your donation into a meaningful gift</h2>
      <p class="callout__text">For a birthday, an anniversary or a thank-you, send the people you
        love a Kurtaran Ev e-card.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="e-kartlar.html">E-cards & certificates <span aria-hidden="true">→</span></a>
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
      <p class="eyebrow">Support · Guardian Angel</p>
      <h1 class="display">Become a Guardian Angel.</h1>
      <p class="page-hero__lead">Your monthly support, starting from ₺3.000, helps keep food, treatment,
        medicine and our shelters going.</p>

      <div class="amounts" data-amounts data-amount-target="#melek-sayfa-cta">
        <p class="amounts__label">Choose your monthly amount</p>
        <div class="amounts__options">
          <button class="amount is-active" type="button" data-amount="3000" aria-pressed="true">₺3.000</button>
          <button class="amount" type="button" data-amount="5000" aria-pressed="false">₺5.000</button>
          <button class="amount" type="button" data-amount="7500" aria-pressed="false">₺7.500</button>
          <button class="amount" type="button" data-amount="custom" aria-pressed="false">Other</button>
          <input class="amount-custom" type="number" min="100" step="100" hidden
                 aria-label="Other amount (₺)" placeholder="₺ amount">
        </div>
      </div>

      <div>
        <a class="btn btn--yellow" href="#melek-form">
          <span id="melek-sayfa-cta">Start with ₺3.000</span> <span aria-hidden="true">→</span>
        </a>
      </div>
      <p class="amounts__note">You can change or cancel your support at any time.</p>
    </div>

    <figure class="page-hero__figure" style="border-color:var(--white); box-shadow:6px 6px 0 var(--yellow);">
      <img src="assets/img/kopek-portre.jpg" alt="A dog reaching out a paw and looking at the camera.">
    </figure>
  </div>
</section>

<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">Why monthly support?</p>
    <h2 class="display" style="margin-bottom:2.4rem;">Keeping going is the hardest part of rescue</h2>
    <div class="tiles">
      <article class="tile tile--warm">
        <span class="tile__kicker">Predictability</span>
        <h3 class="tile__title">We know how much food we can buy each month</h3>
        <p class="tile__text">Steady income means bargaining power with suppliers and real stock planning.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Uninterrupted treatment</span>
        <h3 class="tile__title">Long-term treatments don't get cut short</h3>
        <p class="tile__text">Months of medication and check-ups for chronic conditions are covered.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Capacity</span>
        <h3 class="tile__title">Room opens up for new rescues</h3>
        <p class="tile__text">With current care secured, we can take in new animals from the field.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight" id="melek-form">
  <div class="container">
    <p class="eyebrow">Let's begin</p>
    <h2 class="display" style="margin-bottom:2.2rem;">Guardian Angel sign-up</h2>
    <form class="form-grid" data-demo-form
          data-demo-message="Your sign-up was not saved — payments are not connected in this local prototype.">
      <div class="field"><label for="km-ad">Full name</label><input id="km-ad" name="ad" required></div>
      <div class="field"><label for="km-eposta">E-mail</label><input id="km-eposta" type="email" name="eposta" required></div>
      <div class="field"><label for="km-telefon">Phone</label><input id="km-telefon" type="tel" name="telefon"></div>
      <div class="field">
        <label for="km-tutar">Monthly amount (₺)</label>
        <input id="km-tutar" type="number" name="tutar" value="3000" min="100" step="100">
      </div>
      <div class="field field--full">
        <label for="km-not">Anything you'd like to add</label>
        <textarea id="km-not" name="not" placeholder="Would you like your support to go towards a particular area?"></textarea>
      </div>
      <div class="field field--full">
        <button class="btn btn--yellow" type="submit">Complete sign-up <span aria-hidden="true">→</span></button>
        <p class="form-status" role="status"></p>
        <p class="form-note">Payment processing will be connected when the site goes live.</p>
      </div>
    </form>
  </div>
</section>
""".replace("__CRUMB__", crumb(("Home", "index.html"), ("Support", None), ("Guardian Angel", None)))


E_KARTLAR = page_hero(
    "Support · E-cards & Certificates",
    "Let your gift<br class=\"lb\"> touch a life.",
    "A birthday, an anniversary, a thank-you or a remembrance… We turn your donation into a "
    "personalised e-card or digital certificate.",
    breadcrumb=crumb(("Home", "index.html"), ("Support", None), ("E-cards & Certificates", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="tiles">
      <article class="tile tile--yellow">
        <span class="tile__kicker">E-card</span>
        <h3 class="tile__title">Celebration card</h3>
        <p class="tile__text">With the image and message you choose, delivered to the recipient's
          inbox on the date you pick.</p>
        <p class="tile__meta">With donations from ₺500</p>
      </article>
      <article class="tile tile--sky">
        <span class="tile__kicker">Certificate</span>
        <h3 class="tile__title">Guardian Angel certificate</h3>
        <p class="tile__text">Cover an animal's monthly care in the name of someone you love;
          we'll issue the certificate in their name.</p>
        <p class="tile__meta">With monthly support from ₺3.000</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Remembrance</span>
        <h3 class="tile__title">In-memory donation</h3>
        <p class="tile__text">A specially designed card for donations made in memory of a
          friend you have lost.</p>
        <p class="tile__meta">You choose the amount</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <p class="eyebrow">How does it work?</p>
    <h2 class="display" style="margin-bottom:2rem;">Three steps</h2>
    <div class="steps">
      <div class="step"><span class="step__num">01</span><div>
        <h3 class="step__title">Make your donation</h3>
        <p class="step__text">Choose the amount and how you'd like to give.</p></div></div>
      <div class="step"><span class="step__num">02</span><div>
        <h3 class="step__title">Send us the card details</h3>
        <p class="step__text">The recipient's name and e-mail address, your message and the delivery date.</p></div></div>
      <div class="step"><span class="step__num">03</span><div>
        <h3 class="step__title">We'll send it</h3>
        <p class="step__text">Your card is delivered on the date you chose, on your behalf.</p></div></div>
    </div>

    <div class="callout" style="margin-top:3rem;">
      <h2 class="callout__title">Request an e-card</h2>
      <p class="callout__text">For now we take e-card requests by e-mail.
        Just send us the recipient's details and your message.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="mailto:iletisim@kurtaranev.org?subject=E-card%20request">
          Send an e-mail <span aria-hidden="true">↗</span></a>
        <a class="link-arrow" href="bagis-yap.html">Donate first <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


KURTARAN_SHOP = page_hero(
    "Support · Kurtaran Shop",
    "Every item you buy<br class=\"lb\"> goes to an animal.",
    "Everything you spend at Kurtaran Shop goes directly towards food, treatment and the "
    "running costs of our shelters.",
    breadcrumb=crumb(("Home", "index.html"), ("Support", None), ("Kurtaran Shop", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">Storefront</p>
    <h2 class="display" style="margin-bottom:2.6rem;">Featured</h2>
    <div class="tiles tiles--4">
      <article class="tile tile--white">
        <span class="tile__kicker">Apparel</span>
        <h3 class="tile__title">“Every life safe” T-shirt</h3>
        <p class="tile__text">Organic cotton, unisex fit.</p>
        <p class="tile__meta">₺750</p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">Accessories</span>
        <h3 class="tile__title">Tote bag</h3>
        <p class="tile__text">Kurtaran Ev illustration, roomy.</p>
        <p class="tile__meta">₺350</p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">Home</span>
        <h3 class="tile__title">Mug</h3>
        <p class="tile__text">Your morning coffee with a story of kindness.</p>
        <p class="tile__meta">₺400</p>
      </article>
      <article class="tile tile--white">
        <span class="tile__kicker">Stationery</span>
        <h3 class="tile__title">Sticker set</h3>
        <p class="tile__text">The mascots of our shelters.</p>
        <p class="tile__meta">₺150</p>
      </article>
    </div>
    <p class="form-note">Products and prices are sample content; the shop will be connected when the site goes live.</p>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="callout callout--sky">
      <h2 class="callout__title">Corporate orders</h2>
      <p class="callout__text">Place a bulk order for your company's holiday gifts or event kits.
        All proceeds go to our work in the field.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="kurumsal-is-birligi.html">Corporate partnership <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="mailto:iletisim@kurtaranev.org?subject=Kurtaran%20Shop%20bulk%20order">
          Request a quote <span aria-hidden="true">↗</span></a>
      </div>
    </div>
  </div>
</section>
"""


GUNCEL_IHTIYACLAR = page_hero(
    "Support · Current Needs",
    "What do we need<br class=\"lb\"> most this week?",
    "We update this list regularly based on what the field tells us. You can bring in-kind "
    "donations to our shelters or send them by courier.",
    variant=" page-hero--sky",
    breadcrumb=crumb(("Home", "index.html"), ("Support", None), ("Current Needs", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <article class="tile tile--warm">
        <span class="tile__kicker">Urgent</span>
        <h3 class="tile__title">Dog shelter</h3>
        <ul class="bullets">
          <li>Adult dry dog food</li>
          <li>Internal and external parasite drops</li>
          <li>Blankets and beds</li>
          <li>Disinfectant and bleach</li>
        </ul>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Urgent</span>
        <h3 class="tile__title">Cat shelter</h3>
        <ul class="bullets">
          <li>Clumping cat litter</li>
          <li>Kitten food and milk replacer</li>
          <li>Wet food (for animals in treatment)</li>
          <li>Paper towels</li>
        </ul>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Ongoing</span>
        <h3 class="tile__title">Medical supplies</h3>
        <ul class="bullets">
          <li>IV fluids and syringes</li>
          <li>Bandages, sterile gauze</li>
          <li>Elizabethan collars</li>
        </ul>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Ongoing</span>
        <h3 class="tile__title">Logistics</h3>
        <ul class="bullets">
          <li>Pet carriers</li>
          <li>Collars and harnesses</li>
          <li>Help with transport by car</li>
        </ul>
      </article>
    </div>

    <div class="callout" style="margin-top:3rem;">
      <h2 class="callout__title">Where can I send things?</h2>
      <p class="callout__text">Items you pick from our Amazon wish list are shipped straight to
        our shelters. You're also welcome to drop off in-kind donations during visiting hours;
        if you'd like to send a parcel, write to us first and we'll share the address.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="https://www.amazon.com.tr/kurtaranev" target="_blank" rel="noopener">Amazon wish list <span aria-hidden="true">↗</span></a>
        <a class="link-arrow" href="yasam-alanlari.html">Shelters and hours <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="iletisim.html">Get in touch <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


# ===========================================================================
# GET INVOLVED
# ===========================================================================
GONULLU_OL = page_hero(
    "Get Involved · Volunteer",
    "Your skills,<br class=\"lb\"> wherever they're<br class=\"lb\"> needed.",
    "From walking dogs in the field to creating social media content, from driving animals to the "
    "vet to organising events — we need volunteers in all sorts of areas.",
    actions='<a class="btn" href="#gonullu-form">Apply to volunteer <span aria-hidden="true">→</span></a>',
    figure='<img src="assets/img/hero-kucak.jpg" alt="A volunteer spending time with a dog.">',
    breadcrumb=crumb(("Home", "index.html"), ("Get Involved", None), ("Volunteer", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">Ways to volunteer</p>
    <h2 class="display" style="margin-bottom:2.6rem;">How can you help?</h2>
    <div class="tiles">
      <article class="tile tile--warm">
        <span class="tile__kicker">In the field</span>
        <h3 class="tile__title">Care and socialisation</h3>
        <p class="tile__text">Walking, grooming, play and help with cleaning. Even a few hours a
          week makes a big difference.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Transport</span>
        <h3 class="tile__title">Driving support</h3>
        <p class="tile__text">Volunteers with a car who can help with vet appointments and
          adoption hand-overs.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Digital</span>
        <h3 class="tile__title">Content and communication</h3>
        <p class="tile__text">Photography, video, copywriting, social media management and
          translation.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Expertise</span>
        <h3 class="tile__title">Veterinary and behaviour</h3>
        <p class="tile__text">A volunteer programme for veterinarians, veterinary technicians and
          behaviour specialists.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Events</span>
        <h3 class="tile__title">Stalls and organisation</h3>
        <p class="tile__text">Join the team at adoption days, fundraising events and school
          visits.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">Office</span>
        <h3 class="tile__title">Records and follow-up</h3>
        <p class="tile__text">Behind-the-scenes work such as adoption records, donation tracking
          and reporting.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight" id="gonullu-form">
  <div class="container">
    <p class="eyebrow">Application</p>
    <h2 class="display" style="margin-bottom:2.2rem;">Tell us about yourself</h2>
    <form class="form-grid" data-demo-form
          data-demo-message="Your application was not saved — form submission is not connected in this local prototype.">
      <div class="field"><label for="go-ad">Full name</label><input id="go-ad" name="ad" required></div>
      <div class="field"><label for="go-eposta">E-mail</label><input id="go-eposta" type="email" name="eposta" required></div>
      <div class="field">
        <label for="go-alan">Area you're interested in</label>
        <select id="go-alan" name="alan">
          <option>Care and socialisation in the field</option>
          <option>Driving support</option>
          <option>Content and communication</option>
          <option>Veterinary / behaviour</option>
          <option>Events</option>
          <option>Office and records</option>
        </select>
      </div>
      <div class="field">
        <label for="go-sure">Time you can give per week</label>
        <select id="go-sure" name="sure">
          <option>1–3 hours</option><option>4–8 hours</option><option>More than 8 hours</option>
        </select>
      </div>
      <div class="field field--full">
        <label for="go-not">Your experience and anything else you'd like to add</label>
        <textarea id="go-not" name="not"></textarea>
      </div>
      <div class="field field--full">
        <button class="btn" type="submit">Send application <span aria-hidden="true">→</span></button>
        <p class="form-status" role="status"></p>
      </div>
    </form>
  </div>
</section>
"""


KURUMSAL = page_hero(
    "Get Involved · Corporate Partnership",
    "Your company's<br class=\"lb\"> strength, felt<br class=\"lb\"> in the field.",
    "Work that creates lasting impact, like our mobile clinic project, comes to life through "
    "corporate partnerships. Let's talk about what we can do together.",
    actions='<a class="btn" href="mailto:iletisim@kurtaranev.org?subject=Corporate%20partnership">'
            'Write to us about partnering <span aria-hidden="true">↗</span></a>',
    figure='<img src="assets/img/hikaye-mobil-klinik.png" alt="Presentation of the Kurtaran Araç mobile clinic project.">',
    breadcrumb=crumb(("Home", "index.html"), ("Get Involved", None), ("Corporate Partnership", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">Partnership models</p>
    <h2 class="display" style="margin-bottom:2.6rem;">Four options</h2>
    <div class="tiles tiles--2">
      <article class="tile tile--sky">
        <span class="tile__kicker">01</span>
        <h3 class="tile__title">Project sponsorship</h3>
        <p class="tile__text">Sponsor a defined project such as the mobile clinic, a spay/neuter
          campaign or a shelter renovation. We'll report on the process and the results.</p>
      </article>
      <article class="tile tile--sky">
        <span class="tile__kicker">02</span>
        <h3 class="tile__title">Corporate Guardian Angel</h3>
        <p class="tile__text">Regular monthly support in your company's name; take on the care of
          a set number of animals.</p>
      </article>
      <article class="tile tile--sky">
        <span class="tile__kicker">03</span>
        <h3 class="tile__title">Employee volunteering</h3>
        <p class="tile__text">We organise field days for teams: care, cleaning, play and
          walks. Great for team spirit, too.</p>
      </article>
      <article class="tile tile--sky">
        <span class="tile__kicker">04</span>
        <h3 class="tile__title">In-kind and logistics support</h3>
        <p class="tile__text">Food, medicine, building materials, transport and storage are
          every bit as valuable as cash.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <div>
        <p class="eyebrow">Case study</p>
        <h2 class="display" style="font-size:2.4rem; margin-bottom:1.2rem;">Kurtaran Araç</h2>
        <p class="body-lg" style="margin-bottom:1rem;">Our mobile clinic, launched with the support of
          Anadolu Sigorta, brings volunteer veterinarians into the field to provide on-site
          treatment, spay/neuter surgery and check-ups.</p>
        <p class="body-lg">A moderately equipped mobile clinic makes an enormous difference,
          especially in disaster areas.</p>
        <p style="margin-top:1.6rem;"><a class="link-arrow" href="hikayeler.html">Read about the project <span aria-hidden="true">→</span></a></p>
      </div>
      <figure class="page-hero__figure" style="aspect-ratio:1336/1194;">
        <img src="assets/img/hikaye-mobil-klinik.png" alt="Presentation image of the Kurtaran Araç mobile clinic.">
      </figure>
    </div>
  </div>
</section>
"""
