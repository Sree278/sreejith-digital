# Deployment guide — sreejithdigital.com

This repository now supports both Cloudflare deployment paths. Your failed build log came from **Workers Builds / Wrangler**, not classic Cloudflare Pages:

```text
Executing user deploy command: npx wrangler deploy
✘ [ERROR] Could not detect a directory containing static files
```

That happened because `wrangler deploy` ran from the repository root with no Wrangler configuration and no auto-detected `public/` or `dist/` directory. The deployable HTML was also at the repository root.

## What changed in the repository

- All deployable files were moved into `public/`.
- A root-level `wrangler.toml` now declares `public/` as the static-assets directory.
- `not_found_handling = "404-page"` enables the custom `404.html`.
- `html_handling = "auto-trailing-slash"` preserves clean directory URLs such as `/services/seo-consulting/`.
- `package.json` and `package-lock.json` pin Wrangler `4.168.0`, matching the version in the build log.
- `public/_redirects` now contains only supported path-level redirects. Host-level redirects were removed because domain-level redirects are not supported in `_redirects`.

> The Cloudflare account is not connected to this workspace, so DNS records, custom domains, and project settings have not been changed here.

## Path A — keep the current Workers Builds project

This is the fastest fix: no project recreation is required.

1. Push the latest commit to `arena/06fc82b3-sreejith-digital` (already done for this change).
2. In Cloudflare, open the project’s **Settings → Builds & deployments**.
3. Confirm these values:

   | Setting | Value |
   | --- | --- |
   | Root directory | `/` |
   | Build command | Empty |
   | Deploy command | `npx wrangler deploy` |
   | Production branch | `arena/06fc82b3-sreejith-digital`, or `main` after merging |

4. Trigger **Retry deployment** or push another commit.
5. Verify that the log no longer contains `Could not detect a directory containing static files`.

Important: the root directory must stay `/`. If it is set to `public`, Wrangler will not find `wrangler.toml`.

If the Worker name `sreejithdigital-com` already exists in your account, change `name` in `wrangler.toml` to an available name and commit the change.

### Attach the apex custom domain

For a Workers project:

1. Open **Workers & Pages → your Worker → Settings → Domains & Routes**.
2. Select **Add → Custom Domain**.
3. Enter `sreejithdigital.com`.
4. Let Cloudflare create the required DNS record. Workers custom domains require the zone’s nameservers to be managed by Cloudflare, which is the case for this Cloudflare-registered domain.

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
curl -I https://www.sreejithdigital.com/services/
curl https://sreejithdigital.com/robots.txt
curl https://sreejithdigital.com/sitemap.xml
curl -I https://sreejithdigital.com/this-page-does-not-exist/
```

Expected results:

- Apex home page returns `200`.
- `www` returns `301` to the equivalent apex URL.
- `/robots.txt` lists `https://sreejithdigital.com/sitemap.xml`.
- `/sitemap.xml` contains the clean directory URLs.
- A nonexistent path returns `404` and renders `public/404.html`.
- Deep links such as `/services/seo-consulting/` and `/resources/technical-seo-audit-checklist/` return `200`.
- Dropdowns and the mobile menu work without console errors.
- The contact form opens the visitor’s email application with a prefilled enquiry.

Then submit `https://sreejithdigital.com/sitemap.xml` in Google Search Console.

## Optional GitHub Pages fallback

`public/CNAME` and `public/.nojekyll` remain available for GitHub Pages. If used, deploy the `public` folder from the production branch and enter `sreejithdigital.com` as the custom domain. At Cloudflare DNS, use GitHub’s current documented apex `A`/`AAAA` records and handle `www` with a Cloudflare Redirect Rule. Use DNS-only mode until GitHub has issued the custom-domain certificate.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `Could not detect a directory containing static files` | Keep Workers Build root directory at `/`, ensure `wrangler.toml` is committed, and make sure `public/` contains `index.html`. |
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
- Confirm the four city guides match the real service areas.
- Review the privacy and terms pages, especially if analytics, a CRM, calendar booking, or a form backend is added later.
- Connect a real form endpoint if you do not want enquiries to rely on the visitor’s email app.
- Verify that no fabricated client names, testimonials, rankings, or case-study metrics were added.
- Purge the Cloudflare cache after a content update if cached HTML does not refresh immediately.
