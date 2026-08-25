"""Offline TweetDetail parser, pure cursor walker, and global
human-paced :class:`RequestGovernor` for ``twitter.fetch_thread``.

This module owns three typed components:

1. The typed boundary dataclasses (:class:`Cursor`,
   :class:`TweetDetailPage`) and the pure JSON-to-typed-data
   parser :func:`parse_tweet_detail_page`. The parser inspects
   the TweetDetail wire path
   ``data.threaded_conversation_with_injections_v2.instructions``
   and converts typed timeline entries into existing
   :class:`twitter.models.PostData` instances. Cursors with
   eligible kinds (``Bottom``, ``ShowMore``, ``ShowMoreThreads``)
   are kept; Top and unknown cursors are dropped without
   raising. Tweets wrapped in
   :class:`TweetWithVisibilityResults` are unwrapped via their
   inner ``tweet`` field.

2. The pure FIFO continuation walker
   :func:`walk_continuation_queue` and the pure post-group
   merger :func:`merge_post_groups`. The walker has no
   transport, no sleeper, no request cap, and no roles of its
   own; the future orchestration wraps every provider call in
   :meth:`RequestGovernor.issue`.

3. The global human-paced :class:`RequestGovernor` (and its
   :class:`RequestBudgetExceeded` budget exception). The
   governor owns the ONLY global request count, the ONLY
   pacing state, and the ONLY ordered ``roles`` log. One
   governor per run wraps every provider call later
   (bootstrap homepage, bootstrap JS, tip TweetDetail, root
   TweetDetail, every continuation).

This module deliberately does NOT contain HTTP code, cookie
loading, transaction helpers, the production transport, or
the CLI. Those live in later tasks of the same track and
reuse the parser, the walker, and the governor declared here.
"""
from __future__ import annotations

import sys
from collections import deque
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol

# --- canonical package-or-script import shim ---
# Both `python -m twitter.fetch_thread` (package-mode) and
# `python scripts/twitter/fetch_thread.py` (script-mode) must work.
try:
    from .models import PostData, PostMetrics
except ImportError:  # pragma: no cover - script-mode import
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from models import PostData, PostMetrics


# --- fetcher-local types ---


# --- provider-error taxonomy (Task 9) ---


class FetchError(RuntimeError):
    """Base class for fetcher errors that fail closed.

    The fetcher never retries, never logs, and never echoes
    response bodies, URLs, headers, cursor values, or secret
    values in exception messages. Status code and exception
    type are the only diagnostic surfaces.
    """


class RequestBudgetExceeded(FetchError):
    """Raised when the global request budget is exhausted.

    Inherits from :class:`FetchError` so callers can catch the
    full fetcher-error family with one ``except`` clause. The
    class remains a :class:`RuntimeError` transitively because
    :class:`FetchError` is a :class:`RuntimeError`. Existing
    governor tests that assert the ``RuntimeError`` lineage
    continue to pass.
    """


class AuthError(FetchError):
    """HTTP 401 or 403. The authenticated session is no longer valid."""


class RateLimitError(FetchError):
    """HTTP 429. Twitter rate limit hit; no automatic retry."""


class ProviderError(FetchError):
    """Any non-2xx that is not 401/403/429, or a transport-layer
    failure (``TimeoutError``, ``ConnectionError``, ``OSError``)
    raised by the wrapped operation."""


ELIGIBLE_CURSOR_TYPES: frozenset[str] = frozenset(
    {"Bottom", "ShowMore", "ShowMoreThreads"},
)


@dataclass(frozen=True)
class Cursor:
    """A typed cursor entry from a TweetDetail response."""
    value: str
    cursor_type: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Cursor.value must be non-empty")
        if self.cursor_type not in ELIGIBLE_CURSOR_TYPES:
            raise ValueError(
                f"Cursor.cursor_type {self.cursor_type!r} is not in eligible set"
            )


@dataclass(frozen=True)
class TweetDetailPage:
    """Parsed TweetDetail page: typed posts, eligible cursors, and
    the focal post's ``legacy.conversation_id_str``."""
    posts: tuple[PostData, ...]
    cursors: tuple[Cursor, ...]
    focal_conversation_id: str | None = None


