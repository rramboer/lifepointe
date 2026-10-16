"""Photos, and the placeholders that hold their place until the practice has them.

Each photo field in data/ is null until its file exists (data.py checks the path), and every
slot keeps its size either way, so adding a photo never moves anything:

  headshots (team, doctor)  4:5, the person's initials until there is one
  the office building       16:10, a drawing of a map pin until there is one
  products                  1:1, the Lifepointe heart mark, faint, until there is one

Placeholders are decorative (aria-hidden). Every photo sits beside a heading or text that
already names what it shows, so photos have alt="" too, except where noted.
"""
from .helpers import esc


def initials(name):
    """'Sybil Olson' -> 'SO', 'Dr. Greg Ramboer' -> 'GR', 'Cher' -> 'C'. Titles, lowercase
    words and anything in brackets are skipped."""
    words = [w for w in name.split('(')[0].split() if w[:1].isupper() and w.rstrip('.') not in ('Dr', 'Mr', 'Mrs', 'Ms')]
    if not words:
        return name[:1].upper()
    return words[0][0] + (words[-1][0] if len(words) > 1 else '')


def headshot(photo, name, cls='headshot', base='', eager=False, tag='div'):
    """A 4:5 headshot, or the person's initials in its place. tag='span' for one inside a link."""
    if photo:
        loading = '' if eager else ' loading="lazy"'
        inner = f'<img src="{base}{esc(photo)}" alt="" width="400" height="500"{loading}>'
    else:
        inner = f'<span class="headshot__initials">{esc(initials(name))}</span>'
    return f'<{tag} class="{cls}" aria-hidden="true">{inner}</{tag}>'


# A plain drawing of streets and a map pin, in the brand inks, for the office photo's place.
# It isn't a map of the area: the "Get directions" link beside it opens the real one.
MAP_ART = (
    '<svg class="map-art" viewBox="0 0 320 200" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
    '<rect class="map-art__ground" width="320" height="200"/>'
    '<g class="map-art__blocks">'
    '<rect x="14" y="14" width="74" height="54" rx="8"/><rect x="146" y="10" width="54" height="40" rx="8"/>'
    '<rect x="228" y="118" width="80" height="34" rx="8"/><rect x="236" y="164" width="72" height="30" rx="8"/>'
    '<rect x="16" y="120" width="70" height="66" rx="8"/><rect x="150" y="150" width="56" height="40" rx="8"/>'
    '</g>'
    '<ellipse class="map-art__park" cx="268" cy="40" rx="44" ry="26"/>'
    '<g class="map-art__roads">'
    '<path class="map-art__main" d="M-12 168 C 70 150 150 104 196 82 S 290 34 332 22"/>'
    '<path d="M112 -10 L 128 210"/><path d="M-10 96 L 330 110"/><path d="M216 -10 L 210 210"/>'
    '</g>'
    '<ellipse class="map-art__shadow" cx="168" cy="98" rx="13" ry="4"/>'
    '<path class="map-art__pin" d="M168 97 C 160 86 151 78 151 66 a17 17 0 0 1 34 0 c0 12 -9 20 -17 31 z"/>'
    '<circle class="map-art__dot" cx="168" cy="66" r="6.5"/>'
    '</svg>')


def building(photo, cls='place-photo', base=''):
    """The front of the office, 16:10, or the map drawing. The photo has a description, since
    it shows what to look for when you arrive."""
    if photo:
        return (f'<figure class="{cls}"><img src="{base}{esc(photo)}" alt="The front of the Lifepointe office" '
                f'width="1600" height="1000" loading="lazy"></figure>')
    return f'<div class="{cls} {cls}--placeholder">{MAP_ART}</div>'


def product_photo(photo, base=''):
    """A product's square photo, or the faint heart mark in its place."""
    if photo:
        return (f'<div class="product-card__photo"><img src="{base}{esc(photo)}" alt="" width="600" height="600" '
                f'loading="lazy"></div>')
    return '<div class="product-card__photo product-card__photo--placeholder" aria-hidden="true"></div>'
