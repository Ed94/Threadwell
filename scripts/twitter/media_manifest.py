"""Canonical media manifest: boundary parsing, validation, and wire round-trip."""
from __future__ import annotations

import copy
import json
import mimetypes
import os
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

try:
    from .models import (
        DerivedFromRef,
        MediaItem,
        MediaLocation,
        MediaLocationCheck,
        MediaManifest,
        Publication,
    )
except ImportError:  # pragma: no cover - script-mode import
    from models import (
        DerivedFromRef,
        MediaItem,
        MediaLocation,
        MediaLocationCheck,
        MediaManifest,
        Publication,
    )


SCHEMA_VERSION: int = 2
VISUAL_ROLES: set[str] = {"orig", "crt", "crt_outline", "denoise"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def hash_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temp.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def _from_wire_dict(raw: dict[str, Any]) -> MediaManifest:
    """Boundary parser: turn a wire-shape dict into a typed MediaManifest."""
    return MediaManifest.from_dict(raw)


def _from_wire_item(raw: dict[str, Any]) -> MediaItem:
    """Boundary parser: turn a wire-shape dict into a typed MediaItem."""
    return MediaItem.from_dict(raw)


def _from_wire_items(raw: list[dict[str, Any]]) -> tuple[MediaItem, ...]:
    """Boundary parser: turn a wire-shape items list into typed items."""
    return tuple(MediaItem.from_dict(item) for item in raw)


def item_key(item: MediaItem) -> tuple[str, str, str]:
    return (item.post_id, item.media_id, item.kind or item.role or "")


def find_location(item: MediaItem, location_id: str) -> MediaLocation | None:
    for location in item.locations:
        if location.id == location_id:
            return location
    return None


def location_of_kind(item: MediaItem, kind: str) -> MediaLocation | None:
    for location in item.locations:
        if location.kind == kind:
            return location
    return None


def selected_location(item: MediaItem) -> MediaLocation | None:
    publication = item.publication
    if publication is None:
        return None
    return find_location(item, publication.selected_location_id)


def selected_url(item: MediaItem) -> str | None:
    location = selected_location(item)
    if location is None or location.kind not in {"origin", "fallback"}:
        return None
    value = location.url or ""
    return value if value.startswith("https://") else None


def _media_type(filename: str) -> str:
    guessed, _encoding = mimetypes.guess_type(filename)
    return guessed or "application/octet-stream"


def _local_location(filename: str, local_path: Path, now: str) -> MediaLocation:
    present = local_path.is_file()
    return MediaLocation(
        id="local",
        kind="local",
        local_path=Path(filename),
        sha256=hash_file(local_path) if present else None,
        bytes=local_path.stat().st_size if present else None,
        media_type=_media_type(filename),
        integrity="present" if present else "missing",
        verified_at=now,
    )


def new_original_item(
    *,
    post_id: str,
    media_id: str,
    handle: str,
    origin_url: str,
    filename: str,
    local_path: Path,
    now: str,
) -> MediaItem:
    return MediaItem(
        post_id=post_id,
        media_id=media_id,
        handle=handle,
        kind="orig",
        role="orig",
        embed=True,
        locations=(
            MediaLocation(
                id="origin:x",
                kind="origin",
                provider="x",
                url=origin_url,
                availability="unknown",
            ),
            _local_location(filename, local_path, now),
        ),
        publication=Publication(
            selected_location_id="origin:x",
            selected_at=now,
            reason="default",
        ),
    )


def merge_item(existing: MediaItem, fresh: MediaItem) -> MediaItem:
    if item_key(existing) != item_key(fresh):
        raise ValueError("cannot merge different media items")
    fresh_handle = fresh.handle or existing.handle
    existing_origin = location_of_kind(existing, "origin")
    fresh_origin = location_of_kind(fresh, "origin")
    if (
        existing_origin is not None
        and fresh_origin is not None
        and existing_origin.url != fresh_origin.url
    ):
        raise ValueError(f"origin URL changed for {item_key(existing)!r}")
    fresh_local = location_of_kind(fresh, "local")
    locations: list[MediaLocation] = [
        copy.deepcopy(location)
        for location in existing.locations
        if location.kind != "local"
    ]
    if fresh_local is not None:
        locations.append(copy.deepcopy(fresh_local))
    if location_of_kind(existing, "origin") is None and fresh_origin is not None:
        locations.insert(0, copy.deepcopy(fresh_origin))
    merged = MediaItem(
        post_id=existing.post_id,
        media_id=existing.media_id,
        kind=existing.kind,
        role=existing.role,
        handle=fresh_handle,
        embed=existing.embed,
        locations=tuple(locations),
        publication=existing.publication
        if existing.publication is not None
        else copy.deepcopy(fresh.publication),
    )
    return merged


def merge_manifest_items(
    existing_items: tuple[MediaItem, ...],
    fresh_items: tuple[MediaItem, ...],
) -> tuple[MediaItem, ...]:
    existing_by_key: dict[tuple[str, str, str], MediaItem] = {
        item_key(item): item for item in existing_items
    }
    fresh_keys: set[tuple[str, str, str]] = set()
    merged: list[MediaItem] = []
    for fresh in fresh_items:
        key = item_key(fresh)
        fresh_keys.add(key)
        previous = existing_by_key.get(key)
        merged.append(merge_item(previous, fresh) if previous is not None else fresh)
    for previous in existing_items:
        if item_key(previous) not in fresh_keys:
            merged.append(copy.deepcopy(previous))
    return tuple(merged)


def fallback_location_id(provider: str, url: str) -> str:
    digest = sha256(f"{provider}\0{url}".encode("utf-8")).hexdigest()[:16]
    return f"fallback:{provider}:{digest}"


def new_fallback_location(
    *,
    provider: str,
    url: str,
    content_hash: str | None,
    recorded_at: str,
    uploaded_at: str | None,
) -> MediaLocation:
    return MediaLocation(
        id=fallback_location_id(provider, url),
        kind="fallback",
        provider=provider,
        url=url,
        sha256=content_hash,
        recorded_at=recorded_at,
        uploaded_at=uploaded_at,
        availability="unknown",
    )


def new_derived_item(
    *,
    post_id: str,
    media_id: str,
    handle: str,
    role: str,
    filename: str,
    asset_dir: Path,
    now: str,
) -> MediaItem:
    """Construct a MediaItem for a derived file (crt / crt_outline / denoise / ocr)."""
    return MediaItem(
        post_id=post_id,
        media_id=media_id,
        handle=handle,
        kind=role,
        role=role,
        derived_from=DerivedFromRef(
            post_id=post_id,
            media_id=media_id,
            role="orig",
        ),
        embed=False,
        locations=(_local_location(filename, asset_dir / filename, now),),
        publication=None,
    )


def upsert_derived_item(
    manifest: MediaManifest,
    *,
    post_id: str,
    media_id: str,
    handle: str,
    role: str,
    filename: str,
    asset_dir: Path,
    now: str,
) -> tuple[MediaManifest, MediaItem]:
    """Insert or update a derived item. Returns (manifest, item)."""
    fresh = new_derived_item(
        post_id=post_id,
        media_id=media_id,
        handle=handle,
        role=role,
        filename=filename,
        asset_dir=asset_dir,
        now=now,
    )
    key = item_key(fresh)
    items: list[MediaItem] = list(manifest.items)
    for index, existing in enumerate(items):
        if item_key(existing) == key:
            kept = tuple(loc for loc in existing.locations if loc.kind != "local")
            updated = MediaItem(
                post_id=fresh.post_id,
                media_id=fresh.media_id,
                kind=fresh.kind,
                role=fresh.role,
                handle=fresh.handle,
                embed=existing.embed,
                derived_from=fresh.derived_from,
                locations=kept + fresh.locations,
                publication=copy.deepcopy(existing.publication),
            )
            items[index] = updated
            new_manifest = MediaManifest(
                root_post_id=manifest.root_post_id,
                items=tuple(items),
                schema_version=manifest.schema_version,
                captured_at=manifest.captured_at,
            )
            return new_manifest, updated
    items.append(fresh)
    new_manifest = MediaManifest(
        root_post_id=manifest.root_post_id,
        items=tuple(items),
        schema_version=manifest.schema_version,
        captured_at=manifest.captured_at,
    )
    return new_manifest, fresh


def _item_to_wire(item: MediaItem) -> dict[str, Any]:
    """Convert a typed MediaItem back into a wire-shape dict for round-tripping to disk."""
    locations: list[dict[str, Any]] = []
    for loc in item.locations:
        location_dict: dict[str, Any] = {"kind": loc.kind}
        if loc.id is not None:
            location_dict["id"] = loc.id
        if loc.local_path is not None:
            location_dict["path"] = str(loc.local_path)
        if loc.url is not None:
            location_dict["url"] = loc.url
        if loc.bytes is not None:
            location_dict["bytes"] = loc.bytes
        if loc.sha256 is not None:
            location_dict["sha256"] = loc.sha256
        if loc.media_type is not None:
            location_dict["media_type"] = loc.media_type
        if loc.integrity is not None:
            location_dict["integrity"] = loc.integrity
        if loc.verified_at is not None:
            location_dict["verified_at"] = loc.verified_at
        if loc.provider is not None:
            location_dict["provider"] = loc.provider
        if loc.availability is not None:
            location_dict["availability"] = loc.availability
        if loc.checked_at is not None:
            location_dict["checked_at"] = loc.checked_at
        if loc.checked_status is not None:
            location_dict["checked_status"] = loc.checked_status
        if loc.recorded_at is not None:
            location_dict["recorded_at"] = loc.recorded_at
        if loc.uploaded_at is not None:
            location_dict["uploaded_at"] = loc.uploaded_at
        if loc.confirmed_unavailable_at is not None:
            location_dict["confirmed_unavailable_at"] = loc.confirmed_unavailable_at
        if loc.check is not None:
            location_dict["check"] = {
                "status": loc.check.status,
                "result": loc.check.result,
                "detail": loc.check.detail,
            }
        locations.append(location_dict)
    out: dict[str, Any] = {
        "post_id": item.post_id,
        "media_id": item.media_id,
        "locations": locations,
    }
    if item.kind is not None:
        out["kind"] = item.kind
    if item.handle is not None:
        out["handle"] = item.handle
    if item.role is not None:
        out["role"] = item.role
    if item.embed is not None:
        out["embed"] = item.embed
    if item.caption is not None:
        out["caption"] = item.caption
    if item.derived_from is not None:
        out["derived_from"] = {
            "post_id": item.derived_from.post_id,
            "media_id": item.derived_from.media_id,
            "role": item.derived_from.role,
        }
    if item.publication is not None:
        out["publication"] = {
            "selected_location_id": item.publication.selected_location_id,
            "selected_at": item.publication.selected_at,
            "reason": item.publication.reason,
        }
    return out


def _manifest_to_wire(manifest: MediaManifest) -> dict[str, Any]:
    """Convert a typed MediaManifest back into a wire-shape dict for JSON serialization.

    Schema version, root_post_id, items, captured_at are copied through;
    mirrors are reset to [] (per the original canonical_manifest_bytes contract).
    """
    out: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "root_post_id": manifest.root_post_id,
        "items": [_item_to_wire(item) for item in manifest.items],
        "mirrors": [],
    }
    if manifest.captured_at is not None:
        out["captured_at"] = manifest.captured_at
    return out


