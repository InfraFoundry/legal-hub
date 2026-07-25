#!/usr/bin/env python3
"""Validate the InfraFoundry Legal Hub using only the Python standard library."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://infrafoundry.github.io/legal-hub"
SUPPORT_EMAIL = "kodo.app.labs@gmail.com"

REQUIRED_FILES = (
    ".github/workflows/validate.yml",
    ".github/workflows/pages.yml",
    ".well-known/security.txt",
    "assets/favicon.svg",
    "assets/styles.css",
    "gitpulse/index.html",
    "gitpulse/privacy.html",
    "gitpulse/data-deletion.html",
    "gitpulse/terms.html",
    "gitpulse/contact.html",
    "repolynx/index.html",
    "repolynx/privacy.html",
    "repolynx/data-deletion.html",
    "repolynx/terms.html",
    "repolynx/contact.html",
    "scripts/validate_site.py",
    ".nojekyll",
    "404.html",
    "DEPLOYMENT_REPORT.md",
    "README.md",
    "index.html",
    "robots.txt",
    "site.config.json",
    "sitemap.xml",
)

SITEMAP_URLS = (
    f"{BASE_URL}/",
    f"{BASE_URL}/repolynx/",
    f"{BASE_URL}/repolynx/privacy.html",
    f"{BASE_URL}/repolynx/data-deletion.html",
    f"{BASE_URL}/repolynx/terms.html",
    f"{BASE_URL}/repolynx/contact.html",
    f"{BASE_URL}/gitpulse/",
    f"{BASE_URL}/gitpulse/privacy.html",
    f"{BASE_URL}/gitpulse/data-deletion.html",
    f"{BASE_URL}/gitpulse/terms.html",
    f"{BASE_URL}/gitpulse/contact.html",
)

TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".json",
    ".md",
    ".py",
    ".svg",
    ".txt",
    ".xml",
    ".yml",
    ".yaml",
}


class SiteHTMLParser(HTMLParser):
    """Collect structural facts and URL-bearing attributes from one HTML file."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1_count = 0
        self.has_title = False
        self.title_depth = 0
        self.title_text: list[str] = []
        self.has_viewport = False
        self.links: list[tuple[str, str]] = []
        self.script_count = 0
        self.style_count = 0
        self.form_count = 0
        self.external_assets: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.lower()
        values = {key.lower(): value or "" for key, value in attrs}
        if tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self.has_title = True
            self.title_depth += 1
        elif tag == "meta" and values.get("name", "").lower() == "viewport":
            self.has_viewport = bool(values.get("content", "").strip())
        elif tag == "script":
            self.script_count += 1
            src = values.get("src", "").strip()
            if src:
                self.links.append(("src", src))
                if is_external_url(src):
                    self.external_assets.append(src)
        elif tag == "style":
            self.style_count += 1
        elif tag == "form":
            self.form_count += 1

        if tag == "a" and values.get("href"):
            self.links.append(("href", values["href"]))
        elif tag == "link" and values.get("href"):
            href = values["href"]
            self.links.append(("href", href))
            rel = values.get("rel", "").lower().split()
            if "stylesheet" in rel and is_external_url(href):
                self.external_assets.append(href)
        elif tag in {"img", "source", "video", "audio", "iframe"} and values.get(
            "src"
        ):
            src = values["src"]
            self.links.append(("src", src))
            if is_external_url(src):
                self.external_assets.append(src)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data)


def is_external_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} or url.startswith("//")


def local_target(source: Path, url: str) -> Path | None:
    """Resolve an internal link to its local file, or return None when not local."""

    clean = unquote(url.strip())
    if not clean or clean.startswith(("#", "mailto:", "tel:")):
        return None

    parsed = urlparse(clean)
    if parsed.scheme in {"http", "https"}:
        absolute = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")
        if absolute != BASE_URL and not absolute.startswith(f"{BASE_URL}/"):
            return None
        relative = parsed.path.removeprefix("/legal-hub/").removeprefix(
            "/legal-hub"
        )
        target = ROOT / relative
    elif parsed.scheme:
        return None
    elif parsed.path.startswith("/legal-hub/"):
        target = ROOT / parsed.path.removeprefix("/legal-hub/")
    elif parsed.path in {"/legal-hub", "/legal-hub/"}:
        target = ROOT
    elif parsed.path.startswith("/"):
        return None
    else:
        target = source.parent / parsed.path

    if not parsed.path or parsed.path.endswith("/"):
        target = target / "index.html"
    return target.resolve()


def iter_text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in TEXT_SUFFIXES
    ]


def validate_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")
    if not (ROOT / "index.html").is_file():
        errors.append("root index.html is missing")


def validate_config(errors: list[str]) -> None:
    path = ROOT / "site.config.json"
    if not path.is_file():
        return
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"site.config.json is invalid: {exc}")
        return

    expected = {
        "organization": "InfraFoundry",
        "repository": "legal-hub",
        "base_url": BASE_URL,
        "support_email": SUPPORT_EMAIL,
        "last_updated": "2026-07-25",
    }
    for key, value in expected.items():
        if config.get(key) != value:
            errors.append(f"site.config.json has unexpected {key!r}")


