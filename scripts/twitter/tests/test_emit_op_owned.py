"""End-to-end tests for OP-owned emit on cross-author fixtures.

The OP-owned model emits one archive dir per thread, owned by the OP
(the post with `reply_to_id == None`). All posts in the conversation
are rendered in chronological order. Cross-handle chains are preserved.
"""

from __future__ import annotations

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from twitter.emit_archive import emit
from twitter.models import PostData, PostMetrics


def make_post(
    post_id: str,
    handle: str,
    text: str,
    timestamp: str,
    reply_to: str | None,
) -> PostData:
    return PostData(
        post_id=post_id,
        author=handle,
        handle=handle,
        text=text,
        timestamp=timestamp,
        media_urls=(),
        reply_to_id=reply_to,
        quote_of_id=None,
        metrics=PostMetrics(0, 0, 0, None),
    )


SEVEN_POST: tuple[PostData, ...] = (
    make_post(
        "1597661267845865474",
        "rianflo",
        '"The road to 16-bit floats GPU is paved with our blood" :-/ https://example.com/road',
        "2022-11-29 18:38:24",
        None,
    ),
    make_post(
        "1597717009369735169",
        "NOTimothyLottes",
        "@rianflo Explicit packed 16-bit works on AMD Vulkan Vega and up.",
        "2022-11-29 22:19:53",
        "1597661267845865474",
    ),
    make_post(
        "1597718146663690240",
        "rianflo",
        "@NOTimothyLottes Oh I know the benefits. Just no simple clear way to write it in GLSL for vulkan.",
        "2022-11-29 22:24:24",
        "1597717009369735169",
    ),
    make_post(
        "1597718560511385600",
        "NOTimothyLottes",
        "@rianflo Sure there is. CAS/FSR1/etc all shipped with fantastic GLSL versions using 16-bit packed math.",
        "2022-11-29 22:26:03",
        "1597718146663690240",
    ),
    make_post(
        "1597720097753542656",
        "rianflo",
        "@NOTimothyLottes What GLSL extension did you use?",
        "2022-11-29 22:32:10",
        "1597718560511385600",
    ),
    make_post(
        "1597720454000541696",
        "rianflo",
        "@NOTimothyLottes Oh wait, you're saying you wrote the fp16 math manually?",
        "2022-11-29 22:33:35",
        "1597720097753542656",
    ),
    make_post(
        "1597798161665253376",
        "NOTimothyLottes",
        "@rianflo Explicit packed 16-bit code. FSR1 example: https://example.com/fsr1",
        "2022-11-30 03:42:22",
        "1597720454000541696",
    ),
)


def _wire_dump(posts: tuple[PostData, ...]) -> dict:
    return {
        "root_post_id": "1597798161665253376",
        "source_url": "https://x.com/i/status/1597798161665253376",
        "posts": [
            {
                "post_id": p.post_id,
                "author": p.author,
                "handle": p.handle,
                "text": p.text,
                "timestamp": p.timestamp,
                "media_urls": list(p.media_urls),
                "reply_to_id": p.reply_to_id,
                "quote_of_id": p.quote_of_id,
                "metrics": {
                    "reply_count": p.metrics.reply_count,
                    "repost_count": p.metrics.repost_count,
                    "like_count": p.metrics.like_count,
                    "view_count": p.metrics.view_count,
                },
            }
            for p in posts
        ],
    }


def _wikilink_names(text: str) -> list[str]:
    names: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^\s*-\s+\[\[([^\]|]+)\]\]\s*$", line)
        if m:
            names.append(m.group(1).rsplit("/", 1)[-1])
    return sorted(names)


class OpOwnedEmitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="op_owned_emit_"))
        self.input_dir = self.tmp / "input"
        self.input_dir.mkdir()
        (self.input_dir / "thread_data.json").write_text(
            json.dumps(_wire_dump(SEVEN_POST), indent=2),
            encoding="utf-8",
            newline="\n",
        )
        self.vault = self.tmp / "vault"
        (self.vault / "archive" / "threads").mkdir(parents=True)
        (self.vault / "assets" / "threads").mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_one_archive_dir_owned_by_op(self) -> None:
        """The thread produces exactly one archive dir, owned by the
        OP (rianflo). lottes does not get a separate dir."""
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-24",
            force=True,
        )
        archive_root = self.vault / "archive" / "threads"
        handles = sorted(
            d.name for d in archive_root.iterdir() if d.is_dir()
        )
        self.assertEqual(handles, ["rianflo"])

    def test_one_asset_dir_with_all_seven_posts(self) -> None:
        """The asset dir holds the full thread_data.json (all 7
        posts), not a per-author subset."""
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-24",
            force=True,
        )
        asset_root = self.vault / "assets" / "threads"
        handles = sorted(
            d.name for d in asset_root.iterdir() if d.is_dir()
        )
        self.assertEqual(handles, ["rianflo"])

        thread_dirs = sorted(
            d for d in (asset_root / "rianflo").iterdir() if d.is_dir()
        )
        self.assertEqual(len(thread_dirs), 1)
        thread_data = json.loads(
            (thread_dirs[0] / "thread_data.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(thread_data["posts"]), 7)

    def test_index_md_renders_all_seven_posts_in_order(self) -> None:
        """The index.md shows all 7 posts in chain order with N/
        numbering. The OP (rianflo) is the frontmatter handle and
        source_url."""
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-24",
            force=True,
        )
        thread_dir = next(
            d for d in (self.vault / "archive" / "threads" / "rianflo").iterdir()
            if d.is_dir()
        )
        text = (thread_dir / "index.md").read_text(encoding="utf-8")
        self.assertIn("handle: rianflo", text)
        self.assertIn(
            'source_url: "https://x.com/rianflo/status/1597661267845865474"',
            text,
        )
        # All 7 N/ markers in chronological chain order
        for n in range(1, 8):
            self.assertIn(f"**{n}/**", text)
        # Posts appear in chain order. Use a short, unique fragment
        # of each post's text to locate its position in the file.
        fragments = [
            "The road to 16-bit floats GPU",        # OP post 1
            "Explicit packed 16-bit works on AMD",   # lottes post 1 (2/)
            "Oh I know the benefits",                # rianflo (3/)
            "CAS/FSR1/etc all shipped",              # lottes (4/)
            "What GLSL extension",                   # rianflo (5/)
            "Oh wait, you're saying",                # rianflo (6/)
            "FSR1 example",                          # lottes tip (7/)
        ]
        positions = [text.find(f) for f in fragments]
        self.assertTrue(
            all(p >= 0 for p in positions),
            f"missing fragments in index.md: "
            f"{[fragments[i] for i, p in enumerate(positions) if p < 0]}",
        )
        self.assertEqual(
            positions,
            sorted(positions),
            f"posts out of order in index.md: {positions}",
        )

    def test_lottes_handle_index_does_not_link_to_thread(self) -> None:
        """lottes is a responder, not the OP. Her handle index must
        not wikilink this thread."""
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-24",
            force=True,
        )
        archive_root = self.vault / "archive" / "threads"
        # lottes's handle dir should not exist (she's not the OP)
        lottes_handle = archive_root / "NOTimothyLottes"
        self.assertFalse(
            lottes_handle.exists(),
            "lottes is a responder, not the OP; no handle dir expected",
        )

    def test_rianflo_handle_index_links_to_thread(self) -> None:
        """rianflo is the OP. His handle index lists the new thread."""
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-24",
            force=True,
        )
        archive_root = self.vault / "archive" / "threads"
        rianflo_index = (
            archive_root / "rianflo" / "index.md"
        ).read_text(encoding="utf-8")
        rianflo_thread_dirs = sorted(
            d.name
            for d in (archive_root / "rianflo").iterdir()
            if d.is_dir()
        )
        self.assertEqual(_wikilink_names(rianflo_index), rianflo_thread_dirs)

    def test_no_conversation_section(self) -> None:
        """The OP-owned model does not emit a ## Conversation
        section (the thread is the conversation)."""
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-24",
            force=True,
        )
        thread_dir = next(
            d for d in (self.vault / "archive" / "threads" / "rianflo").iterdir()
            if d.is_dir()
        )
        text = (thread_dir / "index.md").read_text(encoding="utf-8")
        self.assertNotIn("## Conversation", text)