# --- typed raw-boundary helpers ---


def _from_wire_text(node: Mapping[str, object], key: str) -> str:
    raw = node.get(key)
    if not isinstance(raw, str):
        raise KeyError(f"required string field {key!r}")
    return raw


def _from_wire_int(node: Mapping[str, object], key: str) -> int:
    raw = node.get(key)
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise KeyError(f"required int field {key!r}")
    return raw


def _from_wire_optional_int(
    node: Mapping[str, object], key: str,
) -> int | None:
    """Accept ``int`` or numeric-string. Anything else is rejected
    with ``KeyError``. ``None`` propagates as ``None``."""
    raw = node.get(key)
    if raw is None:
        return None
    if isinstance(raw, bool) or not isinstance(raw, int):
        if isinstance(raw, str) and raw.lstrip("-").isdigit():
            return int(raw)
        raise KeyError(f"optional int field {key!r} has wrong type")
    return raw


# --- per-tweet normalization ---


def _find_item_content(
    entry: Mapping[str, object],
) -> Mapping[str, object] | None:
    """Return the entry's ``itemContent``-shaped payload, accepting
    all three layouts seen in real TweetDetail wire responses:
    ``entry.content.itemContent``, ``entry.item.itemContent``,
    and ``entry.itemContent`` directly."""
    content = entry.get("content")
    if isinstance(content, Mapping):
        ic = content.get("itemContent")
        if isinstance(ic, Mapping):
            return ic
    item = entry.get("item")
    if isinstance(item, Mapping):
        ic = item.get("itemContent")
        if isinstance(ic, Mapping):
            return ic
    ic = entry.get("itemContent")
    if isinstance(ic, Mapping):
        return ic
    return None


def _find_cursor_source(entry: Mapping[str, object]) -> Mapping[str, object] | None:
    """Return the entry's cursor source mapping, accepting all
    three layouts (top-level content, module item.itemContent,
    direct itemContent)."""
    content = entry.get("content")
    if isinstance(content, Mapping) and "cursorType" in content:
        return content
    item = entry.get("item")
    if isinstance(item, Mapping):
        item_content = item.get("itemContent")
        if (
            isinstance(item_content, Mapping)
            and "cursorType" in item_content
        ):
            return item_content
    ic = entry.get("itemContent")
    if isinstance(ic, Mapping) and "cursorType" in ic:
        return ic
    return None


def _entry_type(entry: Mapping[str, object]) -> object:
    content = entry.get("content")
    if isinstance(content, Mapping):
        return content.get("entryType")
    return None


def _resolve_post_id(tweet: Mapping[str, object]) -> str:
    rest_id = tweet.get("rest_id")
    if isinstance(rest_id, str) and rest_id:
        return rest_id
    legacy = tweet.get("legacy")
    if isinstance(legacy, Mapping):
        legacy_id = legacy.get("id_str")
        if isinstance(legacy_id, str) and legacy_id:
            return legacy_id
    raise KeyError("tweet: missing rest_id and legacy.id_str")


def _resolve_user(tweet: Mapping[str, object]) -> tuple[str, str]:
    """Return ``(author, handle)`` for the tweet.

    Current shape first: ``user_results.result.core.name`` and
    ``user_results.result.core.screen_name``. BOTH fields must be
    non-empty strings for the current shape to win; otherwise
    fall back to the legacy pair
    ``user_results.result.legacy.name`` and
    ``user_results.result.legacy.screen_name``. The legacy pair
    is mandatory once the current shape is rejected.
    """
    core = tweet.get("core")
    user_results_node: object = None
    if isinstance(core, Mapping):
        user_results_node = core.get("user_results")
    user: object = None
    if isinstance(user_results_node, Mapping):
        user = user_results_node.get("result")
    if isinstance(user, Mapping):
        # Current shape: user.core.name / user.core.screen_name.
        # Wins only when BOTH fields are non-empty strings;
        # otherwise fall through to the legacy pair.
        user_core = user.get("core")
        if isinstance(user_core, Mapping):
            name_node = user_core.get("name")
            screen_node = user_core.get("screen_name")
            if (
                isinstance(name_node, str)
                and name_node
                and isinstance(screen_node, str)
                and screen_node
            ):
                return str(name_node), str(screen_node)
        # Fallback: user.legacy.name / user.legacy.screen_name
        user_legacy = user.get("legacy")
        if isinstance(user_legacy, Mapping):
            name = _from_wire_text(user_legacy, "name")
            handle = _from_wire_text(user_legacy, "screen_name")
            return name, handle
    raise KeyError("tweet: missing user_results.result core or legacy")


