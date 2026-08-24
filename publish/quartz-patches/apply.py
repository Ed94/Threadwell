"""Single source of truth for the Threadwell site base.

Two stages:

1. Apply the SPA basepath patch to quartz/components/scripts/spa.inline.ts so
   relative URLs in the SPA click handler resolve from a directory base.

2. After `npx quartz build`, rewrite every built HTML file:
   - add `<base href="<abs>">` so relative URL resolution works even when
     the URL bar lacks a trailing slash
   - rewrite the sidebar `<a class="page-title">` href to the absolute site
     base, not the directory the page is in

The base URL is read from `publish/quartz.config.yaml`'s `baseUrl`. Change
that line; the next deploy uses the new value everywhere.

Idempotent. Safe to re-run.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve()
VAULT = SCRIPT.parents[2]
QUARTZ_REPO = VAULT / "site" / "quartz"
SPA_FILE = QUARTZ_REPO / "components" / "scripts" / "spa.inline.ts"
PUBLIC = VAULT / "site" / "public"
OVERLAY = VAULT / "publish" / "quartz.config.yaml"


def read_base_url() -> tuple[str, str]:
    """Read `baseUrl` from the overlay (YAML) as the single source of truth.

    Falls back to lenient line scan if YAML parsing isn't available.
    """
    text = OVERLAY.read_text(encoding="utf-8")
    host = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        if stripped.startswith("baseUrl:"):
            host = stripped.split(":", 1)[1].strip()
            break
    if not host or "/" not in host:
        raise SystemExit(f"missing baseUrl in {OVERLAY}")
    if host.startswith("http://"):
        scheme = "http://"
        host = host[len("http://") :]
    elif host.startswith("https://"):
        scheme = "https://"
        host = host[len("https://") :]
    else:
        scheme = "https://"
    domain, _, path = host.partition("/")
    abs_base = (
        f"{scheme}{domain}/{path.rstrip('/')}/" if path else f"{scheme}{domain}/"
    )
    rel_base = "/" + path.rstrip("/") + "/" if path else "/"
    return abs_base, rel_base


ABS_BASE, REL_BASE = read_base_url()
HEAD_RE = re.compile(r"(<head[^>]*>)", re.IGNORECASE)
BASE_TAG = f'<base href="{ABS_BASE}">\n'
TITLE_LINK = re.compile(
    r'(<h2[^>]*class="page-title"><a\s+href=")[^"]*(">)'
)


# --- SPA click-handler patch ----------------------------------------------


INSERT_AFTER = (
    "const isElement = (target: EventTarget | null): target is Element =>\n"
    "  (target as Node)?.nodeType === NODE_TYPE_ELEMENT"
)

INSERT_BLOCK = (
    "const SPA_BASE_HREF = (() => {\n"
    "  if (typeof window === \"undefined\") return \"\"\n"
    "  const { origin, pathname } = window.location\n"
    "  if (pathname.endsWith(\"/\")) return origin + pathname\n"
    "  const last = pathname.split(\"/\").pop() ?? \"\"\n"
    "  if (last.includes(\".\")) return origin + pathname\n"
    "  return origin + pathname.replace(/[^/]*$/, \"\")\n"
    "})()\n\n"
)

REPLACE_GETOPTS = (
    "  const { href } = a\n"
    "  if (!isLocalUrl(href)) return\n"
    "  return { url: new URL(href), scroll: "
    "\"routerNoscroll\" in a.dataset ? false : undefined }\n"
    "}"
)

REPLACE_WITH = (
    "  const { href } = a\n"
    "  if (!isLocalUrl(href)) return\n"
    "  const url = SPA_BASE_HREF ? new URL(href, SPA_BASE_HREF) : new URL(href)\n"
    "  return { url, scroll: "
    "\"routerNoscroll\" in a.dataset ? false : undefined }\n"
    "}"
)


def patch_spa() -> bool:
    if not SPA_FILE.exists():
        print(f"missing {SPA_FILE}")
        return False
    text = SPA_FILE.read_text(encoding="utf-8")
    if "SPA_BASE_HREF" in text:
        print(f"SPA already patched")
        return True
    if INSERT_AFTER not in text:
        print("SPA anchor missing; Quartz upstream changed?")
        return False
    if REPLACE_GETOPTS not in text:
        print("SPA getOpts missing")
        return False
    text = text.replace(INSERT_AFTER, INSERT_BLOCK + INSERT_AFTER, 1)
    text = text.replace(REPLACE_GETOPTS, REPLACE_WITH, 1)
    SPA_FILE.write_text(text, encoding="utf-8")
    print("SPA patched")
    return True


# --- post-build HTML rewrites ----------------------------------------------


def rewrite_html(path: Path) -> str | None:
    """Return 'base' / 'title' / None for what changed."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    out = text
    actions = []

    m = HEAD_RE.search(out)
    if m and "quartz-base" not in out:
        out = out[: m.end()] + "\n" + BASE_TAG + out[m.end():]
        actions.append("base")
    if 'class="page-title"' in out:
        out2 = TITLE_LINK.sub(rf"\g<1>{ABS_BASE}\g<2>", out)
        if out2 != out:
            out = out2
            actions.append("title")

    if out != text:
        path.write_text(out, encoding="utf-8")
    return ",".join(actions) if actions else None


def rewrite_built_htmls() -> tuple[int, int, int]:
    if not PUBLIC.is_dir():
        print(f"missing {PUBLIC} (run after npx quartz build)")
        return 0, 0, 0
    base_count = title_count = total = 0
    for path in PUBLIC.rglob("*.html"):
        total += 1
        result = rewrite_html(path)
        if result:
            if "base" in result:
                base_count += 1
            if "title" in result:
                title_count += 1
    return base_count, title_count, total


# --- entry point ----------------------------------------------------------


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("spa", "all"):
        ok = patch_spa()
        if not ok and mode == "spa":
            return 1

    if mode in ("built", "all"):
        b, t, total = rewrite_built_htmls()
        print(f"base tag: {b}, title link: {t}, total {total}")
        print(f"absolute base: {ABS_BASE}")
        print(f"relative base: {REL_BASE}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
