# InfraFoundry Legal Hub

Static English-language public legal documents for projects operated under the InfraFoundry technical namespace.

Published site: <https://infrafoundry.github.io/legal-hub/>

## Projects and documents

The site currently contains separate legal areas for:

- **RepoLynx** — product and authorized publishing infrastructure;
- **GitPulse** — media brand and editorial/social publishing channels.

Each area has its own English-language project overview, Privacy Policy, User Data Deletion Instructions, Terms of Service, and Contact page.

## Repository structure

```text
.
├── .github/workflows/   Validation and GitHub Pages deployment
├── .well-known/         Security contact metadata
├── assets/              Shared static CSS and favicon
├── gitpulse/            GitPulse legal documents
├── repolynx/            RepoLynx legal documents
├── scripts/             Standard-library site validator
├── 404.html
├── index.html
├── robots.txt
├── site.config.json
└── sitemap.xml
```

The site deliberately has no Jekyll, Node.js, npm, static-site generator, forms, external JavaScript, external fonts, analytics, cookies, or advertising pixels.

## Add a project

1. Add the project to `site.config.json`.
2. Create a project directory containing `index.html`, `privacy.html`, `data-deletion.html`, `terms.html`, and `contact.html`.
3. Use `../assets/styles.css` and `../assets/favicon.svg` from nested pages.
4. Provide English content with one `h1` per page.
5. Add every public page URL to `sitemap.xml`.
6. Add the new files and required policy checks to `scripts/validate_site.py`.
7. Run the validator before opening a pull request.

## Change the GitHub contact or update date

`site.config.json` is the canonical reference for the GitHub Issues contact, private security-reporting URL, and document date. Because this repository is a static site without a generator, update the visible values in all affected HTML, `security.txt`, `sitemap.xml`, and documentation at the same time. The validator checks the configured constants and required legal-page values for consistency.

## Local development

No dependencies need to be installed.

Run the validation:

```bash
python scripts/validate_site.py
```

Serve the repository root locally:

```bash
python -m http.server 8000
```

Then open <http://localhost:8000/>. The public-site prohibition on insecure `http://` URLs applies to committed page content; localhost HTTP is appropriate for local testing only.

## Deployment

The `Validate Legal Hub` workflow runs on pull requests, pushes to `main`, and manual dispatch. The `Deploy Legal Hub to Pages` workflow validates the site, uploads the repository as a static artifact, and deploys it to the `github-pages` environment.

GitHub Pages must use **GitHub Actions** as its source:

```text
Repository → Settings → Pages
→ Build and deployment
→ Source → GitHub Actions
```

No custom domain or `CNAME` is required.

## Meta App URLs

For **RepoLynx Media Publisher**:

- Privacy Policy: <https://infrafoundry.github.io/legal-hub/repolynx/privacy.html>
- User Data Deletion Instructions: <https://infrafoundry.github.io/legal-hub/repolynx/data-deletion.html>
- Terms of Service: <https://infrafoundry.github.io/legal-hub/repolynx/terms.html>
- Contact: <https://infrafoundry.github.io/legal-hub/repolynx/contact.html>

## Security

Never commit App Secret, access tokens, refresh tokens, passwords, recovery codes, private keys, OAuth authorization codes, or production environment files.

Public privacy, deletion, correction, terms, and general requests use [GitHub Issues](https://github.com/InfraFoundry/legal-hub/issues). Issues are public: never post secrets, authentication codes, private keys, payment information, or sensitive personal data.

Security vulnerabilities use [GitHub private vulnerability reporting](https://github.com/InfraFoundry/legal-hub/security/advisories/new).

## Deletion instructions are not a callback

The static deletion pages explain how a person can revoke access and request deletion. GitHub Pages cannot receive or validate a Meta server-to-server POST request and must not be configured as a Meta Data Deletion Callback.

If Meta later requires an automated callback, it is a separate backend task:

```text
POST https://api.repolynx.com/oauth/meta/data-deletion
```

That backend must validate Meta's signed request using an App Secret stored only on the backend, avoid logging secrets and raw tokens, initiate idempotent deletion, return a `confirmation_code` and `status_url`, and keep a secure audit trail.

## Legal note

These documents are working templates for the current technical stage and do not replace advice from qualified legal counsel. Before processing third-party client data, advertising accounts, payments, or expanding into additional jurisdictions, obtain a legal review and ensure the application's actual collection, storage, publishing, and deletion behavior exactly matches the published documents.
