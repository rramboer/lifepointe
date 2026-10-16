"""Success stories page: a chip per category, then one section of testimonials per category."""
from ..errors import BuildError
from ..helpers import esc
from ..icons import svg
from ..layout import V, cta_band, page, page_hero, quote

FILENAME = 'success-stories.html'
TOPICS = 'topics'  # id of the chip list; each section links back to it
# Ids on this page that don't come from a category: the layout's, then the chip list's.
PAGE_IDS = ('main', 'site-nav', TOPICS, f'{TOPICS}-h')


def _check_ids(categories):
    """Each category puts its id and '<id>-h' (its heading) on the page; every id must be unique."""
    seen = set(PAGE_IDS)
    for c in categories:
        for anchor in (c.id, f'{c.id}-h'):
            if anchor in seen:
                made = '' if anchor == c.id else f' makes the heading id "{anchor}", which'
                raise BuildError(f'data/testimonials.json: category id "{c.id}"{made} is already used on '
                                 f'{FILENAME}; choose another')
            seen.add(anchor)


def _section(category, alt):
    anchor = esc(category.id)
    count = len(category.testimonials)
    quotes = '\n'.join(quote(t) for t in category.testimonials)
    cls = 'section section--card' if alt else 'section'
    return f'''
<section class="{cls}" id="{anchor}" aria-labelledby="{anchor}-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">{count} testimonial{'' if count == 1 else 's'}</span>
    <h2 id="{anchor}-h" class="display-2">{esc(category.label)}</h2>
    <div class="quote-columns mt-15">
      {quotes}
    </div>
    <p class="back-link mt-2"><a href="#{TOPICS}">{svg('arrow-up')}Back to topics</a></p>
  </div>
</section>'''


def render(site):
    p = site.practice
    categories = site.testimonials.categories
    _check_ids(categories)

    chips = '\n'.join(f'<li><a class="chip" href="#{esc(c.id)}">{esc(c.label)}</a></li>' for c in categories)
    # Sections alternate background, starting with the card tint.
    sections = ''.join(_section(c, alt=(i % 2 == 0)) for i, c in enumerate(categories))

    body = page_hero('Success stories', 'In our patients&rsquo; own words',
                     'Select a topic to read testimonials from our patients.') + f'''
<div class="rail-wrap">

<section class="section" id="{TOPICS}" aria-labelledby="{TOPICS}-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Browse by topic</span>
    <h2 id="{TOPICS}-h" class="display-2">What brought them in</h2>
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
