# Deployment guide — sreejithdigital.com

This repository now supports both Cloudflare deployment paths. The original failed build came from **Workers Builds / Wrangler**, not classic Cloudflare Pages:

```text
Executing user deploy command: npx wrangler deploy
✘ [ERROR] Could not detect a directory containing static files
```

That happened because `wrangler deploy` initially ran from the README-only `main` branch with no Wrangler configuration and no `public/` directory. It has since been fixed: the site is merged into `main`, dependencies are detected, and the Worker deploys successfully to `https://sreejith-digital.sreejithcu2020.workers.dev/`.

## Current domain status — read this first

The registered domain is:

```text
sreejithdigital.com
```

It has **no hyphen**. Public DNS shows Cloudflare nameservers (`algin.ns.cloudflare.com` and `maria.ns.cloudflare.com`) and apex `A` records `104.21.65.51` and `172.67.140.170`. The apex homepage resolves and renders. `www.sreejithdigital.com` still needs its own DNS record and zone-level redirect if you want the `www` variant; see the dedicated section below.

The following name is **not delegated** and returns `NXDOMAIN`:

```text
sreejith-digital.com
```

That hyphenated name resembles the Cloudflare Worker name and temporary `*.workers.dev` URL, but it is not the registered domain. Opening it produces Chrome’s `DNS_PROBE_POSSIBLE` error. Do not use it as the site URL or as a custom domain.

`wrangler.toml` includes:

```toml
[[routes]]
pattern = "sreejithdigital.com"
custom_domain = true
```

The custom domain is already live. A new Workers Builds deployment publishes updated static assets to the existing Worker; it does not require creating a new domain.

## Domain hardening status — done 27 Nov 2026

Configured in the Cloudflare dashboard and verified live (SSL Labs A+ on all four edge IPs):

| Setting | State |
| --- | --- |
| Always Use HTTPS | On (`http://` → `https://` 301) |
| Minimum TLS | 1.2 (TLS 1.2 and 1.3 only) |
| SSL/TLS mode | Full (strict) |
| HSTS | `max-age=15552000; includeSubDomains`, no preload. Sent by Cloudflare — do not add it to `public/_headers` |
| Certificate Transparency alerts | On |
| `www` | Proxied A record `192.0.2.1` + Redirect Rule `https://www.sreejithdigital.com/*` → `https://sreejithdigital.com/${1}` (301, query kept) |
| DNSSEC | Active; DS published by Cloudflare Registrar |
| Email Routing | On. `hello@sreejithdigital.com` → owner's verified inbox. MX ×3, SPF `include:_spf.mx.cloudflare.net ~all`, DKIM `cf2024-1`, DMARC `p=reject; sp=reject; adkim=s; aspf=s` |
| Google Search Console | Domain property verified by DNS TXT; sitemap submitted |
| Bing Webmaster Tools | Verified by CNAME (DNS only, not proxied); sitemap submitted |
| Crawler Hints (IndexNow) | On |
| Registrar | Transfer lock, WHOIS privacy and auto-renew on; expires 26 Nov 2027 |

Keep the `google-site-verification` TXT record and the Bing CNAME (`18cbf232….sreejithdigital.com` → `verify.bing.com`), or the search consoles lose verification.

**Auto-deploy check:** after every merge to `main`, confirm a build ran in Workers & Pages → `sreejith-digital` → Deployments, and that `/version.txt` shows the new release. On 27 Nov 2026 merges did not start builds because the Cloudflare Workers and Pages GitHub App had access only to `Sree278/dotmiracle`; `Sree278/sreejith-digital` was added (GitHub → Settings → Installed GitHub Apps → Cloudflare Workers and Pages → Repository access). If a merge ever stops starting a build, check that list first.

## Current release to publish

As of `2026-11-27`, the repository contains release `2026-11-27.1` (doorway/spam fixes, case study and conversion layer):

- 40 indexable pages plus `/thank-you/` (noindex) and `404.html`
- 5 project-based location pages (Bengaluru, Delhi NCR, Hyderabad, Chennai, Kerala); Mumbai and Pune redirect to `/locations/`, Kochi redirects to `/locations/kerala/`
- Unique, intent-matched titles and H1s (the site-wide `SEO Expert & Consultant | …` pattern is gone)
- New: `/case-studies/`, `/case-studies/mindtech-solutions-mep-seo/`, `/free-seo-review/`, `/services/ai-search-optimization/`, `/industries/construction-mep-contractors/`, `/resources/location-pages-without-doorway-risk/`
- A Worker (`worker/index.js`) now answers `POST /api/enquiry`; every other request is served straight from `public/` (`run_worker_first = ["/api/*"]`)
- `public/version.txt` shows `release: 2026-11-27.1`

