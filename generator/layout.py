"""The chrome every page shares: head, header, footer, page hero, closing CTA band.

`base` goes in front of every link to the site's own files. '' keeps links relative to the
page, so a copy of the site works in any folder (such as the github.io preview). '/' makes
them root-absolute, for the 404 page, which GitHub Pages serves at whatever address was
missing, at any depth.
"""
from . import seo
from .helpers import esc
from .hours import hours_summary
from .icons import svg

V = '<span class="vertebra" aria-hidden="true"></span>'
# The footer's legal links, as (page, link text). The build stops if a page here isn't one it makes.
LEGAL_LINKS = (('privacy.html', 'Privacy policy'), ('accessibility.html', 'Accessibility statement'))


def head(title, description, base='', extra=''):
    """extra is trusted HTML for the end of <head> (robots, canonical and sharing tags, JSON-LD)."""
    extra_html = f'\n  {extra}' if extra else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="icon" type="image/svg+xml" href="{base}assets/favicon.svg">
  <link rel="stylesheet" href="{base}css/site.css">{extra_html}
</head>'''


def header(site, active, base=''):
    links = []
    for item in site.nav:
        current = ' aria-current="page"' if item.href == active else ''
        links.append(f'<li><a href="{esc(base + item.href)}"{current}>{esc(item.label)}</a></li>')
    name = esc(site.practice.name)
    return f'''
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap site-header__bar">
    <a class="site-header__logo" href="{base}index.html" aria-label="{name} — home">
      <img src="{base}assets/logo-full-color.svg" alt="{name}" width="180" height="61">
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
      <span class="visually-hidden">Menu</span>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>{''.join(links)}</ul>
    </nav>
    <div class="site-header__cta">
      <a class="btn btn--primary btn--sm" href="{base}contact.html#appointment">Request an appointment</a>
    </div>
  </div>
</header>'''


def page_hero(eyebrow, h1, lede='', meta=''):
    """Interior-page hero. Arguments are trusted HTML written in the page module. meta is a
    short line under the lede, such as the date a legal page was last updated."""
    lede_html = f'<p class="lede">{lede}</p>' if lede else ''
    meta_html = f'\n    <p class="page-hero__meta">{meta}</p>' if meta else ''
    return f'''
<section class="page-hero on-dark">
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1 class="display-page">{h1}</h1>
    {lede_html}{meta_html}
  </div>
</section>'''


def cta_band(site, heading='Don&rsquo;t wait any longer to get relief from your pain.',
             sub='Call, or send a request and a member of our team will reach out to you soon.', base=''):
    """Closing call-to-action band. heading and sub are trusted HTML."""
    phone = site.practice.phone
    return f'''
<section class="section section--navy on-dark" aria-label="Request an appointment">
  <div class="wrap center">
    <h2 class="display-2 measure-center">{heading}</h2>
    <p class="lede measure-center">{sub}</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--primary" href="{base}contact.html#appointment">Request an appointment</a>
      <a class="btn btn--ghost" href="{esc('tel:' + phone.tel)}">Call {esc(phone.display)}</a>
    </div>
  </div>
</section>'''


def footer(site, base=''):
    p = site.practice
    name = esc(p.name)
    explore = '\n'.join(
        f'          <li><a href="{esc(base + item.href)}">{esc(getattr(item, "footer_label", item.label))}</a></li>'
        for item in site.nav)
    hours = '\n'.join(f'          <li>{line}</li>' for line in hours_summary(site.hours))
    legal = ' &nbsp;&middot;&nbsp; '.join(
        f'<a href="{esc(base + href)}">{esc(text)}</a>' for href, text in LEGAL_LINKS)
    return f'''
<footer class="site-footer on-dark">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <a class="site-footer__logo" href="{base}index.html" aria-label="{name} — home">
          <img src="{base}assets/logo-reversed.svg" alt="{name}" width="190" height="63">
        </a>
        <p class="site-footer__tagline">Family wellness and chiropractic care for every age &mdash; serving Clarkston since 2001.</p>
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
          <li><a href="{esc(p.maps_url)}">{esc(p.address)}</a></li>
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
      <span>&copy; <span data-year>2026</span> {name}. All rights reserved.</span>
      <span>{legal}</span>
    </div>
  </div>
</footer>
<script src="{base}js/site.js"></script>'''


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
            + f'\n<main id="main">{body}</main>' + footer(site, base) + '\n</body>\n</html>')
