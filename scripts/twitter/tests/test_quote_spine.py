from __future__ import annotations

import json
import unittest
from argparse import Namespace
from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from twitter.emit_archive import (
    archive_for_post,
    quote_ref_for,
    render_gaps,
)
from twitter.models import PostData, PostMetrics, ThreadData
from twitter.render import _post_block, render_spine
from twitter.tree import spine_quote_ids
from twitter.tw import (
    _merge_existing_capture,
    build_parser,
    chase_spine_quotes,
    cmd_refresh,
    overlay_quote_of_ids,
)


def post(
    post_id: str,
    handle: str,
    text: str,
    reply_to_id: str | None,
    quote_of_id: str | None = None,
) -> PostData:
    return PostData(
        post_id=post_id,
        author=handle,
        handle=handle,
        text=text,
        timestamp="2025-02-09 02:35:43",
        media_urls=(),
        reply_to_id=reply_to_id,
        quote_of_id=quote_of_id,
        metrics=PostMetrics(0, 0, 0, None),
    )


class PostBlockQuoteRefTests(unittest.TestCase):
    def test_quote_ref_url_and_wikilink_before_media(self) -> None:
        quoted = post(
            "1888416459132395792",
            "AgileJebrim",
            "Check your compiler.\n\nstep() isn’t necessary however. https://t.co/ianYUdKGcc",
            None,
            "1888409333182218691",
        )
        block = _post_block(
            1,
            quoted,
            {"1888416459132395792": ("https://pbs.twimg.com/media/AAA.jpg",)},
            None,
            (
                "https://x.com/iquilezles/status/1888409333182218691",
                "archive/threads/iquilezles/2025-02-09-slug",
            ),
        )
        self.assertIn("https://t.co/ianYUdKGcc", block)
        url_at = block.index(
            "https://x.com/iquilezles/status/1888409333182218691"
        )
        wiki_at = block.index(
            "[[archive/threads/iquilezles/2025-02-09-slug]]"
        )
        media_at = block.index("https://pbs.twimg.com/media/AAA.jpg")
        self.assertLess(url_at, wiki_at)
        self.assertLess(wiki_at, media_at)

    def test_quote_ref_url_only_when_wiki_missing(self) -> None:
        quoted = post("1", "AgileJebrim", "body https://t.co/ianYUdKGcc", None, "9")
        block = _post_block(
            1,
            quoted,
            None,
            None,
            ("https://x.com/i/status/9", None),
        )
        self.assertIn("https://x.com/i/status/9\n", block)
        self.assertNotIn("[[", block)
        self.assertIn("https://t.co/ianYUdKGcc", block)

    def test_no_quote_ref_leaves_body_unchanged(self) -> None:
        quoted = post("1", "AgileJebrim", "body", None, "9")
        block = _post_block(1, quoted, None)
        self.assertNotIn("x.com", block)


class SpineQuoteIdTests(unittest.TestCase):
    def test_spine_only_unique_order(self) -> None:
        thread = ThreadData(
            root_post_id="1",
            posts=(
                post("1", "A", "qt", None, "9"),
                post("2", "B", "reply", "1"),
                post("3", "A", "qt2", "2", "8"),
                post("4", "C", "branch qt", "1", "7"),
            ),
            source_url="https://x.com/i/status/1",
        )
        self.assertEqual(spine_quote_ids(thread, ["1", "2", "3"]), ["9", "8"])

    def test_duplicate_quote_id_once(self) -> None:
        thread = ThreadData(
            root_post_id="1",
            posts=(
                post("1", "A", "a", None, "9"),
                post("2", "A", "b", "1", "9"),
            ),
            source_url="https://x.com/i/status/1",
        )
        self.assertEqual(spine_quote_ids(thread, ["1", "2"]), ["9"])


class RenderSpineQuoteTests(unittest.TestCase):
    def test_render_spine_passes_quote_ref(self) -> None:
        thread = ThreadData(
            root_post_id="1",
            posts=(post("1", "AgileJebrim", "Check your compiler.", None, "9"),),
            source_url="https://x.com/i/status/1",
        )
        text = render_spine(
            thread,
            ["1"],
            [],
            {},
            "2026-08-26",
            None,
            {"1": ("https://x.com/iquilezles/status/9", "archive/threads/iquilezles/slug")},
        )
        self.assertIn("https://x.com/iquilezles/status/9", text)
        self.assertIn("[[archive/threads/iquilezles/slug]]", text)


