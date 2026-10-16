"""Load the content in data/*.json and check it before anything is built.

Every problem is collected and reported together, each naming its file and field.
The order of every JSON array is the order it is shown on the site.
"""
import json
import re
from types import SimpleNamespace

from .errors import BuildError
from .icons import NAMES as ICON_NAMES

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
SLUG = re.compile(r'[a-z0-9]+(-[a-z0-9]+)*')
TIME = re.compile(r'([01][0-9]|2[0-3]):[0-5][0-9]')
OPENED = re.compile(r'(19|20)[0-9]{2}-(0[1-9]|1[0-2])')
TEL = re.compile(r'\+1[0-9]{10}')
# How the phone and fax numbers are written on the site and the business card.
SHOWN_NUMBER = re.compile(r'[0-9]{3}-[0-9]{3}-[0-9]{4}')
# "street, city, ST 12345". Search engines get the address in parts (seo.py), split by this.
ADDRESS = re.compile(r'(?P<street>[^,]+(?:, [^,]+)*), (?P<city>[^,]+), '
                     r'(?P<region>[A-Z]{2}) (?P<postal>[0-9]{5}(?:-[0-9]{4})?)')
SITE_URL = re.compile(r'https://[a-z0-9-]+(\.[a-z0-9-]+)+')
# The place pin in a Google Maps link: !3d<latitude>!4d<longitude>.
MAP_PIN = re.compile(r'!3d(-?[0-9]+(?:\.[0-9]+)?)!4d(-?[0-9]+(?:\.[0-9]+)?)')
# https://, a domain with at least one dot, an optional port, then any path, query or fragment.
WEB_ADDRESS = re.compile(r'https://[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+(:[0-9]+)?([/?#]\S*)?')
# Photos in the repo's assets/ folder (published with it), each kind in its own folder and named
# in lowercase letters, digits and hyphens: headshots (the team and the doctor) in assets/team/,
# the office in assets/office/, products in assets/products/. Until a photo exists its field is
# null, and the page shows a placeholder of the same size in its place.
PHOTO_FOLDERS = {'team': 'assets/team/sybil-olson.jpg', 'office': 'assets/office/building.jpg',
                 'products': 'assets/products/biofreeze.jpg'}
# A PDF in the repo's forms/ folder, which is published as-is; pages link to it by this path.
FORM_PATH = re.compile(r'forms/[a-z0-9]+(-[a-z0-9]+)*\.pdf')
TOP = '(top level)'
# Data is plain text; esc() turns it into HTML. Entities or tags here would show up literally.
LOOKS_LIKE_HTML = re.compile(r'&(#[0-9]+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);|<[a-zA-Z/!]')
# Testimonials use typographic quotes, and the page draws the opening quote mark itself, so a
# quote isn't wrapped in marks of its own. It may still start or end with an inner quotation.
WRAPPED = re.compile(r'\s*(?:["“].*["”]|[\'‘].*[\'’])\s*', re.DOTALL)
STRAIGHT_QUOTES = re.compile('["\']')
# A language tag for the lang attribute (BCP 47): "es", "zh-Hant", "sr-Latn".
LANG_TAG = re.compile(r'[a-z]{2,3}(-[A-Za-z0-9]{2,8})*')
# The blanks in a language-help notice, filled with the practice's numbers when the page is built.
NOTICE_BLANK = re.compile(r'\{[^{}]*\}')


def _at(where, key):
    return f'{where}.{key}' if where and where != TOP else key


