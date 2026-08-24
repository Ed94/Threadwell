from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from twitter.media_manifest import find_location, selected_url, validate_manifest
from twitter.media_migrate import migrate_legacy_thread
from twitter.tests.helpers import NOW, legacy_thread, read_json


class LegacyMigrationTests(unittest.TestCase):
    def test_origin_local_and_catbox_survive_migration(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            asset_dir, note_dir = legacy_thread(root / "assets", root / "notes")
            result = migrate_legacy_thread(asset_dir, note_dir, now=NOW, apply=False)
            self.assertEqual(result.state, "migratable")
            self.assertFalse(result.changed)
            legacy = read_json(asset_dir / "media.json")
            self.assertNotIn("schema_version", legacy)

            applied = migrate_legacy_thread(asset_dir, note_dir, now=NOW, apply=True)
            self.assertTrue(applied.changed)
            manifest = read_json(asset_dir / "media.json")
            self.assertEqual(validate_manifest(manifest), [])
            item = manifest["items"][0]
            self.assertEqual(
                find_location(item, "origin:x")["url"],
                "https://pbs.twimg.com/media/AAA?format=png&name=orig",
            )
            fallback = next(
                location
                for location in item["locations"]
                if location.get("kind") == "fallback"
            )
            self.assertEqual(fallback["url"], "https://files.catbox.moe/fallback.png")
            self.assertEqual(selected_url(item), find_location(item, "origin:x")["url"])

    def test_second_migration_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            asset_dir, note_dir = legacy_thread(root / "assets", root / "notes")
            migrate_legacy_thread(asset_dir, note_dir, now=NOW, apply=True)
            before = (asset_dir / "media.json").read_bytes()
            result = migrate_legacy_thread(asset_dir, note_dir, now=NOW, apply=True)
            self.assertFalse(result.changed)
            self.assertEqual((asset_dir / "media.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()