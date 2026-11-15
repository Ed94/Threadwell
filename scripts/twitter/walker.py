"""Recursive cursor walker for X conversation threads.

``gallery-dl`` with ``conversations=true`` follows only the top-level
``cursor-bottom-*`` continuation. Replies reachable only through a
``cursor-showmore-*`` nested inside a ``conversationthread-*`` module are
dropped without warning. This module issues the same ``TweetDetail``
request gallery-dl issues, then follows **every** cursor it finds at any
depth.

The request shape is read from the installed gallery-dl at runtime
rather than hardcoded, so a gallery-dl upgrade is picked up without a
code change. When gallery-dl does not expose the endpoint, this module
raises instead of falling back to a stale literal.

Nothing here writes to the vault.
"""
from __future__ import annotations

import ast
import inspect
import json
import logging
import re
import textwrap
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from .paths import COOKIES
except ImportError:  # pragma: no cover - script-mode import
    from paths import COOKIES

logger = logging.getLogger(__name__)

# gallery-dl is imported lazily: only the walker needs it, and importing
# it costs ~100 ms at module import.
_gallery_dl: Any = None

# Marker standing in for gallery-dl's ``tweet_id`` argument in the
# variables template it reads from its own source.
FOCAL_TWEET_ID = "__focal_tweet_id__"


class WalkerError(RuntimeError):
    """Raised when the walker cannot build or run a request."""


@dataclass(frozen=True)
class WalkerResult:
    """What one walk found."""
    post_ids: tuple[str, ...]
    calls: int
    per_focal: dict[str, tuple[str, ...]]
    stopped_reason: str


@dataclass(frozen=True)
class _Page:
    """One TweetDetail response, reduced to what the walker needs."""
    post_ids: tuple[str, ...]
    conversation_ids: tuple[str, ...]
    reply_counts: tuple[int, ...]
    reply_to_ids: tuple[str | None, ...]
    cursors: tuple[str, ...]
    top_level_cursor: str | None


def _load_gallery_dl() -> Any:
    """Import gallery-dl's Twitter extractor module."""
    global _gallery_dl
    if _gallery_dl is None:
        try:
            from gallery_dl.extractor import twitter as gd_twitter
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise WalkerError(
                "gallery-dl is required by the walker: pip install gallery-dl"
            ) from exc
        _gallery_dl = gd_twitter
    return _gallery_dl


def tweet_detail_endpoint() -> str:
    """Return the TweetDetail GraphQL endpoint from the installed gallery-dl.

    Raises ``WalkerError`` when gallery-dl does not expose it. The
    endpoint carries an operation hash that upstream rotates, so there is
    deliberately no hardcoded fallback.
    """
    twitter = _load_gallery_dl()
    try:
        constants = twitter.TwitterAPI.tweet_detail.__code__.co_consts
    except AttributeError as exc:  # pragma: no cover - upstream drift
        raise WalkerError(
            "gallery-dl no longer exposes TwitterAPI.tweet_detail"
        ) from exc
    for value in constants:
        if isinstance(value, str) and value.endswith("/TweetDetail"):
            return value
    raise WalkerError("gallery-dl does not expose a TweetDetail endpoint")


