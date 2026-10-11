# Lifepointe Website — Design System

The website for Lifepointe Chiropractic & Wellness Center. Static HTML/CSS/JS; the seven
pages are generated (see Building below) so the shared chrome stays identical across all of
them.

## Concept
The page's structural device is the subject itself: **alignment**. A vertical "spine rail"
runs down the content gutter with one vertebra node per section; nodes light green as each
section enters view (IntersectionObserver; static without JS; motion killed by
`prefers-reduced-motion`). "Lifepointe" = points along a line. Everything else stays quiet
so the one signature element carries the design.

## Color
The palette is the three official Pantone inks from the 2012 logo sheet, and nothing else.
The colors themselves never change; only how much of each is used. Every neutral is a tint
of the navy (navy mixed with white), so no new hue enters the palette.

| Ink | Screen | Role | Rule |
|---|---|---|---|
| Navy, Pantone 281 C | `#00205B` | Primary. Headings, body text, links, dark sections, footer | Does most of the work (~28% of a page) |
| Green, Pantone 376 C | `#84BD00` | Action. Primary buttons, lit rail nodes, eyebrows and focus ring on dark | Always with navy text (6.8:1). White on green fails (2.3:1) |
| Red, Pantone 1788 C | `#EE2737` | Accent marks. The heart, active-nav underline, quote marks, eyebrow tick | Never text: white on red is 4.2:1, large text only |

Rule of thumb: **green means "do something", red means "this is Lifepointe"**.

## Tokens
| Token | Value | Use |
|---|---|---|
| --navy | #00205B | see above; also `--ink` |
| --green | #84BD00 | `.btn--primary`, rail nodes, on-dark eyebrows, on-dark focus ring |
| --red | #EE2737 | active nav underline, quote marks, `.eyebrow::before` tick |
| --ink-soft | #4A5470 | secondary text (7.5:1 on white) |
| --paper | #F7F8FA | page background (navy 3%) |
| --card | #ffffff | raised surfaces |
| --line | #E0E4EB | borders, the rail (navy 12%) |
| --navy-tint | #F0F2F5 | hover wash, icon chips (navy 6%) |
| --navy-muted / --navy-link / --navy-faint | #CCD2DE / #E6E9EF / #9EAAC1 | text tiers on navy (10.2 / 12.7 / 6.6 : 1) |
| --header-h | 76px | header height; drives scroll-padding + sticky offsets |

The primary button's hover adds a navy (or white, on dark) inner ring and lifts; the green
itself never shifts. The footer uses the same navy as `.section--navy` with a hairline top
border, so the closing CTA band and footer stay distinct without a second navy.

## Logo
`assets/logo-full-color.svg` (header) and `assets/logo-reversed.svg` (footer, on navy) are
cut from the original 2012 vector artwork and set to the exact inks above. The favicon is
the heart mark on a white tile so it reads in light and dark browser tabs. The full logo kit
(PNG/PDF/one-color versions) lives outside the repo in the brand folder.

## Type
- Display: **Bricolage Grotesque** 700/800 — `.display-1` (home h1) > `.display-page`
  (interior h1) > `.display-2` (section h2) > `.display-3` (card h3)
- Body/UI: **Lato** 400/700, 17px, 1.65 line-height
- Eyebrow: Lato 700, 12px, +.17em tracking, uppercase, with a short red tick before it — navy on light; green text and tick on dark

## Rhythm
Post-heading gap `.mt-15` (1.5rem); pre-CTA / group gap `.mt-2` (2rem). No other inline
spacing — new one-offs should become classes.

## Pages
index, about, services, new-patients, success-stories, recipe-book, contact. The practice's
own pages and wording only, nothing invented. Testimonials are taken verbatim from archived
copies of the old site (typo fixes only); entries that name former staff are left out, never
edited.
success-stories: topic chips jump to one section per category (heading = category name, one
vertebra each, alternating background, a "Back to topics" link). Quotes of uneven length flow
in up to three columns (`.quote-columns`), read top to bottom; the home page keeps three
cards in a row.
contact: the `#appointment` section pairs the hours table with a booking card: a green
"Call" button, a ghost "Email us" button (a mailto with the subject and a name / phone /
preferred times template filled in) and a note to leave health details out of email. When
practice.json has a `booking_url`, a green "Book online" button leads and Call turns ghost,
so the card keeps one primary action. No form, no embed: nothing on the site collects health
information or loads a third-party widget.
Shared header (sticky, green CTA → contact#appointment) + footer (navy-ink, white logo).
The closing CTA band is shared verbatim on five pages; new-patients tailors it ("Ready for
your first visit?") and contact omits it — deliberate: never CTA to the page you're on.
`/card` (the business-card QR code) is an unlisted redirect, not a page: logo, one line and a
green button with navy text, its few styles inline, nothing loaded from other sites (README.md).
`404.html` uses the shared header and footer with a short hero and two buttons, home (green)
and contact; its links start with `/` because GitHub Pages serves it at any depth.

## Floor
Skip link + `scroll-padding-top` clearing the sticky header, landmarks, aria-current nav,
focus-visible everywhere (navy on light, green on dark), AA contrast, reduced-motion kills all animation,
mobile nav = button + aria-expanded + focus-scoped Escape, hours table marks "(today)" for
screen readers, no horizontal scroll at 320px. Hamburger below 1081px (the desktop bar
needs ~976px of content width).

## Building
`python3 build.py` builds the seven pages, the 404 page, `sitemap.xml`, `robots.txt` and the
`/card` redirect into `dist/` (see README.md). GitHub Actions runs the same build on every
pull request and every push to `main`, and deploys `main` to GitHub Pages (README.md,
Deploy). The generated HTML is never committed. Edit content in `data/*.json`, page markup
in `generator/pages/`, the shared header, footer and CTA band in `generator/layout.py`,
styling in css/site.css, behavior in js/site.js.

## Known placeholders
- The footer privacy and accessibility links still point at the old website, through `legacy`
  in data/practice.json. A later change replaces them.
