from __future__ import annotations

import unittest

from twitter.tw import build_parser


class TwMediaCommandTests(unittest.TestCase):
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