class Checker:
    """Collects the problems found in one data file."""

    def __init__(self, filename, errors):
        self.filename = filename
        self.errors = errors

    def fail(self, where, problem):
        self.errors.append(f'data/{self.filename}: {where}: {problem}')

    def obj(self, value, where, fields=None):
        """An object; with `fields`, any other key is reported (it is probably a typo)."""
        if not isinstance(value, dict):
            self.fail(where, 'expected an object {...}')
            return {}
        for key in value:
            if fields is not None and key not in fields:
                self.fail(_at(where, key), f'unknown field (expected: {", ".join(fields)})')
        return value

    def items(self, value, where, allow_empty=False):
        if isinstance(value, list) and (value or allow_empty):
            return value
        self.fail(where, 'expected a list [...]' if allow_empty else 'expected a non-empty list [...]')
        return []

    def text(self, obj, key, where, optional=False):
        """A text field. An optional field may be left out, but if it is there it must be text."""
        field = _at(where, key)
        if key not in obj:
            if not optional:
                self.fail(field, 'missing')
            return None
        value = obj[key]
        if not isinstance(value, str):
            self.fail(field, 'must be text (remove the field to leave it out)' if optional else 'must be text')
        elif not value.strip():
            self.fail(field, 'empty')
        else:
            return value
        return None

    def url(self, obj, key, where, optional=False):
        value = self.text(obj, key, where, optional)
        if value and not value.startswith('https://'):
            self.fail(_at(where, key), f'must start with https:// (got "{value}")')
        return value

    def icon(self, obj, key, where):
        name = self.text(obj, key, where)
        if name and name not in ICON_NAMES:
            self.fail(_at(where, key), f'unknown icon "{name}" (known: {", ".join(sorted(ICON_NAMES))})')

    def photo(self, obj, key, where, folder, root):
        """A photo field: null until there is a photo, then a JPEG or PNG in assets/<folder>/."""
        field = _at(where, key)
        example = PHOTO_FOLDERS[folder]
        if key not in obj:
            self.fail(field, 'missing (use null until there is a photo)')
            return
        value = obj[key]
        if value is None:
            return
        if not isinstance(value, str) or not re.fullmatch(rf'assets/{folder}/[a-z0-9]+(-[a-z0-9]+)*\.(jpg|png)', value):
            self.fail(field, f'must be null or a JPEG or PNG in assets/{folder}/, named in lowercase letters, '
                             f'digits and hyphens, like {example} (got {json.dumps(value, ensure_ascii=False)})')
        elif not (root / value).is_file():
            self.fail(field, f'{value} does not exist; add the file to assets/{folder}/')

    def unique(self, values, where, what):
        seen = set()
        for value in values:
            if not isinstance(value, str):
                continue  # already reported as missing or not text
            if value in seen:
                self.fail(where, f'duplicate {what} "{value}"')
            seen.add(value)

    def plain_text(self, value, where):
        """Walk the whole file: every string must be plain text, not HTML."""
        if isinstance(value, dict):
            for key, item in value.items():
                self.plain_text(item, _at(where, key))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                self.plain_text(item, f'{where}[{i}]')
        elif isinstance(value, str) and LOOKS_LIKE_HTML.search(value):
            self.fail(where, 'contains HTML markup or an entity; write plain text with real characters')


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate key "{key}"')
        result[key] = value
    return result


def _read(data_dir, filename):
    path = data_dir / filename
    try:
        with open(path, encoding='utf-8-sig') as f:  # -sig: a BOM from a Windows editor is fine
            return json.load(f, object_pairs_hook=_reject_duplicate_keys)
    except FileNotFoundError:
        raise BuildError(f'data/{filename}: file not found') from None
    except ValueError as e:  # bad JSON, bad UTF-8, or a duplicate key
        raise BuildError(f'data/{filename}: {e}') from None


