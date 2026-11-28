# Project log — sreejithdigital.com (complete history, A–Z)

This is the single record of everything planned and done on this website, from the empty repository onwards. It is written for two uses: a historical record, and the source material for the final case study. It is the only log; the other documents link here.

**How to read it.** Entries run **oldest first**, grouped into phases. Each entry answers five questions: **What** changed, **Why**, **When** (UTC, with the release or PR), **Where** (repo files, Cloudflare, third-party tools) and **How** (method and checks), followed by the **Evidence** and anything left **Open**. IST = UTC + 5:30.

| Resource | Where |
| --- | --- |
| Strategy, milestones, KPIs, keyword map | [`SEO-STRATEGY.md`](SEO-STRATEGY.md) |
| Deployment and owner checklist | [`DEPLOYMENT.md`](DEPLOYMENT.md) |
| Live tracker (milestones, actions, KPIs, 20 keywords) | https://claude.ai/artifact/Vf1ESoPRJQ3FEnYbBuLxpG |
| Case study deck (updated after each task) | https://claude.ai/artifact/QNtkQzmRkkaafw8Jju5Kae |
| Task briefs given to other tools | [`docs/briefs/`](docs/briefs/) |
| Repository | https://github.com/Sree278/sreejith-digital (PRs #1–#29) |

**Who did the work.** Owner: Sreejith CU (decisions, approvals, merges, passkeys, sign-ins, payments). Builders: the Arena coding agent (site build on 26 Nov; Tamil Nadu pages on 27 Nov) and Claude (audit, SEO, infrastructure, measurement, contact safeguards from 27 Nov). Every change reached production through a GitHub pull request merged by the owner.

---

## At a glance

| # | When (UTC) | Phase | What | Where | Status |
| --- | --- | --- | --- | --- | --- |
| A | 26 Nov, 08:37–11:23 | Build and launch | Static site built, deployed on Cloudflare Workers, custom domain attached | PRs #1–#3 | Done |
| B | 26 Nov, 13:50–18:31 | First SEO pass | India SEO strategy v1, homepage, navigation, site-wide title pattern | PRs #4–#10 | Done; pattern later reversed |
| C | 27 Nov, 02:58 | Audit and repair | Doorway and spam fixes, case study, enquiry form, schema, privacy | PR #11, release 27.1 | Done |
| D | 27 Nov | Research | Kerala competitors, Mindtech playbook, keyword and AI-prompt research | `SEO-STRATEGY.md` §6, §15–17 | Done |
| E | 27 Nov, 14:16–15:23 | Location build-out | 8 Kerala city pages, Tamil Nadu hub and 3 city pages | PR #12, release 27.2 | Done |
| F | 27 Nov, 17:58 | Positioning | "Senior SEO expert"; no "independent"/"freelancer" | PR #13 | Done |
| G | 27 Nov, 18:06–18:41 | Domain hardening | HTTPS, HSTS, www, DNSSEC, email routing, consoles, favicons, form to inbox, auto-deploy fix | Cloudflare; PRs #14–#15, release 27.4 | Done |
| H | 27 Nov, 18:41 | Measurement | GTM, GA4, Clarity behind consent; Consent Mode v2 | PR #16, release 27.5 | Done |
| I | 28 Nov, 07:01–08:31 | Competing nationally | Gap plan vs Jijo Joseph; "SEO consultant India" pages and pricing; owner inputs | PRs #17, #20, #21, release 28.1 | Done |
| J | 28 Nov, 07:54–08:05 | Contact details | Area address in schema; phone shown only after email + mobile checks; hours; "SEO since 2015" | PRs #18–#19, releases 28.2–28.3 | Done |
| K | 28 Nov, 08:56–10:21 | Phone safeguards | Signed email link, daily cap (KV), Turnstile | PRs #22–#25 | Done |
| L | 28 Nov, 10:39–11:20 | Email verification switched on and debugged | Brevo sender, invalid key replaced, token reuse fixed, logs on, link bug fixed | PRs #26–#29 | PR #29 awaiting merge |

