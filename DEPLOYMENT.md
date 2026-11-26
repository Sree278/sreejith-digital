# Deployment guide — sreejithdigital.com

This repository is ready to host the static site. **Cloudflare Pages is the recommended platform** because the domain is registered through Cloudflare: it can connect the Git repository, create the DNS records, and issue certificates from the same account.

> The Cloudflare account is not connected to this workspace, so no DNS records, Pages project, or custom-domain settings have been changed here. The exact dashboard steps are below.

## 1. Push the site repository

From this checkout, commit and push the current working branch:

```bash
git add .
git commit -m "Build static site for sreejithdigital.com"
git push -u origin HEAD
```

Deploy this branch for staging, or merge it into `main` first and use `main` as the production branch. If you switch production branches later, update the branch in Cloudflare Pages.

## 2. Create the Cloudflare Pages project

In the Cloudflare dashboard:

1. Go to **Workers & Pages → Create → Pages → Connect to Git**.
2. Authorize GitHub if prompted and select `Sree278/sreejith-digital`.
3. Select the branch you want to deploy.
4. Use these build settings:

   | Field | Value |
   | --- | --- |
   | Framework preset | **None** |
   | Build command | **Empty** |
   | Build output directory | `/` — use `.` only if the UI does not accept `/` |
   | Root directory | `/` |
   | Environment variables | None required |

5. Save and deploy. Cloudflare will provide a temporary `*.pages.dev` URL.
6. Open the temporary URL and verify the home page, `/services/`, `/contact/`, and a deep link such as `/resources/technical-seo-audit-checklist/`.

Because all HTML is already committed, there is no build step and no Node.js dependency.

## 3. Attach the custom domains

In the Pages project, open **Custom domains → Set up a custom domain** and add:

1. `sreejithdigital.com`
2. `www.sreejithdigital.com`

Cloudflare should create the required CNAME records automatically because the domain uses Cloudflare nameservers. The apex record uses Cloudflare CNAME flattening.

If records must be added manually, use:

| Type | Name | Target | Proxy |
| --- | --- | --- | --- |
| `CNAME` | `@` | `<your-project>.pages.dev` | Proxied / orange cloud |
| `CNAME` | `www` | `<your-project>.pages.dev` | Proxied / orange cloud |

Remove stale apex `A`/`AAAA` records or old host records if Cloudflare reports a conflict. Do not delete unrelated mail (`MX`), verification (`TXT`), or DMARC/SPF records.

### Canonical domain

The site uses `https://sreejithdigital.com` as the canonical origin in:

- canonical tags and Open Graph URLs
- `sitemap.xml`
- `robots.txt`
- structured data
- `CNAME`

`_redirects` redirects `www` and HTTP variants to the apex with a `301`. Both custom domains still need to be attached so the redirect rule is evaluated for `www` traffic.

## 4. TLS and Cloudflare settings

Recommended Cloudflare settings for the domain:

- **SSL/TLS → Overview:** Full (strict)
- **SSL/TLS → Edge Certificates → Always Use HTTPS:** On
- **SSL/TLS → Edge Certificates → Minimum TLS Version:** 1.2 or higher
- Wait until both custom domains show an active certificate before announcing the site.
- Optionally enable HSTS only after confirming every intended subdomain works over HTTPS.

The committed `_headers` file adds `nosniff`, a referrer policy, a permissions policy, and a short cache lifetime for assets. It intentionally avoids frame-blocking headers so browser previews and approved embeds are not broken.

## 5. Verify the deployment

Run these checks after the certificate is active:

```bash
curl -I https://sreejithdigital.com/
curl -I https://www.sreejithdigital.com/services/
curl https://sreejithdigital.com/robots.txt
curl https://sreejithdigital.com/sitemap.xml
```

Expected results:

- `https://sreejithdigital.com/` returns `200`.
- `https://www.sreejithdigital.com/...` returns `301` to the equivalent apex URL.
- `/robots.txt` lists `https://sreejithdigital.com/sitemap.xml`.
- `/sitemap.xml` contains the clean directory URLs.
- A nonexistent path renders the custom `404.html`.
- Dropdowns and the mobile menu work without console errors.
- The contact form opens the visitor’s email application with a prefilled enquiry.

Then submit `https://sreejithdigital.com/sitemap.xml` in Google Search Console and request indexing for the home page.

## 6. Optional GitHub Pages fallback

The repository also includes `CNAME` and `.nojekyll`, so it can be served by GitHub Pages if needed:

1. In GitHub, open **Settings → Pages**.
2. Choose **Deploy from a branch**.
3. Select the production branch and the `/(root)` folder.
4. Enter `sreejithdigital.com` as the custom domain and enforce HTTPS.
5. At Cloudflare DNS, use GitHub’s current documented apex `A`/`AAAA` records and a `www` CNAME to `<username>.github.io`. Use DNS-only mode until GitHub has issued the custom-domain certificate.

Cloudflare Pages remains the cleaner option because DNS and TLS are managed in one place, and `_headers` / `_redirects` are natively supported.

## 7. Before announcing the site

- Confirm `hello@sreejithdigital.com` exists, or change `CONTACT_EMAIL` in `scripts/generate_site.py` and regenerate.
- Confirm the four city guides match the real service areas. Remove or replace any location that should not be marketed.
- Review the privacy and terms pages, especially if analytics, a CRM, calendar booking, or a form backend is added later.
- Connect a real form endpoint if you do not want enquiries to rely on the visitor’s email app.
- Verify that no fabricated client names, testimonials, rankings, or case-study metrics were added.
- Purge the Cloudflare cache after a content update if cached HTML does not refresh immediately.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| CSS/JS returns 404 | Build output directory must be the repository root; these files use root-relative URLs. |
| Deep link returns 404 | Ensure the deployed output contains `<page>/index.html` files and that the output directory was not set to `dist`. |
| `www` does not redirect | Attach `www.sreejithdigital.com` as a custom domain and confirm `_redirects` is at the repository root. |
| Redirect loop | Check for a conflicting Cloudflare Bulk Redirect or Page Rule that sends apex traffic back to `www`. |
| Certificate pending | Confirm Cloudflare nameservers, DNS proxy status, and SSL/TLS mode; allow more time for issuance. |
| Sitemap shows wrong host | Update `BASE_URL` in the generator, regenerate, commit, and redeploy. |
