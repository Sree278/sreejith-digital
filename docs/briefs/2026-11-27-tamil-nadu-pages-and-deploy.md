# Task brief — Tamil Nadu location pages, then deploy

**Issued:** 27 Nov 2026 by Claude (instructor) for Arena agents (implementers).
**Owner approval:** Sreejith CU approved this work *and* deployment on 27 Nov 2026.
**Repo:** `Sree278/sreejith-digital`

## 0. Before you start

1. Base branch: `seo/2026-11-27-doorway-fix-case-study-conversion` (PR #11, head `797b05d` or later). Do **not** start from `main` — PR #11 holds the Kerala hierarchy this task extends.
2. Read first: `SEO-STRATEGY.md` §3, §4, §6 and §17, and the top five entries of `PROJECT-LOG.md`.
3. The site is generated: edit `scripts/generate_site.py` only, then run `python3 scripts/generate_site.py`. Never hand-edit `public/**/index.html`. `public/_redirects` is hand-maintained.
4. One implementer, one branch: `arena/tamil-nadu-pages` off the base branch.

## 1. What to build

A Tamil Nadu hub plus three city pages, mirroring the Kerala implementation (`KERALA_CITIES`, `city_place()`, `kerala_city_page()`, `kerala_city_cards()`).

| URL | Page | Primary keyword | Evidence |
| --- | --- | --- | --- |
| `/locations/tamil-nadu/` | State hub | seo expert in tamil nadu / seo company in tamil nadu | Hub for the cities below; links Chennai |
| `/locations/tamil-nadu/coimbatore/` | City | seo expert in coimbatore (Keyword Planner 100–1k, +900% 3-month) | "seo company / services in coimbatore" are popular Google autosuggestions |
| `/locations/tamil-nadu/madurai/` | City | seo company in madurai | popular Google autosuggestion |
| `/locations/tamil-nadu/salem/` | City | seo company in salem / seo services in salem | popular Google autosuggestions |

**Chennai stays at `/locations/chennai/`.** Do not move it. The Tamil Nadu hub links to it as the home-base city, and its schema already sits inside Tamil Nadu.

**Engineering:** generalise rather than copy. Turn `KERALA_CITIES` into a per-state structure (for example `STATE_CITIES = {"kerala": [...], "tamil-nadu": [...]}`), and make the renderer `state_city_page(state_slug, city)` and the cards `state_city_cards(...)`. Then:

- Add a `"tamil-nadu"` entry to `LOCATIONS` (hub) using the same fields as `"kerala"`.
- Kerala output must not change. After building, diff `public/locations/kerala/**` against the base branch: only shared-component changes are acceptable.

## 2. Content rules (non-negotiable)

- **City-name test:** if swapping the city name leaves the page true, it is a doorway page and must not ship. Each city needs 4 sectors, 2 search-behaviour paragraphs, 10 localities and 4–5 FAQs, all specific to that city.
- **Facts must be verified** with a web search before use, and kept stable and checkable (industries, institutions, landmarks). Starting points to verify, not assume:
  - **Coimbatore:** textile mills, pumps and motors, foundries, nearby Tiruppur knitwear, IT parks, hospitals.
  - **Madurai:** Meenakshi temple tourism, textiles, Aravind Eye Hospital, education.
  - **Salem:** steel plant, sago, handloom and textiles, magnesite, mangoes, transport.
- **Page-1 snapshot:** run logged-out Google India searches for "seo expert in <city>" and "seo company in <city>" and record three dated observations, as the Kerala pages do. If you cannot run a real search, **omit the snapshot section for that city**. Never invent one.
- **Honesty about the owner:**
  - Based in Chennai, same state; can meet in person when travelling.
  - Consults in English and Malayalam. **Do not claim Tamil** — it is not confirmed.
  - No local client result in these cities: say so, as the Kerala pages do.
  - No fake office or address. No "best" or "No. 1" claims.
- **"SEO company" intent** dominates Tamil Nadu suggestions. Every city page gets one company-vs-dedicated-expert FAQ in wording unique to that city.
- Titles ≤ 62 characters; descriptions 70–160, unique site-wide; one H1 per page.

## 3. Schema and linking

- `Service.areaServed`: City → district (`AdministrativeArea`) → `STATE_PLACES["Tamil Nadu"]` → India, with Wikipedia `sameAs` for city and district.
- `FAQPage` for each city's FAQs, plus breadcrumbs: Home › Locations › Tamil Nadu › City.
- Add the new cities to `business_node()` `areaServed` and to `locations_item_list()`.
- On the home page "Where I work" section, add a Tamil Nadu city line like the Kerala one. On `/locations/`, add a Tamil Nadu section.
- Add to `public/_redirects`:
  - `/locations/coimbatore/` → `/locations/tamil-nadu/coimbatore/` (same for madurai and salem)
  - `/seo-expert-in-coimbatore/` → `/locations/tamil-nadu/coimbatore/`
  - `/locations/tamilnadu/` → `/locations/tamil-nadu/`

## 4. Verification (all must pass, with output pasted in the PR)

1. `python3 scripts/generate_site.py` runs cleanly.
2. Audit every `public/**/index.html`:
   - titles and descriptions unique and within length;
   - exactly one H1;
   - self-referencing canonical on indexable pages;
   - all JSON-LD parses;
   - every internal `href` resolves to a generated page or a `_redirects` source;
   - every indexable page is in `sitemap.xml`.
3. City-name similarity test across the three new city pages. Use the method in `PROJECT-LOG.md` (27 Nov): `<main>` text, every city name and alias replaced with a placeholder, `difflib.SequenceMatcher` on word lists. Maximum must be **≤ 60%**.
4. Render `/locations/tamil-nadu/coimbatore/` at 390 px and 1280 px in headless Chrome. No horizontal overflow, and the breadcrumb shows four levels.

## 5. Logging

- `SEO-STRATEGY.md`:
  - §4 table: add the Tamil Nadu rows.
  - §6 keyword map: add rows for the new pages.
  - §17: mark "Next, South: Coimbatore…" as done.
- `PROJECT-LOG.md`: a newest-first entry covering what changed, why, the evidence (with the check output) and what comes next.

## 6. Deploy (owner-approved)

Deployment is Cloudflare Workers Builds: a merge to `main` deploys automatically (see `DEPLOYMENT.md`).

1. Open a PR from `arena/tamil-nadu-pages` into `seo/2026-11-27-doorway-fix-case-study-conversion`, and merge it once section 4 passes.
2. Merge PR #11 (`seo/2026-11-27-doorway-fix-case-study-conversion` → `main`) using a merge commit, not a squash.
3. After Workers Builds finishes, check production:
   - `https://sreejithdigital.com/version.txt` shows the new release;
   - `/sitemap.xml` URL count matches the build;
   - `/locations/tamil-nadu/coimbatore/` and `/locations/kerala/thrissur/` return 200;
   - `/locations/kochi/` returns a 301 to `/locations/kerala/kochi/`.
4. If a production check fails, **stop and report**. Do not hot-fix on `main`.
5. Report back:
   - PR links;
   - the merge commit SHA;
   - output of the checks above;
   - anything you skipped and why.

## 7. Do not

- Touch Kerala page content beyond shared-component changes.
- Add city or town pages not listed here.
- Add analytics IDs, secrets or `wrangler.toml` changes.
- Force-push.
- Claim Tamil, a local office, or local client results.
