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

## The funnel
The site's job is to bring in new patients: every page should leave a visitor one easy step
from calling or asking for an appointment, without shouting. The two actions are always the
same and always worded the same: **Request an appointment** (green, to `contact#appointment`)
and **Call 248-623-6107** (ghost, a `tel:` link).
- **Always within reach.** Desktop: the header's green button, with the phone number beside it
  from 1280px. Tablets: Call and Request in the header bar. Phones: an action bar fixed to the
  bottom of the screen (Call, Request), which slides away while the closing band or the
  contact page's appointment section shows the same two buttons.
- **At each moment of intent.** The home hero (with "Prefer the phone? Call …" under its
  buttons), the home page's first-visit section, the new patients and services heroes, the
  services page's "Not sure where to start?" prompt, and the closing band.
- **Trust before the ask.** The home page answers a new patient's questions in order: what
  this is and who it's for (hero, with the years in Clarkston and every in-network plan), what
  we do (each card linking to its service), how we think about care, who you'll see (Dr. Greg
  and the team, with faces), what patients say, what the first visit is like (four numbered
  steps and the forms), and where and when (hours with an "Open now" line, directions).
- **Green means the conversion.** Green buttons are only for Request, Call (where it leads),
  Book online, and a page's own main action (the recipe book, the 404's home link). Browsing
  links ("See all services & products", "Read more success stories") are ghost buttons.
- **The contact page leads with the ask.** Its first section is the appointment request and
  the office hours; every way to reach the office comes after.

## Color
The palette is the three official Pantone inks from the 2012 logo sheet, and nothing else.
The colors themselves never change; only how much of each is used. The page is a warm
off-white with white cards and heroes on it, which reads softer and more human than a cold
grey; text tiers, tiles and placeholders are tints of the navy, so no new hue enters the
palette. Shadows and glows are navy or green at low opacity, never black. The pages declare
`color-scheme: only light`, so a phone's automatic dark mode never recolors the inks.

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
| --ink-soft | #4A5470 | secondary text (7.3:1 on paper, 7.5:1 on white) |
| --paper | #F8F6F2 | page background, a warm off-white |
| --card | #ffffff | raised surfaces, the heroes |
| --line | #E4E1DC | borders, the rail |
| --navy-tint | #EEF1F6 | hover wash, icon tiles, initials, placeholders (navy 6%) |
| --navy-tint-2 | #E1E6EE | detail inside a placeholder (the map drawing's blocks) |
| --navy-muted / --navy-link / --navy-faint | #CCD2DE / #E6E9EF / #9EAAC1 | text tiers on navy (10.2 / 12.7 / 6.6 : 1) |
| --header-h | 4.75rem (76px) | header height; drives scroll-padding + sticky offsets |
| --section-y | clamp(2.5rem, 5vw, 4rem) | a section's top and bottom padding (40–64px); the rail's nodes sit level with each section's eyebrow from it |
| --wrap | 92.5rem (1480px) | widest the content gets; paragraphs stay narrower (`.measure`, 46em, or half a two-column section) so lines stay easy to read |
| --gutter | clamp(1.25rem, 4vw, 2.5rem) | the space beside the content (more on a notched phone held sideways) |
| --action-bar-h | 0, or the bar's height on phones | the footer's bottom padding and `scroll-padding-bottom`, so the action bar never hides content or keyboard focus |
| --radius / -lg / -xl | .75 / 1.25 / 1.75rem | tiles and chips / cards / photos |

**Big screens.** From 1600px wide, the root font size grows with the window, from the
reader's own size (16px by default) to 40% larger at about 3800px, and everything in rem grows
with it: at 2560px the text is 19px and the content 1757px wide (69% of a 27-inch monitor),
so a monitor or a TV across the room reads like a laptop. The reader's own text size setting
still scales everything.

