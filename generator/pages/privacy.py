"""Privacy policy: how this website handles information, and where the Notice of Privacy
Practices fits in.

Every statement here must stay true of the site as built. It says the site has no cookies, no
analytics or tracking and no forms, that its pages load nothing from other sites, who hosts it,
and which other sites it links to. Changing any of those means updating this page and
LAST_UPDATED. The build stops if a page would load anything from another site or has a form
(checks.offsite_loads).

The Notice of Privacy Practices is its own page (privacy_notice.py). The last section here says
what it is and links to it.
"""
from ..helpers import esc, page_href
from ..layout import V, page, page_hero
from . import privacy_notice

FILENAME = 'privacy.html'
LAST_UPDATED = 'October 2026'

# GitHub's own pages on what it collects. The GitHub Pages one says, under "Data collection",
# that a visitor's IP address is logged and stored for security purposes.
GITHUB_PRIVACY = 'https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement'
GITHUB_PAGES_DATA = ('https://docs.github.com/en/pages/getting-started-with-github-pages/'
                     'what-is-github-pages#data-collection')
# The policies of the other sites the pages link to: Facebook and Instagram (Meta), and
# Google reviews, Google Maps, and Google Drive (Google).
META_PRIVACY = 'https://www.facebook.com/privacy/policy/'
GOOGLE_PRIVACY = 'https://policies.google.com/privacy'


def render(site):
    p = site.practice
    name = esc(p.name)
    tel = esc('tel:' + p.phone.tel)
    phone = esc(p.phone.display)
    email = esc(p.email)
    email_link = esc('mailto:' + p.email)
    notice_link = esc(page_href(privacy_notice.FILENAME))
    # With a booking_url, the contact page links to an online booking service: another
    # company's site that collects what people type into it. Name it among the outside links.
    # The /card redirect (generator/card.py) goes there too.
    if p.booking_url:
        how_to_book = ('To book a visit, you call, email, or use our online booking service, which is another '
                       'company&rsquo;s website. To ask a question, you call or email us.')
        booking_link = ', our online booking service'
        card_destination = 'our online booking service'
    else:
        how_to_book = 'To book a visit or ask a question, you call or email us.'
        booking_link = ''
        card_destination = 'our contact page'

    body = page_hero('Your privacy', 'Privacy policy',
                     'This website has no cookies, no analytics or tracking, and no forms. Here&rsquo;s what '
                     'that means, and how we handle what you share with us by phone or email.',
                     f'Last updated {LAST_UPDATED}') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="website-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">This website</span>
    <h2 id="website-h" class="display-2">How this website handles your information</h2>
    <div class="measure mt-15">
      <p>This website belongs to {name} (legal name {esc(p.legal_name)}), called &ldquo;we&rdquo; or &ldquo;us&rdquo; here. This notice covers the website only. Your medical information is covered by our <a href="{notice_link}">Notice of Privacy Practices</a>.</p>

      <h3 class="display-3 mt-2">No cookies, analytics, or tracking</h3>
      <p>This website doesn&rsquo;t use cookies, analytics, advertising, or tracking tools of any kind, and we don&rsquo;t keep a record of who visits. Everything its pages load, including pictures, fonts, and scripts, comes from this website itself, so reading a page sends nothing to Google, Facebook, or any company other than our web host (below). The site&rsquo;s scripts only change how pages look and work in your browser, such as opening the menu on small screens or taking people who scan the QR code on our business card to {card_destination}. They send nothing anywhere.</p>

      <h3 class="display-3 mt-2">No forms</h3>
      <p>There are no forms on this website, so it can&rsquo;t collect your name, contact details, or health information. {how_to_book} The new patient forms are PDF files that you download. This website doesn&rsquo;t receive anything you type into them: we only see a form when you bring it in or send it to us.</p>

      <h3 class="display-3 mt-2">Our web host</h3>
      <p>This website is hosted on GitHub Pages, a service of GitHub, Inc. Like any web server, GitHub&rsquo;s servers receive your device&rsquo;s IP address when you visit. The <a href="{esc(GITHUB_PAGES_DATA)}">GitHub Pages documentation</a> says that when a GitHub Pages site is visited, &ldquo;the visitor&rsquo;s IP address is logged and stored for security purposes.&rdquo; The <a href="{esc(GITHUB_PRIVACY)}">GitHub Privacy Statement</a> explains how GitHub handles that information.</p>

      <h3 class="display-3 mt-2">When you call or email us</h3>
      <p>If you call or email us, we receive what you choose to tell us, such as your name, phone number, email address, and the days and times that suit you. We use it to answer you and to schedule your care.</p>
      <p>Regular email isn&rsquo;t a fully secure way to send health information. When you email us to book, please share only your name, phone number, and preferred days and times. If you&rsquo;d rather not email your completed new patient forms, print them and bring them to your first visit. Health information you give us as a patient is covered by our Notice of Privacy Practices.</p>

      <h3 class="display-3 mt-2">Links to other websites</h3>
      <p>Some links take you to other companies&rsquo; websites: our Facebook and Instagram pages{booking_link}, our reviews on Google, directions in Google Maps, and our recipe book in Google Drive. Once you follow one of those links, that company&rsquo;s own privacy policy applies. Facebook and Instagram are covered by the <a href="{esc(META_PRIVACY)}">Meta Privacy Policy</a>, and Google reviews, Google Maps, and Google Drive by the <a href="{esc(GOOGLE_PRIVACY)}">Google Privacy Policy</a>.</p>

      <h3 class="display-3 mt-2">Children</h3>
      <p>This website doesn&rsquo;t collect personal information from anyone, children included. Information about a child&rsquo;s care that a parent or guardian gives us is covered by our Notice of Privacy Practices.</p>

      <h3 class="display-3 mt-2">Changes to this notice</h3>
      <p>If we change how this website handles information, we&rsquo;ll update this page and the &ldquo;Last updated&rdquo; date at the top.</p>

      <h3 class="display-3 mt-2">Questions</h3>
      <p>If you have a question about this notice or your privacy, please contact us:</p>
      <ul class="list-tight">
        <li>Call <a href="{tel}">{phone}</a></li>
        <li>Email <a href="{email_link}">{email}</a></li>
        <li>Write to {name}, {esc(p.address)}</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--card" id="notice-of-privacy-practices" aria-labelledby="npp-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Your medical information</span>
    <h2 id="npp-h" class="display-2">Notice of Privacy Practices</h2>
    <div class="measure mt-15">
      <p>Our HIPAA <a href="{notice_link}">Notice of Privacy Practices</a>, effective {privacy_notice.EFFECTIVE}, describes how medical information about you may be used and disclosed, and how you can get access to this information.</p>
      <p>You can also ask for a paper copy at any time. <a href="{tel}">Call us at {phone}</a> or ask at the front desk.</p>
    </div>
  </div>
</section>

</div>'''

    return page(site, FILENAME,
                f'Privacy Policy | {p.name}',
                f'How the {p.name} website handles your information: no cookies, no tracking, and no forms. '
                f'Plus how to get a copy of our Notice of Privacy Practices.',
                body)
