# Sreejith Digital — static website

A deployment-ready static website for **https://sreejithdigital.com** — no hyphen. `sreejith-digital` is the Cloudflare Worker name used for the temporary `*.workers.dev` URL; it is not the registered domain. The deployable files live in [`public/`](public/), with a root-level [`wrangler.toml`](wrangler.toml) so the same repository works with:

- **Cloudflare Workers Builds / static assets** using `npx wrangler deploy`
- **Cloudflare Pages** with `public` as the build output directory
- **GitHub Pages** using the committed `public/CNAME` and `public/.nojekyll`

There are no runtime dependencies. `wrangler` is pinned as a development dependency so Cloudflare does not fetch an arbitrary new version on every deployment.

The site implements the recommended consultant-site architecture from the brief:

- `Home`, `About`, `Services`, `Work` (case studies), `Industries`, `Locations`, `Resources`, `Contact`
- Dropdown-ready navigation for services, industries, locations, and resources
- 40 indexable pages with clean directory URLs, unique titles and descriptions, breadcrumbs, and one structured-data graph per page
- Nine services, five industries, five project-based location pages, nine guides, a case study and a free SEO review offer
- Dark visual system with green accents, responsive navigation, accessible focus states, and reduced-motion support
- `robots.txt`, `sitemap.xml`, `_headers`, `_redirects`, `CNAME`, `.nojekyll`, and a custom `404.html`

## Quick preview

Use a server rather than opening an HTML file directly, because the site uses root-relative URLs:

```bash
python3 -m http.server 8000 --bind 0.0.0.0 --directory public
```

Then open `http://localhost:8000/` locally, or use the live preview exposed by the workspace.

Optionally, after `npm install`, `npm run dev` starts Wrangler’s local static-assets server.

## Repository layout

```text
.
├── public/                    # Deployable static output
│   ├── index.html              # Home page
│   ├── 404.html                # Custom not-found page
│   ├── about/                  # Person entity page (Sreejith CU)
│   ├── case-studies/           # Work hub + Mindtech Solutions case study
│   ├── services/               # Service hub + 9 service pages
│   ├── industries/             # Industry hub + 5 industry pages
│   ├── locations/              # Location hub + 5 project-based pages
│   ├── resources/              # Resource hub + 9 guides
│   ├── free-seo-review/        # Lead offer + form
│   ├── thank-you/              # noindex conversion page
│   ├── contact/
│   ├── privacy/
│   ├── terms/
│   ├── assets/
│   ├── sitemap.xml
│   ├── robots.txt
│   ├── _headers
│   ├── _redirects
│   ├── CNAME
│   └── .nojekyll
├── scripts/generate_site.py    # Source for all generated HTML and sitemap.xml
├── worker/index.js             # POST /api/enquiry → email (Cloudflare Email Routing)
├── wrangler.toml               # Workers config: static assets + /api/* Worker
├── package.json                # Pinned Wrangler development dependency
├── package-lock.json
├── DEPLOYMENT.md               # Cloudflare Workers / Pages / domain instructions
├── SEO-STRATEGY.md             # Strategy, keyword map, milestones and KPIs
├── PROJECT-LOG.md              # Complete log book: every change and decision (see its Logbook rules)
├── AGENTS.md                   # Rules for people and AI tools, incl. mandatory logging
└── README.md
```

Cloudflare Workers static assets require an explicit asset directory and explicit 404 / HTML handling; those settings are in `wrangler.toml` and point at `./public/`.

## Regenerating the site

`scripts/generate_site.py` is the single source of truth for page content and metadata. It uses only the Python standard library and writes generated files into `public/`.

```bash
python3 scripts/generate_site.py
```

Do not edit generated HTML directly unless you also remove or update the generator workflow; the next regeneration will overwrite your changes.

Before launch, review these values in `scripts/generate_site.py`:

- `BASE_URL`
- `CONTACT_EMAIL`
- `SERVICES`, `INDUSTRIES`, `LOCATIONS`, and `RESOURCES`
- `LAST_UPDATED`, privacy copy, and terms copy

Owner details (`OWNER_*`, `EXPERIENCE`), analytics IDs and dated client results (`CLIENT_RANKINGS`) also live at the top of the generator. Optional lists render nothing while empty, so no placeholder reaches a live page.

Location pages must pass the city-name test in `SEO-STRATEGY.md`: if the page is still true with another city's name in it, it does not get published.

## Deployment settings

See [`DEPLOYMENT.md`](DEPLOYMENT.md) for the complete setup and custom-domain connection steps.

### Workers Builds / `npx wrangler deploy`

| Setting | Value |
| --- | --- |
| Root directory | `/` |
| Build command | Empty |
| Deploy command | `npx wrangler deploy` |
| Asset directory | From `wrangler.toml`: `./public/` |
| Custom 404 | From `wrangler.toml`: `404-page` |

The preferred Workers Build root directory is `/`; Wrangler needs the repository root so it can find `wrangler.toml`. A mirrored `public/wrangler.toml`, `public/package.json`, and `public/.assetsignore` are also included as a fallback if Cloudflare’s root directory was already set to `/public`.

### Cloudflare Pages

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command | Empty |
| Build output directory | `public` |
| Root directory | `/` |

### Domain canonicalisation

`public/_redirects` contains only path-level redirects. Host-level `www → apex` redirects are not supported by `_redirects`; configure them with Cloudflare Bulk Redirects or Redirect Rules as described in `DEPLOYMENT.md`.

## SEO strategy

`SEO-STRATEGY.md` holds the positioning, doorway/spam fixes, location policy, architecture, keyword-to-URL map, conversion strategy, milestones and KPIs. `PROJECT-LOG.md` records each change with dates and evidence. Client results are dated snapshots; nothing is invented.

## Contact form

Both forms (`/free-seo-review/` and `/contact/`) post JSON to `POST /api/enquiry`, handled by `worker/index.js`, which validates the input, drops obvious bots (honeypot + timing) and emails the enquiry through Cloudflare Email Routing. Visitors land on `/thank-you/?ref=SD-…`.

If the endpoint is not configured yet, or is unreachable (for example on GitHub Pages), `main.js` falls back to opening the visitor's email app with the enquiry and reference pre-filled, so a lead is never silently lost. Setup steps are in `DEPLOYMENT.md` → "After merging release 2026-11-27.1".

## Analytics

None by default. Add `GA4_MEASUREMENT_ID` and/or `CLARITY_PROJECT_ID` in the generator to show a consent banner; scripts load only after a visitor chooses **Allow analytics**. Events: `form_start`, `generate_lead` (once per enquiry reference).
