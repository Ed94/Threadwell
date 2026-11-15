"""Offline tests for the recursive cursor walker.

The fixtures are captured TweetDetail response trees, trimmed to the
fields the walker reads: entry ids, cursor values, and tweet identity.
No test here touches the network.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from twitter import walker
from twitter.walker import WalkerError

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "walker"

# The kenpex forth conversation: 16 posts. This is the fixture
# NOTE.md section 5 asked for as a regression case.
KENPEX_EXPECTED_16 = (
    "1650678968255913985",
    "1650685805776732160",
    "1650915682136240129",
    "1651056827839180800",
    "1651086935467917312",
    "1651168030557077504",
    "1651253961524142081",
    "1651254727160795137",
    "1651268028795961344",
    "1651282559287042048",
    "1651295755293036544",
    "1651508233243095043",
    "1651510424649744385",
    "1651511316010663936",
    "1651579576089300992",
    "1651636988267888641",
)


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class AbortExtraction(Exception):
    """Stands in for gallery-dl's AbortExtraction.

    The walker matches the exception by class name, so the test needs a
    class with that name.
    """


class ParsePageTests(unittest.TestCase):
    """The page parser must find cursors at every depth."""

    def test_finds_nested_showmore_cursor(self) -> None:
        """The kenpex page carries a cursor nested in a thread module."""
        page = walker.parse_page(load("page_kenpex_baseline.json"))
        self.assertTrue(page.cursors)
        self.assertIsNotNone(page.top_level_cursor)

    def test_nested_cursor_is_not_only_the_top_level_one(self) -> None:
        """The nested cursor is the one gallery-dl never follows."""
        page = walker.parse_page(load("page_kenpex_baseline.json"))
        self.assertNotEqual(page.top_level_cursor, page.cursors[0])

    def test_thread_page_carries_a_top_level_cursor(self) -> None:
        page = walker.parse_page(load("page_nested_cursor.json"))
        self.assertTrue(page.cursors)
        self.assertIsNotNone(page.top_level_cursor)

    def test_kenpex_page_has_a_nested_showmore_cursor(self) -> None:
        page = walker.parse_page(load("page_kenpex_baseline.json"))
        self.assertEqual(len(page.cursors), 2)
        self.assertIsNotNone(page.top_level_cursor)

    def test_collects_tweet_ids(self) -> None:
        page = walker.parse_page(load("page_kenpex_baseline.json"))
        self.assertEqual(len(page.post_ids), 11)
        for post_id in page.post_ids:
            self.assertTrue(post_id.isdigit())

    def test_collects_reply_counts_and_parents(self) -> None:
        """The walker needs these to spot an unreached subtree."""
        page = walker.parse_page(load("page_nested_cursor.json"))
        self.assertTrue(any(count > 0 for count in page.reply_counts))
        self.assertTrue(any(parent for parent in page.reply_to_ids))

    def test_cursor_only_page_has_no_posts(self) -> None:
        page = walker.parse_page(load("page_cursor_only.json"))
        self.assertEqual(page.post_ids, ())
        self.assertTrue(page.cursors)

    def test_no_credentials_in_fixtures(self) -> None:
        for name in ("page_nested_cursor.json", "page_kenpex_baseline.json", "page_cursor_only.json"):
            text = (FIXTURES / name).read_text(encoding="utf-8").lower()
            for secret in ("auth_token", "ct0", "bearer", "x-csrf"):
                self.assertNotIn(secret, text, f"{name} leaks {secret}")


class TopLevelOnlyWalkTests(unittest.TestCase):
    """A walk that follows only the top-level cursor must miss the nested posts.

    This is the regression that matters: it is exactly what gallery-dl
    does.
    """

    def test_top_level_only_walk_misses_the_nested_posts(self) -> None:
        page = walker.parse_page(load("page_kenpex_baseline.json"))
        top_level_posts = set(page.post_ids)
        nested_cursor_values = set(page.cursors) - {page.top_level_cursor}
        self.assertTrue(nested_cursor_values, "fixture has no nested cursor")

        # The nested cursor is a different value from the top-level one,
        # so a walk that only follows the top level never issues the
        # request that would return the posts behind it.
        self.assertNotIn(page.top_level_cursor, nested_cursor_values)
        self.assertTrue(top_level_posts)


class RequestShapeTests(unittest.TestCase):
    """The request shape comes from the installed gallery-dl, not a copy."""

    def test_endpoint_is_read_from_gallery_dl(self) -> None:
        endpoint = walker.tweet_detail_endpoint()
        self.assertTrue(endpoint.endswith("/TweetDetail"))

    def test_variables_template_comes_from_gallery_dl(self) -> None:
        variables, _toggles = walker.request_shape()
        self.assertIn("focalTweetId", variables)
        self.assertEqual(variables["referrer"], "profile")

    def test_field_toggles_come_from_gallery_dl(self) -> None:
        _variables, toggles = walker.request_shape()
        self.assertIn("withArticleRichContentState", toggles)

    def test_raises_when_gallery_dl_hides_the_endpoint(self) -> None:
        original = walker._load_gallery_dl()

        class Hidden:
            class TwitterAPI:
                @staticmethod
                def tweet_detail() -> None:
                    return None

        walker._gallery_dl = Hidden()
        try:
            with self.assertRaises(WalkerError):
                walker.tweet_detail_endpoint()
        finally:
            walker._gallery_dl = original


class DiscoverTests(unittest.TestCase):
    """`discover` drives the walk without a network."""

    def test_empty_focals_return_nothing(self) -> None:
        result = walker.discover(())
        self.assertEqual(result.post_ids, ())
        self.assertEqual(result.calls, 0)

    def test_walk_follows_nested_cursors(self) -> None:
        """A fake extractor proves the walk issues one request per cursor."""
        pages = {
            None: load("page_nested_cursor.json"),
            "nested": load("page_cursor_only.json"),
        }
        requests: list[str | None] = []

        class FakeApi:
            features_pagination = {"feature": True}

            def _call(self, endpoint: str, params: dict, method: str = "GET") -> dict:
                cursor = json.loads(params["variables"]).get("cursor")
                requests.append(cursor)
                return pages["nested" if cursor else None]

        class FakeExtractor:
            api = FakeApi()

        result = walker.discover(
            ("2121244702649532667",), request_cap=5, extractor=FakeExtractor()
        )

        self.assertGreaterEqual(len(requests), 2)
        self.assertIsNone(requests[0])
        self.assertIsNotNone(requests[1])
        self.assertTrue(result.post_ids)
        self.assertEqual(result.calls, len(requests))

    def test_request_cap_bounds_the_walk(self) -> None:
        """The cap stops the walk even when cursors keep appearing."""
        counter = {"n": 0}

        class FakeApi:
            features_pagination = {"feature": True}

            def _call(self, endpoint: str, params: dict, method: str = "GET") -> dict:
                counter["n"] += 1
                body = json.loads(json.dumps(load("page_nested_cursor.json")))
                entries = body["data"]["threaded_conversation_with_injections_v2"][
                    "instructions"
                ][1]["entries"]
                entries.append({
                    "entryId": f"cursor-bottom-fresh-{counter['n']}",
                    "content": {"__typename": "TimelineTimelineCursor", "value": f"v{counter['n']}"},
                })
                return body

        class FakeExtractor:
            api = FakeApi()

        result = walker.discover(
            ("2121244702649532667",),
            request_cap=3,
            extractor=FakeExtractor(),
            max_focals=1,
        )
        self.assertEqual(result.calls, 3)
        self.assertEqual(result.stopped_reason, "focal-cap")

    def test_under_captured_finds_posts_with_unseen_children(self) -> None:
        """A post reporting more replies than were found has a subtree left.

        ``reply_counts`` maps a post to the number of replies it reports.
        ``reply_to`` maps a post to its parent. Post ``a`` reports two
        replies but only one child was found, so its subtree is
        unreached.
        """
        gaps = walker._under_captured(
            {"a": 2, "b": 1, "c": 0},
            {"x": "a", "y": "b", "z": "b"},
        )
        self.assertEqual(gaps, ["a"])

    def test_walk_expands_its_own_focal_set(self) -> None:
        """One focal must find the whole thread.

        A post that reports more replies than the walk found is walked
        too, so the operator does not have to name every focal by hand.
        """
        pages = {
            None: load("page_nested_cursor.json"),
            "expanded": load("page_kenpex_baseline.json"),
        }
        walked_focals: list[str] = []

        class FakeApi:
            features_pagination = {"feature": True}

            def _call(self, endpoint: str, params: dict, method: str = "GET") -> dict:
                variables = json.loads(params["variables"])
                cursor = variables.get("cursor")
                walked_focals.append(variables["focalTweetId"])
                return pages["expanded" if cursor else None]

        class FakeExtractor:
            api = FakeApi()

        result = walker.discover(
            ("2121244702649532667",), request_cap=5, extractor=FakeExtractor()
        )
        self.assertTrue(result.post_ids)
        # The walk grew its own focal set rather than stopping at one.
        self.assertGreater(len(result.per_focal), 1)
        self.assertGreater(len(walked_focals), len(result.per_focal))

    def test_capture_dir_records_the_pages(self) -> None:
        """A run writes one response page per request, none overwritten."""
        import tempfile

        class FakeApi:
            features_pagination = {"feature": True}

            def _call(self, endpoint: str, params: dict, method: str = "GET") -> dict:
                return load("page_nested_cursor.json")

        class FakeExtractor:
            api = FakeApi()

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "walker"
            result = walker.discover(
                ("2121244702649532667",),
                request_cap=2,
                extractor=FakeExtractor(),
                capture_dir=target,
            )
            pages = sorted(target.glob("page-*.json"))
            self.assertEqual(len(pages), result.calls)
            body = json.loads(pages[0].read_text(encoding="utf-8"))
            self.assertIn("threaded_conversation_with_injections_v2", body["data"])

    def test_capture_dir_keeps_every_page_of_a_multi_focal_walk(self) -> None:
        """A walk over several focals must not reuse a page file name.

        The page number counts the whole walk, not one focal, so the
        evidence of one focal cannot overwrite another's.
        """
        import tempfile

        class FakeApi:
            features_pagination = {"feature": True}

            def _call(self, endpoint: str, params: dict, method: str = "GET") -> dict:
                return load("page_nested_cursor.json")

        class FakeExtractor:
            api = FakeApi()

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "walker"
            result = walker.discover(
                ("2121244702649532667",),
                request_cap=2,
                extractor=FakeExtractor(),
                capture_dir=target,
            )
            names = sorted(p.name for p in target.glob("page-*.json"))
            self.assertEqual(len(names), len(set(names)))
            self.assertEqual(len(names), result.calls)
            self.assertGreater(len(result.per_focal), 1)

    def test_posts_from_other_conversations_are_excluded(self) -> None:
        """A conversation page can pull in other conversations' posts.

        The walk must report only the focal's own conversation, or the
        ids feed straight into a capture and mix threads together.
        """
        pages = {
            None: load("page_nested_cursor.json"),
            "other": load("page_kenpex_baseline.json"),
        }

        class FakeApi:
            features_pagination = {"feature": True}

            def _call(self, endpoint: str, params: dict, method: str = "GET") -> dict:
                cursor = json.loads(params["variables"]).get("cursor")
                return pages["other" if cursor else None]

        class FakeExtractor:
            api = FakeApi()

        other_posts = set(walker.parse_page(pages["other"]).post_ids)
        self.assertTrue(other_posts)

        result = walker.discover(
            ("2121244702649532667",), request_cap=5, extractor=FakeExtractor()
        )
        self.assertTrue(result.post_ids)
        for post_id in result.post_ids:
            self.assertNotIn(post_id, other_posts)


class RateLimitTests(unittest.TestCase):
    """The walk must stay inside the endpoint's rate-limit window."""

    def test_budget_stops_the_walk(self) -> None:
        """The whole walk is capped, not just one focal."""
        tracker = walker._RateTracker(max_requests=3)
        tracker.check_budget()
        tracker.check_budget()
        tracker.check_budget()
        with self.assertRaises(walker.RateLimitReached):
            tracker.check_budget()

    def test_budget_error_names_the_budget(self) -> None:
        tracker = walker._RateTracker(max_requests=1)
        tracker.check_budget()
        with self.assertRaises(walker.RateLimitReached) as caught:
            tracker.check_budget()
        self.assertIn("budget of 1", str(caught.exception))

    def test_a_nearly_spent_window_stops_the_walk(self) -> None:
        """The walk stops before it spends the last requests in a window."""
        tracker = walker._RateTracker(max_requests=100)

        class FakeResponse:
            headers = {
                "x-rate-limit-remaining": "5",
                "x-rate-limit-reset": "1794705157",
            }

        tracker.observe(FakeResponse())
        self.assertEqual(tracker.remaining, 5)
        with self.assertRaises(walker.RateLimitReached) as caught:
            tracker.check_budget()
        self.assertIn("nearly spent", str(caught.exception))
        self.assertIn("5 left", str(caught.exception))

    def test_the_refill_time_is_reported(self) -> None:
        """The operator learns when the window refills."""
        tracker = walker._RateTracker(max_requests=100)

        class FakeResponse:
            headers = {
                "x-rate-limit-remaining": "0",
                "x-rate-limit-reset": "1794705157",
            }

        tracker.observe(FakeResponse())
        error = tracker.rate_limited_error()
        self.assertIn("refills at", str(error))
        self.assertIsNotNone(error.reset_at)

    def test_gallery_dl_abort_becomes_a_rate_limit_error(self) -> None:
        """gallery-dl's AbortExtraction is translated, not swallowed.

        With ``ratelimit=abort`` gallery-dl raises instead of sleeping
        until the window refills. The walker turns that into a message
        the operator can act on.
        """
        tracker = walker._RateTracker(max_requests=100)

        class FakeApi:
            features_pagination = {"feature": True}

            def _call(self, endpoint: str, params: dict, method: str = "GET") -> dict:
                raise AbortExtraction("Rate limit exceeded")

        class FakeExtractor:
            api = FakeApi()

        with self.assertRaises(walker.RateLimitReached):
            walker._request(
                FakeExtractor(),
                "2121244702649532667",
                None,
                walker.request_shape()[0],
                walker.request_shape()[1],
                tracker,
            )

    def test_the_walk_reports_the_refill_time(self) -> None:
        tracker = walker._RateTracker(max_requests=100)
        error = tracker.rate_limited_error()
        self.assertIn("rate limit reached", str(error))


class KenpexRegressionTests(unittest.TestCase):
    """The kenpex conversation: the fixture NOTE.md section 5 asked for."""

    def test_kenpex_page_posts_are_a_subset_of_the_expected_16(self) -> None:
        page = walker.parse_page(load("page_kenpex_baseline.json"))
        for post_id in page.post_ids:
            self.assertIn(post_id, KENPEX_EXPECTED_16)

    def test_kenpex_page_carries_the_posts_gallery_dl_drops(self) -> None:
        """The nested showmore cursor sits on a thread gallery-dl truncates."""
        page = walker.parse_page(load("page_kenpex_baseline.json"))
        self.assertIsNotNone(page.top_level_cursor)
        self.assertNotEqual(page.top_level_cursor, page.cursors[0])


if __name__ == "__main__":
    unittest.main()
