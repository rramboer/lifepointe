"""The chrome every page shares: head, header, footer, page hero, closing CTA band.

`base` goes in front of every link to the site's own files. '' keeps links relative to the
page, so a copy of the site works in any folder (such as the github.io preview). '/' makes
them root-absolute, for the 404 page, which GitHub Pages serves at whatever address was
missing, at any depth. Links to pages go through helpers.page_href, which leaves out .html.
"""
import hashlib
from functools import cache
from pathlib import Path

from . import seo
from .helpers import esc, page_href
from .hours import hours_summary
from .icons import svg

V = '<span class="vertebra" aria-hidden="true"></span>'
# The footer's legal links, as (page, link text). The build stops if a page here isn't one it makes.
LEGAL_LINKS = (('privacy.html', 'Privacy policy'),
               ('notice-of-privacy-practices.html', 'Notice of Privacy Practices'),
               ('accessibility.html', 'Accessibility statement'),
               ('nondiscrimination.html', 'Nondiscrimination notice'),
               ('good-faith-estimate.html', 'Good Faith Estimate'))


ROOT = Path(__file__).resolve().parent.parent


@cache
def versioned(path):
    """'css/site.css' -> 'css/site.css?v=<first 10 hex digits of the file's SHA-256>'. GitHub
    Pages lets browsers keep a file for 10 minutes, so right after a deploy a returning visitor
    could get the new page with the old stylesheet or script. The version changes whenever the
    file does, so the new page always fetches its own; a file that hasn't changed stays cached."""
    digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:10]
    return f'{path}?v={digest}'


# The latin font files every page draws its first screen with, fetched alongside the stylesheet
# rather than after it, so the text doesn't redraw in its fallback font first.
PRELOAD_FONTS = ('bricolage-grotesque-latin.woff2', 'lato-400-latin.woff2', 'lato-700-latin.woff2')


def _preloads(base):
    return '\n'.join(f'  <link rel="preload" href="{base}assets/fonts/{name}" as="font" type="font/woff2" crossorigin>'
                     for name in PRELOAD_FONTS)


def head(title, description, base='', extra=''):
    """extra is trusted HTML for the end of <head> (robots, canonical and sharing tags, JSON-LD)."""
    extra_html = f'\n  {extra}' if extra else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="color-scheme" content="only light">
  <meta name="theme-color" content="#ffffff">
  <link rel="icon" type="image/svg+xml" href="{base}assets/favicon.svg">
  <link rel="apple-touch-icon" href="{base}assets/apple-touch-icon.png">
{_preloads(base)}
  <link rel="stylesheet" href="{base}{versioned('css/site.css')}">{extra_html}
</head>'''


def header(site, active, base=''):
    """The sticky header. Wide windows show the menu, the phone number (widest only) and the
    appointment button. Narrower ones fold the menu behind a Menu button and keep a Call button
    and, above phone width, the appointment button in the bar; on phones those two live in the
    action bar at the bottom of the screen instead (action_bar)."""
    p = site.practice
    links = []
    for item in site.nav:
        if getattr(item, 'header', True) is False:
            continue
        current = ' aria-current="page"' if item.href == active else ''
        links.append(f'<li><a href="{esc(page_href(item.href, base))}"{current}>{esc(item.label)}</a></li>')
    name = esc(p.name)
    tel = esc('tel:' + p.phone.tel)
    phone = esc(p.phone.display)
    appointment = page_href('contact.html#appointment', base)
    return f'''
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap site-header__bar">
    <a class="site-header__logo" href="{page_href('index.html', base)}" aria-label="{name} — home">
      <img src="{base}assets/logo-full-color.svg" alt="{name}" width="180" height="61">
    </a>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>{''.join(links)}</ul>
      <div class="site-nav__actions">
        <a class="btn btn--primary" href="{appointment}">Request an appointment</a>
        <a class="btn btn--ghost" href="{tel}">{svg('phone')}Call {phone}</a>
      </div>
    </nav>
    <div class="site-header__actions">
      <a class="header-phone" href="{tel}">{svg('phone')}<span class="header-phone__label">Call </span><span class="header-phone__number">{phone}</span></a>
      <a class="btn btn--primary btn--sm site-header__cta" href="{appointment}">Request an appointment</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
        <svg class="nav-toggle__open" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
        <svg class="nav-toggle__close" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
        <span class="nav-toggle__label">Menu</span>
      </button>
    </div>
  </div>
</header>'''


def action_bar(site, base=''):
    """Phones only (css): Call and Request an appointment, fixed to the bottom of the screen so
    they are always one tap away. site.js slides it away while the closing call-to-action band
    or the contact page's appointment section is on screen, since those show the same two
    actions. It comes last in the page, after the footer, so it is last in the tab order."""
    p = site.practice
    return f'''
<nav class="action-bar" aria-label="Call or request an appointment">
  <a class="btn btn--ghost action-bar__call" href="{esc('tel:' + p.phone.tel)}">{svg('phone')}Call<span class="action-bar__number"> {esc(p.phone.display)}</span></a>
  <a class="btn btn--primary" href="{page_href('contact.html#appointment', base)}">Request an appointment</a>
