"""Merge non-orig media.json rows back after emit --force.

emit collect_media rewrites media.json with orig only. CRT / OCR files stay
on disk. Run this on the thread assets dir to restore those rows.

  python media_merge.py --thread C:\\projects\\Threadwell\\assets\\threads\\HANDLE\\DATE-SLUG
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from .media_manifest import (
        _from_wire_dict,
        _manifest_to_wire,
        atomic_write_json,
        upsert_derived_item,
    )
except ImportError:  # pragma: no cover - script-mode import
    from media_manifest import (
        _from_wire_dict,
        _manifest_to_wire,
        atomic_write_json,
        upsert_derived_item,
    )

ROLE_SUFFIX: dict[str, str] = {
    "_crt.png": "crt",
    "_crt_outline.png": "crt_outline",
    "_denoise.png": "denoise",
    "_ocr.txt": "ocr",
}


def role_of(name: str) -> str | None:
    """Map a filename suffix (``_crt.png``, ``_ocr.txt``, ...) to a media role label."""
    for suffix, role in ROLE_SUFFIX.items():
        if name.endswith(suffix):
            return role
    return None


def parse_ids(name: str) -> tuple[str, str]:
    """Extract ``(post_id, media_id)`` from a derived filename; returns ``("", stem)`` on mismatch."""
    stem = name
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
    if data.get("schema_version") != 2:
        raise SystemExit(
            "legacy media.json requires: tw.py migrate-media --id <id> --apply"
        )

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    items_raw = list(data.get("items") or [])
    have = {(str(i.get("filename") or ""), str(i.get("role") or "")) for i in items_raw}
    handles = {str(i.get("media_id") or ""): str(i.get("handle") or "") for i in items_raw}
    manifest = _from_wire_dict(data)
    added = 0
    for path in sorted(args.thread.iterdir()):
        role = role_of(path.name)
        if role is None:
            continue
        if (path.name, role) in have:
            continue
        post_id, media_id = parse_ids(path.name)
        handle = handles.get(media_id, "")
        manifest, _ = upsert_derived_item(
            manifest,
            post_id=post_id,
            media_id=media_id,
            handle=handle,
            role=role,
            filename=path.name,
            asset_dir=args.thread,
            now=now,
        )
        added += 1
        print(f"restore {path.name} role={role}")
    wire = _manifest_to_wire(manifest)
    wire["mirrors"] = list(data.get("mirrors") or [])
    atomic_write_json(media_path, wire)
    print(f"added {added} -> {media_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
