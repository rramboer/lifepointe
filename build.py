#!/usr/bin/env python3
"""Generate the Lifepointe website prototype. All content extracted from the live site."""
import os

import pathlib
OUT = str(pathlib.Path(__file__).resolve().parent)

# ---------------------------------------------------------------- facts
PHONE = '(248) 623-6107'
PHONE_TEL = 'tel:+12486236107'
FAX = '(248) 623-6443'
EMAIL = 'lifepointechiro@gmail.com'
ADDRESS = '5896 Dixie Hwy, Ste A, Clarkston, MI 48346'
MAPS = 'https://www.google.com/maps/place/Lifepointe+Chiropractic+and+Wellness+Center/@42.7066913,-83.4049681,15z/data=!4m5!3m4!1s0x0:0xa9dd54196a5af191!8m2!3d42.7066913!4d-83.4049681'
FACEBOOK = 'https://www.facebook.com/lifepointewellness/'
INSTAGRAM = 'https://www.instagram.com/lifepointe.chiropractic/'
FORM_APPT = 'https://api.leadconnectorhq.com/widget/form/f8vb0aCndV7BQySGJTI7'
FORM_ADULT = 'https://res2.yourwebsite.life/res/62f173898d9d30000fa9b6b9/62f53d6f602bec000da85f13'
FORM_CHILD = 'https://res2.yourwebsite.life/res/62f173898d9d30000fa9b6b9/62f53d8125203f000dcbf00d'
PAMPHLET_HEALTH = 'https://res2.yourwebsite.life/res/62f173898d9d30000fa9b6b9/62f3246e6f6f3a000de4f063'
PAMPHLET_NUTRITION = 'https://res2.yourwebsite.life/res/62f173898d9d30000fa9b6b9/62f324a98b3ec5000e69cdd5'
PAMPHLET_TEXT = {PAMPHLET_HEALTH: 'Download the health assessment pamphlet',
                 PAMPHLET_NUTRITION: 'Download the nutrition consultation pamphlet'}
RECIPE_DRIVE = 'https://drive.google.com/drive/folders/1gd1SYQlyzjPkBetDiqH9II4pzZ_H9Nxt'
VIMEO = 'https://vimeo.com/737699204'
LIVE = 'https://lifepointechiropractic.com'

# ---------------------------------------------------------------- icons
I = 'width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICONS = {
 'spine':   f'<svg {I}><circle cx="12" cy="4" r="1.7"/><circle cx="12" cy="9.3" r="1.7"/><circle cx="12" cy="14.6" r="1.7"/><circle cx="12" cy="20" r="1.7"/></svg>',
 'hand':    f'<svg {I}><path d="M8 13V5.5a1.5 1.5 0 0 1 3 0V12"/><path d="M11 12V4.5a1.5 1.5 0 0 1 3 0V12"/><path d="M14 12V6a1.5 1.5 0 0 1 3 0v6"/><path d="M17 12v-1a1.5 1.5 0 0 1 3 0v4a7 7 0 0 1-7 7h-1a7 7 0 0 1-7-7v-2a1.5 1.5 0 0 1 3 0"/></svg>',
 'scan':    f'<svg {I}><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/></svg>',
 'leaf':    f'<svg {I}><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6C9.5 14.5 12 13 13 12"/></svg>',
 'arrows':  f'<svg {I}><line x1="12" y1="3" x2="12" y2="9"/><polyline points="9 6 12 3 15 6"/><line x1="12" y1="15" x2="12" y2="21"/><polyline points="9 18 12 21 15 18"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
 'foot':    f'<svg {I}><path d="M10 21c-2.6 0-4.2-2-4.2-5 0-4 2-7.5 4.2-7.5s4.2 3.5 4.2 7.5c0 3-1.6 5-4.2 5Z"/><circle cx="16.5" cy="6.5" r="1"/><circle cx="14" cy="4.5" r="1"/><circle cx="11" cy="3.8" r="1"/></svg>',
 'clip':    f'<svg {I}><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4a3 3 0 0 1 6 0"/><line x1="9" y1="10" x2="15" y2="10"/><line x1="9" y1="14" x2="15" y2="14"/><line x1="9" y1="18" x2="13" y2="18"/></svg>',
 'shield':  f'<svg {I}><path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10Z"/><polyline points="9 11.5 11.2 13.7 15.5 9.4"/></svg>',
 'heart':   f'<svg {I}><path d="M19.5 12.6 12 20l-7.5-7.4a5 5 0 1 1 7.1-7.1l.4.3.4-.3a5 5 0 1 1 7.1 7.1Z"/></svg>',
 'phone':   f'<svg {I}><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.8a2 2 0 0 1-.4 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.9.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>',
 'mail':    f'<svg {I}><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
 'fax':     f'<svg {I}><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8" rx="1"/></svg>',
 'pin':     f'<svg {I}><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
 'clock':   f'<svg {I}><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15.5 13.5"/></svg>',
 'download':f'<svg {I}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
 'arrow':   f'<svg {I} width="18" height="18"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
 'users':   f'<svg {I}><circle cx="9" cy="8" r="3.5"/><path d="M2.5 21a6.5 6.5 0 0 1 13 0"/><circle cx="17.5" cy="9.5" r="2.5"/><path d="M16.5 15.2a5 5 0 0 1 5 4.8"/></svg>',
 'play':    f'<svg {I}><circle cx="12" cy="12" r="9"/><polygon points="10 8.5 16 12 10 15.5" fill="currentColor" stroke="none"/></svg>',
 'facebook': '<svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.1c0-.9.3-1.5 1.6-1.5h1.3V4.9c-.2 0-1-.1-1.9-.1-1.9 0-3.2 1.2-3.2 3.3V11H8.5v3h2.8v7h2.2z"/></svg>',
 'instagram': '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></svg>',
}

