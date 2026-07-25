# InfraFoundry Legal Hub Deployment Report

- Generated at UTC: 2026-07-25 20:41:32 UTC
- Generated at local time: 2026-07-25 23:41:32 +03:00
- Repository: <https://github.com/InfraFoundry/legal-hub>
- Branch: `main`
- Implementation commit SHA: `8c4c1f2d6bc35567fb484344e403b50ae820b4b9`
- Pull request: <https://github.com/InfraFoundry/legal-hub/pull/2>
- Validation run: <https://github.com/InfraFoundry/legal-hub/actions/runs/30174049860>
- Pages workflow run: <https://github.com/InfraFoundry/legal-hub/actions/runs/30174049862>
- Pages URL: <https://infrafoundry.github.io/legal-hub/>

## Result

`COMPLETE`

The English-only, GitHub-contact implementation was pushed in `feat/github-contact-english-only`, reviewed through pull request #2, merged into `main`, validated by GitHub Actions, and deployed to GitHub Pages. GitHub Pages uses the `workflow` build type and enforces HTTPS.

## Implemented

- responsive, accessible English-language legal hub;
- separate RepoLynx and GitPulse project areas;
- Privacy, User Data Deletion, Terms, and Contact pages for both projects;
- required root index, 404, robots, sitemap, security.txt, `.nojekyll`, favicon, and shared CSS;
- standard-library Python validation;
- pull-request and main-branch validation workflow;
- GitHub Actions Pages deployment workflow;
- GitHub Issues and private security reporting configured as contact channels;
- temporary support email retained only in Privacy Policy and Data Deletion pages until a Meta Data Deletion Callback is implemented;
- no analytics, cookies, forms, external scripts, external fonts, or CDN dependencies.

## Validation

- local validator: `LEGAL_HUB_VALIDATION=PASS`
- local HTTP: all 15 checked paths returned 200 with non-empty bodies
- pull-request validation: PASS, run `30174039071`
- main validation: PASS, run `30174049860`
- Pages deployment: PASS, run `30174049862`
- live HTTP and content: PASS; all 15 checked HTTPS paths returned 200, all HTML is English-only, and contact pages contain GitHub Issues and private security-reporting links
- mobile layout at 360 px: PASS on the RepoLynx Contact page; no horizontal overflow, one `h1`, no scripts or forms, no Cyrillic, and all GitHub contact routes present

## Published URLs

- Legal Hub: <https://infrafoundry.github.io/legal-hub/>
- RepoLynx: <https://infrafoundry.github.io/legal-hub/repolynx/>
- RepoLynx Privacy: <https://infrafoundry.github.io/legal-hub/repolynx/privacy.html>
- RepoLynx Data Deletion: <https://infrafoundry.github.io/legal-hub/repolynx/data-deletion.html>
- RepoLynx Terms: <https://infrafoundry.github.io/legal-hub/repolynx/terms.html>
- RepoLynx Contact: <https://infrafoundry.github.io/legal-hub/repolynx/contact.html>
- GitPulse: <https://infrafoundry.github.io/legal-hub/gitpulse/>
- GitPulse Privacy: <https://infrafoundry.github.io/legal-hub/gitpulse/privacy.html>
- GitPulse Data Deletion: <https://infrafoundry.github.io/legal-hub/gitpulse/data-deletion.html>
- GitPulse Terms: <https://infrafoundry.github.io/legal-hub/gitpulse/terms.html>
- GitPulse Contact: <https://infrafoundry.github.io/legal-hub/gitpulse/contact.html>

## Meta Values

- Privacy Policy URL: <https://infrafoundry.github.io/legal-hub/repolynx/privacy.html>
- User Data Deletion Instructions URL: <https://infrafoundry.github.io/legal-hub/repolynx/data-deletion.html>
- Terms of Service URL: <https://infrafoundry.github.io/legal-hub/repolynx/terms.html>
- Contact URL: <https://infrafoundry.github.io/legal-hub/repolynx/contact.html>

## Security Check

- secrets: PASS; assigned-secret and private-key-marker scan found no secret
- trackers: none
- external scripts: none
- forms: none
- support email: limited to the configured address in Privacy Policy and Data Deletion pages
- private vulnerability reporting: enabled
- HTTPS: enforced by GitHub Pages

## Manual Actions Required

None.

## Future Backend Requirement

Do not use a static GitHub Pages URL as a Meta Data Deletion Callback. A future backend task must implement:

```text
POST https://api.repolynx.com/oauth/meta/data-deletion
```

The backend must accept a Meta signed request, verify its signature using an App Secret stored only on the backend, avoid logging secrets or raw tokens, initiate idempotent deletion, return a `confirmation_code` and `status_url`, and maintain a secure audit trail.

## Files Changed

- `.github/workflows/validate.yml`
- `.github/workflows/pages.yml`
- `.well-known/security.txt`
- `.nojekyll`
- `404.html`
- `README.md`
- `assets/favicon.svg`
- `assets/styles.css`
- `gitpulse/index.html`
- `gitpulse/privacy.html`
- `gitpulse/data-deletion.html`
- `gitpulse/terms.html`
- `gitpulse/contact.html`
- `index.html`
- `repolynx/index.html`
- `repolynx/privacy.html`
- `repolynx/data-deletion.html`
- `repolynx/terms.html`
- `repolynx/contact.html`
- `robots.txt`
- `scripts/validate_site.py`
- `site.config.json`
- `sitemap.xml`
