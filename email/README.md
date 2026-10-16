# Lifepointe Chiropractic & Wellness Center: HTML email

`index.html` is a standalone, email-client-safe HTML template for Lifepointe Chiropractic &
Wellness Center. Paste its source into your email platform as a custom-HTML campaign (see
[Unsubscribe and preference links](#unsubscribe-and-preference-links) and the
[HIPAA note](#hipaa-note) before picking a platform).

`components.html` is a gallery of every block a Lifepointe email can use, each under a small grey
label: send it to yourself to see how every kind of content renders, and copy blocks from it into
a campaign (see [Components](#components)). It's a test file; never send it to patients.

`signatures/` holds the Gmail signatures for the office mailbox and Dr. Greg (see
[Signatures](#signatures)).

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
| Request an Appointment button (HTML and Outlook VML) | `https://lifepointechiro.com/contact#appointment` |
| New Patient Info button (HTML and Outlook VML) | `https://lifepointechiro.com/new-patients` |
| Phone (Visit or Call, and the footer, in white) | `tel:+12486236107` (shown as 248-623-6107) |
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
| `signature-logo.png` | 400×148 | Full-color logo on an opaque white background. **Used by the signatures**, shown at 200×74 |
| `icon-facebook.png` | 60×60 | Footer icon, shown at 30×30 |
| `icon-instagram.png` | 60×60 | Footer icon, shown at 30×30 |
| `icon-website.png` | 60×60 | Footer icon (globe), shown at 30×30 |

The logos are rendered from the original vector artwork in the official Pantone colors. They are
PNG rather than SVG because PNG works everywhere: Gmail rasterizes linked SVGs and classic Outlook
for Windows doesn't show them at all ([caniemail](https://www.caniemail.com/features/image-svg/)).

`signature-logo.png` is the logo kit's `lifepointe-logo-full-color.png`, cropped to the artwork,
flattened onto white, scaled to 368px wide with its aspect ratio kept, and centered on a 400×148
white canvas (16px of padding, 8px at display size). The colors are unchanged. The background is
opaque on purpose: some dark-mode mail apps, the Gmail iPhone app among them, darken the message
but leave images alone. A transparent logo's navy wordmark would then sit on a near-black
background, while this one shows as a small white card.

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
After editing any file in `email/`, run `python3 build.py` from the repo root (pull requests run
it too). It fails if a file here names the old website, its vendor's hosts or Google Fonts, or
breaks the practice's naming and phone-number rules (see the main README).

Send yourself a test before any real send. Gmail (web, iOS and Android), Outlook desktop and
Apple Mail cover most readers. Litmus or Email on Acid will render all of them at once if you
want to be thorough.

### Components
`components.html` holds every block, numbered and labeled, in the same markup as `index.html`
(same head, resets, 600px width, colors and Outlook buttons):

| # | Block | Notes |
|---|---|---|
| 1 | Preheader | The inbox preview line; write one per campaign |
| 2 | Top bar | Navy strip with "Clarkston, Michigan • Since 2001" |
| 3 | Logo header | With a text line that stays when images are off |
| 4 | Hero | Headline, paragraph, green button |
| 5 | Full-width image with caption | 520px wide, rounded corners |
| 6 | Text | Heading, subheading, paragraph, bold, inline link, small print |
| 7 | Bulleted list | Table-based, so Outlook lines the bullets up too |
| 8 | Numbered steps | Navy number badges |
| 9 | Buttons | Green (the one main action), navy (a second), outline (a quiet third), text link with an arrow |
| 10 | Two columns | Stack on phones |
| 11 | Image beside text | Stacks on phones, image on top |
| 12 | Three columns | Tinted cards; stack on phones |
| 13 | Testimonial | Patients' exact words with permission; red only for the quote mark |
| 14 | Notice box | Green edge on a tinted box, for closures and schedule changes |
| 15 | Event | Date badge, time and place, a link |
| 16 | Feature card on navy | Here the recipe book |
| 17 | Image as a link | For a video: email can't play one, so a still links to it |
| 18 | Divider and spacer | |
| 19 | Hours and contact | Same as `index.html` |
| 20 | Footer | Same as `index.html` |

Text marked "Example" is made up to show the layout; the rest is the practice's own wording from
the website. To build a campaign, copy the blocks you need into a copy of `index.html` and drop
the grey labels. Photos for a real campaign go in `images/` (their URLs must never change once
sent): the gallery borrows the website's photos from `/assets/`.

Columns stack on phones with the `.stack` class. A column that has side padding also gets
`.stack-pad` (padding becomes a gap below it) or, if it's the last one, `.stack-flush` (padding
removed), or it stays indented once stacked.

### Sending a test
`tools/send-test.py` emails `index.html` exactly as written, from the office@ mailbox:

```
python3 email/tools/send-test.py you@gmail.com
python3 email/tools/send-test.py you@gmail.com --file email/components.html --subject "Test: email components"
```

It asks for office@'s **app password** and keeps it in memory only (or set
`LIFEPOINTE_SMTP_PASSWORD` for that one command). `--dry-run` prints the message instead of
sending it. More addresses can follow the first, and `--subject`, `--file` and `--from`
are optional.

To make the app password: sign in to Google as office@, turn on **2-Step Verification**
(myaccount.google.com → Security; if Google won't allow it, the Admin console needs Security →
Authentication → 2-step verification → "Allow users to turn on 2-Step Verification"), then go to
myaccount.google.com/apppasswords, name it and click Create. Google shows the 16 characters
once. The app password opens the whole mailbox, which holds patient email: never save it in a
file or the repository, and delete it on the same page when it's no longer needed.

Don't test by pasting the page into Gmail's compose window, or by sending it through a tool
that cleans up HTML: they drop the images, the `<style>` block and the `tel:` links, so the
test shows a different email. Putsmail (putsmail.com) sends pasted HTML as written if the
script isn't an option.

## Signatures
Gmail HTML signatures that match the business card:

| File | For | Shows |
|---|---|---|
| `signatures/office.html` | The office mailbox | Logo · Lifepointe Chiropractic & Wellness Center · phone and fax · address · website |
| `signatures/dr-greg.html` | Dr. Greg | Logo · Dr. Greg Ramboer, D.C., CCWP · Lifepointe Chiropractic & Wellness Center · phone and fax · address · website |

- Each file is a standalone page that holds only the signature table, so it can be opened in a
  browser and copied. Everything is inline styles on tables, with no classes and no `<style>`
  (Gmail drops both).
- Font stack `Lato, Helvetica, Arial, sans-serif`. Navy `#00205B` text, `#4A5470` for Dr. Greg's
  credentials (as on the card), and a short red `#EE2737` accent bar above the name.
- Links: the logo and `lifepointechiro.com` go to `https://lifepointechiro.com`, and the phone
  number is `tel:+12486236107`. The fax number isn't linked.
- Under 400px wide, so it wraps on a narrow phone instead of scrolling. About 2,000 characters
  each, well under Gmail's 10,000-character limit
  ([Google help](https://support.google.com/mail/answer/8395)).
- No email address line: the sender's address is already in the From line.
- No confidentiality notice. If the practice wants one, have the wording reviewed and add it once
  for every mailbox with the Google Workspace **Append footer** setting (Admin console → Apps →
  Google Workspace → Gmail → Compliance → Append footer;
  [Google help](https://support.google.com/a/answer/176652)). Google adds it to outgoing mail
  itself, so it also covers mail sent from phones, and users can't change or remove it.

**The logo only shows once lifepointechiro.com is live.** Both signatures load
`https://lifepointechiro.com/email/images/signature-logo.png`. Gmail fetches images through
Google's image proxy, so the URL has to be public and HTTPS. Until the site is live on that domain
you'll see the alt text or a broken-image icon, in the browser and in Gmail, so install the
signatures once that URL opens in a browser.

### Install in Gmail (web)
1. Open the signature file in a desktop browser (double-click `office.html` or `dr-greg.html`).
2. Click on the page, press Ctrl+A (Cmd+A on a Mac) to select everything, then Ctrl+C (Cmd+C) to
   copy. The page holds nothing but the signature.
3. In Gmail: Settings (gear) → **See all settings** → **General** → **Signature** →
   **Create new**. Name it, click in the editor box and paste with Ctrl+V (Cmd+V). The editor
   doesn't accept HTML source, only a copy of the rendered page.
4. Check the paste: the logo should be about as big as in the browser (200px wide). If it comes in
   at double size, click it in the editor and pick a smaller size option (Small, Medium, Large or
   Original size; [Google help](https://support.google.com/mail/answer/11468381)).
5. Under **Signature defaults**, choose the new signature for **For new emails use** and
   **On reply/forward use**. If the mailbox sends as more than one address, set each address's
   default separately.
6. Tick **Insert signature before quoted text in replies and remove the "--" line that precedes
   it**, so the signature sits above the quoted thread.
7. Click **Save Changes** at the bottom of the page.
8. Send a test to an address outside the practice and check the logo and the links.

**Gmail app on phones:** leave the app's mobile signature empty (Android: Settings → the account →
Mobile signature; iPhone and iPad: Settings → Signature settings, with Mobile Signature off). With
none set, the app uses the signature from the computer
([Google help](https://support.google.com/mail/answer/8395)).

### Outlook
- To install: in classic Outlook for Windows, open a new message and go to Message → Signature →
  Signatures. In new Outlook and Outlook on the web, go to Settings → Accounts → Signatures. Paste
  the copied signature into the editor. A signature saved on one computer may not follow the
  account to another
  ([Microsoft help](https://support.microsoft.com/en-us/office/create-and-add-an-email-signature-in-outlook-8ee5d4f4-68fd-464a-a1c1-0e1c80bb27f2)).
- For recipients: classic Outlook blocks pictures by default, so many Outlook readers see the
  logo's alt text until they choose to download images. Every detail is live text, so nothing is
  lost. The logo has `width` and `height` attributes because classic Outlook ignores CSS sizes on
  images.

### Apple Mail
- Mac: Mail → Settings → Signatures, choose the account, click **+** and paste into the right-hand
  pane. Untick **Always match my default message font**, or Mail replaces the signature's fonts
  ([Apple help](https://support.apple.com/guide/mail/create-and-use-email-signatures-mail11943/mac)).
- Signatures are set per device. Mail on an iPhone or iPad has its own, in the device's Settings
  under Mail → Signature.

### Editing
- Change both files together. Their contact lines are identical and write the numbers the way
  the business card, the website and the email template do (248-623-6107 · Fax 248-623-6443).
- Keep every style inline. Gmail removes `<style>` blocks and classes when you paste.
- Keep `signature-logo.png` at the same path. Installed signatures and sent emails load it from
  there.
- After a change, install the signature again in each mailbox. Gmail keeps its own copy.