def icon(name, cls='card__icon'):
    return f'<div class="{cls}">{ICONS[name]}</div>'

# ---------------------------------------------------------------- chrome
NAV = [
    ('About', 'about.html'),
    ('Services &amp; products', 'services.html'),
    ('Success stories', 'success-stories.html'),
    ('New patients', 'new-patients.html'),
    ('Recipe book', 'recipe-book.html'),
    ('Contact', 'contact.html'),
]

def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Lato:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/site.css">
</head>'''

def header(active):
    links = []
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ''
        links.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f'''
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap site-header__bar">
    <a class="site-header__logo" href="index.html" aria-label="Lifepointe Chiropractic and Wellness Center — home">
      <img src="assets/logo-full-color.svg" alt="Lifepointe Chiropractic and Wellness Center" width="180" height="61">
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
      <span class="visually-hidden">Menu</span>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>{''.join(links)}</ul>
    </nav>
    <div class="site-header__cta">
      <a class="btn btn--primary btn--sm" href="contact.html#appointment">Request an appointment</a>
    </div>
  </div>
</header>'''

def cta_band(heading="Don&rsquo;t wait any longer to get relief from your pain.",
             sub="Call, or send a request and a member of our team will reach out to you soon."):
    return f'''
<section class="section section--navy on-dark" aria-label="Request an appointment">
  <div class="wrap center">
    <h2 class="display-2 measure-center">{heading}</h2>
    <p class="lede measure-center">{sub}</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--primary" href="contact.html#appointment">Request an appointment</a>
      <a class="btn btn--ghost" href="{PHONE_TEL}">Call {PHONE}</a>
    </div>
  </div>
</section>'''

def footer():
    return f'''
<footer class="site-footer on-dark">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <a class="site-footer__logo" href="index.html" aria-label="Lifepointe Chiropractic — home">
          <img src="assets/logo-reversed.svg" alt="Lifepointe Chiropractic and Wellness Center" width="190" height="63">
        </a>
        <p class="site-footer__tagline">Family wellness and chiropractic care for every age &mdash; serving Clarkston since 2001.</p>
        <div class="social-row">
          <a href="{FACEBOOK}" aria-label="Lifepointe on Facebook">{ICONS['facebook']}</a>
          <a href="{INSTAGRAM}" aria-label="Lifepointe on Instagram">{ICONS['instagram']}</a>
        </div>
      </div>
      <nav aria-label="Footer">
        <h2>Explore</h2>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="services.html">Services &amp; products</a></li>
          <li><a href="success-stories.html">Success stories</a></li>
          <li><a href="new-patients.html">New patients</a></li>
          <li><a href="recipe-book.html">Recipe book</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </nav>
      <div>
        <h2>Visit</h2>
        <ul>
          <li><a href="{MAPS}">{ADDRESS}</a></li>
          <li><a href="{PHONE_TEL}">{PHONE}</a></li>
          <li>Fax: {FAX}</li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
      <div>
        <h2>Office hours</h2>
        <ul>
          <li>Mon, Wed, Thu: 7:30&ndash;11:30am, 2:30&ndash;6pm</li>
          <li>Tue: 2:30&ndash;6pm</li>
          <li>Fri&ndash;Sun: closed</li>
        </ul>
      </div>
    </div>
    <div class="site-footer__legal">
      <span>&copy; <span data-year>2026</span> Lifepointe Chiropractic and Wellness Center. All rights reserved.</span>
      <span><a href="{LIVE}/privacy-policy">Privacy policy</a> &nbsp;&middot;&nbsp; <a href="{LIVE}/accessibility-statement">Accessibility statement</a></span>
    </div>
  </div>
