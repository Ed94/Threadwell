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
from tempfile import TemporaryDirectory

from twitter.emit_archive import emit
from twitter.models import PostData, PostMetrics, ThreadData


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

        with self.assertRaisesRegex(SystemExit, "leftover dir"):
            emit(
                input_dir=self.input_dir,
                vault=self.vault,
                slug=None,
                archived="2026-08-24",
                force=True,
                tip="1651282559287042048",
            )

        archive_root = self.vault / "archive" / "threads"
        self.assertTrue(
            (archive_root / "NOTimothyLottes" / "2023-04-26-legacy-slug").is_dir(),
        )
        self.assertFalse((archive_root / "kenpex").exists())


class SpinePrefersSameAuthorTests(unittest.TestCase):
    """The spine walker must prefer the OP's own same-handle chain
    over cross-author replies. When the OP has a self-reply plus
    other-author replies to the same post, the self-reply continues
    the spine and the cross-author replies become branches."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="spine_same_author_"))
        self.input_dir = self.tmp / "input"
        self.input_dir.mkdir()
        self.vault = self.tmp / "vault"
        (self.vault / "archive" / "threads").mkdir(parents=True)
        (self.vault / "assets" / "threads").mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_op_with_self_reply_continues_spine(self) -> None:
        """OP has children including a self-reply and a cross-author
        reply that arrived FIRST chronologically. Spine should walk
        the OP's self-reply chain, not stop at the cross-author reply.
        """
        # OP at 00:00. won3d replies at 00:01 (cross-author, earliest).
        # Lottes self-replies at 00:05 (later, same handle, continues
        # the spine).
        thread_data = {
            "root_post_id": "1000",
            "source_url": "https://x.com/i/status/1000",
            "posts": [
                {
                    "post_id": "1000",
                    "author": "OP",
                    "handle": "OP",
                    "text": "OP post",
                    "timestamp": "2023-01-01 00:00:00",
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
                    "post_id": "1001",
                    "author": "won3d",
                    "handle": "won3d",
                    "text": "early reply from outsider",
                    "timestamp": "2023-01-01 00:01:00",
                    "media_urls": [],
                    "reply_to_id": "1000",
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": 0,
                    },
                },
                {
                    "post_id": "1002",
                    "author": "OP",
                    "handle": "OP",
                    "text": "OP self-reply continues the thread",
                    "timestamp": "2023-01-01 00:05:00",
                    "media_urls": [],
                    "reply_to_id": "1000",
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": 0,
                    },
                },
                {
                    "post_id": "1003",
                    "author": "OP",
                    "handle": "OP",
                    "text": "OP continues again",
                    "timestamp": "2023-01-01 00:10:00",
                    "media_urls": [],
                    "reply_to_id": "1002",
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
        )

        archive_root = self.vault / "archive" / "threads"
        thread_dir = next(
            d for d in (archive_root / "OP").iterdir() if d.is_dir()
        )
        text = (thread_dir / "index.md").read_text(encoding="utf-8")
        # The spine should have 3 OP posts in order: 1000, 1002, 1003.
        # won3d's post 1001 should be a branch (separate file).
        self.assertIn("**1/**", text)
        self.assertIn("**2/**", text)
        self.assertIn("**3/**", text)
        # won3d's text appears only in the branch file, not in the spine.
        won3d_spine_mentions = text.count("early reply from outsider")
        self.assertEqual(won3d_spine_mentions, 0)
        # A branch file for won3d exists.
        branch_files = [
            f for f in thread_dir.iterdir()
            if f.is_file() and f.name != "index.md"
        ]
        self.assertEqual(len(branch_files), 1)
        branch_text = branch_files[0].read_text(encoding="utf-8")
        self.assertIn("early reply from outsider", branch_text)


class TipIsOpTests(unittest.TestCase):
    """`--tip=<op>` where the tip's reply_to_id is None. The walker
    must walk DOWN from the OP via children_map, not stop at the
    OP because the back-walk has no parent."""

    def test_tip_with_no_parent_walks_down(self) -> None:
        from twitter.tree import spine_from_tip

        thread_data = {
            "root_post_id": "1000",
            "source_url": "https://x.com/i/status/1000",
            "posts": [
                {
                    "post_id": "1000",
                    "author": "X",
                    "handle": "X",
                    "text": "OP post",
                    "timestamp": "2023-01-01 00:00:00",
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
                    "post_id": "1001",
                    "author": "X",
                    "handle": "X",
                    "text": "self-reply 1",
                    "timestamp": "2023-01-01 00:05:00",
                    "media_urls": [],
                    "reply_to_id": "1000",
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": 0,
                    },
                },
                {
                    "post_id": "1002",
                    "author": "X",
                    "handle": "X",
                    "text": "self-reply 2",
                    "timestamp": "2023-01-01 00:10:00",
                    "media_urls": [],
                    "reply_to_id": "1001",
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
        thread = ThreadData(
            root_post_id="1000",
            posts=tuple(
                PostData(
                    post_id=p["post_id"],
                    author=p["author"],
                    handle=p["handle"],
                    text=p["text"],
                    timestamp=p["timestamp"],
                    media_urls=tuple(p["media_urls"]),
                    reply_to_id=p["reply_to_id"],
                    quote_of_id=p["quote_of_id"],
                    metrics=PostMetrics(0, 0, 0, 0),
                )
                for p in thread_data["posts"]
            ),
            source_url="https://x.com/i/status/1000",
        )
        # --tip=OP, which has reply_to=None. Must walk DOWN.
        spine = spine_from_tip(thread, "1000")
        self.assertEqual(spine, ["1000", "1001", "1002"])

    def test_op_tip_stops_without_same_handle_child(self) -> None:
        from twitter.tree import spine_from_tip

        thread = ThreadData(
            root_post_id="1000",
            posts=(
                make_post(
                    "1000",
                    "mike_acton",
                    "OP post",
                    "2023-01-01 00:00:00",
                    None,
                ),
                make_post(
                    "1001",
                    "aras_p",
                    "joke reply",
                    "2023-01-01 00:05:00",
                    "1000",
                ),
            ),
            source_url="https://x.com/i/status/1000",
        )
        spine = spine_from_tip(thread, "1000")
        self.assertEqual(spine, ["1000"])

    def test_spine_ids_still_promotes_earliest_foreign_child(self) -> None:
        from twitter.tree import spine_ids

        thread = ThreadData(
            root_post_id="1000",
            posts=(
                make_post(
                    "1000",
                    "mike_acton",
                    "OP post",
                    "2023-01-01 00:00:00",
                    None,
                ),
                make_post(
                    "1001",
                    "aras_p",
                    "joke reply",
                    "2023-01-01 00:05:00",
                    "1000",
                ),
            ),
            source_url="https://x.com/i/status/1000",
        )
        self.assertEqual(spine_ids(thread), ["1000", "1001"])

    def test_tip_with_parent_walks_back(self) -> None:
        from twitter.tree import spine_from_tip

        thread_data = {
            "root_post_id": "2000",
            "source_url": "https://x.com/i/status/2000",
            "posts": [
                {
                    "post_id": "2000",
                    "author": "X",
                    "handle": "X",
                    "text": "OP",
                    "timestamp": "2023-01-01 00:00:00",
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
                    "post_id": "2001",
                    "author": "X",
                    "handle": "X",
                    "text": "self-reply",
                    "timestamp": "2023-01-01 00:05:00",
                    "media_urls": [],
                    "reply_to_id": "2000",
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": 0,
                    },
                },
                {
                    "post_id": "2002",
                    "author": "X",
                    "handle": "X",
                    "text": "tip reply",
                    "timestamp": "2023-01-01 00:10:00",
                    "media_urls": [],
                    "reply_to_id": "2001",
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
        thread = ThreadData(
            root_post_id="2000",
            posts=tuple(
                PostData(
                    post_id=p["post_id"],
                    author=p["author"],
                    handle=p["handle"],
                    text=p["text"],
                    timestamp=p["timestamp"],
                    media_urls=tuple(p["media_urls"]),
                    reply_to_id=p["reply_to_id"],
                    quote_of_id=p["quote_of_id"],
                    metrics=PostMetrics(0, 0, 0, 0),
                )
                for p in thread_data["posts"]
            ),
            source_url="https://x.com/i/status/2000",
        )
        # --tip=middle post (has parent). Walks back.
        spine = spine_from_tip(thread, "2002")
        self.assertEqual(spine, ["2000", "2001", "2002"])


class StaleBranchPruneTests(unittest.TestCase):
    """Re-emit must delete branch notes that are no longer roots."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="stale_branch_"))
        self.input_dir = self.tmp / "input"
        self.input_dir.mkdir()
        (self.input_dir / "thread_data.json").write_text(
            json.dumps(
                {
                    "root_post_id": "1000",
                    "source_url": "https://x.com/i/status/1000",
                    "posts": [
                        {
                            "post_id": "1000",
                            "author": "alice",
                            "handle": "alice",
                            "text": "Hello",
                            "timestamp": "2026-01-01 00:00:00",
                            "media_urls": [],
                            "reply_to_id": None,
                            "quote_of_id": None,
                            "metrics": {
                                "reply_count": 0,
                                "repost_count": 0,
                                "like_count": 0,
                                "view_count": 0,
                            },
                        }
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
            newline="\n",
        )
        self.vault = self.tmp / "vault"
        (self.vault / "archive" / "threads").mkdir(parents=True)
        (self.vault / "assets" / "threads").mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_emit_deletes_stale_branch_notes(self) -> None:
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-25",
            force=True,
            tip="1000",
        )
        note_dir = (
            self.vault
            / "archive"
            / "threads"
            / "alice"
            / "2026-01-01-hello"
        )
        stale = note_dir / "2026-01-01-bob-noise.md"
        stale.write_text("leftover\n", encoding="utf-8", newline="\n")
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-25",
            force=True,
            tip="1000",
        )
        self.assertFalse(stale.is_file())
        self.assertTrue((note_dir / "index.md").is_file())


class ReslugReuseTests(unittest.TestCase):
    """Compact same-handle integration tests for the emit-side rename flow.

    Each test pre-populates one or more archive/asset pairs under the
    vault, invokes ``emit`` with explicit ``reconcile_scratch`` and
    ``frozen_ids`` so nothing is written to the workspace scratch and
    no frozen list is read from secrets.
    """

    HANDLE = "alice"
    ROOT_ID = "1000"
    TIMESTAMP = "2026-08-24 12:00:00"
    ROOT_TEXT = "Root title. Extra first-line detail that should be dropped."
    EXPECTED_CANONICAL = "2026-08-24-root-title"

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="reslug_reuse_"))
        self.input_dir = self.tmp / "input"
        self.input_dir.mkdir()
        self.vault = self.tmp / "vault"
        (self.vault / "archive" / "threads").mkdir(parents=True)
        (self.vault / "assets" / "threads").mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write_thread(self) -> None:
        thread = {
            "root_post_id": self.ROOT_ID,
            "source_url": f"https://x.com/{self.HANDLE}/status/{self.ROOT_ID}",
            "posts": [
                {
                    "post_id": self.ROOT_ID,
                    "author": self.HANDLE,
                    "handle": self.HANDLE,
                    "text": self.ROOT_TEXT,
                    "timestamp": self.TIMESTAMP,
                    "media_urls": [],
                    "reply_to_id": None,
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": 0,
                    },
                }
            ],
        }
        (self.input_dir / "thread_data.json").write_text(
            json.dumps(thread, indent=2),
            encoding="utf-8",
            newline="\n",
        )

    def _write_existing_pair(
        self,
        *,
        dir_name: str,
        post_id: str,
        index_body: str = "",
        editorial_tag: str | None = None,
        draft: str = "true",
        timestamp: str | None = None,
    ) -> tuple[Path, Path]:
        archive = self.vault / "archive" / "threads" / self.HANDLE / dir_name
        asset = self.vault / "assets" / "threads" / self.HANDLE / dir_name
        archive.mkdir(parents=True)
        asset.mkdir(parents=True)
        body_timestamp = timestamp or self.TIMESTAMP
        date_value = body_timestamp[:10]
        tags_lines = (
            "tags:\n"
            "  - archive\n"
            "  - twitter\n"
            f"  - {self.HANDLE}\n"
        )
        if editorial_tag:
            tags_lines += f"  - {editorial_tag}\n"
        (archive / "index.md").write_text(
            "---\n"
            'title: "Old title."\n'
            f"handle: {self.HANDLE}\n"
            f'post_id: "{post_id}"\n'
            f"date: {date_value}\n"
            f"draft: {draft}\n"
            f"{tags_lines}---\n\n{index_body}",
            encoding="utf-8",
            newline="\n",
        )
        (asset / "thread_data.json").write_text(
            json.dumps(
                {
                    "root_post_id": post_id,
                    "source_url": f"https://x.com/{self.HANDLE}/status/{post_id}",
                    "posts": [
                        {
                            "post_id": post_id,
                            "author": self.HANDLE,
                            "handle": self.HANDLE,
                            "text": "Old body.",
                            "timestamp": body_timestamp,
                            "media_urls": [],
                            "reply_to_id": None,
                            "quote_of_id": None,
                            "metrics": {},
                        }
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
            newline="\n",
        )
        (asset / "media.json").write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "root_post_id": post_id,
                    "items": [],
                    "mirrors": [],
                },
                indent=2,
            ),
            encoding="utf-8",
            newline="\n",
        )
        return archive, asset

    def test_emit_renames_reused_pair_to_canonical_dir(self) -> None:
        """Existing archive/asset pair found by post identity is renamed
        to date + rendered-title canonical directory."""
        old_dir = "2026-08-24-stale-slug"
        archive_old, asset_old = self._write_existing_pair(
            dir_name=old_dir,
            post_id=self.ROOT_ID,
        )
        self._write_thread()

        with TemporaryDirectory() as scratch_raw:
            emit(
                input_dir=self.input_dir,
                vault=self.vault,
                slug=None,
                archived="2026-08-24",
                force=True,
                reconcile_scratch=Path(scratch_raw),
                frozen_ids=set(),
            )

        self.assertFalse(archive_old.exists())
        self.assertFalse(asset_old.exists())
        archive_new = (
            self.vault
            / "archive"
            / "threads"
            / self.HANDLE
            / self.EXPECTED_CANONICAL
        )
        asset_new = (
            self.vault
            / "assets"
            / "threads"
            / self.HANDLE
            / self.EXPECTED_CANONICAL
        )
        self.assertTrue(archive_new.is_dir())
        self.assertTrue(asset_new.is_dir())
        self.assertTrue((asset_new / "thread_data.json").is_file())
        self.assertTrue((asset_new / "media.json").is_file())
        self.assertTrue((archive_new / "index.md").is_file())

    def test_emit_handle_index_links_to_new_path_after_rename(self) -> None:
        """The handle index wikilink is updated from the old prefix to
        the new canonical prefix after rename."""
        old_dir = "2026-08-24-stale-slug"
        self._write_existing_pair(
            dir_name=old_dir,
            post_id=self.ROOT_ID,
        )
        self._write_thread()

        with TemporaryDirectory() as scratch_raw:
            emit(
                input_dir=self.input_dir,
                vault=self.vault,
                slug=None,
                archived="2026-08-24",
                force=True,
                reconcile_scratch=Path(scratch_raw),
                frozen_ids=set(),
            )

        handle_index = self.vault / "archive" / "threads" / self.HANDLE / "index.md"
        self.assertTrue(handle_index.is_file())
        text = handle_index.read_text(encoding="utf-8")
        self.assertIn(
            f"archive/threads/{self.HANDLE}/{self.EXPECTED_CANONICAL}",
            text,
        )
        self.assertNotIn(f"archive/threads/{self.HANDLE}/{old_dir}", text)

    def test_emit_preserves_draft_false_and_editorial_tags_across_rename(self) -> None:
        """Existing ``draft: false`` and a non-mechanical editorial tag
        survive the rename."""
        old_dir = "2026-08-24-stale-slug"
        self._write_existing_pair(
            dir_name=old_dir,
            post_id=self.ROOT_ID,
            editorial_tag="editorial",
            draft="false",
        )
        self._write_thread()

        with TemporaryDirectory() as scratch_raw:
            emit(
                input_dir=self.input_dir,
                vault=self.vault,
                slug=None,
                archived="2026-08-24",
                force=True,
                reconcile_scratch=Path(scratch_raw),
                frozen_ids=set(),
            )

        archive_new = (
            self.vault
            / "archive"
            / "threads"
            / self.HANDLE
            / self.EXPECTED_CANONICAL
        )
        text = (archive_new / "index.md").read_text(encoding="utf-8")
        self.assertIn("draft: false", text)
        self.assertIn("- editorial", text)

    def test_emit_slug_override_uses_explicit_suffix(self) -> None:
        """An explicit ``--slug`` override produces a ``date-manual-name``
        directory even when a reused old pair exists."""
        old_dir = "2026-08-24-stale-slug"
        self._write_existing_pair(
            dir_name=old_dir,
            post_id=self.ROOT_ID,
        )
        self._write_thread()

        with TemporaryDirectory() as scratch_raw:
            emit(
                input_dir=self.input_dir,
                vault=self.vault,
                slug="manual-name",
                archived="2026-08-24",
                force=True,
                reconcile_scratch=Path(scratch_raw),
                frozen_ids=set(),
            )

        expected = "2026-08-24-manual-name"
        self.assertTrue(
            (self.vault / "archive" / "threads" / self.HANDLE / expected).is_dir()
        )
        self.assertTrue(
            (self.vault / "assets" / "threads" / self.HANDLE / expected).is_dir()
        )
        self.assertFalse(
            (self.vault / "archive" / "threads" / self.HANDLE / old_dir).exists()
        )

    def test_emit_occupied_canonical_target_refuses_before_move(self) -> None:
        """A new-thread emit whose desired canonical target is already
        occupied by another pair must abort with ``SystemExit`` before any
        write, with no ``-2`` suffix fallback."""
        canonical_archive, canonical_asset = self._write_existing_pair(
            dir_name=self.EXPECTED_CANONICAL,
            post_id="9999",
        )
        self._write_thread()

        with TemporaryDirectory() as scratch_raw:
            with self.assertRaisesRegex(SystemExit, "destination occupied"):
                emit(
                    input_dir=self.input_dir,
                    vault=self.vault,
                    slug=None,
                    archived="2026-08-24",
                    force=True,
                    reconcile_scratch=Path(scratch_raw),
                    frozen_ids=set(),
                )

        self.assertFalse(
            (
                self.vault
                / "archive"
                / "threads"
                / self.HANDLE
                / f"{self.EXPECTED_CANONICAL}-2"
            ).exists()
        )
        self.assertFalse(
            (
                self.vault
                / "assets"
                / "threads"
                / self.HANDLE
                / f"{self.EXPECTED_CANONICAL}-2"
            ).exists()
        )
        self.assertTrue(canonical_archive.is_dir())
        self.assertTrue(canonical_asset.is_dir())

    def test_emit_frozen_mismatch_refuses_before_move(self) -> None:
        """A frozen mismatch on the existing asset dir must abort with
        ``SystemExit`` before either directory is moved."""
        old_dir = "2026-08-24-stale-slug"
        archive_old, asset_old = self._write_existing_pair(
            dir_name=old_dir,
            post_id=self.ROOT_ID,
        )
        self._write_thread()

        with TemporaryDirectory() as scratch_raw:
            with self.assertRaisesRegex(SystemExit, "frozen"):
                emit(
                    input_dir=self.input_dir,
                    vault=self.vault,
                    slug=None,
                    archived="2026-08-24",
                    force=True,
                    reconcile_scratch=Path(scratch_raw),
                    frozen_ids={self.ROOT_ID},
                )

        self.assertTrue(archive_old.is_dir())
        self.assertTrue(asset_old.is_dir())
        self.assertFalse(
            (
                self.vault
                / "archive"
                / "threads"
                / self.HANDLE
                / self.EXPECTED_CANONICAL
            ).exists()
        )
        self.assertFalse(
            (
                self.vault
                / "assets"
                / "threads"
                / self.HANDLE
                / self.EXPECTED_CANONICAL
            ).exists()
        )

    def test_emit_matching_existing_name_emits_normally(self) -> None:
        """If the existing reused pair already matches the desired name,
        emit reuses it without rename and writes the fresh note + media."""
        archive_canonical, asset_canonical = self._write_existing_pair(
            dir_name=self.EXPECTED_CANONICAL,
            post_id=self.ROOT_ID,
        )
        self._write_thread()

        with TemporaryDirectory() as scratch_raw:
            emit(
                input_dir=self.input_dir,
                vault=self.vault,
                slug=None,
                archived="2026-08-24",
                force=True,
                reconcile_scratch=Path(scratch_raw),
                frozen_ids=set(),
            )

        self.assertTrue(archive_canonical.is_dir())
        self.assertTrue(asset_canonical.is_dir())
        self.assertTrue((archive_canonical / "index.md").is_file())
        self.assertTrue((asset_canonical / "thread_data.json").is_file())
        handle_dir = self.vault / "archive" / "threads" / self.HANDLE
        dirs = sorted(d.name for d in handle_dir.iterdir() if d.is_dir())
        self.assertEqual(dirs, [self.EXPECTED_CANONICAL])


if __name__ == "__main__":
    unittest.main()