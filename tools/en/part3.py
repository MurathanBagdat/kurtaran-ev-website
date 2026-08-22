# -*- coding: utf-8 -*-
"""English bodies — part 3: Our Story, Impact, Shelters, Stories, Contact."""

from pages import page_hero, crumb, IG_KOPEK, IG_KEDI, IG_ANA


HIKAYEMIZ = page_hero(
    "About · Our Story & Mission",
    "Every life deserves<br class=\"lb\"> to be safe<br class=\"lb\"> and loved.",
    "Kurtaran Ev is a charity that rescues, treats and rehabilitates stray cats and dogs "
    "and finds them permanent homes.",
    figure='<img src="assets/img/hero-kucak.jpg" alt="A volunteer and a rescued dog.">',
    breadcrumb=crumb(("Home", "index.html"), ("About", None), ("Our Story & Mission", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="prose">
      <h2>How it started</h2>
      <p>A small act of help for one street dog slowly grew into a regular network of care.
        First a few animals, then a garden, then separate shelters… Today we look after around
        1,200 dogs and 600 cats at four different locations across Istanbul.</p>

      <h2>What we do</h2>
      <p>Our work has four strands: <strong>rescue</strong>, <strong>treatment</strong>,
        <strong>rehabilitation</strong> and <strong>lifelong care</strong>. Adoption is only one
        link in that chain; our real responsibility is making sure the animals who can’t be
        adopted stay safe for the rest of their lives.</p>

      <h2>What we believe</h2>
      <ul>
        <li>No animal is left behind because of its age or breed.</li>
        <li>Adoption is a match, not a hand-over.</li>
        <li>Neutering is at the heart of any lasting solution.</li>
        <li>We owe our donors transparency.</li>
      </ul>
    </div>

    <div class="callout callout--cream" style="margin-top:3rem;">
      <h2 class="callout__title">Our mission</h2>
      <p class="callout__text">To keep stray animals safe; to heal them and match them with the
        right homes; and to grow a culture of responsible pet ownership in our community.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="etkimiz.html">See our impact <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="yasam-alanlari.html">Our shelters <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


ETKIMIZ = page_hero(
    "About · Our Impact & Work",
    "The numbers,<br class=\"lb\"> and what they mean<br class=\"lb\"> on the ground.",
    "How many animals we care for, the projects we run and our goals for the period ahead.",
    breadcrumb=crumb(("Home", "index.html"), ("About", None), ("Our Impact & Work", None)),
) + """
<section class="stats" aria-label="Kurtaran Ev in numbers">
  <div class="stats__grid">
    <div class="stats__cell"><span class="stats__num">1.200</span><span class="stats__label">dogs</span></div>
    <div class="stats__cell"><span class="stats__num">600</span><span class="stats__label">cats</span></div>
    <div class="stats__cell"><span class="stats__num">4</span><span class="stats__label">shelters</span></div>
    <div class="stats__cell">
      <p class="stats__note">Rescue, treatment, rehabilitation and lifelong care—every one of
        them made possible by your support.</p>
    </div>
  </div>
</section>

<section class="section section--cream section--tight">
  <div class="container">
    <p class="eyebrow">Our areas of work</p>
    <h2 class="display" style="margin-bottom:2.6rem;">What we do, and how</h2>
    <div class="tiles">
      <article class="tile tile--warm">
        <span class="tile__kicker">01</span>
        <h3 class="tile__title">Rescue and emergency response</h3>
        <p class="tile__text">We respond to reports in the field and bring injured and at-risk
          animals to safety.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">02</span>
        <h3 class="tile__title">Treatment and neutering</h3>
        <p class="tile__text">Working with partner clinics and volunteer vets, we handle
          treatment, vaccination and neutering.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">03</span>
        <h3 class="tile__title">Rehabilitation</h3>
        <p class="tile__text">We run socialisation and behaviour work for animals who have
          been through trauma.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">04</span>
        <h3 class="tile__title">Adoption</h3>
        <p class="tile__text">Pre-interview, meet-and-greet, contract and post-adoption
          follow-up — that’s how we build homes that last.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">05</span>
        <h3 class="tile__title">Lifelong care</h3>
        <p class="tile__text">Shelter, food and medical care for life, for the animals who
          can’t be adopted.</p>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">06</span>
        <h3 class="tile__title">Mobile clinic</h3>
        <p class="tile__text">With the Kurtaran Araç vehicle we take treatment to wherever it’s needed.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--warm section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <div>
        <p class="eyebrow">The period ahead</p>
        <h2 class="display" style="font-size:2.4rem; margin-bottom:1.4rem;">Our goals</h2>
        <ul class="bullets bullets--lg">
          <li>Expand capacity and the quarantine unit at the Cat Shelter</li>
          <li>A neighbourhood-based neutering programme with the mobile clinic</li>
          <li>Double the size of our foster network</li>
          <li>Move post-adoption follow-up to a digital system</li>
        </ul>
      </div>
      <div class="callout">
        <h2 class="callout__title">These goals depend on support</h2>
        <p class="callout__text">Regular donations make our work plannable.
          With your monthly support we can grow our capacity.</p>
        <div class="callout__actions">
          <a class="btn btn--white" href="koruyucu-melek.html">Become a Guardian Angel <span aria-hidden="true">→</span></a>
        </div>
      </div>
    </div>
  </div>
</section>
"""


YASAM_ALANLARI = page_hero(
    "About · Visit Our Shelters",
    "Four shelters.<br class=\"lb\"> One promise:<br class=\"lb\"> no one left behind.",
    "Our treatment, rehabilitation, adoption and lifelong-care work continues at four "
    "locations across Istanbul. You don’t need to wait for an invitation — just let us know you’re coming.",
    variant=" page-hero--sky",
    breadcrumb=crumb(("Home", "index.html"), ("About", None), ("Visit Our Shelters", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="tiles tiles--2">
      <article class="tile tile--warm">
        <span class="tile__kicker">01</span>
        <h3 class="tile__title">Hadımköy Shelter</h3>
        <p class="tile__text">Care and rehabilitation for dogs. The centre of our walking, play
          and socialisation work.</p>
        <dl class="info-list" style="margin-top:.6rem;">
          <div class="info-row"><dt>Visiting hours</dt><dd>11.00–17.00</dd></div>
          <div class="info-row"><dt>Appointment</dt><dd>Not required — just let us know you’re coming</dd></div>
          <div class="info-row"><dt>Location</dt>
            <dd><a href="https://maps.app.goo.gl/R77zL5Gg42f7ZfXY6" target="_blank" rel="noopener">View on map ↗</a></dd></div>
        </dl>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">02</span>
        <h3 class="tile__title">Cat Shelter</h3>
        <p class="tile__text">A safe home and care space for cats, with climbing shelves,
          a separate quarantine unit and rest rooms.</p>
        <dl class="info-list" style="margin-top:.6rem;">
          <div class="info-row"><dt>Visits</dt><dd>By appointment</dd></div>
          <div class="info-row"><dt>Note</dt><dd>The quarantine unit is closed to visitors</dd></div>
        </dl>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">03</span>
        <h3 class="tile__title">Beşiktaş Cat Adoption Centre</h3>
        <p class="tile__text">Meet-and-greets and adoptions. Spend time with cats looking for
          a home in a calm setting.</p>
        <dl class="info-list" style="margin-top:.6rem;">
          <div class="info-row"><dt>Visiting hours</dt><dd>10.00–16.00</dd></div>
          <div class="info-row"><dt>Appointment</dt><dd>Recommended at weekends</dd></div>
          <div class="info-row"><dt>Location</dt>
            <dd><a href="https://maps.app.goo.gl/PutVz4WqqHoSv1bNA" target="_blank" rel="noopener">View on map ↗</a></dd></div>
        </dl>
      </article>
      <article class="tile tile--warm">
        <span class="tile__kicker">04</span>
        <h3 class="tile__title">Dumankaya Cat Treatment Centre</h3>
        <p class="tile__text">Treatment and recovery. Post-operative care and the monitoring
          of chronic conditions happen here.</p>
        <dl class="info-list" style="margin-top:.6rem;">
          <div class="info-row"><dt>Visits</dt><dd>By appointment only</dd></div>
          <div class="info-row"><dt>Note</dt><dd>Visits are limited because of ongoing treatment</dd></div>
        </dl>
      </article>
    </div>

    <div class="callout" style="margin-top:3rem;">
      <h2 class="callout__title">Before you visit</h2>
      <p class="callout__text">We share the full address and directions when you book.
        If you’re bringing food or litter, tell us in advance so we can point you to what’s needed most.</p>
      <div class="callout__actions">
        <a class="btn btn--white" href="iletisim.html">Book a visit <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="guncel-ihtiyaclar.html">Current needs <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>
"""


HIKAYELER = page_hero(
    "Blog · News & Stories",
    "The ones who make<br class=\"lb\"> hope visible.",
    "Happy endings, notes from the field and news from our projects.",
    breadcrumb=crumb(("Home", "index.html"), ("About", None), ("News & Stories", None)),
) + """
<section class="section section--cream section--tight">
  <div class="container">
    <div class="stories">
      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-lucy.jpg" alt="A woman holding Lucy on a yellow sofa.">
        </figure>
        <span class="story__tag">Happy ending</span>
        <h2 class="story__title">Lucy’s new life</h2>
        <p class="story__excerpt">While her cancer treatment was still under way, a family opened
          not just their home but their whole heart to her. Lucy now continues her treatment at home.</p>
        <a class="link-arrow link-arrow--sm" href="#">Read the story <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-mobil-klinik.png" alt="Promotional image for the Kurtaran Araç mobile clinic.">
        </figure>
        <span class="story__tag">Project · Corporate partnership</span>
        <h2 class="story__title">Mobile Clinic: Kurtaran Araç</h2>
        <p class="story__excerpt">With the support of Anadolu Sigorta we take treatment, neutering
          and check-ups to wherever they’re needed. It makes a huge difference in disaster areas in particular.</p>
        <a class="link-arrow link-arrow--sm" href="#">Read the story <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/hikaye-kevok.jpg" alt="A man holding Kevok on the seafront.">
        </figure>
        <span class="story__tag">Happy ending</span>
        <h2 class="story__title">Kevok was finally seen</h2>
        <p class="story__excerpt">Overlooked for years because of his breed and age, Kevok met
          the person who truly saw him. He now walks on the seafront every morning.</p>
        <a class="link-arrow link-arrow--sm" href="#">Read the story <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/bahce-kopekler.jpg" alt="Dogs in the shelter garden.">
        </figure>
        <span class="story__tag">From the field</span>
        <h2 class="story__title">Winter preparations complete</h2>
        <p class="story__excerpt">The kennels at Hadımköy have new insulation and the garden
          ground has been levelled. Thank you to our volunteers.</p>
        <a class="link-arrow link-arrow--sm" href="#">Read the story <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/kedi-yasam-alani.jpg" alt="The corridor of the cat shelter.">
        </figure>
        <span class="story__tag">From the field</span>
        <h2 class="story__title">A new wing at the Cat Shelter</h2>
        <p class="story__excerpt">We’ve opened a separate socialisation room for kittens.
          The first guests have already moved in.</p>
        <a class="link-arrow link-arrow--sm" href="#">Read the story <span aria-hidden="true">↗</span></a>
      </article>

      <article class="story">
        <figure class="story__figure">
          <img src="assets/img/kopek-portre.jpg" alt="A golden dog looking at the camera.">
        </figure>
        <span class="story__tag">Guide</span>
        <h2 class="story__title">The first-week guide</h2>
        <p class="story__excerpt">Practical tips for your first seven days with your newly adopted
          animal: feeding, toilet habits and building trust.</p>
        <a class="link-arrow link-arrow--sm" href="#">Read the story <span aria-hidden="true">↗</span></a>
      </article>
    </div>
    <p class="form-note">Full article pages will be added as content comes in.</p>
  </div>
</section>
"""


ILETISIM = page_hero(
    "About · Contact",
    "Get in touch.",
    "Adoption, fostering, donations or volunteering — whatever it’s about, write to us "
    "and we’ll get back to you as soon as we can.",
    breadcrumb=crumb(("Home", "index.html"), ("About", None), ("Contact", None)),
) + """
<section class="section section--cream section--tight" id="kanallar">
  <div class="container">
    <div class="tiles tiles--2">
      <div>
        <p class="eyebrow">Direct contact</p>
        <h2 class="display" style="font-size:2.4rem; margin-bottom:1.6rem;">Channels</h2>
        <dl class="info-list">
          <div class="info-row"><dt>E-mail</dt>
            <dd><a href="mailto:iletisim@kurtaranev.org">iletisim@kurtaranev.org</a></dd></div>
          <div class="info-row"><dt>Instagram</dt>
            <dd><a href="__IG_ANA__" target="_blank" rel="noopener">@kurtaranev</a></dd></div>
          <div class="info-row"><dt>Dogs looking for a home</dt>
            <dd><a href="__IG_KOPEK__" target="_blank" rel="noopener">@kurtaranev_kopekleri</a></dd></div>
          <div class="info-row"><dt>Cats looking for a home</dt>
            <dd><a href="__IG_KEDI__" target="_blank" rel="noopener">@kurtaranev_kedileri</a></dd></div>
          <div class="info-row"><dt>Hadımköy visits</dt>
            <dd>11.00–17.00 · <a href="https://maps.app.goo.gl/R77zL5Gg42f7ZfXY6" target="_blank" rel="noopener">View on map ↗</a></dd></div>
          <div class="info-row"><dt>Beşiktaş visits</dt>
            <dd>10.00–16.00 · <a href="https://maps.app.goo.gl/PutVz4WqqHoSv1bNA" target="_blank" rel="noopener">View on map ↗</a></dd></div>
        </dl>
      </div>

      <div>
        <p class="eyebrow">Leave a message</p>
        <h2 class="display" style="font-size:2.4rem; margin-bottom:1.6rem;">Form</h2>
        <form class="form-grid" style="grid-template-columns:1fr;" data-demo-form
              data-demo-message="Your message was not sent — the form isn’t connected in this local prototype.">
          <div class="field"><label for="il-ad">Full name</label><input id="il-ad" name="ad" required></div>
          <div class="field"><label for="il-eposta">E-mail</label><input id="il-eposta" type="email" name="eposta" required></div>
          <div class="field">
            <label for="il-konu">Subject</label>
            <select id="il-konu" name="konu">
              <option value="sahiplenme">Adoption</option>
              <option value="gecici-yuva">Fostering</option>
              <option value="koruyucu-melek">Guardian Angel</option>
              <option value="bagis">Donation</option>
              <option value="gonulluluk">Volunteering</option>
              <option value="kurumsal">Corporate partnership</option>
              <option value="diger">Other</option>
            </select>
          </div>
          <div class="field"><label for="il-mesaj">Your message</label><textarea id="il-mesaj" name="mesaj" required></textarea></div>
          <div class="field">
            <button class="btn" type="submit">Send <span aria-hidden="true">→</span></button>
            <p class="form-status" role="status"></p>
          </div>
        </form>
      </div>
    </div>
  </div>
</section>
""".replace("__IG_ANA__", IG_ANA).replace("__IG_KOPEK__", IG_KOPEK).replace("__IG_KEDI__", IG_KEDI)
