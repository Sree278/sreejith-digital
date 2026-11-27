# SEO Growth Strategy — sreejithdigital.com (v2, 27 Nov 2026)

The single strategy document for this site. It replaces v1 (26 Nov 2026). Day-by-day changes are recorded in [`PROJECT-LOG.md`](PROJECT-LOG.md). The live measurement tracker is linked in the project log.

## 1. Positioning

**Who:** Sreejith CU, senior SEO consultant. Originally from Kerala, based in Chennai (south Chennai, GST Road), working with businesses across India.

**Promise:** SEO that produces enquiries, shown with **dated, verifiable results — including the misses** — instead of ranking promises.

**Proof engine:** the Mindtech Solutions case study (MEP contractor): from brand-only visibility (Aug 2026) to page 1 for five commercial terms (6 Nov 2026) and a national Google AI Overview citation (25 Nov 2026).

**Why this wins:** Chennai and Kerala SERPs are dominated by solo consultants with "No.1/Best" claims, self-answering FAQs and little verifiable proof (research, 27 Nov 2026). Few combine named, dated case studies, a clean person entity, honest AI-search advice and a working conversion path. That combination is the gap.

## 2. How to make Google "love" this site

Google rewards pages that are the most useful, trustworthy answer for a search. For a consultant site that means:

| Lever | What it means here | Status |
| --- | --- | --- |
| Helpful, people-first content | Every page answers a real buyer question; no page exists only to rank | Done for all 40 URLs; keep the rule for new pages |
| Experience (E-E-A-T) | First-hand work shown with dates, method and misses | Case study live; second case study by M5 |
| Clear entity | One person, one name, one description everywhere; Person + ProfessionalService schema | Schema live; LinkedIn and directories pending (owner) |
| Technical health | Crawlable static HTML, clean URLs, canonical host, fast pages | Done; verify CWV after launch |
| No spam patterns | No doorway city pages, no boilerplate keyword stuffing, no link schemes, no fake reviews | Fixed 27 Nov 2026 (section 3) |
| Earned trust signals | Reviews, directory profiles, mentions, links | Starts in M2 |
| Conversion + measurement | Working form, consent-based analytics, lead events | Built; needs owner configuration (M1) |

## 3. Doorway and spam fixes (27 Nov 2026)

| Problem | Evidence | Fix shipped |
| --- | --- | --- |
| Doorway city pages | 7 city pages shared one template; after removing city names they were **81–87% identical** | 5 project-based pages with unique local context, honest work status, city-specific FAQs → **41–56% similar**, and the overlap left is navigation and shared components |
| Cities with no substance | Mumbai, Pune: no clients, no local insight | 301 → `/locations/` |
| Thin Kochi page | One city, generic copy | Became one Kerala page (Kochi, Thiruvananthapuram, Kozhikode, Thrissur); 301 from `/locations/kochi/` |
| Boilerplate keyword stuffing | "SEO Expert & Consultant \| …" forced into every title, H1, meta, schema and first sentence — including Privacy and Terms | Removed. Every page has a unique, intent-matched title and a natural H1 |
| Home competing with city page | Home and Chennai page targeted the same intent | Home targets India; Chennai page owns Chennai |
| Unverifiable claims | — | Rule: every result has a date and method; misses are published |
| Self-serving review markup | — | None used; reviews will be quoted in HTML only |

**The city-name test (applies to this site and client sites):** swap the city name for another city. If the page is still true, it is a doorway page and does not go live. If the swap makes sentences false, it is a real city page.

## 4. Location policy — project-based targets

| Market | Page | Basis | Status label |
| --- | --- | --- | --- |
| Bengaluru | `/locations/bengaluru/` | Client #1, #3, #5, #8 (6 Nov 2026) | Client results |
| Delhi NCR | `/locations/delhi-ncr/` | Client #4 with one regional page | Client results |
| Hyderabad | `/locations/hyderabad/` | Active client page, not page 1 yet | In progress |
| Chennai | `/locations/chennai/` | Home base | Home base |
| Kerala | `/locations/kerala/` | Home state; NRI/visitor demand insight | Home state |
| Tamil Nadu | `/locations/tamil-nadu/` | Chennai home base in the same state; brief-supplied "SEO company" demand | Same state |

