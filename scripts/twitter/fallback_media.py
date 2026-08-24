"""Activate, restore, and dedupe fallback media locations for a thread."""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

try:
    from .media_manifest import (
        _from_wire_dict,
        _item_to_wire,
        atomic_write_json,
        find_location,
        hash_file,
        new_fallback_location,
        selected_url,
    )
    from .media_refs import atomic_write_text, remote_markup
    from .models import (
        MediaItem,
        MediaLocation,
        MediaLocationCheck,
        MediaManifest,
        Publication,
    )
except ImportError:  # pragma: no cover - script-mode import
    if str(Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from media_manifest import (
        _from_wire_dict,
        _item_to_wire,
        atomic_write_json,
        find_location,
        hash_file,
        new_fallback_location,
        selected_url,
    )
    from media_refs import atomic_write_text, remote_markup
    from models import (
        MediaItem,
        MediaLocation,
        MediaLocationCheck,
        MediaManifest,
        Publication,
    )


@dataclass(frozen=True)
class FallbackResult:
    """Outcome of activating one fallback location for a media item."""
    url: str
    reused: bool


def replace_selected_url(note_dir: Path, old_url: str, new_url: str) -> None:
    """Swap ``old_url`` for ``new_url`` in exactly one note under ``note_dir`` (no-op if already swapped)."""
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


def _group(manifest: MediaManifest, media_id: str) -> list[MediaItem]:
    """Return the slice of ``manifest.items`` sharing a media_id (orig + derived variants)."""
    return [item for item in manifest.items if item.media_id == media_id]


def _one(items: list[MediaItem], role: str) -> MediaItem:
    """Return the single item in ``items`` whose ``kind`` matches ``role`` (raises otherwise)."""
    matches = [item for item in items if item.kind == role]
    if len(matches) != 1:
        raise ValueError(f"expected one role={role}, found {len(matches)}")
    return matches[0]


def _verified_local(item: MediaItem, asset_dir: Path) -> tuple[Path, str]:
    """Return ``(local_path, sha256)`` of ``item``'s local location, verified against its declared hash."""
    local = find_location(item, "local")
    if local is None or local.integrity != "present":
        raise ValueError("selected item has no present local location")
    filename = str(local.local_path) if local.local_path is not None else ""
    path = asset_dir / filename
    expected = local.sha256 or ""
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
    """Activate a fallback URL for ``media_id``: upload (or reuse) and update manifest + note references."""
    if not confirm_origin_unavailable:
        raise ValueError("origin-unavailable confirmation is required")
    media_path = asset_dir / "media.json"
    raw = json.loads(media_path.read_text(encoding="utf-8"))
    manifest: MediaManifest = _from_wire_dict(raw)
    group = _group(manifest, media_id)
    original = _one(group, "orig")
    target = _one(group, role)
    origin = find_location(original, "origin:x")
    if origin is None:
        raise ValueError("original item has no X origin location")
    visible = next((item for item in group if item.embed), original)
    old_url = selected_url(visible)
    if old_url is None:
        raise ValueError("media group has no selected HTTPS location")
    local_path, content_hash = _verified_local(target, asset_dir)
    target = _with_origin_unavailable(target, origin, now)

    fallback = next(
        (
            location
            for location in target.locations
            if location.kind == "fallback"
            and location.provider == provider
            and location.sha256 == content_hash
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
            target = _append_location(target, fallback)
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
        target = _append_location(target, fallback)

    manifest = _with_replaced_item(manifest, target)
    atomic_write_json(media_path, _manifest_to_wire_shape(manifest, raw))
    assert fallback.url is not None
    replace_selected_url(note_dir, old_url, fallback.url)
    manifest = _with_item_attr(manifest, target.post_id, target.media_id, "embed", True)
    manifest = _with_publication(
        manifest,
        target,
        Publication(
            selected_location_id=fallback.id or "",
            selected_at=now,
            reason="origin-unavailable",
        ),
    )
    atomic_write_json(media_path, _manifest_to_wire_shape(manifest, raw))
    return FallbackResult(str(fallback.url or ""), reused)


def _with_origin_unavailable(item: MediaItem, origin: MediaLocation, now: str) -> MediaItem:
    """Return a copy of `item` with the matching origin location marked unavailable."""
    new_locations: list[MediaLocation] = []
    for location in item.locations:
        if location.id == origin.id:
            new_locations.append(
                MediaLocation(
                    kind=location.kind,
                    id=location.id,
                    local_path=location.local_path,
                    url=location.url,
                    bytes=location.bytes,
                    sha256=location.sha256,
                    media_type=location.media_type,
                    integrity=location.integrity,
                    verified_at=location.verified_at,
                    provider=location.provider,
                    availability="unavailable",
                    checked_at=location.checked_at,
                    checked_status=location.checked_status,
                    recorded_at=location.recorded_at,
                    uploaded_at=location.uploaded_at,
                    confirmed_unavailable_at=now,
                    check=location.check,
                )
            )
        else:
            new_locations.append(location)
    return _copy_item_with(item, locations=tuple(new_locations))


def _append_location(item: MediaItem, location: MediaLocation) -> MediaItem:
    return _copy_item_with(item, locations=item.locations + (location,))


def _copy_item_with(item: MediaItem, **changes: Any) -> MediaItem:
    return MediaItem(
        post_id=changes.get("post_id", item.post_id),
        media_id=changes.get("media_id", item.media_id),
        kind=changes.get("kind", item.kind),
        role=changes.get("role", item.role),
        handle=changes.get("handle", item.handle),
        embed=changes.get("embed", item.embed),
        caption=changes.get("caption", item.caption),
        derived_from=changes.get("derived_from", item.derived_from),
        publication=changes.get("publication", item.publication),
        locations=changes.get("locations", item.locations),
    )


def _with_replaced_item(manifest: MediaManifest, replacement: MediaItem) -> MediaManifest:
    new_items: list[MediaItem] = []
    for existing in manifest.items:
        if existing.post_id == replacement.post_id and existing.media_id == replacement.media_id:
            new_items.append(replacement)
        else:
            new_items.append(existing)
    return MediaManifest(
        root_post_id=manifest.root_post_id,
        items=tuple(new_items),
        schema_version=manifest.schema_version,
        captured_at=manifest.captured_at,
    )


def _with_item_attr(
    manifest: MediaManifest,
    post_id: str,
    media_id: str,
    attr: str,
    value: Any,
) -> MediaManifest:
    new_items: list[MediaItem] = []
    for existing in manifest.items:
        if existing.post_id == post_id and existing.media_id == media_id:
            new_items.append(_copy_item_with(existing, **{attr: value}))
        else:
            new_items.append(existing)
    return MediaManifest(
        root_post_id=manifest.root_post_id,
        items=tuple(new_items),
        schema_version=manifest.schema_version,
        captured_at=manifest.captured_at,
    )


def _with_publication(
    manifest: MediaManifest,
    item: MediaItem,
    publication: Publication,
) -> MediaManifest:
    new_items: list[MediaItem] = []
    for existing in manifest.items:
        if existing.post_id == item.post_id and existing.media_id == item.media_id:
            new_items.append(_copy_item_with(existing, publication=publication))
        else:
            new_items.append(existing)
    return MediaManifest(
        root_post_id=manifest.root_post_id,
        items=tuple(new_items),
        schema_version=manifest.schema_version,
        captured_at=manifest.captured_at,
    )


def _manifest_to_wire_shape(manifest: MediaManifest, raw: dict) -> dict:
    out: dict = {
        "schema_version": manifest.schema_version or 2,
        "root_post_id": manifest.root_post_id,
        "items": [_item_to_wire(item) for item in manifest.items],
        "mirrors": list(raw.get("mirrors") or []),
    }
    if manifest.captured_at is not None:
        out["captured_at"] = manifest.captured_at
    return out


def find_existing_fallback(
    assets_root: Path,
    provider: str,
    content_hash: str,
) -> str | None:
    """Scan every thread's media.json for a fallback URL with matching sha256; returns the first or ``None``."""
    urls: set[str] = set()
    urls: set[str] = set()
    for media_path in assets_root.rglob("media.json"):
        raw = json.loads(media_path.read_text(encoding="utf-8"))
        if raw.get("schema_version") != 2:
            continue
        manifest = _from_wire_dict(raw)
        for item in manifest.items:
            for location in item.locations:
                if (
                    location.kind == "fallback"
                    and location.provider == provider
                    and location.sha256 == content_hash
                    and (location.url or "").startswith("https://")
                ):
                    urls.add(location.url or "")
    return sorted(urls)[0] if urls else None


def restore_origin(
    asset_dir: Path,
    note_dir: Path,
    *,
    media_id: str,
    now: str,
) -> None:
    """Switch the visible location for ``media_id`` back to its X origin and rewrite the note references."""
    media_path = asset_dir / "media.json"
    media_path = asset_dir / "media.json"
    raw = json.loads(media_path.read_text(encoding="utf-8"))
    manifest = _from_wire_dict(raw)
    group = _group(manifest, media_id)
    original = _one(group, "orig")
    origin = find_location(original, "origin:x")
    if origin is None:
        raise ValueError("original item has no X origin location")
    visible = next((item for item in group if item.embed), original)
    old_url = selected_url(visible)
    new_url = origin.url or ""
    if old_url is None or not new_url.startswith("https://"):
        raise ValueError("media group has no restorable origin")
    replace_selected_url(note_dir, old_url, new_url)
    new_locations: list[MediaLocation] = []
    for location in original.locations:
        if location.id == origin.id:
            new_locations.append(
                MediaLocation(
                    kind=location.kind,
                    id=location.id,
                    local_path=location.local_path,
                    url=location.url,
                    bytes=location.bytes,
                    sha256=location.sha256,
                    media_type=location.media_type,
                    integrity=location.integrity,
                    verified_at=location.verified_at,
                    provider=location.provider,
                    availability="available",
                    checked_at=now,
                    checked_status=location.checked_status,
                    recorded_at=location.recorded_at,
                    uploaded_at=location.uploaded_at,
                    confirmed_unavailable_at=location.confirmed_unavailable_at,
                    check=MediaLocationCheck(
                        status=None,
                        result="available",
                        detail="manual restore-origin selection",
                    ),
                )
            )
        else:
            new_locations.append(location)
    manifest = _with_replaced_item(
        manifest, _copy_item_with(original, locations=tuple(new_locations))
    )
    new_items: list[MediaItem] = []
    for existing in manifest.items:
        if existing.post_id == original.post_id and existing.media_id == original.media_id:
            new_items.append(_copy_item_with(existing, embed=True))
        else:
            new_items.append(_copy_item_with(existing, embed=False))
    manifest = MediaManifest(
        root_post_id=manifest.root_post_id,
        items=tuple(new_items),
        schema_version=manifest.schema_version,
        captured_at=manifest.captured_at,
    )
    manifest = _with_publication(
        manifest,
        original,
        Publication(
            selected_location_id="origin:x",
            selected_at=now,
            reason="manual",
        ),
    )
    atomic_write_json(media_path, _manifest_to_wire_shape(manifest, raw))
