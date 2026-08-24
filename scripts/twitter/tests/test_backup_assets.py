from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from twitter.backup_assets import backup_thread
from twitter.media_audit import audit_thread
from twitter.media_manifest import (
    _from_wire_dict,
    canonical_manifest_bytes,
    hash_file,
    inventory_digest,
    payload_inventory,
)
from twitter.media_migrate import migrate_legacy_thread
from twitter.tests.helpers import NOW, legacy_thread, read_json


class BackupTests(unittest.TestCase):
    def test_backup_copies_and_verifies_one_thread(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            asset_dir, note_dir = legacy_thread(
                root / "assets" / "threads" / "example" / "fixture",
                root / "notes",
            )
            migrate_legacy_thread(asset_dir, note_dir, now=NOW, apply=True)
            destination = root / "backup"
            result = backup_thread(
                asset_dir,
                assets_root=root / "assets",
                destination_root=destination,
                destination_id="cozy",
                now=NOW,
            )
            self.assertEqual(result.state, "synced")
            copied = destination / "threads" / "example" / "fixture"
            self.assertTrue((copied / "100_AAA_orig.png").is_file())
            manifest = read_json(asset_dir / "media.json")
            self.assertEqual(manifest["mirrors"][0]["state"], "synced")

    def test_missing_destination_parent_does_not_change_publication(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            asset_dir, note_dir = legacy_thread(root / "assets" / "thread", root / "notes")
            migrate_legacy_thread(asset_dir, note_dir, now=NOW, apply=True)
            before = read_json(asset_dir / "media.json")["items"][0]["publication"]
            result = backup_thread(
                asset_dir,
                assets_root=root / "assets",
                destination_root=root / "absent" / "share",
                destination_id="cozy",
                now=NOW,
                require_destination_root=True,
            )
            self.assertEqual(result.state, "error")
            after = read_json(asset_dir / "media.json")["items"][0]["publication"]
            self.assertEqual(after, before)

    def test_inventory_change_marks_mirror_stale(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            asset_dir, note_dir = legacy_thread(
                root / "assets" / "threads" / "example" / "fixture",
                root / "notes",
            )
            migrate_legacy_thread(asset_dir, note_dir, now=NOW, apply=True)
            destination = root / "backup"
            backup_thread(
                asset_dir,
                assets_root=root / "assets",
                destination_root=destination,
                destination_id="cozy",
                now=NOW,
            )
            manifest = read_json(asset_dir / "media.json")
            typed_manifest = _from_wire_dict(manifest)
            inventory = payload_inventory(asset_dir, typed_manifest)
            self.assertEqual(
                manifest["mirrors"][0]["inventory_digest"],
                inventory_digest(inventory),
            )
            backup_inventory_before = inventory_digest(payload_inventory(asset_dir, typed_manifest))
            (asset_dir / "100_AAA_orig.png").write_bytes(b"modified")
            new_inventory = payload_inventory(asset_dir, typed_manifest)
            self.assertNotEqual(
                inventory_digest(new_inventory),
                backup_inventory_before,
            )
            report = audit_thread(asset_dir, note_dir, set())
            self.assertTrue(any("mirror stale" in issue for issue in report.issues))


if __name__ == "__main__":
    unittest.main()