def validate_html(errors: list[str]) -> None:
    html_files = sorted(ROOT.rglob("*.html"))
    if not html_files:
        errors.append("no HTML files found")
        return

    for path in html_files:
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"{relative}: HTML is empty")
            continue
        if not re.match(r"\s*<!doctype\s+html>", text, flags=re.IGNORECASE):
            errors.append(f"{relative}: missing HTML doctype")
        if "http://" in text.lower():
            errors.append(f"{relative}: insecure http:// URL found")

        parser = SiteHTMLParser()
        try:
            parser.feed(text)
            parser.close()
        except Exception as exc:  # HTMLParser normally tolerates malformed markup.
            errors.append(f"{relative}: HTML parsing failed: {exc}")
            continue

        if not parser.has_title or not "".join(parser.title_text).strip():
            errors.append(f"{relative}: missing non-empty title")
        if not parser.has_viewport:
            errors.append(f"{relative}: missing viewport meta")
        if parser.h1_count != 1:
            errors.append(f"{relative}: expected one h1, found {parser.h1_count}")
        if parser.script_count:
            errors.append(f"{relative}: script elements are not allowed")
        if parser.style_count:
            errors.append(f"{relative}: inline style elements are not allowed")
        if parser.form_count:
            errors.append(f"{relative}: forms are not allowed")
        for asset in parser.external_assets:
            errors.append(f"{relative}: external CSS/JS/media asset: {asset}")
        if "© 2026 InfraFoundry" not in text:
            errors.append(f"{relative}: missing InfraFoundry copyright")
        if "No tracking or analytics are used on this legal site." not in text:
            errors.append(f"{relative}: missing no-analytics statement")

        for attribute, url in parser.links:
            target = local_target(path, url)
            if target is None:
                continue
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(
                    f"{relative}: {attribute} escapes repository root: {url}"
                )
                continue
            if not target.is_file():
                errors.append(
                    f"{relative}: broken internal {attribute} {url!r} "
                    f"(expected {target.relative_to(ROOT).as_posix()})"
                )


def validate_policy_content(errors: list[str]) -> None:
    checks = {
        "repolynx": {
            "privacy": (
                "RepoLynx",
                SUPPORT_EMAIL,
                "data-deletion.html",
                "password",
                "access token",
            ),
            "deletion": (
                SUPPORT_EMAIL,
                "RepoLynx Data Deletion Request",
                "7 days",
                "30 days",
                "password",
                "access token",
            ),
        },
        "gitpulse": {
            "privacy": (
                "GitPulse",
                SUPPORT_EMAIL,
                "data-deletion.html",
                "password",
                "access token",
            ),
            "deletion": (
                SUPPORT_EMAIL,
                "GitPulse Data Deletion Request",
                "7 days",
                "30 days",
                "password",
                "access token",
            ),
        },
    }
    for project, page_checks in checks.items():
        for page, terms in page_checks.items():
            path = ROOT / project / f"{page}.html"
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8").lower()
            for term in terms:
                if term.lower() not in text:
                    errors.append(
                        f"{path.relative_to(ROOT).as_posix()}: "
                        f"required content missing: {term}"
                    )

    repolynx_deletion = ROOT / "repolynx/data-deletion.html"
    if repolynx_deletion.is_file():
        text = repolynx_deletion.read_text(encoding="utf-8").lower()
        if (
            "not an automated meta data deletion callback" not in text
            or "signed request" not in text
        ):
            errors.append(
                "repolynx/data-deletion.html: callback limitation is incomplete"
            )


def validate_service_files(errors: list[str]) -> None:
    sitemap_path = ROOT / "sitemap.xml"
    if sitemap_path.is_file():
        sitemap = sitemap_path.read_text(encoding="utf-8")
        for url in SITEMAP_URLS:
            if f"<loc>{url}</loc>" not in sitemap:
                errors.append(f"sitemap.xml: missing URL {url}")
        if sitemap.count("<url>") != len(SITEMAP_URLS):
            errors.append("sitemap.xml: unexpected number of URL entries")

    robots_path = ROOT / "robots.txt"
    if robots_path.is_file():
        robots = robots_path.read_text(encoding="utf-8")
        expected = f"Sitemap: {BASE_URL}/sitemap.xml"
        if expected not in robots:
            errors.append("robots.txt: sitemap declaration is missing")


def validate_secret_hygiene(errors: list[str]) -> None:
    assigned_names = (
        "app_secret",
        "access_token",
        "refresh_token",
        "client_secret",
        "password",
    )
    assignment_patterns = [
        re.compile(rf"(?i)\b{re.escape(name)}\s*=") for name in assigned_names
    ]
    private_key_markers = (
        "BEGIN " + "RSA PRIVATE KEY",
        "BEGIN " + "OPENSSH PRIVATE KEY",
    )

    for path in iter_text_files():
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in assignment_patterns:
            if pattern.search(text):
                errors.append(
                    f"{relative}: possible assigned secret ({pattern.pattern})"
                )
        for marker in private_key_markers:
            if marker.lower() in text.lower():
                errors.append(f"{relative}: private key marker found")


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    validate_config(errors)
    validate_html(errors)
    validate_policy_content(errors)
    validate_service_files(errors)
    validate_secret_hygiene(errors)

    if errors:
        print("Legal Hub validation errors:")
        for error in errors:
            print(f"- {error}")
        print("LEGAL_HUB_VALIDATION=FAIL")
        return 1

    print("LEGAL_HUB_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