---

## Starting state (26 Nov 2026, before any work)

- **Domain:** `sreejithdigital.com` registered through Cloudflare Registrar on 26 Nov 2026 (expires 26 Nov 2027).
- **Repository:** `Sree278/sreejith-digital` created 26 Nov 2026 08:37 UTC with only a README.
- **Search presence:** 0 indexed pages, 0 rankings, 0 referring domains, 0 reviews, 0 enquiries, no Google Business Profile.
- **Business:** Sreejith CU, SEO consultant from Thrissur, Kerala, now based in Chennai (Perungalathur, GST Road), selling SEO consulting across India. One named client result available: Mindtech Solutions (MEP/HVAC contractor).

---

## Phase A — Build and launch (26 Nov 2026)

### A1. Static site built
- **What:** a deployment-ready static website: home, about, contact, 8 services, 4 industries, location pages (Bengaluru, Chennai, Kochi, Mumbai), 4 resources, privacy, 404, robots, sitemap. A Python generator (`scripts/generate_site.py`) writes every page from one source.
- **Why:** a fast, crawlable site with no CMS to maintain or patch.
- **When:** 26 Nov, 09:03 UTC (commit `982acb1`), by the Arena agent.
- **Where:** `scripts/generate_site.py`, `public/` (output), `assets/css`, `assets/js/main.js`.
- **How:** generated HTML with shared header/footer components, canonical tags and JSON-LD.

### A2. Deployed on Cloudflare Workers (PRs #1–#2)
- **What:** site moved to `public/`, Wrangler pinned in `package.json`, Workers Builds configuration, deployment guide; Worker name aligned and `preview_urls = false`.
- **Why:** Cloudflare's build was failing because `main` held only the README.
- **When:** PR #1 merged 11:02 UTC; PR #2 merged 11:11 UTC.
- **Where:** `wrangler.toml`, `package.json`, `DEPLOYMENT.md`, Cloudflare Workers Builds.

### A3. Custom domain attached (PR #3)
- **What:** custom-domain route for `sreejithdigital.com` (no hyphen) in Wrangler.
- **Why:** DNS had been set up on the hyphenated `sreejith-digital.com` by mistake.
- **When:** PR #3 merged 11:23 UTC.
- **Where:** `wrangler.toml`, Cloudflare DNS, `DEPLOYMENT.md`.

---

## Phase B — First SEO pass (26 Nov 2026)

| PR | Merged (UTC) | What | Why |
| --- | --- | --- | --- |
| #4 | 13:51 | India SEO strategy v1; Delhi NCR, Hyderabad, Pune location guides; 4 India resources; keyword alias redirects; `SEO-STRATEGY.md` | Give the site an India-wide keyword map |
| #5 | 14:03 | Homepage title, H1, India content structure, FAQ content and schema | Homepage targets "SEO expert in India" |
| #6 | 14:29 | `/version.txt` release marker; fresh commit to trigger a build | Confirm which release is live |
| #7 | 17:15 | Navigation dropdowns: complete, viewport-safe, scrollable, close on scroll/outside focus | Menus were cut off and missing items |
| #8 | 17:36 | Slow "breathing" hover on the secondary button, with reduced-motion fallback | Owner design request |
| #9–#10 | 18:18, 18:31 | "SEO Expert & Consultant \| …" pattern on every title, H1, meta, schema and first sentence of all 37 pages (releases 26.4–26.5) | Owner request |

- **Result:** 36 indexable pages. The site-wide title pattern was later judged a spam signal and removed in Phase C.

---

## Phase C — Audit and repair (27 Nov 2026, release 2026-11-27.1, PR #11)

