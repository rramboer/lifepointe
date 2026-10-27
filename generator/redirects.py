"""The redirects behind printed QR codes: /card and /review.

  /card    the QR code on the printed business card. It goes to practice.json booking_url,
           or the contact page's appointment section while that is null.
  /review  a QR code for leaving a review. It goes to practice.json review_url, Google's
           review page, so a printed code keeps working if Google's link ever changes.

Printed codes last for years, so neither address may ever stop working. Each page is its
name plus .html, like every other page: GitHub Pages answers /card from card.html, as it
answers /about from about.html. Neither is in the menu or linked from the site.

Their paths are root-absolute and leave out .html, like every link. The meta refresh
redirects without JavaScript; the script at the end of the body redirects without adding
the page to the browser history, after the fallback link is on the page.
"""
import json
import re
from urllib.parse import urldefrag

from .errors import BuildError
from .helpers import esc

DEFAULT_TARGET = '/contact#appointment'

# Each redirect's file, where it goes, its title (before " | " and the practice's name), the
# line it shows, and its button.
REDIRECTS = (
    ('card.html', lambda p: p.booking_url or DEFAULT_TARGET, 'Appointments',
     'Taking you to our appointment page…', 'Go to the appointment page'),
    ('review.html', lambda p: p.review_url, 'Leave a review',
     'Taking you to Google to leave us a review…', 'Leave a review on Google'),
)
FILES = tuple(filename for filename, *_ in REDIRECTS)


def check_targets(site, pages):
    """Stop the build if a redirect goes to a page or section on this site that is missing.

    `pages` maps each generated filename to its HTML. Addresses on other sites are checked
    in data.py instead.
    """
    for filename, target, *_ in REDIRECTS:
        name = '/' + filename.removesuffix('.html')
        to = target(site.practice)
        if not to.startswith('/'):
            continue
        path, _, fragment = to[1:].partition('#')
        page = path + '.html' if path else 'index.html'
        if page not in pages:
            raise BuildError(f'{name} goes to {to}, but the build makes no {page}. '
                             f'Change DEFAULT_TARGET in generator/redirects.py.')
        if fragment and not re.search(r'\sid="' + re.escape(fragment) + '"', pages[page]):
            raise BuildError(f'{name} goes to {to}, but {page} has no id="{fragment}". Keep that id on '
                             f'the appointment section, or change DEFAULT_TARGET in generator/redirects.py.')


def _js_string(value):
    """A JavaScript string literal that is safe inside an inline <script>."""
    return (json.dumps(value)  # ensure_ascii: U+2028 and U+2029 come out escaped too
            .replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'))


def render(site):
    """(filename, html) for each redirect."""
    return [(filename, _page(site.practice, target(site.practice), title, line, button))
            for filename, target, title, line, button in REDIRECTS]


def _page(p, to, title, line, button):
    absolute = p.site_url + to if to.startswith('/') else to
    canonical = urldefrag(absolute)[0]  # a canonical names a page, not a spot on it
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title + ' | ' + p.name)}</title>
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="{esc('0; url=' + to)}">
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <style>
    :root {{ --navy: #00205B; --green: #84BD00; --paper: #F7F8FA; }}
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{
      margin: 0; min-height: 100vh; padding: 2rem 1rem;
      display: flex; align-items: center; justify-content: center;
      background: var(--paper); color: var(--navy); text-align: center;
      font: 1.0625rem/1.65 "Lato", "Helvetica Neue", Arial, sans-serif;
    }}
    main {{ width: 100%; max-width: 26rem; }}
    img {{ display: block; max-width: 100%; height: auto; margin: 0 auto 1.75rem; }}
    h1 {{ margin: 0 0 1.25rem; font: 700 1.35rem/1.3 "Bricolage Grotesque", "Lato", "Helvetica Neue", Arial, sans-serif; text-wrap: balance; }}
    .btn {{
      display: inline-block; padding: .95rem 1.6rem; border-radius: 999px; text-wrap: balance;
      background: var(--green); color: var(--navy); font-weight: 700; line-height: 1.2; text-decoration: none;
    }}
    .btn:hover {{ box-shadow: 0 0 0 3px var(--navy) inset; }}
    :focus-visible {{ outline: 3px solid var(--navy); outline-offset: 2px; }}
  </style>
</head>
<body>
<main>
  <img src="/assets/logo-full-color.svg" alt="{esc(p.name)}" width="240" height="81">
  <h1>{esc(line)}</h1>
  <a class="btn" href="{esc(to)}">{esc(button)}</a>
</main>
<script>location.replace({_js_string(to)});</script>
</body>
</html>
'''
