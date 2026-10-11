# DNS for lifepointechiro.com

This runbook covers everything at the registrar for `lifepointechiro.com`: getting the domain to
resolve, pointing it at GitHub Pages, the Google Workspace email records, and what to do with the
old domain. Email setup in the Google Admin console is in [google-workspace.md](google-workspace.md).

Every value below was checked on 10 Oct 2026 against live DNS and the official docs listed under
[Sources](#sources). Anything that could not be confirmed is marked **Unconfirmed**.

## Current state

- **The domain doesn't resolve at all.** The .com registry delegates it to
  `ns1.domaincom-default.domainparkingserver.net` and `ns2.domaincom-default.domainparkingserver.net`
  (both 208.73.209.34). Those parking servers don't answer, so every lookup fails with SERVFAIL
  ("Name servers did not respond"). Records you add in the panel won't be served until the
  nameservers change.
- **Domain.com is now Network Solutions.** Log in at
  <https://www.networksolutions.com/my-account/login>. Network Solutions says "For most customers,
  your login will remain the same as it is today on Domain.com". For account-access problems after
  the move, its FAQ gives support at 855-834-8495.
- **Registry record:** registrar "Domain.com - Network Solutions, LLC", registered 2023-01-06,
  **expires 2028-01-06**. The status is `active` only, so there is no transfer lock. DNSSEC is off.
- **A default zone is waiting on Domain.com's own nameservers.** `ns1.domain.com` and
  `ns2.domain.com` already answer authoritatively for the domain. It goes live as soon as the
  nameservers are reverted. Its records are listed in
  [step 2](#step-2-review-the-default-records-you-decide-what-to-delete).
- **That zone changed on the evening of 10 Oct 2026**, while this runbook was being written. Its SOA
  serial went from `2023010664` to `124033119`, and the wildcard MX record disappeared. The cause is
  unknown (possibly the Domain.com to Network Solutions move). Treat the step 2 list as a snapshot
  and go by what the panel shows.

## Order of operations

| Step | What | Where | Wait afterwards |
|---|---|---|---|
| 1 | Revert the nameservers to the defaults | Network Solutions | Up to 48 h |
| 2 | Review the default records and decide what to delete | Network Solutions | n/a |
| 3 | Verify the domain with GitHub (TXT record) | GitHub profile settings + Network Solutions | Minutes to 24 h |
| 4 | Add the website records (A ×4, AAAA ×4, CNAME `www`) | Network Solutions | Up to 24 h |
| 5 | Set the custom domain, wait for the certificate, then Enforce HTTPS | GitHub repo settings | Up to 24 h |
| 6 | Test, including `/card` | Terminal + phone | n/a |
| 7 | Email records, in stages over several days | Network Solutions, following [google-workspace.md](google-workspace.md) | See that file |
| 8 | Old domain: confirm ownership, then 301-forward it | Wherever it is registered | Up to 48 h |

Steps 3-6 and step 7 are independent once step 1 is done. Do them in either order.

## All records

This is the complete list of records the domain should end up with. Add each one in Network Solutions under
**Advanced Tools > Manage** (next to **Advanced DNS Records**) **> + Add Record**. In that form, "Host" is the
**Refers to** field: pick `@` or `www`, or pick **Other Host** and type the **Host Name**.

| # | Purpose | Type | Host (Refers to) | Value | TTL | Priority | Value comes from | Add it at |
|---|---|---|---|---|---|---|---|---|
| 1 | GitHub domain verification | TXT | Other Host: `_github-pages-challenge-rramboer` | the string GitHub shows | 3600 | | GitHub: profile **Settings > Pages > Add a domain** | Step 3. Keep it forever |
| 2 | Website | A | `@` | `185.199.108.153` | 3600 | | GitHub (fixed) | Step 4 |
| 3 | Website | A | `@` | `185.199.109.153` | 3600 | | GitHub (fixed) | Step 4 |
| 4 | Website | A | `@` | `185.199.110.153` | 3600 | | GitHub (fixed) | Step 4 |
| 5 | Website | A | `@` | `185.199.111.153` | 3600 | | GitHub (fixed) | Step 4 |
| 6 | Website | AAAA | `@` | `2606:50c0:8000::153` | 3600 | | GitHub (fixed) | Step 4 |
| 7 | Website | AAAA | `@` | `2606:50c0:8001::153` | 3600 | | GitHub (fixed) | Step 4 |
| 8 | Website | AAAA | `@` | `2606:50c0:8002::153` | 3600 | | GitHub (fixed) | Step 4 |
| 9 | Website | AAAA | `@` | `2606:50c0:8003::153` | 3600 | | GitHub (fixed) | Step 4 |
| 10 | Website (`www` redirects to the apex) | CNAME | `www` | `rramboer.github.io` | 3600 | | GitHub (fixed) | Step 4 |
| 11 | Google domain verification | TXT | `@` | `google-site-verification=...` (unique) | 3600 | | Google: Admin console **Account > Domains > Manage domains > Verify domain** (or the signup setup tool) | Workspace signup |
| 12 | Email delivery | MX | `@` | `smtp.google.com` | 3600 | 1 | Google (fixed) | When you activate Gmail |
| 13 | SPF | TXT | `@` | `v=spf1 include:_spf.google.com ~all` | 3600 | | Google (fixed) | With row 12 |
| 14 | DKIM | TXT | Other Host: `google._domainkey` | `v=DKIM1; k=rsa; p=...` | 3600 | | Google: **Apps > Google Workspace > Gmail > Authenticate email** | 24-72 h after Gmail is activated |
| 15 | DMARC | TXT | Other Host: `_dmarc` | `v=DMARC1; p=none; rua=mailto:dmarc@lifepointechiro.com` | 3600 | | Fixed (Google's rollout format) | 48 h or more after SPF and DKIM pass |

Notes on the table:

- **TTL:** Network Solutions defaults to 7200 (2 hours). The existing default zone uses 3600, and either works.
- **Rows 2-10:** these are GitHub's published values. They match what `rramboer.github.io` resolves to
  today. The CNAME target is `rramboer.github.io`: not `rramboer.github.io/lifepointe`, not a
  `*.pages.github.io` name, and not the apex. Network Solutions only allows CNAMEs on third-level names
  like `www`, which is all this setup needs. Its form doesn't list ALIAS/ANAME, so the apex
  uses the A and AAAA records.
- **Row 1 and rows 14-15 use underscore host names.** No Network Solutions page says whether
  **Other Host** accepts them. A third-party guide shows `_dmarc` being entered there, so they very likely
  work. **Unconfirmed.** If the form rejects one, call Network Solutions support.
- **Row 12, priority:** Google asks for priority 1. Network Solutions' current editor has a Priority
  field. Its "Classic View" editor only accepts 10-90. If 1 is rejected, use 10. With a single MX
  record, the number doesn't matter.
- **Rows 12-13 replace defaults.** Google says "Remove any other MX records", and Network Solutions says
  "only one SPF record is allowed per domain". Delete the default MX and SPF (step 2) when you add
  these, not before.
- **Row 13:** the newsletter platform hasn't been chosen. When it is, add its `include:` to
  this same record, for example `v=spf1 include:_spf.google.com include:<platform> ~all`. Don't add a
  second SPF record.
- **Row 14:** Google generates a 2048-bit key, which is longer than 255 characters. Google notes that "Some
  domain providers limit TXT record length". Whether Network Solutions' **TXT Value** field accepts the full key
  is **unconfirmed**. If it doesn't, generate a 1024-bit key instead, which is Google's documented
  fallback.
- **Row 15:** `dmarc@` is a free alias on `office@` (see [google-workspace.md](google-workspace.md)).
  For reports, Google suggests "a dedicated mailbox, a group, or a third-party service" rather than your own
  address. An alias plus a Gmail filter is a lighter compromise: reports stay out of the inbox, and
  `dmarc@` can be pointed somewhere else later without touching DNS. Tighten `p=none` later as
  described in that file.
- **No wildcard records.** GitHub "strongly recommend[s] that you do not use wildcard DNS records ...
  These records put you at an immediate risk of domain takeovers, even if you verify the domain."
- **CAA:** none exist today, which lets any CA issue certificates. If you ever add a CAA record, it must include
  `letsencrypt.org`, or GitHub can't issue the HTTPS certificate.

## Step 1: Revert the nameservers

1. Log in at <https://www.networksolutions.com/my-account/login>.
2. On the left, select **Domain**, choose `lifepointechiro.com`, and click **Settings**.
3. Scroll down to **Advanced Tools** and click **Manage** for the nameservers. The old Domain.com
   help labelled it **Nameservers (DNS)**. Don't use the **Manage** next to **Advanced DNS Records**.
4. A pop-up explains the change. Click **Continue**.
5. Click **Revert to Defaults**, then **Revert**.

Network Solutions says nameserver changes "may take 24-48 hours". Resolvers can keep the old
delegation for up to 48 hours (the .com NS TTL is 172800). Check progress with:

```sh
# Registry view: the nameservers should no longer be the domainparkingserver.net ones
curl -s https://rdap.verisign.com/com/v1/domain/lifepointechiro.com | grep -o '"ldhName":"[^"]*"'

# Resolver view: "Status":0 and an SOA instead of "Status":2
curl -s 'https://dns.google/resolve?name=lifepointechiro.com&type=SOA'
```

**Unconfirmed:** whether "Revert to Defaults" sets `ns1.domain.com`/`ns2.domain.com` or other
Network Solutions nameservers on a migrated Domain.com account. Either is fine. Enter the records wherever
the **Advanced DNS Records** page shows them, and use the checks above to confirm the delegated servers
actually serve what you entered. Network Solutions: "You can only use the Advanced DNS section when your
nameservers default to us."

As soon as the revert takes effect, the default zone goes live. The apex and every subdomain,
including `www`, then resolve to 66.96.162.148, a parking host that returns a 404 page with ads.
Nothing resolves today, so this costs nothing, but clean it up in step 2.

## Step 2: Review the default records (you decide what to delete)

Nothing here gets deleted without your OK. First go to **Advanced Tools > Manage** (next to
**Advanced DNS Records**) and **take a screenshot of the full list**. The table shows what
`ns1.domain.com` and `ns2.domain.com` served on 10 Oct 2026, from direct queries. The zone changed
once that evening (see [Current state](#current-state)), so the panel may differ, and it may label
records slightly differently. If it shows anything not in this table, screenshot it and decide
case by case.

| Host | Type | Value | Conflicts with | Recommendation |
|---|---|---|---|---|
| `@` | A | `66.96.162.148` | Website. GitHub: extra `@` records "may prevent the HTTPS certificate from generating" | Delete before step 4 |
| `*` (wildcard) | A | `66.96.162.148` | Website. This is what makes `www` (and any made-up subdomain) resolve today. GitHub warns against wildcards | Delete before step 4 |
| `*` (wildcard) | MX | `30 mx.lifepointechiro.com` | Website hygiene. It gives every made-up subdomain a mail route | Served earlier on 10 Oct, gone by that evening. Delete it with the wildcard A if the panel still lists it |
| `www` | any | Live DNS shows no explicit `www` record (it comes from the wildcard) | Website. A CNAME can't share a name with other records | Delete if the panel lists one |
| `@` | MX | `30 mx.lifepointechiro.com` | Email. Google: "Remove any other MX records" | Delete when you add row 12 |
| `@` | TXT | `v=spf1 ip4:66.96.128.0/18 include:websitewelcome.com ?all` | Email. Only one SPF record is allowed | Replace with row 13 when you add row 12 |
| `mx` | A | `66.96.140.182`, `66.96.140.183` | Nothing. This is the default mail host the default MX points to | Your call; unused once row 12 is in |
| `webmail` | A | `66.96.162.48` | Nothing | Your call; unused |
| `mail`, `ftp`, `smtp`, `pop`, `imap` | A | `66.96.162.148` | Nothing | Your call; unused |

GitHub's own instruction is: "If your DNS provider automatically sets a default record, remove it
before continuing."

## Step 3: Verify the domain with GitHub

Verification ties the domain to the `rramboer` account, so no other GitHub account can publish
to it or its immediate subdomains. It happens in your **profile** settings, not the repo's.

1. On GitHub, click your profile picture, then **Settings**.
2. In the sidebar under "Code, planning, and automation", click **Pages**.
3. Click **Add a domain**, enter `lifepointechiro.com`, and click **Add domain**.
4. GitHub shows a TXT record. Add it in Network Solutions as row 1 of the table: **Refers to**
   = **Other Host**, **Host Name** = `_github-pages-challenge-rramboer`, **TXT Value** = the string GitHub
   shows.
5. Wait until it resolves ("may be immediate or take up to 24 hours"):

   ```sh
   curl -s 'https://dns.google/resolve?name=_github-pages-challenge-rramboer.lifepointechiro.com&type=TXT'
   # or GitHub's own check:
   dig _github-pages-challenge-rramboer.lifepointechiro.com +nostats +nocomments +nocmd TXT
   ```

6. Back in **Settings > Pages**, click **...** next to the domain, then **Continue verifying**, then
   **Verify**.
7. Leave the TXT record in place permanently. GitHub: "To make sure your custom domain remains verified,
   keep the TXT record".

## Step 4: Add the website records

Once the step 2 deletions are done, add rows 2-10 of the table. Use **+ Add Record** for each one:

- **A:** **Refers to** `@`, **Points to** the IP. Repeat for all four.
- **AAAA:** **Refers to** `@`, **Points to** the IPv6 address. Repeat for all four.
- **CNAME:** **Refers to** `www`, **Alias to** `rramboer.github.io`.

GitHub normally asks you to add the domain to the repo before creating DNS records, to prevent
takeover. Step 3 already covers that risk: a verified domain "stops other GitHub users from taking over
your custom domain". So the records can go in before step 5. Until step 5 is done, the domain shows a
GitHub 404 page.

Check (GitHub: "DNS changes can take up to 24 hours to propagate"):

```sh
curl -s 'https://dns.google/resolve?name=lifepointechiro.com&type=A'          # only the four 185.199.10x.153
curl -s 'https://dns.google/resolve?name=lifepointechiro.com&type=AAAA'       # only the four 2606:50c0:800x::153
curl -s 'https://dns.google/resolve?name=www.lifepointechiro.com&type=CNAME'  # rramboer.github.io.
curl -s 'https://dns.google/resolve?name=zz-test.lifepointechiro.com&type=A'  # "Status":3 (NXDOMAIN): wildcard gone
```

On Windows without `dig`, use `Resolve-DnsName lifepointechiro.com -Type A` in PowerShell.

## Step 5: Set the custom domain on the repo, then HTTPS

**Prerequisite:** the site must already deploy with GitHub Actions. **Settings > Pages > Build and
deployment > Source** should show **GitHub Actions**. With that source, GitHub says "no `CNAME` file
is created, and any existing `CNAME` file is ignored and is not required". The domain lives only in the
repo settings, and the repo has no `CNAME` file. If you do this while Pages still deploys from a branch,
**Save** commits a `CNAME` file to `main`, which you don't want.

1. Open <https://github.com/rramboer/lifepointe>, then **Settings**. In the sidebar under
   "Code, planning, and automation", click **Pages**.
2. Under **Custom domain**, type `lifepointechiro.com` (the apex, not `www`) and click **Save**.
   GitHub runs a DNS check. If it passes, GitHub requests a certificate from Let's Encrypt, and a
   check mark appears next to the domain when the certificate is installed. GitHub: "It can take up to an hour
   for your site to become available over HTTPS".
3. If nothing has happened "several minutes" after **Save**, or after any later DNS change, click
   **Remove**, retype the domain, and click **Save** again. This restarts provisioning.
4. When the option becomes available ("It can take up to 24 hours"), tick **Enforce HTTPS**.

With the apex as the custom domain and both the apex and `www` records in place, GitHub redirects
`www.lifepointechiro.com` to `lifepointechiro.com` and also tries to get a certificate for `www`.

Check from the terminal:

```sh
gh api repos/rramboer/lifepointe/pages --jq '{cname, https_enforced, protected_domain_state}'
# expect: "cname":"lifepointechiro.com", "https_enforced":true, "protected_domain_state":"verified"

gh api repos/rramboer/lifepointe/pages/health
# the first call returns 202 (check started); call again for the 200 result
```

## Step 6: Test

```sh
curl -sI http://lifepointechiro.com/         # 301 -> https://lifepointechiro.com/
curl -sI https://lifepointechiro.com/        # 200, server: GitHub.com
curl -sI https://www.lifepointechiro.com/    # 301 -> https://lifepointechiro.com/
curl -sI https://rramboer.github.io/lifepointe/   # 301 -> https://lifepointechiro.com/

# Certificate: issuer Let's Encrypt; SAN includes lifepointechiro.com (and www once GitHub adds it)
echo | openssl s_client -connect lifepointechiro.com:443 -servername lifepointechiro.com 2>/dev/null \
  | openssl x509 -noout -issuer -ext subjectAltName
```

The `rramboer.github.io` redirect is GitHub's observed behaviour for project sites with a custom
domain, not a documented guarantee. The site's internal links are relative, so the move from
`/lifepointe/` to `/` breaks nothing either way.

### Before printing business cards: `/card`

The QR code on the printed card encodes exactly `https://lifepointechiro.com/card`, with no
trailing slash. That URL must work on the live domain before any cards are ordered.

1. Run the checks:

   ```sh
   curl -sIL https://lifepointechiro.com/card    # ends in 200 (GitHub Pages normally 301s /card to /card/ first)
   curl -sIL https://lifepointechiro.com/card/   # 200
   curl -sIL http://lifepointechiro.com/card     # ends in 200 over https
   ```

2. Open both URLs on a phone and a desktop browser.
3. Scan the QR code from the final print file with a phone camera and confirm it lands on the
   page the card is meant to open.

The card also prints `office@lifepointechiro.com`. Don't hand cards out until mail to `office@` works
([google-workspace.md](google-workspace.md)).

## Step 7: Email records

Add rows 11-15 in the stages and at the times given in [google-workspace.md](google-workspace.md). In
short:

- Row 11 goes in at signup.
- Rows 12-13 go in together, replacing the default MX and SPF, right before **Activate Gmail**.
- Row 14 goes in 24-72 h after activation.
- Row 15 goes in 48 h or more after SPF and DKIM pass.

Checks:

```sh
curl -s 'https://dns.google/resolve?name=lifepointechiro.com&type=MX'                  # only "1 smtp.google.com."
curl -s 'https://dns.google/resolve?name=lifepointechiro.com&type=TXT'                 # one v=spf1 record, plus the verification string
curl -s 'https://dns.google/resolve?name=google._domainkey.lifepointechiro.com&type=TXT'
curl -s 'https://dns.google/resolve?name=_dmarc.lifepointechiro.com&type=TXT'
```

Google's [Admin Toolbox Dig](https://toolbox.googleapps.com/apps/dig/) does the same checks in a browser.

## Afterwards (optional, your call)

- The domain has no transfer lock (registry status `active` only). Consider turning on the lock,
  domain privacy and auto-renew in Network Solutions. The domain expires 2028-01-06.

## The old domain: `lifepointechiropractic.com`

### What its DNS shows today (10 Oct 2026)

| Item | Value |
|---|---|
| Registrar | Tucows (the registry links to Tucows' OpenSRS reseller service). The registrant is hidden by Contact Privacy Inc. |
| Dates and status | Registered 2005-09-08, **expires 2027-09-08**, last changed 2026-08-25. Status `clientTransferProhibited` and `clientUpdateProhibited` |
| Nameservers | `ns01`-`ns04.squarespacedns.com` and `dns1`-`dns4.p01.nsone.net` |
| A (`@` and `www`) | `35.187.82.108`, the old website host. It now answers HTTP 423 (subscription expired) |
| MX | `1 aspmx.l.google.com`, `5 alt1.aspmx.l.google.com`, `5 alt2.aspmx.l.google.com`, `10 alt3.aspmx.l.google.com`, `10 alt4.aspmx.l.google.com`, `5 mx0.mail.nowyouknow.net` |
| TXT | a `google-site-verification=` string, and `v=spf1 include:nowyouknow.net -all` |
| DKIM / DMARC | none |

The Google MX records don't prove a Google Workspace account exists. Google's sign-in check says the domain "isn't using Google Workspace". See
[google-workspace.md, step 0](google-workspace.md#0-check-for-an-existing-workspace-account-first).
With Google at priority 1 and no account behind it, mail to `@lifepointechiropractic.com` probably bounces
today. **Unconfirmed**: send a test message and read the bounce.

### Who owns it (you need to confirm)

The public records don't say. Squarespace's nameservers suggest the domain is managed in a
Squarespace Domains account, but that is an inference. It might be the practice's account, the old
website vendor's, or someone else's. Ways to find out:

- Search `lifepointechiro@gmail.com` and Dr. Greg's email for renewal or receipt emails mentioning the
  domain, Squarespace or Tucows. Renewal notices before 2027-09-08 go to whoever holds it.
- Ask the office whether anyone ever had a Squarespace login or an `@lifepointechiropractic.com`
  mailbox.
- Ask the former website vendor whether they registered it on the practice's behalf.
- **Settle this before the old website vendor's account is cancelled.** If the vendor holds the
  domain, ask them to unlock it and send the transfer authorization (EPP) code, and move it to an
  account the practice controls first. Once their account closes, nobody may be able to renew it
  before it expires on 2027-09-08.

### Plan once ownership is confirmed: 301 to the new domain without breaking mail

1. Before changing anything, find out whether any mailbox still uses the domain. Ask the office,
   send a test message to the address the practice used to publish, and read the reply or bounce.
2. In the account that controls the domain's DNS, **screenshot every record**.
3. Set up a **permanent (301)** forward of `@` and `www` to `https://lifepointechiro.com`. The old
   URL paths don't exist on the new site, so forward every path to the home page. If the domain is in
   Squarespace:
   **Domains dashboard > the domain > Website > Domain Forwarding Rules > Add rule**. Enter `@`, then
   `https://lifepointechiro.com` under **Enter website URL**, then **Advanced settings > Permanent
   Redirect (301)** and **Remove paths**. Click **Save**. Repeat for `www`. If an SSL toggle appears and
   is off, turn it on. Squarespace: "It can take up to 48 hours for domain forwarding to update." If
   the domain is elsewhere, use that provider's URL forwarding with the same choices (301, HTTPS,
   all paths to the home page).
4. **Leave the MX and TXT records exactly as they were.** Forwarding is meant to change only the
   website records. Squarespace notes that "your Squarespace defaults are automatically removed" when forwarding is set
   up, so compare against the screenshot afterwards and restore anything mail-related that changed.
5. Verify:

   ```sh
   curl -sI https://lifepointechiropractic.com/       # 301, location: https://lifepointechiro.com/
   curl -sI https://www.lifepointechiropractic.com/   # same
   curl -sI http://lifepointechiropractic.com/        # same (or 301 to https first)
   curl -s 'https://dns.google/resolve?name=lifepointechiropractic.com&type=MX'   # unchanged from the table above
   ```

6. Optional, later: to have old addresses deliver to `office@`, add the old domain to Workspace as a
   free user alias domain. That changes its MX and SPF, so do it only after step 1 confirms no
   other mailbox depends on them. See [google-workspace.md](google-workspace.md#10-later-the-old-domains-addresses).
7. Keep the domain renewed (it expires 2027-09-08) for as long as you want the redirect to work.
   Moving it to an account the practice controls requires the current holder to lift the transfer
   lock, so do it before that holder's account is closed (see [Who owns it](#who-owns-it-you-need-to-confirm)).

## Sources

GitHub:

- [About custom domains and GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)
- [Managing a custom domain for your GitHub Pages site](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- [Verifying your custom domain for GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
- [Securing your GitHub Pages site with HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
- [Troubleshooting custom domains and GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages)
- [REST API: Get a DNS health check for GitHub Pages](https://docs.github.com/en/rest/pages/pages#get-a-dns-health-check-for-github-pages)

Network Solutions (these pages may show a bot check to scripts; they open normally in a browser):

- [How to manage nameservers for Network Solutions domains](https://www.networksolutions.com/help/article/manage-custom-nameservers) (Revert to Defaults)
- [How to manage DNS and advanced DNS records](https://www.networksolutions.com/help/article/manage-dns-adns-records) (form fields, TTL 7200, CNAME on third-level names only, one SPF record)
- [FAQs: Domain.com is becoming Network Solutions](https://www.networksolutions.com/help/article/faqs-domaindotcom-becoming-network-solutions) (login, DNS unchanged by the move)
- Third-party, for underscore host names: [dmarcian: DMARC on Network Solutions](https://dmarcian.com/dmarc-network-solutions/)

Google:

- [Set up MX records for Google Workspace](https://knowledge.workspace.google.com/admin/domains/set-up-mx-records-for-google-workspace)
- [Set up SPF](https://knowledge.workspace.google.com/admin/security/set-up-spf)
- [Set up DKIM](https://knowledge.workspace.google.com/admin/security/set-up-dkim)
- [Recommended DMARC rollout](https://knowledge.workspace.google.com/admin/security/recommended-dmarc-rollout)

Other:

- [Let's Encrypt: CAA](https://letsencrypt.org/docs/caa/)
- [Squarespace: Forwarding a domain](https://support.squarespace.com/hc/en-us/articles/214767107-Forwarding-a-domain)
- Registry data: [lifepointechiro.com on RDAP](https://rdap.verisign.com/com/v1/domain/lifepointechiro.com).
  For the old domain, swap the name in the same URL.
