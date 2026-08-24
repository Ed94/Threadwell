from __future__ import annotations

import unittest
from pathlib import Path

from twitter.models import (
    LegacyManifest,
    LegacyThreadData,
    MediaItem,
    MediaLocation,
    MediaManifest,
    PostData,
)


class MediaLocationTests(unittest.TestCase):
    """Tests for the MediaLocation boundary dataclass."""

    def test_local_round_trip_with_path_bytes_sha(self) -> None:
        loc = MediaLocation.from_dict({
            "kind": "local",
            "local_path": "asset.png",
            "bytes": 100,
            "sha256": "abc",
        })
        self.assertEqual(loc.kind, "local")
        self.assertEqual(loc.local_path, Path("asset.png"))
        self.assertEqual(loc.bytes, 100)
        self.assertEqual(loc.sha256, "abc")
        self.assertIsNone(loc.url)
        self.assertIsNone(loc.checked_at)
        self.assertIsNone(loc.checked_status)

    def test_remote_round_trip_with_url(self) -> None:
        loc = MediaLocation.from_dict({
            "kind": "remote",
            "url": "https://example.com/asset.png",
        })
        self.assertEqual(loc.kind, "remote")
        self.assertEqual(loc.url, "https://example.com/asset.png")
        self.assertIsNone(loc.local_path)
        self.assertIsNone(loc.bytes)
        self.assertIsNone(loc.sha256)

    def test_empty_dict_raises_keyerror(self) -> None:
        with self.assertRaises(KeyError):
            MediaLocation.from_dict({})

    def test_bytes_bool_raises_typeerror(self) -> None:
        with self.assertRaisesRegex(TypeError, "bytes"):
            MediaLocation.from_dict({
                "kind": "local",
                "local_path": "/tmp/x",
                "bytes": True,
                "sha256": "abc",
            })


class MediaItemTests(unittest.TestCase):
    """Tests for the MediaItem boundary dataclass."""

    def test_image_round_trip_with_locations_tuple(self) -> None:
        item = MediaItem.from_dict({
            "post_id": "100",
            "media_id": "AAA",
            "kind": "image",
            "locations": [
                {"kind": "local", "local_path": "asset.png", "bytes": 100, "sha256": "abc"},
                {"kind": "remote", "url": "https://example.com/asset.png"},
            ],
        })
        self.assertEqual(item.post_id, "100")
        self.assertEqual(item.media_id, "AAA")
        self.assertEqual(item.kind, "image")
        self.assertIsInstance(item.locations, tuple)
        self.assertEqual(len(item.locations), 2)
        self.assertEqual(item.locations[0].kind, "local")
        self.assertEqual(item.locations[1].kind, "remote")
        self.assertIsNone(item.embed)
        self.assertIsNone(item.caption)

    def test_locations_not_list_raises_typeerror(self) -> None:
        with self.assertRaisesRegex(TypeError, "locations"):
            MediaItem.from_dict({
                "post_id": "p",
                "media_id": "m",
                "kind": "image",
                "locations": "not a list",
            })

    def test_embed_not_bool_raises_typeerror(self) -> None:
        with self.assertRaisesRegex(TypeError, "embed"):
            MediaItem.from_dict({
                "post_id": "p",
                "media_id": "m",
                "kind": "image",
                "locations": [],
                "embed": "true",
            })


class MediaManifestTests(unittest.TestCase):
    """Tests for the MediaManifest boundary dataclass."""

    def test_minimal_manifest_round_trip(self) -> None:
        manifest = MediaManifest.from_dict({
            "root_post_id": "100",
            "items": [
                {
                    "post_id": "100",
                    "media_id": "AAA",
                    "kind": "image",
                    "locations": [
                        {"kind": "local", "local_path": "x.png", "bytes": 1, "sha256": "a"},
                    ],
                }
            ],
        })
        self.assertEqual(manifest.root_post_id, "100")
        self.assertIsInstance(manifest.items, tuple)
        self.assertEqual(len(manifest.items), 1)
        self.assertEqual(manifest.items[0].media_id, "AAA")
        self.assertIsNone(manifest.captured_at)

    def test_items_not_list_raises_typeerror(self) -> None:
        with self.assertRaisesRegex(TypeError, "items"):
            MediaManifest.from_dict({"root_post_id": "p", "items": {}})


class LegacyManifestTests(unittest.TestCase):
    """Tests for the LegacyManifest boundary dataclass."""

    def test_round_trip_with_threads(self) -> None:
        manifest = LegacyManifest.from_dict({
            "threads": [
                {
                    "root_post_id": "100",
                    "posts": [],
                    "source_url": "https://x.com/example/status/100",
                }
            ],
        })
        self.assertIsInstance(manifest.threads, tuple)
        self.assertEqual(len(manifest.threads), 1)
        self.assertEqual(manifest.threads[0].root_post_id, "100")


class LegacyThreadDataTests(unittest.TestCase):
    """Tests for the LegacyThreadData boundary dataclass."""

    def test_round_trip_with_posts_tuple(self) -> None:
        thread = LegacyThreadData.from_dict({
            "root_post_id": "100",
            "source_url": "https://x.com/example/status/100",
            "posts": [
                {
                    "post_id": "100",
                    "author": "Example",
                    "handle": "example",
                    "text": "Hello",
                    "timestamp": "2026-08-24 12:00:00",
                    "media_urls": [],
                    "reply_to_id": None,
                    "quote_of_id": None,
                    "metrics": {
                        "reply_count": 0,
                        "repost_count": 0,
                        "like_count": 0,
                        "view_count": None,
                    },
                }
            ],
        })
        self.assertEqual(thread.root_post_id, "100")
        self.assertEqual(thread.source_url, "https://x.com/example/status/100")
        self.assertIsInstance(thread.posts, tuple)
        self.assertEqual(len(thread.posts), 1)
        self.assertIsInstance(thread.posts[0], PostData)
        self.assertEqual(thread.posts[0].post_id, "100")


if __name__ == "__main__":
    unittest.main()