- **What:**
  - **Doorway fix:** 7 template city pages → 5 project-based pages (Bengaluru and Delhi NCR: client results; Hyderabad: in progress; Chennai: home base; Kerala: home state). Mumbai and Pune 301 → `/locations/`; Kochi 301 → `/locations/kerala/`.
  - **Spam-pattern fix:** the forced "SEO Expert & Consultant" pattern removed; every page got a unique, intent-matched title and a natural H1; home targets India, the Chennai page owns Chennai.
  - **Proof:** `/case-studies/` hub and the Mindtech Solutions case study (Aug 2026 baseline → page-1 positions 6 Nov 2026 → Google AI Overview citation 25 Nov 2026), including what had not moved.
  - **New pages:** AI search optimisation service; construction and MEP contractors industry page; "City pages without doorway risk" guide; free SEO review offer; thank-you page.
  - **Conversion:** `/api/enquiry` Worker endpoint with a `mailto:` fallback, enquiry references, header and sticky mobile "Free SEO review" buttons, a short qualifying form.
  - **Entity and schema:** one graph per page — ProfessionalService → founder Person "Sreejith CU"; ProfilePage on About; author bylines; Service and FAQPage only where content is visible.
  - **Fixes:** phone menu button pushed off-screen by a CSS specificity bug; SVG social image replaced by a 1200 × 630 PNG; privacy policy rewritten for India's DPDP Act; terms updated.
- **Why:** a deep-research audit found a `mailto:`-only form and no analytics; city pages 81–87% identical once city names were removed (doorway risk); the same title pattern on all 37 files; at least six other "Sreejith" SEO professionals in search (entity collision). Opportunity: Chennai and Kerala results full of unverifiable "No.1" claims and few dated case studies.
- **When:** PR opened 27 Nov 02:58 UTC; merged 15:23 UTC.
- **Where:** `scripts/generate_site.py`, `worker/index.js` (new), `SEO-STRATEGY.md` v2 §1–14, `public/`.
- **How / evidence:** city-page similarity after removing city names fell from **81–87% to 41–56%**; 40 sitemap URLs, no broken links, unique titles and descriptions, valid JSON-LD; Chrome renders at 390, 700, 1024 and 1440 px with no overflow or console errors; `npx wrangler deploy --dry-run` passes (Wrangler 4.168.0).
- **Rule adopted — the city-name test:** swap the city name for another. If the page is still true, it is a doorway page and does not go live.
- **Also created:** the live tracker and the 12-slide case study deck (links above). Milestones M0–M6 set in `SEO-STRATEGY.md` §10.

---

## Phase D — Research (27 Nov 2026)

### D1. Kerala competitor research
- **What:** Google India results for five Kerala "seo expert in" queries; leaders' sites read. Top 3: Jijo Joseph, Nikhil Soman, Prasad Karthik.
- **Why:** decide how to outrank Kerala consultants.
- **Decision:** the earlier idea of thin Kochi, Calicut, Mumbai, Kolkata and Noida pages dropped (doorway policy).
- **Where:** `SEO-STRATEGY.md` §15.

### D2. Mindtech playbook applied
- **What:** what produced the Mindtech results (page 1 for five terms, one AI Overview citation) mapped to this site; home and five location pages retitled "SEO expert in …" to match Google autocomplete.
- **Gap found:** no third-party profiles yet; Mindtech's lesson was to start them in week one.
- **Where:** `SEO-STRATEGY.md` §16.

### D3. AI-prompt and question research
- **What:** LSIGraph top AI prompts and AnswerThePublic data for "seo expert in kerala" (1.9K searches/month and the freelance/best/top-10 variants). The Kerala page now answers all five LSIGraph prompts.

