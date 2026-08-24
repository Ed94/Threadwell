from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from twitter.media_audit import (
    AuditReport,
    audit_local_item,
    audit_thread,
    classify_origin_response,
)
from twitter.media_manifest import (
    atomic_write_json,
    find_location,
    hash_file,
    new_original_item,
)
from twitter.media_migrate import migrate_legacy_thread
from twitter.tests.helpers import NOW, legacy_thread, read_json


class MediaAuditTests(unittest.TestCase):
    def test_changed_local_bytes_are_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "asset.png"
            path.write_bytes(b"first")
            item = new_original_item(
                post_id="100",
                media_id="AAA",
                handle="example",
                origin_url="https://pbs.twimg.com/media/AAA?format=png&name=orig",
                filename=path.name,
                local_path=path,
                now=NOW,
            )
            path.write_bytes(b"changed")
            issue = audit_local_item(item, path.parent)
            self.assertEqual(issue, "100/AAA/orig local mismatch")

    def test_rate_limit_does_not_mean_unavailable(self) -> None:
        outcome = classify_origin_response(429, "rate limited", NOW)
        self.assertEqual(outcome["result"], "error")
        self.assertFalse(outcome["confirms_unavailable"])

    def test_frozen_thread_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            asset_dir, _note_dir = legacy_thread(root / "assets", root / "notes")
            migrate_legacy_thread(asset_dir, root / "notes", now=NOW, apply=True)
            report = audit_thread(asset_dir, root / "notes", {"100"})
            self.assertEqual(report.frozen, True)
            self.assertTrue(any("frozen: skipped" in issue for issue in report.issues))


if __name__ == "__main__":
    unittest.main()