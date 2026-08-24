from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from twitter.media_manifest import (
    atomic_write_json,
    find_location,
    hash_file,
    merge_item,
    merge_manifest_items,
    new_original_item,
    selected_url,
    validate_manifest,
)
from twitter.tests.helpers import NOW


class ManifestIoTests(unittest.TestCase):
    def test_hash_file_is_sha256(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "asset.bin"
            path.write_bytes(b"abc")
            self.assertEqual(
                hash_file(path),
                hashlib.sha256(b"abc").hexdigest(),
            )

    def test_atomic_write_json_replaces_complete_document(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "media.json"
            path.write_text('{"old": true}\n', encoding="utf-8")
            atomic_write_json(path, {"schema_version": 2, "items": []})
            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")),
                {"schema_version": 2, "items": []},
            )
            self.assertEqual(list(path.parent.glob(".media.json.*.tmp")), [])


class CanonicalManifestTests(unittest.TestCase):
    def test_original_has_independent_origin_and_local_locations(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            local = Path(raw) / "100_AAA_orig.png"
            local.write_bytes(b"png fixture bytes")
            item = new_original_item(
                post_id="100",
                media_id="AAA",
                handle="example",
                origin_url="https://pbs.twimg.com/media/AAA?format=png&name=orig",
                filename=local.name,
                local_path=local,
                now=NOW,
            )
            self.assertEqual(selected_url(item), item["locations"][0]["url"])
            self.assertEqual(find_location(item, "local")["integrity"], "present")
            self.assertEqual(find_location(item, "local")["sha256"], hash_file(local))

    def test_missing_local_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            local = Path(raw) / "missing.png"
            item = new_original_item(
                post_id="100",
                media_id="AAA",
                handle="example",
                origin_url="https://pbs.twimg.com/media/AAA?format=png&name=orig",
                filename=local.name,
                local_path=local,
                now=NOW,
            )
            self.assertEqual(find_location(item, "local")["integrity"], "missing")
            self.assertIsNone(find_location(item, "local")["sha256"])

    def test_merge_preserves_fallback_and_publication(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            local = Path(raw) / "100_AAA_orig.png"
            local.write_bytes(b"png fixture bytes")
            old = new_original_item(
                post_id="100",
                media_id="AAA",
                handle="example",
                origin_url="https://pbs.twimg.com/media/AAA?format=png&name=orig",
                filename=local.name,
                local_path=local,
                now=NOW,
            )
            old["locations"].append(
                {
                    "id": "fallback:catbox:fixture",
                    "kind": "fallback",
                    "provider": "catbox",
                    "url": "https://files.catbox.moe/fallback.png",
                    "sha256": find_location(old, "local")["sha256"],
                    "uploaded_at": NOW,
                    "availability": "unknown",
                    "checked_at": None,
                    "check": None,
                }
            )
            old["publication"] = {
                "selected_location_id": "fallback:catbox:fixture",
                "selected_at": NOW,
                "reason": "origin-unavailable",
            }
            fresh = new_original_item(
                post_id="100",
                media_id="AAA",
                handle="example",
                origin_url="https://pbs.twimg.com/media/AAA?format=png&name=orig",
                filename=local.name,
                local_path=local,
                now="2026-08-25T12:00:00Z",
            )
            merged = merge_item(old, fresh)
            self.assertEqual(selected_url(merged), "https://files.catbox.moe/fallback.png")
            self.assertIsNotNone(find_location(merged, "fallback:catbox:fixture"))
            self.assertEqual(merge_item(merged, fresh), merged)

    def test_merge_refuses_origin_identity_change(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            local = Path(raw) / "100_AAA_orig.png"
            local.write_bytes(b"png fixture bytes")
            old = new_original_item(
                post_id="100",
                media_id="AAA",
                handle="example",
                origin_url="https://pbs.twimg.com/media/AAA?format=png&name=orig",
                filename=local.name,
                local_path=local,
                now=NOW,
            )
            fresh = new_original_item(
                post_id="100",
                media_id="AAA",
                handle="example",
                origin_url="https://pbs.twimg.com/media/DIFFERENT?format=png&name=orig",
                filename=local.name,
                local_path=local,
                now=NOW,
            )
            with self.assertRaisesRegex(ValueError, "origin URL changed"):
                merge_item(old, fresh)

    def test_unmatched_derived_item_survives_manifest_merge(self) -> None:
        derived = {
            "post_id": "100",
            "media_id": "AAA",
            "handle": "example",
            "role": "ocr",
            "derived_from": {"post_id": "100", "media_id": "AAA", "role": "orig"},
            "embed": False,
            "locations": [],
            "publication": None,
        }
        self.assertEqual(merge_manifest_items([derived], []), [derived])

    def test_validator_rejects_local_publication(self) -> None:
        manifest = {
            "schema_version": 2,
            "root_post_id": "100",
            "items": [
                {
                    "post_id": "100",
                    "media_id": "AAA",
                    "handle": "example",
                    "role": "orig",
                    "derived_from": None,
                    "embed": True,
                    "locations": [
                        {
                            "id": "local",
                            "kind": "local",
                            "path": "100_AAA_orig.png",
                            "sha256": None,
                            "bytes": None,
                            "media_type": "image/png",
                            "integrity": "missing",
                            "verified_at": NOW,
                        }
                    ],
                    "publication": {
                        "selected_location_id": "local",
                        "selected_at": NOW,
                        "reason": "manual",
                    },
                }
            ],
            "mirrors": [],
        }
        self.assertIn("items[0] selects non-HTTPS location local", validate_manifest(manifest))


if __name__ == "__main__":
    unittest.main()