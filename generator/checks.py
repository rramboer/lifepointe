"""Checks on the finished output folder. Any problem fails the build."""
import re
from html.parser import HTMLParser
from urllib.parse import unquote

# Text that must never appear anywhere in the published site. Each entry is a regular
# expression, matched case-insensitively against the whole of every text file. Add one to
# extend the list. Between words, (?:\s|&nbsp;|&#160;|&#xa0;)+ also catches no-break spaces
# and line breaks (\s matches U+00A0).
BANNED = [
    r'becky',
    r'\bdrs\.',
    r'gregory',
    r'mama',
    r'nursing(?:\s|&nbsp;|&#160;|&#xa0;)+pillow',
    r'deardoc',
    # The old appointment form's hosts. It loaded trackers and asked for health details.
    r'leadconnector',
    r'msgsndr',
    # The old website's file host.
    r'yourwebsite\.life',
    # The old website vendor's Vimeo account, and its video of the practice. Matching the bare
    # IDs catches every URL form: a link, an embed, a channel or showcase path, URL-encoded.
    r'user100634671(?!\d)',
    r'(?<!\d)737699204(?!\d)',
    # The old website's address. It is gone, and the site has its own privacy and accessibility
    # pages.
    r'lifepointechiropractic',
    # The icon site the old email footer hotlinked its icons from.
    r'flaticon',
    # Google Fonts' hosts: the site serves its own fonts from assets/fonts/, and a request to
    # Google sends the visitor's IP address to a third party. The privacy policy says the pages
    # load nothing from other sites.
    r'fonts\.(?:googleapis|gstatic)\.com',
    # The brand name is written with "&", and phone numbers as 248-623-6107 (data/practice.json),
    # not the old site's "Chiropractic and Wellness Center" or "(248) 623-6107". scan() also
    # catches the practice's own numbers written any other way, such as 248.623.6107.
    r'chiropractic(?:\s|&nbsp;|&#160;|&#xa0;)+and(?:\s|&nbsp;|&#160;|&#xa0;)+wellness(?:\s|&nbsp;|&#160;|&#xa0;)+center',
    r'\(248\)',
]

# What might sit between the parts of a phone number: hyphens and dashes, dots, slashes, a
# closing bracket, spaces and line breaks (\s matches U+00A0), and no-break space entities.
_NUMBER_GAP = r'(?:[-\u2010\u2011\u2013\u2014./)\s]|&nbsp;|&#160;|&#xa0;)*'


def _number_written_otherwise(shown):
    """A pattern for the number shown as '248-623-6107' written any other way: '248.623.6107',
    '248 623 6107', '2486236107', '(248) 623-6107' and so on. The one exception is the home
    page's JSON-LD, which gives search engines "+1-248-623-6107" (seo.py)."""
    area, exchange, line = shown.split('-')
    return re.compile(rf'(?<!"\+1-)(?<!\d)(?!{area}-{exchange}-{line}(?!\d))'
                      rf'{area}{_NUMBER_GAP}{exchange}{_NUMBER_GAP}{line}(?!\d)')


def _text(path):
    """The file's text, or None for a binary file (images, fonts, PDFs)."""
    raw = path.read_bytes()
    if b'\0' in raw[:8192]:
        return None
    try:
        return raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        return None


def scan(out, numbers=()):
    """Return ('file:line: ...' problems found under out, number of text files scanned).
    numbers are the practice's phone and fax numbers as data/practice.json writes them
    (248-623-6107); writing one any other way is a problem too."""
    patterns = [(re.compile(p, re.IGNORECASE), f'banned text /{p}/') for p in BANNED]
    patterns += [(_number_written_otherwise(shown), f'{shown} written another way (write {shown}, '
                  f'from data/practice.json)') for shown in numbers]
    problems = []
    scanned = 0
    for path in sorted(p for p in out.rglob('*') if p.is_file()):
        text = _text(path)
        if text is None:
            continue
        scanned += 1
        name = path.relative_to(out).as_posix()
        for pattern, why in patterns:
            for match in pattern.finditer(text):
                number = text.count('\n', 0, match.start()) + 1
                excerpt = ' '.join(text[max(match.start() - 40, 0):match.end() + 40].split())
                problems.append(f'{name}:{number}: {why} in "{excerpt}"')
    return problems, scanned


_CSS_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)
_CSS_URL = re.compile(r'url\(\s*(["\']?)([^"\')]*)\1\s*\)', re.IGNORECASE)
_SCHEME = re.compile(r'[a-z][a-z0-9+.-]*:', re.IGNORECASE)