### D4. Keyword research with free tools
- **What:** Google, Bing and YouTube autosuggest, Google Trends, Ahrefs free keyword generator and backlink checker, added to Keyword Planner, AnswerThePublic and LSIGraph data. `SEO-STRATEGY.md` §6 became a data-backed keyword → page map.
- **Findings:** Kerala has India's highest Trends interest in "seo expert" (down 50% YoY); "seo expert in kerala/kochi", "seo company in kerala" and "seo services in chennai" rated Ahrefs "Easy"; Chennai leads "seo company in" and "seo services in" suggestions. Competitor authority: Nikhil DR 55, Jijo DR 32, Prasad DR 18, Sreehari DR 0 (still #2 in Kochi).
- **Correction recorded:** a batched Ahrefs check first showed DR 32 for this site; a one-at-a-time recheck showed DR 0 and 0 backlinks (the 32 was Jijo Joseph's).

### D5. Owner facts added
- **What:** home town Thrissur; consults in English and Malayalam; based in Chennai and meets Kerala clients in person when travelling. Applied to Person schema (`knowsLanguage`), About, home, Kerala hub and all city pages.
- **Limit:** a Chennai-based Google Business Profile cannot list Kerala service areas, so Kerala map-pack results stay out of reach; organic and AI-answer visibility are the target there.

---

## Phase E — Location build-out (27 Nov 2026, PR #12, release 2026-11-27.2)

### E1. Eight Kerala city pages
- **What:** `/locations/kerala/{kochi,trivandrum,calicut,thrissur,malappuram,kannur,kollam,palakkad}/`, each with local sectors, search behaviour, localities, a dated page-1 snapshot, city FAQs, an "In short" answer and nested Service schema (City > District > State > Country, Wikipedia `sameAs`). Kerala FAQs answer cost, "best SEO expert" and "company vs independent expert".
- **Why:** owner asked to rank for "SEO expert in <city>" across Kerala first, routed Country > State > City > Town.
- **Policy change (owner, 27 Nov):** the proof gate was dropped; kept were the city-name test, honesty (no fake office or borrowed results) and a **demand gate** (Google autocomplete suggestion or 100+ searches/month in Keyword Planner).
- **Evidence:** 48 indexable pages pass title, description, H1, canonical, JSON-LD and link checks; city pages 50–60% similar (shared part is navigation components).

### E2. Tamil Nadu hub and three city pages
- **What:** `/locations/tamil-nadu/` plus Coimbatore, Madurai and Salem; `KERALA_CITIES` refactored into `STATE_CITIES`; four-level breadcrumbs, FAQPage schema, ItemList, `areaServed`, five redirect rules.
- **Why:** Chennai is in Tamil Nadu, and Tamil Nadu tier-2 cities dominate "seo company in" suggestions.
- **When:** built by the Arena agent from brief [`docs/briefs/2026-11-27-tamil-nadu-pages-and-deploy.md`](docs/briefs/2026-11-27-tamil-nadu-pages-and-deploy.md) in six checkpoints (14:54–15:21 UTC); PR #12 merged 15:23 UTC.
- **How:** each page has four verified sectors (district `.nic.in` sources), ten localities, five city FAQs and three dated page-1 observations from logged-out Google India searches (`gl=in`, `hl=en`, `pws=0`). No Tamil-language consulting, local office, "best" or "No. 1" claim.
- **Evidence:** 52 indexable pages; titles unique ≤ 62 chars; descriptions 70–160; one H1 each; JSON-LD parses; canonicals self-referencing; all hrefs resolve; Tamil Nadu city pages 55.6–57.9% similar (gate ≤ 60%); 390/1280 px renders passed live.

---

## Phase F — Positioning (27 Nov 2026, PR #13)

- **What:** every self-description says "SEO expert / senior SEO consultant"; agency-vs-expert FAQs say "dedicated expert"; schema job title, byline, footer and OG image updated.
- **Why:** the site should read as a senior specialist, not a solo freelancer.
- **When:** merged 17:58 UTC.
- **Evidence:** 0 matches for "independent"/"freelanc" across `public/`. Search-query data that people type (e.g. "freelance seo expert india") kept in the strategy on purpose.

---

## Phase G — Domain hardening (27 Nov 2026, PRs #14–#15, release 2026-11-27.4)

- **What (Cloudflare):** Always Use HTTPS; minimum TLS 1.2; SSL Full (strict); HSTS 6 months with includeSubDomains (no preload); Certificate Transparency alerts; `www` record + 301 to the apex (path and query kept); DNSSEC; Email Routing `hello@` → owner Gmail with SPF, DKIM and DMARC `p=reject`; Google Search Console Domain property and Bing Webmaster Tools verified by DNS, sitemaps submitted; Crawler Hints (IndexNow) on; Worker secret `ENQUIRY_TO`.
- **What (repo):** `[[send_email]]` binding so the form emails enquiries straight to the inbox; favicon set (`/favicon.ico`, `/apple-touch-icon.png`, 192 and 512 PNGs, `/site.webmanifest`); `logo` in ProfessionalService schema.
- **Why:** `http://` and `https://` both returned 200 (every page existed twice); `www` did not resolve; TLS 1.0 was accepted; `hello@` had no MX, so enquiries bounced; nothing was verified in a search console; Google needs a favicon that is a multiple of 48 px; production was two releases behind `main`.
- **Root cause of stale deploys (fixed):** Cloudflare's GitHub App could only see `Sree278/dotmiracle`, so merges to `main` started no build. `sreejith-digital` was added to its access (owner passkey).
- **When:** PR #14 merged 18:11 UTC; PR #15 (verified results) 18:41 UTC.
- **Evidence:** SSL Labs **A+** on all four edge IPs; DNSSEC DS + AD=true; MX ×3, SPF, DMARC; `http://…/about/?a=1` → 301 HTTPS with query; `www` → 301 apex; all 52 URLs 200 with self-canonicals and valid JSON-LD; test email to `hello@` shows **Forwarded**; test enquiry landed on `/thank-you/?ref=SD-20261127-6EP28L` and arrived in Gmail (not spam). Billing "payment failed" notices were retries; all invoices paid; registrar lock, WHOIS privacy and auto-renew on.

---

## Phase H — Measurement (27 Nov 2026, PR #16, release 2026-11-27.5)

- **What:** GA4 property `sreejithdigital.com` (565911323), stream `G-EP5M7JTRXK`, 14-month retention, linked to Search Console; Microsoft Clarity `zkbxk7xkbk`; Google Tag Manager `GTM-K4MJL3SM` with the GA4 tag, `generate_lead` and `form_start` events and the Clarity tag. `main.js` loads GTM only after "Allow analytics" and sets Consent Mode v2 defaults (analytics granted, all ad signals denied).
- **Why:** owner plans Google Ads; one GTM container lets Ads conversion tags be added later without code changes. Loading only after consent keeps the DPDP privacy promise.
- **When:** merged 18:41 UTC.
- **Evidence:** headless Chromium: no third-party request before consent; after "Allow" one request to `gtm.js`; `generate_lead` pushed on the thank-you page; after "No thanks" no third-party request. GA4 live report showed 1 visitor and 1 test lead (`SD-20261127-TESTGA`, internal). Indexing for 6 key pages requested in Search Console (status: "Discovered – currently not indexed"); all 52 pages submitted to Bing. Auto-deploy proven by this merge.
- **Open:** mark `generate_lead` as a GA4 key event; filter internal traffic; add an advertising consent choice before any Google Ads tag.

---

## Phase I — Competing nationally (28 Nov 2026)

### I1. Gap plan against Jijo Joseph (PR #20)
- **What:** competitor snapshot (~26 pages, 36 posts), winnable-now vs later keyword tiers, actions. Docs only.
- **Where:** `SEO-STRATEGY.md` §18. **When:** written 07:01, merged 08:16 UTC.

### I2. "SEO consultant India" page set and pricing (PR #17, release 2026-11-28.1)
- **What:** `/services/seo-consulting/` retargeted to "SEO consultant in India" with 2 new FAQs incl. price range; `/resources/seo-cost-india/` gained dated published price ranges (₹10,000–₹50,000/month market range, owner-approved placeholder); new guide `/resources/seo-consultant-vs-agency-india/`.
- **Why:** SERP checks showed MysticDigi and Jijo Joseph winning "seo consultant in india" with a dedicated page and prices in the snippet; Google's AI Overview for "seo expert in india" quotes ₹ ranges.
- **When:** merged 07:19 UTC. **Evidence:** 53 pages rebuilt.

### I3. Owner inputs recorded (PR #21)
- **What:** Mindtech approved naming and rankings (by phone, owner confirmed). No LinkedIn or headshot yet, so no `sameAs` published. **When:** merged 08:31 UTC.

---

## Phase J — Contact details and gated phone number (28 Nov 2026)

### J1. Area address and gated phone (PR #18, release 2026-11-28.2)
- **What:** postal code 600063 (Perungalathur, Chennai) in schema and a "where I work from" panel on `/contact/` (area only, no street). New `/api/contact` Worker route shows the phone only after checks: email format, disposable/relay blocklist, reputable-provider allowlist, MX check, honeypot, fill-time check, per-IP/email limits. The number lives only in the `CONTACT_PHONE` secret; no `telephone` in schema. Every reveal emails the owner.
- **Why:** owner wanted the number hidden from scrapers and spam and shown only to genuine people.
- **When:** merged 07:54 UTC. **Evidence:** 11 gating cases tested; contact page at 390/1280 px.

### J2. Visitor mobile, hours, "SEO since 2015" (PR #19, release 2026-11-28.3)
- **What:** visitors must also give their own mobile (fillers like 9999999999 rejected), included in the owner's notification; hours 9am–6pm IST (`openingHoursSpecification`, Mon–Fri assumed); "SEO since 2015" on About, home and Person schema.
- **When:** merged 08:05 UTC. **Evidence:** 14 gating cases tested.

---

## Phase K — Phone safeguards (28 Nov 2026)

| PR | Merged (UTC) | What | Where |
| --- | --- | --- | --- |
| #22 | 08:56 | Signed 30-minute email link (`/api/contact/verify`, HMAC with `VERIFY_SECRET`), daily reveal cap, Turnstile hook — each inert until its secret/binding exists | `worker/index.js`, `main.js`, `DEPLOYMENT.md` |
| #23 | 10:15 | Turnstile widget created (managed mode); public site key on the form; `TURNSTILE_SECRET` set | Cloudflare Turnstile, generator |
| #24 | 10:19 | KV namespace `sreejith-contact` bound as `CONTACT_KV`: daily cap of 20 reveals and single-use links | `wrangler.toml`, Cloudflare KV |
| #25 | 10:21 | Status recorded | `DEPLOYMENT.md`, this log |

- **Why:** the first gate (Phase J) only checked the email's format and domain. A real person must now prove they own the inbox, pass a bot check, and there is a hard ceiling per day.
- **How:** stateless signed token — no database of pending requests; KV only records used links and the daily count. Tested locally: send, verify, reuse refused, tampered token refused.
- **Evidence:** a request without a Turnstile token is refused with `challenge_failed`; the widget renders on `/contact/`.

---

## Phase L — Email verification switched on and debugged (28 Nov 2026)

1. **Brevo set up (owner + Claude).** Free Brevo account; domain `sreejithdigital.com` authenticated (two DKIM records, Brevo code, DMARC); sender `hello@sreejithdigital.com`; Brevo phone verification done by the owner; send-only API key; Worker secrets `BREVO_API_KEY` and `VERIFY_SECRET`. **Why Brevo:** a free transactional sender for visitors' own addresses (Cloudflare's `send_email` binding is kept for owner notifications).
2. **PR #26 (10:40 UTC):** `VERIFY_FROM` pinned in `wrangler.toml` so git deploys keep it.
3. **Bug — "Please complete the check" after a green Turnstile tick.** Cause: Turnstile tokens work once, and the widget was not reset after a failed attempt. **PR #27 (10:53 UTC):** reset the widget after every attempt; log Brevo's status and message on a failed send.
4. **Bug — "We couldn't check that address just now".** Worker logs were off, so the reason was invisible. **PR #28 (10:59 UTC):** `[observability] enabled = true`. The log then showed Brevo **401 "Key not found"**: the stored key had been pasted wrongly.
5. **Key replaced (≈11:13 UTC, 16:43 IST).** A new Brevo key was generated and pasted into the `BREVO_API_KEY` secret in the owner's Chrome, then deployed. **Evidence:** the form showed "Check your inbox", and the email "Confirm your email to see my phone number" from `hello@sreejithdigital.com` arrived in Gmail at 16:46 IST (inbox, not spam).
6. **Bug — link opened, no number shown.** Cause: in `main.js` the `?verify=` handler called `setStatus` before its `const` declaration (temporal dead zone), so the script stopped before asking the server. Confirmed live with a dummy link: no message appears at all. **PR #29 (opened 11:20 UTC):** moves the declaration above its first use; `node --check` passes.
   - The red "Workers Builds" check on PR #29 is the branch-preview deploy (`wrangler preview` wants Preview values for `<REPLACE_ME>` placeholders), not the change. Production deploys from `main`.