class MergeOmittedOpTests(unittest.TestCase):
    def test_retains_op_when_fresh_omits_root(self) -> None:
        existing = ThreadData(
            root_post_id="1",
            posts=(
                post("1", "A", "op qt", None, "9"),
                post("2", "B", "tip", "1"),
            ),
            source_url="https://x.com/i/status/1",
        )
        fresh = ThreadData(
            root_post_id="2",
            posts=(post("2", "B", "tip-fresh", "1"),),
            source_url="https://x.com/i/status/2",
        )
        merged, retained = _merge_existing_capture(fresh, existing, "2")
        ids = {p.post_id: p for p in merged.posts}
        self.assertIn("1", ids)
        self.assertEqual(ids["1"].quote_of_id, "9")
        self.assertEqual(ids["2"].text, "tip-fresh")
        self.assertEqual(retained, ("1",))


class OverlayQuoteOfIdTests(unittest.TestCase):
    def test_keeps_on_disk_when_fresh_empty(self) -> None:
        previous = ThreadData(
            root_post_id="1",
            posts=(post("1", "A", "old", None, "9"),),
            source_url="https://x.com/i/status/1",
        )
        fresh = ThreadData(
            root_post_id="1",
            posts=(post("1", "A", "new", None, None),),
            source_url="https://x.com/i/status/1",
        )
        merged = overlay_quote_of_ids(fresh, previous)
        self.assertEqual(merged.posts[0].text, "new")
        self.assertEqual(merged.posts[0].quote_of_id, "9")

    def test_fresh_nonempty_wins(self) -> None:
        previous = ThreadData(
            root_post_id="1",
            posts=(post("1", "A", "old", None, "9"),),
            source_url="https://x.com/i/status/1",
        )
        fresh = ThreadData(
            root_post_id="1",
            posts=(post("1", "A", "new", None, "8"),),
            source_url="https://x.com/i/status/1",
        )
        merged = overlay_quote_of_ids(fresh, previous)
        self.assertEqual(merged.posts[0].quote_of_id, "8")

    def test_missing_previous_post_unchanged(self) -> None:
        previous = ThreadData(
            root_post_id="1",
            posts=(post("1", "A", "old", None, "9"),),
            source_url="https://x.com/i/status/1",
        )
        fresh = ThreadData(
            root_post_id="2",
            posts=(post("2", "A", "only-fresh", None, None),),
            source_url="https://x.com/i/status/2",
        )
        merged = overlay_quote_of_ids(fresh, previous)
        self.assertIsNone(merged.posts[0].quote_of_id)


