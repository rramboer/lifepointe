"""Contact page. It has no closing CTA band: never send people to the page they're on."""
from ..helpers import esc
from ..hours import hours_table
from ..icons import icon
from ..layout import V, page, page_hero

FILENAME = 'contact.html'


def render(site):
    p = site.practice
    tel = esc('tel:' + p.phone.tel)
    phone = esc(p.phone.display)
    email = esc(p.email)
    mailto = esc('mailto:' + p.email)

    body = page_hero('Contact', 'Keep in touch',
                     'Call, email, stop by, or send a request &mdash; a member of our team will reach out to you soon.') + f'''
<div class="rail-wrap">

<section class="section" aria-labelledby="reach-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Reach us</span>
    <h2 id="reach-h" class="display-2">Every way to say hello</h2>
    <div class="grid-4 mt-15">
      <div class="card">
        {icon('phone')}
        <h3 class="display-3">Call us</h3>
        <p><a href="{tel}">{phone}</a></p>
      </div>
      <div class="card">
        {icon('mail')}
        <h3 class="display-3">Email us</h3>
        <p><a href="{mailto}">{email}</a></p>
      </div>
      <div class="card">
        {icon('fax')}
        <h3 class="display-3">Fax</h3>
        <p>{esc(p.fax)}</p>
      </div>
      <div class="card">
        {icon('pin')}
        <h3 class="display-3">Find us</h3>
        <p>{esc(p.address)}</p>
        <p><a href="{esc(p.maps_url)}">Get directions &rarr;</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section section--card" id="appointment" aria-labelledby="appt-h">
  {V}
  <div class="wrap grid-2 grid--top">
    <div>
      <span class="eyebrow">Request an appointment</span>
      <h2 id="appt-h" class="display-2">We&rsquo;d love to hear from you</h2>
      <p>Send us a message using this form and a member of our team will reach out to you soon. Prefer the phone? <a href="{tel}">Call {phone}</a> during office hours.</p>
      {hours_table(site.hours, 'hours-table mt-15')}
    </div>
    <div class="card card--form">
      <iframe src="{esc(p.legacy.appointment_form)}" title="Appointment request form" loading="lazy"></iframe>
      <script src="{esc(p.legacy.appointment_form_script)}" async></script>
      <p class="form-fallback">If the form doesn&rsquo;t load, email <a href="{mailto}?subject=Request%20an%20Appointment">{email}</a> or call <a href="{tel}">{phone}</a>.</p>
    </div>
  </div>
</section>

</div>'''

    return page(site, FILENAME,
                f'Contact & Appointments | {p.name}',
                f'Contact Lifepointe Chiropractic in Clarkston, MI — request an appointment online or call {p.phone.display}.',
                body)
