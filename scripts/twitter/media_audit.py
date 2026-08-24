"""Audit per-thread media manifest: local integrity, note refs, mirror freshness, origin probes."""
from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import dataclass, replace
from http.client import HTTPResponse
from pathlib import Path
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from .frozen import frozen_match
    from .media_manifest import (
        _from_wire_dict,
        find_location,
        hash_file,
        inventory_digest,
        item_key,
        payload_inventory,
        selected_url,
        validate_manifest,
    )
    from .media_refs import remote_markup
    from .models import LegacyMediaJson, MediaItem, MediaLocation, MediaLocationCheck, MediaManifest, OriginCheck
except ImportError:  # pragma: no cover - script-mode import
    if str(Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from frozen import frozen_match
    from media_manifest import (
        _from_wire_dict,
        find_location,
        hash_file,
        inventory_digest,
        item_key,
        payload_inventory,
        selected_url,
        validate_manifest,
    )
    from media_refs import remote_markup
    from models import (
        LegacyMediaJson,
        MediaItem,
        MediaLocation,
        MediaLocationCheck,
        MediaManifest,
        OriginCheck,
    )


@dataclass(frozen=True)
class AuditReport:
    """Outcome of a per-thread media audit: frozen flag plus blocking issues."""
    frozen: bool
    issues: tuple[str, ...]


def audit_local_item(item: MediaItem, asset_dir: Path) -> str | None:
    local = find_location(item, "local")
    if local is None:
        return f"{'/'.join(item_key(item))} missing local location"
    filename = str(local.local_path) if local.local_path is not None else ""
    path = asset_dir / filename
    if not path.is_file():
        return f"{'/'.join(item_key(item))} local missing"
    sha_expected = local.sha256 or ""
    bytes_expected = local.bytes
    if bytes_expected is not None and path.stat().st_size != bytes_expected:
        return f"{'/'.join(item_key(item))} local mismatch"
    if hash_file(path) != sha_expected:
        return f"{'/'.join(item_key(item))} local mismatch"
    return None


def classify_origin_response(status: int | None, detail: str, checked_at: str) -> OriginCheck:
    """Build an ``OriginCheck`` from an HTTP probe status + detail string.

    The detail string is truncated to 200 chars so the persisted check
    does not bloat the manifest. ``confirms_unavailable`` is always False
    here; callers that detect a definitive unavailability set it True.
    """
    available = status is not None and 200 <= status < 400
    return OriginCheck(
        checked_at=checked_at,
        status=status,
        result="available" if available else "error",
        detail=detail[:200],
        confirms_unavailable=False,
    )


def check_origin_url(
    url: str,
    checked_at: str,
    opener: Callable[..., HTTPResponse] = urlopen,
) -> OriginCheck:
    """Probe ``url`` with HEAD and return a typed ``OriginCheck``.

    ``opener`` is variadic because ``urlopen`` accepts both ``url`` and
    ``Request`` shapes with different keyword argument sets; callers
    passing a custom opener can match either.
    """
    request = Request(url, method="HEAD", headers={"User-Agent": "Threadwell-media-audit/1"})
    try:
        with opener(request, timeout=30) as response:
            return classify_origin_response(
                int(response.status),
                "HEAD completed",
                checked_at,
            )
    except HTTPError as exc:
        return classify_origin_response(exc.code, f"HTTP {exc.code}", checked_at)
    except (URLError, TimeoutError, OSError) as exc:
        return classify_origin_response(None, type(exc).__name__, checked_at)


def record_origin_check(
    manifest: LegacyMediaJson, item_index: int, outcome: OriginCheck
) -> LegacyMediaJson:
    """Return a new ``LegacyMediaJson`` with the origin check at ``item_index`` persisted.

    The input ``LegacyMediaJson`` is frozen, so the update is a
    round-trip: each affected ``MediaItem`` is reconstructed with the
    updated ``MediaLocation`` for ``origin:x`` carrying the check
    metadata. Returns the new manifest; the caller is responsible for
    serializing it back to disk.
    """
    items = list(manifest.items)
    if not (0 <= item_index < len(items)):
        raise ValueError("item_index out of range")
    item = items[item_index]
    new_locations: list[MediaLocation] = []
    found_origin = False
    for location in item.locations:
        if location.id == "origin:x":
            found_origin = True
            new_availability = (
                "available"
                if outcome.result == "available"
                else location.availability
            )
            new_locations.append(
                replace(
                    location,
                    availability=new_availability,
                    checked_at=outcome.checked_at,
                    checked_status=outcome.status,
                    check=MediaLocationCheck(
                        status=outcome.status,
                        result=outcome.result,
                        detail=outcome.detail,
                    ),
                )
            )
        else:
            new_locations.append(location)
    if not found_origin:
        raise ValueError("item has no origin:x location")
    items[item_index] = replace(item, locations=tuple(new_locations))
    return replace(manifest, items=tuple(items))


def audit_thread(
    asset_dir: Path,
    note_dir: Path,
    frozen_ids: set[str],
) -> AuditReport:
    """Audit a single thread's media manifest + note references.

    Reads ``media.json`` at the boundary into ``LegacyMediaJson`` (for the
    opaque mirrors blob) and a typed ``MediaManifest`` (for item /
    location validation). Reports issues with the local file presence,
    note reference counts, and mirror staleness.
    """
    match = frozen_match(asset_dir, frozen_ids)
    if match is not None:
        return AuditReport(True, (f"frozen: skipped ({match})",))
    manifest_dict = json.loads((asset_dir / "media.json").read_text(encoding="utf-8"))
    legacy = LegacyMediaJson.from_dict(manifest_dict)
    manifest = _from_wire_dict(manifest_dict)
    issues: list[str] = list(validate_manifest(manifest))
    for item in manifest.items:
        if find_location(item, "local") is not None:
            issue = audit_local_item(item, asset_dir)
            if issue is not None:
                issues.append(issue)

    expected = Counter(
        remote_markup(url or "")
        for item in manifest.items
        if item.embed and (url := selected_url(item)) is not None
    )
    note_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(note_dir.glob("*.md"))
    )
    for markup, count in expected.items():
        actual = note_text.count(markup)
        if actual != count:
            issues.append(
                f"selected reference count mismatch: {markup} expected={count} actual={actual}"
            )

    current_digest = inventory_digest(payload_inventory(asset_dir, manifest))
    for mirror in (legacy.mirrors or {}).values():
        if mirror.get("state") == "synced" and mirror.get("inventory_digest") != current_digest:
            issues.append(f"mirror stale: {mirror.get('destination_id')}")
    return AuditReport(False, tuple(sorted(set(issues))))