def _check_practice(c, raw, root):
    p = c.obj(raw, TOP, ('name', 'legal_name', 'opened', 'doctor', 'phone', 'fax', 'email', 'address', 'geo',
                         'maps_url', 'building_photo', 'social', 'recipe_book_url', 'site_url', 'booking_url',
                         'in_network', 'forms'))
    c.text(p, 'name', TOP)
    c.text(p, 'legal_name', TOP)
    # The month the practice opened, YYYY-MM: the home page counts the years from it.
    opened = c.text(p, 'opened', TOP)
    if opened and not OPENED.fullmatch(opened):
        c.fail('opened', f'must be the year and month, like 2001-07 (got "{opened}")')
    fax = c.text(p, 'fax', TOP)
    if fax and not SHOWN_NUMBER.fullmatch(fax):
        c.fail('fax', f'must be written like 248-555-0123 (got "{fax}")')
    address = c.text(p, 'address', TOP)
    if address and not ADDRESS.fullmatch(address):
        c.fail('address', f'must read "street, city, ST 12345", like "5896 Dixie Hwy, Ste A, '
                          f'Clarkston, MI 48346" (got "{address}")')
    # The map pin's coordinates, for search engines (seo.py). They must match the pin in
    # maps_url when the link has one.
    geo = c.obj(p.get('geo'), 'geo', ('latitude', 'longitude'))
    coordinates = []
    if isinstance(p.get('geo'), dict):
        for key, limit in (('latitude', 90), ('longitude', 180)):
            value = geo.get(key)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not -limit <= value <= limit:
                c.fail(f'geo.{key}', f'must be a number from -{limit} to {limit} (got {json.dumps(value)})')
            else:
                coordinates.append(value)
    maps_url = c.url(p, 'maps_url', TOP)
    pin = MAP_PIN.search(maps_url or '')
    if pin and len(coordinates) == 2 and any(
            abs(float(pin[i + 1]) - coordinates[i]) > 1e-6 for i in range(2)):
        c.fail('geo', f'does not match the pin in maps_url ({pin[1]}, {pin[2]}); copy those numbers '
                      f'into latitude and longitude')
    email = c.text(p, 'email', TOP)
    if email and '@' not in email:
        c.fail('email', f'not an email address (got "{email}")')
    # The front of the office (home page and contact page). Until there is one, both show a
    # drawing of a map pin in its place.
    c.photo(p, 'building_photo', TOP, 'office', root)
    # The doctor's headshot (home and about pages), 4:5 like the team's; null shows his initials.
    doctor = c.obj(p.get('doctor'), 'doctor', ('name', 'credentials', 'photo'))
    c.text(doctor, 'name', 'doctor')
    c.text(doctor, 'credentials', 'doctor')
    c.photo(doctor, 'photo', 'doctor', 'team', root)
    phone = c.obj(p.get('phone'), 'phone', ('display', 'tel'))
    display = c.text(phone, 'display', 'phone')
    if display and not SHOWN_NUMBER.fullmatch(display):
        c.fail('phone.display', f'must be written like 248-555-0123 (got "{display}")')
    tel = c.text(phone, 'tel', 'phone')
    if tel and not TEL.fullmatch(tel):
        c.fail('phone.tel', f'must be +1 and the 10-digit number, digits only, like +12485550123 (got "{tel}")')
    elif tel and display and SHOWN_NUMBER.fullmatch(display) and display.replace('-', '') != tel[2:]:
        c.fail('phone', f'display "{display}" and tel "{tel}" are different numbers')
    c.url(p, 'recipe_book_url', TOP)
    site_url = c.text(p, 'site_url', TOP)
    if site_url and not SITE_URL.fullmatch(site_url):
        c.fail('site_url', f'must be just https:// and the domain, in lowercase, with no path or '
                           f'trailing slash, like https://example.com (got "{site_url}")')
    # The online booking page. When set, the contact page's appointment section leads with a
    # "Book online" button and the /card page (business-card QR code) sends people here;
    # null means /card goes to the contact page.
    if 'booking_url' not in p:
        c.fail('booking_url', 'missing (use null to send /card to the contact page)')
    elif p['booking_url'] is not None:
        booking = p['booking_url']
        if not isinstance(booking, str) or not WEB_ADDRESS.fullmatch(booking):
            c.fail('booking_url', f'must be null or an https:// address with a domain and no spaces, '
                                  f'like https://example.com/book (got {json.dumps(booking, ensure_ascii=False)})')
    # The insurance plans the practice is in-network with, in the order the pages list them
    # (home page and new patients page).
    plans = c.items(p.get('in_network'), 'in_network')
    for i, plan in enumerate(plans):
        if not isinstance(plan, str) or not plan.strip():
            c.fail(f'in_network[{i}]', 'must be non-empty text, the plan\'s name')
    c.unique([plan for plan in plans if isinstance(plan, str)], 'in_network', 'plan')
    social = c.obj(p.get('social'), 'social', ('facebook', 'instagram'))
    c.url(social, 'facebook', 'social')
    c.url(social, 'instagram', 'social')
    # The new-patient intake PDFs, kept in forms/ and linked from the home and new-patients pages.
    forms = c.obj(p.get('forms'), 'forms', ('adult', 'child'))
    for key in ('adult', 'child'):
        path = c.text(forms, key, 'forms')
        if path and not FORM_PATH.fullmatch(path):
            c.fail(f'forms.{key}', f'must be a PDF in the forms/ folder, like forms/new-patient-adult.pdf, '
                                   f'named in lowercase letters, digits and hyphens (got "{path}")')
        elif path and not (root / path).is_file():
            c.fail(f'forms.{key}', f'{path} does not exist; add the file to the forms/ folder')