</footer>
<script src="js/site.js"></script>
</html>'''

def page(fname, title, desc, active, body):
    html = head(title, desc) + '\n<body>' + header(active) + f'\n<main id="main">{body}</main>' + footer() + '\n</body>'
    # </html> is emitted by footer(); fix ordering
    html = html.replace('</html>\n</body>', '</body>\n</html>')
    with open(os.path.join(OUT, fname), 'w') as f:
        f.write(html)
    print('wrote', fname)

def page_hero(eyebrow, h1, lede=''):
    lede_html = f'<p class="lede">{lede}</p>' if lede else ''
    return f'''
<section class="page-hero on-dark">
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1 class="display-page">{h1}</h1>
    {lede_html}
  </div>
</section>'''

V = '<span class="vertebra" aria-hidden="true"></span>'

# ================================================================ INDEX
services_cards = [
    ('spine', 'Specific spinal adjustments', 'Gentle, precise adjustments to improve function and help the body express optimal health.'),
    ('hand',  'Licensed massage therapy', 'Improved circulation, reduced stress, and adjustments that hold longer.'),
    ('scan',  'On-premise digital X-ray', 'High-quality digital X-ray, right in the office, when your exam calls for it.'),
    ('leaf',  'Nutrition &amp; sensitivity testing', 'Personal nutritional consultations plus food allergy, microbiome, and metabolic testing.'),
    ('arrows','Cervical &amp; lumbar traction', 'Relieves pressure on the spine and helps align the vertebrae.'),
    ('foot',  'Custom-made foot orthotics', 'Designed to fit the specific contours of your feet.'),
]
cards_html = '\n'.join(
    f'''<a class="card card--link" href="services.html">
      {icon(ic)}
      <h3 class="display-3">{t}</h3>
      <p>{d}</p>
      <p class="card__more">Learn more &rarr;</p>
    </a>''' for ic, t, d in services_cards)

quotes_home = [
    ('After 3 weeks, my headaches are virtually gone! My head has not felt this clear in years!', 'Deb C.', 'Headaches &amp; migraines'),
    ('I had low-grade pain for 6&ndash;8 months with a loss of mobility&hellip; my back is the best it has been in 20 years!', 'Mike A.', 'Back pain'),
    ('I can breathe normally now, and have not used an inhaler since my first adjustment &mdash; 2&frac12; years now!', 'Gail H.', 'Allergies &amp; asthma'),
]
quotes_html = '\n'.join(
    f'''<figure class="quote">
      <blockquote><p>{q}</p></blockquote>
      <footer>{a} <span>{c} &middot; Lifepointe patient</span></footer>
    </figure>''' for q, a, c in quotes_home)

index_body = f'''
<section class="section" aria-labelledby="hero-h">
  <div class="wrap grid-2">
    <div>
      <span class="eyebrow rise">Family chiropractic &middot; Clarkston, Michigan</span>
      <h1 id="hero-h" class="display-1 rise rise-2">Health comes from within.<br>We clear the way.</h1>
      <p class="lede rise rise-3">Your body is built to heal itself &mdash; our job is to remove what&rsquo;s interfering. Since 2001, Lifepointe has cared for Clarkston families at every age, from newborns just minutes old to the most experienced members of our community.</p>
      <div class="btn-row rise rise-4 mt-15">
        <a class="btn btn--primary" href="contact.html#appointment">Request an appointment</a>
        <a class="btn btn--ghost" href="new-patients.html">What to expect</a>
      </div>
      <div class="badge-row rise rise-4 mt-2">
        <span class="badge">{ICONS['shield']} In-network with BCBS, Medicare &amp; VA</span>
        <span class="badge">{ICONS['users']} All ages welcome</span>
      </div>
    </div>
    <div class="hero-media rise rise-3">
      <figure class="photo">
        <img src="assets/photo-adjustment.jpg" alt="A chiropractor examining a patient&rsquo;s spine and posture by hand" width="1396" height="930">
      </figure>
      <div class="photo-chip">Serving Clarkston for 25 years<span>Est. July 2001</span></div>
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
      <a class="btn btn--ghost" href="about.html#chiropractic-care">Learn about chiropractic care</a>
    </div>
    <figure class="photo">
      <img src="assets/photo-stretch.jpg" alt="A person stretching comfortably at home, arms extended" width="1920" height="1281" loading="lazy">
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
      <a class="btn btn--primary" href="services.html">See all services &amp; products</a>
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="stories-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Patient stories</span>
    <h2 id="stories-h" class="display-2">Real words from real patients</h2>
    <p class="lede measure mb-2">Fifteen categories of success stories, in our patients&rsquo; own words.</p>
    <div class="grid-3">
      {quotes_html}
    </div>
    <div class="btn-row mt-2">
      <a class="btn btn--ghost" href="success-stories.html">Read more success stories</a>
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
      <a class="btn btn--ghost" href="new-patients.html">The full first-visit guide</a>
    </div>
    <div class="card">
      {icon('clip')}
      <h3 class="display-3">Skip the waiting room</h3>
      <p>Fill out your forms ahead of time and email them to us before your first appointment.</p>
      <ul class="link-list">
        <li><a href="{FORM_ADULT}">Download adult new patient forms</a></li>
        <li><a href="{FORM_CHILD}">Download child new patient forms (under 12)</a></li>
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
      <table class="hours-table">
        <caption class="visually-hidden">Office hours by day</caption>
        <tr data-days="1"><th scope="row">Monday</th><td>7:30&ndash;11:30am &nbsp;&bull;&nbsp; 2:30&ndash;6:00pm</td></tr>
        <tr data-days="2"><th scope="row">Tuesday</th><td>2:30&ndash;6:00pm</td></tr>
        <tr data-days="3"><th scope="row">Wednesday</th><td>7:30&ndash;11:30am &nbsp;&bull;&nbsp; 2:30&ndash;6:00pm</td></tr>
        <tr data-days="4"><th scope="row">Thursday</th><td>7:30&ndash;11:30am &nbsp;&bull;&nbsp; 2:30&ndash;6:00pm</td></tr>
        <tr data-days="5,6,0"><th scope="row">Fri&ndash;Sun</th><td>Closed</td></tr>
      </table>
    </div>
    <div class="card-stack">
      <div class="card">
        {icon('pin')}
        <h3 class="display-3">Lifepointe Chiropractic &amp; Wellness Center</h3>
        <p>{ADDRESS}</p>
        <a class="btn btn--ghost btn--sm" href="{MAPS}">Get directions</a>
      </div>
      <div class="card">
        {icon('shield')}
        <h3 class="display-3">Insurance</h3>
        <p>We are in-network with <strong>Blue Cross Blue Shield, Medicare, Medicare Advantage,</strong> and <strong>Veterans Affairs</strong>. Other policies are accepted out-of-network.</p>
      </div>
    </div>
  </div>
