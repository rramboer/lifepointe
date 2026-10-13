# Lifepointe Website — Design System

The website for Lifepointe Chiropractic & Wellness Center. Static HTML/CSS/JS; the nine
pages are generated (see Building below) so the shared chrome stays identical across all of
them.

## Concept
The page's structural device is the subject itself: **alignment**. A vertical "spine rail"
runs down the content gutter with one vertebra node per section. As the page scrolls, the
rail fills green, a small green point rides the fill's leading edge, and each node lights
(with a soft pop) as the fill reaches it: just as its section's eyebrow reaches a reading line
55% of the way down the window. A page opens with the fill at the first node, never halfway
down, and it catches up as you scroll; at the bottom of the page the whole rail is lit (grey
and static without JS). "Lifepointe" =
points along a line. Everything else stays quiet so the one signature element carries the
design.

## Color
The palette is the three official Pantone inks from the 2012 logo sheet, and nothing else.
The colors themselves never change; only how much of each is used. Every neutral is a tint
of the navy (navy mixed with white), so no new hue enters the palette. Shadows and glows are
navy or green at low opacity, never black.

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
| --section-y | clamp(2.5rem, 5vw, 4rem) | a section's top and bottom padding (40–64px); the rail's nodes sit level with each section's eyebrow from it |
| --wrap | 1480px | widest the content gets (55% of a 2560px-wide 27-inch monitor, 73% of a 1920px one); paragraphs stay narrower (`.measure`, 46em, or half a two-column section) so lines stay easy to read |

The primary button's hover adds a navy (or white, on dark) inner ring and lifts; the green
itself never shifts. On phones (540px and narrower) the buttons in the page content span
the column, so a stacked pair lines up and each is an easy thumb target; small buttons
(`.btn--sm`: the header's, the home card's Get directions) keep their size. The footer uses the same navy as `.section--navy` with a hairline top
border, so the closing CTA band and footer stay distinct without a second navy.

## Logo
`assets/logo-full-color.svg` (header) and `assets/logo-reversed.svg` (footer, on navy) are
cut from the original 2012 vector artwork and set to the exact inks above. The favicon is
the heart mark on a white tile so it reads in light and dark browser tabs.
`assets/apple-touch-icon.png` is the same mark on a solid white 180×180 square (iOS rounds
the corners itself, and fills transparent pixels with black): it is the icon for an iPhone
home-screen bookmark and for the small-card link preview in Messages. The full logo kit
(PNG/PDF/one-color versions) lives outside the repo in the brand folder.

## Type
- Display: **Bricolage Grotesque** 700/800 — `.display-1` (home h1) > `.display-page`
  (interior h1) > `.display-2` (section h2) > `.display-3` (card h3)
- Body/UI: **Lato** 400/700, 17px, 1.65 line-height
- Eyebrow: Lato 700, 12px, +.17em tracking, uppercase, with a short red tick before it — navy on light; green text and tick on dark
- Both are self-hosted from `assets/fonts/` (README.md, Fonts): only these four weights, no
  italics, and no request to Google

## Motion
Few, quiet, and each with a job; all of it in css/site.css and js/site.js, nothing loaded.
- **Hero entrance** (`.rise`): every page's opening lines fade up once on load, 100ms apart:
  the home hero, and the navy banner (eyebrow, title, line below, date) on every other page.
- **Spine rail** (see Concept): the fill, its point, and the nodes follow the scroll.
- **Scroll reveal** (`.reveal`): below the first screen, each section's blocks, and the cards,
  columns, quotes, and steps in its grids, fade up 14px the first time they scroll into view,
  70ms apart when they arrive together. Only what starts below the window is ever hidden, so
  nothing on screen blinks; print shows everything.
- **Hover**: link cards lift 3px, their icon tile turns navy with a white icon, and action
  arrows nudge 3px; buttons lift 1px. Keyboard focus gets the card's tile change too.
- **Header**: a soft navy shadow appears once the page has scrolled.

`prefers-reduced-motion` turns all of it off: no reveal (nothing is hidden), no entrance,
pop, or transitions; the rail still shows progress, without movement. No parallax, nothing
that moves on its own, no counters.

## Icons
Line icons on a 24-unit grid, 1.8 stroke, round ends, navy, in a 46px `--navy-tint` tile on
cards (40px in the contact panel). Lucide first; Tabler where it has the clearer picture
(massage, physiotherapist, apple, medical clipboard); the spine is drawn for the site in
the same style. One picture per meaning: no icon repeats within a grid of cards. Sources and
licenses: README.md, Icons.

