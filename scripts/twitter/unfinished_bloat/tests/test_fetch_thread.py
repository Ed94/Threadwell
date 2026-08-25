"""Offline tests for ``twitter.fetch_thread``. Zero network calls.

Task 2 boundary tests: parse a sanitized ``tip_tweet_detail.json``
fixture into the fetcher-local :class:`TweetDetailPage` whose
``posts`` are the existing :class:`models.PostData` instances.
Asserts exactly five posts on the tip spine, the resolved
``focal_conversation_id`` is the known root, note-tweet text wins
over ``legacy.full_text``, current-shape user core maps cleanly,
visibility-wrapped tweets unwrap, photo URLs land in
``media_urls``, the highest-bitrate MP4 variant is selected, and
numeric-string view counts parse to ``int``.

The :class:`Cursor` and :class:`TweetDetailPage` types are
fetcher-local; only those two new dataclasses appear in this
task. The :class:`Cursor`\s ``__post_init__`` rejects ineligible
cursor kinds at construction time; the parser never reaches
construction for Top or unknown kinds.

Task 8 tests: :class:`RequestGovernor` is the global, human-paced
request envelope that wraps every provider call. The walker stays
pure (no pacing, no cap, no roles of its own). The governor owns
the only request count, the only pacing, and the only ordered
``roles`` log. Tests use the actual ``RecordingSleeper`` from
Task 1; no clock is involved (the governor does not poll time).
"""
from __future__ import annotations

import unittest

from twitter.fetch_thread import (
    AuthError,
    Cursor,
    FetchError,
    ProviderError,
    RateLimitError,
    RequestBudgetExceeded,
    RequestGovernor,
    Sleeper,
    TweetDetailPage,
    issue_provider_request,
    parse_tweet_detail_page,
    resolve_root_from_tip,
    walk_continuation_queue,
)
from twitter.models import PostData, PostMetrics
from twitter.tests.fetch_thread_helpers import (
    EXPECTED_16,
    KNOWN_ROOT_ID,
    KNOWN_TIP_ID,
    RecordingSleeper,
    load_json_fixture,
)

TIP_ID = KNOWN_TIP_ID
ROOT_ID = KNOWN_ROOT_ID
WADETB_ID = "1651056827839180800"
KENPEX_ID = "1651253961524142081"
LOTTES_ID = "1651268028795961344"


class TipPageParserTests(unittest.TestCase):
    """The fixture exercises one TimelineAddEntries instruction
    containing one top-level TimelineTimelineItem (root) and one
    TimelineTimelineModule (``content.items[]``) wrapping four
    payload items plus one Top cursor. Parser must produce 5
    posts, 0 cursors, focal_id == root."""

    def setUp(self) -> None:
        self.raw = load_json_fixture("tip_tweet_detail")

    def test_parse_returns_exactly_five_post_data_with_exact_id_set(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=TIP_ID)
        self.assertIsInstance(page, TweetDetailPage)
        self.assertEqual(len(page.posts), 5)
        ids = {p.post_id for p in page.posts}
        self.assertEqual(
            ids,
            {ROOT_ID, WADETB_ID, KENPEX_ID, LOTTES_ID, TIP_ID},
        )
        # Each post is an existing models.PostData instance with
        # an existing models.PostMetrics metrics field; no
        # fetcher-local duplicates are introduced.
        for post in page.posts:
            self.assertIsInstance(post, PostData)
            self.assertIsInstance(post.metrics, PostMetrics)

    def test_parent_chain_walks_root_to_tip_in_order(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=TIP_ID)
        by_id = {p.post_id: p for p in page.posts}
        expected_chain = [
            (TIP_ID, LOTTES_ID),
            (LOTTES_ID, KENPEX_ID),
            (KENPEX_ID, WADETB_ID),
            (WADETB_ID, ROOT_ID),
            (ROOT_ID, None),
        ]
        for post_id, parent_id in expected_chain:
            self.assertEqual(
                by_id[post_id].reply_to_id,
                parent_id,
                msg=f"post {post_id}: parent mismatch",
            )

    def test_focal_conversation_id_resolves_to_root(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=TIP_ID)
        self.assertEqual(page.focal_conversation_id, ROOT_ID)

    def test_tip_page_has_zero_eligible_cursors(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=TIP_ID)
        self.assertEqual(page.cursors, ())
        self.assertEqual(len(page.cursors), 0)

    def test_note_tweet_text_overrides_legacy_full_text(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=TIP_ID)
        kenpex = next(p for p in page.posts if p.post_id == KENPEX_ID)
        self.assertEqual(
            kenpex.text,
            "fixture-note-tweet-text-kenpex-override",
        )

    def test_current_core_user_mapping(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=TIP_ID)
        root = next(p for p in page.posts if p.post_id == ROOT_ID)
        self.assertEqual(root.author, "fixture-author-root")
        self.assertEqual(root.handle, "fixture-handle-root")
        # The legacy string on user_results.result is deliberately
        # different in the fixture; the current core shape must
        # win and the legacy fallback must NOT leak through.
        self.assertNotIn("legacy-should-be-ignored", root.author)
        self.assertNotIn("legacy-should-be-ignored", root.handle)
        tip = next(p for p in page.posts if p.post_id == TIP_ID)
        self.assertEqual(tip.author, "fixture-author-tip")
        self.assertEqual(tip.handle, "fixture-handle-tip")

    def test_visibility_wrapped_lottes_post_is_parsed(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=TIP_ID)
        lottes = next(p for p in page.posts if p.post_id == LOTTES_ID)
        self.assertEqual(lottes.post_id, LOTTES_ID)
        # visibility wrapper must be unwrapped; text reaches the
        # parser through the inner Tweet.
        self.assertEqual(lottes.text, "fixture-text-lottes")

    def test_photo_url_lands_in_media_urls(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=TIP_ID)
        wadetb = next(p for p in page.posts if p.post_id == WADETB_ID)
        self.assertIn(
            "https://pbs.twimg.com/media/fixture-photo-wadetb.jpg",
            wadetb.media_urls,
        )

    def test_highest_bitrate_mp4_selected_lower_bitrate_excluded(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=TIP_ID)
        lottes = next(p for p in page.posts if p.post_id == LOTTES_ID)
        # Highest bitrate (1280000) wins; lower bitrates are not
        # appended. The HLS m3u8 variant is not video/mp4 so it
        # is filtered out at the variant-content-type check.
        self.assertIn(
            "https://video.twimg.com/fixture-video-high.mp4",
            lottes.media_urls,
        )
        self.assertNotIn(
            "https://video.twimg.com/fixture-video-low.mp4",
            lottes.media_urls,
        )
        self.assertNotIn(
            "https://video.twimg.com/fixture-video-med.mp4",
            lottes.media_urls,
        )
        self.assertNotIn(
            "https://video.twimg.com/fixture-video.m3u8",
            lottes.media_urls,
        )

    def test_numeric_string_view_count_parses_as_int(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=TIP_ID)
        tip = next(p for p in page.posts if p.post_id == TIP_ID)
        self.assertEqual(tip.metrics.view_count, 1234)
        self.assertIsInstance(tip.metrics.view_count, int)


class CursorConstructorTests(unittest.TestCase):
    """The fetcher-local :class:`Cursor` rejects empty values and
    ineligible kinds at construction. Top and unknown cursor types
    never reach construction during parse (the parser returns
    ``None`` for ineligible kinds)."""

    def test_eligible_cursor_constructs(self) -> None:
        for kind in ("Bottom", "ShowMore", "ShowMoreThreads"):
            with self.subTest(kind=kind):
                cursor = Cursor(value="abcdef", cursor_type=kind)
                self.assertEqual(cursor.value, "abcdef")
                self.assertEqual(cursor.cursor_type, kind)

    def test_empty_value_raises(self) -> None:
        with self.assertRaises(ValueError):
            Cursor(value="", cursor_type="Bottom")

    def test_unknown_kind_raises(self) -> None:
        with self.assertRaises(ValueError):
            Cursor(value="abcdef", cursor_type="Top")


class ExpectedSixteenTests(unittest.TestCase):
    """The test-vs-production invariant from the Task 1 helpers
    module is mirrored here. The five-post tip spine is a subset
    of the planned 16-post :data:`EXPECTED_16` set; this test
    pins the overlap so the helpers and parser agree."""

    def test_tip_spine_is_subset_of_expected_16(self) -> None:
        page = parse_tweet_detail_page(
            load_json_fixture("tip_tweet_detail"), focal_id=TIP_ID,
        )
        page_ids = {p.post_id for p in page.posts}
        self.assertTrue(page_ids.issubset(EXPECTED_16))


# --- helpers for synthetic wire objects (in-memory, no fixture files) ---


def _wrap_tweet_result(tweet_inner: dict) -> dict:
    """Wrap a single tweet ``result`` mapping as the body of a
    TimelineTimelineItem entry's ``tweet_results.result``."""
    return {
        "tweet_results": {"result": tweet_inner},
    }