**Open (Phase L):** merge PR #29, then test end to end: fresh link → number and WhatsApp shown → second click refused → owner notification received. Delete the two unused Brevo keys. Decide on branch-preview builds (fill Preview values or turn them off).

**Owner suggestion not adopted:** "force users to accept analytics". Advised against: the privacy policy promises nothing loads without consent (DPDP), and a forced wall costs enquiries. Alternative offered: cookieless Cloudflare Web Analytics for basic counts. Awaiting the owner's decision.

---

## Where things stand (28 Nov 2026)

| Area | State |
| --- | --- |
| Pages | 53 indexable pages (release 2026-11-28.3): 6 location pages, 8 Kerala and 3 Tamil Nadu city pages, services, industries, resources, case study |
| Infrastructure | Cloudflare Workers; auto-deploy from `main`; SSL Labs A+; DNSSEC; HSTS; www → apex; observability on |
| Email | `hello@` forwards to Gmail; enquiry form delivers to the inbox; Brevo sends visitor verification links |
| Measurement | GSC + Bing verified; GA4, Clarity via GTM behind consent |
| Contact safeguards | Turnstile, email + mobile checks, signed single-use email link, daily cap 20, owner notified per reveal |
| Search results | Not yet indexed by Google ("Discovered – currently not indexed" on 27 Nov); baseline still 0 rankings, 0 referring domains, 0 reviews |

