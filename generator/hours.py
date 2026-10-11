"""Office hours, rendered from data/hours.json as the full table and the footer summary.

Table: one row per open day; a run of closed days shares one row ("Fri–Sun  Closed").
Summary: days with identical hours share a line ("Mon, Wed, Thu: ..."); a run of three
or more days is written as a range ("Fri–Sun: closed").
"""
from .helpers import esc


def _js_day(index):
    """data/hours.json starts on Monday; JavaScript's getDay() counts Sunday as 0."""
    return (index + 1) % 7


def _clock(hhmm, always_minutes):
    hours, minutes = int(hhmm[:2]), int(hhmm[3:])
    suffix = 'am' if hours < 12 else 'pm'
    text = str(hours % 12 or 12)
    if minutes or always_minutes:
        text += f':{minutes:02d}'
    return text, suffix


def _span(session, always_minutes):
    """'7:30–11:30am', '2:30–6:00pm' (table) or '2:30–6pm' (summary)."""
    start, start_suffix = _clock(session.open, always_minutes)
    end, end_suffix = _clock(session.close, always_minutes)
    if start_suffix != end_suffix:
        start += start_suffix
    return f'{start}&ndash;{end}{end_suffix}'


def hours_table(days, cls='hours-table'):
    groups = []
    for index, day in enumerate(days):
        if not day.hours and groups and not groups[-1][-1][1].hours:
            groups[-1].append((index, day))
        else:
            groups.append([(index, day)])
    rows = []
    for group in groups:
        first, last = group[0][1], group[-1][1]
        label = esc(first.day) if len(group) == 1 else f'{esc(first.day[:3])}&ndash;{esc(last.day[:3])}'
        nums = ','.join(str(_js_day(index)) for index, _ in group)
        times = ' &nbsp;&bull;&nbsp; '.join(_span(s, True) for s in first.hours) or 'Closed'
        rows.append(f'        <tr data-days="{nums}"><th scope="row">{label}</th><td>{times}</td></tr>')
    rows_html = '\n'.join(rows)
    return f'''<table class="{cls}">
        <caption class="visually-hidden">Office hours by day</caption>
{rows_html}
      </table>'''


def hours_summary(days):
    """One line per set of identical hours, in order of the first day that has them."""
    groups = {}
    for index, day in enumerate(days):
        key = tuple((s.open, s.close) for s in day.hours)
        groups.setdefault(key, []).append(index)
    lines = []
    for key, indexes in groups.items():
        short = [esc(days[i].day[:3]) for i in indexes]
        consecutive = indexes == list(range(indexes[0], indexes[0] + len(indexes)))
        label = f'{short[0]}&ndash;{short[-1]}' if len(indexes) >= 3 and consecutive else ', '.join(short)
        times = ', '.join(_span(s, False) for s in days[indexes[0]].hours) or 'closed'
        lines.append(f'{label}: {times}')
    return lines
