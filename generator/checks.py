"""Checks on the finished output folder. Any problem fails the build."""
import re
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
]

# Checked like BANNED, except in email/. Google Fonts' hosts: the site serves its own fonts
# from assets/fonts/, and a request to Google sends the visitor's IP address to a third party.
# The email template still loads Lato from Google. If that link goes, move this into BANNED.
BANNED_OUTSIDE_EMAIL = [
    r'fonts\.(?:googleapis|gstatic)\.com',
]


def _text(path):
    """The file's text, or None for a binary file (images, fonts, PDFs)."""
    raw = path.read_bytes()
    if b'\0' in raw[:8192]:
        return None
    try:
        return raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        return None


def scan(out):
    """Return ('file:line: ...' problems found under out, number of text files scanned)."""
    everywhere = [re.compile(p, re.IGNORECASE) for p in BANNED]
    outside_email = everywhere + [re.compile(p, re.IGNORECASE) for p in BANNED_OUTSIDE_EMAIL]
    problems = []
    scanned = 0
    for path in sorted(p for p in out.rglob('*') if p.is_file()):
        text = _text(path)
        if text is None:
            continue
        scanned += 1
        name = path.relative_to(out).as_posix()
        patterns = everywhere if name.startswith('email/') else outside_email
        for pattern in patterns:
            for match in pattern.finditer(text):
                number = text.count('\n', 0, match.start()) + 1
                excerpt = ' '.join(text[max(match.start() - 40, 0):match.end() + 40].split())
                problems.append(f'{name}:{number}: banned text /{pattern.pattern}/ in "{excerpt}"')
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
