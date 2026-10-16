"""Accessibility statement: the standard the site meets (WCAG 2.1 AA), what it does and how to
report a problem.

"What the site does" restates the accessibility floor in DESIGN.md. Keep the two in step: if
the floor changes, or a page stops meeting it, update this list and LAST_REVIEWED.
"""
from ..helpers import esc, page_href
from ..layout import V, page, page_hero
from . import nondiscrimination

FILENAME = 'accessibility.html'
LAST_REVIEWED = 'October 2026'
WCAG_21 = 'https://www.w3.org/TR/WCAG21/'


def render(site):
    p = site.practice
    tel = esc('tel:' + p.phone.tel)
    phone = esc(p.phone.display)
    email = esc(p.email)
    email_link = esc('mailto:' + p.email)
    nondiscrimination_link = esc(page_href(nondiscrimination.FILENAME))

    body = page_hero('Accessibility', 'Accessibility statement',
                     'We want everyone to be able to use this website, including people who use a screen '
                     'reader, a keyboard, screen magnification, or other assistive technology.',
                     f'Last reviewed {LAST_REVIEWED}') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="standard-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Our standard</span>
    <h2 id="standard-h" class="display-2">WCAG 2.1 Level AA</h2>
    <div class="measure mt-15">
      <p>This website meets the <a href="{esc(WCAG_21)}">Web Content Accessibility Guidelines (WCAG) 2.1</a> at Level AA. These guidelines, from the World Wide Web Consortium (W3C), explain how to make web content accessible to people with disabilities.</p>
      <p>We last tested every page in {LAST_REVIEWED}, with an automated checker and by hand: using only a keyboard, zoomed in and on narrow screens, and checking color contrast and text spacing.</p>

      <h3 class="display-3 mt-2">What the site does</h3>
      <ul class="list-tight">
        <li>A &ldquo;Skip to main content&rdquo; link comes first on every page, for keyboard and screen reader users.</li>
        <li>You can reach every link and button with a keyboard, and the one in focus always shows a clear outline.</li>
        <li>Text and background colors meet the WCAG AA contrast levels.</li>
        <li>Pages are organized with headings, lists, and landmarks (header, menu, main content, and footer), so screen readers can move around them.</li>
        <li>Images have text descriptions. Purely decorative icons are hidden from screen readers.</li>
        <li>Icon-only links, such as Facebook and Instagram, have text labels for screen readers, and links to PDF files say &ldquo;(PDF)&rdquo;.</li>
        <li>The menu button tells screen readers whether the menu is open, and the Escape key closes it.</li>
        <li>On phones, the Call and &ldquo;Request an appointment&rdquo; buttons stay at the bottom of the screen, and the page scrolls so they never cover the link or button you&rsquo;re on.</li>
        <li>The office hours tables tell screen readers which day is today.</li>
        <li>If your device is set to reduce motion, the site&rsquo;s animations and smooth scrolling are turned off.</li>
        <li>Pages fit screens as narrow as 320 pixels without scrolling sideways. In a desktop browser window 1280 pixels wide, that means you can zoom in up to 400%.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="feedback-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Feedback</span>
    <h2 id="feedback-h" class="display-2">Tell us about a problem</h2>
    <div class="measure mt-15">
      <p>If something on this website is hard to use, or you need information from it in another way, please contact us:</p>
      <ul class="list-tight">
        <li>Call <a href="{tel}">{phone}</a> (TTY users: call 711)</li>
        <li>Email <a href="{email_link}">{email}</a></li>
      </ul>
      <p>Tell us which page you were on, what you were trying to do, and what went wrong. We&rsquo;ll do our best to get you the information you need and to fix the problem.</p>
      <p>We provide auxiliary aids and services, such as information in large print or other formats, and language assistance free of charge. Our <a href="{nondiscrimination_link}">nondiscrimination notice</a> explains how to ask for them, and how to file a complaint.</p>
    </div>
  </div>
</section>

</div>'''

    return page(site, FILENAME,
                f'Accessibility Statement | {p.name}',
                f'How the {p.name} website meets WCAG 2.1 AA, and how to tell us about a problem.',
                body)