def _tweet_result_with_user(
    *,
    rest_id: str,
    author_legacy: str,
    handle_legacy: str,
    user_core: dict | None,
    full_text: str,
    created_at: str = "Mon Apr 26 12:00:00 +0000 2026",
    conversation_id: str = "8888000000000000000",
    in_reply_to: str | None = None,
) -> dict:
    """Build a typed ``result`` mapping for one tweet (no wrapper).

    ``user_core`` is the dict placed on ``user_results.result.core``
    (or ``None`` to omit the current shape entirely). Legacy name /
    screen_name on ``user_results.result.legacy`` are always present
    so the production fallback path stays defined.
    """
    user: dict = {
        "__typename": "User",
        "id_str": "777777777",
        "legacy": {
            "name": author_legacy,
            "screen_name": handle_legacy,
        },
    }
    if user_core is not None:
        user["core"] = user_core
    return {
        "__typename": "Tweet",
        "rest_id": rest_id,
        "core": {"user_results": {"result": user}},
        "legacy": {
            "id_str": rest_id,
            "conversation_id_str": conversation_id,
            "created_at": created_at,
            "full_text": full_text,
            "in_reply_to_status_id_str": in_reply_to,
            "quoted_status_id_str": None,
            "reply_count": 0,
            "retweet_count": 0,
            "favorite_count": 0,
        },
    }


def _page(instructions: list) -> object:
    """Wrap a list of instructions in the data -> threaded path envelope."""
    return {
        "data": {
            "threaded_conversation_with_injections_v2": {
                "instructions": instructions,
            },
        },
    }


class CurrentShapeUserEdgeCasesTests(unittest.TestCase):
    """Item 3: current-shape ``user.core.name`` / ``user.core.screen_name``
    must both be non-empty strings for the current shape to win. A
    partial current shape (name only, screen_name missing, or empty
    string screen_name) must fall back to ``user.legacy.name`` /
    ``user.legacy.screen_name``.

    In-memory wire objects only; no fixture file is touched.
    """

    def test_current_shape_with_only_name_falls_back_to_legacy(self) -> None:
        # Current core has name but no screen_name key at all.
        # Legacy carries both name and screen_name. The parser
        # MUST use the legacy pair (not return an empty handle).
        tweet = _tweet_result_with_user(
            rest_id="9999000000000000001",
            author_legacy="fixture-legacy-edge-author",
            handle_legacy="fixture-legacy-edge-handle",
            user_core={"name": "fixture-edge-author"},  # no screen_name
            full_text="fixture-edge-text-1",
        )
        wire = _page([
            {
                "type": "TimelineAddEntries",
                "entries": [
                    {
                        "entryId": "entry-edge-1",
                        "content": {
                            "entryType": "TimelineTimelineItem",
                            "itemContent": _wrap_tweet_result(tweet),
                        },
                    },
                ],
            },
        ])
        page = parse_tweet_detail_page(wire)
        self.assertEqual(len(page.posts), 1)
        post = page.posts[0]
        self.assertEqual(post.author, "fixture-legacy-edge-author")
        self.assertEqual(post.handle, "fixture-legacy-edge-handle")

    def test_current_shape_with_empty_screen_name_falls_back_to_legacy(self) -> None:
        # Current core has name and an empty-string screen_name;
        # an empty string is NOT a valid handle and must trigger
        # the legacy fallback.
        tweet = _tweet_result_with_user(
            rest_id="9999000000000000002",
            author_legacy="fixture-legacy-edge-author-2",
            handle_legacy="fixture-legacy-edge-handle-2",
            user_core={"name": "fixture-edge-author-2", "screen_name": ""},
            full_text="fixture-edge-text-2",
        )
        wire = _page([
            {
                "type": "TimelineAddEntries",
                "entries": [
                    {
                        "entryId": "entry-edge-2",
                        "content": {
                            "entryType": "TimelineTimelineItem",
                            "itemContent": _wrap_tweet_result(tweet),
                        },
                    },
                ],
            },
        ])
        page = parse_tweet_detail_page(wire)
        self.assertEqual(len(page.posts), 1)
        post = page.posts[0]
        self.assertEqual(post.author, "fixture-legacy-edge-author-2")
        self.assertEqual(post.handle, "fixture-legacy-edge-handle-2")


class DedupeCharacterizationTests(unittest.TestCase):
    """Item 4: characterization tests for the documented dedupe
    behaviour. These pin existing production behaviour rather than
    force a RED. Pinning them as named tests guards against
    regressions in dedupe order, value-key, and module-wrapped
    cursor parsing.
    """

    def test_post_dedupe_last_seen_data_one_output(self) -> None:
        # Two TimelineAddEntries entries share the same rest_id.
        # The second entry carries a different author and text.
        # After dedupe the output must contain exactly one post
        # whose data comes from the LAST occurrence.
        first = _tweet_result_with_user(
            rest_id="1650678968255913985",
            author_legacy="fixture-dedupe-handle-first",
            handle_legacy="fixture-dedupe-handle-first",
            user_core={"name": "fixture-dedupe-first", "screen_name": "fixture-dedupe-first"},
            full_text="text-dedupe-first",
            created_at="Mon Apr 26 12:00:00 +0000 2026",
        )
        second = _tweet_result_with_user(
            rest_id="1650678968255913985",
            author_legacy="fixture-dedupe-handle-second",
            handle_legacy="fixture-dedupe-handle-second",
            user_core={"name": "fixture-dedupe-second", "screen_name": "fixture-dedupe-second"},
            full_text="text-dedupe-second",
            created_at="Mon Apr 26 12:05:00 +0000 2026",
        )
        wire = _page([
            {
                "type": "TimelineAddEntries",
                "entries": [
                    {
                        "entryId": "tweet-dedupe-first",
                        "content": {
                            "entryType": "TimelineTimelineItem",
                            "itemContent": _wrap_tweet_result(first),
                        },
                    },
                    {
                        "entryId": "tweet-dedupe-second",
                        "content": {
                            "entryType": "TimelineTimelineItem",
                            "itemContent": _wrap_tweet_result(second),
                        },
                    },
                ],
            },
        ])
        page = parse_tweet_detail_page(wire)
        self.assertEqual(len(page.posts), 1)
        post = page.posts[0]
        self.assertEqual(post.post_id, "1650678968255913985")
        # Last-seen data wins: author is "fixture-dedupe-second"
        # and text is "text-dedupe-second".
        self.assertEqual(post.author, "fixture-dedupe-second")
        self.assertEqual(post.text, "text-dedupe-second")

    def test_cursor_dedupe_by_value(self) -> None:
        # Two TimelineTimelineCursor entries with the same value
        # and the same eligible kind: only one Cursor must appear.
        wire = _page([
            {
                "type": "TimelineAddEntries",
                "entries": [
                    {
                        "entryId": "cursor-a",
                        "content": {
                            "entryType": "TimelineTimelineCursor",
                            "cursorType": "ShowMore",
                            "value": "fixture-dedupe-cursor-value",
                        },
                    },
                    {
                        "entryId": "cursor-b",
                        "content": {
                            "entryType": "TimelineTimelineCursor",
                            "cursorType": "ShowMore",
                            "value": "fixture-dedupe-cursor-value",
                        },
                    },
                ],
            },
        ])
        page = parse_tweet_detail_page(wire)
        self.assertEqual(len(page.cursors), 1)
        self.assertEqual(
            page.cursors[0].value, "fixture-dedupe-cursor-value",
        )
        self.assertEqual(page.cursors[0].cursor_type, "ShowMore")

    def test_eligible_cursor_wrapped_under_item_itemcontent_parses(self) -> None:
        # The cursor lives inside a TimelineTimelineModule's
        # content.items[] entry whose payload is wrapped under
        # item.itemContent (the "module" layout described in the
        # brief). The parser must surface the eligible cursor.
        wire = _page([
            {
                "type": "TimelineAddEntries",
                "entries": [
                    {
                        "entryId": "module-with-eligible-cursor",
                        "content": {
                            "entryType": "TimelineTimelineModule",
                            "items": [
                                {
                                    "entryId": "mod-cursor-showmore",
                                    "itemType": "TimelineTimelineCursor",
                                    "item": {
                                        "itemContent": {
                                            "cursorType": "ShowMore",
                                            "value": "fixture-showmore-cursor-under-item",
                                        },
                                    },
                                },
                            ],
                        },
                    },
                ],
            },
        ])
        page = parse_tweet_detail_page(wire)
        self.assertEqual(len(page.cursors), 1)
        cursor = page.cursors[0]
        self.assertEqual(
            cursor.value, "fixture-showmore-cursor-under-item",
        )
        self.assertEqual(cursor.cursor_type, "ShowMore")


