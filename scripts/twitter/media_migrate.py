from __future__ import annotations

import copy
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

try:
    from .frozen import frozen_match
    from .media_manifest import (
        SCHEMA_VERSION,
        atomic_write_json,
        find_location,
        hash_file,
        new_derived_item,
        new_fallback_location,
        new_original_item,
        validate_manifest,
    )
    from .media_refs import apply_rewrite_plan, atomic_write_text, plan_thread_rewrites
except ImportError:  # pragma: no cover - script-mode import
    if str(Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from frozen import frozen_match
    from media_manifest import (
        SCHEMA_VERSION,
        atomic_write_json,
        find_location,
        hash_file,
        new_derived_item,
        new_fallback_location,
        new_original_item,
        validate_manifest,
    )
    from media_refs import apply_rewrite_plan, atomic_write_text, plan_thread_rewrites


@dataclass(frozen=True)
class MigrationResult:
    state: str
    changed: bool
    issues: tuple[str, ...]
    item_count: int


def media_id_from_url(url: str, index: int) -> str:
    segment = Path(unquote(urlparse(url).path)).name
    return segment if segment else f"m{index}"


def source_urls(thread_data: dict[str, Any]) -> dict[tuple[str, str], str]:
    result: dict[tuple[str, str], str] = {}
    for post in thread_data.get("posts") or []:
        post_id = str(post.get("post_id") or "")
        for index, url in enumerate(post.get("media_urls") or [], start=1):
            key = (post_id, media_id_from_url(str(url), index))
            if key in result and result[key] != url:
                raise ValueError(f"duplicate source mapping for {key!r}")
            result[key] = str(url)
    return result


def reference_maps(
    legacy: dict[str, Any], canonical: dict[str, Any]
) -> tuple[dict[str, str], dict[str, list[str]]]:
    canonical_by_key = {
        (
            str(item.get("post_id") or ""),
            str(item.get("media_id") or ""),
            str(item.get("role") or ""),
        ): item
        for item in canonical.get("items") or []
    }
    filename_origins: dict[str, str] = {}
    fallback_origins: dict[str, list[str]] = {}
    for old in legacy.get("items") or []:
        if old.get("role") != "orig":
            continue
        key = (
            str(old.get("post_id") or ""),
            str(old.get("media_id") or ""),
            "orig",
        )
        item = canonical_by_key[key]
        origin = next(
            location
            for location in item["locations"]
            if location.get("kind") == "origin"
        )["url"]
        filename_origins[str(old.get("filename") or "")] = origin
        old_url = str(old.get("url") or "")
        if old_url.startswith("https://"):
            fallback_origins.setdefault(old_url, []).append(origin)
    return filename_origins, fallback_origins


def corpus_inventory(
    assets_root: Path,
    note_root: Path,
    frozen_ids: set[str],
    *,
    now: str,
) -> dict[str, object]:
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
    threads: list[dict[str, object]] = []
    frozen_hashes: dict[str, str] = {}
    for media_path in media_paths:
        asset_dir = media_path.parent
        relative = asset_dir.relative_to(assets_root).as_posix()
        match = frozen_match(asset_dir, frozen_ids)
        legacy = json.loads(media_path.read_text(encoding="utf-8"))
        is_legacy = legacy.get("schema_version") != SCHEMA_VERSION
        legacy_items = list(legacy.get("items") or [])
        unique_legacy = {
            (
                str(item.get("post_id") or ""),
                str(item.get("media_id") or ""),
                str(item.get("role") or ""),
            )
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
        thread_data = json.loads(thread_data_path.read_text(encoding="utf-8"))
        try:
            canonical, issues = canonical_from_legacy(legacy, thread_data, asset_dir, now)
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
        counts["migratable"] += len(canonical["items"])
        thread_entry: dict[str, object] = {
            "relative": relative,
            "state": "migratable" if is_legacy else "current",
            "item_count": len(canonical["items"]),
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
    legacy: dict[str, Any],
    thread_data: dict[str, Any],
    asset_dir: Path,
    now: str,
) -> tuple[dict[str, Any], tuple[str, ...]]:
    sources = source_urls(thread_data)
    items: list[dict[str, Any]] = []
    issues: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    for old in legacy.get("items") or []:
        role = str(old.get("role") or "")
        post_id = str(old.get("post_id") or "")
        media_id = str(old.get("media_id") or "")
        filename = str(old.get("filename") or "")
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
                handle=str(old.get("handle") or ""),
                origin_url=origin_url,
                filename=filename,
                local_path=asset_dir / filename,
                now=now,
            )
            old_url = str(old.get("url") or "")
            if old_url.startswith("https://"):
                local = find_location(item, "local")
                item["locations"].append(
                    new_fallback_location(
                        provider="catbox",
                        url=old_url,
                        content_hash=str(local.get("sha256") or "") or None,
                        recorded_at=now,
                        uploaded_at=None,
                    )
                )
            items.append(item)
        elif role in {"crt", "crt_outline", "denoise", "ocr"}:
            item = new_derived_item(legacy=old, asset_dir=asset_dir, now=now)
            old_url = str(old.get("url") or "")
            if old_url.startswith("https://"):
                local = find_location(item, "local")
                item["locations"].append(
                    new_fallback_location(
                        provider="catbox",
                        url=old_url,
                        content_hash=str(local.get("sha256") or "") or None,
                        recorded_at=now,
                        uploaded_at=None,
                    )
                )
            items.append(item)
        else:
            issues.append(f"invalid legacy role: {post_id}/{media_id}/{role}")
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "root_post_id": str(legacy.get("root_post_id") or ""),
        "items": items,
        "mirrors": copy.deepcopy(legacy.get("mirrors") or []),
    }
    issues.extend(validate_manifest(manifest))
    return manifest, tuple(issues)


def migrate_legacy_thread(
    asset_dir: Path,
    note_dir: Path,
    *,
    now: str,
    apply: bool,
) -> MigrationResult:
    media_path = asset_dir / "media.json"
    legacy = json.loads(media_path.read_text(encoding="utf-8"))
    if legacy.get("schema_version") == SCHEMA_VERSION:
        return MigrationResult("current", False, (), len(legacy.get("items") or []))
    thread_data = json.loads((asset_dir / "thread_data.json").read_text(encoding="utf-8"))
    canonical, issues = canonical_from_legacy(legacy, thread_data, asset_dir, now)
    if issues:
        return MigrationResult("blocked", False, issues, len(legacy.get("items") or []))
    if apply:
        filename_origins, fallback_origins = reference_maps(legacy, canonical)
        plan = plan_thread_rewrites(
            note_dir,
            filename_origins=filename_origins,
            fallback_origins=fallback_origins,
        )
        if plan.issues:
            return MigrationResult("blocked", False, plan.issues, len(legacy.get("items") or []))
        note_backup: dict[Path, str] = {}
        try:
            for rewrite in plan.files:
                note_backup[rewrite.path] = rewrite.before
            atomic_write_json(media_path, canonical)
            apply_rewrite_plan(plan)
        except Exception:
            for path, before in note_backup.items():
                atomic_write_text(path, before)
            raise
    return MigrationResult("migratable", apply, (), len(legacy.get("items") or []))