"""New patients page: the first visit, step by step, and the intake forms."""
from ..helpers import esc
from ..icons import icon
from ..layout import V, cta_band, page, page_hero

FILENAME = 'new-patients.html'


def render(site):
    p = site.practice
    email = esc(p.email)

    body = page_hero('New patients', 'Your first visit, step by step',
                     'Our examination procedures are geared toward detecting and correcting vertebral subluxation &mdash; selected specifically for your spine and nervous system health.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="steps-h">
  {V}
  <div class="wrap grid-2 grid--top">
    <div>
      <span class="eyebrow">What to expect</span>
      <h2 id="steps-h" class="display-2">A first visit that&rsquo;s measured, not rushed</h2>
      <p>Your exam gives us a scientific baseline &mdash; much more accurate than depending on &ldquo;how you feel&rdquo; on any given day &mdash; so we can measure your progress as your spine corrects and your nervous system function improves.</p>
      <ol class="steps mt-15">
        <li class="step">
          <div><h3>Forms before you arrive</h3><p>Download your forms below and email them back to us &mdash; and skip the waiting room.</p></div>
        </li>
        <li class="step">
          <div><h3>Spinal &amp; nervous system exam</h3><p>Hands-on palpation plus specialized tests: balance scales, posture evaluation, range-of-motion measurements, and orthopedic tests.</p></div>
        </li>
        <li class="step">
          <div><h3>X-rays, only if needed</h3><p>Depending on your age and situation. X-rays show the position of the spinal bones, the level of degeneration present, and the areas that need precise adjustment &mdash; we skip them for pregnancy, most young children, and anyone with recent usable films.</p></div>
        </li>
        <li class="step">
          <div><h3>Your Report of Findings</h3><p>We sit down and explain what every test means, what we found, and the care plan we recommend &mdash; before any treatment begins.</p></div>
        </li>
      </ol>
    </div>
    <div class="card-stack card-stack--sticky">
      <div class="card">
        {icon('download')}
        <h3 class="display-3">New patient forms</h3>
        <p>Print and bring them, or fill them out on a computer and email them to <a href="{esc('mailto:' + p.email)}">{email}</a> before your appointment.</p>
        <ul class="link-list">
          <li><a href="{esc(p.legacy.adult_forms)}">Download adult new patient forms</a></li>
          <li><a href="{esc(p.legacy.child_forms)}">Download child new patient forms (under 12)</a></li>
        </ul>
      </div>
      <div class="card">
        {icon('shield')}
        <h3 class="display-3">Insurance</h3>
        <p>In-network with Blue Cross Blue Shield, Medicare, Medicare Advantage, and Veterans Affairs; other policies accepted out-of-network. Questions? <a href="{esc('tel:' + p.phone.tel)}">Call {esc(p.phone.display)}</a>.</p>
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
