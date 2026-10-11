"""Success stories page: category chips, then one section of testimonials per on-site category."""
from ..helpers import esc
from ..layout import V, cta_band, page, page_hero

FILENAME = 'success-stories.html'


def _chip(site, category, on_page):
    label = esc(category.label)
    if category.id in on_page:
        return f'<li><a class="chip" href="#{esc(category.id)}">{label}</a></li>'
    href = esc(site.practice.legacy.old_site + category.old_site_path)
    return (f'<li><a class="chip chip--ext" href="{href}" target="_blank" rel="noopener">{label}'
            f'<span class="visually-hidden"> (opens the current live site)</span></a></li>')


def _section(section, label, alt):
    anchor = esc(section.category)
    quotes = '\n'.join(
        f'''<figure class="quote">
          <blockquote><p>{esc(t.quote)}</p></blockquote>
          <footer>{esc(t.author)} <span>Lifepointe patient</span></footer>
        </figure>''' for t in section.testimonials)
    cls = 'section section--card' if alt else 'section'
    return f'''
<section class="{cls}" id="{anchor}" aria-labelledby="{anchor}-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">{esc(label)}</span>
    <h2 id="{anchor}-h" class="display-2">{esc(section.heading)}</h2>
    <div class="grid-3 mt-15">
      {quotes}
    </div>
  </div>
</section>'''


def render(site):
    p = site.practice
    stories = site.testimonials
    labels = {c.id: c.label for c in stories.categories}
    on_page = {s.category for s in stories.sections}

    chips = '\n'.join(_chip(site, c, on_page) for c in stories.categories)
    # Sections alternate background, starting with the card tint.
    sections = ''.join(_section(s, labels[s.category], alt=(i % 2 == 0)) for i, s in enumerate(stories.sections))

    body = page_hero('Success stories', 'In our patients&rsquo; own words',
                     'Select a topic to read testimonials from our patients &mdash; fifteen categories and counting.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="cats-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Browse by topic</span>
    <h2 id="cats-h" class="display-2">What brought them in</h2>
    <ul class="chip-grid mt-15">
      {chips}
    </ul>
  </div>
</section>
{sections}
<section class="section" aria-label="Leave a review">
  {V}
  <div class="wrap center">
    <p class="lede measure-center">Has Lifepointe made a difference for you?</p>
    <a class="btn btn--ghost" href="{esc(p.social.facebook)}">Leave a review</a>
  </div>
</section>
</div>
{cta_band(site)}'''

    return page(site, FILENAME,
                f'Patient Success Stories | {p.name}',
                'Real testimonials from Lifepointe patients — back pain, headaches, allergies, fertility, pediatric care, and more.',
                body)