def _check_nav(c, raw, pages):
    hrefs = []
    for i, entry in enumerate(c.items(raw, TOP)):
        where = f'[{i}]'
        entry = c.obj(entry, where, ('label', 'footer_label', 'href', 'header'))
        c.text(entry, 'label', where)
        c.text(entry, 'footer_label', where, optional=True)
        # "header": false keeps a page out of the header menu; the footer lists every entry.
        if 'header' in entry and not isinstance(entry['header'], bool):
            c.fail(f'{where}.header', 'must be true or false (leave it out for true)')
        href = c.text(entry, 'href', where)
        if href and href.split('#')[0] not in pages:
            c.fail(f'{where}.href', f'"{href}" is not a page this build generates ({", ".join(sorted(pages))})')
        hrefs.append(href)
    c.unique(hrefs, TOP, 'href')


def _check_hours(c, raw):
    days = c.items(raw, TOP)
    names = [d.get('day') for d in days if isinstance(d, dict)]
    if names != DAYS:
        c.fail(TOP, f'needs exactly one entry per day, in order {", ".join(DAYS)}')
    for i, day in enumerate(days):
        where = f'[{i}]'
        day = c.obj(day, where, ('day', 'hours'))
        previous_close = None
        for j, session in enumerate(c.items(day.get('hours'), f'{where}.hours', allow_empty=True)):
            at = f'{where}.hours[{j}]'
            session = c.obj(session, at, ('open', 'close'))
            times = {}
            for key in ('open', 'close'):
                value = c.text(session, key, at)
                if value and not TIME.fullmatch(value):
                    c.fail(f'{at}.{key}', f'must be 24-hour HH:MM, like 07:30 or 18:00 (got "{value}")')
                elif value:
                    times[key] = value  # zero-padded HH:MM compares correctly as text
            opens, closes = times.get('open'), times.get('close')
            if opens and closes and opens >= closes:
                c.fail(at, 'must close after it opens')
            if opens and previous_close and opens < previous_close:
                c.fail(at, 'overlaps the hours before it')
            previous_close = closes


def _check_services(c, raw, root):
    s = c.obj(raw, TOP, ('home_cards', 'services', 'products'))
    # Each service has an id, its card's anchor on the services page (services#massage); each
    # home page card links to one of them with "service".
    services = c.items(s.get('services'), 'services')
    service_ids = []
    for i, entry in enumerate(services):
        where = f'services[{i}]'
        entry = c.obj(entry, where, ('id', 'icon', 'title', 'summary'))
        sid = c.text(entry, 'id', where)
        if sid and not SLUG.fullmatch(sid):
            c.fail(f'{where}.id', f'use lowercase letters, digits and hyphens (got "{sid}")')
        service_ids.append(sid)
        c.icon(entry, 'icon', where)
        c.text(entry, 'title', where)
        c.text(entry, 'summary', where)
    c.unique(service_ids, 'services', 'id')
    c.unique([e.get('title') for e in services if isinstance(e, dict)], 'services', 'title')
    cards = c.items(s.get('home_cards'), 'home_cards')
    for i, entry in enumerate(cards):
        where = f'home_cards[{i}]'
        entry = c.obj(entry, where, ('icon', 'title', 'summary', 'service'))
        c.icon(entry, 'icon', where)
        c.text(entry, 'title', where)
        c.text(entry, 'summary', where)
        target = c.text(entry, 'service', where)
        if target and target not in service_ids:
            c.fail(f'{where}.service', f'"{target}" is not the id of a service in "services" '
                                       f'({", ".join(i for i in service_ids if isinstance(i, str))})')
    c.unique([e.get('title') for e in cards if isinstance(e, dict)], 'home_cards', 'title')
    # Products: a name, an optional short note (what it is) and a photo, null until there is one.
    products = c.items(s.get('products'), 'products')
    for i, product in enumerate(products):
        where = f'products[{i}]'
        product = c.obj(product, where, ('name', 'note', 'photo'))
        c.text(product, 'name', where)
        c.text(product, 'note', where, optional=True)
        c.photo(product, 'photo', where, 'products', root)
    c.unique([p.get('name') for p in products if isinstance(p, dict)], 'products', 'name')


