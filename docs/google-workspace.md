# Google Workspace email for lifepointechiro.com

This runbook sets up `office@lifepointechiro.com` as the practice's mailbox, with `contact@` and
`info@` as free aliases on it. It covers the sign-up, the HIPAA Business Associate Amendment (BAA),
the DNS timing, and the move off `lifepointechiro@gmail.com`. The DNS values themselves live in
[dns.md](dns.md#all-records), and "row N" below refers to that table.

Prices, menu paths and quotes were checked on 10 Oct 2026 against the Google pages listed under
[Sources](#sources). Anything that could not be confirmed is marked **Unconfirmed**.

**Before you start:** `lifepointechiro.com` has to resolve. See [dns.md, step 1](dns.md#step-1-revert-the-nameservers).

## 0. Check for an existing Workspace account first

The old domain `lifepointechiropractic.com` has Google MX records and a `google-site-verification`
TXT record. That could mean someone once set up Google Workspace (or G Suite) for the practice. A
domain can belong to only one Workspace account, so check before signing up.

1. Open `https://www.google.com/a/lifepointechiropractic.com/ServiceLogin` in a browser. If the page says
   "Sorry, you've reached a login page for a domain that isn't using Google Workspace", no account
   uses it as its primary domain. That is what it said on 10 Oct 2026, and the same goes for
   `lifepointechiro.com`. For comparison, `google.com` shows a normal sign-in page. **Unconfirmed:**
   whether this check also catches a domain that is only a secondary or alias domain of another
   account.
2. Ask the office whether anyone ever had an `@lifepointechiropractic.com` mailbox or a Google Admin
   login. Also search `lifepointechiro@gmail.com` and the card statements for "Google Workspace",
   "G Suite" or "Google Apps".
3. Try signing in at <https://admin.google.com> with likely addresses such as
   `office@lifepointechiropractic.com` or `info@lifepointechiropractic.com`.
4. At sign-up (step 2), if Google says "This domain is already in use", an account exists.

The `google-site-verification=` record proves nothing on its own, because Search Console uses the
same format.

**If no account exists (the expected case):** sign up fresh in step 2.

**If an account exists:** don't create a second one.

1. Regain super admin access. Resetting the admin password "send[s] an email to the secondary email you
   provided when you signed up". If that's lost, use Google's form on
   [Can't sign up my domain](https://knowledge.workspace.google.com/admin/support/troubleshooting/cant-sign-up-my-domain-for-a-google-service).
   Support says it will "get back to you within 48 hours".
2. Check the edition. The legacy free edition (G Suite / "Google Apps Standard Edition") can't
   accept the BAA, so upgrade it to a paid edition first.
3. Add the new domain: **Account > Domains > Manage domains > Add a domain > Secondary domain**,
   enter `lifepointechiro.com` and verify it (row 11). Then create the `office` user on that domain.
4. Optionally make `lifepointechiro.com` the primary domain: **Manage domains > Change primary
   domain**. Google calls this "an involved process". It isn't possible during a free trial or while the
   domain is unverified, and changes can take up to 48 hours.
5. Continue from step 3 below.

## 1. Edition and cost

US list prices per user per month, before tax, from the
[pricing page](https://workspace.google.com/pricing):

| Edition | Annual plan | Flexible plan | Storage |
|---|---|---|---|
| **Business Starter** (recommended) | $7.00 ($84/yr) | $8.40 ($100.80/yr) | 30 GB pooled per user |
| Business Standard | $14.00 | $16.80 | 2 TB pooled per user |

- **Start on Business Starter, Flexible plan.** Flexible lets you add or remove users and cancel at
  any time. Annual is 16% cheaper, but "You can reduce licenses only when renewing", and cancelling
  early means "you're charged for the remaining balance of your contract and no refunds are issued".
  You can switch from Annual back to Flexible only "during your free trial or when you renew".
- **Promo:** the page advertises "up to" 50% off the first 3 months, and the discount shown changes between
  page loads (20% and 50% both appeared on 10 Oct 2026). Budget on list price; checkout shows the
  final price.
- **Trial:** 14 days, up to 10 users. "Your payment method will not be charged until your free trial
  ends."
- **Aliases are free:** "You can add up to 30 email aliases for each user at no extra cost."
- **BAA eligibility:** Google's BAA page excludes only non-administrators and the legacy free edition,
  and names no other edition limit. Business Starter should therefore qualify. **Unconfirmed until
  you see the BAA entry in your own Admin console** (step 3).

## 2. Sign up and verify the domain

1. Go to <https://workspace.google.com/> and start the free trial.
2. Business name: **Lifepointe Chiropractic Center** (the practice's legal/billing name). This
   account is billed, and it is the party that accepts the HIPAA BAA in step 3. Use the same name
   when you set up billing. Country: United States.
3. For your current contact email, use an address you will keep, such as `lifepointechiro@gmail.com`.
   Google sends admin password recovery to "the secondary email you provided when you signed up".
4. When asked about a domain, choose the option for a domain you **already own** and enter
   `lifepointechiro.com`. Don't take the email-only sign-up path, because several admin controls
   need a verified domain.
5. Create the first account as **`office`**. It becomes the super admin.
6. Verify the domain: Admin console **Account > Domains > Manage domains > Verify domain**, or the
   setup tool. Pick Network Solutions if it's listed, or "My domain uses a different host". Copy the
   `google-site-verification=...` value, add it as row 11, then click **Come back here and
   confirm...** and **Confirm**. Google allows "up to 72 hours" for this. Google also says: "You must verify your domain
   within the first 9 days of your free trial period". An unverified account is deleted within 21
   days unless billing is set up. Leave the TXT record in place afterwards. Google says it "can be safely
   removed", but keeping it does no harm.
7. Turn on 2-Step Verification for `office@` now, and store its backup codes somewhere safe and
   offline. Google is moving to require 2SV for all admin accounts.

Google also recommends that an organization "should have more than one super administrator account" and that
you "Don't use a super admin account for daily activities". Following that fully costs another license. A
practical minimum: if Dr. Greg gets his own user (step 5), make him a second super admin.

## 3. Accept the HIPAA BAA before Gmail goes live

Google: "Customers who have not signed a BAA with Google must not use PHI in Google Workspace". Accept
the BAA **before** step 6 (MX and Activate Gmail). Patients can email the practice as soon as
mail flows, so accepting it any later is too late.

1. Sign in as the super admin (`office@`).
2. Admin console: **Menu > Account > Account settings > Legal and compliance**.
3. Go to the **Security and Privacy Additional Terms** section.
4. Click **Google Workspace/Cloud Identity HIPAA Business Associate Amendment** to review it.
5. Click **Review and Accept** and answer all three questions confirming the practice is a HIPAA
   covered entity.
6. Click **OK**.
7. **Take a screenshot** of the acceptance. Google: "the customer can produce a screenshot of their
   Admin Console/HIPAA acceptance". The electronic agreement is as binding as a paper one.

**Unconfirmed:** whether the BAA can be accepted during the free trial. If the entry isn't offered,
don't activate Gmail yet. Set up billing, and if it still doesn't appear, ask Google support. That
question involves no patient information, so asking is fine.

### What the BAA covers

Google's list of covered Workspace services (last updated 2025-08-31) includes **Gmail**, **Google
Calendar**, **Google Drive** (including Docs, Forms, Sheets, Slides, Vids), **Google Meet**, Google
Chat, Google Groups, Google Keep, Google Sites, Google Tasks, Google Vault (if applicable), Google
Voice (managed users only), AppSheet, Google Apps Script, Google Cloud Search and Cloud Identity
Management. The full, current list is on
[HIPAA: covered Workspace services](https://docs.cloud.google.com/docs/security/compliance/hipaa).

These are **not** covered, so keep patient information out of them:

- **Additional Google services** such as YouTube, Blogger and Google Business Profile Manager.
  "neither the Cloud Data Processing Addendum (CDPA) nor the Google Workspace BAA terms extend to
  Additional Google Services."
- **Third-party apps and add-ons:** "Third-party applications including add-ons are not included".
- **Google Contacts.** Google's HIPAA implementation guide lists it as a core service "in which PHI is
  not permitted".
- **Google Photos.** Google's list puts it under Drive, but the implementation guide names it as
  a service to disable. Treat it as not covered.
- **Google support channels.** The guide says not to give PHI to Google technical support.

### Restrict what isn't covered

1. **Apps > Additional Google services**: click each service **> Service status > Off for
   everyone > Save**.
2. **Account > Account settings > Preferences > Release preferences > New products**: choose
   **Turned off when released**, then **Save**. New Google services then stay off until you turn them on.
3. **Apps > Google Workspace Marketplace apps > Apps list > User Install Settings > Manage access to
   apps**: don't let users install apps, or allow only allowlisted apps.
4. In each user's Gmail: **Settings > See all settings**, then in the **Create contacts for
   auto-complete** section select **I'll add contacts myself** and click **Save changes**. By default, Gmail
   saves everyone you email to Contacts ("Other contacts"), and Contacts isn't covered.
5. The implementation guide suggests setting external calendar sharing to "Only free/busy
   information". Beyond that, keep Drive files with patient information private (no "anyone with the
   link" sharing), and keep patient details out of file names.
6. Give every person their own login with 2SV, and never share logins. HIPAA requires "Unique user identification"
   (45 CFR 164.312(a)(2)(i)).
7. The old consumer account `lifepointechiro@gmail.com` is not under any BAA. Once `office@` works,
   stop using it for patient email.

## 4. Aliases on office@

1. Admin console: **Menu > Directory > Users**, then click **office**.
2. On the left, under the user's name, click **Add Alternate Emails**.
3. Click **Alternate email** and enter `contact`. Repeat for `info` and `dmarc`, then click **Save**.
   "Changes can take up to 24 hours".

`dmarc@` receives the DMARC reports (row 15). In `office@` Gmail, create a filter: **To:**
`dmarc@lifepointechiro.com` **> Skip the Inbox, Apply the label "DMARC"**.

Optional: to reply *as* `contact@` or `info@`, go to Gmail **Settings > See all settings > Accounts > Send mail as > Add
another email address** and keep **Treat as an alias** ticked. Google's January 2027 "Send as" change "does
not affect Google Workspace aliases".

## 5. Dr. Greg's address (decision needed)

Dr. Greg's address hasn't been chosen. The names below are examples only.

| Option | What | Extra cost | Trade-offs |
|---|---|---|---|
| A: alias | An alias such as `drgreg@` on `office@` | $0 | One inbox. If staff also read `office@`, Dr. Greg and the staff share one login, which conflicts with HIPAA's unique-user rule. There is no per-person audit trail and no second super admin |
| B: own user | A user such as `greg@` (plus a `drgreg@` alias if wanted), with delegate access to `office@` | +$8.40/mo flexible ($100.80/yr) or +$7/mo annual ($84/yr) | Separate login, 2SV and audit trail. He becomes the natural second super admin |

If anyone other than Dr. Greg reads `office@`, option B is the safer choice.

**Also decide who reads `office@`.** If more than one person will, each needs their own user with
delegated access to `office@` (the same cost as option B, per person). Otherwise only one named
person signs in as `office@`. Either way, nobody shares a login (step 3).

For option B, or for each person who reads `office@`, after adding the user (**Directory > Users >
Add new user**):

1. Turn on delegation: **Apps > Google Workspace > Gmail > User settings > Mail delegation**, tick
   "Let users delegate access to their mailbox to other users in the domain", and **Save**.
2. In `office@` Gmail: **Settings > See all settings > Accounts** (or **Accounts and Import**) **>
   Grant access to your account > Add another account**, then enter that person's address.

## 6. Turn on mail

1. In Network Solutions, delete the default MX and SPF records
   ([dns.md, step 2](dns.md#step-2-review-the-default-records-you-decide-what-to-delete)). Add row 12
   (MX `smtp.google.com`, priority 1) and row 13 (SPF `v=spf1 include:_spf.google.com ~all`).
2. Admin console: **Account > Domains > Manage domains > Activate Gmail**, then follow the steps.
   **Write down the date and time.** The DKIM wait starts here.
3. "It can take up to 72 hours for new MX records to be recognized." Then send test messages from an
   outside account to `office@`, `contact@`, `info@`, `dmarc@` and Dr. Greg's address. Reply from `office@`.
   In the received copy, **Show original** should report SPF: PASS.

## 7. DKIM (24-72 hours after Activate Gmail)

Google: "after you turn on Gmail for your organization, you must wait 24–72 hours before you can get
your DKIM key".

1. Admin console: **Menu > Apps > Google Workspace > Gmail > Authenticate email**.
2. Under **Selected domain**, pick `lifepointechiro.com` and click **Generate New Record**.
3. Choose **2048** bits and keep the prefix selector `google`. Click **Generate**.
4. Copy the **DNS Host name** (`google._domainkey`) and the **TXT record value** into row 14. Don't
   click **Start authentication** yet. If Network Solutions rejects the 2048-bit value as too long,
   generate a **1024**-bit key instead.
5. Once the record resolves (see the checks in [dns.md, step 7](dns.md#step-7-email-records)), click
   **Start authentication**. "It can take up to 48 hours for DKIM authentication to start working."

## 8. DMARC: start at p=none, tighten later

Google: "Set up DKIM and SPF at least 48 hours before setting up DMARC."

1. Add row 15: `v=DMARC1; p=none; rua=mailto:dmarc@lifepointechiro.com`.
2. Read the reports under the DMARC label for at least a week ("One week is usually enough time").
3. If the reports show only legitimate mail passing, tighten in steps. Each step is an edit to row 15:
   - `v=DMARC1; p=quarantine; pct=10; rua=mailto:dmarc@lifepointechiro.com` (Google: "a small organization
     might start with 10%")
   - raise `pct` gradually to 100
   - optionally `v=DMARC1; p=reject; rua=mailto:dmarc@lifepointechiro.com`

Before tightening, every other service that sends as `@lifepointechiro.com` must pass SPF or DKIM.
That includes the newsletter platform once it's chosen. Add its `include:` to the one SPF record
(row 13) and publish its DKIM record. Otherwise its mail gets quarantined or rejected.

## 9. Move off lifepointechiro@gmail.com

Do this after the BAA is accepted (step 3) and mail flows (step 6).

**Copy the old mail into office@** with Google's Data import tool. It supports a personal Gmail
account as the source, on Business Starter and up.

1. Admin console (as super admin): **Menu > Data > Data import & export > Data import**.
2. For **Gmail**, click **Import**. Enter `lifepointechiro@gmail.com` as the **Source email address** and click
   **Request authorization**. The Gmail owner must approve within 24 hours or "the request expires".
   If you own the account, you can approve it directly from the Admin console. If the old account
   uses Google's Advanced Protection Program, turn that off for the duration of the import.
3. Choose `office@lifepointechiro.com` as the target, pick the options (start date, whether to include
   deleted and spam mail), and click **Start import**.
   - What comes across: messages with their labels, stars and read state.
   - What doesn't: attachments are skipped when "the message plus attachment is larger than 25
     MB". Contacts and calendars are not part of the import.

**Forward new mail** from the old account:

1. In `lifepointechiro@gmail.com`: **Settings > See all settings > Forwarding and POP/IMAP > Add
   a forwarding address**, enter `office@lifepointechiro.com`.
2. Open the verification link that arrives at `office@`.
3. Back in the old account, select **Forward a copy of incoming mail to** `office@lifepointechiro.com`. Choose
   **Keep Gmail's copy in the Inbox** (Google's recommendation) or **archive** it, then click **Save
   Changes**. Spam isn't forwarded.

**Finish the import:**

1. Run a **delta import** to pick up mail that arrived during the first import.
2. Download the report.
3. Click **Exit import**. Exiting "removes OAuth access in the source account".

**What was discontinued:** don't plan on Gmail's **Check mail from other accounts** (POP fetch) or
Gmailify for this move. Google: "Gmail will no longer support checking emails from third-party
accounts through POP" and "After the first quarter of 2026, this feature no longer supports new
users. Existing users can still use the feature until January 2027." Gmail's import from other
accounts remains, but "this is a one-time import, and messages do not sync continuously". Forwarding
plus Data import, as above, replaces both.

**Keep the old account. Don't delete it.**

- Check what it owns, such as the Google Business Profile, reviews or YouTube. Those are consumer
  services that are switched off in Workspace (step 3), so they stay in this account.
- Turn on 2-Step Verification and set `office@lifepointechiro.com` as its recovery email.
- Sign in at least once every two years. Google may delete accounts that are "inactive across Google for at least
  two years".
- Don't use it for patient email, and don't send as `office@` from it.

### Then: go public with office@

1. **Merge the PR that switches the website to `office@lifepointechiro.com` (`config/office-email`) only after
   both of these are true:**
   - a test message to `office@` has arrived and a reply from it has been received outside the
     practice (step 6)
   - the BAA acceptance screenshot is saved (step 3)
2. Update the printed and PDF documents that still show the Gmail address. Of the New 2026 documents,
   only the X-ray release form does, in both files:
   `05 Policies, Consents & Records/New 2026/X-ray release form Request from another Dr.docx` and its
   `.pdf`. Regenerate the PDF from the corrected .docx.
3. Change the address anywhere else it is listed: the Google Business Profile, social profiles, and
   insurance or payer portals.
4. The business card already prints `office@lifepointechiro.com`. Don't hand cards out before step 6
   works.

## 10. Later: the old domain's addresses

Once you know who controls `lifepointechiropractic.com` and that no mailbox depends on its current
MX records ([dns.md, old domain](dns.md#the-old-domain-lifepointechiropracticcom)), you can add
it as a user alias domain. Google: "Each user gets an email address at both your primary domain and
the user alias domain". For example, `office@lifepointechiropractic.com` would reach `office@`. Check
in the Admin console which alias addresses (such as `info@`) also carry over before relying on them.

1. **Account > Domains > Manage domains > Add a domain > User alias domain**, and verify the domain.
2. Set its MX to `smtp.google.com`, replacing both the Google `aspmx` records and the
   `nowyouknow.net` record. Set its SPF to `v=spf1 include:_spf.google.com ~all`.
3. Click **Activate Gmail** for it.

The cost is "No extra cost per user or group". There is one side effect: any personal Google
Account that uses an `@lifepointechiropractic.com` address "[is] automatically renamed".

## Sources

Google Workspace Admin Help:

- [Pricing](https://workspace.google.com/pricing) and [Flexible vs. Annual plans](https://knowledge.workspace.google.com/admin/billing/compare-flexible-and-annual-fixed-term-payment-plans)
- [Sign up for a free trial](https://knowledge.workspace.google.com/admin/getting-started/sign-up-for-a-free-google-workspace-trial) and [About your free trial](https://knowledge.workspace.google.com/admin/getting-started/about-your-google-workspace-free-trial)
- [Verify your domain](https://knowledge.workspace.google.com/admin/domains/verify-your-domain-for-google-workspace) and [Verify with a TXT record](https://knowledge.workspace.google.com/admin/domains/verify-your-domain-with-a-txt-record)
- [Can't sign up my domain](https://knowledge.workspace.google.com/admin/support/troubleshooting/cant-sign-up-my-domain-for-a-google-service)
- [Add a user alias domain or secondary domain](https://knowledge.workspace.google.com/admin/domains/add-a-user-alias-domain-or-secondary-domain)
- [Change your primary domain](https://knowledge.workspace.google.com/admin/domains/change-your-primary-domain-for-google-workspace)
- [Security best practices for administrator accounts](https://knowledge.workspace.google.com/admin/users/security-best-practices-for-administrator-accounts)
- [2SV enforcement for admins](https://knowledge.workspace.google.com/admin/security/about-2sv-enforcement-for-admins)
- [HIPAA compliance with Google Workspace](https://knowledge.workspace.google.com/admin/compliance/hipaa-compliance-with-google-workspace-and-cloud-identity)
- [Privacy compliance (how to accept the BAA)](https://knowledge.workspace.google.com/admin/compliance/privacy-compliance-and-records-for-google-workspace-and-cloud-identity)
- [Turn on or off additional Google services](https://knowledge.workspace.google.com/admin/users/advanced/turn-on-or-off-additional-google-services)
- [Turn new services on or off by default](https://knowledge.workspace.google.com/admin/releases/turn-new-services-on-or-off-by-default)
- [Set whether users can install Marketplace apps](https://knowledge.workspace.google.com/admin/apps/set-whether-users-can-install-marketplace-apps)
- [Add an email alias](https://knowledge.workspace.google.com/admin/users/add-or-delete-an-alternate-email-address-email-alias)
- [Let users delegate access to a Gmail account](https://knowledge.workspace.google.com/admin/gmail/let-users-delegate-access-to-a-gmail-account)
- [Set up MX records](https://knowledge.workspace.google.com/admin/domains/set-up-mx-records-for-google-workspace), [SPF](https://knowledge.workspace.google.com/admin/security/set-up-spf), [DKIM](https://knowledge.workspace.google.com/admin/security/set-up-dkim), [DMARC](https://knowledge.workspace.google.com/admin/security/set-up-dmarc), [recommended DMARC rollout](https://knowledge.workspace.google.com/admin/security/recommended-dmarc-rollout)
- [Import email from a Gmail account](https://knowledge.workspace.google.com/admin/migrate/migrate-email-from-a-gmail-account) and [About the data import tool](https://knowledge.workspace.google.com/admin/migrate/about-importing-email-with-the-data-import-tool)

Google Cloud, terms and guides:

- [HIPAA: covered Workspace services](https://docs.cloud.google.com/docs/security/compliance/hipaa)
- [HIPAA Business Associate Amendment (text)](https://workspace.google.com/terms/2015/1/hipaa_baa/)
- [HIPAA Implementation Guide (PDF)](https://services.google.com/fh/files/misc/gsuite_cloud_identity_hipaa_implementation_guide.pdf)

Gmail and account help:

- [Automatically forward Gmail messages](https://support.google.com/mail/answer/10957)
- [Changes to Gmailify & POP in Gmail](https://support.google.com/mail/answer/16604719)
- [Send emails from a different address or alias](https://support.google.com/mail/answer/22370)
- [Delegate your Gmail account](https://support.google.com/mail/answer/138350)
- [Contacts: auto-saved "Other contacts"](https://support.google.com/contacts/answer/1069522)
- [Inactive Google Account policy](https://support.google.com/accounts/answer/12418290)

Regulation: [45 CFR 164.312](https://www.law.cornell.edu/cfr/text/45/164.312) (unique user identification).