class ResolveRootFromTipTests(unittest.TestCase):
    """Task 3: ``resolve_root_from_tip`` reads the resolved root
    directly off ``page.focal_conversation_id`` (parsed from the
    focal tip post's ``legacy.conversation_id_str``).

    The function is a pure page-level helper: it does NOT walk
    parents, query the transport, or substitute a
    ``reply_to_id is None`` heuristic. Parent-chain closure is
    validated later after the tip+root page merge.
    """

    def test_returns_focal_conversation_id_for_known_tip(self) -> None:
        # The existing tip_tweet_detail.json fixture has the
        # focal tip post whose legacy.conversation_id_str equals
        # the resolved root (1650678968255913985). Parsing the
        # fixture with focal_id=KNOWN_TIP_ID gives a page whose
        # focal_conversation_id is that root. The function must
        # return it.
        raw = load_json_fixture("tip_tweet_detail")
        page = parse_tweet_detail_page(raw, focal_id=KNOWN_TIP_ID)
        root = resolve_root_from_tip(KNOWN_TIP_ID, page)
        self.assertEqual(root, KNOWN_ROOT_ID)
        self.assertEqual(root, "1650678968255913985")

    def test_raises_when_tip_absent_from_page_posts(self) -> None:
        # The tip is not in page.posts (the parsed page holds
        # the five-post tip spine). An unknown tip must raise
        # ValueError; the function does not silently fall back
        # to a heuristic.
        raw = load_json_fixture("tip_tweet_detail")
        page = parse_tweet_detail_page(raw, focal_id=KNOWN_TIP_ID)
        with self.assertRaises(ValueError):
            resolve_root_from_tip("0000000000000000000", page)

    def test_raises_when_focal_conversation_id_is_none(self) -> None:
        # The tip is in page.posts, but focal_conversation_id
        # is None. The function must raise ValueError — the
        # resolved root MUST come from the focal post's
        # conversation_id_str, not from a parent-walk or
        # reply_to_id is None heuristic.
        tip_post = PostData(
            post_id=KNOWN_TIP_ID,
            author="fixture-author-tip",
            handle="fixture-handle-tip",
            text="fixture-text-tip",
            timestamp="2026-08-24 00:00:00",
            media_urls=(),
            reply_to_id="1651268028795961344",
            quote_of_id=None,
            metrics=PostMetrics(0, 0, 0, None),
        )
        page = TweetDetailPage(
            posts=(tip_post,),
            cursors=(),
            focal_conversation_id=None,
        )
        with self.assertRaises(ValueError):
            resolve_root_from_tip(KNOWN_TIP_ID, page)

    def test_raises_when_focal_conversation_id_is_empty_string(self) -> None:
        # An empty-string focal_conversation_id is the same
        # kind of absent-value case as None and must also raise.
        tip_post = PostData(
            post_id=KNOWN_TIP_ID,
            author="fixture-author-tip",
            handle="fixture-handle-tip",
            text="fixture-text-tip",
            timestamp="2026-08-24 00:00:00",
            media_urls=(),
            reply_to_id="1651268028795961344",
            quote_of_id=None,
            metrics=PostMetrics(0, 0, 0, None),
        )
        page = TweetDetailPage(
            posts=(tip_post,),
            cursors=(),
            focal_conversation_id="",
        )
        with self.assertRaises(ValueError):
            resolve_root_from_tip(KNOWN_TIP_ID, page)

    def test_prefers_focal_conversation_id_over_reply_to_none_heuristic(
        self,
    ) -> None:
        # Construct a page with two posts:
        #   - a "misleading" post whose reply_to_id is None
        #     (would be picked by a "first post with no parent"
        #      heuristic as the root) — id 9999000000000000000
        #   - the tip itself, whose parent chain does NOT
        #     reach the misleading post
        # The focal_conversation_id is the canonical root
        # 1650678968255913985, which differs from the misleading
        # id. The function MUST return the focal_conversation_id
        # value, proving the heuristic is not in play.
        misleading_root = PostData(
            post_id="9999000000000000000",
            author="fixture-misleading-author",
            handle="fixture-misleading-handle",
            text="fixture-misleading-text",
            timestamp="2026-08-24 00:00:00",
            media_urls=(),
            reply_to_id=None,
            quote_of_id=None,
            metrics=PostMetrics(0, 0, 0, None),
        )
        tip_post = PostData(
            post_id=KNOWN_TIP_ID,
            author="fixture-author-tip",
            handle="fixture-handle-tip",
            text="fixture-text-tip",
            timestamp="2026-08-24 00:05:00",
            media_urls=(),
            reply_to_id="1651268028795961344",
            quote_of_id=None,
            metrics=PostMetrics(0, 0, 0, None),
        )
        page = TweetDetailPage(
            posts=(misleading_root, tip_post),
            cursors=(),
            focal_conversation_id=KNOWN_ROOT_ID,
        )
        root = resolve_root_from_tip(KNOWN_TIP_ID, page)
        # MUST be the focal_conversation_id value, NOT the
        # misleading "no parent" post's id.
        self.assertEqual(root, KNOWN_ROOT_ID)
        self.assertNotEqual(root, misleading_root.post_id)


class RootPageParserTests(unittest.TestCase):
    """Task 4: the root fixture exercises ``TimelineAddToModule``
    (a parser path not central in the tip fixture). It contains the
    14 root-side public ids from NOTE §2.1 (all of :data:`EXPECTED_16`
    except the wvo tip ``1651282559287042048`` and the lottes post
    ``1651268028795961344``). The tip fixture supplies those two.
    No eligible cursors. The focal root post's
    ``legacy.conversation_id_str`` is the root id.
    """

    def setUp(self) -> None:
        self.raw = load_json_fixture("root_tweet_detail")

    def test_parse_returns_exactly_fourteen_post_data_with_exact_id_set(
        self,
    ) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=ROOT_ID)
        self.assertIsInstance(page, TweetDetailPage)
        self.assertEqual(len(page.posts), 14)
        ids = {p.post_id for p in page.posts}
        expected_root_only = set(EXPECTED_16) - {LOTTES_ID, TIP_ID}
        self.assertEqual(ids, expected_root_only)
        # Lottes and tip absent from root page.
        self.assertNotIn(LOTTES_ID, ids)
        self.assertNotIn(TIP_ID, ids)
        # Each post is an existing models.PostData instance with
        # an existing models.PostMetrics metrics field.
        for post in page.posts:
            self.assertIsInstance(post, PostData)
            self.assertIsInstance(post.metrics, PostMetrics)

    def test_root_focal_conversation_id_is_root(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=ROOT_ID)
        self.assertEqual(page.focal_conversation_id, ROOT_ID)

    def test_root_page_has_zero_eligible_cursors(self) -> None:
        page = parse_tweet_detail_page(self.raw, focal_id=ROOT_ID)
        self.assertEqual(page.cursors, ())
        self.assertEqual(len(page.cursors), 0)

    def test_parent_graph_uses_only_in_fixture_post_ids(self) -> None:
        # Every non-root post in the root fixture must have its
        # reply_to_id point at another post in the same fixture.
        # (The lone lottes child of kenpex->wadetb lives in the
        # tip page, not here, so the root page alone cannot satisfy
        # lottes's closure; we only assert intra-fixture closure.)
        page = parse_tweet_detail_page(self.raw, focal_id=ROOT_ID)
        ids = {p.post_id for p in page.posts}
        for post in page.posts:
            if post.reply_to_id is None:
                self.assertEqual(post.post_id, ROOT_ID)
                continue
            self.assertIn(
                post.reply_to_id, ids,
                msg=f"post {post.post_id}: parent {post.reply_to_id} absent from root fixture",
            )