| Kerala cities (8) | `/locations/kerala/<city>/` — Kochi, Trivandrum, Calicut, Thrissur, Malappuram, Kannur, Kollam, Palakkad | Owner decision 27 Nov 2026; autocomplete demand gate | Home state — no local client result yet, said on each page |
| Tamil Nadu cities (3) | `/locations/tamil-nadu/<city>/` — Coimbatore, Madurai, Salem | Brief 27 Nov 2026; logged-out Google India page-1 snapshots, verified local facts and city-name gate | Same state — no local office, no local client result and no Tamil-language consulting claimed on each page |

**Changed 27 Nov 2026 (owner):** the proof gate is dropped, as it was for Mindtech on 15 Nov. What stays: the city-name test, honesty (no fake office, no borrowed results) and a **demand gate** — Google India autocomplete shows "seo expert in <city>" as a popular suggestion, or Keyword Planner shows 100+ searches a month. Towns get a page only on the same gate.

**Previously: add a new city only when** it has (1) real work or real local knowledge, (2) a local fact that is not the city name, (3) an honest line about where work was done, and (4) distinct demand in Search Console. Candidates: Coimbatore, Kochi (own page once Kerala has a Kochi client), Mumbai.

## 5. Site architecture

```text
/                                   National: "SEO expert in India" + proof + CTA
/about/                             Person entity home (ProfilePage → Person "Sreejith CU")
/case-studies/                      Work and results hub (+ work history)
  /case-studies/mindtech-solutions-mep-seo/
/services/  (9)                     seo-consulting, technical-seo, local-seo, ai-search-optimization,
                                    seo-services, content-strategy, analytics-reporting,
                                    google-ads-management, website-design
/industries/ (5)                    construction-mep-contractors (proven), b2b-saas,
                                    professional-services, ecommerce, local-multi-location
/locations/ (5)                     bengaluru, delhi-ncr, hyderabad, chennai, kerala
/resources/ (9)                     incl. location-pages-without-doorway-risk (new)
/free-seo-review/                   Lead magnet + form
/contact/                           General enquiry form (ContactPage)
/thank-you/                         noindex; conversion page (generate_lead)
/privacy/  /terms/
```

**Internal linking model**
- Home → case study, 6 services, 5 locations, 5 industries, 3 guides, free review.
- Every service page → answer block, evidence (case study), related services, free review.
- Every location page → status aside, case study, 3 services + 1 industry, the other 4 locations.
- Every guide → 3 related services, 3 related guides, author (About).
- No orphan pages; breadcrumbs everywhere; descriptive anchors only.

**Structured data:** one `@graph` per page — ProfessionalService (`/#business`, founder → Person), Person (`/about/#person`), WebSite, WebPage/ProfilePage/CollectionPage/ContactPage, BreadcrumbList, plus Service, FAQPage (visible FAQs only), TechArticle/Article where relevant. No self-serving Review/AggregateRating.

## 6. Keyword → URL map (data-backed, 27 Nov 2026)

Sources: Google Keyword Planner (India, Nov 2025–Oct 2026, ranges), Google and Bing autosuggest (en-IN), Google Trends (India, 12 months), Ahrefs free keyword generator (difficulty, volume band), AnswerThePublic and LSIGraph (free tiers). KD = Ahrefs difficulty band; "—" = not shown free.

