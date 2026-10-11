"""Services & products page."""
from ..helpers import esc
from ..icons import icon
from ..layout import V, cta_band, page, page_hero

FILENAME = 'services.html'


def render(site):
    p = site.practice

    cards_html = '\n'.join(
        f'''<div class="card">
      {icon(service.icon)}
      <h3 class="display-3">{esc(service.title)}</h3>
      <p>{esc(service.summary)}</p>
    </div>''' for service in site.services.services)

    products_html = '\n'.join(f'<li>{esc(product)}</li>' for product in site.services.products)

    body = page_hero('Services &amp; products', 'Everything under one roof',
                     'A modern facility known for its range of chiropractic techniques and the wellness services that support them.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="svc-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Services offered</span>
    <h2 id="svc-h" class="display-2">Care built around your exam, not a menu</h2>
    <div class="grid-3">
      {cards_html}
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="prod-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Available products</span>
    <h2 id="prod-h" class="display-2">Stocked in our office</h2>
    <ul class="list-tight list-columns">
      {products_html}
    </ul>
  </div>
</section>

</div>
{cta_band(site)}'''

    return page(site, FILENAME,
                f'Services & Products | {p.name}',
                'Spinal adjustments, massage therapy, digital X-ray, traction, nutrition consultations, sensitivity testing, and custom orthotics in Clarkston, MI.',
                body)
