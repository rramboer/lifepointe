"""Accessibility statement: the standard the site aims for, what it does, its known limits and
how to report a problem.

"What the site does" restates the accessibility floor in DESIGN.md. Keep the two in step: if
the floor changes, or a page stops meeting it, update this list and LAST_REVIEWED.
"""
from ..helpers import esc
from ..layout import V, page, page_hero

FILENAME = 'accessibility.html'
LAST_REVIEWED = 'October 2026'
WCAG_21 = 'https://www.w3.org/TR/WCAG21/'


def render(site):
    p = site.practice
    tel = esc('tel:' + p.phone.tel)
    phone = esc(p.phone.display)
    email = esc(p.email)
    email_link = esc('mailto:' + p.email)
    # With a booking_url, the contact page links to an online booking service on another site.
    if p.booking_url:
        other_sites = 'Facebook, Instagram, Google Maps and our online booking service'
    else:
        other_sites = 'Facebook, Instagram and Google Maps'

    body = page_hero('Accessibility', 'Accessibility statement',
                     'We want everyone to be able to use this website, including people who use a screen '
                     'reader, a keyboard, screen magnification or other assistive technology.',
                     f'Last reviewed {LAST_REVIEWED}') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="standard-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Our goal</span>
    <h2 id="standard-h" class="display-2">Working toward WCAG 2.1 AA</h2>
    <div class="measure mt-15">
      <p>We aim for this website to meet the <a href="{esc(WCAG_21)}">Web Content Accessibility Guidelines (WCAG) 2.1</a> at Level AA. These guidelines, from the World Wide Web Consortium (W3C), explain how to make web content more accessible to people with disabilities.</p>

      <h3 class="display-3 mt-2">What the site does</h3>
      <ul class="list-tight">
        <li>A &ldquo;Skip to main content&rdquo; link comes first on every page, for keyboard and screen reader users.</li>
        <li>You can reach every link and button with a keyboard, and the one in focus always shows a clear outline.</li>
        <li>Text and background colors meet the WCAG AA contrast levels.</li>
        <li>Pages are organized with headings, lists and landmarks (header, menu, main content and footer), so screen readers can move around them.</li>
        <li>Images have text descriptions. Purely decorative icons are hidden from screen readers.</li>
        <li>Icon-only links, such as Facebook and Instagram, have text labels for screen readers, and links to PDF files say &ldquo;(PDF)&rdquo;.</li>
        <li>The menu button tells screen readers whether the menu is open, and the Escape key closes it.</li>
        <li>The office hours tables tell screen readers which day is today.</li>
        <li>If your device is set to reduce motion, the site&rsquo;s animations and smooth scrolling are turned off.</li>
        <li>Pages fit screens as narrow as 320 pixels without scrolling sideways. In a desktop browser window 1280 pixels wide, that means you can zoom in up to 400%.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="limits-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Known limitations</span>
    <h2 id="limits-h" class="display-2">Where we know it falls short</h2>
    <div class="measure mt-15">
      <h3 class="display-3">New patient forms</h3>
      <p>The fillable PDF forms may not be fully accessible. Some screen readers and PDF apps may not read every field clearly, and the body diagram on the adult form isn&rsquo;t fillable. If the forms don&rsquo;t work for you, <a href="{tel}">call us at {phone}</a>. We&rsquo;ll help, or fill them in with you at the office.</p>

      <h3 class="display-3 mt-2">Other websites</h3>
      <p>Our recipe book is in Google Drive, and some links lead to {other_sites}. We don&rsquo;t control how accessible those sites are. If one of them doesn&rsquo;t work for you, please let us know.</p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="feedback-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Feedback</span>
    <h2 id="feedback-h" class="display-2">Tell us about a problem</h2>
    <div class="measure mt-15">
      <p>If something on this website is hard to use, or you need information from it in another way, please contact us:</p>
      <ul class="list-tight">
        <li>Call <a href="{tel}">{phone}</a></li>
        <li>Email <a href="{email_link}">{email}</a></li>
      </ul>
      <p>Tell us which page you were on, what you were trying to do and what went wrong. We&rsquo;ll do our best to get you the information you need and to fix the problem.</p>
    </div>
  </div>
</section>

</div>'''

    return page(site, FILENAME,
                f'Accessibility Statement | {p.name}',
                f'How the {p.name} website works toward WCAG 2.1 AA, its known limitations, '
                f'and how to tell us about a problem.',
                body)
