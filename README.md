# Sreejith Digital — static website

A deployment-ready, dependency-free static website for **https://sreejithdigital.com**. The repository is designed for Cloudflare Pages with **no build command**: the generated HTML, CSS, JavaScript, images, sitemap, and routing files live in the repository root.

The site implements the recommended consultant-site architecture from the brief:

- `Home`, `About`, `Services`, `Industries`, `Locations`, `Resources`, `Contact`
- Dropdown-ready navigation for services, industries, locations, and resources
- 29 indexable pages with clean directory URLs, unique metadata, breadcrumbs, and structured data
- Eight service pages, four industry pages, four location guides, and four practical resources
- Dark visual system with green accents, responsive navigation, accessible focus states, and reduced-motion support
- `robots.txt`, `sitemap.xml`, `_headers`, `_redirects`, `CNAME`, `.nojekyll`, and a custom `404.html`

## Quick preview

Root-relative URLs are used throughout, so preview through a server rather than opening `index.html` directly:

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

Then open `http://localhost:8000/` locally, or use the live preview exposed by the workspace.

## Repository layout

```text
.
├── index.html                 # Home page
├── 404.html                   # Cloudflare Pages / GitHub Pages 404
├── about/                     # About
├── services/                  # Service hub + 8 service pages
├── industries/                # Industry hub + 4 industry pages
├── locations/                 # Location hub + 4 location guides
├── resources/                 # Resource hub + 4 guides
├── contact/                   # Static contact form
├── privacy/                   # Privacy policy
├── terms/                     # Terms of use
├── assets/
│   ├── css/styles.css
│   ├── js/main.js
│   └── img/                   # Favicon and social card
├── scripts/generate_site.py   # Source for all generated HTML and sitemap.xml
├── sitemap.xml
├── robots.txt
├── _headers                   # Cloudflare Pages response headers
├── _redirects                 # www → apex canonical redirect
├── CNAME                      # GitHub Pages custom-domain fallback
├── .nojekyll                  # Prevent Jekyll processing on GitHub Pages
├── DEPLOYMENT.md              # Cloudflare Pages + custom-domain instructions
└── README.md
```

## Regenerating the site

`scripts/generate_site.py` is the single source of truth for page content and metadata. It uses only the Python standard library.

```bash
python3 scripts/generate_site.py
```

It rewrites every `index.html`, `404.html`, and `sitemap.xml` from the structured data at the top of the script. **Do not edit generated HTML directly** unless you also remove or update the generator workflow; otherwise the next regeneration will overwrite your changes.

Before launch, review these values in `scripts/generate_site.py`:

- `BASE_URL`
- `CONTACT_EMAIL`
- `SERVICES`, `INDUSTRIES`, `LOCATIONS`, and `RESOURCES`
- `LAST_UPDATED`, privacy copy, and terms copy

The location pages explicitly describe remote-first consulting and do **not** claim physical offices. Adjust the locations and market descriptions if they do not match the real service areas.

## Deployment

See [`DEPLOYMENT.md`](DEPLOYMENT.md) for the complete Cloudflare Pages setup and custom-domain connection steps.

Recommended settings:

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command | Leave empty |
| Build output directory | `/` (or `.` if the UI rejects `/`) |
| Root directory | `/` |
| Primary custom domain | `sreejithdigital.com` |
| Additional custom domain | `www.sreejithdigital.com` |

## Contact form

The contact form is intentionally static and privacy-friendly: JavaScript builds a `mailto:` link in the visitor’s email application. No data is stored by this website, and no analytics, advertising pixels, or third-party form service are loaded.

For production lead capture without requiring an email app, connect a form endpoint (for example, a Cloudflare Worker or a form service) and update `contact_page()` in the generator. Also update the privacy policy if the new service processes personal data.

## No runtime dependencies

There is no `npm install`, package manager, framework, database, or server-side runtime. Every page is plain HTML with one shared stylesheet and one shared JavaScript file.