class MergePostGroupsTests(unittest.TestCase):
    """Task 4: ``merge_post_groups`` is the pure merger that joins
    the tip and root pages into the final 16-post set without a
    second query per post.

    - Last-seen data wins for posts appearing in multiple groups.
    - First-insertion order is preserved: the first occurrence of
      each id defines its position in the output.
    - Returns a tuple of existing :class:`PostData` instances
      (no copies, no synthetic PostData wrappers).
    """

    @staticmethod
    def _parsed_pages() -> tuple:
        tip_page = parse_tweet_detail_page(
            load_json_fixture("tip_tweet_detail"), focal_id=TIP_ID,
        )
        root_page = parse_tweet_detail_page(
            load_json_fixture("root_tweet_detail"), focal_id=ROOT_ID,
        )
        return tip_page, root_page

    def test_merge_tip_and_root_yields_expected_16(self) -> None:
        from twitter.fetch_thread import merge_post_groups
        tip_page, root_page = self._parsed_pages()
        merged = merge_post_groups(tip_page.posts, root_page.posts)
        ids = {p.post_id for p in merged}
        self.assertEqual(ids, set(EXPECTED_16))
        self.assertEqual(len(merged), 16)

    def test_merge_one_output_per_id_no_duplicates(self) -> None:
        from twitter.fetch_thread import merge_post_groups
        tip_page, root_page = self._parsed_pages()
        merged = merge_post_groups(tip_page.posts, root_page.posts)
        ids = [p.post_id for p in merged]
        self.assertEqual(len(ids), len(set(ids)))

    def test_last_seen_group_wins_on_overlap(self) -> None:
        # Two PostData instances with the same post_id but
        # different text/metrics. The second group wins.
        from twitter.fetch_thread import merge_post_groups
        first = PostData(
            post_id="1650678968255913985",
            author="fixture-dedupe-first",
            handle="fixture-dedupe-first",
            text="text-dedupe-first",
            timestamp="2026-08-24 00:00:00",
            media_urls=(),
            reply_to_id=None,
            quote_of_id=None,
            metrics=PostMetrics(0, 0, 0, None),
        )
        second = PostData(
            post_id="1650678968255913985",
            author="fixture-dedupe-second",
            handle="fixture-dedupe-second",
            text="text-dedupe-second",
            timestamp="2026-08-24 00:05:00",
            media_urls=(),
            reply_to_id=None,
            quote_of_id=None,
            metrics=PostMetrics(1, 2, 3, 4),
        )
        merged = merge_post_groups((first,), (second,))
        self.assertEqual(len(merged), 1)
        post = merged[0]
        self.assertEqual(post.text, "text-dedupe-second")
        self.assertEqual(post.author, "fixture-dedupe-second")
        self.assertEqual(post.metrics.like_count, 3)
        self.assertEqual(post.metrics.reply_count, 1)
        self.assertEqual(post.metrics.view_count, 4)

    def test_first_insertion_order_preserved(self) -> None:
        # Tip posts appear first (5 ids, in tip order); root posts
        # are appended after in root order. Overlap ids (root,
        # wadetb, kenpex->wadetb) keep the tip's first-insertion
        # position.
        from twitter.fetch_thread import merge_post_groups
        tip_page, root_page = self._parsed_pages()
        merged = merge_post_groups(tip_page.posts, root_page.posts)
        ids = [p.post_id for p in merged]
        self.assertEqual(
            ids,
            [
                "1650678968255913985",
                "1651056827839180800",
                "1651253961524142081",
                "1651268028795961344",
                "1651282559287042048",
                "1650685805776732160",
                "1650915682136240129",
                "1651086935467917312",
                "1651168030557077504",
                "1651254727160795137",
                "1651295755293036544",
                "1651508233243095043",
                "1651510424649744385",
                "1651511316010663936",
                "1651579576089300992",
                "1651636988267888641",
            ],
        )

    def test_merged_parent_graph_closure(self) -> None:
        # Every non-root post's reply_to_id must point at a post
        # present in the merged set. The root itself may have no
        # parent.
        from twitter.fetch_thread import merge_post_groups
        tip_page, root_page = self._parsed_pages()
        merged = merge_post_groups(tip_page.posts, root_page.posts)
        merged_ids = {p.post_id for p in merged}
        for post in merged:
            if post.post_id == ROOT_ID:
                continue
            self.assertIn(
                post.reply_to_id, merged_ids,
                msg=f"post {post.post_id}: parent {post.reply_to_id} missing from merged set",
            )
        # The tip's parent chain must reach root through the
        # captured set: tip -> lottes -> kenpex->wadetb -> wadetb -> root.
        tip_post = next(p for p in merged if p.post_id == TIP_ID)
        self.assertEqual(tip_post.reply_to_id, LOTTES_ID)
        lottes = next(p for p in merged if p.post_id == LOTTES_ID)
        self.assertEqual(lottes.reply_to_id, "1651253961524142081")
        kenpex_to_wadetb = next(p for p in merged if p.post_id == "1651253961524142081")
        self.assertEqual(kenpex_to_wadetb.reply_to_id, "1651056827839180800")
        wadetb = next(p for p in merged if p.post_id == "1651056827839180800")
        self.assertEqual(wadetb.reply_to_id, ROOT_ID)

    def test_merged_objects_remain_existing_post_data(self) -> None:
        from twitter.fetch_thread import merge_post_groups
        tip_page, root_page = self._parsed_pages()
        merged = merge_post_groups(tip_page.posts, root_page.posts)
        for post in merged:
            self.assertIsInstance(post, PostData)
            self.assertIsInstance(post.metrics, PostMetrics)


class ContinuationWalkerTests(unittest.TestCase):
    """Task 5: ``walk_continuation_queue`` is the pure FIFO walker
    that follows eligible explicit reply cursors off an initial
    :class:`TweetDetailPage`. It carries no transport, sleeper, or
    request cap: tests inject a callback that returns parsed pages
    directly.

    The walker:

    - treats the initial page's ``cursors`` as the FIFO seed,
    - calls the callback exactly once per *unseen* cursor value,
    - merges returned posts via ``merge_post_groups``
      (last-seen wins, first-insertion order preserved),
    - enqueues unseen eligible cursors from each returned page,
    - stops when the FIFO is empty,
    - re-raises callback exceptions immediately (no swallow, no retry).

    The fixture exercises one synthetic
    ``ShowMoreThreads`` cursor that resolves to the tip branch
    (lottes ``1651268028795961344`` and tip
    ``1651282559287042048``). Combined with the root page's
    14 posts, the merged result must equal ``EXPECTED_16``.
    """

    CONTINUATION_CURSOR_VALUE: str = "fixture-show-more-tip-branch"
    LOTTES_ID: str = "1651268028795961344"
    TIP_ID: str = TIP_ID

    def _initial_page_with_synthetic_cursor(self) -> TweetDetailPage:
        """Parse the root fixture and append one synthetic
        ``ShowMoreThreads`` cursor. The walker treats this as the
        only eligible continuation off the root page."""
        root_raw = load_json_fixture("root_tweet_detail")
        root_page = parse_tweet_detail_page(root_raw, focal_id=ROOT_ID)
        synthetic_cursor = Cursor(
            value=self.CONTINUATION_CURSOR_VALUE,
            cursor_type="ShowMoreThreads",
        )
        return TweetDetailPage(
            posts=root_page.posts,
            cursors=(synthetic_cursor,),
            focal_conversation_id=root_page.focal_conversation_id,
        )

    def _continuation_page(self) -> TweetDetailPage:
        """Parse the sanitized tip-branch continuation fixture."""
        return parse_tweet_detail_page(
            load_json_fixture("continuation_tip_branch"),
            focal_id=ROOT_ID,
        )

    def test_walker_calls_callback_once_and_merges_to_expected_16(self) -> None:
        # The walker imports a missing function name; the RED is
        # the ImportError when ``walk_continuation_queue`` is not
        # yet exported from twitter.fetch_thread.
        from twitter.fetch_thread import walk_continuation_queue

        initial_page = self._initial_page_with_synthetic_cursor()
        synthetic_cursor = initial_page.cursors[0]
        # Pre-parse the continuation page so the callback and
        # the verification lookup share the same parsed object
        # instances (PostData is frozen; identity == "same object
        # from one parse").
        continuation_page = self._continuation_page()

        captured: list[Cursor] = []

        def fetch_page(cursor: Cursor) -> TweetDetailPage:
            captured.append(cursor)
            self.assertEqual(cursor, synthetic_cursor)
            self.assertEqual(cursor.value, self.CONTINUATION_CURSOR_VALUE)
            self.assertEqual(cursor.cursor_type, "ShowMoreThreads")
            return continuation_page

        result = walk_continuation_queue(
            initial_page, fetch_page=fetch_page,
        )

        # Exactly one callback call: the synthetic cursor and
        # nothing else (the continuation page exposes no eligible
        # cursors, so the FIFO empties immediately after the merge).
        self.assertEqual(len(captured), 1)
        self.assertEqual(result.fetched_cursor_count, 1)

        # Merged post set equals EXPECTED_16 exactly: root14 +
        # continuation2 (lottes + tip) without duplicates.
        ids = {p.post_id for p in result.posts}
        self.assertEqual(ids, set(EXPECTED_16))
        self.assertEqual(len(result.posts), 16)
        self.assertIn(LOTTES_ID, ids)
        self.assertIn(TIP_ID, ids)

        # One output per id: no duplicates in the merged tuple.
        merged_ids = [p.post_id for p in result.posts]
        self.assertEqual(len(merged_ids), len(set(merged_ids)))

        # Parent links: lottes -> kenpex->wadetb; tip -> lottes.
        # Both links must be intact after the merge.
        by_id = {p.post_id: p for p in result.posts}
        self.assertEqual(
            by_id[LOTTES_ID].reply_to_id, KENPEX_ID,
            msg="lottes reply_to_id must be kenpex->wadetb",
        )
        self.assertEqual(
            by_id[TIP_ID].reply_to_id, LOTTES_ID,
            msg="tip reply_to_id must be lottes",
        )

        # PostData instances preserved: shared ids (root, wadetb,
        # kenpex->wadetb) come from the *initial* page (same
        # object), not from copies or rewrites. Continuation-only
        # ids (lottes, tip) come from the continuation page.
        initial_by_id = {p.post_id: p for p in initial_page.posts}
        continuation_by_id = {
            p.post_id: p for p in continuation_page.posts
        }
        for shared_id in (ROOT_ID, WADETB_ID, KENPEX_ID):
            self.assertIs(
                by_id[shared_id], initial_by_id[shared_id],
                msg=f"shared id {shared_id}: PostData instance must be preserved",
            )
        for continuation_only_id in (LOTTES_ID, TIP_ID):
            self.assertIs(
                by_id[continuation_only_id],
                continuation_by_id[continuation_only_id],
                msg=(
                    f"continuation-only id {continuation_only_id}: "
                    f"PostData instance must come from continuation page"
                ),
            )

        # Every post is the existing models.PostData type with the
        # existing PostMetrics field intact.
        for post in result.posts:
            self.assertIsInstance(post, PostData)
            self.assertIsInstance(post.metrics, PostMetrics)

    def test_callback_exception_propagates_immediately_no_second_call(
        self,
    ) -> None:
        from twitter.fetch_thread import walk_continuation_queue

        class CallbackError(Exception):
            pass

        initial_page = self._initial_page_with_synthetic_cursor()
        call_count = 0

        def fetch_page(cursor: Cursor) -> TweetDetailPage:
            nonlocal call_count
            call_count += 1
            raise CallbackError(
                f"simulated callback failure for {cursor.value}",
            )

        with self.assertRaises(CallbackError):
            walk_continuation_queue(
                initial_page, fetch_page=fetch_page,
            )

        # Exactly one call: the first (and only) cursor in the
        # FIFO queue. The walker must not swallow the exception
        # and must not re-invoke the callback before raising.
        self.assertEqual(call_count, 1)

    def test_duplicate_initial_cursor_values_result_in_one_callback(
        self,
    ) -> None:
        # Characterization: two distinct Cursor instances that
        # share a ``value`` must collapse to one callback call.
        # ``seen_cursor_values`` is the dedupe key, not the Cursor
        # dataclass identity.
        from twitter.fetch_thread import walk_continuation_queue

        root_raw = load_json_fixture("root_tweet_detail")
        root_page = parse_tweet_detail_page(root_raw, focal_id=ROOT_ID)
        duplicate_cursor = Cursor(
            value=self.CONTINUATION_CURSOR_VALUE,
            cursor_type="ShowMoreThreads",
        )
        initial_page = TweetDetailPage(
            posts=root_page.posts,
            cursors=(duplicate_cursor, duplicate_cursor),
            focal_conversation_id=root_page.focal_conversation_id,
        )

        call_count = 0

        def fetch_page(cursor: Cursor) -> TweetDetailPage:
            nonlocal call_count
            call_count += 1
            return self._continuation_page()

        result = walk_continuation_queue(
            initial_page, fetch_page=fetch_page,
        )

        self.assertEqual(call_count, 1)
        self.assertEqual(result.fetched_cursor_count, 1)
        ids = {p.post_id for p in result.posts}
        self.assertEqual(ids, set(EXPECTED_16))


