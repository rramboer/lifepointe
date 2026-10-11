"""The 404 page. GitHub Pages serves it, with status 404, for any address that doesn't exist.

It is served at the missing address itself (/old/page shows this page), so every link to the
site's own files starts with / (BASE). Those links only work at the root of a domain: on the
rramboer.github.io/lifepointe/ preview it shows without styles. It is noindex and not in
pages.PAGES, so it stays out of the sitemap.
"""
from ..helpers import esc
from ..layout import V, page, page_hero

FILENAME = '404.html'
BASE = '/'


def render(site):
    p = site.practice
    body = page_hero('Page not found', 'We couldn&rsquo;t find that page',
                     'The link may be out of date, or the address may have a typo.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="next-h">
  {V}
  <div class="wrap">
    <h2 id="next-h" class="display-2">Where to next?</h2>
    <div class="btn-row mt-15">
      <a class="btn btn--primary" href="{BASE}index.html">Go to the home page</a>
      <a class="btn btn--ghost" href="{BASE}contact.html">Contact us</a>
    </div>
    <p class="mt-2">Questions? <a href="{esc('tel:' + p.phone.tel)}">Call {esc(p.phone.display)}</a>.</p>
  </div>
</section>

</div>'''

    return page(site, FILENAME,
                f'Page not found | {p.name}',
                f'This page doesn’t exist. Go to the {p.name} home page or contact us.',
                body, base=BASE, indexable=False)
