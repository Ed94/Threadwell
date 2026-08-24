"""Frozen-id helpers: refuse writes to threads matching the do-not-refetch list."""
from __future__ import annotations

import json
from pathlib import Path


def load_frozen_ids(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def captured_ids(asset_dir: Path) -> set[str]:
    found: set[str] = set()
    media_path = asset_dir / "media.json"
    if media_path.is_file():
        media = json.loads(media_path.read_text(encoding="utf-8"))
        root_id = str(media.get("root_post_id") or "")
        if root_id:
            found.add(root_id)
        for item in media.get("items") or []:
            post_id = str(item.get("post_id") or "")
            if post_id:
                found.add(post_id)
    thread_path = asset_dir / "thread_data.json"
    if thread_path.is_file():
        thread = json.loads(thread_path.read_text(encoding="utf-8"))
        root_id = str(thread.get("root_post_id") or "")
        if root_id:
            found.add(root_id)
        for post in thread.get("posts") or []:
            post_id = str(post.get("post_id") or "")
            if post_id:
                found.add(post_id)
    return found


def frozen_match(asset_dir: Path, frozen_ids: set[str]) -> str | None:
    matches = sorted(captured_ids(asset_dir) & frozen_ids)
    return matches[0] if matches else None


def require_writable(asset_dir: Path, frozen_ids: set[str]) -> None:
    match = frozen_match(asset_dir, frozen_ids)
    if match is not None:
        raise SystemExit(f"frozen: skipped ({match})")