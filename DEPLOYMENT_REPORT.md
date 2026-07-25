# InfraFoundry Legal Hub Deployment Report

- Generated at UTC: 2026-07-25 20:04:41 UTC
- Generated at local time: 2026-07-25 23:04:41 +03:00
- Repository: <https://github.com/InfraFoundry/legal-hub>
- Branch: `feat/legal-hub-v1`
- Implementation commit SHA: `ec160791dface1a802c6b49bf682a53f0c77a3bf`
- Workflow run: Not created; remote rejected branch push
- Pages URL: <https://infrafoundry.github.io/legal-hub/>

## Result

`BLOCKED`

The complete implementation is committed locally. A push to `origin/feat/legal-hub-v1` was attempted and rejected with HTTP 403 because the available Git credential belongs to `maksim4351`, which does not have write permission for `InfraFoundry/legal-hub`. The browser GitHub session is signed out, and GitHub CLI has no authenticated host. Remote publication cannot be completed without an account that has repository write access.

## Implemented

- responsive, accessible bilingual EN/RU legal hub;
- separate RepoLynx and GitPulse project areas;
- Privacy, User Data Deletion, Terms, and Contact pages for both projects;
- required root index, 404, robots, sitemap, security.txt, `.nojekyll`, favicon, and shared CSS;
- standard-library Python validation;
- pull-request and main-branch validation workflow;
- GitHub Actions Pages deployment workflow;
- public support email centralized in `site.config.json`;
- no analytics, cookies, forms, external scripts, external fonts, or CDN dependencies.

## Validation

- local validator: `LEGAL_HUB_VALIDATION=PASS`
- local HTTP: all nine required paths returned 200 with non-empty bodies
- GitHub Actions: not run; the branch could not be published
- Pages: not enabled or deployed from this implementation
- live HTTP: all nine required URLs returned HTTP 404 on 2026-07-25
- mobile layout at 360 px: PASS for the root page and RepoLynx Privacy Policy; no horizontal overflow, stylesheet loaded, one `h1`, and EN/RU sections present

## Published URLs

- Legal Hub: <https://infrafoundry.github.io/legal-hub/>
- RepoLynx: <https://infrafoundry.github.io/legal-hub/repolynx/>
- GitPulse: <https://infrafoundry.github.io/legal-hub/gitpulse/>

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
- HTTPS: all committed canonical and public URLs use HTTPS

## Manual Actions Required

Authenticate GitHub CLI on this workstation with an account that has write and admin access to `InfraFoundry/legal-hub`, then resume this Codex task. Codex will push the branch, open the pull request, run and verify Actions, configure the Pages source shown below, and repeat the live HTTP checks.

```text
Repository → Settings → Pages
→ Build and deployment
→ Source → GitHub Actions
```

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