def _resolve_text(tweet: Mapping[str, object]) -> str:
    note_tweet = tweet.get("note_tweet")
    if isinstance(note_tweet, Mapping):
        results = note_tweet.get("note_tweet_results")
        if isinstance(results, Mapping):
            inner = results.get("result")
            if isinstance(inner, Mapping):
                txt = inner.get("text")
                if isinstance(txt, str) and txt:
                    return txt
    legacy = tweet.get("legacy")
    if isinstance(legacy, Mapping):
        full_text = legacy.get("full_text")
        if isinstance(full_text, str) and full_text:
            return full_text
    raise KeyError("tweet: missing note_tweet text and legacy.full_text")


def _normalize_created_at(created_at: str) -> str:
    """Twitter ``created_at`` → ``YYYY-MM-DD HH:MM:SS``."""
    dt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _resolve_media_urls(legacy: Mapping[str, object]) -> tuple[str, ...]:
    """Collect media URLs from ``legacy.extended_entities.media[]``
    (falling back to ``entities.media[]``). Each photo URL is added;
    each video contributes its highest-bitrate ``video/mp4``
    variant URL. Duplicates are dropped, preserving order."""
    ee_node = legacy.get("extended_entities")
    ents: object = ee_node if isinstance(ee_node, Mapping) else None
    if ents is None:
        ents = legacy.get("entities")
    if not isinstance(ents, Mapping):
        return ()
    media_node = ents.get("media")
    if not isinstance(media_node, list):
        return ()
    urls: list[str] = []
    for m in media_node:
        if not isinstance(m, Mapping):
            continue
        photo_url = m.get("media_url_https")
        if not isinstance(photo_url, str):
            photo_url = m.get("media_url")
        if isinstance(photo_url, str) and photo_url:
            urls.append(photo_url)
        video_info = m.get("video_info")
        if isinstance(video_info, Mapping):
            variants_node = video_info.get("variants")
            if isinstance(variants_node, list):
                best: tuple[int, str] | None = None
                for v in variants_node:
                    if not isinstance(v, Mapping):
                        continue
                    if v.get("content_type") != "video/mp4":
                        continue
                    vurl = v.get("url")
                    if not isinstance(vurl, str):
                        continue
                    br_node = v.get("bitrate")
                    if isinstance(br_node, bool) or not isinstance(br_node, int):
                        br = 0
                    else:
                        br = br_node
                    if best is None or br > best[0]:
                        best = (br, vurl)
                if best is not None:
                    urls.append(best[1])
    seen: set[str] = set()
    deduped: list[str] = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            deduped.append(u)
    return tuple(deduped)


def _build_post_data(tweet: Mapping[str, object]) -> PostData:
    """Convert an unwrapped tweet mapping into a typed
    :class:`PostData`. Raises ``KeyError`` or ``TypeError`` on
    missing or wrong-typed required fields."""
    post_id = _resolve_post_id(tweet)
    author, handle = _resolve_user(tweet)
    text = _resolve_text(tweet)
    legacy_node = tweet.get("legacy")
    if not isinstance(legacy_node, Mapping):
        raise KeyError(f"tweet {post_id}: missing legacy")
    created_at = _from_wire_text(legacy_node, "created_at")
    timestamp = _normalize_created_at(created_at)
    reply_to_node = legacy_node.get("in_reply_to_status_id_str")
    reply_to_id: str | None = (
        str(reply_to_node)
        if isinstance(reply_to_node, str) and reply_to_node
        else None
    )
    quote_node = legacy_node.get("quoted_status_id_str")
    quote_of_id: str | None = (
        str(quote_node)
        if isinstance(quote_node, str) and quote_node
        else None
    )
    media_urls = _resolve_media_urls(legacy_node)
    views_node = tweet.get("views")
    views_count: int | None
    if isinstance(views_node, Mapping):
        views_count = _from_wire_optional_int(views_node, "count")
    else:
        views_count = None
    metrics = PostMetrics(
        reply_count=_from_wire_int(legacy_node, "reply_count"),
        repost_count=_from_wire_int(legacy_node, "retweet_count"),
        like_count=_from_wire_int(legacy_node, "favorite_count"),
        view_count=views_count,
    )
    return PostData(
        post_id=post_id,
        author=author,
        handle=handle,
        text=text,
        timestamp=timestamp,
        media_urls=media_urls,
        reply_to_id=reply_to_id,
        quote_of_id=quote_of_id,
        metrics=metrics,
    )


