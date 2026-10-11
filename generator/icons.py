"""Inline SVG icons. Pages and data files refer to them by name."""
from .errors import BuildError

_LINE = 'width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICONS = {
 'spine':   f'<svg {_LINE}><circle cx="12" cy="4" r="1.7"/><circle cx="12" cy="9.3" r="1.7"/><circle cx="12" cy="14.6" r="1.7"/><circle cx="12" cy="20" r="1.7"/></svg>',
 'hand':    f'<svg {_LINE}><path d="M8 13V5.5a1.5 1.5 0 0 1 3 0V12"/><path d="M11 12V4.5a1.5 1.5 0 0 1 3 0V12"/><path d="M14 12V6a1.5 1.5 0 0 1 3 0v6"/><path d="M17 12v-1a1.5 1.5 0 0 1 3 0v4a7 7 0 0 1-7 7h-1a7 7 0 0 1-7-7v-2a1.5 1.5 0 0 1 3 0"/></svg>',
 'scan':    f'<svg {_LINE}><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/></svg>',
 'leaf':    f'<svg {_LINE}><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6C9.5 14.5 12 13 13 12"/></svg>',
 'arrows':  f'<svg {_LINE}><line x1="12" y1="3" x2="12" y2="9"/><polyline points="9 6 12 3 15 6"/><line x1="12" y1="15" x2="12" y2="21"/><polyline points="9 18 12 21 15 18"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
 'foot':    f'<svg {_LINE}><path d="M10 21c-2.6 0-4.2-2-4.2-5 0-4 2-7.5 4.2-7.5s4.2 3.5 4.2 7.5c0 3-1.6 5-4.2 5Z"/><circle cx="16.5" cy="6.5" r="1"/><circle cx="14" cy="4.5" r="1"/><circle cx="11" cy="3.8" r="1"/></svg>',
 'clip':    f'<svg {_LINE}><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4a3 3 0 0 1 6 0"/><line x1="9" y1="10" x2="15" y2="10"/><line x1="9" y1="14" x2="15" y2="14"/><line x1="9" y1="18" x2="13" y2="18"/></svg>',
 'shield':  f'<svg {_LINE}><path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10Z"/><polyline points="9 11.5 11.2 13.7 15.5 9.4"/></svg>',
 'heart':   f'<svg {_LINE}><path d="M19.5 12.6 12 20l-7.5-7.4a5 5 0 1 1 7.1-7.1l.4.3.4-.3a5 5 0 1 1 7.1 7.1Z"/></svg>',
 'phone':   f'<svg {_LINE}><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.8a2 2 0 0 1-.4 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.9.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>',
 'mail':    f'<svg {_LINE}><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
 'fax':     f'<svg {_LINE}><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8" rx="1"/></svg>',
 'pin':     f'<svg {_LINE}><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
 'download':f'<svg {_LINE}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
 'users':   f'<svg {_LINE}><circle cx="9" cy="8" r="3.5"/><path d="M2.5 21a6.5 6.5 0 0 1 13 0"/><circle cx="17.5" cy="9.5" r="2.5"/><path d="M16.5 15.2a5 5 0 0 1 5 4.8"/></svg>',
 'facebook': '<svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.1c0-.9.3-1.5 1.6-1.5h1.3V4.9c-.2 0-1-.1-1.9-.1-1.9 0-3.2 1.2-3.2 3.3V11H8.5v3h2.8v7h2.2z"/></svg>',
 'instagram': '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></svg>',
}


def svg(name):
    """The bare <svg> for an icon name."""
    if name not in ICONS:
        raise BuildError(f'unknown icon "{name}"')
    return ICONS[name]


def icon(name, cls='card__icon'):
    """An icon in its round chip, as used at the top of cards."""
    return f'<div class="{cls}">{svg(name)}</div>'
