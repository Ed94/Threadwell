from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from twitter.media_manifest import (
    atomic_write_json,
    canonical_manifest_bytes,
    find_location,
    hash_file,
    merge_item,
    merge_manifest_items,
    new_original_item,
    payload_inventory,
    selected_url,
    validate_manifest,
    _from_wire_dict,
)
from twitter.models import MediaItem, MediaLocation, MediaManifest, Publication
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
            self.assertEqual(selected_url(item), item.locations[0].url)
            self.assertEqual(find_location(item, "local").integrity, "present")
            self.assertEqual(find_location(item, "local").sha256, hash_file(local))

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
            self.assertEqual(find_location(item, "local").integrity, "missing")
            self.assertIsNone(find_location(item, "local").sha256)

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
            local_sha = find_location(old, "local").sha256
            fallback = MediaLocation(
                id="fallback:catbox:fixture",
                kind="fallback",
                provider="catbox",
                url="https://files.catbox.moe/fallback.png",
                sha256=local_sha,
                uploaded_at=NOW,
                availability="unknown",
            )
            old_with_fallback = MediaItem(
                post_id=old.post_id,
                media_id=old.media_id,
                kind=old.kind,
                role=old.role,
                handle=old.handle,
                embed=old.embed,
                locations=old.locations + (fallback,),
                publication=Publication(
                    selected_location_id="fallback:catbox:fixture",
                    selected_at=NOW,
                    reason="origin-unavailable",
                ),
            )
            fresh = new_original_item(
                post_id="100",
                media_id="AAA",
                handle="example",
                origin_url="https://pbs.twimg.com/media/AAA?format=png&name=orig",
                filename=local.name,
                local_path=local,
                now="2026-08-25T12:00:00Z",
            )
            merged = merge_item(old_with_fallback, fresh)
            self.assertEqual(
                selected_url(merged), "https://files.catbox.moe/fallback.png"
            )
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
        derived = MediaItem(
            post_id="100",
            media_id="AAA",
            kind="ocr",
            role="ocr",
            handle="example",
            locations=(),
            publication=None,
        )
        result = merge_manifest_items((), (derived,))
        self.assertEqual(result, (derived,))

    def test_validator_rejects_local_publication(self) -> None:
        item = MediaItem(
            post_id="100",
            media_id="AAA",
            kind="orig",
            role="orig",
            handle="example",
            embed=True,
            locations=(
                MediaLocation(
                    id="local",
                    kind="local",
                    local_path=Path("100_AAA_orig.png"),
                    sha256=None,
                    bytes=None,
                    media_type="image/png",
                    integrity="missing",
                    verified_at=NOW,
                ),
            ),
            publication=Publication(
                selected_location_id="local",
                selected_at=NOW,
                reason="manual",
            ),
        )
        manifest = MediaManifest(
            schema_version=2,
            root_post_id="100",
            items=(item,),
        )
        self.assertIn(
            "items[0] selects non-HTTPS location local", validate_manifest(manifest)
        )


