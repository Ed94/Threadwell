from __future__ import annotations

import json
from pathlib import Path


NOW = "2026-08-24T12:00:00Z"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def legacy_thread(asset_dir: Path, note_dir: Path) -> tuple[Path, Path]:
    asset_dir.mkdir(parents=True, exist_ok=True)
    note_dir.mkdir(parents=True, exist_ok=True)
    original = asset_dir / "100_AAA_orig.png"
    original.write_bytes(b"png fixture bytes")
    write_json(
        asset_dir / "thread_data.json",
        {
            "root_post_id": "100",
            "source_url": "https://x.com/example/status/100",
            "posts": [
                {
                    "post_id": "100",
                    "author": "Example",
                    "handle": "example",
                    "text": "Fixture post",
                    "timestamp": "2026-08-24 12:00:00",
                    "media_urls": [
                        "https://pbs.twimg.com/media/AAA?format=png&name=orig"
                    ],
                    "reply_to_id": None,
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": 1,
                    },
                }
            ],
        },
    )
    write_json(
        asset_dir / "media.json",
        {
            "root_post_id": "100",
            "items": [
                {
                    "post_id": "100",
                    "media_id": "AAA",
                    "handle": "example",
                    "role": "orig",
                    "filename": original.name,
                    "publish": True,
                    "url": "https://files.catbox.moe/fallback.png",
                    "embed": True,
                }
            ],
        },
    )
    (note_dir / "index.md").write_text(
        "---\npost_id: \"100\"\ndraft: false\n---\n\n"
        "**1/**\n\nFixture post\n\n"
        "![](https://files.catbox.moe/fallback.png)\n",
        encoding="utf-8",
        newline="\n",
    )
    return asset_dir, note_dir