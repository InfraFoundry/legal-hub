# InfraFoundry Legal Hub Deployment Report

- Generated at UTC: 2026-07-25 23:34:12 UTC
- Generated at local time: 2026-07-26 02:34:12 +03:00
- Repository: <https://github.com/InfraFoundry/legal-hub>
- Branch: `main`
- Implementation commit SHA: `937ec89bbea47745835803ad302d66a3d962f4f4`
- Change delivery: direct push to `main`
- Validation run: <https://github.com/InfraFoundry/legal-hub/actions/runs/30179608682>
- Pages workflow run: <https://github.com/InfraFoundry/legal-hub/actions/runs/30179608711>
- Pages URL: <https://infrafoundry.github.io/legal-hub/>

## Result

`COMPLETE`

The Pages artifact configuration now explicitly includes hidden files, so `.well-known/security.txt` is published with the rest of the English-only static site. Commit `937ec89bbea47745835803ad302d66a3d962f4f4` was validated by GitHub Actions and deployed to GitHub Pages. The legal text, existing URLs, temporary deletion email, and site structure were not changed.

## Implemented

- responsive, accessible English-language legal hub;
- separate RepoLynx and GitPulse project areas;
- Privacy, User Data Deletion, Terms, and Contact pages for both projects;
- required root index, 404, robots, sitemap, security.txt, `.nojekyll`, favicon, and shared CSS;
- standard-library Python validation;
- pull-request and main-branch validation workflow;
- GitHub Actions Pages deployment workflow using Node 24-compatible action majors: `actions/checkout@v7`, `actions/setup-python@v7`, `actions/configure-pages@v6`, `actions/upload-pages-artifact@v5`, and `actions/deploy-pages@v5`;
- Pages artifact upload configured with `path: "."` and `include-hidden-files: true`;
- GitHub Issues and private security reporting configured as contact channels;
- temporary support email retained only in Privacy Policy and Data Deletion pages until a Meta Data Deletion Callback is implemented;
- no analytics, cookies, forms, external scripts, external fonts, or CDN dependencies.

## Validation

- local validator: `LEGAL_HUB_VALIDATION=PASS`
- local sitemap validation: PASS; all 11 listed URLs map to existing files and are unique HTTPS URLs under the configured Pages base URL
- main validation: PASS, run `30179608682`
- Pages deployment: PASS, run `30179608711`
- live HTML HTTP and content: PASS; all 12 repository HTML pages returned 200 with non-empty bodies and no GitHub Pages 404 response, including `404.html`, which is not listed in the sitemap
- live service URLs: PASS; `/.well-known/security.txt`, `/robots.txt`, `/sitemap.xml`, and `/404.html` each returned HTTP 200
- live security.txt: PASS; `/.well-known/security.txt` returned HTTP 200 with `text/plain; charset=utf-8`
- live English-only check: PASS across all 12 HTML pages; no Cyrillic characters, `Русский` label, or language-switcher markup was found
- live support-email scope: PASS; the support email and `Meta Data Deletion Callback` notice appear only on the four Privacy Policy and Data Deletion URLs
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
- published security.txt: PASS; HTTP 200 at <https://infrafoundry.github.io/legal-hub/.well-known/security.txt>
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
