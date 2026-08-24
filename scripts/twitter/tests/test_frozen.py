from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from twitter.frozen import frozen_match, load_frozen_ids
from twitter.tests.helpers import write_json


class FrozenTests(unittest.TestCase):
    def test_descendant_id_freezes_entire_thread(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            frozen_file = root / "do_not_refetch.txt"
            frozen_file.write_text("# comment\n200\n", encoding="utf-8")
            asset_dir = root / "thread"
            write_json(
                asset_dir / "thread_data.json",
                {
                    "root_post_id": "100",
                    "posts": [
                        {"post_id": "100"},
                        {"post_id": "200"},
                    ],
                },
            )
            write_json(asset_dir / "media.json", {"root_post_id": "100", "items": []})
            self.assertEqual(load_frozen_ids(frozen_file), {"200"})
            self.assertEqual(frozen_match(asset_dir, {"200"}), "200")

    def test_unrelated_thread_is_writable(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            asset_dir = Path(raw) / "thread"
            write_json(
                asset_dir / "thread_data.json",
                {"root_post_id": "100", "posts": [{"post_id": "100"}]},
            )
            write_json(asset_dir / "media.json", {"root_post_id": "100", "items": []})
            self.assertIsNone(frozen_match(asset_dir, {"200"}))


if __name__ == "__main__":
    unittest.main()