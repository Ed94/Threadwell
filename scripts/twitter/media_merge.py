"""Merge non-orig media.json rows back after emit --force.

emit collect_media rewrites media.json with orig only. CRT / OCR files stay
on disk. Run this on the thread assets dir to restore those rows.

  python media_merge.py --thread C:\\projects\\Threadwell\\assets\\threads\\HANDLE\\DATE-SLUG
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROLE_SUFFIX = {
    "_crt.png": "crt",
    "_crt_outline.png": "crt_outline",
    "_denoise.png": "denoise",
    "_ocr.txt": "ocr",
}


def role_of(name: str) -> str | None:
    for suffix, role in ROLE_SUFFIX.items():
        if name.endswith(suffix):
            return role
    return None


def parse_ids(name: str) -> tuple[str, str]:
    stem = name
    for suffix in ROLE_SUFFIX:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    if stem.endswith("_orig"):
        stem = stem[: -len("_orig")]
    parts = stem.split("_", 1)
    if len(parts) != 2:
        return "", stem
    return parts[0], parts[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thread", type=Path, required=True)
    args = parser.parse_args(argv)
    media_path = args.thread / "media.json"
    data = json.loads(media_path.read_text(encoding="utf-8"))
    items = list(data.get("items") or [])
    have = {(i.get("filename"), i.get("role")) for i in items}
    added = 0
    for path in sorted(args.thread.iterdir()):
        role = role_of(path.name)
        if role is None:
            continue
        if (path.name, role) in have:
            continue
        post_id, media_id = parse_ids(path.name)
        handle = ""
        for item in items:
            if item.get("media_id") == media_id:
                handle = str(item.get("handle") or "")
                break
        items.append({
            "post_id": post_id,
            "media_id": media_id,
            "handle": handle,
            "role": role,
            "filename": path.name,
            "publish": False,
            "url": None,
            "embed": False,
        })
        added += 1
        print(f"restore {path.name} role={role}")
    data["items"] = items
    media_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"added {added} -> {media_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
