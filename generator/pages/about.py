"""About page: Dr. Greg, the team, and what chiropractic is."""
from ..helpers import esc
from ..icons import svg
from ..layout import V, cta_band, page, page_hero
from ..media import headshot

FILENAME = 'about.html'


def _name(person):
    credentials = getattr(person, 'credentials', None)
    return f'{esc(person.name)}, {esc(credentials)}' if credentials else esc(person.name)


def _team_card(person):
    """A team member's card: the headshot, or their initials in its place until there is one
    (data/team.json "photo": null), then name, title and any bio. The photo area is the same
    4:5 box either way, so adding a headshot doesn't change the card. The name is the heading
    right below, so the picture is decorative (alt="")."""
    bio = getattr(person, 'bio', None)
    bio_html = f'\n          <p>{esc(bio)}</p>' if bio else ''
    return f'''<div class="card team-card">
        {headshot(person.photo, person.name, 'headshot team-card__photo')}
        <div class="team-card__body">
          <h3 class="display-3">{_name(person)}</h3>
          <p class="team-card__title">{esc(person.title)}</p>{bio_html}
        </div>
      </div>'''


def render(site):
    p = site.practice

    staff_html = '\n      '.join(_team_card(person) for person in site.team.staff)

    badges_html = '\n'.join(
        f'      <span class="badge">{svg(m.icon)} {esc(m.label)}</span>' for m in site.team.memberships)

    body = page_hero('About us', 'The practice of our dreams',
                     'Caring for our patients for life &mdash; with the emphasis on the people we take care of, not just their symptoms.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="greg-h">
  {V}
  <div class="wrap doctor">
    {headshot(p.doctor.photo, p.doctor.name, 'headshot doctor__photo', eager=True)}
    <div class="doctor__text">
      <span class="eyebrow">Meet the doctor</span>
      <h2 id="greg-h" class="display-2">{_name(p.doctor)}</h2>
      <div class="doctor__columns">
        <div>
          <p>I opened {esc(p.name)} in July of 2001. Our mission, in a nutshell, is to teach our community that all health comes from within &mdash; and that you already have everything it takes to be truly healthy, happy, and well. This inner health potential lacks its full expression when it&rsquo;s interfered with. That&rsquo;s where we fit into the picture: our role is to determine whether you have this interference, and if so, to help you reduce it for life.</p>
          <p>We adjust people of all ages, from newborns just a few minutes old to the wisest members of our community. We also work with athletes at every level, from students to elite professionals. We love what we do, and we love to teach and share what we&rsquo;ve learned.</p>
        </div>
        <div class="card">
          <h3 class="display-3">Background</h3>
          <ul class="list-tight">
            <li>Originally from Ridgetown, Ontario, Canada</li>
            <li>Bachelor of Human Kinetics with Honors in Applied Kinesiology, University of Windsor</li>
            <li>Doctor of Chiropractic, Logan College of Chiropractic, 2000</li>
            <li>Founded Lifepointe in Clarkston, July 2001</li>
            <li>Certified Chiropractic Wellness Practitioner (CCWP), 2013</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--card" id="team" aria-labelledby="team-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">The team</span>
    <h2 id="team-h" class="display-2">The people who&rsquo;ll take care of you</h2>
    <div class="team-grid mt-15">
      {staff_html}
    </div>
    <div class="badge-row mt-2">
{badges_html}
    </div>
  </div>
</section>

<section class="section" id="chiropractic-care" aria-labelledby="care-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">What is chiropractic?</span>
    <h2 id="care-h" class="display-2">A drug-free approach with the nervous system at the center</h2>
    <div class="grid-2 grid--top">
      <div>
        <p>Chiropractic is a healthcare profession focused on the health of the musculoskeletal and nervous systems. It&rsquo;s a drug-free approach that looks to establish and maintain proper posture and biomechanics, and to alleviate the manifestation of stress on the body &mdash; based on the scientific knowledge that the human body is a self-healing, self-regulating organism, always striving to heal as long as it has the right raw materials and no interference.</p>
        <p>Many people think we are &ldquo;back pain&rdquo; doctors. In reality, we focus on nervous system function &mdash; the nervous system just happens to be housed inside the spine. Through this network of nerves, your brain constantly coordinates the entire body. It&rsquo;s our job to ensure the messages traveling up and down the spine can do so without disruption.</p>
      </div>
      <div>
        <p>While many people first come in because an issue is limiting the life they want to live, chiropractic is not a treatment for any specific disease. Our goal is to get to the root cause of your symptoms &mdash; and by addressing root causes, symptoms begin to go away on their own.</p>
        <p>True spinal correction takes repetition, time, and energy, so we give our patients an active role in supporting care at home. And beyond correction, a wellness program of maintenance adjustments has been consistently correlated with decreased injury rates and pain, normalized blood pressure, increased energy, better immune function, and better sleep &mdash; at every stage of life.</p>
      </div>
    </div>
  </div>
</section>

</div>
{cta_band(site)}'''

    return page(site, FILENAME,
                f'About Us | {p.name}',
                f'Meet {p.doctor.name} and the Lifepointe team — family and sports chiropractic care in Clarkston since 2001.',
                body)
