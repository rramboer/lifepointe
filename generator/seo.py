"""What search engines and link previews read: canonical URLs, Open Graph tags, the home
page's schema.org JSON-LD, sitemap.xml and robots.txt.

Every address is built from practice.json site_url. A page's canonical URL is site_url + '/'
for the home page and site_url + '/<file>.html' for the rest, the same form as the site's own
links. The sitemap lists exactly the pages in pages.PAGES, so a new page is added there only.
"""
import json
import re
import struct
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xml_escape

from .data import ADDRESS
from .errors import BuildError
from .helpers import esc

HOME = 'index.html'
SITEMAP = 'sitemap.xml'
ROBOTS = 'robots.txt'
FILES = (SITEMAP, ROBOTS)
SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'

# The picture a shared link shows (Open Graph). The width and height are the file's own;
# check_images() stops the build if the file is missing or a different size.
SHARE_IMAGE = 'assets/photo-adjustment.jpg'
SHARE_IMAGE_SIZE = (1396, 930)
SHARE_IMAGE_ALT = 'A chiropractor examining a patient’s spine and posture by hand'
LOGO = 'assets/logo-full-color.svg'

# schema.org has no chiropractic type (Chiropractic is only a MedicineSystem value).
# MedicalBusiness ("a particular physical or virtual business of an organization for medical
# purposes") fits a chiropractic office best. Its subtypes are other specialties (Physician,
# Dentist, Physiotherapy, ...) or facility types that don't describe one: MedicalClinic ("a
# facility, often associated with a hospital or medical school"), Pharmacy.
BUSINESS_TYPE = 'MedicalBusiness'


def _image_size(path):
    """(width, height) from a JPEG's or PNG's header, or None if it is neither."""
    data = path.read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', data[16:24]) if len(data) >= 24 else None
    i = 2 if data[:2] == b'\xff\xd8' else len(data)
    while i + 9 <= len(data) and data[i] == 0xFF:
        marker = data[i + 1]
        if marker == 0xFF:  # fill byte before a marker
            i += 1
        elif 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):  # a frame header (SOFn)
            height, width = struct.unpack('>HH', data[i + 5:i + 9])
            return width, height
        elif marker == 0xDA:  # image data starts; every frame header comes before it
            break
        else:
            i += 2 + struct.unpack('>H', data[i + 2:i + 4])[0]
    return None


def check_images(root):
    """The files the tags and JSON-LD point at must exist, and the share image must be the
    size og:image:width and og:image:height state."""
    for path in (SHARE_IMAGE, LOGO):
        if not (root / path).is_file():
            raise BuildError(f'{path} is missing; generator/seo.py points search engines and link previews at it')
    size = _image_size(root / SHARE_IMAGE)
    if size is None:
        raise BuildError(f'{SHARE_IMAGE}: can\'t read its width and height; use a JPEG or PNG')
    if size != SHARE_IMAGE_SIZE:
        raise BuildError(f'{SHARE_IMAGE} is {size[0]}x{size[1]}, but SHARE_IMAGE_SIZE in generator/seo.py '
                         f'says {SHARE_IMAGE_SIZE[0]}x{SHARE_IMAGE_SIZE[1]}; update it, and the width and '
                         f'height wherever a page shows this file')


def canonical_url(site, filename):
    return f'{site.practice.site_url}/{"" if filename == HOME else filename}'


def head_tags(site, filename, title, description):
    """The canonical link plus Open Graph and Twitter card tags for an indexable page."""
    url = canonical_url(site, filename)
    width, height = SHARE_IMAGE_SIZE
    properties = [
        ('og:type', 'website'),
        ('og:site_name', site.practice.name),
        ('og:title', title),
        ('og:description', description),
        ('og:url', url),
        ('og:image', f'{site.practice.site_url}/{SHARE_IMAGE}'),
        ('og:image:width', width),
        ('og:image:height', height),
        ('og:image:alt', SHARE_IMAGE_ALT),
        ('og:locale', 'en_US'),
    ]
    tags = [f'<link rel="canonical" href="{esc(url)}">']
    tags += [f'<meta property="{name}" content="{esc(value)}">' for name, value in properties]
    tags.append('<meta name="twitter:card" content="summary_large_image">')
    return '\n  '.join(tags)


def _us_phone(number):
    """'+1-248-623-6107' from '+12486236107' or '248-623-6107' (data.py checks both)."""
    digits = re.sub(r'[^0-9]', '', number)[-10:]
    return f'+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}'


def _opening_hours(days):
    """One entry per opening session, with every day that has it. Closed days are left out:
    schema.org reads a day with no hours as closed."""
    sessions = {}
    for day in days:
        for session in day.hours:
            sessions.setdefault((session.open, session.close), []).append(day.day)
    return [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': names,
             'opens': f'{opens}:00', 'closes': f'{closes}:00'}
            for (opens, closes), names in sessions.items()]


def local_business(site):
    """The home page's <script type="application/ld+json"> describing the practice."""
    p = site.practice
    address = ADDRESS.fullmatch(p.address)
    data = {
        '@context': 'https://schema.org',
        '@type': BUSINESS_TYPE,
        'name': p.name,
        'url': canonical_url(site, HOME),
        'logo': f'{p.site_url}/{LOGO}',
        'image': f'{p.site_url}/{SHARE_IMAGE}',
        'telephone': _us_phone(p.phone.tel),
        'faxNumber': _us_phone(p.fax),
        'email': p.email,
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': address['street'],
            'addressLocality': address['city'],
            'addressRegion': address['region'],
            'postalCode': address['postal'],
            'addressCountry': 'US',
        },
        'geo': {'@type': 'GeoCoordinates', 'latitude': p.geo.latitude, 'longitude': p.geo.longitude},
        'hasMap': p.maps_url,
        'openingHoursSpecification': _opening_hours(site.hours),
        'sameAs': [p.social.facebook, p.social.instagram],
    }
    # Inside <script>, "</" could end the element early and "<!--" changes how it is parsed.
    # Both escapes are still valid JSON for the same text.
    text = (json.dumps(data, ensure_ascii=False, indent=2)
            .replace('</', '<\\/').replace('<!--', '<\\u0021--'))
    if json.loads(text) != data:
        raise BuildError('the home page JSON-LD does not read back as the data it was made from')
    return f'<script type="application/ld+json">\n{text}\n</script>'


def sitemap(site, filenames):
    """sitemap.xml listing the canonical URL of each page, in order."""
    urls = [canonical_url(site, filename) for filename in filenames]
    entries = '\n'.join(f'  <url><loc>{xml_escape(url)}</loc></url>' for url in urls)
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="{SITEMAP_NS}">\n{entries}\n</urlset>\n'
    try:
        locs = [loc.text for loc in ET.fromstring(xml.encode('utf-8')).iter(f'{{{SITEMAP_NS}}}loc')]
    except ET.ParseError as e:
        raise BuildError(f'{SITEMAP} is not valid XML: {e}') from None
    if locs != urls:
        raise BuildError(f'{SITEMAP} does not list the canonical URLs of the pages')
    return xml


def robots(site):
    """robots.txt: crawl everything, and here is the sitemap."""
    return f'''User-agent: *
Allow: /

Sitemap: {site.practice.site_url}/{SITEMAP}
'''
