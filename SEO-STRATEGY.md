# SEO Growth Strategy — sreejithdigital.com (v2, 27 Nov 2026)

The single strategy document for this site. It replaces v1 (26 Nov 2026). Day-by-day changes are recorded in [`PROJECT-LOG.md`](PROJECT-LOG.md). The live measurement tracker is linked in the project log.

## 1. Positioning

**Who:** Sreejith CU, independent SEO consultant. Originally from Kerala, based in Chennai (south Chennai, GST Road), working with businesses across India.

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

**Add a new city only when** it has (1) real work or real local knowledge, (2) a local fact that is not the city name, (3) an honest line about where work was done, and (4) distinct demand in Search Console. Candidates: Coimbatore, Kochi (own page once Kerala has a Kochi client), Mumbai.

## 5. Site architecture

```text
/                                   National: "Independent SEO consultant in India" + proof + CTA
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

## 6. Keyword → URL map

Demand tiers are estimates (H/M/L); confirm in Google Keyword Planner and Search Console.

| Cluster | Example queries | Intent | Demand | Target URL | Priority |
| --- | --- | --- | --- | --- | --- |
| Brand / person | sreejith digital, sreejith cu seo | Navigational | L | `/`, `/about/` | Quick win |
| Industry: contractors | seo for mep contractors, hvac contractor seo, seo for construction companies india | Commercial | L | `/industries/construction-mep-contractors/` | **Best quick win** |
| Proof | seo case study india, mep company seo case study | Investigation | L | `/case-studies/…` | Quick win |
| Technical | technical seo consultant india, seo audit services india | Commercial | L–M | `/services/technical-seo/` | Quick win |
| AI search | ai seo services india, geo / aeo consultant, ai overviews optimization | Commercial | L–M, rising | `/services/ai-search-optimization/` | Medium |
| Chennai | seo consultant chennai, seo expert in chennai, freelance seo expert chennai | Commercial/local | M | `/locations/chennai/` | Long-term core |
| South Chennai | seo consultant tambaram, seo services gst road | Local | L | Chennai page section | Quick win |
| Kerala | seo expert kerala, seo expert kochi / trivandrum / calicut | Commercial/local | M | `/locations/kerala/` | Medium |
| Bengaluru | seo consultant bangalore / bengaluru | Commercial | M | `/locations/bengaluru/` | Medium |
| Hyderabad | seo consultant hyderabad | Commercial | M | `/locations/hyderabad/` | Medium |
| Delhi NCR | seo consultant delhi ncr / gurgaon / noida | Commercial | M–H | `/locations/delhi-ncr/` | Medium |
| National | seo consultant india, hire seo expert india | Commercial | M–H | `/` | Long-term |
| Pricing | seo cost in india, seo packages india | Investigation | M | `/resources/seo-cost-india/` (+ `/pricing/` once prices are set) | High |
| City pages (how-to) | location pages seo, service area pages | Informational | L | `/resources/location-pages-without-doorway-risk/` | Supporting |

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
- Same name, photo, headline and one-line bio on the site, LinkedIn, Clutch, GoodFirms and author bios: "Sreejith CU — independent SEO consultant, Chennai".
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
- Get into the sources AI cites: independent listicles, directories, review profiles.
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
| Dec 2026 | Freelance SEO consultant vs agency in India | Resources → national consultant |
| Jan 2027 | SEO for MEP and HVAC contractors: service × city pages that rank | Industry cluster |
| Jan 2027 | Does llms.txt work? What the evidence says | AI search cluster |
| Feb 2027 | Original data: Core Web Vitals + schema on 50 Chennai SMB sites | Link-earning asset |
| Feb 2027 | `/pricing/` with "from" prices (once set) | Pricing cluster |

## 13. Owner inputs needed

- [ ] Confirm public name **"Sreejith CU"** (add a surname if preferred)
- [ ] LinkedIn and other profile URLs → `OWNER_PROFILES`
- [ ] Headshot → `OWNER_PHOTO`
- [ ] Work history (employers, roles, years) → `EXPERIENCE`
- [ ] Languages you consult in → `OWNER_LANGUAGES`
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