| Page | Primary keyword (volume, KD) | Secondary keywords | Notes |
| --- | --- | --- | --- |
| `/` | seo expert in india (1k–10k) | seo services india (1k–10k) · seo consultant india (100–1k) · freelance seo expert india (10–100) | Bing en-IN ranks "seo expert in india" first; Trends +50% |
| `/locations/kerala/` | seo expert in kerala (1k–10k; ATP 1.9K; Easy) | seo company in kerala (1k–10k; Easy; +900% YoY) · best seo expert in kerala (100–1k; Medium) · freelance seo expert in kerala (100–1k) · seo services in kerala (100–1k) · best seo company in kerala (Easy) | Trends: Kerala has India's highest interest in "seo expert" (index 100), but it is down 50% year on year |
| `/locations/kerala/kochi/` | seo expert in kochi (100–1k; Easy) | seo services / company / agency in kochi (100–1k each) · seo expert in ernakulam (10–100) | |
| `/locations/kerala/calicut/` | seo expert in calicut (100–1k; +900% 3-month) | seo company in calicut (100–1k) · seo expert in kozhikode (—) | |
| `/locations/kerala/thrissur/` | seo expert in thrissur (100–1k; +900% 3-month) | — | Home town |
| `/locations/kerala/trivandrum/` | seo company in trivandrum (100–1k) | seo expert in trivandrum (10–100) | The "company" phrasing has more volume here |
| `/locations/kerala/{malappuram,kannur,palakkad}/` | seo expert in <city> (100–1k each) | — | |
| `/locations/kerala/kollam/` | seo expert in kollam (no Keyword Planner data; popular autosuggest) | — | Merge into the Kerala hub if it has no impressions after 90 days |
| `/locations/tamil-nadu/` | seo expert in tamil nadu / seo company in tamil nadu | seo services in tamil nadu · Chennai home-base link | State hub; links Chennai without moving its URL |
| `/locations/tamil-nadu/coimbatore/` | seo expert in coimbatore (brief-supplied Keyword Planner 100–1k, +900% 3-month) | seo company in coimbatore · seo services in coimbatore | Popular autosuggestions; textile, pump, IT park and hospital sectors |
| `/locations/tamil-nadu/madurai/` | seo company in madurai | seo services in madurai | Popular autosuggestion; §17 lists no Keyword Planner data for "seo expert in madurai" |
| `/locations/tamil-nadu/salem/` | seo company in salem / seo services in salem | seo expert in salem | Popular autosuggestions; steel, sago, handloom, mango and transport sectors |
| `/locations/chennai/` | seo expert in chennai (100–1k) | seo company in chennai (1k–10k) · seo services in chennai (100–1k; Easy) | Chennai tops Google autosuggest for both "seo services in" and "seo company in". Home base: a Google Business Profile is possible here |
| `/locations/bengaluru/` | seo expert in bangalore (100–1k; top bid ₹292) | seo company in bangalore (1k–10k) | |
| `/locations/hyderabad/` | seo expert in hyderabad (100–1k) | seo company in hyderabad (1k–10k) | Not in Google autosuggest |
| `/locations/delhi-ncr/` | seo expert in delhi (1k–10k; Trends +70%) | seo expert in noida / gurgaon (100–1k each) | |
| `/services/ai-search-optimization/` | ai seo expert (100–1k; Trends rising +60%) | ai seo expert in kerala (<100) | |
| `/resources/seo-cost-india/` | how much does seo cost in india (popular autosuggest) | seo cost for small business per month | PAA "How much does it cost to hire an SEO expert?" on every Kerala SERP |
| `/industries/ecommerce/` | ecommerce seo expert in kerala (<100) | — | LSIGraph AI prompt |
| `/industries/construction-mep-contractors/` | seo for mep contractors (L) | hvac contractor seo | Proof-backed quick win |

**Not targeted:** training intent ("seo expert course", "kaise bane", salary, interview questions — YouTube autosuggest) and "top 10 / no 1 seo expert" lists (self-ranking).

**Authority gap (Ahrefs free backlink checker, 27 Nov 2026):** nikhilsoman.in DR 55, 835 linking sites · jijojosephseo.in DR 32, 588 · digitalcommunicator.in DR 18, 285 · sreeharisk.in DR 0, 3 linking sites — yet it ranks #2 for "seo expert in kochi", with a Kochi Google Business Profile and 14 reviews · sreejithdigital.com DR 0, 0. Links aren't the only lever at this level; relevance, local proof and profiles carry the low-DR winners.

**South rollout shipped 27 Nov 2026:** Tamil Nadu hub plus Coimbatore, Madurai and Salem are live in the generator. The hub keeps Chennai at `/locations/chennai/`; each city has four verified sectors, two search-behaviour paragraphs, ten localities, five FAQs and three dated logged-out Google India page-1 observations. Trichy, Tirunelveli, Nagercoil, Mysuru, Mangaluru, Vizag and Vijayawada remain gated on demand and distinct local substance.

