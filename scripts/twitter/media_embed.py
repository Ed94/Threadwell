"""Select which still a note cites, and optionally attach OCR under it.

Notes currently say:

  Media (not lifted): `1736…_GBgHT…_orig.png`

After lift they will say:

  ![](https://files.catbox.moe/xxxx.png)

This script only rewrites those two shapes. It does not upload.

  python media_embed.py --thread <assets-thread-dir> --notes <archive-thread-dir> --media-id GBgHT_2WIAAKuNq --show crt
  python media_embed.py --thread <assets-thread-dir> --notes <archive-thread-dir> --media-id GBgHT_2WIAAKuNq --attach-ocr
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

IMAGE_MD = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LIFTED_LINE = re.compile(r"^Media \(not lifted\): (.+)$", re.M)


def load_media(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_media(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def group_items(items: list[dict]) -> dict[tuple[str, str], dict[str, dict]]:
    groups: dict[tuple[str, str], dict[str, dict]] = {}
    for item in items:
        key = (str(item.get("post_id") or ""), str(item.get("media_id") or ""))
        groups.setdefault(key, {})[str(item.get("role") or "")] = item
    return groups


def set_embed(items: list[dict], media_id: str, show: str) -> None:
    found = False
    for item in items:
        if str(item.get("media_id") or "") != media_id:
            continue
        if item.get("role") in ("orig", "crt", "crt_outline"):
            item["embed"] = item.get("role") == show
            found = True
    if not found:
        raise SystemExit(f"no orig/crt row for media_id {media_id}")


def token_for(item: dict) -> str:
    url = item.get("url")
    if url:
        return str(url)
    return str(item.get("filename") or "")


def rewrite_notes(notes_dir: Path, old: str, new: str) -> int:
    if not old or old == new:
        return 0
    changed = 0
    for path in notes_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if old not in text:
            continue
        path.write_text(text.replace(old, new), encoding="utf-8")
        changed += 1
        print(f"rewrote {path.name}")
    return changed


def ocr_block(text: str) -> str:
    body = text.strip("\n")
    return (
        "<details>\n"
        "<summary>Text from still</summary>\n"
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
        if "<summary>Text from still</summary>" in text and image_token in text:
            print(f"ocr already near token in {path.name}")
            continue
        # After the line that cites the still.
        lines = text.splitlines(keepends=True)
        out: list[str] = []
        i = 0
        inserted = False
        while i < len(lines):
            out.append(lines[i])
            if image_token in lines[i] and not inserted:
                if not lines[i].endswith("\n"):
                    out[-1] = lines[i] + "\n"
                out.append("\n")
                out.append(block + "\n")
                inserted = True
            i += 1
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
    parser.add_argument("--show", choices=("orig", "crt"), default=None)
    parser.add_argument("--attach-ocr", action="store_true")
    args = parser.parse_args(argv)

    media_path = args.thread / "media.json"
    data = load_media(media_path)
    items = data["items"]
    groups = group_items(items)
    match = None
    pair = None
    for key, roles in groups.items():
        if key[1] == args.media_id:
            match = key
            pair = roles
            break
    if pair is None or match is None:
        raise SystemExit(f"media_id {args.media_id} not in {media_path}")

    if args.show:
        if args.show not in pair:
            raise SystemExit(f"no role={args.show} for {args.media_id}")
        old_item = next((pair[r] for r in ("crt", "orig") if pair.get(r, {}).get("embed")), None)
        if old_item is None:
            old_item = pair.get("orig") or pair.get("crt")
        set_embed(items, args.media_id, args.show)
        save_media(media_path, data)
        new_item = pair[args.show]
        rewrite_notes(args.notes, token_for(old_item), token_for(new_item))
        print(f"embed {args.media_id} -> {args.show} ({token_for(new_item)})")

    if args.attach_ocr:
        ocr = pair.get("ocr")
        if ocr is None:
            raise SystemExit(f"no role=ocr for {args.media_id}; run ocr_pass.py first")
        ocr_path = args.thread / str(ocr["filename"])
        if not ocr_path.is_file():
            raise SystemExit(f"missing {ocr_path}")
        shown = next((pair[r] for r in ("crt", "orig") if pair.get(r, {}).get("embed")), None)
        if shown is None:
            shown = pair.get("orig") or pair.get("crt")
        attach_ocr(args.notes, token_for(shown), ocr_path.read_text(encoding="utf-8"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
