from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from twitter.media_audit import (
    AuditReport,
    audit_local_item,
    audit_thread,
    check_origin_url,
    classify_origin_response,
    record_origin_check,
)
from twitter.media_manifest import (
    atomic_write_json,
    find_location,
    hash_file,
    new_original_item,
)
from twitter.media_migrate import migrate_legacy_thread
from twitter.models import (
    LegacyMediaJson,
    MediaItem,
    MediaManifest,
    OriginCheck,
)
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
        self.assertEqual(outcome.result, "error")
        self.assertFalse(outcome.confirms_unavailable)

    def test_frozen_thread_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            asset_dir, _note_dir = legacy_thread(root / "assets", root / "notes")
            migrate_legacy_thread(asset_dir, root / "notes", now=NOW, apply=True)
            report = audit_thread(asset_dir, root / "notes", {"100"})
            self.assertEqual(report.frozen, True)
            self.assertTrue(any("frozen: skipped" in issue for issue in report.issues))


class OriginCheckTests(unittest.TestCase):
    """Tests for the OriginCheck boundary dataclass and its producers."""

    def test_classify_available_2xx_marks_available(self) -> None:
        outcome = classify_origin_response(200, "HEAD completed", NOW)
        self.assertEqual(outcome.status, 200)
        self.assertEqual(outcome.result, "available")
        self.assertFalse(outcome.confirms_unavailable)

    def test_classify_truncates_detail_to_200_chars(self) -> None:
        long_detail = "x" * 500
        outcome = classify_origin_response(500, long_detail, NOW)
        self.assertEqual(len(outcome.detail), 200)

    def test_check_origin_url_uses_opener(self) -> None:
        class _FakeResponse:
            status = 200

            def __enter__(self) -> "_FakeResponse":
                return self

            def __exit__(self, *args: object) -> None:
                return None

        def fake_opener(*args: object, **kwargs: object) -> _FakeResponse:
            return _FakeResponse()

        outcome = check_origin_url(
            "https://example.com/x.png",
            NOW,
            opener=fake_opener,
        )
        self.assertEqual(outcome.result, "available")
        self.assertEqual(outcome.status, 200)


class RecordOriginCheckTests(unittest.TestCase):
    """Tests for the record_origin_check round-trip helper."""

    def test_record_check_updates_origin_x_location(self) -> None:
        item = new_original_item(
            post_id="100",
            media_id="AAA",
            handle="example",
            origin_url="https://pbs.twimg.com/media/AAA",
            filename="asset.png",
            local_path=Path("asset.png"),
            now=NOW,
        )
        manifest = LegacyMediaJson.from_dict(
            {
                "schema_version": 2,
                "root_post_id": "100",
                "items": [
                    {
                        "post_id": item.post_id,
                        "media_id": item.media_id,
                        "kind": item.kind,
                        "role": item.role,
                        "handle": item.handle,
                        "locations": [
                            {
                                "kind": loc.kind,
                                "id": loc.id,
                                "url": loc.url,
                                "provider": loc.provider,
                                "availability": loc.availability,
                            }
                            for loc in item.locations
                        ],
                        "publication": {
                            "selected_location_id": "origin:x",
                            "selected_at": NOW,
                            "reason": "default",
                        },
                    }
                ],
            }
        )
        outcome = classify_origin_response(200, "HEAD completed", NOW)
        updated = record_origin_check(manifest, 0, outcome)
        updated_item: MediaItem = updated.items[0]
        origin = find_location(updated_item, "origin:x")
        self.assertIsNotNone(origin)
        self.assertEqual(origin.checked_at, NOW)
        self.assertEqual(origin.checked_status, 200)
        self.assertEqual(origin.availability, "available")
        self.assertIsNotNone(origin.check)
        self.assertEqual(origin.check.result, "available")

    def test_record_check_out_of_range_raises(self) -> None:
        manifest = LegacyMediaJson.from_dict(
            {"root_post_id": "100", "items": []}
        )
        outcome = classify_origin_response(200, "HEAD", NOW)
        with self.assertRaises(ValueError):
            record_origin_check(manifest, 0, outcome)


class LegacyMediaJsonTests(unittest.TestCase):
    """Tests for the LegacyMediaJson boundary dataclass."""

    def test_minimal_legacy_round_trip(self) -> None:
        legacy = LegacyMediaJson.from_dict(
            {
                "root_post_id": "100",
                "items": [
                    {
                        "post_id": "100",
                        "media_id": "AAA",
                        "role": "orig",
                        "filename": "x.png",
                        "url": "https://files.catbox.moe/x.png",
                    }
                ],
            }
        )
        self.assertEqual(legacy.root_post_id, "100")
        self.assertIsNone(legacy.schema_version)
        self.assertEqual(len(legacy.items), 1)
        self.assertEqual(legacy.items[0].filename, "x.png")
        self.assertEqual(legacy.items[0].url, "https://files.catbox.moe/x.png")
        self.assertEqual(legacy.items[0].locations, ())
        self.assertIsNone(legacy.mirrors)
        self.assertIsNone(legacy.frozen)

    def test_v2_with_mirrors_dict(self) -> None:
        legacy = LegacyMediaJson.from_dict(
            {
                "schema_version": 2,
                "root_post_id": "100",
                "captured_at": NOW,
                "frozen": True,
                "mirrors": {
                    "dest1": {"destination_id": "dest1", "state": "synced"},
                },
                "items": [],
            }
        )
        self.assertEqual(legacy.schema_version, 2)
        self.assertEqual(legacy.captured_at, NOW)
        self.assertEqual(legacy.frozen, True)
        self.assertIsNotNone(legacy.mirrors)
        self.assertIn("dest1", legacy.mirrors)

    def test_mirrors_list_wire_is_coerced_to_dict(self) -> None:
        legacy = LegacyMediaJson.from_dict(
            {
                "root_post_id": "100",
                "items": [],
                "mirrors": [
                    {"destination_id": "alpha", "state": "synced"},
                    {"destination_id": "beta", "state": "synced"},
                ],
            }
        )
        self.assertIsNotNone(legacy.mirrors)
        self.assertEqual(set(legacy.mirrors), {"alpha", "beta"})

    def test_missing_root_post_id_raises_keyerror(self) -> None:
        with self.assertRaises(KeyError):
            LegacyMediaJson.from_dict({"items": []})

    def test_items_not_list_raises_typeerror(self) -> None:
        with self.assertRaisesRegex(TypeError, "items"):
            LegacyMediaJson.from_dict({"root_post_id": "100", "items": {}})

    def test_mirrors_invalid_type_raises_typeerror(self) -> None:
        with self.assertRaisesRegex(TypeError, "mirrors"):
            LegacyMediaJson.from_dict(
                {"root_post_id": "100", "items": [], "mirrors": "nope"}
            )


if __name__ == "__main__":
    unittest.main()