</section>

</div>
{cta_band()}'''

page('index.html',
     'Lifepointe Chiropractic &amp; Wellness Center | Clarkston, MI',
     'Family chiropractic and wellness care in Clarkston, MI since 2001. Gentle adjustments, massage therapy, digital X-ray, and nutrition — for every age.',
     None, index_body)

# ================================================================ ABOUT
about_body = page_hero('About us', 'The practice of our dreams',
    'Caring for our patients for life &mdash; with the emphasis on the people we take care of, not just their symptoms.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="greg-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Meet the doctor</span>
    <h2 id="greg-h" class="display-2">Dr. Greg Ramboer, DC</h2>
    <div class="grid-2 grid--top">
      <div>
        <p>I opened Lifepointe Chiropractic and Wellness Center in July of 2001. Our mission, in a nutshell, is to teach our community that all health comes from within &mdash; and that you already have everything it takes to be truly healthy, happy, and well. This inner health potential lacks its full expression when it&rsquo;s interfered with. That&rsquo;s where we fit into the picture: our role is to determine whether you have this interference, and if so, to help you reduce it for life.</p>
        <p>Our practice is family based &mdash; we adjust people of all ages, from newborns just a few minutes old to the very wise and experienced members of our community. We love what we do, and we love to teach and share what we&rsquo;ve learned.</p>
        <a class="btn btn--ghost btn--sm" href="{VIMEO}">Watch: inside Lifepointe</a>
      </div>
      <div class="card">
        <h3 class="display-3">Background</h3>
        <ul class="list-tight">
          <li>Originally from Ridgetown, Ontario, Canada</li>
          <li>Bachelor of Human Kinetics with Honors in Applied Kinesiology, University of Windsor</li>
          <li>Doctor of Chiropractic, Logan College of Chiropractic, 2000</li>
          <li>Founded Lifepointe in Clarkston, July 2001</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="team-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">The team</span>
    <h2 id="team-h" class="display-2">The people who&rsquo;ll take care of you</h2>
    <div>
      <div class="card measure">
        {icon('hand')}
        <h3 class="display-3">Kaitlin Crocker, LMT</h3>
        <p>Licensed massage therapist, graduate of Irene&rsquo;s Myomassology Institute in Southfield, Michigan. Kaitlin specializes in therapeutic massage techniques and holds certifications in multiple modalities &mdash; with a particular focus on the neck and feet, areas she finds essential for overall relaxation and well-being. Before massage, she spent eight years as a head chef; off the table you&rsquo;ll find her kayaking, reading, or relaxing with her cat.</p>
      </div>
    </div>
    <div class="badge-row mt-2">
      <span class="badge">{ICONS['shield']} Michigan Association of Chiropractors</span>
      <span class="badge">{ICONS['heart']} International Chiropractic Pediatrics Association</span>
      <span class="badge">{ICONS['heart']} ICA Council on Chiropractic Pediatrics</span>
      <span class="badge">{ICONS['users']} Clarkston Chamber of Commerce</span>
    </div>
  </div>
</section>

<section class="section" id="chiropractic-care" aria-labelledby="care-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">What is chiropractic?</span>
    <h2 id="care-h" class="display-2">A drug-free approach with the nervous system at the center</h2>
    <div class="grid-2 grid--top">
      <div>
        <p>Chiropractic is a healthcare profession focused on the health of the musculoskeletal and nervous systems. It&rsquo;s a drug-free approach that looks to establish and maintain proper posture and biomechanics, and to alleviate the manifestation of stress on the body &mdash; based on the scientific knowledge that the human body is a self-healing, self-regulating organism, always striving to heal as long as it has the right raw materials and no interference.</p>
        <p>Many people think we are &ldquo;back pain&rdquo; doctors. In reality, we focus on nervous system function &mdash; the nervous system just happens to be housed inside the spine. Through this network of nerves, your brain constantly coordinates the entire body. It&rsquo;s our job to ensure the messages traveling up and down the spine can do so without disruption.</p>
      </div>
      <div>
        <p>While many people first come in because an issue is limiting the life they want to live, chiropractic is not a treatment for any specific disease. Our goal is to get to the root cause of your symptoms &mdash; and by addressing root causes, symptoms begin to go away on their own.</p>
        <p>True spinal correction takes repetition, time, and energy, so we give our patients an active role in supporting care at home. And beyond correction, a wellness program of maintenance adjustments has been consistently correlated with decreased injury rates and pain, normalized blood pressure, increased energy, better immune function, and better sleep &mdash; at every stage of life.</p>
      </div>
    </div>
  </div>
</section>

</div>
{cta_band()}'''

