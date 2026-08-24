"""Audit every handle index in the vault against real subdirectories.

Reports per handle:
  real       — set of subdirectory basenames on disk
  links      — set of basenames extracted from index.md wikilinks
  missing    — subdirectories with no wikilink in index.md
  stale      — wikilinks in index.md whose subdirectory does not exist

Usage:
  python scripts/twitter/audit_handle_index.py            # text report
  python scripts/twitter/audit_handle_index.py --json     # JSON report
  python scripts/twitter/audit_handle_index.py --vault <root>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_VAULT = HERE.parent.parent

_WIKILINK_ITEM = re.compile(r"^- \[\[([^\]|]+)\]\]\s*$")


def _split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end < 0:
        return "", text
    return text[: end + 4], text[end + 4 :]


def _index_links(idx_path: Path) -> set[str]:
    if not idx_path.is_file():
        return set()
    text = idx_path.read_text(encoding="utf-8")
    _, body = _split_frontmatter(text)
    out: set[str] = set()
    for line in body.splitlines():
        match = _WIKILINK_ITEM.match(line)
        if not match:
            continue
        target = match.group(1)
        # vault-root path: archive/threads/<handle>/<dir-name>
        # compare basename to the set of real_dirs
        name = target.rsplit("/", 1)[-1]
        if name:
            out.add(name)
    return out


def audit_one(handle_dir: Path) -> dict[str, object]:
    idx_path = handle_dir / "index.md"
    real = {d.name for d in handle_dir.iterdir() if d.is_dir()}
    links = _index_links(idx_path)
    missing = sorted(real - links)
    stale = sorted(links - real)
    return {
        "handle": handle_dir.name,
        "has_index": idx_path.is_file(),
        "real": sorted(real),
        "links": sorted(links),
        "missing": missing,
        "stale": stale,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json", action="store_true", help="emit JSON instead of text"
    )
    parser.add_argument(
        "--vault",
        default=str(DEFAULT_VAULT),
        help=f"vault root (default: {DEFAULT_VAULT})",
    )
    args = parser.parse_args(argv)

    vault = Path(args.vault).resolve()
    threads_root = vault / "archive" / "threads"
    if not threads_root.is_dir():
        raise SystemExit(f"missing {threads_root}")

    reports: list[dict[str, object]] = []
    for entry in sorted(threads_root.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        reports.append(audit_one(entry))

    if args.json:
        print(json.dumps(reports, indent=2, ensure_ascii=False))
        return 0

    if not reports:
        print("no handles found")
        return 0

    max_handle = max(len(str(r["handle"])) for r in reports)
    flagged = 0
    for r in reports:
        handle = str(r["handle"]).ljust(max_handle)
        real_n = len(r["real"])
        link_n = len(r["links"])
        miss_n = len(r["missing"])
        stale_n = len(r["stale"])
        marker = ""
        if miss_n or stale_n:
            marker = "  ***"
            flagged += 1
        print(
            f"{handle}  real={real_n:<3}  links={link_n:<3}  "
            f"missing={miss_n:<3}  stale={stale_n}{marker}"
        )

    print()
    if flagged:
        print(f"flagged {flagged} handle(s):")
        for r in reports:
            if not (r["missing"] or r["stale"]):
                continue
            if r["missing"]:
                missing_sample = ", ".join(r["missing"][:5])
                if len(r["missing"]) > 5:
                    missing_sample += f", ... (+{len(r['missing']) - 5} more)"
                print(f"  {r['handle']}: missing_in_index = {missing_sample}")
            if r["stale"]:
                stale_sample = ", ".join(r["stale"])
                print(f"  {r['handle']}: stale_in_index = {stale_sample}")
    else:
        print("clean: no handle has missing or stale wikilinks")
    return 0


if __name__ == "__main__":
    sys.exit(main())