## 7. Conversion strategy

1. **One primary offer everywhere:** "Get a free SEO review" (header button, hero, every CTA band, sticky button on phones). Secondary: "See the case study".
2. **Proof before the ask:** dated rankings card in the home hero; evidence blocks on service, industry and location pages.
3. **Short, qualifying form:** name, business email, website, service, monthly budget band, message (optional on the review form), DPDP consent. Honeypot + timing check against bots.
4. **Form never loses a lead:** posts to the Worker (`/api/enquiry` → email via Cloudflare Email Routing). If that is not configured or fails, it opens the visitor's email app with the enquiry and a reference pre-filled.
5. **Thank-you page with reference** (`/thank-you/?ref=SD-…`), noindex, fires `generate_lead` once per enquiry (only with analytics consent).
6. **Trust:** no guarantees, misses published, reply-time expectation ("usually within one business day"), privacy policy written for DPDP.
7. **Privacy preference respected:** no personal phone number. Optional later: a WhatsApp Business link on a separate business number.
8. **Events to track:** `form_start`, `generate_lead` (key event), outbound case-study clicks (optional).

## 8. Entity, E-E-A-T and off-page plan

**Entity (M1–M2)**
- Same name, photo, headline and one-line bio on the site, LinkedIn, Clutch, GoodFirms and author bios: "Sreejith CU — SEO consultant, Chennai".
- Add verified profile URLs to `OWNER_PROFILES` (feeds `sameAs`), a headshot to `OWNER_PHOTO`, and confirmed roles to `EXPERIENCE` in `scripts/generate_site.py`.
- Google Business Profile **only if** you meet Chennai clients in person (Google requires in-person contact). Then: service-area business, address hidden, business-only number, service areas within the Chennai region. If remote-only, skip it.

**Links and mentions that work for a solo consultant (M2 onward)**
- Directories with reviews: Clutch, GoodFirms, DesignRush (free), Sulekha, Justdial, LinkedIn company page.
- Journalist requests: Featured (free tier), Qwoted (free tier), #JournoRequest — 3 pitches a week.
- Client credit links with permission (brand anchor, e.g. the existing "Site by Sreejith CU" footer credit on mindtechsolutions.co.in).
- Original data asset (M4): e.g. "Core Web Vitals and schema on 50 Chennai SMB websites".
- Talks and posts with Chennai and Kerala business and startup communities; contractor trade media.

**Never:** PBNs, paid guest-post packages, link exchanges, expired-domain redirects, AI-spun guest posts, self-ranking "Top 10 SEO experts" lists, incentivised reviews.

## 9. AEO / GEO (AI search) plan

- Google's guidance (May 2026): optimising for AI features is still SEO; no special files or markup needed. Effort goes to entity clarity, answer-first content and third-party corroboration.
- Answer blocks (40–60 words) open every service page; FAQs are visible and marked up.
- Crawl access: allow Googlebot, Bingbot, OAI-SearchBot, PerplexityBot; check Cloudflare AI Crawl Control (owner, M1).
- Get into the sources AI cites: third-party listicles, directories, review profiles.
- Baseline and monthly re-run of 15 fixed prompts in ChatGPT, Perplexity, Gemini, Copilot and Google AI Mode (logged in the tracker).
- llms.txt: optional, no measurable effect in current evidence.

## 10. Milestones and timeline

Targets are estimates for a domain registered on 26 Nov 2026, not guarantees.