def canonical_manifest_bytes(manifest: MediaManifest) -> bytes:
    stable = _manifest_to_wire(manifest)
    return (
        json.dumps(stable, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def payload_inventory(asset_dir: Path, manifest: MediaManifest) -> dict[str, str]:
    inventory: dict[str, str] = {
        "media.json#canonical": sha256(canonical_manifest_bytes(manifest)).hexdigest()
    }
    for path in sorted(asset_dir.iterdir(), key=lambda candidate: candidate.name):
        if path.is_file() and path.name != "media.json":
            inventory[path.name] = hash_file(path)
    return inventory


def inventory_digest(inventory: dict[str, str]) -> str:
    encoded = json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()


def validate_manifest(manifest: MediaManifest) -> list[str]:
    issues: list[str] = []
    if manifest.schema_version != SCHEMA_VERSION:
        issues.append(f"schema_version must be {SCHEMA_VERSION}")
    if not manifest.root_post_id:
        issues.append("root_post_id is empty")
    seen: set[tuple[str, str, str]] = set()
    for index, item in enumerate(manifest.items):
        key = item_key(item)
        if not all(key):
            issues.append(f"items[{index}] has incomplete key {key!r}")
        if key in seen:
            issues.append(f"items[{index}] duplicates key {key!r}")
        seen.add(key)
        location_ids: set[str] = set()
        for location in item.locations:
            location_id = location.id or ""
            if not location_id:
                issues.append(f"items[{index}] has empty location id")
            elif location_id in location_ids:
                issues.append(f"items[{index}] duplicates location {location_id}")
            location_ids.add(location_id)
        publication = item.publication
        if publication is None:
            role = item.kind or item.role or ""
            if role in VISUAL_ROLES and item.embed:
                issues.append(f"items[{index}] embeds without publication")
            continue
        location = find_location(item, publication.selected_location_id)
        if location is None:
            issues.append(
                f"items[{index}] selects missing location {publication.selected_location_id}"
            )
        elif location.kind not in {"origin", "fallback"}:
            issues.append(
                f"items[{index}] selects non-HTTPS location {publication.selected_location_id}"
            )
        elif location.url is None or not location.url.startswith("https://"):
            issues.append(
                f"items[{index}] selects non-HTTPS location {publication.selected_location_id}"
            )
    return issues
