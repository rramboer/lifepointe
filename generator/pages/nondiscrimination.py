"""Nondiscrimination notice and notice of free language help: Section 1557 of the Affordable
Care Act, 45 CFR 92.10 and 92.11.

The practice bills Medicare, so these rules apply to it. Both notices must be at a conspicuous
location on the website: every page's footer links here and lists the languages
(layout.footer). They must also be posted in the office in at least 20-point sans-serif type:
printing this page gives that poster (css/site.css, "Printed notice"). The language notice also
goes on intake forms, the Notice of Privacy Practices and the other documents listed in
45 CFR 92.11(c)(5).

The notice of nondiscrimination follows HHS's 2024 sample notice and covers what 92.10(a)(1)
requires. A practice with fewer than 15 employees needs no Section 1557 coordinator or
grievance procedure (92.7, 92.8(c)), so it names the office instead. The English language-help
notice follows HHS's 2024 sample; the translations in data/language-help.json are HHS's own,
copied exactly. Never edit or machine-translate them.
"""
import re

from ..helpers import esc, language_anchor
from ..layout import V, page, page_hero

FILENAME = 'nondiscrimination.html'
LAST_UPDATED = 'October 2026'
# The relay service: dialing 711 connects TTY and other relay users anywhere in the US.
TTY = '711'
OCR_PORTAL = 'https://ocrportal.hhs.gov/ocr/portal/lobby.jsf'
OCR_FORMS = 'https://www.hhs.gov/ocr/complaints/index.html'


def fill(text, site, rtl):
    """A notice's text as HTML, with the practice's phone number and the relay number in its blanks.
    In right-to-left text, a bracketed run with Latin letters in it, such as "(TTY: {tty})", is kept
    in left-to-right order; otherwise it shows as "(711 :TTY)"."""
    phone = site.practice.phone
    number = f'<a href="{esc("tel:" + phone.tel)}" dir="ltr">{esc(phone.display)}</a>'
    html = esc(text)
    html = re.sub(r'\([^()]*[A-Za-z][^()]*\)', lambda m: f'<span dir="ltr">{m.group()}</span>', html) \
        if rtl else html
    return html.replace('{phone}', number).replace('{tty}', f'<span dir="ltr">{TTY}</span>')


def render(site):
    p = site.practice
    name = esc(p.name)
    tel = esc('tel:' + p.phone.tel)
    phone = esc(p.phone.display)
    email = esc(p.email)
    email_link = esc('mailto:' + p.email)
    url = esc(f'{p.site_url.removeprefix("https://")}/nondiscrimination')

    taglines = '\n'.join(
        f'''        <li id="{esc(language_anchor(t.lang))}" lang="{esc(t.lang)}" dir="{esc(t.dir)}">
          <h3 class="tagline__name">{esc(t.name)}</h3>
          <p>{fill(t.text, site, t.dir == 'rtl')}</p>
        </li>''' for t in site.language_help.languages)

    body = page_hero('Your rights', 'Nondiscrimination notice',
                     'We don&rsquo;t discriminate, and we offer free language help and free aids for people '
                     'with disabilities.',
                     f'Last updated {LAST_UPDATED}') + f'''
<div class="rail-wrap notice-print">

<section class="section" aria-labelledby="notice-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Notice of nondiscrimination</span>
    <h2 id="notice-h" class="display-2">Discrimination is against the law</h2>
    <div class="measure mt-15">
      <p>{name} complies with applicable federal civil rights laws and does not discriminate on the basis of race, color, national origin (including limited English proficiency and primary language), age, disability, or sex. {name} does not exclude people or treat them less favorably because of race, color, national origin, age, disability, or sex.</p>
      <p>{name}:</p>
      <ul class="list-tight">
        <li>Provides people with disabilities reasonable modifications and free appropriate auxiliary aids and services to communicate effectively with us, such as:
          <ul class="list-tight">
            <li>Qualified sign language interpreters</li>
            <li>Written information in other formats (large print, audio, accessible electronic formats, other formats)</li>
          </ul>
        </li>
        <li>Provides free language assistance services to people whose primary language is not English, which may include:
          <ul class="list-tight">
            <li>Qualified interpreters</li>
            <li>Information written in other languages, including electronic and written translated documents</li>
          </ul>
        </li>
      </ul>
      <p>We provide these free of charge and in a timely manner. If you need reasonable modifications, appropriate auxiliary aids and services, or language assistance services, call <a href="{tel}">{phone}</a> (TTY: {TTY}), email <a href="{email_link}">{email}</a>, or ask at the front desk.</p>
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="language-help-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Language help</span>
    <h2 id="language-help-h" class="display-2">Free language help and other formats</h2>
    <div class="measure mt-15">
      <p>ATTENTION: Free language assistance services are available to you. Appropriate auxiliary aids and services to provide information in accessible formats are also available free of charge. Call <a href="{tel}">{phone}</a> (TTY: {TTY}) or speak to your provider.</p>
      <ul class="taglines">
{taglines}
      </ul>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="complaint-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Complaints</span>
    <h2 id="complaint-h" class="display-2">If you believe we&rsquo;ve discriminated</h2>
    <div class="measure mt-15">
      <p>If you believe that {name} has failed to provide these services or discriminated in another way on the basis of race, color, national origin, age, disability, or sex, please tell us: call <a href="{tel}">{phone}</a>, email <a href="{email_link}">{email}</a>, or write to {name}, {esc(p.address)}.</p>
      <p>You can also file a civil rights complaint with the U.S. Department of Health and Human Services, Office for Civil Rights, electronically through the Office for Civil Rights Complaint Portal, available at <a class="url" href="{esc(OCR_PORTAL)}">{esc(OCR_PORTAL)}</a>, or by mail or phone at:</p>
      <p>U.S. Department of Health and Human Services<br>200 Independence Avenue, SW<br>Room 509F, HHH Building<br>Washington, D.C. 20201<br><span class="nowrap">1-800-368-1019</span>, <span class="nowrap">800-537-7697</span> (TDD)</p>
      <p>Complaint forms are available at <a class="url" href="{esc(OCR_FORMS)}">{esc(OCR_FORMS)}</a>.</p>
      <p>This notice is available at {name}&rsquo;s website: <span class="url">{url}</span>.</p>
    </div>
  </div>
</section>

</div>'''

    return page(site, FILENAME,
                f'Nondiscrimination Notice | {p.name}',
                f'{p.name} does not discriminate, and offers free language help and free aids for people with '
                f'disabilities. How to get them, and how to file a complaint.',
                body)