class FullDepthContinuationCharacterizationTests(unittest.TestCase):
    """Task 6 characterization: the pure FIFO walker must follow
    explicit continuation cursors through SEVEN reply depths with
    no shallow depth limit, dedupe seen cursors, terminate naturally
    on a leaf, and short-circuit when the initial page has no
    cursors.

    The walker is the existing ``walk_continuation_queue`` in
    ``twitter.fetch_thread``. These tests pin its behavior under
    seven levels of nested reply continuation, with no production
    change. The fixtures are seven sanitized raw TweetDetail
    continuation pages (``continuation_depth_1.json`` through
    ``continuation_depth_7.json``); depth-3 additionally echoes its
    own/current cursor alongside the next cursor to prove
    seen-cursor loop suppression.
    """

    DEPTH_POST_IDS: tuple[str, ...] = (
        "1700000000000000001",
        "1700000000000000002",
        "1700000000000000003",
        "1700000000000000004",
        "1700000000000000005",
        "1700000000000000006",
        "1700000000000000007",
    )

    def _initial_page_with_root_and_one_cursor(
        self,
    ) -> TweetDetailPage:
        """Build an initial page with the known root post and
        exactly one eligible ``ShowMoreThreads`` cursor valued
        ``fixture-depth-1``. The seven sanitized depth fixtures
        are loaded separately.
        """
        root_tweet = _tweet_result_with_user(
            rest_id=ROOT_ID,
            author_legacy="fixture-root-author",
            handle_legacy="fixture-root-handle",
            user_core={
                "name": "fixture-root-author",
                "screen_name": "fixture-root-handle",
            },
            full_text="fixture-root-text",
            in_reply_to=None,
        )
        initial_wire = _page([
            {
                "type": "TimelineAddEntries",
                "entries": [
                    {
                        "entryId": "initial-root",
                        "content": {
                            "entryType": "TimelineTimelineItem",
                            "itemContent": _wrap_tweet_result(root_tweet),
                        },
                    },
                    {
                        "entryId": "initial-cursor-depth-1",
                        "content": {
                            "entryType": "TimelineTimelineCursor",
                            "cursorType": "ShowMoreThreads",
                            "value": "fixture-depth-1",
                        },
                    },
                ],
            },
        ])
        return parse_tweet_detail_page(initial_wire, focal_id=ROOT_ID)

    def _parse_all_depth_pages(
        self,
    ) -> dict[str, TweetDetailPage]:
        """Parse all seven sanitized raw TweetDetail continuation
        pages and key them by the cursor value that fetches them:
        page N is fetched via ``fixture-depth-N``.
        """
        pages: dict[str, TweetDetailPage] = {}
        for n in range(1, 8):
            page = parse_tweet_detail_page(
                load_json_fixture(f"continuation_depth_{n}"),
                focal_id=ROOT_ID,
            )
            pages[f"fixture-depth-{n}"] = page
        return pages

    def test_initial_page_has_root_and_exactly_one_cursor(self) -> None:
        # The initial page must contain the known root post and
        # exactly one eligible ShowMoreThreads cursor valued
        # ``fixture-depth-1``. This is the seed the walker consumes.
        initial_page = self._initial_page_with_root_and_one_cursor()
        self.assertEqual(len(initial_page.posts), 1)
        self.assertEqual(initial_page.posts[0].post_id, ROOT_ID)
        self.assertEqual(len(initial_page.cursors), 1)
        cursor = initial_page.cursors[0]
        self.assertEqual(cursor.value, "fixture-depth-1")
        self.assertEqual(cursor.cursor_type, "ShowMoreThreads")

    def test_seven_levels_walked_callback_order_and_exact_parent_chain(
        self,
    ) -> None:
        # The walker follows seven explicit continuation cursors
        # FIFO to a leaf, with no depth limit. Result: exactly
        # seven callbacks, in cursor order; eight posts in the
        # accumulator (root + seven synthetic); parent chain
        # walks back to the known root.
        initial_page = self._initial_page_with_root_and_one_cursor()
        pages_by_cursor = self._parse_all_depth_pages()
        callback_calls: list[str] = []

        def fetch_page(cursor: Cursor) -> TweetDetailPage:
            callback_calls.append(cursor.value)
            return pages_by_cursor[cursor.value]

        result = walk_continuation_queue(
            initial_page, fetch_page=fetch_page,
        )

        self.assertEqual(result.fetched_cursor_count, 7)
        self.assertEqual(
            callback_calls,
            [
                "fixture-depth-1",
                "fixture-depth-2",
                "fixture-depth-3",
                "fixture-depth-4",
                "fixture-depth-5",
                "fixture-depth-6",
                "fixture-depth-7",
            ],
        )

        ids = {p.post_id for p in result.posts}
        self.assertEqual(ids, {ROOT_ID, *self.DEPTH_POST_IDS})
        self.assertEqual(len(result.posts), 8)

        by_id = {p.post_id: p for p in result.posts}
        for n in range(6, 0, -1):
            self.assertEqual(
                by_id[self.DEPTH_POST_IDS[n]].reply_to_id,
                self.DEPTH_POST_IDS[n - 1],
                msg=f"depth-{n + 1} must reply to depth-{n}",
            )
        self.assertEqual(
            by_id[self.DEPTH_POST_IDS[0]].reply_to_id,
            ROOT_ID,
            msg="depth-1 must reply to the known root",
        )
        self.assertIsNone(by_id[ROOT_ID].reply_to_id)

        for post in result.posts:
            self.assertIsInstance(post, PostData)
            self.assertIsInstance(post.metrics, PostMetrics)

    def test_repeated_current_cursor_is_not_called_twice_no_loop(
        self,
    ) -> None:
        # Depth-3's fixture echoes its own incoming cursor
        # (``fixture-depth-3``) alongside the next cursor
        # (``fixture-depth-4``). The walker must skip the echo via
        # seen-cursor dedupe; the callback is invoked exactly once
        # for that value and the queue does not loop.
        initial_page = self._initial_page_with_root_and_one_cursor()
        pages_by_cursor = self._parse_all_depth_pages()
        depth_3_call_count: int = 0
        callback_calls: list[str] = []

        def fetch_page(cursor: Cursor) -> TweetDetailPage:
            nonlocal depth_3_call_count
            callback_calls.append(cursor.value)
            if cursor.value == "fixture-depth-3":
                depth_3_call_count += 1
            return pages_by_cursor[cursor.value]

        result = walk_continuation_queue(
            initial_page, fetch_page=fetch_page,
        )

        self.assertEqual(depth_3_call_count, 1)
        self.assertEqual(result.fetched_cursor_count, 7)
        # No loop: total callback invocations equal distinct cursors
        # (7). If the echo were not skipped, the count would exceed
        # 7 or the queue would not drain.
        self.assertEqual(len(callback_calls), 7)
        self.assertEqual(
            callback_calls.count("fixture-depth-3"),
            1,
        )

    def test_depth_seven_is_a_leaf_queue_exhausts_naturally(self) -> None:
        # Depth-7's fixture exposes no eligible continuation cursor.
        # The walker must terminate by the queue emptying naturally,
        # not by any error or cap.
        initial_page = self._initial_page_with_root_and_one_cursor()
        pages_by_cursor = self._parse_all_depth_pages()

        def fetch_page(cursor: Cursor) -> TweetDetailPage:
            return pages_by_cursor[cursor.value]

        result = walk_continuation_queue(
            initial_page, fetch_page=fetch_page,
        )

        ids = {p.post_id for p in result.posts}
        self.assertIn(self.DEPTH_POST_IDS[6], ids)
        # Depth-7 has no cursors, so the FIFO empties after the
        # seventh fetch. fetched_cursor_count is exactly seven.
        self.assertEqual(result.fetched_cursor_count, 7)
        self.assertNotIn(
            self.DEPTH_POST_IDS[6],
            {c.value for c in pages_by_cursor["fixture-depth-7"].cursors},
        )

    def test_no_cursor_fast_path_initial_posts_unchanged(self) -> None:
        # An initial page with zero cursors is the fast path:
        # the walker makes no callback calls, leaves initial posts
        # unchanged, and reports fetched_cursor_count == 0.
        root_tweet = _tweet_result_with_user(
            rest_id=ROOT_ID,
            author_legacy="fixture-root-author",
            handle_legacy="fixture-root-handle",
            user_core={
                "name": "fixture-root-author",
                "screen_name": "fixture-root-handle",
            },
            full_text="fixture-root-text",
            in_reply_to=None,
        )
        initial_wire = _page([
            {
                "type": "TimelineAddEntries",
                "entries": [
                    {
                        "entryId": "initial-root-only",
                        "content": {
                            "entryType": "TimelineTimelineItem",
                            "itemContent": _wrap_tweet_result(root_tweet),
                        },
                    },
                ],
            },
        ])
        initial_page = parse_tweet_detail_page(
            initial_wire, focal_id=ROOT_ID,
        )
        self.assertEqual(initial_page.cursors, ())

        callback_calls: list[str] = []

        def fetch_page(cursor: Cursor) -> TweetDetailPage:
            callback_calls.append(cursor.value)
            raise AssertionError(
                f"callback must not fire; got cursor {cursor.value!r}",
            )

        result = walk_continuation_queue(
            initial_page, fetch_page=fetch_page,
        )

        self.assertEqual(callback_calls, [])
        self.assertEqual(result.fetched_cursor_count, 0)
        ids = {p.post_id for p in result.posts}
        self.assertEqual(ids, {ROOT_ID})
        self.assertEqual(len(result.posts), 1)


