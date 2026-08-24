from __future__ import annotations

import copy
import json
import mimetypes
import os
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 2
VISUAL_ROLES = {"orig", "crt", "crt_outline", "denoise"}


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


def item_key(item: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(item.get("post_id") or ""),
        str(item.get("media_id") or ""),
        str(item.get("role") or ""),
    )


def find_location(item: dict[str, Any], location_id: str) -> dict[str, Any] | None:
    for location in item.get("locations") or []:
        if str(location.get("id") or "") == location_id:
            return location
    return None


def location_of_kind(item: dict[str, Any], kind: str) -> dict[str, Any] | None:
    for location in item.get("locations") or []:
        if location.get("kind") == kind:
            return location
    return None


def selected_location(item: dict[str, Any]) -> dict[str, Any] | None:
    publication = item.get("publication")
    if not isinstance(publication, dict):
        return None
    return find_location(item, str(publication.get("selected_location_id") or ""))


def selected_url(item: dict[str, Any]) -> str | None:
    location = selected_location(item)
    if not location or location.get("kind") not in {"origin", "fallback"}:
        return None
    value = str(location.get("url") or "")
    return value if value.startswith("https://") else None


def _media_type(filename: str) -> str:
    guessed, _encoding = mimetypes.guess_type(filename)
    return guessed or "application/octet-stream"


def _local_location(filename: str, local_path: Path, now: str) -> dict[str, Any]:
    present = local_path.is_file()
    return {
        "id": "local",
        "kind": "local",
        "path": filename,
        "sha256": hash_file(local_path) if present else None,
        "bytes": local_path.stat().st_size if present else None,
        "media_type": _media_type(filename),
        "integrity": "present" if present else "missing",
        "verified_at": now,
    }


def new_original_item(
    *,
    post_id: str,
    media_id: str,
    handle: str,
    origin_url: str,
    filename: str,
    local_path: Path,
    now: str,
) -> dict[str, Any]:
    return {
        "post_id": post_id,
        "media_id": media_id,
        "handle": handle,
        "role": "orig",
        "derived_from": None,
        "embed": True,
        "locations": [
            {
                "id": "origin:x",
                "kind": "origin",
                "provider": "x",
                "url": origin_url,
                "availability": "unknown",
                "checked_at": None,
                "check": None,
                "confirmed_unavailable_at": None,
            },
            _local_location(filename, local_path, now),
        ],
        "publication": {
            "selected_location_id": "origin:x",
            "selected_at": now,
            "reason": "default",
        },
    }


def merge_item(existing: dict[str, Any], fresh: dict[str, Any]) -> dict[str, Any]:
    if item_key(existing) != item_key(fresh):
        raise ValueError("cannot merge different media items")
    merged = copy.deepcopy(existing)
    merged["handle"] = fresh["handle"]
    existing_origin = location_of_kind(existing, "origin")
    fresh_origin = location_of_kind(fresh, "origin")
    if (
        existing_origin is not None
        and fresh_origin is not None
        and existing_origin.get("url") != fresh_origin.get("url")
    ):
        raise ValueError(f"origin URL changed for {item_key(existing)!r}")
    fresh_local = location_of_kind(fresh, "local")
    locations = [
        copy.deepcopy(location)
        for location in merged.get("locations") or []
        if location.get("kind") != "local"
    ]
    if fresh_local is not None:
        locations.append(copy.deepcopy(fresh_local))
    if location_of_kind(merged, "origin") is None:
        fresh_origin = location_of_kind(fresh, "origin")
        if fresh_origin is not None:
            locations.insert(0, copy.deepcopy(fresh_origin))
    merged["locations"] = locations
    if merged.get("publication") is None:
        merged["publication"] = copy.deepcopy(fresh.get("publication"))
    return merged