class FromWireDictTests(unittest.TestCase):
    """Tests for the _from_wire_dict boundary parser."""

    def test_full_wire_payload_round_trips(self) -> None:
        raw: dict = {
            "schema_version": 2,
            "root_post_id": "100",
            "captured_at": NOW,
            "items": [
                {
                    "post_id": "100",
                    "media_id": "AAA",
                    "role": "orig",
                    "embed": True,
                    "locations": [
                        {
                            "id": "origin:x",
                            "kind": "origin",
                            "provider": "x",
                            "url": "https://pbs.twimg.com/media/AAA",
                            "availability": "unknown",
                            "checked_at": None,
                        },
                        {
                            "id": "local",
                            "kind": "local",
                            "path": "100_AAA_orig.png",
                            "sha256": "deadbeef",
                            "bytes": 12345,
                            "media_type": "image/png",
                            "integrity": "present",
                            "verified_at": NOW,
                        },
                    ],
                    "publication": {
                        "selected_location_id": "origin:x",
                        "selected_at": NOW,
                        "reason": "default",
                    },
                }
            ],
            "mirrors": [],
        }
        manifest = _from_wire_dict(raw)
        self.assertEqual(manifest.schema_version, 2)
        self.assertEqual(manifest.root_post_id, "100")
        self.assertEqual(manifest.captured_at, NOW)
        self.assertEqual(len(manifest.items), 1)
        item = manifest.items[0]
        self.assertEqual(item.post_id, "100")
        self.assertEqual(item.media_id, "AAA")
        self.assertEqual(item.kind, "orig")
        self.assertEqual(item.embed, True)
        self.assertEqual(len(item.locations), 2)
        loc0, loc1 = item.locations
        self.assertEqual(loc0.id, "origin:x")
        self.assertEqual(loc0.kind, "origin")
        self.assertEqual(loc0.url, "https://pbs.twimg.com/media/AAA")
        self.assertEqual(loc0.provider, "x")
        self.assertEqual(loc0.availability, "unknown")
        self.assertEqual(loc1.id, "local")
        self.assertEqual(loc1.kind, "local")
        self.assertEqual(loc1.integrity, "present")
        self.assertEqual(loc1.sha256, "deadbeef")
        self.assertEqual(loc1.bytes, 12345)
        self.assertIsNotNone(item.publication)
        assert item.publication is not None
        self.assertEqual(item.publication.selected_location_id, "origin:x")
        self.assertEqual(item.publication.reason, "default")

    def test_minimal_wire_payload(self) -> None:
        raw: dict = {
            "schema_version": 2,
            "root_post_id": "100",
            "items": [
                {
                    "post_id": "100",
                    "media_id": "AAA",
                    "role": "orig",
                    "locations": [],
                }
            ],
        }
        manifest = _from_wire_dict(raw)
        self.assertEqual(manifest.root_post_id, "100")
        self.assertEqual(len(manifest.items), 1)
        self.assertEqual(manifest.items[0].kind, "orig")

    def test_wire_payload_with_derived_from(self) -> None:
        raw: dict = {
            "schema_version": 2,
            "root_post_id": "100",
            "items": [
                {
                    "post_id": "100",
                    "media_id": "AAA",
                    "role": "ocr",
                    "derived_from": {
                        "post_id": "100",
                        "media_id": "AAA",
                        "role": "orig",
                    },
                    "embed": False,
                    "locations": [],
                    "publication": None,
                }
            ],
        }
        manifest = _from_wire_dict(raw)
        item = manifest.items[0]
        self.assertEqual(item.kind, "ocr")
        self.assertIsNotNone(item.derived_from)
        assert item.derived_from is not None
        self.assertEqual(item.derived_from.role, "orig")
        self.assertIsNone(item.publication)


class CanonicalManifestBytesTests(unittest.TestCase):
    """Tests for canonical_manifest_bytes with typed MediaManifest."""

    def test_canonical_manifest_bytes_is_stable(self) -> None:
        manifest = MediaManifest(
            schema_version=2,
            root_post_id="100",
            items=(
                MediaItem(
                    post_id="100",
                    media_id="AAA",
                    kind="orig",
                    role="orig",
                    locations=(
                        MediaLocation(
                            id="origin:x",
                            kind="origin",
                            url="https://pbs.twimg.com/media/AAA",
                            availability="unknown",
                        ),
                    ),
                    publication=Publication(
                        selected_location_id="origin:x",
                        selected_at=NOW,
                        reason="default",
                    ),
                ),
            ),
        )
        first = canonical_manifest_bytes(manifest)
        second = canonical_manifest_bytes(manifest)
        self.assertEqual(first, second)
        decoded = json.loads(first.decode("utf-8"))
        self.assertEqual(decoded["schema_version"], 2)
        self.assertEqual(decoded["root_post_id"], "100")
        self.assertEqual(decoded["mirrors"], [])
        self.assertEqual(len(decoded["items"]), 1)
        self.assertEqual(decoded["items"][0]["media_id"], "AAA")

    def test_canonical_manifest_bytes_omits_mirrors_and_canonicalizes(self) -> None:
        manifest = MediaManifest(
            schema_version=2,
            root_post_id="100",
            items=(
                MediaItem(
                    post_id="100",
                    media_id="AAA",
                    kind="orig",
                    role="orig",
                    locations=(
                        MediaLocation(
                            id="origin:x",
                            kind="origin",
                            url="https://x",
                            availability="unknown",
                        ),
                    ),
                    publication=Publication(
                        selected_location_id="origin:x",
                        selected_at=NOW,
                        reason="default",
                    ),
                ),
            ),
        )
        encoded = canonical_manifest_bytes(manifest)
        self.assertIn(b'"mirrors":[]', encoded)


if __name__ == "__main__":
    unittest.main()