| # | Milestone | Due | Exit criteria |
| --- | --- | --- | --- |
| M0 | Foundation fixed | 27 Nov 2026 | This release merged and deployed; `/version.txt` shows `2026-11-27.1` |
| M1 | Measurement live | 4 Dec 2026 | GSC Domain property + sitemap; Bing WMT; Email Routing + form endpoint delivering a test enquiry; GA4 + Clarity IDs live behind consent; AI crawler settings checked; www → apex redirect |
| M2 | Indexed + entity | 26 Dec 2026 | ≥ 90% of 40 URLs indexed; #1 for "sreejith digital"; LinkedIn aligned + `sameAs`; 4 directory profiles; case-study permission confirmed; AI-prompt baseline logged |
| M3 | First traction | 25 Jan 2027 | ≥ 200 non-brand impressions/month; first top-20 positions on industry/long-tail terms; 2 new guides; 3 reviews; first qualified enquiries |
| M4 | Authority start | 26 Feb 2027 | ≥ 10 relevant referring domains; ≥ 5 reviews; first page-1 niche term; Chennai and Kerala pages top 30; Google Ads test decision |
| M5 | Competitive | 27 May 2027 | Chennai page top 10 for a primary term (stretch); second case study; ≥ 1 AI mention in the 15-prompt set; ≥ 20 referring domains |
| M6 | Category position | 27 Nov 2027 | Top 5 for a primary Chennai or Kerala term (stretch); 3 case studies; steady flow of qualified enquiries each month |

## 11. Measurement (free tools only)

| KPI | Source | Cadence |
| --- | --- | --- |
| Indexed pages, exclusion reasons | GSC Pages report, Bing WMT | Weekly to M2, then monthly |
| Brand position and impressions | GSC (query contains "sreejith") | Monthly |
| Non-brand impressions, clicks, average position | GSC (brand filtered out) | Monthly |
| 20 tracked keywords | Manual Google India check (logged-out) + GSC | Monthly, same day |
| Qualified enquiries | GA4 `generate_lead` + inbox, qualified by hand | Monthly |
| Enquiry conversion rate | GA4 (leads ÷ sessions) | Monthly |
| AI mention rate + AI referrals | 15-prompt log; GA4 sources chatgpt.com, perplexity.ai, gemini.google.com, copilot.microsoft.com | Monthly |
| Referring domains | Ahrefs Webmaster Tools, GSC Links | Monthly |
| Reviews | Clutch, GoodFirms, LinkedIn, GBP (if eligible) | Monthly |
| Core Web Vitals, UX friction | PageSpeed Insights, Clarity | Monthly |

**Monthly routine (first working day):** export GSC queries → update tracker → run the 20-keyword check and 15 AI prompts → note what moved and why → one decision for the month → log it in `PROJECT-LOG.md`.

## 12. Content plan (next 90 days)

