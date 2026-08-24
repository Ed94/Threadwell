from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from twitter.emit_archive import missing_local_media, preserve_review_state
from twitter.media_manifest import new_original_item
from twitter.render import render_media


class EmitMediaTests(unittest.TestCase):
    def test_render_media_uses_image_and_video_markup(self) -> None:
        self.assertEqual(
            render_media("https://pbs.twimg.com/media/A?format=png&name=orig"),
            "![](https://pbs.twimg.com/media/A?format=png&name=orig)",
        )
        self.assertEqual(
            render_media("https://video.twimg.com/ext_tw_video/A.mp4"),
            '<video controls src="https://video.twimg.com/ext_tw_video/A.mp4"></video>',
        )

    def test_refresh_preserves_draft_and_reviewed_tags(self) -> None:
        old = (
            "---\n"
            "title: Old\n"
            "draft: false\n"
            "tags:\n"
            "  - archive\n"
            "  - twitter\n"
            "  - example\n"
            "  - vulkan\n"
            "---\n\nOld body\n"
        )
        fresh = (
            "---\n"
            "title: Fresh\n"
            "draft: true\n"
            "tags:\n"
            "  - archive\n"
            "  - twitter\n"
            "  - example\n"
            "---\n\nFresh body\n"
        )
        merged = preserve_review_state(old, fresh, mechanical_tags={"archive", "twitter", "example"})
        self.assertIn("draft: false", merged)
        self.assertIn("  - vulkan", merged)
        self.assertIn("Fresh body", merged)
        self.assertNotIn("Old body", merged)

    def test_missing_local_media_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "missing.png"
            item = new_original_item(
                post_id="100",
                media_id="AAA",
                handle="example",
                origin_url="https://pbs.twimg.com/media/AAA?format=png&name=orig",
                filename=path.name,
                local_path=path,
                now="2026-08-24T12:00:00Z",
            )
            self.assertEqual(missing_local_media([item]), ["100/AAA/orig"])


if __name__ == "__main__":
    unittest.main()