def _check_testimonials(c, raw):
    """Returns the testimonial ids, for home-quotes.json."""
    t = c.obj(raw, TOP, ('categories',))
    category_ids, testimonial_ids = [], []
    for i, category in enumerate(c.items(t.get('categories'), 'categories')):
        where = f'categories[{i}]'
        category = c.obj(category, where, ('id', 'label', 'testimonials'))
        cid = c.text(category, 'id', where)
        if cid and not SLUG.fullmatch(cid):
            c.fail(f'{where}.id', f'use lowercase letters, digits and hyphens (got "{cid}")')
        category_ids.append(cid)
        c.text(category, 'label', where)
        for j, item in enumerate(c.items(category.get('testimonials'), f'{where}.testimonials')):
            at = f'{where}.testimonials[{j}]'
            item = c.obj(item, at, ('id', 'quote', 'author'))
            tid = c.text(item, 'id', at)
            if tid and not SLUG.fullmatch(tid):
                c.fail(f'{at}.id', f'use lowercase letters, digits and hyphens (got "{tid}")')
            testimonial_ids.append(tid)
            quote = c.text(item, 'quote', at)
            if quote and WRAPPED.fullmatch(quote):
                c.fail(f'{at}.quote', 'is wrapped in quote marks; leave them out (the page adds its own)')
            elif quote and STRAIGHT_QUOTES.search(quote):
                c.fail(f'{at}.quote', 'has a straight \' or "; use ’ for apostrophes and ‘ ’ or “ ” for quotes')
            c.text(item, 'author', at)
    c.unique(category_ids, 'categories', 'id')
    c.unique(testimonial_ids, 'categories', 'testimonial id')
    return {tid for tid in testimonial_ids if isinstance(tid, str)}


def _check_home_quotes(c, raw, testimonial_ids):
    ids = c.items(raw, TOP)
    for i, tid in enumerate(ids):
        if not isinstance(tid, str) or not tid.strip():
            c.fail(f'[{i}]', 'must be the id of a testimonial in testimonials.json')
        elif tid not in testimonial_ids:
            c.fail(f'[{i}]', f'unknown testimonial "{tid}" (use an id from testimonials.json)')
    c.unique([tid for tid in ids if isinstance(tid, str)], TOP, 'testimonial')


def _check_strings(c, raw, what):
    values = c.items(raw, TOP)
    for i, value in enumerate(values):
        if not isinstance(value, str) or not value.strip():
            c.fail(f'[{i}]', 'must be non-empty text')
    c.unique([v for v in values if isinstance(v, str)], TOP, what)


def _check_team(c, raw, root):
    t = c.obj(raw, TOP, ('staff', 'memberships'))
    staff = c.items(t.get('staff'), 'staff')
    for i, person in enumerate(staff):
        where = f'staff[{i}]'
        person = c.obj(person, where, ('name', 'credentials', 'title', 'photo', 'bio'))
        c.text(person, 'name', where)
        c.text(person, 'credentials', where, optional=True)
        c.text(person, 'title', where)
        c.text(person, 'bio', where, optional=True)
        # The headshot; null shows the person's initials in its place until there is one.
        c.photo(person, 'photo', where, 'team', root)
    c.unique([p.get('name') for p in staff if isinstance(p, dict)], 'staff', 'name')
    for i, membership in enumerate(c.items(t.get('memberships'), 'memberships')):
        where = f'memberships[{i}]'
        membership = c.obj(membership, where, ('icon', 'label'))
        c.icon(membership, 'icon', where)
        c.text(membership, 'label', where)