</nav>'''


def page_hero(eyebrow, h1, lede='', meta='', actions=''):
    """Interior-page hero, on a light band. Arguments are trusted HTML written in the page
    module. meta is a short line under the lede, such as the date a legal page was last updated.
    actions is a row of buttons for pages where a visitor is ready to act (new patients,
    services). Its lines fade up on load one after another (.rise), like the home page's hero."""
    lede_html = f'\n    <p class="lede rise rise-3">{lede}</p>' if lede else ''
    meta_html = f'\n    <p class="page-hero__meta rise rise-4">{meta}</p>' if meta else ''
    actions_html = f'\n    <div class="btn-row page-hero__actions rise rise-4">{actions}</div>' if actions else ''
    return f'''
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow rise">{eyebrow}</span>
    <h1 class="display-page rise rise-2">{h1}</h1>{lede_html}{meta_html}{actions_html}
  </div>
</section>'''


def quote(testimonial, note=''):
    """A testimonial card: the patient's words, then their name. note is a line under the name,
    such as the category; plain text. No avatar: there will never be patient photos, and initials
    in a circle would look like one of the site's photo placeholders."""
    note_html = f'<span class="quote__note">{esc(note)}</span>' if note else ''
    return f'''<figure class="quote">
        <blockquote><p>{esc(testimonial.quote)}</p></blockquote>
        <figcaption class="quote__by">{esc(testimonial.author)}{note_html}</figcaption>
      </figure>'''


def cta_band(site, heading='Don&rsquo;t wait any longer to get relief from your pain.',
             sub='Call, or send a request, and a member of our team will reach out to you soon.', base=''):
    """Closing call-to-action band. heading and sub are trusted HTML."""
    phone = site.practice.phone
    return f'''
<section class="section section--navy cta-band on-dark" aria-label="Request an appointment">
  <div class="wrap center">
    <h2 class="display-2 measure-center">{heading}</h2>
    <p class="lede measure-center">{sub}</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--primary" href="{page_href('contact.html#appointment', base)}">Request an appointment</a>
      <a class="btn btn--ghost" href="{esc('tel:' + phone.tel)}">{svg('phone')}Call {esc(phone.display)}</a>
    </div>
  </div>
</section>'''


def footer(site, base=''):
    p = site.practice
    name = esc(p.name)
    explore = '\n'.join(
        f'          <li><a href="{esc(page_href(item.href, base))}">{esc(getattr(item, "footer_label", item.label))}</a></li>'
        for item in site.nav)
    hours = '\n'.join(f'          <li>{line}</li>' for line in hours_summary(site.hours))
    # "Clarkston, MI 48346" stays on one line (practice.json's format is "street, city, ST 12345")
    street, city, state_zip = p.address.rsplit(', ', 2)
    address = f'{esc(street)}, <span class="nowrap">{esc(city)}, {esc(state_zip)}</span>'
    legal = ' &nbsp;&middot;&nbsp; '.join(
        f'<a href="{esc(page_href(href, base))}">{esc(text)}</a>' for href, text in LEGAL_LINKS)
    return f'''
<footer class="site-footer on-dark">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <a class="site-footer__logo" href="{page_href('index.html', base)}" aria-label="{name} — home">
          <img src="{base}assets/logo-reversed.svg" alt="{name}" width="190" height="63">
        </a>
        <p class="site-footer__tagline">Family and sports chiropractic for every age &mdash; serving Clarkston since 2001.</p>
        <div class="social-row">
          <a href="{esc(p.social.facebook)}" aria-label="Lifepointe on Facebook">{svg('facebook')}</a>
          <a href="{esc(p.social.instagram)}" aria-label="Lifepointe on Instagram">{svg('instagram')}</a>
        </div>
      </div>
      <nav aria-label="Footer">
        <h2>Explore</h2>
        <ul>
{explore}
        </ul>
      </nav>
      <div>
        <h2>Visit</h2>
        <ul>
          <li><a href="{esc(p.maps_url)}">{address}</a></li>
          <li><a href="{esc('tel:' + p.phone.tel)}">{esc(p.phone.display)}</a></li>
          <li>Fax: <span class="nowrap">{esc(p.fax)}</span></li>
          <li><a href="{esc('mailto:' + p.email)}">{esc(p.email)}</a></li>
        </ul>
      </div>
      <div>
        <h2>Office hours</h2>
        <ul>
{hours}
        </ul>
      </div>
    </div>
    <div class="site-footer__legal">
      <span>&copy; <span data-year>2026</span> {esc(p.legal_name)}. All rights reserved.</span>
      <span>{legal}</span>
    </div>
  </div>
</footer>'''


def page(site, filename, title, description, body, *, head_extra='', base='', indexable=True):
    """A complete HTML document. title and description are plain text; body and head_extra
    are HTML. An indexable page gets its canonical URL and sharing tags (seo.py); any other
    is marked noindex and has neither."""
    if indexable:
        tags = seo.head_tags(site, filename, title, description)
    else:
        tags = '<meta name="robots" content="noindex">'
    extra = tags + (f'\n  {head_extra}' if head_extra else '')
    return (head(title, description, base, extra) + '\n<body>' + header(site, filename, base)
            + f'\n<main id="main">{body}</main>' + footer(site, base) + action_bar(site, base)
            + f'\n<script src="{base}{versioned('js/site.js')}"></script>\n</body>\n</html>')
