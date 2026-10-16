"""Contact page. It has no closing CTA band: never send people to the page they're on.

Appointments are booked by phone or email (or online, once practice.json has a booking_url).
There is deliberately no form: nothing on the site collects health information, and the
appointment email asks only for a name, a phone number and preferred times.
"""
from ..helpers import esc, mailto
from ..hours import hours_table
from ..icons import icon, svg
from ..layout import V, page, page_hero
from ..media import building

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
    # On a narrow screen, the email may break only before the @, and the
    # address keeps "Clarkston, MI 48346" together (practice.json's format is "street, city, ST 12345").
    email_wrapping = email.replace('@', '<wbr>@')
    maps = esc(p.maps_url)
    street, city, state_zip = p.address.rsplit(', ', 2)
    address = f'{esc(street)}, <span class="nowrap">{esc(city)}, {esc(state_zip)}</span>'
    # With an online booking page, it is the one primary action; call and email follow it.
    if p.booking_url:
        heading = 'Book online, call, or email us'
        book_online = f'<a class="btn btn--primary" href="{esc(p.booking_url)}">{svg("calendar")}Book online</a>\n          '
        call_style = 'btn--ghost'
    else:
        heading = 'Call or email us to book'
        book_online = ''
        call_style = 'btn--primary'

    body = page_hero('Contact', 'Keep in touch',
                     'Call, email, stop by, or send a request &mdash; a member of our team will reach out to you soon.') + f'''
<div class="rail-wrap">

<section class="section" id="appointment" aria-labelledby="appt-h">
  {V}
  <div class="wrap grid-2 grid--top">
    <div>
      <span class="eyebrow">Request an appointment</span>
      <h2 id="appt-h" class="display-2">We&rsquo;d love to hear from you</h2>
      <p>Send us a message, and a member of our team will reach out to you soon. Prefer the phone? <a href="{tel}">Call {phone}</a> during office hours.</p>
      <div class="card booking-card mt-15">
        {icon('calendar')}
        <h3 class="display-3">{heading}</h3>
        <div class="btn-row mt-15">
          {book_online}<a class="btn {call_style}" href="{tel}">{svg('phone')}Call {phone}</a>
          <a class="btn btn--ghost" href="{appointment_mail}">{svg('mail')}Email us</a>
        </div>
      </div>
    </div>
    <div class="card hours-card">
      <h3 class="display-3">Office hours</h3>
      <p class="open-status" data-open-status hidden></p>
      {hours_table(site.hours)}
    </div>
  </div>
</section>

<section class="section section--card" aria-labelledby="reach-h">
  {V}
  <div class="wrap">
    <span class="eyebrow">Reach us</span>
    <h2 id="reach-h" class="display-2">Every way to say hello</h2>
    <div class="reach-card mt-15">
      <!-- A bigger target for "Get directions" with a mouse or finger. Keyboard and screen
           reader users have that link in the list, so this copy is left out of both. -->
      <a class="reach-card__place" href="{maps}" tabindex="-1" aria-hidden="true">
        {building(p.building_photo)}
      </a>
      <ul class="reach-list">
        <li class="reach-item">
          {icon('phone')}
          <div>
            <h3 class="reach-item__label">Call us</h3>
            <p class="reach-item__value"><a class="reach-item__link" href="{tel}">{phone}</a></p>
          </div>
          <span class="reach-item__go reach-item__go--arrow" aria-hidden="true">{svg('arrow-right')}</span>
        </li>
        <li class="reach-item">
          {icon('mail')}
          <div>
            <h3 class="reach-item__label">Email us</h3>
            <p class="reach-item__value"><a class="reach-item__link" href="{email_link}">{email_wrapping}</a></p>
          </div>
          <div class="reach-item__go"><button class="copy-btn" type="button" data-copy="{email}" hidden>Copy email address</button><span class="visually-hidden" role="status"></span></div>
        </li>
        <li class="reach-item">
          {icon('pin')}
          <div>
            <h3 class="reach-item__label">Find us</h3>
            <p class="reach-item__value">{address}</p>
          </div>
          <p class="reach-item__go action-link"><a class="reach-item__link" href="{maps}">Get directions{svg('arrow-right')}</a></p>
        </li>
      </ul>
    </div>
  </div>
</section>

</div>'''

    return page(site, FILENAME,
                f'Contact & Appointments | {p.name}',
                f'Contact {p.name} in Clarkston, MI — request an appointment by email or call {p.phone.display}.',
                body)
