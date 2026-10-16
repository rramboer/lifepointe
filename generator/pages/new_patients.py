"""New patients page: the first visit, step by step, and the intake forms."""
from ..helpers import esc, in_series, page_href
from ..icons import icon, svg
from ..layout import V, cta_band, page, page_hero
from . import good_faith_estimate

FILENAME = 'new-patients.html'
FORMS_ID = 'forms'  # the forms card; the hero's "New patient forms" button jumps to it

# The first visit, in order, as (title, text): trusted HTML. The home page's "Your first visit"
# section lists the titles too.
STEPS = (
    ('Forms before you arrive',
     'Download your forms below and email them back to us &mdash; and skip the waiting room.'),
    ('Spinal &amp; nervous system exam',
     'Hands-on palpation plus specialized tests: balance scales, posture evaluation, range-of-motion '
     'measurements, and orthopedic tests.'),
    ('X-rays, only if needed',
     'Depending on your age and situation. X-rays show the position of the spinal bones, the level of '
     'degeneration present, and the areas that need precise adjustment &mdash; we skip them for pregnancy, '
     'most young children, and anyone with recent usable films.'),
    ('Your Report of Findings',
     'We sit down and explain what every test means, what we found, and the care plan we recommend '
     '&mdash; before any treatment begins.'),
)


def render(site):
    p = site.practice
    email = esc(p.email)
    steps_html = '\n'.join(
        f'''        <li class="step">
          <div><h3>{title}</h3><p>{text}</p></div>
        </li>''' for title, text in STEPS)
    actions = (f'<a class="btn btn--primary" href="{page_href("contact.html#appointment")}">Request an appointment</a>'
               f'<a class="btn btn--ghost" href="#{FORMS_ID}">{svg("download")}New patient forms</a>')

    body = page_hero('New patients', 'Your first visit, step by step',
                     'Our examination procedures are geared toward detecting and correcting vertebral subluxation &mdash; selected specifically for your spine and nervous system health.',
                     actions=actions) + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="steps-h">
  {V}
  <div class="wrap grid-2 grid--top">
    <div>
      <span class="eyebrow">What to expect</span>
      <h2 id="steps-h" class="display-2">A first visit that&rsquo;s measured, not rushed</h2>
      <p>Your exam gives us a scientific baseline &mdash; much more accurate than depending on &ldquo;how you feel&rdquo; on any given day &mdash; so we can measure your progress as your spine corrects and your nervous system function improves.</p>
      <ol class="steps mt-15">
{steps_html}
      </ol>
    </div>
    <div class="card-stack card-stack--sticky">
      <div class="card" id="{FORMS_ID}">
        {icon('download')}
        <h3 class="display-3">New patient forms</h3>
        <p>Print and bring them, or fill them out on a computer and email them to <a href="{esc('mailto:' + p.email)}">{email}</a> before your appointment.</p>
        <ul class="link-list">
          <li><a class="file-link" href="{esc(p.forms.adult)}">{svg('download')}<span>Download adult new patient forms (PDF)</span></a></li>
          <li><a class="file-link" href="{esc(p.forms.child)}">{svg('download')}<span>Download child new patient forms (under 12) (PDF)</span></a></li>
        </ul>
      </div>
      <div class="card">
        {icon('shield')}
        <h3 class="display-3">Insurance</h3>
        <p>In-network with {in_series(esc(plan) for plan in p.in_network)}; other policies accepted out-of-network. Questions? <a href="{esc('tel:' + p.phone.tel)}">Call {esc(p.phone.display)}</a>.</p>
        <p>Paying for your care yourself? You can ask for a <a href="{esc(page_href(good_faith_estimate.FILENAME))}">Good Faith Estimate</a> of the cost.</p>
      </div>
    </div>
  </div>
</section>

</div>
{cta_band(site, 'Ready for your first visit?', 'Request a time that works for your family and we&rsquo;ll confirm it with you.')}'''

    return page(site, FILENAME,
                f'New Patients | {p.name}',
                'What to expect at your first Lifepointe visit — exam, X-rays if needed, and your Report of Findings — plus downloadable new patient forms.',
                body)