class RequestGovernorFirstCallTests(unittest.TestCase):
    """Task 8 (item 1): the very first call to ``governor.issue``
    must not call ``sleeper.sleep`` (the operator has not yet
    issued a prior request; there is nothing to pace against) and
    must return the operation's ``(status, body)`` tuple verbatim.
    """

    def test_first_call_does_not_sleep_and_returns_result_verbatim(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        # Sentinel: would explode if invoked.
        def operation() -> tuple[int, str]:
            return (200, "first-call-body")

        result = governor.issue("bootstrap_homepage", operation)

        # Result is passed through unchanged.
        self.assertEqual(result, (200, "first-call-body"))
        # No sleep fired on the first call.
        self.assertEqual(sleeper.durations, [])
        # The first attempt is counted and recorded exactly once.
        self.assertEqual(governor.count, 1)
        self.assertEqual(governor.roles, ("bootstrap_homepage",))


class RequestGovernorFourRoleSequenceTests(unittest.TestCase):
    """Task 8 (item 2): the human-paced sequence for the locked
    four-provider call shape is four roles with three sleeps in
    between (the first call does not sleep). The exact role
    tuple is the ordered log of issued calls.
    """

    SEQUENCE: tuple[tuple[str, tuple[int, str]], ...] = (
        ("bootstrap_homepage", (200, "home")),
        ("bootstrap_js",       (200, "js")),
        ("tip_tweet_detail",   (200, "tip")),
        ("root_tweet_detail",  (200, "root")),
    )

    def test_four_roles_three_sleeps_with_exact_role_order(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )

        for role, body in self.SEQUENCE:
            def operation(
                _body: tuple[int, str] = body,
            ) -> tuple[int, str]:
                return _body
            governor.issue(role, operation)

        # Three sleeps between the four calls; each value is
        # exactly ``min_delay`` (5.0).
        self.assertEqual(sleeper.durations, [5.0, 5.0, 5.0])
        # Roles preserve insertion order.
        self.assertEqual(
            governor.roles,
            ("bootstrap_homepage", "bootstrap_js",
             "tip_tweet_detail", "root_tweet_detail"),
        )
        self.assertEqual(governor.count, 4)


class RequestGovernorMaxRequestsTests(unittest.TestCase):
    """Task 8 (item 3): with ``max_requests=8`` the governor must
    execute exactly 8 operations, sleep 7 times, and on the ninth
    attempt raise ``RequestBudgetExceeded`` without calling the
    operation, without sleeping, and without appending a role.
    """

    def test_ninth_attempt_raises_without_calling_sentinel(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        # Eight innocuous operations that each return (200, "").
        for _ in range(8):
            governor.issue("ok", lambda: (200, ""))

        sentinel_calls: list[int] = []

        def sentinel() -> tuple[int, str]:
            sentinel_calls.append(1)
            return (200, "should-never-run")

        with self.assertRaises(RequestBudgetExceeded):
            governor.issue("ninth", sentinel)

        # Exactly seven sleeps (one between each of the eight
        # successful calls; none on the first, none on the ninth).
        self.assertEqual(len(sleeper.durations), 7)
        self.assertEqual(sleeper.durations, [5.0] * 7)
        # The sentinel operation is never invoked.
        self.assertEqual(sentinel_calls, [])
        # No extra role was appended for the failed ninth attempt.
        self.assertEqual(len(governor.roles), 8)
        # ``RequestBudgetExceeded`` is a ``RuntimeError``.
        self.assertTrue(
            issubclass(RequestBudgetExceeded, RuntimeError),
            msg="RequestBudgetExceeded must subclass RuntimeError",
        )


class RequestGovernorOperationExceptionTests(unittest.TestCase):
    """Task 8 (item 4): if the wrapped operation raises, the
    governor must propagate the exception immediately, must not
    retry, must not catch, must not strip the role from the count
    (the attempted call still counts), and must not append a
    second sleep entry.
    """

    def test_operation_exception_propagates_role_counted_no_retry(self) -> None:
        class CallbackError(RuntimeError):
            pass

        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        call_count: list[int] = []

        def operation() -> tuple[int, str]:
            call_count.append(1)
            raise CallbackError("simulated provider failure")

        with self.assertRaises(CallbackError):
            governor.issue("bootstrap_homepage", operation)

        # Operation called exactly once; no retry from the governor.
        self.assertEqual(call_count, [1])
        # The attempted call is counted (it would have been a
        # budgeted request).
        self.assertEqual(governor.count, 1)
        self.assertEqual(governor.roles, ("bootstrap_homepage",))
        # No sleep was issued: this is the first call.
        self.assertEqual(sleeper.durations, [])

    def test_operation_exception_after_pacing_still_propagates_no_extra_sleep(
        self,
    ) -> None:
        # Two-issue sequence: the first call succeeds, the second
        # raises. The governor must not append a second sleep after
        # the failing call, and the failing call must remain
        # counted.
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )

        class CallbackError(RuntimeError):
            pass

        governor.issue("bootstrap_homepage", lambda: (200, "ok"))
        with self.assertRaises(CallbackError):
            governor.issue(
                "bootstrap_js",
                lambda: (_ for _ in ()).throw(CallbackError("boom")),
            )
        # Exactly one sleep: the pace between the two attempted
        # calls. No sleep is appended on the failing path.
        self.assertEqual(sleeper.durations, [5.0])
        # Both attempted calls are counted.
        self.assertEqual(governor.count, 2)
        self.assertEqual(
            governor.roles, ("bootstrap_homepage", "bootstrap_js"),
        )


class RequestGovernorValidationTests(unittest.TestCase):
    """Task 8 (item 5): construction rejects ``max_requests < 1``
    and ``min_delay < 0``; ``issue`` rejects empty roles. The
    governor fails closed at construction and at every call.
    """

    def test_constructor_rejects_zero_max_requests(self) -> None:
        sleeper = RecordingSleeper()
        with self.assertRaises(ValueError):
            RequestGovernor(max_requests=0, min_delay=5.0, sleeper=sleeper)

    def test_constructor_rejects_negative_max_requests(self) -> None:
        sleeper = RecordingSleeper()
        with self.assertRaises(ValueError):
            RequestGovernor(max_requests=-1, min_delay=5.0, sleeper=sleeper)

    def test_constructor_rejects_negative_min_delay(self) -> None:
        sleeper = RecordingSleeper()
        with self.assertRaises(ValueError):
            RequestGovernor(max_requests=8, min_delay=-0.1, sleeper=sleeper)

    def test_constructor_accepts_zero_min_delay(self) -> None:
        # min_delay == 0 is allowed; the operator may opt out of
        # pacing entirely. The first call still does not sleep and
        # later calls sleep(0.0).
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=0.0, sleeper=sleeper,
        )
        governor.issue("a", lambda: (200, ""))
        governor.issue("b", lambda: (200, ""))
        self.assertEqual(sleeper.durations, [0.0])

    def test_issue_rejects_empty_role(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        with self.assertRaises(ValueError):
            governor.issue("", lambda: (200, ""))

    def test_constructor_rejects_bool_max_requests(self) -> None:
        # ``True`` is an ``int`` subclass; the governor must still
        # reject it. A bool is not a valid request budget.
        sleeper = RecordingSleeper()
        with self.assertRaises(ValueError):
            RequestGovernor(max_requests=True, min_delay=5.0, sleeper=sleeper)

    def test_constructor_rejects_bool_min_delay(self) -> None:
        # Same reasoning: ``True`` is an ``int`` but not a valid
        # delay. The governor fails closed.
        sleeper = RecordingSleeper()
        with self.assertRaises(ValueError):
            RequestGovernor(max_requests=8, min_delay=True, sleeper=sleeper)

    def test_constructor_rejects_none_sleeper(self) -> None:
        # The sleeper is required: there is no default. The
        # governor must reject ``None`` at construction rather
        # than blow up on the first call.
        with self.assertRaises(ValueError):
            RequestGovernor(max_requests=8, min_delay=5.0, sleeper=None)

    def test_issue_rejects_non_string_role(self) -> None:
        # Roles must be strings. An int, ``None``, or any other
        # type is rejected before any state mutation. The first
        # call to ``issue`` is the validation target.
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        with self.assertRaises(ValueError):
            governor.issue(123, lambda: (200, ""))  # type: ignore[arg-type]
        # No role was appended for the rejected call.
        self.assertEqual(governor.count, 0)
        self.assertEqual(governor.roles, ())
        # And ``None`` is rejected too.
        with self.assertRaises(ValueError):
            governor.issue(None, lambda: (200, ""))  # type: ignore[arg-type]
        self.assertEqual(governor.count, 0)
        self.assertEqual(governor.roles, ())


class RequestGovernorSleeperExceptionTests(unittest.TestCase):
    """Task 8 (item 3 follow-up): if ``sleeper.sleep`` raises
    between two attempted calls, the governor must propagate
    the exception, must NOT append the second role, must NOT
    invoke the second operation, and must leave the count at
    the post-first-call value. The governor does not catch,
    retry, or strip the role.
    """

    def test_sleeper_exception_prevents_second_role_append_and_operation(
        self,
    ) -> None:
        class SleeperFailure(RuntimeError):
            pass

        class RaisingSleeper:
            """A :class:`Sleeper`-shaped fake that raises on the
            FIRST ``sleep`` call only. The first attempted call
            does not sleep (the governor skips the sleep when
            ``count == 0``), so the first call succeeds; the
            second attempted call invokes ``sleep`` for the first
            time and that invocation raises."""

            def __init__(self) -> None:
                self.sleep_calls: list[float] = []

            def sleep(self, seconds: float) -> None:
                self.sleep_calls.append(seconds)
                raise SleeperFailure("simulated sleeper failure")

        sleeper = RaisingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )

        # First call succeeds: no sleep on the first call, the
        # operation runs, the role is appended.
        first_result = governor.issue(
            "bootstrap_homepage", lambda: (200, "home"),
        )
        self.assertEqual(first_result, (200, "home"))
        self.assertEqual(governor.count, 1)
        self.assertEqual(governor.roles, ("bootstrap_homepage",))

        # The second attempted call triggers a sleep; the sleeper
        # raises before the role is appended and before the
        # operation is invoked.
        second_op_calls: list[int] = []

        def second_operation() -> tuple[int, str]:
            second_op_calls.append(1)
            return (200, "should-never-run")

        with self.assertRaises(SleeperFailure):
            governor.issue("bootstrap_js", second_operation)

        # The second role is not appended.
        self.assertEqual(governor.roles, ("bootstrap_homepage",))
        # The second operation is not invoked.
        self.assertEqual(second_op_calls, [])
        # The count remains at the post-first-call value.
        self.assertEqual(governor.count, 1)
        # The sleeper was called exactly once with ``min_delay``
        # before raising on the first (and only) invocation —
        # the governor does not retry the sleep.
        self.assertEqual(sleeper.sleep_calls, [5.0])


