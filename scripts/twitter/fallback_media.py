from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

try:
    from .media_manifest import (
        atomic_write_json,
        find_location,
        hash_file,
        new_fallback_location,
        selected_url,
    )
    from .media_refs import atomic_write_text, remote_markup
except ImportError:  # pragma: no cover - script-mode import
    if str(Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from media_manifest import (
        atomic_write_json,
        find_location,
        hash_file,
        new_fallback_location,
        selected_url,
    )
    from media_refs import atomic_write_text, remote_markup


@dataclass(frozen=True)
class FallbackResult:
    url: str
    reused: bool


def replace_selected_url(note_dir: Path, old_url: str, new_url: str) -> None:
    if old_url == new_url:
        return
    old_markup = remote_markup(old_url)
    new_markup = remote_markup(new_url)
    hits: list[Path] = []
    for path in note_dir.glob("*.md"):
        if old_markup in path.read_text(encoding="utf-8"):
            hits.append(path)
    total = sum(path.read_text(encoding="utf-8").count(old_markup) for path in hits)
    if total != 1:
        if total == 0 and sum(
            path.read_text(encoding="utf-8").count(new_markup)
            for path in note_dir.glob("*.md")
        ) == 1:
            return
        raise ValueError("selected origin reference not found exactly once")
    path = hits[0]
    text = path.read_text(encoding="utf-8")
    atomic_write_text(path, text.replace(old_markup, new_markup, 1))


def _group(manifest: dict[str, Any], media_id: str) -> list[dict[str, Any]]:
    return [
        item
        for item in manifest.get("items") or []
        if str(item.get("media_id") or "") == media_id
    ]


def _one(items: list[dict[str, Any]], role: str) -> dict[str, Any]:
    matches = [item for item in items if item.get("role") == role]
    if len(matches) != 1:
        raise ValueError(f"expected one role={role}, found {len(matches)}")
    return matches[0]


def _verified_local(item: dict[str, Any], asset_dir: Path) -> tuple[Path, str]:
    local = find_location(item, "local")
    if local is None or local.get("integrity") != "present":
        raise ValueError("selected item has no present local location")
    path = asset_dir / str(local.get("path") or "")
    expected = str(local.get("sha256") or "")
    if not path.is_file() or not expected or hash_file(path) != expected:
        raise ValueError("selected local file failed hash verification")
    return path, expected


def activate_fallback(
    asset_dir: Path,
    note_dir: Path,
    *,
    media_id: str,
    role: str,
    provider: str,
    confirm_origin_unavailable: bool,
    now: str,
    upload: Callable[[Path], str],
    lookup: Callable[[str, str], str | None] | None = None,
) -> FallbackResult:
    if not confirm_origin_unavailable:
        raise ValueError("origin-unavailable confirmation is required")
    media_path = asset_dir / "media.json"
    manifest = json.loads(media_path.read_text(encoding="utf-8"))
    group = _group(manifest, media_id)
    original = _one(group, "orig")
    target = _one(group, role)
    origin = find_location(original, "origin:x")
    if origin is None:
        raise ValueError("original item has no X origin location")
    old_url = selected_url(next((item for item in group if item.get("embed")), original))
    if old_url is None:
        raise ValueError("media group has no selected HTTPS location")
    local_path, content_hash = _verified_local(target, asset_dir)
    origin["availability"] = "unavailable"
    origin["confirmed_unavailable_at"] = now

    fallback = next(
        (
            location
            for location in target.get("locations") or []
            if location.get("kind") == "fallback"
            and location.get("provider") == provider
            and location.get("sha256") == content_hash
        ),
        None,
    )
    reused = fallback is not None
    if fallback is None and lookup is not None:
        reused_url = lookup(provider, content_hash)
        if reused_url is not None:
            fallback = new_fallback_location(
                provider=provider,
                url=reused_url,
                content_hash=content_hash,
                recorded_at=now,
                uploaded_at=None,
            )
            target.setdefault("locations", []).append(fallback)
            reused = True
    if fallback is None:
        url = upload(local_path)
        fallback = new_fallback_location(
            provider=provider,
            url=url,
            content_hash=content_hash,
            recorded_at=now,
            uploaded_at=now,
        )
        target.setdefault("locations", []).append(fallback)

    atomic_write_json(media_path, manifest)
    replace_selected_url(note_dir, old_url, str(fallback["url"]))
    for item in group:
        item["embed"] = item is target
    target["publication"] = {
        "selected_location_id": fallback["id"],
        "selected_at": now,
        "reason": "origin-unavailable",
    }
    atomic_write_json(media_path, manifest)
    return FallbackResult(str(fallback["url"]), reused)


def find_existing_fallback(
    assets_root: Path,
    provider: str,
    content_hash: str,
) -> str | None:
    urls: set[str] = set()
    for media_path in assets_root.rglob("media.json"):
        data = json.loads(media_path.read_text(encoding="utf-8"))
        if data.get("schema_version") != 2:
            continue
        for item in data.get("items") or []:
            for location in item.get("locations") or []:
                if (
                    location.get("kind") == "fallback"
                    and location.get("provider") == provider
                    and location.get("sha256") == content_hash
                    and str(location.get("url") or "").startswith("https://")
                ):
                    urls.add(str(location["url"]))
    return sorted(urls)[0] if urls else None


def restore_origin(
    asset_dir: Path,
    note_dir: Path,
    *,
    media_id: str,
    now: str,
) -> None:
    media_path = asset_dir / "media.json"
    manifest = json.loads(media_path.read_text(encoding="utf-8"))
    group = _group(manifest, media_id)
    original = _one(group, "orig")
    origin = find_location(original, "origin:x")
    if origin is None:
        raise ValueError("original item has no X origin location")
    visible = next((item for item in group if item.get("embed")), original)
    old_url = selected_url(visible)
    new_url = str(origin.get("url") or "")
    if old_url is None or not new_url.startswith("https://"):
        raise ValueError("media group has no restorable origin")
    replace_selected_url(note_dir, old_url, new_url)
    origin["availability"] = "available"
    origin["checked_at"] = now
    origin["check"] = {
        "status": None,
        "result": "available",
        "detail": "manual restore-origin selection",
    }
    for item in group:
        item["embed"] = item is original
    original["publication"] = {
        "selected_location_id": "origin:x",
        "selected_at": now,
        "reason": "manual",
    }
    atomic_write_json(media_path, manifest)