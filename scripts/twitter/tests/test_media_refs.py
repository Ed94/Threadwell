from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from twitter.media_migrate import migrate_legacy_thread
from twitter.media_refs import plan_thread_rewrites
from twitter.tests.helpers import NOW, legacy_thread


class MediaReferenceTests(unittest.TestCase):
    def test_catbox_reference_becomes_origin_without_losing_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            asset_dir, note_dir = legacy_thread(root / "assets", root / "notes")
            result = migrate_legacy_thread(asset_dir, note_dir, now=NOW, apply=True)
            self.assertTrue(result.changed)
            text = (note_dir / "index.md").read_text(encoding="utf-8")
            self.assertIn(
                "![](https://pbs.twimg.com/media/AAA?format=png&name=orig)",
                text,
            )
            self.assertNotIn("files.catbox.moe", text)
            self.assertIn("**1/**\n\nFixture post", text)
            self.assertIn('post_id: "100"', text)
            self.assertIn("draft: false", text)

    def test_filename_line_with_two_images_becomes_two_embeds(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            note_dir = Path(raw)
            note = note_dir / "index.md"
            note.write_text(
                "before\nMedia (not lifted): `a.png` `b.jpg`\nafter\n",
                encoding="utf-8",
            )
            plan = plan_thread_rewrites(
                note_dir,
                filename_origins={
                    "a.png": "https://pbs.twimg.com/media/A?format=png&name=orig",
                    "b.jpg": "https://pbs.twimg.com/media/B?format=jpg&name=orig",
                },
                fallback_origins={},
            )
            self.assertEqual(plan.issues, ())
            self.assertIn("![](https://pbs.twimg.com/media/A?format=png&name=orig)", plan.files[0].after)
            self.assertIn("![](https://pbs.twimg.com/media/B?format=jpg&name=orig)", plan.files[0].after)
            self.assertNotIn("Media (not lifted)", plan.files[0].after)

    def test_video_uses_video_element(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            note_dir = Path(raw)
            note = note_dir / "index.md"
            note.write_text("Media (not lifted): `clip.mp4`\n", encoding="utf-8")
            plan = plan_thread_rewrites(
                note_dir,
                filename_origins={"clip.mp4": "https://video.twimg.com/ext_tw_video/clip.mp4"},
                fallback_origins={},
            )
            self.assertIn(
                '<video controls src="https://video.twimg.com/ext_tw_video/clip.mp4"></video>',
                plan.files[0].after,
            )

    def test_untracked_catbox_url_blocks_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            note_dir = Path(raw)
            note = note_dir / "index.md"
            note.write_text("![](https://files.catbox.moe/unknown.png)\n", encoding="utf-8")
            plan = plan_thread_rewrites(
                note_dir,
                filename_origins={},
                fallback_origins={},
            )
            self.assertEqual(plan.files, ())
            self.assertEqual(
                plan.issues,
                ("untracked fallback reference: https://files.catbox.moe/unknown.png",),
            )


if __name__ == "__main__":
    unittest.main()