The primary button's hover adds a navy (or white, on dark) inner ring and lifts; the green
itself never shifts. Buttons are at least 48px tall (small ones 44px). On phones (540px and
narrower) the buttons in the page content span the column, so a stacked pair lines up and each
is an easy thumb target; small buttons (`.btn--sm`: the header's, the home location card's
Get directions and Call) keep their size. Call buttons carry the phone icon. The footer uses the same navy as `.section--navy` with a hairline top
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
- Headings balance their lines (`text-wrap: balance`: no single word left on the last line);
  paragraphs avoid a lone last word (`pretty`). The home headline's two sentences each start a
  line.
- Both are self-hosted from `assets/fonts/` (README.md, Fonts): only these four weights, no
  italics, and no request to Google

## Motion
Few, quiet, and each with a job; all of it in css/site.css and js/site.js, nothing loaded.
- **Hero entrance** (`.rise`): every page's opening lines fade up once on load, 100ms apart:
  the home hero, and the light banner (eyebrow, title, line below, date, buttons) on every
  other page.
- **Spine rail** (see Concept): the fill, its point, and the nodes follow the scroll.
- **Scroll reveal** (`.reveal`): below the first screen, each section's blocks, and the cards,
  columns, quotes, and steps in its grids, fade up 14px the first time they scroll into view,
  70ms apart when they arrive together. Only what starts below the window is ever hidden, so
  nothing on screen blinks; print shows everything.