def _eval_literal(node: ast.AST) -> Any:
    """Evaluate a literal AST node, tolerating a bare name for the tweet id.

    gallery-dl writes ``"focalTweetId": tweet_id`` where ``tweet_id`` is
    the method argument. That name is replaced with the
    ``FOCAL_TWEET_ID`` marker and filled in per request.
    """
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return FOCAL_TWEET_ID
    if isinstance(node, ast.Dict):
        return {
            _eval_literal(key): _eval_literal(value)
            for key, value in zip(node.keys, node.values)
            if key is not None
        }
    if isinstance(node, ast.List):
        return [_eval_literal(element) for element in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(_eval_literal(element) for element in node.elts)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_literal(node.operand)
    raise WalkerError(f"gallery-dl uses a non-literal expression: {type(node).__name__}")


def _literal_from_source(source: str, name: str) -> dict[str, Any]:
    """Extract a dict literal assigned to ``name`` from gallery-dl source.

    The variables template and field toggles are literals in
    ``TwitterAPI.tweet_detail``. Reading them from the installed source
    keeps the walker in step with gallery-dl instead of freezing a copy.
    """
    tree = ast.parse(textwrap.dedent(source))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == name:
                value = _eval_literal(node.value)
                if isinstance(value, dict):
                    return value
    raise WalkerError(f"gallery-dl does not define a {name} literal")


def request_shape() -> tuple[dict[str, Any], dict[str, Any]]:
    """Return the ``(variables, field_toggles)`` pair gallery-dl sends."""
    twitter = _load_gallery_dl()
    source = inspect.getsource(twitter.TwitterAPI.tweet_detail)
    variables = _literal_from_source(source, "variables")
    toggles = _literal_from_source(source, "field_toggles")
    return variables, toggles


def build_extractor() -> Any:
    """Build a gallery-dl extractor that is authenticated with the vault cookies.

    Cookies, the CSRF token, and the transaction id all come from
    gallery-dl's own request layer, so the walker speaks the same
    protocol gallery-dl does.
    """
    twitter = _load_gallery_dl()
    url = "https://x.com/i/web/status/1"
    extractor = twitter.TwitterTweetExtractor.from_url(url)
    if extractor is None:
        raise WalkerError("gallery-dl could not build a Twitter tweet extractor")
    extractor.initialize()
    extractor.cookies_load(str(COOKIES))
    csrf = extractor.cookies.get("ct0", domain=".x.com")
    if csrf:
        extractor.api.headers["x-csrf-token"] = csrf
    extractor.api.headers["x-twitter-auth-type"] = "OAuth2Session"
    extractor.login()
    return extractor


def _cursor_value(entry: dict[str, Any]) -> str | None:
    """Extract a continuation cursor value from an entry.

    Twitter uses several shapes for the same thing: a top-level cursor
    entry, a cursor nested in a thread module, and a legacy
    ``operation.cursor`` wrapper. Cursor values are opaque and are never
    logged.
    """
    for wrapper_key in ("content", "item"):
        wrapper = entry.get(wrapper_key)
        if not isinstance(wrapper, dict):
            continue
        item_content = wrapper.get("itemContent")
        if isinstance(item_content, dict):
            value = item_content.get("value")
            if isinstance(value, str) and value:
                return value
        value = wrapper.get("value")
        if isinstance(value, str) and value:
            return value
        operation = wrapper.get("operation")
        if isinstance(operation, dict):
            cursor = operation.get("cursor")
            if isinstance(cursor, dict):
                value = cursor.get("value")
                if isinstance(value, str) and value:
                    return value
    return None


_CURSOR_ENTRY = re.compile(r"cursor-(bottom|top|showmore)")


def _is_cursor_entry(entry_id: str) -> bool:
    """True for any continuation cursor entry, at any depth."""
    if not entry_id:
        return False
    return bool(_CURSOR_ENTRY.search(entry_id))


def _tweet_ids(node: Any, found: list[tuple[str, str, int, str | None]]) -> None:
    """Collect ``(post_id, conversation_id, reply_count, reply_to)`` tuples."""
    if isinstance(node, dict):
        result = node.get("result")
        if isinstance(result, dict) and result.get("__typename") == "Tweet":
            legacy = result.get("legacy")
            legacy = legacy if isinstance(legacy, dict) else {}
            tweet_id = str(legacy.get("id_str") or result.get("rest_id") or "")
            if tweet_id:
                conversation = str(legacy.get("conversation_id_str") or "")
                reply_count = int(legacy.get("reply_count") or 0)
                reply_to = legacy.get("in_reply_to_status_id_str")
                entry = (
                    tweet_id,
                    conversation,
                    reply_count,
                    str(reply_to) if reply_to else None,
                )
                if entry not in found:
                    found.append(entry)
        for value in node.values():
            _tweet_ids(value, found)
    elif isinstance(node, list):
        for value in node:
            _tweet_ids(value, found)


_THREAD_MODULE_PREFIXES = (
    "homeConversation-",
    "profile-conversation-",
    "conversationthread-",
)


def _is_thread_module(entry_id: str) -> bool:
    """True for a thread module entry, false for its sub-entries.

    A module entry id is a known prefix followed by digits only. Its
    sub-entries share the prefix but carry a ``-tweet-`` or
    ``-cursor-`` suffix.
    """
    if not entry_id.startswith(_THREAD_MODULE_PREFIXES):
        return False
    suffix = entry_id.split("-", 1)[1] if "-" in entry_id else ""
    return suffix.isdigit()


def parse_page(body: dict[str, Any]) -> _Page:
    """Reduce a TweetDetail response to its post ids and its cursors.

    Every cursor in the tree is collected, including the ones nested
    inside thread modules and ``ShowMoreThreadsPrompt`` entries. The
    top-level ``cursor-bottom-*`` is reported separately because that is
    the only one gallery-dl follows.
    """
    post_ids: list[tuple[str, str]] = []
    cursors: list[str] = []
    top_level: str | None = None

    def add_cursor(entry: dict[str, Any], top_level_entry: bool) -> None:
        nonlocal top_level
        entry_id = entry.get("entryId")
        if not isinstance(entry_id, str) or not _is_cursor_entry(entry_id):
            return
        value = _cursor_value(entry)
        if not value:
            return
        if value not in cursors:
            cursors.append(value)
        if top_level_entry and entry_id.startswith("cursor-bottom-"):
            if top_level is None:
                top_level = value

    def walk_entries(entries: Any, depth: int) -> None:
        if not isinstance(entries, list):
            return
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            entry_id = entry.get("entryId")
            entry_id = entry_id if isinstance(entry_id, str) else ""
            if _is_cursor_entry(entry_id):
                add_cursor(entry, depth == 0)
                continue
            if _is_thread_module(entry_id):
                content = entry.get("content")
                items = content.get("items") if isinstance(content, dict) else None
                walk_entries(items, depth + 1)
                _find_cursors(content, add_cursor)
                continue
            if "showmore" in entry_id.lower():
                content = entry.get("content")
                items = content.get("items") if isinstance(content, dict) else None
                _find_cursors(items, add_cursor)
                walk_entries(items, depth + 1)
            _find_cursors(entry, add_cursor)
            _tweet_ids(entry, post_ids)

    def walk_instructions(instructions: Any) -> None:
        if not isinstance(instructions, list):
            return
        for instruction in instructions:
            if not isinstance(instruction, dict):
                continue
            kind = instruction.get("type")
            if kind == "TimelineAddEntries":
                walk_entries(instruction.get("entries"), 0)
            elif kind == "TimelineAddToModule":
                walk_entries(instruction.get("moduleItems"), 0)
            elif kind in ("TimelineReplaceEntry", "TimelinePinEntry"):
                entry = instruction.get("entry")
                if isinstance(entry, dict):
                    add_cursor(entry, True)
                    _find_cursors(entry, add_cursor)
                    _tweet_ids(entry, post_ids)

    data = body.get("data")
    data = data if isinstance(data, dict) else {}
    conversation = data.get("threaded_conversation_with_injections_v2")
    conversation = conversation if isinstance(conversation, dict) else {}
    walk_instructions(conversation.get("instructions"))
    return _Page(
        post_ids=tuple(entry[0] for entry in post_ids),
        conversation_ids=tuple(entry[1] for entry in post_ids),
        reply_counts=tuple(entry[2] for entry in post_ids),
        reply_to_ids=tuple(entry[3] for entry in post_ids),
        cursors=tuple(cursors),
        top_level_cursor=top_level,
    )


def _find_cursors(node: Any, add_cursor: Any) -> None:
    """Find every cursor anywhere below ``node``.

    This is the part gallery-dl skips: cursors inside a thread module
    or a ``ShowMoreThreadsPrompt`` are never followed.
    """
    if isinstance(node, dict):
        entry_id = node.get("entryId")
        if isinstance(entry_id, str) and _is_cursor_entry(entry_id):
            add_cursor(node, False)
        for value in node.values():
            _find_cursors(value, add_cursor)
    elif isinstance(node, list):
        for value in node:
            _find_cursors(value, add_cursor)


def _request(
    extractor: Any,
    focal_id: str,
    cursor: str | None,
    variables: dict[str, Any],
    toggles: dict[str, Any],
) -> dict[str, Any]:
    """Issue one TweetDetail request through gallery-dl's request layer."""
    request_variables = dict(variables)
    request_variables["focalTweetId"] = focal_id
    if cursor:
        request_variables["cursor"] = cursor
    params = {
        "variables": json.dumps(request_variables, separators=(",", ":"), ensure_ascii=False),
        "features": json.dumps(
            extractor.api.features_pagination, separators=(",", ":"), ensure_ascii=False
        ),
        "fieldToggles": json.dumps(toggles, separators=(",", ":"), ensure_ascii=False),
    }
    body = extractor.api._call(tweet_detail_endpoint(), params, method="GET")
    if not isinstance(body, dict):
        raise WalkerError("TweetDetail returned a non-object body")
    return body


def _walk_focal(
    extractor: Any,
    focal_id: str,
    request_cap: int,
    variables: dict[str, Any],
    toggles: dict[str, Any],
    capture_dir: Path | None = None,
) -> tuple[set[str], dict[str, int], dict[str, str | None], int, str]:
    """Walk every cursor under one focal.

    Returns ``(post_ids, reply_counts, reply_to_ids, calls, reason)``.
    """
    post_ids: set[str] = set()
    reply_counts: dict[str, int] = {}
    reply_to: dict[str, str | None] = {}
    seen_cursors: set[str] = set()
    pending: deque[str | None] = deque([None])
    calls = 0
    conversation: str | None = None
    while pending and calls < request_cap:
        cursor = pending.popleft()
        calls += 1
        body = _request(extractor, focal_id, cursor, variables, toggles)
        if capture_dir is not None:
            _capture_page(capture_dir, calls, body)
        page = parse_page(body)
        if conversation is None:
            conversation = _focal_conversation(page, focal_id)
        for index, tweet_id in enumerate(page.post_ids):
            if page.conversation_ids[index] != conversation:
                continue
            post_ids.add(tweet_id)
            reply_counts[tweet_id] = page.reply_counts[index]
            reply_to[tweet_id] = page.reply_to_ids[index]
        for value in page.cursors:
            if value in seen_cursors:
                continue
            seen_cursors.add(value)
            pending.append(value)
    reason = "request-cap" if pending else "exhausted"
    return post_ids, reply_counts, reply_to, calls, reason


def _capture_page(capture_dir: Path, ordinal: int, body: dict[str, Any]) -> None:
    """Write one response page so a run can be inspected afterwards.

    The page holds tweet text and cursor values. It stays in scratch and
    is never written to the vault.
    """
    capture_dir.mkdir(parents=True, exist_ok=True)
    target = capture_dir / f"page-{ordinal:03d}.json"
    target.write_text(
        json.dumps(body, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _focal_conversation(page: _Page, focal_id: str) -> str:
    """Return the conversation id the focal's replies share.

    The focal's own conversation id is the one its replies carry. When
    the focal is not in the first page, the page's modal conversation
    id is used.
    """
    pairs = list(zip(page.post_ids, page.conversation_ids))
    for tweet_id, conversation in pairs:
        if tweet_id == focal_id and conversation:
            return conversation
    counts: dict[str, int] = {}
    for _tweet_id, conversation in pairs:
        if conversation:
            counts[conversation] = counts.get(conversation, 0) + 1
    if not counts:
        return ""
    return max(counts.items(), key=lambda item: item[1])[0]


def _under_captured(
    reply_counts: dict[str, int],
    reply_to: dict[str, str | None],
) -> list[str]:
    """Return posts whose reply count exceeds the children actually seen.

    A post that reports more replies than the walk found is a post with
    a subtree the walk has not reached yet. Walking it is how the walk
    expands without the operator naming every focal by hand.
    """
    children: dict[str, int] = {}
    for parent in reply_to.values():
        if parent:
            children[parent] = children.get(parent, 0) + 1
    return [
        post_id
        for post_id, count in reply_counts.items()
        if count > children.get(post_id, 0)
    ]

def discover(
    focal_ids: tuple[str, ...] | list[str],
    request_cap: int = 20,
    extractor: Any | None = None,
    max_focals: int = 40,
    capture_dir: Path | None = None,
) -> WalkerResult:
    """Walk each focal's conversation and return every post id found.

    The walk expands its own focal set: a post that reports more
    replies than were found has a subtree not yet reached, so it is
    walked too. That is what lets one focal find the whole thread.

    ``request_cap`` bounds the requests issued per focal.
    ``max_focals`` bounds how many focals the expansion may add, so a
    conversation that keeps reporting unreached children cannot run
    away. Requests are sequential. No cursor value is logged or
    persisted.
    """
    if not focal_ids:
        return WalkerResult(post_ids=(), calls=0, per_focal={}, stopped_reason="no-focals")
    variables, toggles = request_shape()
    if extractor is None:
        extractor = build_extractor()
    all_posts: set[str] = set()
    per_focal: dict[str, tuple[str, ...]] = {}
    calls = 0
    stopped = "exhausted"
    walked: set[str] = set()
    queue = list(dict.fromkeys(focal_ids))
    while queue and len(walked) < max_focals:
        focal = queue.pop(0)
        if focal in walked:
            continue
        walked.add(focal)
        posts, reply_counts, reply_to, focal_calls, reason = _walk_focal(
            extractor, focal, request_cap, variables, toggles, capture_dir
        )
        per_focal[focal] = tuple(sorted(posts))
        all_posts.update(posts)
        calls += focal_calls
        stopped = reason
        if len(walked) >= max_focals:
            stopped = "focal-cap"
            break
        for parent in _under_captured(reply_counts, reply_to):
            if parent not in walked:
                queue.append(parent)
    logger.info(
        "walker found %d posts across %d focals in %d requests",
        len(all_posts), len(walked), calls,
    )
    return WalkerResult(
        post_ids=tuple(sorted(all_posts)),
        calls=calls,
        per_focal=per_focal,
        stopped_reason=stopped,
    )
