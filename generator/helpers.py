import html
from urllib.parse import quote


def esc(value):
    """Escape a data value for HTML text or a quoted attribute. Use it on every value from data/."""
    return html.escape(str(value), quote=True)


def page_href(target, base=''):
    """The link to one of the site's pages, from its file name and an optional #section:
    'about.html#team' -> 'about#team'. Links leave out .html: GitHub Pages (and preview.py)
    serve about.html at /about. The home page is the site's root, './' or base. The result is
    a URL, not HTML: pass a value from data/ through esc()."""
    filename, hash_, fragment = target.partition('#')
    if filename == 'index.html':
        path = base or './'
    else:
        path = base + (filename[:-len('.html')] if filename.endswith('.html') else filename)
    return path + hash_ + fragment


def in_series(items):
    """Items joined for running text, with the serial comma: 'A', 'A and B', 'A, B, and C'.
    Items are HTML already, so escape data values first."""
    items = list(items)
    if len(items) < 3:
        return ' and '.join(items)
    return ', '.join(items[:-1]) + ', and ' + items[-1]


def language_anchor(lang):
    """The id of a language's notice of free language help on the nondiscrimination page:
    'lang-es', 'lang-zh-hant'. The footer links to it."""
    return 'lang-' + lang.lower()


def mailto(address, subject='', body=''):
    """A mailto: link (RFC 6068) that opens a new email with the subject and body filled in.

    Every part is percent-encoded (spaces as %20, never +) and every line break in the body
    (LF, CRLF or a lone CR) is written as CRLF, as the RFC asks. The result is a URL, not
    HTML: pass it through esc() like any value.
    """
    fields = []
    if subject:
        fields.append('subject=' + quote(subject, safe=''))
    if body:
        lines = body.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        fields.append('body=' + quote('\r\n'.join(lines), safe=''))
    return 'mailto:' + quote(address, safe='@+') + ('?' + '&'.join(fields) if fields else '')
