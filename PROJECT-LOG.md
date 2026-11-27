# Project log — sreejithdigital.com

Newest first. Each entry records what changed, why, the evidence, and what comes next.

| Resource | Where |
| --- | --- |
| Strategy, milestones, KPIs | [`SEO-STRATEGY.md`](SEO-STRATEGY.md) |
| Live tracker (milestones, actions, KPIs, 20 keywords) | https://claude.ai/artifact/Vf1ESoPRJQ3FEnYbBuLxpG |
| Deployment and owner checklist | [`DEPLOYMENT.md`](DEPLOYMENT.md) |

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

### Next

**M1 — Measurement live, due 4 Dec 2026.** Owner actions are listed on the tracker's Actions sheet and in `DEPLOYMENT.md`.

---

## 2026-11-26 — Site built and domain registered

- `sreejithdigital.com` registered through Cloudflare Registrar; the static generator site deploys on Cloudflare Workers (PRs #1–#10).
- 36 indexable pages: 8 services, 4 industries, 7 location guides and 8 resources, with a site-wide "SEO Expert & Consultant | …" title pattern (removed on 27 Nov).