class OpOwnedEmitTipModeTests(unittest.TestCase):
    """--tip mode climbs back to the OP and renders the full chain."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="op_owned_tip_"))
        self.input_dir = self.tmp / "input"
        self.input_dir.mkdir()
        (self.input_dir / "thread_data.json").write_text(
            json.dumps(_wire_dump(SEVEN_POST), indent=2),
            encoding="utf-8",
            newline="\n",
        )
        self.vault = self.tmp / "vault"
        (self.vault / "archive" / "threads").mkdir(parents=True)
        (self.vault / "assets" / "threads").mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_tip_mode_emits_full_chain(self) -> None:
        """Passing --tip with the tip's post_id still produces one
        OP-owned dir with all 7 posts."""
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-24",
            force=True,
            tip="1597798161665253376",
        )
        archive_root = self.vault / "archive" / "threads"
        handles = sorted(
            d.name for d in archive_root.iterdir() if d.is_dir()
        )
        self.assertEqual(handles, ["rianflo"])

        thread_dirs = [
            d for d in (archive_root / "rianflo").iterdir() if d.is_dir()
        ]
        self.assertEqual(len(thread_dirs), 1)

        asset_root = self.vault / "assets" / "threads"
        thread_dirs = [
            d for d in (asset_root / "rianflo").iterdir() if d.is_dir()
        ]
        self.assertEqual(len(thread_dirs), 1)
        thread_data = json.loads(
            (thread_dirs[0] / "thread_data.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(thread_data["posts"]), 7)


class OrphansNotReusedTests(unittest.TestCase):
    """An old archive keyed by a non-OP handle must not be reused.
    A pre-existing tip-as-root archive of a cross-author conversation
    is treated as orphan; the OP-owned emit produces a fresh dir at
    the OP handle."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="op_owned_orphan_"))
        self.input_dir = self.tmp / "input"
        self.input_dir.mkdir()
        self.vault = self.tmp / "vault"
        (self.vault / "archive" / "threads").mkdir(parents=True)
        (self.vault / "assets" / "threads").mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_old_archive_at_non_op_handle_is_not_reused(self) -> None:
        """Pre-existing dir keyed by the tip's handle (lottes) must
        not be reused when the OP is a different handle (kenpex).
        The emit creates a fresh dir at the OP handle."""
        # Simulate a pre-existing tip-as-root archive at NOTimothyLottes
        legacy_archive = (
            self.vault
            / "archive"
            / "threads"
            / "NOTimothyLottes"
            / "2023-04-26-legacy-slug"
        )
        legacy_archive.mkdir(parents=True)
        (legacy_archive / "index.md").write_text(
            (
                "---\n"
                "title: legacy\n"
                "handle: NOTimothyLottes\n"
                'post_id: "1651268028795961344"\n'
                "draft: false\n"
                "---\n\n"
                "old single-post archive\n"
            ),
            encoding="utf-8",
            newline="\n",
        )
        (legacy_archive.parent / "index.md").write_text(
            (
                "---\n"
                "title: NOTimothyLottes\n"
                "---\n\n"
                "- [[archive/threads/NOTimothyLottes/2023-04-26-legacy-slug]]\n"
            ),
            encoding="utf-8",
            newline="\n",
        )

        # Write the cross-author thread data (5 posts, kenpex OP)
        thread_data = {
            "root_post_id": "1651282559287042048",
            "source_url": "https://x.com/i/status/1651282559287042048",
            "posts": [
                {
                    "post_id": "1650678968255913985",
                    "author": "c0de517e",
                    "handle": "kenpex",
                    "text": "Nerds are crazy",
                    "timestamp": "2023-04-25 01:51:48",
                    "media_urls": [],
                    "reply_to_id": None,
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": 0,
                    },
                },
                {
                    "post_id": "1651056827839180800",
                    "author": "wadetb",
                    "handle": "wadetb",
                    "text": "Forth is asm-level",
                    "timestamp": "2023-04-26 02:53:17",
                    "media_urls": [],
                    "reply_to_id": "1650678968255913985",
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": 0,
                    },
                },
                {
                    "post_id": "1651253961524142081",
                    "author": "kenpex",
                    "handle": "kenpex",
                    "text": "Yes of course",
                    "timestamp": "2023-04-26 15:56:37",
                    "media_urls": [],
                    "reply_to_id": "1651056827839180800",
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": 0,
                    },
                },
                {
                    "post_id": "1651268028795961344",
                    "author": "NOTimothyLottes",
                    "handle": "NOTimothyLottes",
                    "text": "Custom forth in few K",
                    "timestamp": "2023-04-26 16:52:31",
                    "media_urls": [],
                    "reply_to_id": "1651253961524142081",
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": 0,
                    },
                },
                {
                    "post_id": "1651282559287042048",
                    "author": "wvo",
                    "handle": "wvo",
                    "text": "Why not 1K?",
                    "timestamp": "2023-04-26 17:50:16",
                    "media_urls": [],
                    "reply_to_id": "1651268028795961344",
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": 0,
                    },
                },
            ],
        }
        (self.input_dir / "thread_data.json").write_text(
            json.dumps(thread_data, indent=2),
            encoding="utf-8",
            newline="\n",
        )

        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-24",
            force=True,
            tip="1651282559287042048",
        )

        archive_root = self.vault / "archive" / "threads"
        # The OP-owned archive lives under kenpex, not NOTimothyLottes
        self.assertTrue(
            (archive_root / "kenpex").is_dir(),
            "OP-owned archive must live under the OP handle's dir",
        )
        kenpex_thread_dirs = sorted(
            d.name
            for d in (archive_root / "kenpex").iterdir()
            if d.is_dir()
        )
        self.assertEqual(len(kenpex_thread_dirs), 1)

        # The legacy NOTimothyLottes dir is left as orphan; this
        # test does not auto-remove it (manual cleanup is operator
        # responsibility).
        self.assertTrue(
            (archive_root / "NOTimothyLottes" / "2023-04-26-legacy-slug").is_dir(),
        )


if __name__ == "__main__":
    unittest.main()