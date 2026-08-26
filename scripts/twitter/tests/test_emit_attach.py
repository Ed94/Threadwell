"""Emit --attach, broken-walk abort, and leftover-dir retire."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from twitter.emit_archive import emit
from twitter.models import PostData, PostMetrics, ThreadData


def post(
    post_id: str,
    handle: str,
    text: str,
    reply_to: str | None,
    timestamp: str = "2025-02-25 12:00:00",
) -> dict:
    return {
        "post_id": post_id,
        "author": handle,
        "handle": handle,
        "text": text,
        "timestamp": timestamp,
        "media_urls": [],
        "reply_to_id": reply_to,
        "quote_of_id": None,
        "metrics": {
            "reply_count": 0,
            "repost_count": 0,
            "like_count": 0,
            "view_count": 0,
        },
    }


class EmitAttachTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="emit_attach_"))
        self.input_dir = self.tmp / "input"
        self.input_dir.mkdir()
        self.vault = self.tmp / "vault"
        (self.vault / "archive" / "threads").mkdir(parents=True)
        (self.vault / "assets" / "threads").mkdir(parents=True)
        self._write(
            [
                post("1", "levelsio", "IT WORKS", None, "2025-02-25 16:00:00"),
                post(
                    "2",
                    "Jonathan_Blow",
                    "overview",
                    "deleted",
                    "2025-02-25 22:00:00",
                ),
                post(
                    "3",
                    "Jonathan_Blow",
                    "udp nat",
                    "2",
                    "2025-02-25 22:10:00",
                ),
            ]
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, posts: list[dict]) -> None:
        (self.input_dir / "thread_data.json").write_text(
            json.dumps(
                {
                    "root_post_id": "3",
                    "source_url": "https://x.com/i/status/3",
                    "posts": posts,
                },
                indent=2,
            ),
            encoding="utf-8",
            newline="\n",
        )

    def test_attach_walks_tip_to_op(self) -> None:
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-25",
            force=True,
            tip="3",
            attaches=(("2", "1"),),
        )
        note = (
            self.vault
            / "archive"
            / "threads"
            / "levelsio"
            / "2025-02-25-it-works"
            / "index.md"
        )
        text = note.read_text(encoding="utf-8")
        self.assertIn("**1/** **@levelsio** ^1", text)
        self.assertIn("**2/** **@Jonathan_Blow** ^2", text)
        self.assertIn("**3/** **@Jonathan_Blow** ^3", text)

    def test_broken_walk_aborts_without_override(self) -> None:
        with self.assertRaisesRegex(SystemExit, "missing_parent=deleted"):
            emit(
                input_dir=self.input_dir,
                vault=self.vault,
                slug=None,
                archived="2026-08-25",
                force=True,
                tip="3",
            )

    def test_allow_broken_walk_emits_short_spine(self) -> None:
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-25",
            force=True,
            tip="3",
            allow_broken_walk=True,
        )
        note = (
            self.vault
            / "archive"
            / "threads"
            / "Jonathan_Blow"
            / "2025-02-25-overview"
            / "index.md"
        )
        text = note.read_text(encoding="utf-8")
        self.assertIn("**1/** **@Jonathan_Blow** ^2", text)
        self.assertNotIn("@levelsio", text)

    def test_leftover_dir_aborts_without_override(self) -> None:
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-25",
            force=True,
            tip="3",
            allow_broken_walk=True,
        )
        with self.assertRaisesRegex(SystemExit, "leftover dir"):
            emit(
                input_dir=self.input_dir,
                vault=self.vault,
                slug=None,
                archived="2026-08-25",
                force=True,
                tip="3",
                attaches=(("2", "1"),),
            )

    def test_retire_old_dir_removes_foreign_handle(self) -> None:
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-25",
            force=True,
            tip="3",
            allow_broken_walk=True,
        )
        old = (
            self.vault
            / "archive"
            / "threads"
            / "Jonathan_Blow"
            / "2025-02-25-overview"
        )
        self.assertTrue(old.is_dir())
        emit(
            input_dir=self.input_dir,
            vault=self.vault,
            slug=None,
            archived="2026-08-25",
            force=True,
            tip="3",
            attaches=(("2", "1"),),
            retire_old_dir=True,
        )
        self.assertFalse(old.is_dir())
        note = (
            self.vault
            / "archive"
            / "threads"
            / "levelsio"
            / "2025-02-25-it-works"
            / "index.md"
        )
        self.assertTrue(note.is_file())