## Decisions and rules adopted (for the case study)

- **No doorway pages:** the city-name test and a demand gate decide every location page.
- **No boilerplate keyword patterns** in titles or headings (the 26 Nov pattern was reversed on 27 Nov).
- **Proof over promises:** results carry a date and method; misses are published; no invented clients, reviews or offices.
- **Privacy first:** no analytics before consent; phone never in HTML or schema.
- **Free tools only** for research, measurement and email.
- **One canonical host:** `https://sreejithdigital.com`.
- **Every change through a PR**, merged by the owner; secrets live only in Cloudflare.

## Lessons learned

- A site-wide keyword pattern looks like optimisation but reads as spam; unique, intent-matched titles replaced it within a day.
- Most launch-day risks were outside the code: bouncing email, duplicate http/https pages, a disconnected GitHub App that silently stopped deploys.
- Turn on logs before debugging a third-party integration: the Brevo failure took one log line to diagnose once observability was on.
- Single-use tokens (Turnstile) need a reset after every attempt, not just after success.
- A JavaScript error on a rarely used path (the emailed link) hides easily; test the whole journey, not just the form.

## Open items and next milestones

- **Now:** merge PR #29 and run the end-to-end link test; delete unused Brevo keys; decide branch-preview builds; decide on analytics approach.
- **Owner:** star `generate_lead` in GA4; internal-traffic filter; LinkedIn, headshot and other profiles (`sameAs`); written Mindtech permission; "from" prices; whether he meets Chennai clients in person (Google Business Profile eligibility); DotMiracle's role.
- **Milestones:** M1 measurement live (due 4 Dec 2026, mostly done); M2 indexed + entity (26 Dec 2026); M3 first traction (25 Jan 2027) — see `SEO-STRATEGY.md` §10.
