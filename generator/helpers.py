import html


def esc(value):
    """Escape a data value for HTML text or a quoted attribute. Use it on every value from data/."""
    return html.escape(str(value), quote=True)
