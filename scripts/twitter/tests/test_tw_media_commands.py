from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from twitter.tw import (
    _capture_ids,
    _gallery_base_args,
    _merge_gallery_files,
    _validate_capture_ids,
    build_parser,
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


if __name__ == "__main__":
    unittest.main()