def _normalize_tweet_entry(entry: Mapping[str, object]) -> PostData | None:
    """Return a :class:`PostData` if ``entry`` carries a Tweet.
    Returns ``None`` for cursors, modules, tombstone / unavailable
    results, or entries whose inner ``__typename`` is not ``Tweet``."""
    entry_type = _entry_type(entry)
    item_type = entry.get("itemType")
    if (
        entry_type not in ("TimelineTimelineItem", "TimelineTweet")
        and item_type not in ("TimelineTimelineItem", "TimelineTweet")
    ):
        return None
    ic = _find_item_content(entry)
    if ic is None:
        return None
    tweet_results = ic.get("tweet_results")
    if not isinstance(tweet_results, Mapping):
        return None
    inner = tweet_results.get("result")
    if not isinstance(inner, Mapping):
        return None
    if inner.get("__typename") == "TweetWithVisibilityResults":
        inner = inner.get("tweet")
        if not isinstance(inner, Mapping):
            return None
    if inner.get("__typename") != "Tweet":
        return None
    return _build_post_data(inner)


def _normalize_cursor_entry(entry: Mapping[str, object]) -> Cursor | None:
    """Return a :class:`Cursor` for ``entry`` if it is a
    TimelineTimelineCursor with an eligible ``cursorType``.
    Top and unknown kinds are silently dropped."""
    cursor_source = _find_cursor_source(entry)
    if cursor_source is None:
        return None
    entry_type = _entry_type(entry)
    item_type = entry.get("itemType")
    if (
        entry_type != "TimelineTimelineCursor"
        and item_type != "TimelineTimelineCursor"
    ):
        return None
    cursor_type_node = cursor_source.get("cursorType")
    if not isinstance(cursor_type_node, str):
        return None
    if cursor_type_node not in ELIGIBLE_CURSOR_TYPES:
        return None
    value_node = cursor_source.get("value")
    if isinstance(value_node, str):
        value = value_node
    elif isinstance(value_node, int) and not isinstance(value_node, bool):
        value = str(value_node)
    else:
        return None
    try:
        return Cursor(value=value, cursor_type=cursor_type_node)
    except ValueError:
        return None


def _extract_focal_conversation_id(
    entry: Mapping[str, object], focal_id: str,
) -> str | None:
    """Return ``legacy.conversation_id_str`` from the wrapped tweet
    whose id equals ``focal_id``. Inspects only the current entry;
    iterators like :func:`_walk_entries` are responsible for
    visiting every nested timeline node and calling this function
    on each."""
    ic = _find_item_content(entry)
    if ic is None:
        return None
    tweet_results = ic.get("tweet_results")
    if not isinstance(tweet_results, Mapping):
        return None
    inner = tweet_results.get("result")
    if not isinstance(inner, Mapping):
        return None
    if inner.get("__typename") == "TweetWithVisibilityResults":
        inner = inner.get("tweet")
    if not isinstance(inner, Mapping):
        return None
    cand_id = inner.get("rest_id")
    if not isinstance(cand_id, str) or not cand_id:
        legacy = inner.get("legacy")
        if isinstance(legacy, Mapping):
            cand_id = legacy.get("id_str")
    if not isinstance(cand_id, str) or cand_id != focal_id:
        return None
    legacy = inner.get("legacy")
    if not isinstance(legacy, Mapping):
        return None
    cid = legacy.get("conversation_id_str")
    if isinstance(cid, str) and cid:
        return cid
    return None


