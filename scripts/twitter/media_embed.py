"""Attach OCR transcripts under the cited origin media. Local variants are
not publication locations; visual selection is driven by the canonical
manifest's `embed` flag.

  python media_embed.py --thread <assets-thread-dir> --notes <archive-thread-dir> --media-id <id> --attach-ocr
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from .media_manifest import (
        _from_wire_dict,
        _item_to_wire,
        atomic_write_json,
        find_location,
        selected_url,
        validate_manifest,
    )
except ImportError:  # pragma: no cover - script-mode import
    if str(Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from media_manifest import (
        _from_wire_dict,
        _item_to_wire,
        atomic_write_json,
        find_location,
        selected_url,
        validate_manifest,
    )


OCR_DETAILS: str = "<summary>Text from still</summary>"


def ocr_block(text: str) -> str:
    body = text.strip("\n")
    return (
        "<details>\n"
        f"{OCR_DETAILS}\n"
        "\n"
        "```\n"
        f"{body}\n"
        "```\n"
        "\n"
        "</details>"
    )


def attach_ocr(notes_dir: Path, image_token: str, ocr_text: str) -> int:
    block = ocr_block(ocr_text)
    changed = 0
    for path in notes_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if image_token not in text:
            continue
        if OCR_DETAILS in text and image_token in text:
            print(f"ocr already near token in {path.name}")
            continue
        lines = text.splitlines(keepends=True)
        out: list[str] = []
        inserted = False
        for i, line in enumerate(lines):
            out.append(line)
            if image_token in line and not inserted:
                if not line.endswith("\n"):
                    out[-1] = line + "\n"
                out.append("\n")
                out.append(block + "\n")
                inserted = True
        if inserted:
            path.write_text("".join(out), encoding="utf-8")
            changed += 1
            print(f"attached ocr in {path.name}")
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thread", type=Path, required=True, help="assets/threads/.../ folder")
    parser.add_argument("--notes", type=Path, required=True, help="archive/threads/.../ folder")
    parser.add_argument("--media-id", required=True)
    parser.add_argument("--attach-ocr", action="store_true")
    args = parser.parse_args(argv)

    if args.show:
        raise SystemExit(
            "local variants are not publishable locations; after confirming an "
            "origin failure, use tw.py fallback with the desired --role"
        )
    if not args.attach_ocr:
        parser.print_help()
        return 2

    media_path = args.thread / "media.json"
    data = json.loads(media_path.read_text(encoding="utf-8"))
    manifest = _from_wire_dict(data)
    issues = validate_manifest(manifest)
    if issues:
        raise SystemExit(f"manifest invalid: {issues[0]}")

    raw_items: list[dict] = list(data.get("items") or [])
    target_dict: dict | None = None
    for item in raw_items:
        if (
            str(item.get("media_id") or "") == args.media_id
            and str(item.get("role") or "") == "ocr"
        ):
            target_dict = item
            break
    if target_dict is None:
        raise SystemExit(f"no role=ocr for {args.media_id}; run ocr_pass.py first")
    ocr_path = args.thread / str(target_dict.get("filename") or "")
    if not ocr_path.is_file():
        raise SystemExit(f"missing {ocr_path}")

    visible = None
    for item in manifest.items:
        if item.media_id != args.media_id:
            continue
        if item.embed and selected_url(item):
            visible = item
            break
    if visible is None:
        raise SystemExit("media group has no embedded origin")
    image_token = selected_url(visible) or ""
    if not image_token:
        raise SystemExit("media group has no selected HTTPS location")
    attach_ocr(args.notes, image_token, ocr_path.read_text(encoding="utf-8"))
    atomic_write_json(media_path, data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())