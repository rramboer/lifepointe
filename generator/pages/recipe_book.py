"""Healthy recipe book page."""
from ..helpers import esc
from ..icons import icon
from ..layout import V, cta_band, page, page_hero

FILENAME = 'recipe-book.html'


def render(site):
    p = site.practice
    staples_html = '\n'.join(f'<li>{esc(staple)}</li>' for staple in site.recipe_staples)

    body = page_hero('Healthy recipe book', 'From our kitchen to yours',
                     'Simple, tasty, and wholesome recipes that promote vibrant health and healing &mdash; from Dr.&nbsp;Greg.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="recipes-h">
  {V}
  <div class="wrap grid-2 grid--top">
    <div>
      <span class="eyebrow">Healthy for Life</span>
      <h2 id="recipes-h" class="display-2">Wholesome recipes, zero inflammatory foods</h2>
      <p>Every recipe avoids inflammatory foods like refined sugar, grain, dairy, and processed food. If you see our logo next to an ingredient, it can be purchased right here at our office; for other items, links inside the recipes point to the same brands we use in our own home.</p>
      <p>And if you see a star next to a recipe &mdash; those are our Ramboer Family Favorites!</p>
      <a class="btn btn--primary" href="{esc(p.recipe_book_url)}">Open the recipe book</a>
    </div>
    <div class="card">
      {icon('leaf')}
      <h3 class="display-3">Our staple ingredients</h3>
      <p>A few favorites always in our kitchen:</p>
      <ul class="list-tight">
        {staples_html}
      </ul>
      <p class="hint">As an Amazon Associate, we earn from qualifying purchases &mdash; brand links are inside the recipe book.</p>
    </div>
  </div>
</section>

</div>
{cta_band(site)}'''

    return page(site, FILENAME,
                f'Healthy Recipe Book | {p.name}',
                'The Lifepointe Healthy for Life recipe book — simple, wholesome recipes free of refined sugar, grain, dairy, and processed food.',
                body)
