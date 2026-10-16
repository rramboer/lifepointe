"""Services & products page."""
from ..helpers import esc, page_href
from ..icons import icon, svg
from ..layout import V, cta_band, page, page_hero
from ..media import product_photo
from . import recipe_book

FILENAME = 'services.html'


def render(site):
    p = site.practice
    appointment = page_href('contact.html#appointment')
    what_to_expect = page_href('new-patients.html')

    # Each card has its service's id, so the home page's cards link straight to it.
    cards_html = '\n'.join(
        f'''<div class="card service-card" id="{esc(service.id)}">
      {icon(service.icon)}
      <h3 class="display-3">{esc(service.title)}</h3>
      <p>{esc(service.summary)}</p>
    </div>''' for service in site.services.services)

    def product(item):
        note = getattr(item, 'note', None)
        note_html = f'\n        <p>{esc(note)}</p>' if note else ''
        return f'''<li class="card product-card">
      {product_photo(item.photo)}
      <div class="product-card__body">
        <h3>{esc(item.name)}</h3>{note_html}
      </div>
    </li>'''

    products_html = '\n'.join(product(item) for item in site.services.products)
    actions = (f'<a class="btn btn--primary" href="{appointment}">Request an appointment</a>'
               f'<a class="btn btn--ghost" href="{what_to_expect}">What to expect</a>')

    body = page_hero('Services &amp; products', 'Everything under one roof',
                     'A modern facility known for its range of chiropractic techniques and the wellness services that support them.',
                     actions=actions) + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="svc-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Services offered</span>
    <h2 id="svc-h" class="display-2">Care built around your exam, not a menu</h2>
    <div class="grid-3 mt-15">
      {cards_html}
    </div>
    <div class="callout mt-2">
      <div>
        <h3 class="display-3">Not sure where to start?</h3>
        <p>Your first visit is a thorough spinal and nervous system exam. Then we explain everything at your Report of Findings.</p>
      </div>
      <div class="btn-row">
        <a class="btn btn--primary" href="{appointment}">Request an appointment</a>
        <a class="btn btn--ghost" href="{what_to_expect}">What to expect</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="prod-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Available products</span>
    <h2 id="prod-h" class="display-2">Stocked in our office</h2>
    <ul class="product-grid mt-15">
    {products_html}
    </ul>
    <div class="card card--link card--row mt-2">
      {icon('leaf')}
      <div>
        <h3 class="display-3"><a class="card__link" href="{page_href(recipe_book.FILENAME)}">Healthy recipe book</a></h3>
        <p>Simple, tasty, and wholesome recipes that promote vibrant health and healing &mdash; from Dr.&nbsp;Greg.</p>
      </div>
      <span class="card__more" aria-hidden="true">{svg('arrow-right')}</span>
    </div>
  </div>
</section>

</div>
{cta_band(site)}'''

    return page(site, FILENAME,
                f'Services & Products | {p.name}',
                'Spinal adjustments, massage therapy, digital X-ray, traction, nutrition consultations, sensitivity testing, and custom orthotics in Clarkston, MI.',
                body)