Check the live domain against `/version.txt` and `/sitemap.xml` (40 URLs). If it shows an older release, open Workers Builds, select the latest commit on `main`, and run **New deployment / Retry build**.

## After merging release 2026-11-27.1 — owner checklist

These steps need the Cloudflare and Google dashboards, which are not connected to this workspace.

### 1. Enquiry form → your inbox (Cloudflare Email Routing, free)

**Status 27 Nov 2026:** steps 1–5 are done (Email Routing on, inbox verified, `hello@` routed, `[[send_email]]` enabled in release `2026-11-27.4`, `ENQUIRY_TO` secret set). Step 6 passed on 27 Nov 2026: reference `SD-20261127-6EP28L` arrived in the inbox.

Without the binding or the secret the form still works: it opens the visitor's email app with the enquiry pre-filled.

1. Cloudflare dashboard → `sreejithdigital.com` → **Email → Email Routing** → enable it (Cloudflare adds the MX/TXT records).
2. **Destination addresses** → add your inbox and click the verification link Cloudflare emails you.
3. **Routing rules** → create `hello@sreejithdigital.com` → your inbox (this also makes the address shown on the site work).
4. In `wrangler.toml`, uncomment:
   ```toml
   [[send_email]]
   name = "ENQUIRY_EMAIL"
   ```
5. Set the destination as a secret so it never appears in this public repository:
   ```bash
   npx wrangler secret put ENQUIRY_TO   # paste your verified inbox address
   ```
   (or Workers → `sreejith-digital` → Settings → Variables and Secrets → add secret `ENQUIRY_TO`).
6. Commit, let Workers Builds deploy, then send a test from `/free-seo-review/`. You should land on `/thank-you/?ref=SD-…` and receive an email with the same reference. Reply-To is the visitor's address.
7. Optional: create a KV namespace, uncomment the `[[kv_namespaces]]` block with its id, and every enquiry is also kept for 180 days.

### 2. Analytics (only after consent)

**Status 27 Nov 2026: live through Google Tag Manager.**

| Tool | ID | Where it is configured |
| --- | --- | --- |
| Google Tag Manager | `GTM-K4MJL3SM` (account "Sreejith") | `GTM_CONTAINER_ID` in `scripts/generate_site.py` |
| Google Analytics 4 | `G-EP5M7JTRXK` (account "Sreejith Digital", property 565911323) | Google tag in GTM, trigger Initialization – All Pages |
| Microsoft Clarity | `zkbxk7xkbk` | Custom HTML tag in GTM, trigger All Pages |

- `main.js` loads GTM only after the visitor chooses **Allow analytics**. Before GTM loads it sets Consent Mode v2 defaults: `analytics_storage` granted, `ad_storage`, `ad_user_data` and `ad_personalization` denied. "No thanks" loads nothing.
- Events pushed to the dataLayer: `form_start` (`form_location`) and `generate_lead` (`reference`, sent to GA4 as `enquiry_reference`), each with a GA4 event tag in GTM.
- GA4: data retention 14 months; linked to the Search Console Domain property. Mark `generate_lead` as a key event in Admin → Events once the first one arrives (GA4 only lists events it has received).
- Keep `GA4_MEASUREMENT_ID` and `CLARITY_PROJECT_ID` empty while GTM is set, or the tools load twice.
- **Before adding Google Ads tags:** add an advertising choice to the consent banner and send `ad_storage`, `ad_user_data` and `ad_personalization` updates from it. Ads conversion tags then go into GTM without code changes.

### 3. Search engines and crawlers

**Status 27 Nov 2026:** Search Console, Bing Webmaster Tools and the `www` redirect are done (see the hardening table above). Still to do: request indexing for the key pages.

- Google Search Console → add a **Domain** property for `sreejithdigital.com` (DNS TXT verification in Cloudflare) → submit `https://sreejithdigital.com/sitemap.xml` → request indexing for `/`, `/about/`, the case study and `/free-seo-review/`.
- Bing Webmaster Tools → **Import from Google Search Console**.
- Cloudflare → **Security → Bots / AI Crawl Control**: make sure search and citation crawlers (Googlebot, Bingbot, OAI-SearchBot, PerplexityBot) are allowed. Blocking only training crawlers is a valid choice.
- Add the `www` → apex Redirect Rule described below.

