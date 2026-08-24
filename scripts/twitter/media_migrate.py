"""Migrate per-thread media.json from legacy wire shape to canonical v2."""
from __future__ import annotations

import copy
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

try:
    from .frozen import frozen_match
    from .media_manifest import (
        SCHEMA_VERSION,
        _from_wire_dict,
        _item_to_wire,
        atomic_write_json,
        find_location,
        hash_file,
        location_of_kind,
        new_derived_item,
        new_fallback_location,
        new_original_item,
        selected_url,
        validate_manifest,
    )
    from .media_refs import apply_rewrite_plan, atomic_write_text, plan_thread_rewrites
    from .models import LegacyMediaJson, LegacyThreadData, MediaItem, MediaManifest
except ImportError:  # pragma: no cover - script-mode import
    if str(Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from frozen import frozen_match
    from media_manifest import (
        SCHEMA_VERSION,
        _from_wire_dict,
        _item_to_wire,
        atomic_write_json,
        find_location,
        hash_file,
        location_of_kind,
        new_derived_item,
        new_fallback_location,
        new_original_item,
        selected_url,
        validate_manifest,
    )
    from media_refs import apply_rewrite_plan, atomic_write_text, plan_thread_rewrites
    from models import LegacyMediaJson, LegacyThreadData, MediaItem, MediaManifest


@dataclass(frozen=True)
class MigrationResult:
    """Outcome of a per-thread legacy-to-canonical media.json migration.

    ``state`` is one of ``current``, ``migratable``, ``blocked``. ``changed``
    reports whether the apply pass wrote files. ``issues`` collects any
    blocking findings; ``item_count`` echoes the number of legacy items
    inspected.
    """
    state: str
    changed: bool
    issues: tuple[str, ...]
    item_count: int


def media_id_from_url(url: str, index: int) -> str:
    segment = Path(unquote(urlparse(url).path)).name
    return segment if segment else f"m{index}"


def source_urls(thread_data: LegacyThreadData) -> dict[tuple[str, str], str]:
    """Map ``(post_id, media_id)`` to the original provider URL for each media reference.

    Reads the post-level ``media_urls`` list from the typed ``LegacyThreadData``
    and indexes each URL by a media id derived from its filename segment.
    """
    result: dict[tuple[str, str], str] = {}
    for post in thread_data.posts:
        post_id = post.post_id
        for index, url in enumerate(post.media_urls, start=1):
            key = (post_id, media_id_from_url(url, index))
            if key in result and result[key] != url:
                raise ValueError(f"duplicate source mapping for {key!r}")
            result[key] = url
    return result


def reference_maps(
    legacy: LegacyMediaJson, canonical: MediaManifest
) -> tuple[dict[str, str], dict[str, list[str]]]:
    """Build ``(filename → origin URL)`` and ``(legacy URL → origin URLs)`` maps for rewrite planning.

    The filename map rewrites note references that still point at the local
    file basename. The fallback URL map rewrites notes that still cite the
    pre-migration fallback host.
    """
    canonical_by_key: dict[tuple[str, str, str], MediaItem] = {}
    for item in canonical.items:
        key = (item.post_id, item.media_id, item.kind or item.role or "")
        canonical_by_key[key] = item
    filename_origins: dict[str, str] = {}
    fallback_origins: dict[str, list[str]] = {}
    for old in legacy.items:
        if (old.role or old.kind or "") != "orig":
            continue
        key = (old.post_id, old.media_id, "orig")
        item = canonical_by_key[key]
        origin = next(location for location in item.locations if location.kind == "origin")
        filename_origins[old.filename or ""] = origin.url or ""
        old_url = old.url or ""
        if old_url.startswith("https://"):
            fallback_origins.setdefault(old_url, []).append(origin.url or "")
    return filename_origins, fallback_origins


def corpus_inventory(
    assets_root: Path,
    note_root: Path,
    frozen_ids: set[str],
    *,
    now: str,
) -> dict:
    """Walk the corpus and produce a typed-shape inventory ``dict`` (output of this function).

    The inventory is a different document than ``media.json``; it is emitted
    to disk as JSON, not consumed as ``LegacyMediaJson``. Internally, every
    media.json read is parsed into ``LegacyMediaJson`` at the boundary.
    """
    media_paths = sorted(assets_root.rglob("media.json"))
    counts: dict[str, int] = {
        "input_items": 0,
        "migratable": 0,
        "frozen_skipped": 0,
        "missing_origin_mapping": 0,
        "missing_local_file": 0,
        "ambiguous_note_reference": 0,
        "invalid_legacy_row": 0,
    }
    threads: list[dict] = []
    frozen_hashes: dict[str, str] = {}
    for media_path in media_paths:
        asset_dir = media_path.parent
        relative = asset_dir.relative_to(assets_root).as_posix()
        match = frozen_match(asset_dir, frozen_ids)
        legacy = LegacyMediaJson.from_dict(json.loads(media_path.read_text(encoding="utf-8")))
        is_legacy = legacy.schema_version != SCHEMA_VERSION
        legacy_items = list(legacy.items)
        unique_legacy: set[tuple[str, str, str]] = {
            (item.post_id, item.media_id, item.role or item.kind or "")
            for item in legacy_items
        }
        counts["input_items"] += len(unique_legacy)
        for path in sorted(asset_dir.iterdir()):
            if path.is_file() and path.name != "media.json":
                key = f"{relative}/{path.name}"
                frozen_hashes[key] = hash_file(path)
        for archive in sorted((note_root / relative).glob("*.md")) if (note_root / relative).is_dir() else []:
            key = f"{relative}/{archive.name}"
            frozen_hashes[key] = hash_file(archive)
        if match is not None:
            counts["frozen_skipped"] += len(unique_legacy)
            threads.append({
                "relative": relative,
                "state": "frozen_skipped",
                "frozen_id": match,
                "item_count": len(unique_legacy),
            })
            continue
        thread_data_path = asset_dir / "thread_data.json"
        if not thread_data_path.is_file():
            counts["missing_origin_mapping"] += len(unique_legacy)
            threads.append({
                "relative": relative,
                "state": "missing_origin_mapping",
                "item_count": len(unique_legacy),
                "issues": ["missing thread_data.json"],
            })
            continue
        thread_data = LegacyThreadData.from_dict(
            json.loads(thread_data_path.read_text(encoding="utf-8"))
        )
        try:
            canonical_manifest, issues = canonical_from_legacy(legacy, thread_data, asset_dir, now)
        except Exception as exc:
            counts["invalid_legacy_row"] += len(unique_legacy)
            threads.append({
                "relative": relative,
                "state": "invalid_legacy_row",
                "item_count": len(unique_legacy),
                "issues": [str(exc)],
            })
            continue
        if issues:
            counts["invalid_legacy_row"] += len(unique_legacy)
            threads.append({
                "relative": relative,
                "state": "invalid_legacy_row",
                "item_count": len(unique_legacy),
                "issues": list(issues),
            })
            continue
        counts["migratable"] += len(canonical_manifest.items)
        thread_entry: dict = {
            "relative": relative,
            "state": "migratable" if is_legacy else "current",
            "item_count": len(canonical_manifest.items),
        }
        threads.append(thread_entry)
    expected_total = (
        counts["migratable"]
        + counts["frozen_skipped"]
        + counts["missing_origin_mapping"]
        + counts["missing_local_file"]
        + counts["ambiguous_note_reference"]
        + counts["invalid_legacy_row"]
    )
    if counts["input_items"] != expected_total:
        raise SystemExit("corpus accounting mismatch")
    return {
        "schema_version": 1,
        "generated_at": now,
        "counts": counts,
        "threads": threads,
        "frozen_hashes": frozen_hashes,
    }


def canonical_from_legacy(
    legacy: LegacyMediaJson,
    thread_data: LegacyThreadData,
    asset_dir: Path,
    now: str,
) -> tuple[MediaManifest, tuple[str, ...]]:
    """Build a canonical ``MediaManifest`` from a legacy ``LegacyMediaJson`` + ``LegacyThreadData``.

    Each legacy item produces a single canonical ``MediaItem``. Legacy
    ``orig`` items gain a fallback ``MediaLocation`` if they already cited
    the pre-migration fallback host on the wire.
    """
    sources = source_urls(thread_data)
    items: list[MediaItem] = []
    issues: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    for old in legacy.items:
        role = old.role or old.kind or ""
        post_id = old.post_id
        media_id = old.media_id
        filename = old.filename or ""
        handle = old.handle or ""
        old_url = old.url or ""
        key = (post_id, media_id, role)
        if key in seen:
            continue
        seen.add(key)
        if role == "orig":
            origin_url = sources.get((post_id, media_id))
            if origin_url is None:
                issues.append(f"missing origin mapping: {post_id}/{media_id}")
                continue
            item = new_original_item(
                post_id=post_id,
                media_id=media_id,
                handle=handle,
                origin_url=origin_url,
                filename=filename,
                local_path=asset_dir / filename,
                now=now,
            )
            if old_url.startswith("https://"):
                local = find_location(item, "local")
                sha = local.sha256 if local is not None else None
                item = MediaItem(
                    post_id=item.post_id,
                    media_id=item.media_id,
                    kind=item.kind,
                    role=item.role,
                    handle=item.handle,
                    embed=item.embed,
                    locations=item.locations
                    + (
                        new_fallback_location(
                            provider="catbox",
                            url=old_url,
                            content_hash=sha or None,
                            recorded_at=now,
                            uploaded_at=None,
                        ),
                    ),
                    publication=item.publication,
                    derived_from=item.derived_from,
                    caption=item.caption,
                )
            items.append(item)
        elif role in {"crt", "crt_outline", "denoise", "ocr"}:
            item = new_derived_item(
                post_id=post_id,
                media_id=media_id,
                handle=handle,
                role=role,
                filename=filename,
                asset_dir=asset_dir,
                now=now,
            )
            if old_url.startswith("https://"):
                local = find_location(item, "local")
                sha = local.sha256 if local is not None else None
                item = MediaItem(
                    post_id=item.post_id,
                    media_id=item.media_id,
                    kind=item.kind,
                    role=item.role,
                    handle=item.handle,
                    embed=item.embed,
                    locations=item.locations
                    + (
                        new_fallback_location(
                            provider="catbox",
                            url=old_url,
                            content_hash=sha or None,
                            recorded_at=now,
                            uploaded_at=None,
                        ),
                    ),
                    publication=item.publication,
                    derived_from=item.derived_from,
                    caption=item.caption,
                )
            items.append(item)
        else:
            issues.append(f"invalid legacy role: {post_id}/{media_id}/{role}")
    manifest = MediaManifest(
        schema_version=SCHEMA_VERSION,
        root_post_id=legacy.root_post_id,
        items=tuple(items),
    )
    issues.extend(validate_manifest(manifest))
    return manifest, tuple(issues)


def migrate_legacy_thread(
    asset_dir: Path,
    note_dir: Path,
    *,
    now: str,
    apply: bool,
) -> MigrationResult:
    """Migrate a per-thread ``media.json`` to the canonical v2 shape in place.

    Returns a ``MigrationResult`` describing the outcome (``current``,
    ``blocked``, ``migratable``). When ``apply`` is False, no files are
    written; when True, the canonical manifest is atomically written and
    the corresponding note references are rewritten with rollback on
    failure.
    """
    media_path = asset_dir / "media.json"
    legacy = LegacyMediaJson.from_dict(json.loads(media_path.read_text(encoding="utf-8")))
    if legacy.schema_version == SCHEMA_VERSION:
        return MigrationResult("current", False, (), len(legacy.items))
    thread_data = LegacyThreadData.from_dict(
        json.loads((asset_dir / "thread_data.json").read_text(encoding="utf-8"))
    )
    canonical, issues = canonical_from_legacy(legacy, thread_data, asset_dir, now)
    if issues:
        return MigrationResult("blocked", False, issues, len(legacy.items))
    if apply:
        filename_origins, fallback_origins = reference_maps(legacy, canonical)
        plan = plan_thread_rewrites(
            note_dir,
            filename_origins=filename_origins,
            fallback_origins=fallback_origins,
        )
        if plan.issues:
            return MigrationResult("blocked", False, plan.issues, len(legacy.items))
        note_backup: dict[Path, str] = {}
        try:
            for rewrite in plan.files:
                note_backup[rewrite.path] = rewrite.before
            atomic_write_json(
                media_path,
                _manifest_to_wire_shape(canonical, legacy),
            )
            apply_rewrite_plan(plan)
        except Exception:
            for path, before in note_backup.items():
                atomic_write_text(path, before)
            raise
    return MigrationResult("migratable", apply, (), len(legacy.items))


def _manifest_to_wire_shape(
    manifest: MediaManifest, legacy: LegacyMediaJson
) -> dict:
    """Convert a typed manifest back to a wire-shape dict for atomic_write_json.

    Carries forward legacy mirrors (typed MediaManifest doesn't model
    mirrors). Mirrors are written as a list to preserve wire compatibility
    with downstream producers (the typed view keys them by destination id).
    """
    mirrors_out: list = []
    if legacy.mirrors is not None:
        mirrors_out = list(copy.deepcopy(legacy.mirrors).values())
    out: dict = {
        "schema_version": manifest.schema_version,
        "root_post_id": manifest.root_post_id,
        "items": [_item_to_wire(item) for item in manifest.items],
        "mirrors": mirrors_out,
    }
    if manifest.captured_at is not None:
        out["captured_at"] = manifest.captured_at
    return out
