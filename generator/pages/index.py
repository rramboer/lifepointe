"""Home page."""
from ..helpers import esc, month_year, page_href, years_since
from ..hours import hours_table
from ..icons import icon, svg
from ..layout import V, cta_band, page
from ..seo import local_business

FILENAME = 'index.html'


def render(site):
    p = site.practice
    maps = esc(p.maps_url)
    categories = site.testimonials.categories
    stories = {t.id: (t, c.label) for c in categories for t in c.testimonials}

    cards_html = '\n'.join(
        f'''<a class="card card--link" href="{page_href('services.html')}">
      {icon(card.icon)}
      <h3 class="display-3">{esc(card.title)}</h3>
      <p>{esc(card.summary)}</p>
      <p class="card__more">Learn more{svg('arrow-right')}</p>
    </a>''' for card in site.services.home_cards)

    # home-quotes.json lists testimonial ids; the label line is the testimonial's category.
    quotes_html = '\n'.join(
        f'''<figure class="quote">
      <blockquote><p>{esc(t.quote)}</p></blockquote>
      <footer>{esc(t.author)} <span>{esc(label)} &middot; Lifepointe patient</span></footer>
    </figure>''' for t, label in (stories[tid] for tid in site.home_quotes))

    plans = '\n          '.join(f'<li><span class="chip">{esc(plan)}</span></li>' for plan in p.in_network)

    body = f'''
<section class="section hero" aria-labelledby="hero-h">
  <div class="wrap grid-2">
    <div>
      <span class="eyebrow rise">Family &amp; sports chiropractic &middot; Clarkston, Michigan</span>
      <h1 id="hero-h" class="display-1 rise rise-2">Health comes from within.<br>We clear the way.</h1>
      <p class="lede rise rise-3">Your body is built to heal itself &mdash; our job is to remove what&rsquo;s interfering. Since 2001, Lifepointe has cared for Clarkston families at every age, from newborns just minutes old to the most experienced members of our community.</p>
      <div class="btn-row rise rise-4 mt-15">
        <a class="btn btn--primary" href="{page_href('contact.html#appointment')}">Request an appointment</a>
        <a class="btn btn--ghost" href="{page_href('new-patients.html')}">What to expect</a>
      </div>
      <div class="badge-row rise rise-4 mt-2">
        <span class="badge">{svg('users')} All ages welcome</span>
      </div>
    </div>
    <div class="hero-media rise rise-3">
      <figure class="photo">
        <img src="assets/photo-adjustment.jpg" alt="A chiropractor examining a patient&rsquo;s spine and posture by hand" width="1396" height="930">
      </figure>
      <div class="photo-chip">Serving Clarkston for <span data-since="{esc(p.opened)}">{years_since(p.opened)}</span> years<span class="photo-chip__note">Est. {month_year(p.opened)}</span></div>
    </div>
  </div>
  <div class="wrap">
    <div class="hero-plans rise rise-4">
      <div class="hero-plans__row">
        <h2 id="plans-h" class="hero-plans__title">{svg('shield')} In-network with<span class="visually-hidden"> these insurance plans</span></h2>
        <ul class="chip-grid" aria-labelledby="plans-h">
          {plans}
        </ul>
      </div>
      <p class="hero-plans__note">Other policies are accepted out-of-network.</p>
    </div>
  </div>
</section>

<div class="rail-wrap">

<section class="section section--card" aria-labelledby="approach-h">
  {V}
  <div class="wrap grid-2">
    <div>
      <span class="eyebrow">The approach</span>
      <h2 id="approach-h" class="display-2">More than back-pain doctors</h2>
      <p>Chiropractic is a drug-free healthcare profession focused on the musculoskeletal and nervous systems. Your nervous system &mdash; brain, spinal cord, and the nerves branching to every cell, tissue, and organ &mdash; just happens to be housed inside your spine.</p>
      <p>We&rsquo;re highly specialized in analyzing joint mobility and correcting subluxations (misalignments) in the spine, using gentle techniques that restore proper joint function and, more importantly, nervous system communication. We get to the root cause &mdash; and the symptoms begin to go away on their own.</p>
      <a class="btn btn--ghost" href="{page_href('about.html#chiropractic-care')}">Learn about chiropractic care</a>
    </div>
    <figure class="photo">
      <img src="assets/photo-posture-check.jpg" alt="A chiropractor&rsquo;s hands on a patient&rsquo;s shoulder and upper back, checking posture" width="1440" height="960" loading="lazy">
    </figure>
  </div>
</section>

<section class="section" aria-labelledby="services-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">What we do</span>
    <h2 id="services-h" class="display-2">One place for the whole family&rsquo;s care</h2>
    <p class="lede measure mb-2">A modern facility known for its range of chiropractic techniques &mdash; Diversified, Activator, Logan Basic, Thompson, and Webster &mdash; and the wellness services that support them.</p>
    <div class="grid-3">
      {cards_html}
    </div>
    <div class="btn-row mt-2">
      <a class="btn btn--primary" href="{page_href('services.html')}">See all services &amp; products</a>
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="stories-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Patient stories</span>
    <h2 id="stories-h" class="display-2">Real words from real patients</h2>
    <p class="lede measure mb-2">Success stories, in our patients&rsquo; own words.</p>
    <div class="grid-3">
      {quotes_html}
    </div>
    <div class="btn-row mt-2">
      <a class="btn btn--ghost" href="{page_href('success-stories.html')}">Read more success stories</a>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="visit-h">
  {V}
  <div class="wrap grid-2 grid--top">
    <div>
      <span class="eyebrow">Your first visit</span>
      <h2 id="visit-h" class="display-2">Know what to expect before you walk in</h2>
      <p>Your first visit is a thorough spinal and nervous system exam &mdash; hands-on palpation, posture and range-of-motion checks, and X-rays only if your age and situation call for them. Then we explain everything at your Report of Findings.</p>
      <a class="btn btn--ghost" href="{page_href('new-patients.html')}">The full first-visit guide</a>
    </div>
    <div class="card">
      {icon('clip')}
      <h3 class="display-3">Skip the waiting room</h3>
      <p>Fill out your forms ahead of time and email them to us before your first appointment.</p>
      <ul class="link-list">
        <li><a href="{esc(p.forms.adult)}">Download adult new patient forms (PDF)</a></li>
        <li><a href="{esc(p.forms.child)}">Download child new patient forms (under 12) (PDF)</a></li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="hours-h">
  {V}
  <div class="wrap grid-2 grid--top">
    <div>
      <span class="eyebrow">Hours &amp; location</span>
      <h2 id="hours-h" class="display-2">Easy to find on Dixie&nbsp;Hwy</h2>
      {hours_table(site.hours)}
    </div>
    <div class="card-stack">
      <div class="card">
        {icon('pin')}
        <h3 class="display-3">{esc(p.name)}</h3>
        <p>{esc(p.address)}</p>
        <a class="btn btn--ghost btn--sm" href="{maps}">Get directions</a>
      </div>
    </div>
  </div>
</section>

</div>
{cta_band(site)}'''

    return page(site, FILENAME,
                f'{p.name} | Clarkston, MI',
                'Family & sports chiropractic and wellness care in Clarkston, MI since 2001. Gentle adjustments, massage therapy, digital X-ray, and nutrition — for every age.',
                body, head_extra=local_business(site))
