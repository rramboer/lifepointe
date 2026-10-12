import html


def esc(value):
    """Escape a data value for HTML text or a quoted attribute. Use it on every value from data/."""
    return html.escape(str(value), quote=True)


_NUMBER_WORDS = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
                 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen',
                 'eighteen', 'nineteen', 'twenty')


def number_word(n):
    """A count for running text: spelled out up to twenty, digits above."""
    return _NUMBER_WORDS[n] if 0 <= n < len(_NUMBER_WORDS) else str(n)


def counted(n, singular, plural):
    """A count and its noun for running text: 'one category', 'fifteen categories'."""
    return f'{number_word(n)} {singular if n == 1 else plural}'
