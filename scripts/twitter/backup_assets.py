from __future__ import annotations

import json
import shutil
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

try:
    from .media_manifest import (
        atomic_write_json,
        hash_file,
        inventory_digest,
        payload_inventory,
    )
except ImportError:  # pragma: no cover - script-mode import
    if str(Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from media_manifest import (
        atomic_write_json,
        hash_file,
        inventory_digest,
        payload_inventory,
    )


@dataclass(frozen=True)
class BackupResult:
    state: str
    destination: Path
    error: str | None


def load_destination_root(vault: Path, destination_id: str) -> Path:
    path = vault / "secrets" / "credentials.toml"
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
        raise RuntimeError("credentials.toml [backup] root is empty")
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
    media_path = asset_dir / "media.json"
    manifest = json.loads(media_path.read_text(encoding="utf-8"))
    relative = asset_dir.relative_to(assets_root)
    destination = destination_root / relative
    inventory = payload_inventory(asset_dir, manifest)
    digest = inventory_digest(inventory)
    mirror = {
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
        for entry in manifest.get("mirrors") or []
        if entry.get("destination_id") != destination_id
    ]
    try:
        if require_destination_root and not destination_root.is_dir():
            raise OSError(f"destination root unavailable: {destination_root}")
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
        mirror["error"] = str(exc)[:300]
    manifest["mirrors"] = others + [mirror]
    atomic_write_json(media_path, manifest)
    if mirror["state"] == "synced":
        shutil.copy2(media_path, destination / "media.json")
        if hash_file(media_path) != hash_file(destination / "media.json"):
            mirror["state"] = "error"
            mirror["error"] = "final manifest verification failed"
            atomic_write_json(media_path, manifest)
            return BackupResult("error", destination, mirror["error"])
    return BackupResult(mirror["state"], destination, mirror["error"])