page('about.html',
     'About Us | Lifepointe Chiropractic &amp; Wellness Center',
     'Meet Dr. Greg Ramboer and the Lifepointe team — family-based chiropractic care in Clarkston since 2001.',
     'about.html', about_body)

# ================================================================ SERVICES
SERVICES = [
    ('spine',  'Specific spinal adjustments', 'To improve function and help the body express optimal health.', None),
    ('spine',  'A variety of techniques', 'Including Diversified, Activator, Logan Basic, Thompson, and Webster.', None),
    ('arrows', 'Cervical &amp; lumbar traction', 'Relieves pressure on the spine and helps to align the vertebrae.', None),
    ('scan',   'On-premise digital X-ray facility', 'High-quality digital X-ray services for a variety of purposes.', None),
    ('clip',   'Complete computerized health assessments', 'A comprehensive picture of your health.', PAMPHLET_HEALTH),
    ('leaf',   'Personal nutritional consultations', 'Diabetes, autoimmune conditions, autism spectrum disorders, weight loss, and more.', PAMPHLET_NUTRITION),
    ('leaf',   'Food allergy &amp; sensitivity testing', 'Individualized microbiome and metabolic testing.', None),
    ('hand',   'Licensed massage therapy', 'Improved circulation, reduced stress levels, and more.', None),
    ('foot',   'Custom-made foot orthotics', 'Designed to fit the specific contours of your feet.', None),
]
svc_cards = '\n'.join(
    f'''<div class="card">
      {icon(ic)}
      <h3 class="display-3">{t}</h3>
      <p>{d}</p>
      {f'<p><a href="{pdf}">{ICONS["download"]}&nbsp; {PAMPHLET_TEXT[pdf]}</a></p>' if pdf else ''}
    </div>''' for ic, t, d, pdf in SERVICES)

PRODUCTS = [
    'Innate Choice D Sufficiency (Vitamin D3)', 'Innate Choice Probiotic Sufficiency',
    'Innate Choice Omega Sufficiency (professional-grade fish oil)', 'Innate Choice Vita Sufficiency (multivitamin)',
    'Whole-food-based Vitamin C', 'Lumbar (low back) support pillows', 'Cervical (neck) support pillows',
    'Biofreeze', 'Ice packs', 'Challenge boards',
]
prod_items = '\n'.join(f'<li>{p}</li>' for p in PRODUCTS)

