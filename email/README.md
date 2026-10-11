# Lifepointe Chiropractic — HTML Email

`index.html` is a standalone, email-client-safe HTML template for Lifepointe Chiropractic and
Wellness Center. Open it in a browser to preview, or paste the source into your email platform
(Mailchimp, Constant Contact, Brevo, etc.) as a custom HTML campaign.

## What's in it
- 600px table-based layout, centered on a `#edf0f5` background
- Hidden preheader text (inbox preview line)
- Hero with a bulletproof VML/HTML button that renders in Outlook
- 2×2 services grid that stacks to one column under 600px
- Office hours + address/phone/email block
- Dark footer with social icons and a text-link fallback
- Unsubscribe / preferences links

## Logo files (`images/`)
| File | What it is |
|---|---|
| `lifepointe-logo.png` | 440×149, full-color logo for light backgrounds — **used by the email** (shown at 220×74) |
| `lifepointe-logo-white.png` | 1320×441, reversed logo (white wordmark) for dark backgrounds |

Both are rendered from the original 2012 vector artwork in the official Pantone colors (see
below), replacing the earlier versions that were recolored from a low-resolution WebP. PNG
rather than SVG because Gmail and Outlook don't render SVG images.

## Typography
Everything in the email uses one stack:
`'Lato', 'Helvetica Neue', Helvetica, Arial, sans-serif` — Lato being the typeface the website
itself runs on. Hierarchy comes from weight, size, and letter-spacing rather than a second
typeface, which is what keeps it looking like one designed piece instead of a template.

| Element | Size / line-height | Weight | Tracking |
|---|---|---|---|
| H1 (hero) | 33 / 41 | 900 | −0.5px |
| H2 (section) | 23 / 31 | 900 | −0.3px |
| Eyebrow labels | 11–12 | 700 | +1.2 to +2.5px, uppercase |
| Body | 15–16 / 25–26 | 400 | normal |
| Buttons | 16 | 700 | normal |

The heavy 900 headings deliberately echo the bold condensed wordmark in the logo. Lato loads via
Google Fonts for clients that support webfonts (Apple Mail, iOS, Outlook.com, Samsung); Gmail and
Outlook desktop fall back to Helvetica/Arial, which have close enough proportions that nothing
reflows. An `[if mso]` block forces Outlook desktop onto Arial so it never defaults to Times.

## Brand colors (official Pantone inks, same tokens as the website)
| Role | Hex | Source |
|---|---|---|
| Navy: header strip, hero, headings, labels, secondary button, footer | `#00205B` | Pantone 281 C |
| Green: primary button (always with navy text, 6.8:1) | `#84BD00` | Pantone 376 C |
| Red: the logo heart only | `#EE2737` | Pantone 1788 C |
| Body text | `#4A5470` | navy-tinted neutral (7.5:1 on white) |
| Muted text on navy / links on navy / fine print on navy | `#CCD2DE` / `#E6E9EF` / `#9EAAC1` | navy tints, all AA on navy |
| Page background / dividers | `#F0F2F5` / `#E0E4EB` | navy tints |

No gold, indigo or near-black: those came from the old DearDoc site, not the brand. See
`../lifepointe-website/DESIGN.md` for the full color rules.

## Before you send — three things to replace
1. **Logo — host it and use an absolute URL.** `images/lifepointe-logo.png` is referenced by a
   relative path so the file previews correctly in a browser. Email clients can't resolve
   relative paths — upload the PNG to your email platform's image host and replace the `src`
   with the full `https://` URL. Leave `width="220" height="83"` as-is.
2. **Social icons** (footer): currently hotlinked from flaticon's CDN. Self-host these —
   third-party CDNs can rate-limit or disappear, and self-hosted images look more trustworthy
   to spam filters. 60×60px PNGs displayed at 30×30.
3. **Unsubscribe links**: `{{UnsubscribeURL}}` and `{{PreferencesURL}}` are placeholders —
   replace with your platform's merge tags (Mailchimp uses `*|UNSUB|*`, Brevo uses
   `{{ unsubscribe }}`, etc.). CAN-SPAM requires a working unsubscribe on commercial email.

## Email best practices already applied
- Inline styles everywhere (Gmail strips `<style>` in some contexts; the `<style>` block only
  holds resets and media queries, which is the safe split)
- Tables for layout, no flexbox/grid, no external CSS or fonts
- One typeface throughout (see Typography below)
- Every image has `alt` text and the design still reads with images off
- `role="presentation"` on layout tables so screen readers skip them
- Apple/Gmail auto-link detection suppressed on the address and phone blocks
- Absolute URLs with `target="_blank"` on every link
- `tel:` and `mailto:` links for one-tap contact on mobile

## Testing
Send yourself a test before any real send. Gmail (web + iOS/Android), Outlook desktop, and
Apple Mail cover most of the audience. Litmus or Email on Acid will render all of them at once
if you want to be thorough.