## What changed in the repository

- All deployable files were moved into `public/`.
- A root-level `wrangler.toml` now declares `public/` as the static-assets directory.
- `not_found_handling = "404-page"` enables the custom `404.html`.
- `html_handling = "auto-trailing-slash"` preserves clean directory URLs such as `/services/seo-consulting/`.
- `package.json` and `package-lock.json` pin Wrangler `4.168.0`, matching the version in the build log.
- A mirrored `public/wrangler.toml`, `public/package.json`, and `public/.assetsignore` make the build work even if Cloudflare’s root directory is accidentally set to `/public`. The preferred root directory is still `/`.
- Both Wrangler configs declare `sreejithdigital.com` as a custom domain so Cloudflare can create its DNS record and certificate during deployment.
- `public/_redirects` now contains only supported path-level redirects. Host-level redirects were removed because domain-level redirects are not supported in `_redirects`.

> The Cloudflare account is not connected to this workspace, so DNS records, custom domains, and project settings have not been changed here.

## Path A — keep the current Workers Builds project

This is the fastest fix: no project recreation is required.

1. Confirm Cloudflare is connected to this repository and that the configured production branch contains the latest commit. Production branch should be `main`; if the project is configured to watch `arena/06fc82b3-sreejith-digital`, that branch is also synced to the same commit. The earlier README-only state is resolved.
2. In Cloudflare, open the project’s **Settings → Builds & deployments**.
3. Confirm these values:

   | Setting | Value |
   | --- | --- |
   | Root directory | `/` |
   | Build command | Empty |
   | Deploy command | `npx wrangler deploy` |
   | Production branch | `main` (or the synced active branch, if that is what Cloudflare is configured to watch) |

4. On the latest commit, trigger **Retry deployment**. A fresh commit to the configured production branch should also trigger auto-deploy if enabled.
5. Verify that the deployment succeeds, dependencies are detected, assets are read from `public/`, and the custom-domain route is created.

The preferred root directory is `/`. If it is already set to `/public`, the mirrored `public/wrangler.toml` fallback should still deploy, but change it back to `/` when convenient so the root configuration remains the single source of truth.

`wrangler.toml` uses the Worker name `sreejith-digital` to match the name supplied by Cloudflare Workers Builds. `preview_urls = false` is set explicitly so Wrangler does not emit the implicit Preview URLs warning. If you rename the Worker in Cloudflare, update `name` in both the root and mirrored `public/wrangler.toml` files.

### Attach the apex custom domain

The `[[routes]]` entry in `wrangler.toml` should be retained so the custom-domain binding stays attached to the Worker during each deployment. The apex domain is already resolving on Cloudflare; a content deployment does not need a new custom-domain setup.

If the custom domain is ever detached or stops resolving:

1. Open **Workers & Pages → your Worker → Settings → Domains & Routes**.
2. Select **Add → Custom Domain**.
3. Enter `sreejithdigital.com` — no hyphen.
4. Select **Add Custom Domain** and let Cloudflare create the required DNS record and certificate. Workers custom domains require the zone’s nameservers to be managed by Cloudflare, which is the case here.

Do **not** enter `sreejith-digital.com`; that name is not delegated.

## Path B — classic Cloudflare Pages

If you prefer the older Pages workflow:

1. Go to **Workers & Pages → Create → Pages → Connect to Git**.
2. Select `Sree278/sreejith-digital` and the desired branch.
3. Use these settings:

   | Setting | Value |
   | --- | --- |
   | Framework preset | None |
   | Build command | Empty |
   | Build output directory | `public` |
   | Root directory | `/` |
   | Deploy command | None — do not use `npx wrangler deploy` |

4. Save and deploy.
5. Under **Custom domains**, add `sreejithdigital.com`.

Do not mix the two paths: a classic Pages project should not have a Wrangler deploy command, and a Workers Builds project should not set a Pages build output directory.

## Redirect `www` to the apex

`_redirects` does not support domain-level redirects. Use a zone-level rule instead.

Cloudflare’s documented Pages/Workers approach is:

1. Go to **Bulk Redirects** and create a redirect list with:

   | Source URL | Target URL | Status | Parameters |
   | --- | --- | --- | --- |
   | `www.sreejithdigital.com` | `https://sreejithdigital.com` | `301` | Preserve query string · Subpath matching · Preserve path suffix · Include subdomains |