def _write_thread(path: Path, thread: ThreadData) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(asdict(thread), indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


class ArchiveForPostTests(unittest.TestCase):
    def test_finds_post_in_thread_data(self) -> None:
        with TemporaryDirectory() as tmp:
            vault = Path(tmp)
            assets = vault / "assets" / "threads" / "iquilezles" / "2025-02-09-slug"
            notes = vault / "archive" / "threads" / "iquilezles" / "2025-02-09-slug"
            notes.mkdir(parents=True)
            thread = ThreadData(
                root_post_id="9",
                posts=(post("9", "iquilezles", "quoted root", None),),
                source_url="https://x.com/iquilezles/status/9",
            )
            _write_thread(assets / "thread_data.json", thread)
            found_assets, found_notes = archive_for_post(vault, "9")
            self.assertEqual(found_assets, assets)
            self.assertEqual(found_notes, notes)
            url, wiki = quote_ref_for(vault, "9")
            self.assertEqual(url, "https://x.com/iquilezles/status/9")
            self.assertEqual(wiki, "archive/threads/iquilezles/2025-02-09-slug")

    def test_block_id_when_not_op(self) -> None:
        with TemporaryDirectory() as tmp:
            vault = Path(tmp)
            assets = vault / "assets" / "threads" / "H" / "slug"
            notes = vault / "archive" / "threads" / "H" / "slug"
            notes.mkdir(parents=True)
            thread = ThreadData(
                root_post_id="1",
                posts=(
                    post("1", "H", "op", None),
                    post("2", "H", "child", "1"),
                ),
                source_url="https://x.com/H/status/1",
            )
            _write_thread(assets / "thread_data.json", thread)
            url, wiki = quote_ref_for(vault, "2")
            self.assertEqual(url, "https://x.com/H/status/2")
            self.assertEqual(wiki, "archive/threads/H/slug#^2")

    def test_miss_uses_i_status(self) -> None:
        with TemporaryDirectory() as tmp:
            url, wiki = quote_ref_for(Path(tmp), "9")
            self.assertEqual(url, "https://x.com/i/status/9")
            self.assertIsNone(wiki)


class RenderGapsQuoteTests(unittest.TestCase):
    def test_lists_missing_quoted_ids(self) -> None:
        thread = ThreadData(
            root_post_id="1",
            posts=(post("1", "A", "qt", None, "9"),),
            source_url="https://x.com/i/status/1",
        )
        text = render_gaps(
            thread, ["1"], input_kind="tip", missing_quote_of=["9"]
        )
        self.assertIn("quote_of:\n9\n", text)
        self.assertNotIn("quote_of:\n1\n", text)

    def test_unset_when_none_missing(self) -> None:
        thread = ThreadData(
            root_post_id="1",
            posts=(post("1", "A", "qt", None, "9"),),
            source_url="https://x.com/i/status/1",
        )
        text = render_gaps(
            thread, ["1"], input_kind="tip", missing_quote_of=[]
        )
        self.assertIn("quote_of: unset\n", text)


class ParserNoQuotesTests(unittest.TestCase):
    def test_refresh_accepts_no_quotes(self) -> None:
        args = build_parser().parse_args(
            ["refresh", "--id", "1", "--tip", "--no-quotes"]
        )
        self.assertTrue(args.no_quotes)

    def test_refresh_default_chases(self) -> None:
        args = build_parser().parse_args(["refresh", "--id", "1", "--tip"])
        self.assertFalse(args.no_quotes)


class ChaseSpineQuotesTests(unittest.TestCase):
    def test_inner_refresh_is_root_no_quotes(self) -> None:
        thread = ThreadData(
            root_post_id="1",
            posts=(
                post("1", "A", "qt", None, "9"),
                post("2", "B", "reply", "1"),
                post("4", "C", "branch qt", "1", "7"),
            ),
            source_url="https://x.com/i/status/1",
        )
        calls: list[Namespace] = []

        def fake_refresh(args: Namespace) -> int:
            calls.append(args)
            return 0

        with (
            patch("twitter.tw.locate", return_value=(None, None)),
            patch("twitter.tw.check_frozen"),
            patch("twitter.tw.cmd_refresh", fake_refresh),
        ):
            chase_spine_quotes(thread, tip=True, tip_id="2")
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].id, "9")
        self.assertFalse(calls[0].tip)
        self.assertTrue(calls[0].no_quotes)
        self.assertEqual(calls[0].branch, [])

    def test_locate_hit_skips_refresh(self) -> None:
        thread = ThreadData(
            root_post_id="1",
            posts=(post("1", "A", "qt", None, "9"),),
            source_url="https://x.com/i/status/1",
        )
        calls: list[Namespace] = []

        def fake_refresh(args: Namespace) -> int:
            calls.append(args)
            return 0

        with (
            patch(
                "twitter.tw.locate",
                return_value=(Path("assets"), Path("notes")),
            ),
            patch("twitter.tw.cmd_refresh", fake_refresh),
        ):
            chase_spine_quotes(thread, tip=True, tip_id="1")
        self.assertEqual(calls, [])

    def test_frozen_skips_refresh(self) -> None:
        thread = ThreadData(
            root_post_id="1",
            posts=(post("1", "A", "qt", None, "9"),),
            source_url="https://x.com/i/status/1",
        )
        calls: list[Namespace] = []

        def fake_refresh(args: Namespace) -> int:
            calls.append(args)
            return 0

        def fake_frozen(post_id: str) -> None:
            raise SystemExit(f"frozen: skipped ({post_id})")

        with (
            patch("twitter.tw.locate", return_value=(None, None)),
            patch("twitter.tw.check_frozen", fake_frozen),
            patch("twitter.tw.cmd_refresh", fake_refresh),
        ):
            chase_spine_quotes(thread, tip=True, tip_id="1")
        self.assertEqual(calls, [])

    def test_inner_failure_does_not_raise(self) -> None:
        thread = ThreadData(
            root_post_id="1",
            posts=(post("1", "A", "qt", None, "9"),),
            source_url="https://x.com/i/status/1",
        )

        def fake_refresh(args: Namespace) -> int:
            raise SystemExit("gallery-dl failed")

        with (
            patch("twitter.tw.locate", return_value=(None, None)),
            patch("twitter.tw.check_frozen"),
            patch("twitter.tw.cmd_refresh", fake_refresh),
        ):
            chase_spine_quotes(thread, tip=True, tip_id="1")

    def test_cmd_refresh_no_quotes_skips_chase(self) -> None:
        args = Namespace(
            id="1",
            branch=[],
            tip=True,
            slug=None,
            preserve_existing=False,
            attach=[],
            allow_broken_walk=False,
            retire_old_dir=False,
            no_quotes=True,
        )
        with (
            patch("twitter.tw.check_frozen"),
            patch("twitter.tw.cmd_refetch", return_value=0),
            patch("twitter.tw.cmd_graph", return_value=0),
            patch("twitter.tw.cmd_emit", return_value=0),
            patch("twitter.tw.chase_spine_quotes") as chase,
            patch("twitter.tw.scratch_dir") as scratch,
            patch("twitter.tw.locate", return_value=(None, None)),
        ):
            scratch.return_value = Path("missing-scratch")
            result = cmd_refresh(args)
        self.assertEqual(result, 0)
        chase.assert_not_called()