## Rhythm
Sections are padded `--section-y` (40px on phones, up to 64px on desktop), interior page
heroes 36–52px and cards 20–26px: enough to separate things without leaving screens of
empty space. Post-heading gap `.mt-15` (1.5rem); pre-CTA / group gap `.mt-2` (2rem). No other inline
spacing — new one-offs should become classes.

## Pages
index, about, services, new-patients, success-stories, recipe-book, contact, plus the
footer's legal pages, privacy and accessibility. The practice's own pages and wording only,
nothing invented. Testimonials are taken verbatim from archived copies of the old site (typo
fixes only); entries that name former staff are left out, never edited. The site's own text
uses the serial (Oxford) comma in every list of three or more ("name, phone number, and
preferred times"), "&" lists too, and a comma before "and", "but" or "or" when it joins two
full clauses ("Send us a message, and a member of our team will reach out"); quoted text (testimonials, the CMS and HHS notices) stays as
written.
success-stories: topic chips jump to one section per category (heading = category name, one
vertebra each, alternating background, a "Back to topics" link). Quotes of uneven length flow
in up to three columns (`.quote-columns`), read top to bottom; the home page keeps three
cards in a row.
services: the products list runs in two columns where they fit (`.list-columns`), read top to
bottom, under a full-width heading.
contact: "Every way to say hello" is one panel (`.contact-panel`) of call, email, fax, and
address, split by hairlines: four columns on a desktop, 2×2 below 1180px, one column below
641px, so short items never sit in empty boxes. The email may break only before the @, and
the address keeps "Clarkston, MI 48346" on one line. The `#appointment` section pairs the hours table with a booking card: a green
"Call" button, a ghost "Email us" button (a mailto with the subject and a name / phone /
preferred times template filled in) and a note to leave health details out of email. When
practice.json has a `booking_url`, a green "Book online" button leads and Call turns ghost,
so the card keeps one primary action. No form, no embed: nothing on the site collects health
information or loads a third-party widget.
Shared header (sticky, green CTA → contact#appointment) + footer (navy-ink, white logo).
Home: the hero closes with a full-width row, under a hairline, that lists every in-network
insurance plan as text chips after an "In-network with" label (`.hero-plans`), where the old
site had insurer logos; the logos (VA seal, Medicare, Blue Cross Blue Shield) need permission to
use, and text stays readable and in the brand inks. All eight fit one line on screens about
1270px and wider; narrower, the chips wrap under the label.
The footer's Facebook and Instagram logos follow Meta's brand rules: the official shapes
(Facebook's whole disc with the "f" cut out, never the "f" alone), white, 29px (Instagram's
minimum), with half a glyph of clear space and no container shape. Hover never recolors them.
The closing CTA band is shared verbatim on five pages; new-patients tailors it ("Ready for
your first visit?") and contact omits it — deliberate: never CTA to the page you're on.
the legal pages (privacy, the Notice of Privacy Practices, accessibility, nondiscrimination,
Good Faith Estimate) omit it too: they are reference text, not sales pages. Each is plain prose
in a `.measure` column (h2 per section, `.display-3` h3 per topic, `.display-4` h4 inside a
topic, `.mt-2` between topics), with the "Last updated", "Last reviewed" or "Effective" date in
the hero (`.page-hero__meta`).
`/card` (the business-card QR code) is an unlisted redirect, not a page: logo, one line and a
green button with navy text, its few styles inline, nothing loaded from other sites (README.md).
`404.html` uses the shared header and footer with a short hero and two buttons, home (green)
and contact; its links start with `/` because GitHub Pages serves it at any depth.

## Floor
Skip link + `scroll-padding-top` clearing the sticky header, landmarks, aria-current nav,
focus-visible everywhere (navy on light, green on dark), AA contrast, reduced-motion kills all animation,
mobile nav = button + aria-expanded + focus-scoped Escape, hours table marks "(today)" for
screen readers, no horizontal scroll at 320px. Hamburger at 1179px and below (the desktop bar
needs ~1065px of content width, plus up to 17px for a desktop scrollbar); under user text
spacing the desktop menu wraps to a second row rather than pushing the button off-screen.
accessibility.html tells visitors about this floor; keep it in step.

## Building
`python3 build.py` builds the nine pages, the 404 page, `sitemap.xml`, `robots.txt` and the
`/card` redirect into `dist/` (see README.md). GitHub Actions runs the same build on every
pull request and every push to `main`, and deploys `main` to GitHub Pages (README.md,
Deploy). The generated HTML is never committed. Edit content in `data/*.json`, page markup
in `generator/pages/`, the shared header, footer and CTA band in `generator/layout.py`,
styling in css/site.css, behavior in js/site.js.