def _walk_entries(
    entries: Sequence[object], focal_id: str | None,
) -> tuple[list[PostData], list[Cursor], str | None]:
    """Walk entries / modules iteratively via an explicit stack.

    The walk is bounded to the typed entries / modules tree. It
    does NOT recursively scan tweet / quote / user payloads for
    cursor-looking strings; cursors are only read from the
    typed cursor source locations at the entry / module level.

    Source order is preserved: the stack is initialised with
    the entries in reverse so the first ``pop`` yields the
    first source entry, and module items are pushed in reverse
    so the same invariant applies recursively.

    Returns ``(posts, cursors, focal_conversation_id_or_none)``.
    """
    posts: list[PostData] = []
    cursors: list[Cursor] = []
    focal_conversation_id: str | None = None
    stack: list[object] = list(reversed(list(entries)))
    while stack:
        node = stack.pop()
        if not isinstance(node, Mapping):
            continue
        post = _normalize_tweet_entry(node)
        if post is not None:
            posts.append(post)
        cursor = _normalize_cursor_entry(node)
        if cursor is not None:
            cursors.append(cursor)
        if focal_id is not None and focal_conversation_id is None:
            cid = _extract_focal_conversation_id(node, focal_id)
            if cid is not None:
                focal_conversation_id = cid
        content = node.get("content")
        if isinstance(content, Mapping) and content.get(
            "entryType"
        ) == "TimelineTimelineModule":
            items_node = content.get("items")
            if isinstance(items_node, list):
                for item in reversed(items_node):
                    stack.append(item)
    return posts, cursors, focal_conversation_id


def parse_tweet_detail_page(
    raw: object, *, focal_id: str | None = None,
) -> TweetDetailPage:
    """Parse a TweetDetail response into typed posts, eligible
    cursors, and the focal post's ``legacy.conversation_id_str``.

    The wire path is
    ``data.threaded_conversation_with_injections_v2.instructions``;
    this function walks only those instructions and the module
    contents they reference. It does not recursively scan
    tweet / quote / user payloads for cursor-looking strings.

    Args:
        raw: The deserialised wire JSON. Accepts ``object`` so
            the caller can hand anything to the parser; a
            non-mapping ``raw`` produces an empty page rather
            than raising.
        focal_id: When set, the parser walks all entries
            (including those nested in TimelineTimelineModule
            content.items[]) to find the entry whose id equals
            ``focal_id`` and exposes its
            ``legacy.conversation_id_str`` as
            ``page.focal_conversation_id``.

    Returns:
        A :class:`TweetDetailPage`. ``posts`` is deduped by id
        with last-seen data preserved (first-seen order intact);
        ``cursors`` is deduped by value with first-seen wins.
    """
    if not isinstance(raw, Mapping):
        return TweetDetailPage(
            posts=(), cursors=(), focal_conversation_id=None,
        )
    data_node = raw.get("data")
    if not isinstance(data_node, Mapping):
        return TweetDetailPage(
            posts=(), cursors=(), focal_conversation_id=None,
        )
    threaded = data_node.get("threaded_conversation_with_injections_v2")
    if not isinstance(threaded, Mapping):
        return TweetDetailPage(
            posts=(), cursors=(), focal_conversation_id=None,
        )
    instructions = threaded.get("instructions")
    if not isinstance(instructions, list):
        return TweetDetailPage(
            posts=(), cursors=(), focal_conversation_id=None,
        )
    all_posts: list[PostData] = []
    all_cursors: list[Cursor] = []
    final_focal: str | None = None
    for instruction in instructions:
        if not isinstance(instruction, Mapping):
            continue
        itype = instruction.get("type")
        if itype == "TimelineAddEntries":
            entries = instruction.get("entries")
            if isinstance(entries, list):
                posts, cursors, focal = _walk_entries(entries, focal_id)
                all_posts.extend(posts)
                all_cursors.extend(cursors)
                if final_focal is None and focal is not None:
                    final_focal = focal
        elif itype == "TimelineAddToModule":
            module_items = instruction.get("moduleItems")
            if isinstance(module_items, list):
                posts, cursors, focal = _walk_entries(module_items, focal_id)
                all_posts.extend(posts)
                all_cursors.extend(cursors)
                if final_focal is None and focal is not None:
                    final_focal = focal
        elif itype == "TimelineReplaceEntry":
            entry = instruction.get("entry")
            if isinstance(entry, Mapping):
                posts, cursors, focal = _walk_entries([entry], focal_id)
                all_posts.extend(posts)
                all_cursors.extend(cursors)
                if final_focal is None and focal is not None:
                    final_focal = focal
    by_id: dict[str, PostData] = {}
    order: list[str] = []
    for post in all_posts:
        if post.post_id not in by_id:
            order.append(post.post_id)
        by_id[post.post_id] = post
    deduped_posts: list[PostData] = [by_id[oid] for oid in order]
    seen_cursor_values: set[str] = set()
    deduped_cursors: list[Cursor] = []
    for c in all_cursors:
        if c.value not in seen_cursor_values:
            seen_cursor_values.add(c.value)
            deduped_cursors.append(c)
    return TweetDetailPage(
        posts=tuple(deduped_posts),
        cursors=tuple(deduped_cursors),
        focal_conversation_id=final_focal,
    )