2. Create a Bulk Redirect rule using that list.
3. In **DNS**, create this record for `www`:

   | Type | Name | IPv4 address | Proxy status |
   | --- | --- | --- | --- |
   | `A` | `www` | `192.0.2.1` | Proxied |

4. If an earlier attempt added a `www` CNAME to `*.pages.dev` or the Worker, remove that conflicting record before adding the dummy proxied `A` record. Do not attach `www` as a second custom domain while using this Bulk Redirect DNS pattern.
5. Wait for DNS propagation and verify:

   ```bash
   curl -I https://www.sreejithdigital.com/services/
   ```

   The response should be `301` with a `Location` header on `https://sreejithdigital.com/services/`.

Reference: [Cloudflare — Redirecting www to domain apex](https://developers.cloudflare.com/pages/how-to/www-redirect/).

## TLS and Cloudflare settings

- **SSL/TLS → Overview:** Full (strict)
- **SSL/TLS → Edge Certificates → Always Use HTTPS:** On
- **Minimum TLS Version:** 1.2 or higher
- Wait until the custom-domain certificate is active before announcing the site.
- Enable HSTS only after confirming every intended subdomain works over HTTPS.

`public/_headers` adds `nosniff`, a referrer policy, a permissions policy, and a short asset cache lifetime. It intentionally avoids frame-blocking headers so browser previews and approved embeds are not broken.

## Verify the deployment

```bash
curl -I https://sreejithdigital.com/
curl https://sreejithdigital.com/version.txt
curl https://sreejithdigital.com/robots.txt
curl https://sreejithdigital.com/sitemap.xml
curl -I https://sreejithdigital.com/locations/delhi-ncr/
curl -I https://sreejithdigital.com/resources/seo-cost-india/
curl -I https://sreejithdigital.com/this-page-does-not-exist/
```

Expected results:

- Apex home page returns `200`.
- `/version.txt` shows `release: 2026-11-26.5` and `indexable-pages: 36`.
- `/robots.txt` lists `https://sreejithdigital.com/sitemap.xml`.
- `/sitemap.xml` contains 36 clean directory URLs, including Delhi NCR, Hyderabad, Pune and the four India-focused guides.
- `/locations/delhi-ncr/` and `/resources/seo-cost-india/` return `200`.
- A nonexistent path returns `404` and renders `public/404.html`.
- Deep links such as `/services/seo-consulting/` and `/resources/technical-seo-audit-checklist/` return `200`.
- Dropdowns and the mobile menu work without console errors.
- The contact form opens the visitor’s email application with a prefilled enquiry.
- If the `www` redirect has been configured, `https://www.sreejithdigital.com/services/` returns `301` to the equivalent apex URL.

Then submit `https://sreejithdigital.com/sitemap.xml` in Google Search Console.

## Optional GitHub Pages fallback

`public/CNAME` and `public/.nojekyll` remain available for GitHub Pages. If used, deploy the `public` folder from the production branch and enter `sreejithdigital.com` as the custom domain. At Cloudflare DNS, use GitHub’s current documented apex `A`/`AAAA` records and handle `www` with a Cloudflare Redirect Rule. Use DNS-only mode until GitHub has issued the custom-domain certificate.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Same `Could not detect a directory containing static files` error after a fix | Check that Cloudflare is connected to this repository and to a branch containing `wrangler.toml`, `public/`, and `package.json`. `main` now contains the site. |
| `DNS_PROBE_POSSIBLE` on `sreejith-digital.com` | Use `sreejithdigital.com` without the hyphen. The hyphenated name is not delegated. |
| `sreejithdigital.com` stops resolving | Check Cloudflare DNS and **Domains & Routes**, then redeploy so the `[[routes]] custom_domain = true` entry can re-create the binding. Wait for the certificate to become active. |
| Live site shows the old homepage, a 29-URL sitemap, or `/version.txt` returns `404` | Cloudflare has not published the latest commit. Select the latest commit in Workers Builds and click **Retry deployment**; confirm production branch, root `/`, and deploy command `npx wrangler deploy`. Then purge cache and recheck `/version.txt`. |
| `No dependencies detected to cache` plus `npx` installing Wrangler | Usually means Cloudflare is cloning the wrong branch or a subfolder without `package.json`. Verify production branch and root directory `/`. |
| `Could not detect a directory containing static files` on the correct branch | Ensure `wrangler.toml` is committed, `public/index.html` exists, and the preferred Workers Build root directory is `/`. A `/public` root should work through the mirrored fallback config. |
| Wrangler still installs a random version | Confirm `package.json` and `package-lock.json` are committed; Cloudflare should install the pinned Wrangler before the deploy command. |
| CSS/JS returns 404 | Workers: check `wrangler.toml` asset directory. Pages: set build output directory to `public`. |
| Deep link returns 404 | Workers: confirm `html_handling = "auto-trailing-slash"`. Pages: confirm `public` is the output directory. |
| Custom 404 is ignored | Workers: confirm `not_found_handling = "404-page"`. Pages: confirm `public/404.html` is in the deployed output. |
| `www` does not redirect | Use Bulk Redirects / Redirect Rules at the zone level; do not rely on domain-level rules in `_redirects`. |
| Redirect loop | Remove conflicting Bulk Redirects, Page Rules, and old `www` DNS records, then keep one canonical redirect method. |
| Certificate pending | Confirm Cloudflare nameservers, DNS proxy status, and SSL/TLS mode; allow more time for issuance. |
| Sitemap shows wrong host | Update `BASE_URL` in `scripts/generate_site.py`, regenerate, commit, and redeploy. |

## Before announcing the site

- Confirm `hello@sreejithdigital.com` exists, or change `CONTACT_EMAIL` in `scripts/generate_site.py` and regenerate.
- Confirm the seven city guides match genuine service areas without implying physical offices.
- Review the privacy and terms pages, especially if analytics, a CRM, calendar booking, or a form backend is added later.
- Connect a real form endpoint if you do not want enquiries to rely on the visitor’s email app.
- Verify that no fabricated client names, testimonials, rankings, or case-study metrics were added.
- Purge the Cloudflare cache after a content update if cached HTML does not refresh immediately.

## Gated phone number (28 Nov 2026)

The contact page shows the phone/WhatsApp number only after a visitor gives a valid, non-disposable email (`/api/contact` in `worker/index.js`). The number is never in the HTML or schema.

Owner steps (secrets never go in this repo):
1. `npx wrangler secret put CONTACT_PHONE` — enter the number with country code, e.g. `+919XXXXXXXXX`. Until set, the panel says the number is not available online.
2. Optional human challenge (recommended): create a free Cloudflare Turnstile widget for sreejithdigital.com, then `npx wrangler secret put TURNSTILE_SECRET` and put the public site key in `TURNSTILE_SITE_KEY` in `scripts/generate_site.py`.
3. Optional: add a Cloudflare WAF rate-limiting rule on `/api/contact` (the Worker's own limit is best effort per instance).

Accepted: Gmail, Outlook/Hotmail, Yahoo, iCloud, Proton, Zoho, Rediff and any domain with a working MX record. Rejected: disposable inboxes and relay/alias services (Apple private relay, SimpleLogin, addy.io, Firefox Relay, duck.com). Every successful reveal emails the visitor's address to ENQUIRY_TO as a lead.


## Phone safeguards, stage 2 (28 Nov 2026)

The code is live and switches on piece by piece. Nothing breaks if a piece is not set up yet.

| Safeguard | Turn it on |
|---|---|
| Turnstile human check | Cloudflare dashboard → Turnstile → Add widget for `sreejithdigital.com`. Put the site key in `TURNSTILE_SITE_KEY` in `scripts/generate_site.py`; add the secret as `TURNSTILE_SECRET` (Worker → Settings → Variables and Secrets). |
| Daily cap (default 20 a day) | Workers & Pages → KV → create a namespace, then bind it to the Worker as `CONTACT_KV`. Optional variable `DAILY_REVEAL_CAP`. |
| Email-link verification | Free Brevo account (300 emails a day). Verify a sender address, create an API key, then add secrets `BREVO_API_KEY`, `VERIFY_FROM` (the verified sender) and `VERIFY_SECRET` (any long random string). When all three exist, the number appears only after the visitor opens the emailed link (valid 30 minutes, single use when KV is bound). |

Test after each step on `/contact/`: a Gmail plus a real mobile gets an email; the link shows the number; opening it twice is refused.

**Status, 28 Nov 2026:** Turnstile is ON (widget `sreejithdigital-contact`, secret `TURNSTILE_SECRET`, site key in `generate_site.py`). The daily cap is ON (KV namespace `sreejith-contact` bound as `CONTACT_KV` in `wrangler.toml`; cap 20 a day). Email-link verification is OFF until `BREVO_API_KEY`, `VERIFY_FROM` and `VERIFY_SECRET` are added.