services_body = page_hero('Services &amp; products', 'Everything under one roof',
    'A modern facility known for its range of chiropractic techniques and the wellness services that support them.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="svc-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Services offered</span>
    <h2 id="svc-h" class="display-2">Care built around your exam, not a menu</h2>
    <div class="grid-3">
      {svc_cards}
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="prod-h">
  {V}
  <div class="wrap grid-2 grid--top">
    <div>
      <span class="eyebrow">Available products</span>
      <h2 id="prod-h" class="display-2">Stocked in our office</h2>
      <ul class="list-tight">
        {prod_items}
      </ul>
    </div>
  </div>
</section>

</div>
{cta_band()}'''

page('services.html',
     'Services &amp; Products | Lifepointe Chiropractic &amp; Wellness Center',
     'Spinal adjustments, massage therapy, digital X-ray, traction, nutrition consultations, sensitivity testing, and custom orthotics in Clarkston, MI.',
     'services.html', services_body)

# ================================================================ SUCCESS STORIES
CATEGORIES = [
    ('Allergies &amp; asthma', '#allergies-asthma'), ('Back pain', '#back-pain'),
    ('Children', f'{LIVE}/patient-success-stories/children-chiropractic-treatment'),
    ('Chronic pain &amp; fatigue', f'{LIVE}/patient-success-stories/chronic-pain-fatigue-care'),
    ('Depression &amp; anxiety', f'{LIVE}/patient-success-stories/depression-anxiety-care'),
    ('Digestive issues', f'{LIVE}/patient-success-stories/digestive-issues-treatment'),
    ('Disc herniations', f'{LIVE}/patient-success-stories/disc-herniation-treatment'),
    ('Extremity pain', f'{LIVE}/patient-success-stories/extremity-pain-care'),
    ('Fertility &amp; female issues', '#fertility'),
    ('Headaches &amp; migraines', '#headaches'),
    ('Immune function', f'{LIVE}/patient-success-stories/immune-function-treatment'),
    ('Neck pain', f'{LIVE}/patient-success-stories/neck-pain-care'),
    ('Optimal health', f'{LIVE}/patient-success-stories/optimal-health-treatment'),
    ('Scoliosis', f'{LIVE}/patient-success-stories/scoliosis-treatment'),
    ('Words from our little ones', '#little-ones'),
]
def chip(label, href):
    if href.startswith('http'):
        return (f'<li><a class="chip chip--ext" href="{href}" target="_blank" rel="noopener">{label}'
                f'<span class="visually-hidden"> (opens the current live site)</span></a></li>')
    return f'<li><a class="chip" href="{href}">{label}</a></li>'
chips = '\n'.join(chip(label, href) for label, href in CATEGORIES)

def quote_group(anchor, eyebrow, heading, quotes, alt=False):
    qs = '\n'.join(
        f'''<figure class="quote">
          <blockquote><p>{q}</p></blockquote>
          <footer>{a} <span>Lifepointe patient</span></footer>
        </figure>''' for q, a in quotes)
    cls = 'section section--card' if alt else 'section'
    return f'''
<section class="{cls}" id="{anchor}" aria-labelledby="{anchor}-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h2 id="{anchor}-h" class="display-2">{heading}</h2>
    <div class="grid-3 mt-15">
      {qs}
    </div>
  </div>
</section>'''

stories_body = page_hero('Success stories', 'In our patients&rsquo; own words',
    'Select a topic to read testimonials from our patients &mdash; fifteen categories and counting.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="cats-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Browse by topic</span>
    <h2 id="cats-h" class="display-2">What brought them in</h2>
    <ul class="chip-grid mt-15">
      {chips}
    </ul>
  </div>
</section>
''' + quote_group('back-pain', 'Back pain', 'Moving again, without the meds', [
    ('I had low-grade pain for 6&ndash;8 months with a loss of mobility&hellip; my back is the best it has been in 20 years!', 'Mike A.'),
    ('My lower back would hurt so bad that I couldn&rsquo;t sit, stand or walk&hellip; my back is feeling great!', 'Ryan H.'),
    ('Because of the severity of my back, I was told there was no hope&hellip; What a difference chiropractors make!', 'Bill L.'),
], alt=True) + quote_group('headaches', 'Headaches &amp; migraines', 'Clear heads, back to daily life', [
    ('After 3 weeks, my headaches are virtually gone! My head has not felt this clear in years!', 'Deb C.'),
    ('I am now free to enjoy my husband and children instead of hiding in a dark room.', 'Carmen L.'),
    ('I had been suffering from headaches, sometimes migraines, for 7 years&hellip; I have not had ANY headaches!', 'Mary R.'),
]) + quote_group('fertility', 'Fertility &amp; female issues', 'Growing families', [
    ('My husband and I had been trying to get pregnant when my cousin suggested Lifepointe&hellip; Two months after starting care, we got pregnant!', 'Leigh G.'),
    ('I had 2 miscarriages in 6 months&hellip; We decided to see a chiropractor&hellip; I&rsquo;m 16 weeks pregnant &mdash; with twins! Using no fertility drugs!', 'Tamara S.'),
], alt=True) + quote_group('allergies-asthma', 'Allergies &amp; asthma', 'Breathing easier', [
    ('I can breathe normally now, and have not used an inhaler since my first adjustment &mdash; 2&frac12; years now!', 'Gail H.'),
]) + quote_group('little-ones', 'Words from our little ones', 'The littlest patients', [
    ('Chiropractic is good for everyone, people should try it! I feel much better, I don&rsquo;t miss as much school, and I get better faster when I&rsquo;m sick.', 'Larissa'),
], alt=True) + f'''
<section class="section" aria-label="Leave a review">
  {V}
  <div class="wrap center">
    <p class="lede measure-center">Has Lifepointe made a difference for you?</p>
    <a class="btn btn--ghost" href="{FACEBOOK}">Leave a review</a>
  </div>
</section>
</div>
{cta_band()}'''

page('success-stories.html',
     'Patient Success Stories | Lifepointe Chiropractic &amp; Wellness Center',
     'Real testimonials from Lifepointe patients — back pain, headaches, allergies, fertility, pediatric care, and more.',
     'success-stories.html', stories_body)

# ================================================================ NEW PATIENTS
newpt_body = page_hero('New patients', 'Your first visit, step by step',
    'Our examination procedures are geared toward detecting and correcting vertebral subluxation &mdash; selected specifically for your spine and nervous system health.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="steps-h">
  {V}
  <div class="wrap grid-2 grid--top">
    <div>
      <span class="eyebrow">What to expect</span>
      <h2 id="steps-h" class="display-2">A first visit that&rsquo;s measured, not rushed</h2>
      <p>Your exam gives us a scientific baseline &mdash; much more accurate than depending on &ldquo;how you feel&rdquo; on any given day &mdash; so we can measure your progress as your spine corrects and your nervous system function improves.</p>
      <ol class="steps mt-15">
        <li class="step">
          <div><h3>Forms before you arrive</h3><p>Download your forms below and email them back to us &mdash; and skip the waiting room.</p></div>
        </li>
        <li class="step">
          <div><h3>Spinal &amp; nervous system exam</h3><p>Hands-on palpation plus specialized tests: balance scales, posture evaluation, range-of-motion measurements, and orthopedic tests.</p></div>
        </li>
        <li class="step">
          <div><h3>X-rays, only if needed</h3><p>Depending on your age and situation. X-rays show the position of the spinal bones, the level of degeneration present, and the areas that need precise adjustment &mdash; we skip them for pregnancy, most young children, and anyone with recent usable films.</p></div>
        </li>
        <li class="step">
          <div><h3>Your Report of Findings</h3><p>We sit down and explain what every test means, what we found, and the care plan we recommend &mdash; before any treatment begins.</p></div>
        </li>
      </ol>
    </div>
    <div class="card-stack card-stack--sticky">
      <div class="card">
        {icon('download')}
        <h3 class="display-3">New patient forms</h3>
        <p>Print and bring them, or fill them out on a computer and email them to <a href="mailto:{EMAIL}">{EMAIL}</a> before your appointment.</p>
        <ul class="link-list">
          <li><a href="{FORM_ADULT}">Download adult new patient forms</a></li>
          <li><a href="{FORM_CHILD}">Download child new patient forms (under 12)</a></li>
        </ul>
      </div>
      <div class="card">
        {icon('shield')}
        <h3 class="display-3">Insurance</h3>
        <p>In-network with Blue Cross Blue Shield, Medicare, Medicare Advantage, and Veterans Affairs; other policies accepted out-of-network. Questions? <a href="{PHONE_TEL}">Call {PHONE}</a>.</p>
      </div>
    </div>
  </div>
</section>

</div>
{cta_band("Ready for your first visit?", "Request a time that works for your family and we&rsquo;ll confirm it with you.")}'''

page('new-patients.html',
     'New Patients | Lifepointe Chiropractic &amp; Wellness Center',
     'What to expect at your first Lifepointe visit — exam, X-rays if needed, and your Report of Findings — plus downloadable new patient forms.',
     'new-patients.html', newpt_body)

# ================================================================ RECIPE BOOK
STAPLES = [
    ('Avocado oil'), ('Arrowroot starch'), ('Coconut flour'), ('Full-fat coconut milk'),
    ('Sea salt'), ('Shredded coconut flakes'), ('Vanilla extract'),
]
staple_items = '\n'.join(f'<li>{s}</li>' for s in STAPLES)

recipe_body = page_hero('Healthy recipe book', 'From our kitchen to yours',
    'Simple, tasty, and wholesome recipes that promote vibrant health and healing &mdash; from Dr.&nbsp;Greg.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="recipes-h">
  {V}
  <div class="wrap grid-2 grid--top">
    <div>
      <span class="eyebrow">Healthy for Life</span>
      <h2 id="recipes-h" class="display-2">Wholesome recipes, zero inflammatory foods</h2>
      <p>Every recipe avoids inflammatory foods like refined sugar, grain, dairy, and processed food. If you see our logo next to an ingredient, it can be purchased right here at our office; for other items, links inside the recipes point to the same brands we use in our own home.</p>
      <p>And if you see a star next to a recipe &mdash; those are our Ramboer Family Favorites!</p>
      <a class="btn btn--primary" href="{RECIPE_DRIVE}">Open the recipe book</a>
    </div>
    <div class="card">
      {icon('leaf')}
      <h3 class="display-3">Our staple ingredients</h3>
      <p>A few favorites always in our kitchen:</p>
      <ul class="list-tight">
        {staple_items}
      </ul>
      <p class="hint">As an Amazon Associate, we earn from qualifying purchases &mdash; brand links are inside the recipe book.</p>
    </div>
  </div>
</section>

</div>
{cta_band()}'''

page('recipe-book.html',
     'Healthy Recipe Book | Lifepointe Chiropractic &amp; Wellness Center',
     'The Lifepointe Healthy for Life recipe book — simple, wholesome recipes free of refined sugar, grain, dairy, and processed food.',
     'recipe-book.html', recipe_body)

# ================================================================ CONTACT
contact_body = page_hero('Contact', 'Keep in touch',
    'Call, email, stop by, or send a request &mdash; a member of our team will reach out to you soon.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="reach-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Reach us</span>
    <h2 id="reach-h" class="display-2">Every way to say hello</h2>
    <div class="grid-4 mt-15">
      <div class="card">
        {icon('phone')}
        <h3 class="display-3">Call us</h3>
        <p><a href="{PHONE_TEL}">{PHONE}</a></p>
      </div>
      <div class="card">
        {icon('mail')}
        <h3 class="display-3">Email us</h3>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div class="card">
        {icon('fax')}
        <h3 class="display-3">Fax</h3>
        <p>{FAX}</p>
      </div>
      <div class="card">
        {icon('pin')}
        <h3 class="display-3">Find us</h3>
        <p>{ADDRESS}</p>
        <p><a href="{MAPS}">Get directions &rarr;</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section section--card" id="appointment" aria-labelledby="appt-h">
  {V}
  <div class="wrap grid-2 grid--top">
    <div>
      <span class="eyebrow">Request an appointment</span>
      <h2 id="appt-h" class="display-2">We&rsquo;d love to hear from you</h2>
      <p>Send us a message using this form and a member of our team will reach out to you soon. Prefer the phone? <a href="{PHONE_TEL}">Call {PHONE}</a> during office hours.</p>
      <table class="hours-table mt-15">
        <caption class="visually-hidden">Office hours by day</caption>
        <tr data-days="1"><th scope="row">Monday</th><td>7:30&ndash;11:30am &nbsp;&bull;&nbsp; 2:30&ndash;6:00pm</td></tr>
        <tr data-days="2"><th scope="row">Tuesday</th><td>2:30&ndash;6:00pm</td></tr>
        <tr data-days="3"><th scope="row">Wednesday</th><td>7:30&ndash;11:30am &nbsp;&bull;&nbsp; 2:30&ndash;6:00pm</td></tr>
        <tr data-days="4"><th scope="row">Thursday</th><td>7:30&ndash;11:30am &nbsp;&bull;&nbsp; 2:30&ndash;6:00pm</td></tr>
        <tr data-days="5,6,0"><th scope="row">Fri&ndash;Sun</th><td>Closed</td></tr>
      </table>
    </div>
    <div class="card card--form">
      <iframe src="{FORM_APPT}" title="Appointment request form" loading="lazy"></iframe>
      <script src="https://link.msgsndr.com/js/form_embed.js" async></script>
      <p class="form-fallback">If the form doesn&rsquo;t load, email <a href="mailto:{EMAIL}?subject=Request%20an%20Appointment">{EMAIL}</a> or call <a href="{PHONE_TEL}">{PHONE}</a>.</p>
    </div>
  </div>
</section>

</div>'''

page('contact.html',
     'Contact &amp; Appointments | Lifepointe Chiropractic &amp; Wellness Center',
     'Contact Lifepointe Chiropractic in Clarkston, MI — request an appointment online or call (248) 623-6107.',
     'contact.html', contact_body)

print('done')
