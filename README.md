# Sreejith Digital — static website

A deployment-ready static website for **https://sreejithdigital.com** — no hyphen. `sreejith-digital` is the Cloudflare Worker name used for the temporary `*.workers.dev` URL; it is not the registered domain. The deployable files live in [`public/`](public/), with a root-level [`wrangler.toml`](wrangler.toml) so the same repository works with:

- **Cloudflare Workers Builds / static assets** using `npx wrangler deploy`
- **Cloudflare Pages** with `public` as the build output directory
- **GitHub Pages** using the committed `public/CNAME` and `public/.nojekyll`

There are no runtime dependencies. `wrangler` is pinned as a development dependency so Cloudflare does not fetch an arbitrary new version on every deployment.

The site implements the recommended consultant-site architecture from the brief:

- `Home`, `About`, `Services`, `Industries`, `Locations`, `Resources`, `Contact`
- Dropdown-ready navigation for services, industries, locations, and resources
- 29 indexable pages with clean directory URLs, unique metadata, breadcrumbs, and structured data
- Eight service pages, four industry pages, four location guides, and four practical resources
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
│   ├── about/
│   ├── services/               # Service hub + 8 service pages
│   ├── industries/             # Industry hub + 4 industry pages
│   ├── locations/              # Location hub + 7 priority location guides
│   ├── resources/              # Resource hub + 8 India-focused guides
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
├── wrangler.toml               # Workers static-assets configuration
├── package.json                # Pinned Wrangler development dependency
├── package-lock.json
├── DEPLOYMENT.md               # Cloudflare Workers / Pages / domain instructions
├── SEO-STRATEGY.md             # Keyword map, content plan and 90-day roadmap
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

The location pages explicitly describe remote-first consulting and do not claim physical offices. Adjust the locations and market descriptions if they do not match the real service areas.

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

`SEO-STRATEGY.md` contains the India keyword-to-URL map, staged location rollout, content calendar, technical SEO checklist, E-E-A-T inputs still needed from the owner, and the 90-day execution roadmap. It uses the actual URLs generated by this repository and deliberately avoids fabricated case studies, credentials, rankings or office locations.

## Contact form

The contact form is intentionally static and privacy-friendly: JavaScript builds a `mailto:` link in the visitor’s email application. No data is stored by this website, and no analytics, advertising pixels, or third-party form service are loaded.

For production lead capture without requiring an email app, connect a form endpoint and update `contact_page()` in the generator. Also update the privacy policy if the new service processes personal data.