# --- root resolution (Task 3) ---


def resolve_root_from_tip(tip: str, page: TweetDetailPage) -> str:
    """Resolve the conversation root from a parsed tip page.

    Returns ``page.focal_conversation_id``, which
    :func:`parse_tweet_detail_page` extracted from the focal tip
    post's ``legacy.conversation_id_str``.

    Verifies that ``tip`` is present in ``page.posts`` and that
    ``page.focal_conversation_id`` is a non-empty string. Neither
    a parent-chain walk nor a ``reply_to_id is None`` heuristic is
    used; the resolved root must come from the focal post's
    conversation id. Parent-chain closure is validated later after
    the tip+root page merge.

    Args:
        tip: The post id of the input tip (the user's ``--tip``
            value).
        page: A parsed :class:`TweetDetailPage` from
            :func:`parse_tweet_detail_page`.

    Returns:
        The resolved conversation root post id.

    Raises:
        ValueError: ``tip`` is not present in ``page.posts``.
        ValueError: ``page.focal_conversation_id`` is ``None`` or
            an empty string.
    """
    tip_ids = {post.post_id for post in page.posts}
    if tip not in tip_ids:
        raise ValueError(f"tip {tip!r} not present in page.posts")
    focal = page.focal_conversation_id
    if not focal:
        raise ValueError(
            "page.focal_conversation_id is missing or empty; "
            "cannot resolve conversation root"
        )
    return focal


# --- tip + root page merge (Task 4) ---


def merge_post_groups(
    *groups: Sequence[PostData],
) -> tuple[PostData, ...]:
    """Merge multiple post sequences into a deduped tuple.

    Last-seen data wins: when the same ``post_id`` appears in more
    than one group, the later group's :class:`PostData` replaces the
    earlier one. First-insertion order is preserved: the position of
    each id in the output is the position of its first appearance in
    the iteration order. Pure function; no I/O, network, or sample
    constants.
    """
    seen: dict[str, PostData] = {}
    order: list[str] = []
    for group in groups:
        for post in group:
            if post.post_id not in seen:
                order.append(post.post_id)
            seen[post.post_id] = post
    return tuple(seen[pid] for pid in order)


# --- continuation queue walker (Task 5) ---


@dataclass(frozen=True)
class ContinuationWalkResult:
    """Outcome of :func:`walk_continuation_queue`.

    ``posts`` is the deduped union of the initial page's posts and
    every continuation page's posts, with last-seen data wins and
    first-insertion order preserved. ``fetched_cursor_count`` is
    the number of times the walker invoked ``fetch_page`` (i.e.,
    the number of unseen eligible cursors it followed).
    """
    posts: tuple[PostData, ...]
    fetched_cursor_count: int


