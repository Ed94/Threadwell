from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from .frozen import frozen_match
    from .media_manifest import (
        find_location,
        hash_file,
        inventory_digest,
        item_key,
        payload_inventory,
        selected_url,
        validate_manifest,
    )
    from .media_refs import remote_markup
except ImportError:  # pragma: no cover - script-mode import
    if str(Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from frozen import frozen_match
    from media_manifest import (
        find_location,
        hash_file,
        inventory_digest,
        item_key,
        payload_inventory,
        selected_url,
        validate_manifest,
    )
    from media_refs import remote_markup


@dataclass(frozen=True)
class AuditReport:
    frozen: bool
    issues: tuple[str, ...]


def audit_local_item(item: dict[str, Any], asset_dir: Path) -> str | None:
    local = find_location(item, "local")
    if local is None:
        return f"{'/'.join(item_key(item))} missing local location"
    path = asset_dir / str(local.get("path") or "")
    if not path.is_file():
        return f"{'/'.join(item_key(item))} local missing"
    if path.stat().st_size != local.get("bytes") or hash_file(path) != local.get("sha256"):
        return f"{'/'.join(item_key(item))} local mismatch"
    return None


def classify_origin_response(status: int | None, detail: str, checked_at: str) -> dict[str, Any]:
    available = status is not None and 200 <= status < 400
    return {
        "checked_at": checked_at,
        "status": status,
        "result": "available" if available else "error",
        "detail": detail[:200],
        "confirms_unavailable": False,
    }


def check_origin_url(
    url: str,
    checked_at: str,
    opener: Any = urlopen,
) -> dict[str, Any]:
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


def record_origin_check(item: dict[str, Any], outcome: dict[str, Any]) -> None:
    origin = find_location(item, "origin:x")
    if origin is None:
        raise ValueError("item has no origin:x location")
    origin["checked_at"] = outcome["checked_at"]
    origin["check"] = {
        "status": outcome["status"],
        "result": outcome["result"],
        "detail": outcome["detail"],
    }
    if outcome["result"] == "available":
        origin["availability"] = "available"


def audit_thread(
    asset_dir: Path,
    note_dir: Path,
    frozen_ids: set[str],
) -> AuditReport:
    match = frozen_match(asset_dir, frozen_ids)
    if match is not None:
        return AuditReport(True, (f"frozen: skipped ({match})",))
    manifest = json.loads((asset_dir / "media.json").read_text(encoding="utf-8"))
    issues = list(validate_manifest(manifest))
    for item in manifest.get("items") or []:
        if find_location(item, "local") is not None:
            issue = audit_local_item(item, asset_dir)
            if issue is not None:
                issues.append(issue)

    expected = Counter(
        remote_markup(url)
        for item in manifest.get("items") or []
        if item.get("embed") and (url := selected_url(item)) is not None
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
    for mirror in manifest.get("mirrors") or []:
        if mirror.get("state") == "synced" and mirror.get("inventory_digest") != current_digest:
            issues.append(f"mirror stale: {mirror.get('destination_id')}")
    return AuditReport(False, tuple(sorted(set(issues))))