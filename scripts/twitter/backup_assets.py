"""Back up thread assets to a configured destination. Verifies every file."""

from __future__ import annotations

import json
import shutil
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

try:
    from .media_manifest import (
        _from_wire_dict,
        _manifest_to_wire,
        atomic_write_json,
        hash_file,
        inventory_digest,
        payload_inventory,
    )
    from .models import MediaManifest
except ImportError:  # pragma: no cover - script-mode import
    if str(Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from media_manifest import (
        _from_wire_dict,
        _manifest_to_wire,
        atomic_write_json,
        hash_file,
        inventory_digest,
        payload_inventory,
    )
    from models import MediaManifest


@dataclass(frozen=True)
class BackupResult:
    """Outcome of a single-thread backup attempt to one destination."""
    state: str
    destination: Path
    error: str | None


def load_destination_root(vault: Path, destination_id: str) -> Path:
    """Read the configured backup destination root from ``vault/secrets/config.toml``."""
    path = vault / "secrets" / "config.toml"
    if not path.is_file():
        raise RuntimeError(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    try:
        data = tomllib.loads(text)
        backup = data.get("backup") or {}
        configured_id = str(backup.get("id") or "cozy")
        root = str(backup.get("root") or "").strip()
    except tomllib.TOMLDecodeError:
        values: dict[str, str] = {}
        in_backup = False
        for raw in text.splitlines():
            line = raw.strip()
            if line.startswith("[") and line.endswith("]"):
                in_backup = line[1:-1].strip().lower() == "backup"
                continue
            if in_backup and "=" in line:
                key, _equals, remainder = line.partition("=")
                values[key.strip().lower()] = remainder.strip().strip("\"'")
        configured_id = values.get("id", "cozy")
        root = values.get("root", "")
    if configured_id != destination_id:
        raise RuntimeError(f"backup destination not configured: {destination_id}")
    if not root:
        raise RuntimeError("config.toml [backup] root is empty")
    return Path(root)


def backup_thread(
    asset_dir: Path,
    *,
    assets_root: Path,
    destination_root: Path,
    destination_id: str,
    now: str,
    require_destination_root: bool = False,
) -> BackupResult:
    """Mirror ``asset_dir`` into ``destination_root/<relative>`` and verify every payload by sha256."""
    media_path = asset_dir / "media.json"
    raw = json.loads(media_path.read_text(encoding="utf-8"))
    manifest = _from_wire_dict(raw)
    relative = asset_dir.relative_to(assets_root)
    destination = destination_root / relative
    inventory = payload_inventory(asset_dir, manifest)
    digest = inventory_digest(inventory)
    mirror: dict = {
        "destination_id": destination_id,
        "relative_path": relative.as_posix(),
        "state": "error",
        "inventory_digest": digest,
        "last_attempted_at": now,
        "completed_at": None,
        "verified_at": None,
        "error": None,
    }
    others = [
        entry
        for entry in raw.get("mirrors") or []
        if entry.get("destination_id") != destination_id
    ]
    try:
        if require_destination_root and not destination_root.is_dir():
            raise OSError("destination root unavailable")
        destination.mkdir(parents=True, exist_ok=True)
        for source in sorted(asset_dir.iterdir(), key=lambda path: path.name):
            if source.is_file():
                shutil.copy2(source, destination / source.name)
        for name, expected in inventory.items():
            if name == "media.json#canonical":
                continue
            copied = destination / name
            if not copied.is_file() or hash_file(copied) != expected:
                raise OSError(f"backup verification failed: {name}")
        mirror["state"] = "synced"
        mirror["completed_at"] = now
        mirror["verified_at"] = now
    except OSError as exc:
        text = str(exc)
        if str(destination_root) in text or str(destination) in text:
            mirror["error"] = "backup copy or verification failed"
        else:
            mirror["error"] = text[:300]
    raw["mirrors"] = others + [mirror]
    media_path.write_text(
        json.dumps(_manifest_to_wire_for_disk(manifest, raw), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    if mirror["state"] == "synced":
        shutil.copy2(media_path, destination / "media.json")
        if hash_file(media_path) != hash_file(destination / "media.json"):
            mirror["state"] = "error"
            mirror["error"] = "final manifest verification failed"
            media_path.write_text(
                json.dumps(_manifest_to_wire_for_disk(manifest, raw), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            return BackupResult("error", destination, mirror["error"])
    return BackupResult(mirror["state"], destination, mirror["error"])


def _manifest_to_wire_for_disk(manifest: MediaManifest, raw: dict) -> dict:
    """Merge typed manifest with the on-disk wire shape (incl. mirrors)."""
    typed_wire = _manifest_to_wire(manifest)
    typed_wire["mirrors"] = list(raw.get("mirrors") or [])
    return typed_wire
