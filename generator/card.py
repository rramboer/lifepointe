"""The /card redirect behind the QR code on the printed business card.

The cards encode exactly https://lifepointechiro.com/card, so that address must never stop
working. GitHub Pages answers /card either with card.html or with a redirect to /card/, so
the same page is written to both files. It is not in the menu or linked from the site.

The destination is practice.json booking_url, or the contact page's appointment section
while that is null. Paths are root-absolute because the page is served at two depths.
The meta refresh redirects without JavaScript; the script at the end of the body redirects
without adding /card to the browser history, after the fallback link is on the page.
"""
import json
import re
from urllib.parse import urldefrag

from .errors import BuildError
from .helpers import esc

FILES = ('card.html', 'card/index.html')
DEFAULT_TARGET = '/contact.html#appointment'


def target(site):
    """Where the QR code sends people: the online booking page if set, else the contact page."""
    return site.practice.booking_url or DEFAULT_TARGET


def check_target(site, pages):
    """Stop the build if the target is on this site but its page or section is missing.

    `pages` maps each generated filename to its HTML. A booking_url on another site is
    checked in data.py instead.
    """
    to = target(site)
    if not to.startswith('/'):
        return
    path, _, fragment = to[1:].partition('#')
    if path not in pages:
        raise BuildError(f'/card goes to {to}, but the build makes no {path}. '
                         f'Change DEFAULT_TARGET in generator/card.py.')
    if fragment and not re.search(r'\sid="' + re.escape(fragment) + '"', pages[path]):
        raise BuildError(f'/card goes to {to}, but {path} has no id="{fragment}". Keep that id on '
                         f'the appointment section, or change DEFAULT_TARGET in generator/card.py.')


def _js_string(value):
    """A JavaScript string literal that is safe inside an inline <script>."""
    return (json.dumps(value)  # ensure_ascii: U+2028 and U+2029 come out escaped too
            .replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'))


def render(site):
    p = site.practice
    to = target(site)
    absolute = p.site_url + to if to.startswith('/') else to
    canonical = urldefrag(absolute)[0]  # a canonical names a page, not a spot on it
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc('Appointments | ' + p.name)}</title>
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="{esc('0; url=' + to)}">
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
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
  <h1>Taking you to our appointment page…</h1>
  <a class="btn" href="{esc(to)}">Go to the appointment page</a>
</main>
<script>location.replace({_js_string(to)});</script>
</body>
</html>
'''