def _check_language_help(c, raw):
    """The notice of free language help in each language (nondiscrimination page and footer).
    Each text is copied from the source exactly, with {phone} and {tty} where it has blanks.
    edition is the year of the HHS text: 2024, or 2016 where HHS has no 2024 translation."""
    top = c.obj(raw, TOP, ('source', 'languages'))
    c.text(top, 'source', TOP)
    languages = c.items(top.get('languages'), 'languages')
    for i, entry in enumerate(languages):
        where = f'languages[{i}]'
        entry = c.obj(entry, where, ('language', 'name', 'lang', 'dir', 'edition', 'text'))
        c.text(entry, 'language', where)
        c.text(entry, 'name', where)
        lang = c.text(entry, 'lang', where)
        if lang and not LANG_TAG.fullmatch(lang):
            c.fail(f'{where}.lang', f'must be a language tag like es, ar or zh-Hant (got "{lang}")')
        if entry.get('dir') not in ('ltr', 'rtl'):
            c.fail(f'{where}.dir', 'must be "ltr" (left to right) or "rtl" (right to left, as in Arabic)')
        if entry.get('edition') not in ('2016', '2024'):
            c.fail(f'{where}.edition', 'must be "2024" or "2016", the year of the HHS translation')
        text = c.text(entry, 'text', where)
        if text:
            blanks = NOTICE_BLANK.findall(text)
            if blanks.count('{phone}') != 1 or any(b not in ('{phone}', '{tty}') for b in blanks) \
                    or blanks.count('{tty}') > 1:
                c.fail(f'{where}.text', 'must have {phone} once where the phone number goes, and at most one '
                                        '{tty}; no other {...} blanks')
    entries = [e for e in languages if isinstance(e, dict)]
    c.unique([e.get('lang') for e in entries], 'languages', 'lang')
    c.unique([e.get('language') for e in entries], 'languages', 'language')


def _namespace(value):
    """JSON objects become attribute-style namespaces so templates read site.practice.phone.display."""
    if isinstance(value, dict):
        return SimpleNamespace(**{k: _namespace(v) for k, v in value.items()})
    if isinstance(value, list):
        return [_namespace(v) for v in value]
    return value


def load(data_dir, pages):
    """Read and check every data file. `pages` is the set of filenames the build generates."""
    raw = {name: _read(data_dir, name) for name in (
        'practice.json', 'nav.json', 'hours.json', 'services.json',
        'testimonials.json', 'home-quotes.json', 'recipe-staples.json', 'team.json', 'language-help.json')}
    errors = []

    def checker(name):
        c = Checker(name, errors)
        c.plain_text(raw[name], '')
        return c

    _check_practice(checker('practice.json'), raw['practice.json'], data_dir.parent)
    _check_nav(checker('nav.json'), raw['nav.json'], pages)
    _check_hours(checker('hours.json'), raw['hours.json'])
    _check_services(checker('services.json'), raw['services.json'], data_dir.parent)
    testimonial_ids = _check_testimonials(checker('testimonials.json'), raw['testimonials.json'])
    _check_home_quotes(checker('home-quotes.json'), raw['home-quotes.json'], testimonial_ids)
    _check_strings(checker('recipe-staples.json'), raw['recipe-staples.json'], 'staple')
    _check_team(checker('team.json'), raw['team.json'], data_dir.parent)
    _check_language_help(checker('language-help.json'), raw['language-help.json'])
    if errors:
        raise BuildError('the data files have problems:\n  ' + '\n  '.join(errors))

    return SimpleNamespace(
        practice=_namespace(raw['practice.json']),
        nav=_namespace(raw['nav.json']),
        hours=_namespace(raw['hours.json']),
        services=_namespace(raw['services.json']),
        testimonials=_namespace(raw['testimonials.json']),
        home_quotes=_namespace(raw['home-quotes.json']),
        recipe_staples=raw['recipe-staples.json'],
        team=_namespace(raw['team.json']),
        language_help=_namespace(raw['language-help.json']),
    )