def walk_continuation_queue(
    initial_page: TweetDetailPage,
    *,
    fetch_page: Callable[[Cursor], TweetDetailPage],
) -> ContinuationWalkResult:
    """Walk the eligible explicit reply cursor queue, FIFO.

    Seeds the queue with ``initial_page.cursors``. For each unseen
    cursor value (deduped by ``Cursor.value``), invokes
    ``fetch_page`` exactly once, merges the returned page's posts
    into the accumulator via :func:`merge_post_groups`, and
    enqueues the returned page's own cursors. Iteration terminates
    when the queue empties.

    The walker has no HTTP, sleep, retry, request cap, root/tip
    special case, or logging. The future global ``RequestGovernor``
    wraps ``fetch_page`` and is the only request cap; depth /
    loop behaviour is unbounded here.

    Exceptions raised by ``fetch_page`` propagate immediately on
    the call that raised them. The walker does not catch, swallow,
    or re-invoke the callback after a failure.

    Args:
        initial_page: The starting :class:`TweetDetailPage`. Its
            ``posts`` seed the accumulator; its ``cursors`` seed
            the FIFO queue.
        fetch_page: Callable invoked with one :class:`Cursor` and
            returning the parsed page for that continuation.

    Returns:
        A :class:`ContinuationWalkResult` with the merged posts
        and the count of callback invocations.
    """
    queue: deque[Cursor] = deque(initial_page.cursors)
    seen_cursor_values: set[str] = set()
    accumulator: tuple[PostData, ...] = initial_page.posts
    fetched_cursor_count: int = 0
    while queue:
        cursor = queue.popleft()
        if cursor.value in seen_cursor_values:
            continue
        seen_cursor_values.add(cursor.value)
        next_page = fetch_page(cursor)
        fetched_cursor_count += 1
        accumulator = merge_post_groups(accumulator, next_page.posts)
        for next_cursor in next_page.cursors:
            if next_cursor.value not in seen_cursor_values:
                queue.append(next_cursor)
    return ContinuationWalkResult(
        posts=accumulator,
        fetched_cursor_count=fetched_cursor_count,
    )


# --- global human-paced request governor (Task 8) ---


class Sleeper(Protocol):
    """The duck-typed surface the governor depends on.

    Production passes a real sleeper that blocks for
    ``seconds``; tests pass ``RecordingSleeper`` from
    :mod:`twitter.tests.fetch_thread_helpers`, which records
    durations without blocking.
    """

    def sleep(self, seconds: float) -> None:
        """Block (or record) for ``seconds`` seconds."""