class RequestGovernorIndependentInstancesTests(unittest.TestCase):
    """Task 8 (item 6): two governor instances do not share
    state. Counts, roles, and sleep histories are independent.
    """

    def test_independent_governors_do_not_share_state(self) -> None:
        sleeper_a = RecordingSleeper()
        sleeper_b = RecordingSleeper()
        a = RequestGovernor(max_requests=8, min_delay=5.0, sleeper=sleeper_a)
        b = RequestGovernor(max_requests=8, min_delay=5.0, sleeper=sleeper_b)

        a.issue("bootstrap_homepage", lambda: (200, ""))
        a.issue("bootstrap_js", lambda: (200, ""))

        b.issue("tip_tweet_detail", lambda: (200, ""))

        self.assertEqual(a.count, 2)
        self.assertEqual(
            a.roles, ("bootstrap_homepage", "bootstrap_js"),
        )
        self.assertEqual(b.count, 1)
        self.assertEqual(b.roles, ("tip_tweet_detail",))

        # Sleepers tracked their respective governors; neither
        # saw the other's calls.
        self.assertEqual(sleeper_a.durations, [5.0])
        self.assertEqual(sleeper_b.durations, [])

    def test_sleeper_protocol_is_runtime_checkable_shape(self) -> None:
        # The :class:`Sleeper` protocol declares ``sleep``; the
        # Task 1 ``RecordingSleeper`` satisfies it. This pins the
        # duck-typed surface the governor depends on.
        sleeper = RecordingSleeper()
        self.assertTrue(hasattr(sleeper, "sleep"))
        self.assertTrue(callable(sleeper.sleep))


