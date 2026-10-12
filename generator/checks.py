"""Checks on the finished output folder. Any match fails the build."""
import re

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
    patterns = [re.compile(p, re.IGNORECASE) for p in BANNED]
    problems = []
    scanned = 0
    for path in sorted(p for p in out.rglob('*') if p.is_file()):
        text = _text(path)
        if text is None:
            continue
        scanned += 1
        for pattern in patterns:
            for match in pattern.finditer(text):
                number = text.count('\n', 0, match.start()) + 1
                excerpt = ' '.join(text[max(match.start() - 40, 0):match.end() + 40].split())
                problems.append(f'{path.relative_to(out).as_posix()}:{number}: '
                                f'banned text /{pattern.pattern}/ in "{excerpt}"')
    return problems, scanned
