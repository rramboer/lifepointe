# Lifepointe Chiropractic & Wellness Center: HTML email

`index.html` is a standalone, email-client-safe HTML template for Lifepointe Chiropractic &
Wellness Center. Paste its source into your email platform as a custom-HTML campaign (see
[Unsubscribe and preference links](#unsubscribe-and-preference-links) and the
[HIPAA note](#hipaa-note) before picking a platform).

All images load from the website by absolute URL
(`https://lifepointechiro.com/email/images/...`). Opening `index.html` in a browser previews the
layout, but the logo and icons only appear once the site is live on that domain with HTTPS. Until
then you'll see their alt text instead.

## What's in it
- 600px table-based layout, centered on a `#F0F2F5` background
- Hidden preheader text (the inbox preview line)
- Navy hero with a bulletproof VML/HTML button that also renders in Outlook desktop
- 2×2 services grid that stacks to one column under 600px
- Office hours, plus address, phone, fax and email
- Navy footer with self-hosted social icons and a text-link fallback
- Unsubscribe / preferences links (placeholders until a platform is chosen)

### Links
| Element | Goes to |
|---|---|
| Logo, globe icon, footer text link | `https://lifepointechiro.com/` |
| Request an Appointment button (HTML and Outlook VML) | `https://lifepointechiro.com/contact.html#appointment` |
| New Patient Info button (HTML and Outlook VML) | `https://lifepointechiro.com/new-patients.html` |
| Phone | `tel:+12486236107` (shown as 248-623-6107) |
| Email | `mailto:office@lifepointechiro.com` |
| Address | Google Maps listing |
| Facebook / Instagram | `facebook.com/lifepointewellness/` / `instagram.com/lifepointe.chiropractic/` |

Each button has two links, the normal `<a>` and the `href` on the `<v:roundrect>` that Outlook
desktop uses. Change both if a button's target changes.

## Images (`images/`)
Served by the website at `https://lifepointechiro.com/email/images/<file>`. Emails that have
already been sent keep loading these URLs, so **don't rename, move or delete these files**. To
change an image, replace the file under the same name (or add a new name for new campaigns).

| File | Size | Use |
|---|---|---|
| `lifepointe-logo.png` | 440×149 | Full-color logo for light backgrounds. **Used by the template**, shown at 220×74 |
| `lifepointe-logo-white.png` | 1320×441 | Reversed logo (white wordmark) for dark backgrounds. Not used by the template |
| `icon-facebook.png` | 60×60 | Footer icon, shown at 30×30 |
| `icon-instagram.png` | 60×60 | Footer icon, shown at 30×30 |
| `icon-website.png` | 60×60 | Footer icon (globe), shown at 30×30 |

The logos are rendered from the original vector artwork in the official Pantone colors. They are
PNG rather than SVG because PNG works everywhere: Gmail rasterizes linked SVGs and classic Outlook
for Windows doesn't show them at all ([caniemail](https://www.caniemail.com/features/image-svg/)).

### Social icons
White glyphs on transparent backgrounds, so they sit on the navy footer with no box around them:
- **Facebook:** a white disc with the "f" cut out, so the footer navy shows through the "f".
  Meta's rules forbid recoloring the Facebook logo to your own brand colors and using the "f"
  without its circle, so it stays white and complete
  ([Facebook logo guidelines](https://www.meta.com/brand/resources/facebook/logo/)).
- **Instagram:** the official glyph in white. Instagram allows the glyph in any solid color as long
  as its shape is unchanged, never smaller than 29×29px. It spans 29px at the 30px display size
  ([Instagram icon guidelines](https://about.meta.com/brand/resources/instagram/icons)).
- **Website:** a white globe outline (a generic icon, not a brand mark).

The cells have 8px of padding, so there are 16px between icons. That covers Facebook's clear
space (¼ of the logo's width) and Instagram's (½ of the glyph).

The Facebook and Instagram shapes are the official logos as traced by Simple Icons 16.35.0 (CC0),
the same paths the website footer uses. To match Meta's files byte for byte, download the white
versions from Meta's brand resource pages and swap their SVG paths into the script below.
Nothing else in the process changes.

**Regenerating the icons.** `tools/make-social-icons.js` draws the logos as inline SVG and
rasterizes them with [sharp](https://sharp.pixelplumbing.com/). It checks every output (60×60,
alpha channel, transparent corners, a transparent "f") and exits non-zero if a check fails.
Install sharp in a temporary folder **outside the repo**, so no `package.json` or `node_modules`
ends up here. This optional tool is the only thing in the repository that uses npm; the website
build never needs it. The command pins the sharp version that made the committed PNGs and skips
install scripts (sharp ships prebuilt binaries, so it needs none):

```sh
mkdir -p /tmp/icon-tools && (cd /tmp/icon-tools && npm install --ignore-scripts --no-save sharp@0.35.5)

# from the repo root: rewrites email/images/icon-*.png in place
NODE_TOOLS=/tmp/icon-tools node email/tools/make-social-icons.js

# optional: contact sheets on navy and white, written outside email/images
NODE_TOOLS=/tmp/icon-tools node email/tools/make-social-icons.js --preview /tmp/icon-preview
```

Other options: `--out DIR`, `--size N` (default 60), `--svg` (also write the SVG sources),
`--color #RRGGBB` (default white; keep Facebook white).

## Typography
Everything in the email uses one stack:
`'Lato', 'Helvetica Neue', Helvetica, Arial, sans-serif`. Lato is the website's body typeface.
Hierarchy comes from weight, size and letter-spacing rather than a second typeface.

| Element | Size / line-height | Weight | Tracking |
|---|---|---|---|
| H1 (hero) | 33 / 41 (26 / 34 on mobile) | 700 | −0.5px |
| H2 (section) | 23 / 31 (20 / 28 on mobile) | 700 | −0.3px |
| Eyebrow labels | 11–12 | 700 | +1.2 to +2.5px, uppercase |
| Body | 14–16 / 22–26 | 400 | normal |
| Buttons | 16 | 700 | normal |

The email loads no web font, so opening it sends no request to Google or any other font
service. Lato shows where it is installed on the reader's device; everywhere else the stack
falls back to Helvetica/Arial, which have close enough proportions that nothing reflows. Only
weights 400 and 700 are used, the brand's Lato weights. An `[if mso]` block forces Outlook
desktop onto Arial so it never defaults to Times.

## Brand colors (official Pantone inks, same tokens as the website)
| Role | Hex | Source |
|---|---|---|
| Navy: top bar, hero, headings, labels, secondary button, footer | `#00205B` | Pantone 281 C |
| Green: primary button (always with navy text, 6.8:1) | `#84BD00` | Pantone 376 C |
| Red: the logo heart only | `#EE2737` | Pantone 1788 C |
| Body text | `#4A5470` | navy-tinted neutral (7.5:1 on white) |
| Muted text / links / fine print on navy | `#CCD2DE` / `#E6E9EF` / `#9EAAC1` | navy tints, all AA on navy |
| Page background / dividers | `#F0F2F5` / `#E0E4EB` | navy tints |
| Footer icons | `#FFFFFF` | white glyphs |

Nothing outside this palette. See [`../DESIGN.md`](../DESIGN.md) for the full color rules.

## Unsubscribe and preference links
The footer has two placeholders, `{{UnsubscribeURL}}` and `{{PreferencesURL}}`. Replace them with
your platform's tags once the platform is chosen. CAN-SPAM requires a working opt-out and a
physical postal address on commercial email; the address is already in the footer
([FTC guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business)).

| Platform | Replace `{{UnsubscribeURL}}` with | Replace `{{PreferencesURL}}` with | Notes | Source |
|---|---|---|---|---|
| Mailchimp | `*\|UNSUB\|*` | `*\|UPDATE_PROFILE\|*` | Adds its own footer if `*\|UNSUB\|*` is missing. `*\|CURRENT_YEAR\|*` can replace the © year | [Merge tags](https://mailchimp.com/help/all-the-merge-tags-cheat-sheet/) |
| Brevo | `{{ unsubscribe }}` | `{{ update_profile }}` | Restores its own unsubscribe link if yours is missing | [Template language](https://help.brevo.com/hc/en-us/articles/360000946299), [unsubscribe link](https://help.brevo.com/hc/en-us/articles/209553645) |
| MailerLite | `{$unsubscribe}` | `{$preferences}` | The custom-HTML editor won't send without an unsubscribe link | [Variables](https://www.mailerlite.com/help/how-to-use-variables-in-mailerlite) |
| Kit | `{{ unsubscribe_url }}` | `{{ subscriber_preferences_url }}` | Kit templates are wrappers: the template must also contain `{{ message_content }}`, so it would need splitting into a wrapper and a body | [HTML templates](https://help.kit.com/en/articles/2810454-troubleshooting-html-email-templates) |

**Constant Contact** adds its own footer, with the address and the unsubscribe link, to every
custom-code email. Delete the template's Unsubscribe / Update preferences line (both links and the
dot between them) so readers don't get dead or duplicate links. Constant Contact also warns that
Outlook-only markup such as `<v:roundrect>` may not display correctly, so check both buttons in
its preview ([custom HTML emails](https://knowledgebase.constantcontact.com/articles/KnowledgeBase/34400-Create-an-Email-with-Custom-HTML-Code)).

**Gmail mail merge** (Google Workspace Business Standard or higher) adds its own unsubscribe link
to each message, so delete that line there too
([mail merge](https://support.google.com/mail/answer/12921167)).

The line above the links reads "You're receiving this email because you're on the mailing list for
Lifepointe Chiropractic & Wellness Center." It deliberately doesn't say the reader is a patient
(see the HIPAA note). Change it if your platform supplies its own permission reminder.

## HIPAA note
This is not legal advice; confirm with the practice's attorney before sending to patients.

- **A patient list is protected health information.** HIPAA's definition of health information
  covers information that relates to "the provision of health care to an individual", so a list
  of the practice's patients and their email addresses is PHI
  ([45 CFR 160.103](https://www.ecfr.gov/current/title-45/section-160.103)).
- **The sending platform then needs a BAA.** A vendor that stores or transmits PHI for the
  practice is a business associate under the same section, and the practice needs a signed
  business associate agreement (BAA) with it before uploading the list.
- **Mailchimp and Brevo exclude HIPAA use.** Mailchimp's terms say "If you're subject to
  regulations (like HIPAA) and you use the Service, then we won't be liable if the Service doesn't
  meet those requirements" ([terms](https://mailchimp.com/legal/terms/)), and its acceptable use
  policy forbids uploading "sensitive personal information regulated by applicable law"
  ([AUP](https://mailchimp.com/legal/acceptable_use/)). Brevo's terms say "You should not use the
  Services where your communications would be subject to … HIPAA"
  ([terms](https://www.brevo.com/legal/termsofuse/)).
- **MailerLite and Kit** say nothing about HIPAA or BAAs in their public terms
  ([MailerLite](https://www.mailerlite.com/legal/terms-of-service), [Kit](https://kit.com/terms)).
  Treat them as not suitable for a patient list unless they sign a BAA in writing.
- **Constant Contact signs a BAA:** its standard form only, requested from
  legal@constantcontact.com before you use the service. Only contact details and "the fact that
  the individuals on your email subscriber lists may have a relationship with your business" may
  be stored there ([BAA article](https://knowledgebase.constantcontact.com/articles/KnowledgeBase/6240-business-association-agreements)).
- **Gmail** is covered by Google's Workspace BAA once it is accepted in the Admin console
  ([Google HIPAA](https://workspace.google.com/terms/2015/1/hipaa_functionality/)).
- **Marketing the practice's own services** doesn't need patient authorization: communications
  about the covered entity's own health-related services are excluded from HIPAA's definition of
  marketing unless a third party pays for them
  ([45 CFR 164.501](https://www.ecfr.gov/current/title-45/section-164.501)).
- **In the content itself:** no details about any patient's care, and no lists segmented by
  condition (for example "back-pain patients").

A list made only of people who opted in through a sign-up form that collects just an email
address (and maybe a name) is not a patient list, but don't import the patient roster into it.

## Before you send
1. **The site is live.** `https://lifepointechiro.com/email/images/lifepointe-logo.png` and the
   three `icon-*.png` files open in a browser over HTTPS.
2. **The mailbox works.** `office@lifepointechiro.com` receives mail.
3. **The platform is chosen**, and if the list is patients, its BAA is signed (see above).
4. **Placeholders are replaced:** `{{UnsubscribeURL}}` and `{{PreferencesURL}}` swapped for the
   platform's tags, or the line deleted on Constant Contact and Gmail mail merge.
   `grep -n 'UnsubscribeURL\|PreferencesURL' email/index.html` should find nothing.
5. **The preheader** (hidden text at the top of `<body>`) matches this campaign and the subject
   line. On Mailchimp you can use `*|MC_PREVIEW_TEXT|*` and set it in the campaign instead.
6. **The copy is the practice's own wording.** Anything new is approved by Dr. Greg; no claims,
   statistics or testimonials are added; Dr. Greg is "Dr. Greg" or "Greg Ramboer", never a
   longer form of his first name; no information about any patient.
7. **The © year** in the footer is current.
8. **Every link works** (see [Links](#links)), including the Outlook VML button links.
9. **A test send looks right** in Gmail (web and phone app), Outlook desktop and Apple Mail, and
   with images turned off.

## Email best practices already applied
- Inline styles everywhere. The `<style>` block only holds resets and media queries, which is the
  safe split because some clients strip `<style>`.
- Tables for layout; no flexbox or grid; no external CSS or web fonts. The only external
  requests are the images, all on lifepointechiro.com (see Typography above).
- One typeface throughout.
- Every image has `alt` text, styled so it stays readable when images are blocked, and the
  footer repeats the icon links as text.
- `role="presentation"` on layout tables so screen readers skip them.
- Apple and Gmail auto-link detection is suppressed on plain-text phone numbers and addresses
  (`.unstyle-auto-detected-links`). The class goes only on plain text, never on an element that
  holds the template's own links, or its reset would strip their color, weight and underline.
- Absolute URLs with `target="_blank"` on every link.
- `tel:` and `mailto:` links for one-tap contact on phones.

## Testing
Send yourself a test before any real send. Gmail (web, iOS and Android), Outlook desktop and
Apple Mail cover most readers. Litmus or Email on Acid will render all of them at once if you
want to be thorough.