def missing_css_files(out):
    """'file:line: ...' for each url() in the output's stylesheets that names a file the output
    doesn't have, such as a renamed font. A browser would just fall back to another font."""
    root = out.resolve()
    problems = []
    for css in sorted(out.rglob('*.css')):
        # Blank out comments, keeping their line breaks so line numbers stay right.
        text = _CSS_COMMENT.sub(lambda m: re.sub(r'[^\n]', ' ', m.group()),
                                css.read_text(encoding='utf-8-sig'))
        for match in _CSS_URL.finditer(text):
            url = match.group(2).strip()
            path = unquote(url.split('#')[0].split('?')[0])
            if not path or _SCHEME.match(url) or url.startswith('//'):
                continue  # data: URIs, other sites and #fragment references aren't files here
            target = (root / path.lstrip('/')) if path.startswith('/') else (css.parent / path)
            target = target.resolve()
            if root not in target.parents or not target.is_file():
                number = text.count('\n', 0, match.start()) + 1
                problems.append(f'{css.relative_to(out).as_posix()}:{number}: '
                                f'url("{url}") names no file in the output')
    return problems


# The privacy policy says the pages load nothing from other sites and that there are no forms.
# Elements that would put a form or another site's content on a page:
_NOT_ALLOWED = {'form', 'input', 'textarea', 'select', 'iframe', 'frame', 'frameset', 'embed',
                'object', 'portal'}
# Attributes whose URL the browser fetches, or sends a request to, without a click.
_LOADS = ('src', 'poster', 'data', 'background', 'ping', 'action', 'formaction')
_SRCSETS = ('srcset', 'imagesrcset')
# SVG elements that fetch their href: an image, a <use> of another file, a filter image, a script.
_SVG_HREF = {'image', 'use', 'feimage', 'script'}
# <link> types that fetch nothing: the canonical address and alternate versions of the page.
_LINK_NO_LOAD = {'canonical', 'alternate'}
_CSS_IMPORT = re.compile(r'@import\s+(["\'])([^"\']*)\1', re.IGNORECASE)  # @import url() is a url()


def _elsewhere(url, site_url):
    """Whether a browser would fetch url from another site. Browsers drop tabs and line breaks
    from a URL and read a backslash as a slash, so two backslashes start another site's address
    just as two slashes do."""
    url = re.sub(r'[\t\n\r]', '', url).strip().replace('\\', '/')
    if url == site_url or url.startswith(site_url + '/'):
        return False
    return url.startswith('//') or bool(re.match(r'(?:https?|wss?|ftp):', url, re.IGNORECASE))


def _css_loads(css, site_url):
    """(offset, url) for each @import and url() in css that loads from another site."""
    css = _CSS_COMMENT.sub(lambda m: re.sub(r'[^\n]', ' ', m.group()), css)
    for pattern in (_CSS_IMPORT, _CSS_URL):
        for match in pattern.finditer(css):
            if _elsewhere(match.group(2), site_url):
                yield match.start(), match.group(2).strip()


class _PageLoads(HTMLParser):
    """Collects (line, what) for each form, frame or embed, and each off-site load, in a page."""

    def __init__(self, site_url):
        super().__init__(convert_charrefs=True)
        self.site_url = site_url
        self.found = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        a = {name: value or '' for name, value in attrs}
        if tag in _NOT_ALLOWED:
            self.found.append((line, f'a <{tag}> element'))
        urls = [a[name] for name in _LOADS if name in a]
        for name in _SRCSETS:
            urls += [part.split()[0] for part in a.get(name, '').split(',') if part.strip()]
        if tag in _SVG_HREF:
            urls += [a[name] for name in ('href', 'xlink:href') if name in a]
        if tag in ('link', 'base') and 'href' in a:
            rels = set(a.get('rel', '').lower().split())
            if tag == 'base' or not rels or not rels <= _LINK_NO_LOAD:
                urls.append(a['href'])
        for url in urls:
            if _elsewhere(url, self.site_url):
                self.found.append((line, f'<{tag}> loads "{url[:80]}"'))
        for _, url in _css_loads(a.get('style', ''), self.site_url):
            self.found.append((line, f'a style attribute loads "{url[:80]}"'))
        self._in_style = tag == 'style'

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self._in_style = False

    def handle_endtag(self, tag):
        self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            line = self.getpos()[0]
            for offset, url in _css_loads(data, self.site_url):
                self.found.append((line + data.count('\n', 0, offset), f'<style> loads "{url[:80]}"'))


def offsite_loads(out, site_url):
    """'file:line: ...' for each thing in the output's pages, stylesheets and SVGs that makes a
    browser fetch something from another site as the page opens (a script, image, font,
    stylesheet, preconnect, frame or embed), and for each form or form field. Links people
    click, the canonical link, link-preview tags and the /card meta refresh may point anywhere.
    What a script does once it runs can't be checked here."""
    problems = []
    for path in sorted(p for p in out.rglob('*') if p.is_file()):
        suffix = path.suffix.lower()
        if suffix not in ('.html', '.htm', '.svg', '.css'):
            continue
        text = path.read_text(encoding='utf-8-sig')
        if suffix == '.css':
            found = [(text.count('\n', 0, offset) + 1, f'loads "{url[:80]}"')
                     for offset, url in _css_loads(text, site_url)]
        else:
            parser = _PageLoads(site_url)
            parser.feed(text)
            parser.close()
            found = parser.found
        problems += [f'{path.relative_to(out).as_posix()}:{line}: {what}' for line, what in found]
    return problems