def merge_manifest_items(
    existing_items: list[dict[str, Any]],
    fresh_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    existing_by_key = {item_key(item): item for item in existing_items}
    fresh_keys: set[tuple[str, str, str]] = set()
    merged: list[dict[str, Any]] = []
    for fresh in fresh_items:
        key = item_key(fresh)
        fresh_keys.add(key)
        previous = existing_by_key.get(key)
        merged.append(merge_item(previous, fresh) if previous is not None else fresh)
    for previous in existing_items:
        if item_key(previous) not in fresh_keys:
            merged.append(copy.deepcopy(previous))
    return merged


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
) -> dict[str, Any]:
    return {
        "id": fallback_location_id(provider, url),
        "kind": "fallback",
        "provider": provider,
        "url": url,
        "sha256": content_hash,
        "recorded_at": recorded_at,
        "uploaded_at": uploaded_at,
        "availability": "unknown",
        "checked_at": None,
        "check": None,
    }


def new_derived_item(
    *,
    legacy: dict[str, Any],
    asset_dir: Path,
    now: str,
) -> dict[str, Any]:
    filename = str(legacy.get("filename") or "")
    post_id = str(legacy.get("post_id") or "")
    media_id = str(legacy.get("media_id") or "")
    role = str(legacy.get("role") or "")
    return {
        "post_id": post_id,
        "media_id": media_id,
        "handle": str(legacy.get("handle") or ""),
        "role": role,
        "derived_from": {
            "post_id": post_id,
            "media_id": media_id,
            "role": "orig",
        },
        "embed": False,
        "locations": [_local_location(filename, asset_dir / filename, now)],
        "publication": None,
    }


def upsert_derived_item(
    manifest: dict[str, Any],
    *,
    post_id: str,
    media_id: str,
    handle: str,
    role: str,
    filename: str,
    asset_dir: Path,
    now: str,
) -> dict[str, Any]:
    legacy_shape = {
        "post_id": post_id,
        "media_id": media_id,
        "handle": handle,
        "role": role,
        "filename": filename,
    }
    fresh = new_derived_item(legacy=legacy_shape, asset_dir=asset_dir, now=now)
    key = item_key(fresh)
    items = list(manifest.get("items") or [])
    for index, existing in enumerate(items):
        if item_key(existing) == key:
            fresh["locations"] = [
                location
                for location in existing.get("locations") or []
                if location.get("kind") != "local"
            ] + fresh["locations"]
            fresh["embed"] = bool(existing.get("embed"))
            fresh["publication"] = copy.deepcopy(existing.get("publication"))
            items[index] = fresh
            manifest["items"] = items
            return fresh
    items.append(fresh)
    manifest["items"] = items
    return fresh


def canonical_manifest_bytes(data: dict[str, Any]) -> bytes:
    stable = copy.deepcopy(data)
    stable["mirrors"] = []
    return (
        json.dumps(stable, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def payload_inventory(asset_dir: Path, manifest: dict[str, Any]) -> dict[str, str]:
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


def validate_manifest(data: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if data.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"schema_version must be {SCHEMA_VERSION}")
    if not str(data.get("root_post_id") or ""):
        issues.append("root_post_id is empty")
    seen: set[tuple[str, str, str]] = set()
    for index, item in enumerate(data.get("items") or []):
        key = item_key(item)
        if not all(key):
            issues.append(f"items[{index}] has incomplete key {key!r}")
        if key in seen:
            issues.append(f"items[{index}] duplicates key {key!r}")
        seen.add(key)
        location_ids: set[str] = set()
        for location in item.get("locations") or []:
            location_id = str(location.get("id") or "")
            if not location_id:
                issues.append(f"items[{index}] has empty location id")
            elif location_id in location_ids:
                issues.append(f"items[{index}] duplicates location {location_id}")
            location_ids.add(location_id)
        publication = item.get("publication")
        if publication is None:
            if item.get("role") in VISUAL_ROLES and item.get("embed"):
                issues.append(f"items[{index}] embeds without publication")
            continue
        selected_id = str(publication.get("selected_location_id") or "")
        location = find_location(item, selected_id)
        if location is None:
            issues.append(f"items[{index}] selects missing location {selected_id}")
        elif location.get("kind") not in {"origin", "fallback"}:
            issues.append(f"items[{index}] selects non-HTTPS location {selected_id}")
        elif not str(location.get("url") or "").startswith("https://"):
            issues.append(f"items[{index}] selects non-HTTPS location {selected_id}")
    return issues