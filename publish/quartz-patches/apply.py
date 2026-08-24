"""Patch quartz spa.inline.ts so relative URL clicks resolve from a directory base.

Quartz's SPA click handler calls `new URL(href)`. When the URL bar is missing
a trailing slash, the browser treats the last path segment as a file, so
`../../../../tags/archive` from `/Threadwell/x/y/` (no slash) resolves to
`/Threadwell/x/tags/archive` instead of `/Threadwell/tags/archive`. SPA routing
loses the `/Threadwell/` base path on GitHub Pages project deployments.

Fix: compute `SPA_BASE_HREF` from `window.location`, always ending with `/`,
and resolve relative URLs against it.

Idempotent: safe to re-run.
"""
from __future__ import annotations

from pathlib import Path

TARGET = Path(
    "quartz/components/scripts/spa.inline.ts"
)

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
    "const isElement"
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


def patch(path: Path) -> bool:
    if not path.exists():
        print(f"missing {path}")
        return False
    text = path.read_text(encoding="utf-8")
    if "SPA_BASE_HREF" in text:
        print(f"already patched {path}")
        return True
    if INSERT_AFTER not in text:
        print(f"anchor missing in {path}")
        return False
    if REPLACE_GETOPTS not in text:
        print(f"getOpts block missing in {path}")
        return False
    text = text.replace(INSERT_AFTER, INSERT_BLOCK, 1)
    text = text.replace(REPLACE_GETOPTS, REPLACE_WITH, 1)
    path.write_text(text, encoding="utf-8")
    print(f"patched {path}")
    return True


def main() -> int:
    import sys

    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    return 0 if patch(base / TARGET) else 1


if __name__ == "__main__":
    raise SystemExit(main())
