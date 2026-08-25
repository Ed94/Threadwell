from __future__ import annotations

import json
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from dataclasses import asdict, replace
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from twitter import tw as tw_module
from twitter.emit_archive import ReslugConflict, ReslugPlan
from twitter.models import PostData, PostMetrics, ThreadData, load_thread
from twitter.tw import (
    _capture_ids,
    _copy_selected_media,
    _gallery_base_args,
    _merge_branch_posts,
    _merge_existing_capture,
    _merge_gallery_files,
    _select_branch_capture,
    _validate_capture_ids,
    build_parser,
    cmd_add_branch,
    cmd_emit,
    cmd_reslug,
)


def make_post(post_id: str, reply_to_id: str | None) -> PostData:
    return PostData(
        post_id=post_id,
        author=post_id,
        handle=post_id,
        text=post_id,
        timestamp=f"2026-01-01 00:00:{int(post_id) % 60:02d}",
        media_urls=(),
        reply_to_id=reply_to_id,
        quote_of_id=None,
        metrics=PostMetrics(0, 0, 0, None),
    )


def write_test_thread(path: Path, thread: ThreadData) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(asdict(thread), indent=2) + "\n",
        encoding="utf-8",
    )


class TwMediaCommandTests(unittest.TestCase):
    def test_refetch_accepts_repeatable_branch(self) -> None:
        args = build_parser().parse_args([
            "refetch", "--id", "100",
            "--branch", "200",
            "--branch", "300",
        ])
        self.assertEqual(args.branch, ["200", "300"])

    def test_refresh_accepts_repeatable_branch(self) -> None:
        args = build_parser().parse_args([
            "refresh", "--id", "100", "--tip",
            "--branch", "200",
        ])
        self.assertEqual(args.branch, ["200"])

    def test_capture_ids_deduplicates_in_first_seen_order(self) -> None:
        self.assertEqual(
            _capture_ids("100", ["200", "100", "300", "200"]),
            ("100", "200", "300"),
        )

    def test_gallery_base_args_disable_retries_and_add_pacing(self) -> None:
        args = _gallery_base_args()
        self.assertEqual(args[args.index("--retries") + 1], "0")
        self.assertEqual(args[args.index("--sleep-extractor") + 1], "5")
        self.assertEqual(args[args.index("--sleep-request") + 1], "5")

    def test_merge_gallery_files_concatenates_arrays(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first.json"
            second = root / "second.json"
            output = root / "gallery.json"
            first.write_text('[{"id": "100"}]', encoding="utf-8")
            second.write_text('[{"id": "200"}]', encoding="utf-8")
            _merge_gallery_files([first, second], output)
            self.assertEqual(
                json.loads(output.read_text(encoding="utf-8")),
                [{"id": "100"}, {"id": "200"}],
            )

    def test_merge_gallery_files_rejects_non_array(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            capture = root / "capture.json"
            capture.write_text('{"id": "100"}', encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "JSON array"):
                _merge_gallery_files([capture], root / "gallery.json")

    def test_validate_capture_ids_rejects_missing_requested_id(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "thread_data.json"
            path.write_text(
                json.dumps({
                    "root_post_id": "100",
                    "source_url": "https://x.com/i/status/100",
                    "posts": [
                        {"post_id": "100", "metrics": {}},
                        {"post_id": "200", "metrics": {}},
                    ],
                }),
                encoding="utf-8",
            )
            _validate_capture_ids(path, ("100", "200"))
            with self.assertRaisesRegex(SystemExit, "300"):
                _validate_capture_ids(path, ("100", "300"))

    def test_select_branch_capture_keeps_entire_visible_subtree(self) -> None:
        existing = ThreadData(
            root_post_id="100",
            posts=(make_post("100", None),),
            source_url="https://x.com/i/status/200",
        )
        captured = ThreadData(
            root_post_id="300",
            posts=(
                make_post("100", None),
                make_post("300", "100"),
                make_post("400", "300"),
                make_post("500", "300"),
                make_post("600", "100"),
            ),
            source_url="https://x.com/i/status/300",
        )
        selected, leaves = _select_branch_capture(existing, captured, "300")
        self.assertEqual(
            tuple(post.post_id for post in selected),
            ("300", "400", "500"),
        )
        self.assertEqual(leaves, ("400", "500"))

    def test_select_branch_capture_keeps_missing_attachment_path(self) -> None:
        existing = ThreadData(
            root_post_id="100",
            posts=(make_post("100", None),),
            source_url="https://x.com/i/status/200",
        )
        captured = ThreadData(
            root_post_id="300",
            posts=(
                make_post("100", None),
                make_post("250", "100"),
                make_post("300", "250"),
                make_post("400", "300"),
            ),
            source_url="https://x.com/i/status/300",
        )
        selected, leaves = _select_branch_capture(existing, captured, "300")
        self.assertEqual(
            tuple(post.post_id for post in selected),
            ("250", "300", "400"),
        )
        self.assertEqual(leaves, ("400",))

    def test_select_branch_capture_rejects_unattached_capture(self) -> None:
        existing = ThreadData(
            root_post_id="100",
            posts=(make_post("100", None),),
            source_url="https://x.com/i/status/200",
        )
        captured = ThreadData(
            root_post_id="999",
            posts=(make_post("999", None), make_post("300", "999")),
            source_url="https://x.com/i/status/300",
        )
        with self.assertRaisesRegex(SystemExit, "does not attach"):
            _select_branch_capture(existing, captured, "300")

    def test_merge_branch_posts_preserves_existing_and_first_new_post(self) -> None:
        existing_100 = make_post("100", None)
        existing_200 = make_post("200", "100")
        existing = ThreadData(
            root_post_id="100",
            posts=(existing_100, existing_200),
            source_url="https://x.com/i/status/200",
        )
        first_300 = make_post("300", "100")
        second_300 = replace(first_300, text="replacement must not win")
        merged, added = _merge_branch_posts(
            existing,
            [
                (replace(existing_200, text="fresh duplicate"), first_300),
                (second_300, make_post("400", "300")),
            ],
        )
        self.assertEqual(merged.posts, (
            existing_100,
            existing_200,
            first_300,
            make_post("400", "300"),
        ))
        self.assertEqual(merged.root_post_id, existing.root_post_id)
        self.assertEqual(merged.source_url, existing.source_url)
        self.assertEqual(added, ("300", "400"))

    def test_copy_selected_media_copies_only_selected_post_files(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            destination = root / "destination"
            (source / "media").mkdir(parents=True)
            (destination / "media").mkdir(parents=True)
            (source / "media" / "300_1.jpg").write_bytes(b"300")
            (source / "media" / "400_1.png").write_bytes(b"400")
            (source / "media" / "600_1.jpg").write_bytes(b"600")
            (destination / "media" / "existing.jpg").write_bytes(b"old")
            copied = _copy_selected_media(
                source,
                destination,
                {"300", "400"},
            )
            self.assertEqual(
                tuple(path.name for path in copied),
                ("300_1.jpg", "400_1.png"),
            )
            self.assertEqual(
                sorted(path.name for path in (destination / "media").iterdir()),
                ["300_1.jpg", "400_1.png", "existing.jpg"],
            )

    def test_add_branch_accepts_repeatable_from_nodes(self) -> None:
        args = build_parser().parse_args([
            "add-branch",
            "--id", "200",
            "--from", "300",
            "--from", "400",
        ])
        self.assertEqual(args.id, "200")
        self.assertEqual(args.from_ids, ["300", "400"])

    def test_add_branch_stages_selected_subtree_and_keeps_spine_tip(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = root / "assets"
            notes = root / "notes"
            notes.mkdir()
            existing = ThreadData(
                root_post_id="200",
                posts=(make_post("100", None), make_post("200", "100")),
                source_url="https://x.com/i/status/200",
            )
            existing_path = assets / "thread_data.json"
            write_test_thread(existing_path, existing)
            existing_bytes = existing_path.read_bytes()

            branch_scratch = root / "refetch_300"
            captured = ThreadData(
                root_post_id="300",
                posts=(
                    make_post("100", None),
                    make_post("300", "100"),
                    make_post("400", "300"),
                    make_post("500", "300"),
                    make_post("600", "100"),
                ),
                source_url="https://x.com/i/status/300",
            )
            write_test_thread(branch_scratch / "thread_data.json", captured)
            (branch_scratch / "media").mkdir()
            for post_id in ("300", "400", "500", "600"):
                (branch_scratch / "media" / f"{post_id}_1.jpg").write_bytes(
                    post_id.encode("ascii"),
                )

            def fake_scratch(post_id: str) -> Path:
                return root / f"refetch_{post_id}"

            with (
                patch.object(tw_module, "locate", return_value=(assets, notes)),
                patch.object(tw_module, "scratch_dir", side_effect=fake_scratch),
                patch.object(tw_module, "check_frozen"),
                patch.object(tw_module, "cmd_refetch") as refetch,
                patch.object(tw_module, "cmd_emit") as emit,
            ):
                with redirect_stdout(StringIO()):
                    result = cmd_add_branch(
                        Namespace(id="200", from_ids=["300"]),
                    )

            self.assertEqual(result, 0)
            refetch_args = refetch.call_args.args[0]
            self.assertEqual(refetch_args.id, "300")
            self.assertEqual(refetch_args.branch, [])
            emit_args = emit.call_args.args[0]
            self.assertEqual(emit_args.id, "200")
            self.assertTrue(emit_args.tip)
            self.assertIsNone(emit_args.slug)

            staged = load_thread(root / "refetch_200" / "thread_data.json")
            self.assertEqual(
                tuple(post.post_id for post in staged.posts),
                ("100", "200", "300", "400", "500"),
            )
            self.assertEqual(
                sorted(path.name for path in (root / "refetch_200" / "media").iterdir()),
                ["300_1.jpg", "400_1.jpg", "500_1.jpg"],
            )
            self.assertEqual(existing_path.read_bytes(), existing_bytes)

    def test_add_branch_rejects_id_that_is_not_stored_spine_tip(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = root / "assets"
            notes = root / "notes"
            notes.mkdir()
            write_test_thread(
                assets / "thread_data.json",
                ThreadData(
                    root_post_id="100",
                    posts=(make_post("100", None), make_post("200", "100")),
                    source_url="https://x.com/i/status/100",
                ),
            )
            with (
                patch.object(tw_module, "locate", return_value=(assets, notes)),
                patch.object(tw_module, "check_frozen"),
                patch.object(
                    tw_module,
                    "cmd_refetch",
                    side_effect=AssertionError("must reject before fetch"),
                ),
            ):
                with self.assertRaisesRegex(SystemExit, "stored spine tip"):
                    cmd_add_branch(Namespace(id="200", from_ids=["300"]))

    def test_merge_existing_capture_keeps_fresh_and_retains_missing(self) -> None:
        old_100 = make_post("100", None)
        old_200 = make_post("200", "100")
        old_300 = make_post("300", "100")
        existing = ThreadData(
            root_post_id="100",
            posts=(old_100, old_200, old_300),
            source_url="https://x.com/i/status/100",
        )
        fresh_100 = replace(old_100, text="fresh root")
        fresh_200 = replace(old_200, text="fresh tip")
        fresh_400 = make_post("400", "200")
        fresh = ThreadData(
            root_post_id="200",
            posts=(fresh_100, fresh_200, fresh_400),
            source_url="https://x.com/i/status/200",
        )
        merged, retained = _merge_existing_capture(fresh, existing, "200")
        self.assertEqual(
            merged.posts,
            (fresh_100, fresh_200, fresh_400, old_300),
        )
        self.assertEqual(merged.root_post_id, "200")
        self.assertEqual(merged.source_url, fresh.source_url)
        self.assertEqual(retained, ("300",))

    def test_merge_existing_capture_rejects_different_conversation(self) -> None:
        existing = ThreadData(
            root_post_id="100",
            posts=(make_post("100", None),),
            source_url="https://x.com/i/status/100",
        )
        fresh = ThreadData(
            root_post_id="200",
            posts=(make_post("200", None),),
            source_url="https://x.com/i/status/200",
        )
        with self.assertRaisesRegex(SystemExit, "different conversation"):
            _merge_existing_capture(fresh, existing, "200")

    def test_emit_and_refresh_accept_preserve_existing(self) -> None:
        emit_args = build_parser().parse_args([
            "emit", "--id", "200", "--tip", "--preserve-existing",
        ])
        refresh_args = build_parser().parse_args([
            "refresh", "--id", "200", "--tip", "--preserve-existing",
        ])
        self.assertTrue(emit_args.preserve_existing)
        self.assertTrue(refresh_args.preserve_existing)

    def test_emit_preserve_existing_merges_before_running_emitter(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            scratch = root / "refetch_200"
            assets = root / "assets"
            notes = root / "notes"
            notes.mkdir()
            existing = ThreadData(
                root_post_id="100",
                posts=(
                    make_post("100", None),
                    make_post("200", "100"),
                    make_post("300", "100"),
                ),
                source_url="https://x.com/i/status/100",
            )
            fresh = ThreadData(
                root_post_id="200",
                posts=(
                    replace(make_post("100", None), text="fresh"),
                    replace(make_post("200", "100"), text="fresh"),
                    make_post("400", "200"),
                ),
                source_url="https://x.com/i/status/200",
            )
            write_test_thread(assets / "thread_data.json", existing)
            write_test_thread(scratch / "thread_data.json", fresh)
            with (
                patch.object(tw_module, "scratch_dir", return_value=scratch),
                patch.object(tw_module, "dump_dir", return_value=root / "dump"),
                patch.object(tw_module, "locate", return_value=(assets, notes)),
                patch.object(tw_module, "locate_all", return_value=[]),
                patch.object(tw_module, "check_frozen"),
                patch.object(tw_module, "run") as run,
                redirect_stdout(StringIO()),
            ):
                result = cmd_emit(Namespace(
                    id="200",
                    tip=True,
                    slug=None,
                    preserve_existing=True,
                ))
            self.assertEqual(result, 0)
            self.assertTrue(run.called)
            merged = load_thread(scratch / "thread_data.json")
            self.assertEqual(
                tuple(post.post_id for post in merged.posts),
                ("100", "200", "400", "300"),
            )
            self.assertEqual(merged.root_post_id, "200")

    def test_migrate_defaults_to_dry_run(self) -> None:
        args = build_parser().parse_args(["migrate-media", "--id", "100"])
        self.assertEqual(args.cmd, "migrate-media")
        self.assertFalse(args.apply)

    def test_fallback_requires_exact_media(self) -> None:
        args = build_parser().parse_args(
            [
                "fallback",
                "--id",
                "100",
                "--media-id",
                "AAA",
                "--role",
                "orig",
                "--confirm-origin-unavailable",
            ]
        )
        self.assertEqual(args.media_id, "AAA")
        self.assertTrue(args.confirm_origin_unavailable)


class ReslugCommandParserTests(unittest.TestCase):
    def test_reslug_parser_dry_run_defaults(self) -> None:
        args = build_parser().parse_args(["reslug", "--all"])
        self.assertEqual(args.cmd, "reslug")
        self.assertTrue(args.all_threads)
        self.assertFalse(args.apply)

    def test_reslug_parser_apply_flag(self) -> None:
        args = build_parser().parse_args(["reslug", "--all", "--apply"])
        self.assertEqual(args.cmd, "reslug")
        self.assertTrue(args.all_threads)
        self.assertTrue(args.apply)


class ReslugCommandDispatchTests(unittest.TestCase):
    def test_reslug_dry_run_does_not_apply(self) -> None:
        plan = ReslugPlan(
            vault=Path("/tmp"),
            moves=(),
            noops=(),
            frozen=(),
            frozen_dirs=(),
            conflicts=(),
        )
        with (
            patch.object(tw_module, "plan_reslug", return_value=plan) as plan_fn,
            patch.object(tw_module, "format_reslug_plan", return_value="") as fmt,
            patch.object(tw_module, "apply_reslug_plan") as apply,
            redirect_stdout(StringIO()),
        ):
            result = cmd_reslug(Namespace(all_threads=True, apply=False))
        self.assertEqual(result, 0)
        plan_fn.assert_called_once()
        fmt.assert_called_once()
        apply.assert_not_called()

    def test_reslug_conflicts_return_two_without_apply(self) -> None:
        plan = ReslugPlan(
            vault=Path("/tmp"),
            moves=(),
            noops=(),
            frozen=(),
            frozen_dirs=(),
            conflicts=(ReslugConflict(Path("/tmp/x"), "bad"),),
        )
        with (
            patch.object(tw_module, "plan_reslug", return_value=plan),
            patch.object(tw_module, "format_reslug_plan", return_value=""),
            patch.object(tw_module, "apply_reslug_plan") as apply,
            redirect_stdout(StringIO()),
        ):
            result = cmd_reslug(Namespace(all_threads=True, apply=False))
        self.assertEqual(result, 2)
        apply.assert_not_called()

    def test_reslug_clean_apply_calls_apply_once_with_plan_and_scratch(self) -> None:
        plan = ReslugPlan(
            vault=Path("/tmp"),
            moves=(),
            noops=(),
            frozen=(),
            frozen_dirs=(),
            conflicts=(),
        )
        with (
            patch.object(tw_module, "plan_reslug", return_value=plan),
            patch.object(tw_module, "format_reslug_plan", return_value=""),
            patch.object(tw_module, "apply_reslug_plan", return_value=()) as apply,
            redirect_stdout(StringIO()),
        ):
            result = cmd_reslug(Namespace(all_threads=True, apply=True))
        self.assertEqual(result, 0)
        apply.assert_called_once()
        positional = apply.call_args.args
        self.assertEqual(positional[0], plan)
        self.assertEqual(positional[1], tw_module.SCRATCH)


class ReslugParserNoCrossContaminationTests(unittest.TestCase):
    def test_emit_and_refresh_parser_have_no_reslug_attr(self) -> None:
        emit_args = build_parser().parse_args(["emit", "--id", "100"])
        refresh_args = build_parser().parse_args(["refresh", "--id", "100"])
        self.assertFalse(hasattr(emit_args, "reslug"))
        self.assertFalse(hasattr(refresh_args, "reslug"))


if __name__ == "__main__":
    unittest.main()
