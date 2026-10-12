"""Contact page. It has no closing CTA band: never send people to the page they're on.

Appointments are booked by phone or email (or online, once practice.json has a booking_url).
There is deliberately no form: nothing on the site collects health information, and the
appointment email asks only for a name, a phone number and preferred times.
"""
from ..helpers import esc, mailto
from ..hours import hours_table
from ..icons import icon
from ..layout import V, page, page_hero

FILENAME = 'contact.html'
# The new email the "Email us" button opens.
APPOINTMENT_SUBJECT = 'Appointment request'
APPOINTMENT_BODY = 'Name: \nPhone: \nPreferred days and times: '


def render(site):
    p = site.practice
    tel = esc('tel:' + p.phone.tel)
    phone = esc(p.phone.display)
    email = esc(p.email)
    email_link = esc('mailto:' + p.email)
    appointment_mail = esc(mailto(p.email, APPOINTMENT_SUBJECT, APPOINTMENT_BODY))
    # With an online booking page, it is the one primary action; call and email follow it.
    if p.booking_url:
        heading = 'Book online, call or email us'
        book_online = f'<a class="btn btn--primary" href="{esc(p.booking_url)}">Book online</a>\n        '
        call_style = 'btn--ghost'
    else:
        heading = 'Call or email us to book'
        book_online = ''
        call_style = 'btn--primary'

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
        <p><a href="{email_link}">{email}</a></p>
      </div>
      <div class="card">
        {icon('fax')}
        <h3 class="display-3">Fax</h3>
        <p class="nowrap">{esc(p.fax)}</p>
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
      <p>Send us a message and a member of our team will reach out to you soon. Prefer the phone? <a href="{tel}">Call {phone}</a> during office hours.</p>
      {hours_table(site.hours, 'hours-table mt-15')}
    </div>
    <div class="card">
      {icon('calendar')}
      <h3 class="display-3">{heading}</h3>
      <div class="btn-row mt-15">
        {book_online}<a class="btn {call_style}" href="{tel}">Call {phone}</a>
        <a class="btn btn--ghost" href="{appointment_mail}">Email us</a>
      </div>
      <p class="muted mt-15">Emailing <a href="{appointment_mail}">{email}</a>? Please share only your name, phone number and preferred days and times, and leave out any health details.</p>
    </div>
  </div>
</section>

</div>'''

    return page(site, FILENAME,
                f'Contact & Appointments | {p.name}',
                f'Contact {p.name} in Clarkston, MI — request an appointment by email or call {p.phone.display}.',
                body)
