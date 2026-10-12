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


_NUMBER_WORDS = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
                 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen',
                 'eighteen', 'nineteen', 'twenty')


def number_word(n):
    """A count for running text: spelled out up to twenty, digits above."""
    return _NUMBER_WORDS[n] if 0 <= n < len(_NUMBER_WORDS) else str(n)


def counted(n, singular, plural):
    """A count and its noun for running text: 'one category', 'fifteen categories'."""
    return f'{number_word(n)} {singular if n == 1 else plural}'
