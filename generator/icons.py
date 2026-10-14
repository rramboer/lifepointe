"""Inline SVG icons. Pages and data files refer to them by name: the keys of FILES and BRANDS.

Each icon in FILES is an SVG file in the repo's icons/ folder, kept exactly as its source
publishes it, so it can be checked against the original or updated by copying a newer file
over it. Each folder's LICENSE file travels with its icons:

  icons/lucide/      Lucide (lucide.dev), from lucide-static 1.48.0: ISC license, and MIT for
                     the icons Lucide took from Feather (listed in its LICENSE)
  icons/tabler/      Tabler Icons (tabler.io/icons), from @tabler/icons 3.48.0: MIT license
  icons/lifepointe/  drawn for this site on Lucide's 24-unit grid, in its style

The build keeps only the shapes in each file and draws them in the site's own style (_LINE):
a 1.8 stroke with round ends, hidden from screen readers. To add an icon, copy its SVG file
from the set into its folder unchanged and give it a name here.
"""
import xml.etree.ElementTree as ET
from functools import cache
from html import escape
from pathlib import Path

from .errors import BuildError

FOLDER = Path(__file__).resolve().parent.parent / 'icons'

_LINE = 'width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
# Arrows on action links, beside text rather than in a chip: 1em square (css/site.css .arrow),
# with a stroke as heavy as bold Lato's.
_ARROW = 'class="arrow{}" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"'
_ATTRS = {'arrow-right': _ARROW.format(''), 'arrow-up': _ARROW.format(' arrow--up')}

FILES = {
    # Service cards (data/services.json)
    'spine':       'lifepointe/spine.svg',
    'physio':      'tabler/physiotherapist.svg',
    'traction':    'lucide/unfold-vertical.svg',
    'scan':        'lucide/scan-line.svg',
    'report':      'tabler/report-medical.svg',
    'apple':       'tabler/apple.svg',
    'test-tube':   'lucide/test-tube-diagonal.svg',
    'massage':     'tabler/massage.svg',
    'footprints':  'lucide/footprints.svg',
    # Cards on the pages: the new patient forms and the recipe book
    'clip':        'lucide/clipboard-list.svg',
    'leaf':        'lucide/leaf.svg',
    # The about page's affiliations (data/team.json) and the home page's badge
    'shield':      'lucide/shield-check.svg',
    'heart':       'lucide/heart.svg',
    'users':       'lucide/users.svg',
    # Contact details, booking and downloads
    'phone':       'lucide/phone.svg',
    'mail':        'lucide/mail.svg',
    'fax':         'lucide/printer.svg',
    'calendar':    'lucide/calendar.svg',
    'pin':         'lucide/map-pin.svg',
    'download':    'lucide/download.svg',
    # Beside link text (_ARROW)
    'arrow-right': 'lucide/arrow-right.svg',
    'arrow-up':    'lucide/arrow-up.svg',
}

BRANDS = {
    # Official logo shapes, white on the navy footer, never recolored (Meta's brand rules for
    # Facebook and Instagram). Paths: Simple Icons 16.35.0 "facebook" and "instagram" (CC0),
    # tracings of the current logos; to match Meta byte for byte, swap in the paths from the files
    # in Meta's Brand Resource Center. Both fill their 24-unit box, so at 29px they meet
    # Instagram's 29x29px minimum. Facebook is the whole disc with the "f" cut out: Meta forbids
    # the "f" on its own.
    'facebook': '<svg width="29" height="29" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/></svg>',
    'instagram': '<svg width="29" height="29" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/></svg>',
}

NAMES = frozenset(FILES) | frozenset(BRANDS)
_SHAPES = {'path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon'}


@cache
def _shapes(name):
    """The shapes inside an icon's SVG file, as markup."""
    where = f'icons/{FILES[name]}'
    try:
        root = ET.parse(FOLDER / FILES[name]).getroot()
    except (OSError, ET.ParseError) as e:
        raise BuildError(f'{where}: can\'t read the icon ({e})') from None
    if root.get('viewBox') != '0 0 24 24':
        raise BuildError(f'{where}: the viewBox must be "0 0 24 24" (got "{root.get("viewBox")}")')
    shapes = []
    for shape in root:
        tag = shape.tag.rpartition('}')[2]
        if shape.get('stroke') == 'none':  # Tabler's invisible 24x24 frame
            continue
        if tag not in _SHAPES or len(shape):
            raise BuildError(f'{where}: <{tag}> isn\'t a simple shape; icons hold only {", ".join(sorted(_SHAPES))}')
        shapes.append(f'<{tag} ' + ' '.join(f'{k}="{escape(v)}"' for k, v in shape.attrib.items()) + '/>')
    if not shapes:
        raise BuildError(f'{where}: no shapes to draw')
    return ''.join(shapes)


def svg(name):
    """The bare <svg> for an icon name."""
    if name in BRANDS:
        return BRANDS[name]
    if name not in FILES:
        raise BuildError(f'unknown icon "{name}"')
    return f'<svg {_ATTRS.get(name, _LINE)}>{_shapes(name)}</svg>'


def icon(name, cls='card__icon'):
    """An icon in its round chip, as used at the top of cards."""
    return f'<div class="{cls}">{svg(name)}</div>'
