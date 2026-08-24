from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from twitter.fallback_media import activate_fallback, restore_origin
from twitter.media_manifest import selected_url
from twitter.media_migrate import migrate_legacy_thread
from twitter.tests.helpers import NOW, legacy_thread, read_json


class FallbackTests(unittest.TestCase):
    def test_existing_matching_fallback_does_not_upload(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            asset_dir, note_dir = legacy_thread(root / "assets", root / "notes")
            migrate_legacy_thread(asset_dir, note_dir, now=NOW, apply=True)
            calls: list[Path] = []

            def upload(path: Path) -> str:
                calls.append(path)
                return "https://files.catbox.moe/new.png"

            result = activate_fallback(
                asset_dir,
                note_dir,
                media_id="AAA",
                role="orig",
                provider="catbox",
                confirm_origin_unavailable=True,
                now=NOW,
                upload=upload,
            )
            self.assertEqual(calls, [])
            self.assertEqual(result.url, "https://files.catbox.moe/fallback.png")
            manifest = read_json(asset_dir / "media.json")
            self.assertEqual(selected_url(manifest["items"][0]), result.url)

    def test_note_rewrite_failure_keeps_origin_selected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            asset_dir, note_dir = legacy_thread(root / "assets", root / "notes")
            migrate_legacy_thread(asset_dir, note_dir, now=NOW, apply=True)
            (note_dir / "index.md").write_text("no media reference\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "selected origin reference not found exactly once"):
                activate_fallback(
                    asset_dir,
                    note_dir,
                    media_id="AAA",
                    role="orig",
                    provider="catbox",
                    confirm_origin_unavailable=True,
                    now=NOW,
                    upload=lambda _path: "https://files.catbox.moe/fallback.png",
                )
            manifest = read_json(asset_dir / "media.json")
            self.assertTrue(selected_url(manifest["items"][0]).startswith("https://pbs.twimg.com/"))

    def test_restore_origin_retains_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            asset_dir, note_dir = legacy_thread(root / "assets", root / "notes")
            migrate_legacy_thread(asset_dir, note_dir, now=NOW, apply=True)
            activate_fallback(
                asset_dir,
                note_dir,
                media_id="AAA",
                role="orig",
                provider="catbox",
                confirm_origin_unavailable=True,
                now=NOW,
                upload=lambda _path: "https://files.catbox.moe/fallback.png",
            )
            restore_origin(asset_dir, note_dir, media_id="AAA", now=NOW)
            item = read_json(asset_dir / "media.json")["items"][0]
            self.assertTrue(selected_url(item).startswith("https://pbs.twimg.com/"))
            self.assertTrue(any(loc.get("kind") == "fallback" for loc in item["locations"]))


if __name__ == "__main__":
    unittest.main()