- **Hover** (pointers that hover only, so taps don't leave cards lifted): link cards lift 3px,
  their icon tile turns navy with a white icon, and action arrows nudge 3px; buttons lift 1px.
  Keyboard focus rings the whole card and gets the tile change too.
- **Header**: a soft navy shadow appears once the page has scrolled.
- **Action bar** (phones): slides down out of the way while the closing band or the contact
  page's appointment section is on screen, and back up after.

`prefers-reduced-motion` turns all of it off: no reveal (nothing is hidden), no entrance,
pop, or transitions; the rail still shows progress, without movement. No parallax, nothing
that moves on its own, no counters.

## Icons
Line icons on a 24-unit grid, 1.8 stroke, round ends, navy, in a 46px `--navy-tint` tile on
cards (40px in the contact panel). Buttons and file links carry a small one before their text
(phone, mail, download, pin). Lucide first; Tabler where it has the clearer picture
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
services: each service card has an id (`services#massage`), the target of the home page's
cards, and the one arrived at gets a green ring. After the services, a "Not sure where to
start?" prompt (`.callout`) offers Request and What to expect. Products are cards with a
square photo (or the placeholder) and the name, with what it is under it (`.product-grid`: two
across on phones, up to five on a desktop), then a link card to the recipe book, which left the
header menu for the footer.
contact: the first section (`#appointment`, where every Request button lands) pairs the
booking card, a green "Call" button, a ghost "Email us" button (a mailto with the subject and a
name / phone / preferred times template filled in) and a note to leave health details out of
email, with the office hours and their "Open now" line. When practice.json has a
`booking_url`, a green "Book online" button leads and Call turns ghost, so the card keeps one
primary action. Then "Every way to say hello": one panel (`.contact-panel`) of call, email
(with "Copy email address", since a mailto does nothing on a computer with no email program),
fax, and address, split by hairlines, 2×2 beside the office photo or its placeholder (a bigger
"Get directions" target for mouse and touch only) on a desktop, the photo below it under
1100px, one column below 641px. The email may break only before the @, and the address keeps
"Clarkston, MI 48346" on one line. No form, no embed: nothing on the site collects health
information or loads a third-party widget.
Shared header (sticky; see The funnel) + footer (navy-ink, white logo; its Explore list has
every page, the recipe book too). The menu is About, Services & products, New patients,
Success stories, Contact (`data/nav.json`; `"header": false` keeps an entry in the footer
only).
Home: the sections follow The funnel's order. The hero closes with a full-width row, under a hairline, that lists every in-network
insurance plan as text chips after an "In-network with" label (`.hero-plans`), where the old
site had insurer logos; the logos (VA seal, Medicare, Blue Cross Blue Shield) need permission to
use, and text stays readable and in the brand inks. All eight fit one line on screens about
1270px and wider; narrower, the chips wrap under the label.
The footer's Facebook and Instagram logos follow Meta's brand rules: the official shapes
(Facebook's whole disc with the "f" cut out, never the "f" alone), white, 29px (Instagram's
minimum), with half a glyph of clear space and no container shape. Hover never recolors them.
The closing CTA band is shared verbatim on five pages; new-patients tailors it ("Ready for
your first visit?") and contact omits it — deliberate: never CTA to the page you're on.
about: Dr. Greg's 4:5 portrait beside his words and background (on phones a small portrait
beside his name); the home page shows it too, with the team's faces before "Meet Dr. Greg and
the team". The team are cards 16rem wide (two across on phones) with a 4:5 headshot on top;
adding a photo never changes a card's size.
Photos the practice doesn't have yet keep their place (generator/media.py): a headshot shows
the person's initials on the navy tint; the office (home and contact, 16:10) shows a drawing
of streets and a map pin in the inks; a product shows the Lifepointe heart mark, faint
(`assets/mark.svg`, the favicon's mark in one color, used as a mask). Each turns into the
photo when its data field gets a path (README.md, Photos). Testimonials show the patient's
initials, decorative, beside their name.
the legal pages (privacy, the Notice of Privacy Practices, accessibility, nondiscrimination,
Good Faith Estimate) omit it too: they are reference text, not sales pages. Each is plain prose
in a `.measure` column (h2 per section, `.display-3` h3 per topic, `.display-4` h4 inside a
topic, `.mt-2` between topics), with the "Last updated", "Last reviewed" or "Effective" date in
the hero (`.page-hero__meta`).
`/card` (the business-card QR code) is an unlisted redirect, not a page: logo, one line and a
green button with navy text, its few styles inline, nothing loaded from other sites (README.md).
`404.html` uses the shared header and footer with a short hero and two buttons, home (green)
and contact; its links start with `/` because GitHub Pages serves it at any depth.
Every page opens with a light hero: white, a soft green glow in the top corner and a navy one
low on the other side, a hairline below. The navy is kept for the closing band and the
footer, so a page reads light to dark toward its ask.

## Floor
Skip link + `scroll-padding-top` clearing the sticky header (and `scroll-padding-bottom`
clearing the phones' action bar, which is also hidden from the keyboard while it is away),
landmarks (the action bar is a labeled nav), aria-current nav, focus-visible everywhere (navy
on light, green on dark; a link card's ring goes round the whole card), AA contrast,
reduced-motion kills all animation, mobile nav = a "Menu" button with a visible label +
aria-expanded + focus-scoped Escape, closing on a tap outside it or a choice inside it, and
scrolling on its own when taller than the screen. The hours table marks "(today)" for screen
readers, by the office's own time zone, and the "Open now" line is text, its dot only
repeating it. Buttons are 44px tall or more; smaller targets (topic chips, Copy email address,
footer links) still meet WCAG 2.2's 24px minimum or its spacing rule. No horizontal
scroll from 280px (a folded phone) to 3840px (a TV); content clears a notched phone's
corners held sideways (`viewport-fit=cover` with safe-area padding). Menu button at 1099px
and below (the desktop bar needs ~980px of content width, plus up to 17px for a desktop
scrollbar); under user text spacing the desktop menu wraps to a second row rather than
pushing the button off-screen.
accessibility.html tells visitors about this floor; keep it in step.

## Building
`python3 build.py` builds the nine pages, the 404 page, `sitemap.xml`, `robots.txt` and the
`/card` redirect into `dist/` (see README.md). GitHub Actions runs the same build on every
pull request and every push to `main`, and deploys `main` to GitHub Pages (README.md,
Deploy). The generated HTML is never committed. Edit content in `data/*.json`, page markup
in `generator/pages/`, the shared header, footer and CTA band in `generator/layout.py`,
styling in css/site.css, behavior in js/site.js.