class IssueProviderRequestSuccessTests(unittest.TestCase):
    """Task 9: 2xx responses return the body string verbatim and
    invoke the operation exactly once through the governor."""

    def test_200_returns_body_one_call_count_one(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        body = "ok-body-sentinel"
        call_count: list[int] = []

        def op() -> tuple[int, str]:
            call_count.append(1)
            return (200, body)

        result = issue_provider_request(
            governor, role="bootstrap_homepage", operation=op,
        )
        self.assertEqual(result, body)
        self.assertEqual(call_count, [1])
        self.assertEqual(governor.count, 1)
        self.assertEqual(governor.roles, ("bootstrap_homepage",))

    def test_204_returns_body_one_call_count_one(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        body = "no-content-sentinel"
        call_count: list[int] = []

        def op() -> tuple[int, str]:
            call_count.append(1)
            return (204, body)

        result = issue_provider_request(
            governor, role="bootstrap_js", operation=op,
        )
        self.assertEqual(result, body)
        self.assertEqual(call_count, [1])
        self.assertEqual(governor.count, 1)


class IssueProviderRequestAuthErrorTests(unittest.TestCase):
    """Task 9: 401 and 403 responses raise :class:`AuthError`,
    the operation is called exactly once, and no retry occurs."""

    def test_401_raises_auth_error_no_retry(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        call_count: list[int] = []

        def op() -> tuple[int, str]:
            call_count.append(1)
            return (401, "")

        with self.assertRaises(AuthError):
            issue_provider_request(
                governor, role="tip_tweet_detail", operation=op,
            )
        self.assertEqual(call_count, [1])
        self.assertEqual(governor.count, 1)

    def test_403_raises_auth_error_no_retry(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        call_count: list[int] = []

        def op() -> tuple[int, str]:
            call_count.append(1)
            return (403, "")

        with self.assertRaises(AuthError):
            issue_provider_request(
                governor, role="root_tweet_detail", operation=op,
            )
        self.assertEqual(call_count, [1])
        self.assertEqual(governor.count, 1)


class IssueProviderRequestRateLimitTests(unittest.TestCase):
    """Task 9: 429 responses raise :class:`RateLimitError`,
    the operation is called exactly once, and no retry occurs."""

    def test_429_raises_rate_limit_error_no_retry(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        call_count: list[int] = []

        def op() -> tuple[int, str]:
            call_count.append(1)
            return (429, "")

        with self.assertRaises(RateLimitError):
            issue_provider_request(
                governor, role="continuation_tweet_detail", operation=op,
            )
        self.assertEqual(call_count, [1])
        self.assertEqual(governor.count, 1)


class IssueProviderRequestGenericErrorTests(unittest.TestCase):
    """Task 9: any non-2xx that is not 401/403/429 raises
    :class:`ProviderError`, the operation is called exactly once,
    and no retry occurs. Statuses covered: 400, 404, 500, 503."""

    def _assert_provider_error(
        self, status: int, role: str,
    ) -> tuple[RequestGovernor, list[int]]:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        call_count: list[int] = []

        def op() -> tuple[int, str]:
            call_count.append(1)
            return (status, "")

        with self.assertRaises(ProviderError):
            issue_provider_request(
                governor, role=role, operation=op,
            )
        self.assertEqual(call_count, [1])
        self.assertEqual(governor.count, 1)
        return governor, call_count

    def test_400_raises_provider_error_no_retry(self) -> None:
        self._assert_provider_error(400, "tip_tweet_detail")

    def test_404_raises_provider_error_no_retry(self) -> None:
        self._assert_provider_error(404, "root_tweet_detail")

    def test_500_raises_provider_error_no_retry(self) -> None:
        self._assert_provider_error(500, "bootstrap_homepage")

    def test_503_raises_provider_error_no_retry(self) -> None:
        self._assert_provider_error(503, "continuation_tweet_detail")


class IssueProviderRequestTransportErrorTests(unittest.TestCase):
    """Task 9: :class:`TimeoutError`, :class:`ConnectionError`, and
    :class:`OSError` raised by the operation are translated into
    :class:`ProviderError` chained from the original, with the
    operation called exactly once."""

    def test_timeout_error_becomes_provider_error_chained(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        sentinel = TimeoutError("simulated timeout sentinel")
        call_count: list[int] = []

        def op() -> tuple[int, str]:
            call_count.append(1)
            raise sentinel

        with self.assertRaises(ProviderError) as ctx:
            issue_provider_request(
                governor, role="tip_tweet_detail", operation=op,
            )
        self.assertIs(ctx.exception.__cause__, sentinel)
        self.assertEqual(call_count, [1])
        self.assertEqual(governor.count, 1)

    def test_connection_error_becomes_provider_error_chained(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        sentinel = ConnectionError("simulated connection sentinel")
        call_count: list[int] = []

        def op() -> tuple[int, str]:
            call_count.append(1)
            raise sentinel

        with self.assertRaises(ProviderError) as ctx:
            issue_provider_request(
                governor, role="tip_tweet_detail", operation=op,
            )
        self.assertIs(ctx.exception.__cause__, sentinel)
        self.assertEqual(call_count, [1])
        self.assertEqual(governor.count, 1)

    def test_oserror_becomes_provider_error_chained(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        sentinel = OSError("simulated os sentinel")
        call_count: list[int] = []

        def op() -> tuple[int, str]:
            call_count.append(1)
            raise sentinel

        with self.assertRaises(ProviderError) as ctx:
            issue_provider_request(
                governor, role="tip_tweet_detail", operation=op,
            )
        self.assertIs(ctx.exception.__cause__, sentinel)
        self.assertEqual(call_count, [1])
        self.assertEqual(governor.count, 1)


class IssueProviderRequestNonProviderExceptionTests(unittest.TestCase):
    """Task 9: arbitrary programmer/parser exceptions such as
    :class:`ValueError` propagate unchanged and are NOT mislabelled
    as a provider failure."""

    def test_value_error_propagates_unchanged(self) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        sentinel = ValueError("simulated parser sentinel")
        call_count: list[int] = []

        def op() -> tuple[int, str]:
            call_count.append(1)
            raise sentinel

        with self.assertRaises(ValueError) as ctx:
            issue_provider_request(
                governor, role="tip_tweet_detail", operation=op,
            )
        # Same instance propagates, not wrapped in ProviderError.
        self.assertIs(ctx.exception, sentinel)
        self.assertEqual(call_count, [1])
        self.assertEqual(governor.count, 1)


class IssueProviderRequestSecretFreeErrorMessagesTests(unittest.TestCase):
    """Task 9: exception messages must NOT echo the response body,
    URL, header value, or cursor value carried by the operation.
    Status and exception type are the only diagnostic surfaces."""

    def test_provider_error_message_does_not_leak_payload_sentinels(
        self,
    ) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        body_sentinel = "SENTINEL_BODY_abcdef0123456789"
        url_sentinel = "https://SENTINEL_URL.example/x"
        header_sentinel = "SENTINEL_HEADER_abcdef0123456789"
        cursor_sentinel = "SENTINEL_CURSOR_abcdef0123456789"

        def op() -> tuple[int, str]:
            return (503, body_sentinel)

        with self.assertRaises(ProviderError) as ctx:
            issue_provider_request(
                governor,
                role=(
                    f"{url_sentinel} {header_sentinel} {cursor_sentinel}"
                ),
                operation=op,
            )
        message = str(ctx.exception)
        for needle in (
            body_sentinel, url_sentinel, header_sentinel, cursor_sentinel,
        ):
            self.assertNotIn(needle, message)

    def test_auth_error_message_does_not_leak_payload_sentinels(
        self,
    ) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        body_sentinel = "SENTINEL_BODY_abcdef0123456789"
        url_sentinel = "https://SENTINEL_URL.example/x"
        header_sentinel = "SENTINEL_HEADER_abcdef0123456789"
        cursor_sentinel = "SENTINEL_CURSOR_abcdef0123456789"

        def op() -> tuple[int, str]:
            return (401, body_sentinel)

        with self.assertRaises(AuthError) as ctx:
            issue_provider_request(
                governor,
                role=(
                    f"{url_sentinel} {header_sentinel} {cursor_sentinel}"
                ),
                operation=op,
            )
        message = str(ctx.exception)
        for needle in (
            body_sentinel, url_sentinel, header_sentinel, cursor_sentinel,
        ):
            self.assertNotIn(needle, message)

    def test_rate_limit_error_message_does_not_leak_payload_sentinels(
        self,
    ) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        body_sentinel = "SENTINEL_BODY_abcdef0123456789"
        url_sentinel = "https://SENTINEL_URL.example/x"
        header_sentinel = "SENTINEL_HEADER_abcdef0123456789"
        cursor_sentinel = "SENTINEL_CURSOR_abcdef0123456789"

        def op() -> tuple[int, str]:
            return (429, body_sentinel)

        with self.assertRaises(RateLimitError) as ctx:
            issue_provider_request(
                governor,
                role=(
                    f"{url_sentinel} {header_sentinel} {cursor_sentinel}"
                ),
                operation=op,
            )
        message = str(ctx.exception)
        for needle in (
            body_sentinel, url_sentinel, header_sentinel, cursor_sentinel,
        ):
            self.assertNotIn(needle, message)


class IssueProviderRequestBudgetExceededTests(unittest.TestCase):
    """Task 9: :class:`RequestBudgetExceeded` must remain a
    :class:`RuntimeError` and a :class:`FetchError`; the ninth
    operation never runs when the budget is 8."""

    def test_request_budget_exceeded_is_runtime_error_and_fetch_error(
        self,
    ) -> None:
        self.assertTrue(
            issubclass(RequestBudgetExceeded, RuntimeError),
            msg="RequestBudgetExceeded must remain a RuntimeError",
        )
        self.assertTrue(
            issubclass(RequestBudgetExceeded, FetchError),
            msg=(
                "RequestBudgetExceeded must be a FetchError subclass "
                "while remaining a RuntimeError"
            ),
        )

    def test_ninth_operation_never_called_after_eight_successful(
        self,
    ) -> None:
        sleeper = RecordingSleeper()
        governor = RequestGovernor(
            max_requests=8, min_delay=5.0, sleeper=sleeper,
        )
        for i in range(8):
            governor.issue(
                f"ok-{i}", lambda i=i: (200, f"body-{i}"),
            )

        sentinel_calls: list[int] = []

        def sentinel() -> tuple[int, str]:
            sentinel_calls.append(1)
            return (200, "should-never-run")

        with self.assertRaises(RequestBudgetExceeded):
            issue_provider_request(
                governor, role="ninth", operation=sentinel,
            )
        self.assertEqual(sentinel_calls, [])
        self.assertEqual(governor.count, 8)
        self.assertEqual(
            governor.roles,
            tuple(f"ok-{i}" for i in range(8)),
        )


if __name__ == "__main__":
    unittest.main()