class RequestGovernor:
    """Global, human-paced request envelope.

    Exactly one :class:`RequestGovernor` wraps every provider
    call later in the orchestration (bootstrap homepage,
    bootstrap JS, tip TweetDetail, root TweetDetail, every
    continuation). The governor owns the **only** global request
    count and the **only** pacing state. The pure cursor walker
    :func:`walk_continuation_queue` carries no
    ``max_requests``, no request index, no sleeper, and no role
    log of its own.

    Behaviour:

    - ``max_requests >= 1`` and ``min_delay >= 0`` are enforced
      at construction; non-empty ``role`` is enforced at every
      ``issue``.
    - Before every ``issue``: if ``count >= max_requests`` the
      governor raises :class:`RequestBudgetExceeded` **before**
      sleeping and **before** invoking the operation. No sleep
      is appended, no role is appended.
    - The very first attempted call does not sleep. Every later
      attempted call sleeps exactly once with the configured
      ``min_delay`` before invoking the operation.
    - The role is appended and counted exactly once,
      immediately before invoking the operation. If the
      operation raises, the attempted call remains counted; the
      governor does not catch, retry, or strip the role.
    - No logging, no HTTP, no URL inspection, no cursor
      inspection, no retry, no concurrency, no time polling,
      no automatic backoff.
    """

    def __init__(
        self,
        *,
        max_requests: int = 8,
        min_delay: float = 5.0,
        sleeper: Sleeper,
    ) -> None:
        if not isinstance(max_requests, int) or isinstance(max_requests, bool):
            raise ValueError(
                f"max_requests must be int, got {type(max_requests).__name__}",
            )
        if max_requests < 1:
            raise ValueError(
                f"max_requests must be >= 1, got {max_requests}",
            )
        if not isinstance(min_delay, (int, float)) or isinstance(min_delay, bool):
            raise ValueError(
                f"min_delay must be numeric, got {type(min_delay).__name__}",
            )
        if float(min_delay) < 0.0:
            raise ValueError(
                f"min_delay must be >= 0, got {min_delay}",
            )
        if sleeper is None:
            raise ValueError("sleeper must not be None")
        self._max_requests: int = max_requests
        self._min_delay: float = float(min_delay)
        self._sleeper: Sleeper = sleeper
        self._roles: list[str] = []

    @property
    def count(self) -> int:
        """The number of attempted calls counted so far."""
        return len(self._roles)

    @property
    def roles(self) -> tuple[str, ...]:
        """The ordered tuple of roles appended for attempted calls."""
        return tuple(self._roles)

    def issue(
        self,
        role: str,
        operation: Callable[[], tuple[int, str]],
    ) -> tuple[int, str]:
        """Wrap ``operation`` in the pacing + budget envelope.

        Args:
            role: A non-empty label for the attempted call
                (e.g., ``"bootstrap_homepage"``,
                ``"tip_tweet_detail"``,
                ``"continuation_tweet_detail"``). Appended to
                :attr:`roles` exactly once on attempted calls.
            operation: A zero-argument callable returning
                ``(status_code, body_text)``. The governor
                invokes it at most once.

        Returns:
            The ``(status_code, body_text)`` tuple returned by
            ``operation``.

        Raises:
            ValueError: ``role`` is empty or not a string.
            RequestBudgetExceeded: ``count >= max_requests``
                before this call. Raised **before** sleeping and
                **before** invoking ``operation``; the operation
                is not called, no role is appended, no sleep is
                recorded.
            Exception: any exception raised by ``operation``
                propagates immediately. The attempted call is
                counted (the role was already appended), and the
                governor does not retry.
        """
        if not isinstance(role, str):
            raise ValueError(
                f"role must be str, got {type(role).__name__}",
            )
        if not role:
            raise ValueError("role must be non-empty")
        if self.count >= self._max_requests:
            raise RequestBudgetExceeded(
                f"request budget of {self._max_requests} exhausted "
                f"before issuing role {role!r}",
            )
        if self.count > 0:
            self._sleeper.sleep(self._min_delay)
        self._roles.append(role)
        return operation()


# --- shared provider-error adapter (Task 9) ---


def issue_provider_request(
    governor: RequestGovernor,
    *,
    role: str,
    operation: Callable[[], tuple[int, str]],
) -> str:
    """Run a single provider request through ``governor`` and
    translate the outcome into either a body string or a typed
    :class:`FetchError` subclass.

    Behaviour:

    - The wrapped ``operation`` is invoked exactly once through
      :meth:`RequestGovernor.issue`. The governor owns the
      pacing, the role log, and the budget cap.
    - 2xx responses (``200``-``299``) return the body string
      unchanged.
    - ``401`` and ``403`` raise :class:`AuthError`.
    - ``429`` raises :class:`RateLimitError`.
    - Any other non-2xx status raises :class:`ProviderError`.
    - ``TimeoutError``, ``ConnectionError``, and ``OSError`` raised
      by ``operation`` are translated into :class:`ProviderError`
      chained from the original via ``raise ... from exc``.
    - ``RequestBudgetExceeded`` (raised by the governor when the
      cap is reached) propagates unchanged. It is already a
      :class:`FetchError` subclass and remains a
      :class:`RuntimeError`.
    - Arbitrary programmer/parser exceptions (e.g.,
      :class:`ValueError`) propagate unchanged; they are not
      mislabelled as a provider failure.

    Diagnostic policy: exception messages are limited to the
    numeric HTTP status and the exception class name. They never
    include the response body, the URL, header values, cursor
    values, or any secret value. The ``role`` argument is the
    caller's own label and is intentionally not echoed into the
    exception.
    """
    try:
        status, body = governor.issue(role, operation)
    except (TimeoutError, ConnectionError, OSError) as exc:
        raise ProviderError("transport error") from exc
    if 200 <= status <= 299:
        return body
    if status in (401, 403):
        raise AuthError(f"http {status}")
    if status == 429:
        raise RateLimitError(f"http {status}")
    raise ProviderError(f"http {status}")
