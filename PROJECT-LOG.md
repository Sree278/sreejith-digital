# Project log — sreejithdigital.com

Newest first. Each entry records what changed, why, the evidence, and what comes next.

| Resource | Where |
| --- | --- |
| Strategy, milestones, KPIs | [`SEO-STRATEGY.md`](SEO-STRATEGY.md) |
| Live tracker (milestones, actions, KPIs, 20 keywords) | https://claude.ai/artifact/Vf1ESoPRJQ3FEnYbBuLxpG |
| Case study deck (updated after each task) | https://claude.ai/artifact/QNtkQzmRkkaafw8Jju5Kae |
| Deployment and owner checklist | [`DEPLOYMENT.md`](DEPLOYMENT.md) |

---

## 2026-11-27 — Keyword research with more free tools

- Added Google and Bing autosuggest, YouTube autosuggest, Google Trends, and Ahrefs' free keyword generator and backlink checker to the Keyword Planner, AnswerThePublic and LSIGraph data. `SEO-STRATEGY.md` §6 is now a data-backed keyword → page map.
- Findings: Kerala has India's highest Trends interest in "seo expert" (down 50% YoY). "seo expert in kerala", "seo expert in kochi", "seo company in kerala" and "seo services in chennai" are all Ahrefs "Easy". Chennai leads both "seo company in" and "seo services in" suggestions. Tamil Nadu tier-2 cities dominate "seo company in" suggestions.
- Competitor authority: Nikhil DR 55, Jijo DR 32, Prasad DR 18, Sreehari DR 0 (still #2 in Kochi).
- Shipped: AI search service title targets "AI SEO expert"; Chennai description and FAQ cover "SEO services/company in Chennai"; Trivandrum and Calicut FAQs cover the "SEO company" phrasing, which outnumbers "SEO expert" in Trivandrum.
- Correction: a batched Ahrefs check first showed DR 32 against sreejithdigital.com. A one-at-a-time recheck showed DR 0 and 0 backlinks; the 32 was Jijo Joseph's.
- Next (owner): Chennai Google Business Profile as a service-area business (you meet Chennai clients in person). Next build: Tamil Nadu hub plus Coimbatore.

---

## 2026-11-27 — AI-prompt and question research applied

- LSIGraph (via Chrome) listed the top AI prompts for "seo expert in kerala"; AnswerThePublic's free report gave 1.9K searches a month and the freelance / best / top-10 variants.
- Kerala page now answers all five LSIGraph prompts: hiring checklist, local rankings and ecommerce added to the existing best and cost answers. "Freelance" is used where it accurately describes an independent consultant.
- Next: run LSIGraph's free brand check for "Sreejith Digital" after launch, as an AI-visibility baseline.

---

## 2026-11-27 — Owner facts added: Thrissur, Malayalam, in-person meetings

- Owner confirmed: home town Thrissur; consults in English and Malayalam; based in Chennai and meets Kerala clients in person when travelling.
- Applied: `OWNER_ORIGIN`, `OWNER_LANGUAGES` (feeds Person `knowsLanguage` and the About page); home hero; Kerala hub lede, description, FAQ and "How it works"; all eight city pages (answer block, office FAQ, working-together list); Thrissur page marked "Home town" with a home-town lede.
- Checked: 48 pages pass the title, description, H1 and JSON-LD checks; city pages are 51–60% similar after the change.
- Limit: a Chennai-based Google Business Profile can't list Kerala service areas, so Kerala map-pack results stay out of reach. Organic and AI-answer visibility remain the target there.

---

## 2026-11-27 — Location hierarchy and eight Kerala city pages

- Owner asked to rank for "SEO expert in <city>" across Kerala first, then South and North, routed Country > State > City > Town.
- Demand data: Google autocomplete (popular suggestions) and Keyword Planner (India, 12 months, 44 keywords). Page-1 snapshots for all 8 cities captured in the in-app browser. Summary in `SEO-STRATEGY.md` §17.
- Shipped: `/locations/kerala/{kochi,trivandrum,calicut,thrissur,malappuram,kannur,kollam,palakkad}/`, each with local sectors, search behaviour, localities, a dated page-1 snapshot, city FAQs, an entity "In short" answer and nested Service schema (City > District > State > Country with Wikipedia sameAs). Kerala hub links all eight; the home page and locations hub route to them; the locations hub has an ItemList. Kerala FAQs now answer the People-also-ask questions on cost and "best SEO expert", plus "SEO company vs independent expert" (the 1k–10k "seo company in kerala" intent). Redirects for old and alternate city URLs.
- Checked: 48 indexable pages; titles and descriptions unique and within length; one H1 each; canonicals correct; JSON-LD parses; no broken internal links; all pages in the sitemap. City-name test on the 8 city pages: 50–59% similar (SequenceMatcher), at most 33% 5-gram overlap; the shared part is navigation-style components. Rendered at 390 px and 1280 px in headless Chrome.
- Not done: deploy; LSIGraph (Cloudflare human check); case-study deck update.
- Next: owner confirms hometown in Kerala, languages (Malayalam?) and whether he ever meets Kerala clients in person — each would add real local substance. Then the South rollout (§17).

---

## 2026-11-27 — Mindtech playbook applied

- Extracted what produced the Mindtech results (page-1 for five terms, one AI Overview citation) from its repo docs and mapped each tactic to this site: `SEO-STRATEGY.md` §16.
- Shipped: home and five location pages retitled to "SEO expert in …" to match Google's autocomplete phrasing. No new pages; the doorway policy stands.
- Checked: build passes; 40 indexable pages; one H1 each; titles and descriptions unique; JSON-LD parses.
- Gap found: no third-party profiles yet. Mindtech's own lesson was to start these in week one. Ledger added to §16.
- Caveat: not deployed. Needs a Wrangler deploy.
- Next (owner): Search Console and Bing, LinkedIn, Clutch, GoodFirms, Justdial; answer the Chennai in-person question; confirm Mindtech permission.

---

## 2026-11-27 — Kerala competitor research

- Captured Google India results for five Kerala "seo expert in" queries in the in-app browser; read the leaders' sites with web fetch (the in-app browser refused them).
- Top 3 overall: Jijo Joseph, Nikhil Soman, Prasad Karthik. Per-city top 3 and the plan to outperform are in `SEO-STRATEGY.md` §15.
- Decision: the earlier idea of new Kochi, Calicut, Mumbai, Kolkata and Noida pages is dropped; it conflicts with the doorway policy (§3–4). Depth on the Kerala page comes first.
- Limits: one snapshot, no traffic or backlink data, schema unconfirmed.
- Next: owner confirms Mindtech case-study permission and any Kerala client evidence; then rebuild the Kerala page.

---

## 2026-11-27 — Audit, doorway/spam fixes, case study, conversion layer (release 2026-11-27.1)

### Research findings (deep research, 27 Nov 2026)

- Domain registered 26 Nov 2026 (Cloudflare Registrar). No pages indexed, no links, no reviews, no Google Business Profile.
- Risks found: a `mailto:`-only form and no analytics; 7 near-duplicate city pages; the "SEO Expert & Consultant | …" pattern on all 37 HTML files; at least six other "Sreejith" SEO professionals visible in search (entity collision); Google Business Profile requires in-person contact.
- Opportunity: Chennai and Kerala results are crowded with unverifiable "No.1" claims; few consultants show dated case studies; contractor-niche SEO terms have little competition.
- Possible billing issue: Cloudflare "payment failed" notices in the inbox — check so the domain cannot lapse.

### What changed

- **Doorway fix:** 7 city pages → 5 project-based pages (Bengaluru and Delhi NCR: client results; Hyderabad: in progress; Chennai: home base; Kerala: home state). Mumbai and Pune 301 → `/locations/`; Kochi 301 → `/locations/kerala/`.
  - Duplication between city pages after removing city names: **81–87% → 41–56%**; what remains is navigation and shared components.
- **Spam-pattern fix:** removed the forced title/H1/meta/intro pattern. All 42 HTML files now have unique titles and descriptions; the home page targets India, and the Chennai page owns Chennai.
- **Proof:** new `/case-studies/` hub and the Mindtech Solutions case study (Aug 2026 baseline → page-1 positions on 6 Nov 2026 → AI Overview citation on 25 Nov 2026), including what has not moved yet. Work history on About and the hub.
- **New pages:** AI search optimisation service; construction and MEP contractors industry page; "City pages without doorway risk" guide; free SEO review offer; thank-you page.
- **Conversion:** a Worker endpoint at `/api/enquiry` (Cloudflare Email Routing) with a `mailto:` fallback; enquiry references; consent-gated GA4 and Clarity hooks; header and sticky mobile "Free SEO review" buttons; a short, qualifying form.
- **Entity and schema:** one graph per page with ProfessionalService → founder Person "Sreejith CU"; ProfilePage on About; author bylines on every guide; Service and FAQPage only where content is visible.
- **Fixes:** the phone menu button was pushed off-screen by a CSS specificity bug (pre-existing); the SVG social image was replaced with a 1200 × 630 PNG; the privacy policy was rewritten for the DPDP Act; the terms were updated.

### Verified

- The generator runs. The sitemap lists 40 URLs, with no broken internal links, no duplicate titles or descriptions, and valid JSON-LD.
- Rendered in Chrome at 390, 700, 1024 and 1440 px with no horizontal overflow and no console errors.
- `npx wrangler deploy --dry-run` passes with Wrangler 4.168.0.

### Baseline

Indexed pages 0 · rankings none · referring domains 0 · reviews 0 · enquiries 0.

### Tracking

The tracker and the 12-slide case study deck were created for this project (links above).

### Next

**M1 — Measurement live, due 4 Dec 2026.** Owner actions are listed on the tracker's Actions sheet and in `DEPLOYMENT.md`.

---

## 2026-11-26 — Site built and domain registered

- `sreejithdigital.com` registered through Cloudflare Registrar; the static generator site deploys on Cloudflare Workers (PRs #1–#10).
- 36 indexable pages: 8 services, 4 industries, 7 location guides and 8 resources, with a site-wide "SEO Expert & Consultant | …" title pattern (removed on 27 Nov).