| When | Piece | Target URL / cluster |
| --- | --- | --- |
| Dec 2026 | How long SEO takes for a new website in India (with this site's own timeline) | Resources → AEO questions |
| Dec 2026 | SEO consultant vs agency in India | Resources → national consultant |
| Jan 2027 | SEO for MEP and HVAC contractors: service × city pages that rank | Industry cluster |
| Jan 2027 | Does llms.txt work? What the evidence says | AI search cluster |
| Feb 2027 | Original data: Core Web Vitals + schema on 50 Chennai SMB sites | Link-earning asset |
| Feb 2027 | `/pricing/` with "from" prices (once set) | Pricing cluster |

## 13. Owner inputs needed

- [ ] Confirm public name **"Sreejith CU"** (add a surname if preferred)
- [ ] LinkedIn and other profile URLs → `OWNER_PROFILES`
- [ ] Headshot → `OWNER_PHOTO`
- [ ] Work history (employers, roles, years) → `EXPERIENCE`
- [x] Languages you consult in → `OWNER_LANGUAGES` (English, Malayalam — 27 Nov 2026)
- [x] Home town: Thrissur; based in Chennai; meets Kerala clients in person when travelling (27 Nov 2026)
- [ ] Client permission to publish the Mindtech case study with name and rankings
- [ ] Keep the free review offer and the "usually within one business day" reply promise?
- [ ] Do you meet Chennai clients in person? (decides Google Business Profile eligibility)
- [ ] "From" prices for a `/pricing/` page
- [ ] GA4 and Clarity IDs; Email Routing + Worker binding (see `DEPLOYMENT.md`)
- [ ] Decide DotMiracle's role (recommended: websites/maintenance studio, not a second SEO-consulting site)

## 14. Guardrails

- No ranking guarantees; no invented clients, numbers, reviews or offices.
- No city page that fails the city-name test.
- No boilerplate keyword patterns in titles or headings.
- No analytics before consent; update the privacy policy before adding any new processor.
- One canonical host: `https://sreejithdigital.com` (no `www`, no hyphen).
- Never publish the same guide on sreejithdigital.com and DotMiracle.

## 15. Kerala competitor analysis (27 Nov 2026)

**Method:** Google India results for "seo expert in" + kerala, kochi, calicut, trivandrum, thrissur, captured in the in-app browser (logged out, results localised to each city by Google). Competitor sites were then read with the web-fetch tool, because the in-app browser refused them. Schema could not be confirmed from page text. One snapshot; no traffic or backlink data (free tools only).

**Top 3 overall (page 1 or AI Overview in most Kerala-city queries)**

| # | Competitor | Appears for | Why it leads | Weakness to exploit |
| --- | --- | --- | --- | --- |
| 1 | Jijo Joseph — jijojosephseo.in | Kerala, Kochi, Calicut, Trivandrum | Exact-match title/H1 "SEO Expert in Kerala"; ~20 city pages (Kerala districts, 6 metros, UAE, London, Sydney); 8 named case studies; 14+ yrs, 12,000+ students, YouTube/Malayalam audience; GTM, entity map page | Same template across cities; inconsistent stats; unverified "No.1"; no prices |
| 2 | Nikhil Soman — nikhilsoman.in | Kochi (AI Overview), Kerala, Calicut, Trivandrum | One ~2,000-word page per city; published prices ₹10k/13k/18k; local FAQs; GBP/Maps + AI-search angle; web-dev pages feed internal links | UAE case study on the Calicut page; testimonials not local; plan names inconsistent |
| 3 | Prasad Karthik — digitalcommunicator.in | Kerala, Trivandrum | Prices ₹15k/30k/50k; metric-led case studies; journalism story | No city pages; duplicated sections, typos; anonymised proof |

Runners-up: Sreehari SK (Kochi, Kerala), Dilshad Mirsha (Kerala, Calicut), Sanoop Balan (Kochi).

**Top 3 per Kerala location (organic order on the day; local pack in brackets)**

| Location | 1 | 2 | 3 |
| --- | --- | --- | --- |
| Kerala | Jijo Joseph | Amitha Mohan (Kottayam) | Prasad Karthik |
| Kochi | Jijo Joseph | Sreehari SK | Sanoop Balan (pack: Digital Nishad, SEO Engineer) |
| Calicut | Junaid KK | Jijo Joseph | Nikhil Soman (pack: Kiran Johnson) |
| Trivandrum | Abhishek SK | Nikhil Soman | Krishnapriya R R |
| Thrissur | Nishad Ismail | Antony Benny | Nexxa Corporates (agency) |

**Other locations the leaders target (from their sitemaps/pages, not verified rankings):** Jijo — India, Chennai, Mumbai, Bangalore, Delhi, Hyderabad, Kasaragod, Kannur, Kottayam, Malappuram, Palakkad, Kollam, UAE, Dubai, Abu Dhabi, London, Sydney. Nikhil — Kerala, Kochi, Trivandrum, Kannur, Bangalore, India, UAE. Prasad — Kerala, Trivandrum, India, UAE.

**Common patterns:** `/seo-expert-in-[city]/` flat URLs; personal-name domains; exact-match title + H1; pricing on city pages (two of three); WhatsApp + free-audit CTA; AEO/GEO as the 2026 differentiator; Gulf/UAE as the second market; Malayalam content (Jijo). Shared gaps: no confirmed JSON-LD, duplicated copy, unverifiable superlatives, case studies that are not local, neighbourhoods named but not linked.

**How we outperform (consistent with sections 3–4)**
1. Do not copy the 20-city spray. It fails our city-name test. Go deep on `/locations/kerala/` and add a Kochi page only once a Kochi client or real local evidence exists.
2. Proof they lack: named, dated Mindtech case study with method; publish misses as well as wins; no superlatives.
3. Publish price ranges between Nikhil's and Prasad's bands.
4. Ship Person, ProfessionalService and FAQPage JSON-LD (none confirmed on any competitor).
5. Add Malayalam FAQs and an AEO/GEO section; interlink Kerala neighbourhoods to real sections.
6. Realistic: Kerala local-pack positions (80+ reviews) are out of reach for a Chennai-based new domain. Aim for organic and AI-answer visibility first; Thrissur and long-tail "SEO for [industry] in Kerala" are the softest targets.
7. Track "seo expert in kerala/kochi/calicut/trivandrum/thrissur" weekly in Search Console from M1.

## 16. Mindtech playbook applied to this site (27 Nov 2026)

Source: Mindtech repo docs (`LOCAL-SEO-PLAN`, `PAGE-MAP-SEO`, `COMPETITOR-TEARDOWN`, `GEO-AI-OVERVIEW…`, `ONPAGE-SEO-RECOVERY`, `SEO-INDEXATION-AUDIT`) and the published case study. Results there: five page-1 terms in about three months from a brand-only baseline (#1 retail fit-out Bengaluru, #3 MEP Bengaluru, #4 MEP Delhi NCR, #5 fire Bengaluru, #8 HVAC Bengaluru, 6 Nov 2026) and an AI Overview citation for "MEP contractors in India" (25 Nov 2026).

| # | Mindtech tactic | Status here |
| --- | --- | --- |
| 1 | Record indexation and keyword baseline before changing anything | Baseline in tracker; Search Console not yet connected — **owner, M1** |
| 2 | Titles, descriptions and H1s aligned to buyer phrasing | **Done today:** home and five location pages now use "SEO expert in …" (the phrase Google autocomplete shows) |
| 3 | One page per intent; home claims India, each city claims its city | Done |
| 4 | City-name test; thin pages merged or redirected | Done (§3); no new city pages |
| 5 | Proof beside the claim, mirrored in structured data | Mindtech case study linked from every page; Article, Service, FAQPage JSON-LD live |
| 6 | Visible FAQs with matching FAQPage markup (the AI Overview text mirrored FAQ and schema wording) | Done on home, services, locations |
| 7 | Consent-based GA4 and Clarity, reference on every enquiry | Built; needs IDs — **owner, M1** |
| 8 | Publish misses, dated results | Done |
| 9 | Third-party corroboration started in week one (Mindtech's stated regret) | **Ledger below — none submitted yet** |
| 10 | Google Business Profile facts gathered in week one | Waiting on one answer: do you meet Chennai clients in person? |
| 11 | Reviewed releases with checks and rollback | Generator build plus checks; deploy via Wrangler |

**Differences that matter.** Mindtech's SERPs were thinner (keyword-stuffed single pages) and it brought a decade of real projects, ISO certification and 100+ store references. "SEO expert in Kerala" has established freelancers with years of content, reviews and student audiences (see §15). The tactics transfer; the speed may not. Judge progress against dated Search Console data, not against Mindtech's three months.

**Off-page ledger (free listings; all owner actions — accounts need your login)**

| Platform | Why | Status | Date |
| --- | --- | --- | --- |
| LinkedIn profile + company page | Feeds `sameAs`; AI sources cite it | Not started | — |
| Clutch | Review profile for agencies and consultants | Not started | — |
| GoodFirms | Same | Not started | — |
| DesignRush | Free listing | Not started | — |
| Sulekha, Justdial | Indian local directories (NAP consistency) | Not started | — |
| Kompass India | Mindtech's AI Overview cited it as a source | Not started | — |
| Bing Webmaster Tools + Google Search Console | Indexing; feeds ChatGPT search | Not started | — |

After each profile goes live: record the URL and date here, match name, role and one-line bio exactly, then add the URL to `OWNER_PROFILES`.


## 17. Location hierarchy and keyword data (27 Nov 2026)

**Hierarchy:** India (home page) → Locations hub (ItemList of every location page) → state/region (Kerala, Tamil Nadu, Delhi NCR) or metro (Chennai, Bengaluru, Hyderabad) → city (`/locations/kerala/<city>/` or `/locations/tamil-nadu/<city>/`) → town only on demand. Breadcrumbs and `BreadcrumbList` follow the same path; `Service.areaServed` nests City → District → State → Country with Wikipedia `sameAs` for disambiguation. The Tamil Nadu hub now has three city pages; Karnataka still waits for two qualifying city pages.

**Keyword Planner (India, Nov 2025–Oct 2026, ranges — no active ad spend; plan saved as a draft in the DotMiracle Ads account)**

| Band | Keywords |
| --- | --- |
| 1k–10k | seo expert in kerala · seo expert in india · seo expert in delhi · seo company in kerala (+900% YoY) · seo services india · seo company in chennai / bangalore / hyderabad · digital marketing agency in kochi |
| 100–1k | seo expert in kochi, calicut (+900% 3-month), thrissur (+900%), malappuram, kannur, palakkad (+900%), chennai, bangalore, hyderabad, mumbai, kolkata, noida, gurgaon, chandigarh, coimbatore · best / freelance seo expert in kerala · seo services in kerala, kochi, chennai · seo company in kochi, calicut, trivandrum · seo agency in kochi · seo consultant india · ai seo expert |
| 10–100 | seo expert in trivandrum, ernakulam · seo consultant in kerala · freelance seo expert india |
| No data | seo expert in kollam, kottayam, kozhikode, thiruvananthapuram, madurai |

Top-of-page bids (high range) show commercial value: Bengaluru ₹292, Mumbai ₹340, Kerala ₹162, Kochi ₹142.

**Autocomplete (popular suggestions):** Kerala — kerala, kochi, calicut, thrissur, trivandrum, kannur, kollam, malappuram, palakkad. South — chennai, bangalore (coimbatore, madurai, trichy, vizag, vijayawada only as minor suggestions). North — delhi, noida, gurgaon, mumbai, kolkata, chandigarh, mohali, varanasi. "seo expert in hyderabad" was not suggested, but Keyword Planner shows 100–1k.

**People also ask, on every Kerala results page:** "How much does it cost to hire an SEO expert?" and "Who is the best SEO expert in Kerala?" Both are now answered on the Kerala page without self-ranking.

**Tools:** Google Keyword Planner, Google autocomplete, Google results pages (in-app browser), LSIGraph and AnswerThePublic (free tiers, via Chrome), Search Console and Bing once connected.

**AnswerThePublic (free report, 27 Nov 2026):** "seo expert in kerala", 1.9K searches a month, CPC US$2.14. Top ideas: freelance / best / top / top 10 / best freelance SEO expert in Kerala. The rest is behind the free daily limit.

**LSIGraph target prompts (what people ask AI):** best SEO expert in Kerala for small businesses · which Kerala SEO expert can improve local Google rankings · what to look for when hiring an SEO expert in Kerala · how much an SEO expert in Kerala charges · which SEO consultant in Kerala is best for ecommerce. All five are now answered in the Kerala page FAQs. Its free brand check (ChatGPT, Gemini, AI Mode, AI Overviews) should be run for "Sreejith Digital" once the site is live and indexed, as an AI-visibility baseline.

**Rollout order (each page must pass the city-name and demand gates)**
1. Done: Kerala hub + 8 cities; home and metros retitled "SEO expert in …".
2. Done: Tamil Nadu hub + Coimbatore, Madurai and Salem on 27 Nov 2026. Trichy, Mysuru, Mangaluru, Vizag and Vijayawada remain gated on demand and distinct local substance.
3. Then North: split Noida and Gurugram out of Delhi NCR only with distinct content; Mumbai, Kolkata, Chandigarh.
4. Measure: Search Console impressions per city page each week from M1; a page with no impressions after 90 days is merged back into its hub.

**Honest limits:** No page can be made "competition-proof". The moat is what competitors lack and can't copy quickly: named, dated proof, consistent entity data, real local substance per city, and third-party profiles (ledger in §16). FAQ rich results are shown only for government and health sites, so FAQPage markup here serves AI parsing, not SERP stars. Breadcrumbs remain eligible for rich results. Review stars are not used, because self-served reviews are ineligible and none exist yet. llms.txt is skipped, consistent with the AI-search service page (no measured effect).
