from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self
import json


@dataclass(frozen=True)
class PostMetrics:
    """Post engagement counters (replies / reposts / likes / views)."""
    reply_count: int
    repost_count: int
    like_count: int
    view_count: int | None


@dataclass(frozen=True)
class PostData:
    """A single tweet post extracted from a Twitter archive."""
    post_id: str
    author: str
    handle: str
    text: str
    timestamp: str
    media_urls: tuple[str, ...]
    reply_to_id: str | None
    quote_of_id: str | None
    metrics: PostMetrics


@dataclass(frozen=True)
class ThreadData:
    """A complete Twitter thread (root post + replies)."""
    root_post_id: str
    posts: tuple[PostData, ...]
    source_url: str


@dataclass(frozen=True)
class MediaLocation:
    """A single media location record (local / remote / fallback / mirror / derived)."""
    kind: str
    local_path: Path | None = None
    url: str | None = None
    bytes: int | None = None
    sha256: str | None = None
    checked_at: str | None = None
    checked_status: int | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        if "kind" not in raw:
            raise KeyError("MediaLocation.from_dict: 'kind' is required")
        return cls(
            kind=_required_str(raw["kind"], "kind"),
            local_path=_optional_path(raw.get("local_path"), "local_path"),
            url=_optional_str(raw.get("url"), "url"),
            bytes=_optional_int(raw.get("bytes"), "bytes"),
            sha256=_optional_str(raw.get("sha256"), "sha256"),
            checked_at=_optional_str(raw.get("checked_at"), "checked_at"),
            checked_status=_optional_int(raw.get("checked_status"), "checked_status"),
        )


@dataclass(frozen=True)
class MediaItem:
    """A single media entry attached to a post (image / crt / crt_outline / denoise / ocr)."""
    post_id: str
    media_id: str
    kind: str
    locations: tuple[MediaLocation, ...]
    embed: bool | None = None
    caption: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        for required in ("post_id", "media_id", "kind", "locations"):
            if required not in raw:
                raise KeyError(f"MediaItem.from_dict: '{required}' is required")
        locations_raw = raw["locations"]
        if not isinstance(locations_raw, list):
            raise TypeError(
                f"MediaItem.from_dict: 'locations' must be list, got {type(locations_raw).__name__}"
            )
        return cls(
            post_id=_required_str(raw["post_id"], "post_id"),
            media_id=_required_str(raw["media_id"], "media_id"),
            kind=_required_str(raw["kind"], "kind"),
            locations=tuple(MediaLocation.from_dict(loc) for loc in locations_raw),
            embed=_optional_bool(raw.get("embed"), "embed"),
            caption=_optional_str(raw.get("caption"), "caption"),
        )


@dataclass(frozen=True)
class MediaManifest:
    """A whole media.json document (one thread)."""
    root_post_id: str
    items: tuple[MediaItem, ...]
    captured_at: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        for required in ("root_post_id", "items"):
            if required not in raw:
                raise KeyError(f"MediaManifest.from_dict: '{required}' is required")
        items_raw = raw["items"]
        if not isinstance(items_raw, list):
            raise TypeError(
                f"MediaManifest.from_dict: 'items' must be list, got {type(items_raw).__name__}"
            )
        return cls(
            root_post_id=_required_str(raw["root_post_id"], "root_post_id"),
            items=tuple(MediaItem.from_dict(item) for item in items_raw),
            captured_at=_optional_str(raw.get("captured_at"), "captured_at"),
        )


@dataclass(frozen=True)
class LegacyThreadData:
    """Pre-v2 thread_data.json shape paired with media items during migration."""
    root_post_id: str
    posts: tuple[PostData, ...]
    source_url: str
    media_items: tuple[MediaItem, ...] = ()

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        for required in ("root_post_id", "posts", "source_url"):
            if required not in raw:
                raise KeyError(f"LegacyThreadData.from_dict: '{required}' is required")
        posts_raw = raw["posts"]
        if not isinstance(posts_raw, list):
            raise TypeError(
                f"LegacyThreadData.from_dict: 'posts' must be list, got {type(posts_raw).__name__}"
            )
        media_items_raw = raw.get("media_items")
        media_items: tuple[MediaItem, ...] = ()
        if media_items_raw is not None:
            if not isinstance(media_items_raw, list):
                raise TypeError(
                    f"LegacyThreadData.from_dict: 'media_items' must be list, got {type(media_items_raw).__name__}"
                )
            media_items = tuple(MediaItem.from_dict(item) for item in media_items_raw)
        return cls(
            root_post_id=_required_str(raw["root_post_id"], "root_post_id"),
            posts=tuple(_parse_post(p) for p in posts_raw),
            source_url=_required_str(raw["source_url"], "source_url"),
            media_items=media_items,
        )


@dataclass(frozen=True)
class LegacyManifest:
    """Pre-v2 corpus inventory shape used during media migration."""
    threads: tuple[LegacyThreadData, ...]
    schema_version: int | None = None
    generated_at: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        if "threads" not in raw:
            raise KeyError("LegacyManifest.from_dict: 'threads' is required")
        threads_raw = raw["threads"]
        if not isinstance(threads_raw, list):
            raise TypeError(
                f"LegacyManifest.from_dict: 'threads' must be list, got {type(threads_raw).__name__}"
            )
        return cls(
            threads=tuple(LegacyThreadData.from_dict(t) for t in threads_raw),
            schema_version=_optional_int(raw.get("schema_version"), "schema_version"),
            generated_at=_optional_str(raw.get("generated_at"), "generated_at"),
        )


def _norm_handle(raw: str) -> str:
    h = (raw or "").strip()
    return h[1:] if h.startswith("@") else h


def _norm_id(raw: object) -> str | None:
    if raw is None:
        return None
    s = str(raw).strip()
    return s or None


def _required_str(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name}: expected str, got {type(value).__name__}")
    return value


def _optional_str(value: object, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{field}: expected str, got {type(value).__name__}")
    return value


def _optional_int(value: object, field: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field}: expected int, got {type(value).__name__}")
    return value


def _optional_bool(value: object, field: str) -> bool | None:
    if value is None:
        return None
    if not isinstance(value, bool):
        raise TypeError(f"{field}: expected bool, got {type(value).__name__}")
    return value


def _optional_path(value: object, field: str) -> Path | None:
    if value is None:
        return None
    if isinstance(value, Path):
        return value
    if isinstance(value, str):
        return Path(value)
    raise TypeError(f"{field}: expected str or Path, got {type(value).__name__}")


def _parse_post(raw: object) -> PostData:
    if not isinstance(raw, dict):
        raise TypeError(f"post entry: expected dict, got {type(raw).__name__}")
    m = raw.get("metrics") or {}
    if not isinstance(m, dict):
        raise TypeError(f"post entry metrics: expected dict, got {type(m).__name__}")
    view = m.get("view_count")
    media_urls_raw = raw.get("media_urls") or []
    if not isinstance(media_urls_raw, list):
        raise TypeError(
            f"post entry media_urls: expected list, got {type(media_urls_raw).__name__}"
        )
    return PostData(
        post_id=str(raw.get("post_id") or ""),
        author=str(raw.get("author") or ""),
        handle=_norm_handle(str(raw.get("handle") or "")),
        text=str(raw.get("text") or ""),
        timestamp=str(raw.get("timestamp") or ""),
        media_urls=tuple(str(u) for u in media_urls_raw),
        reply_to_id=_norm_id(raw.get("reply_to_id")),
        quote_of_id=_norm_id(raw.get("quote_of_id")),
        metrics=PostMetrics(
            reply_count=int(m.get("reply_count") or 0),
            repost_count=int(m.get("repost_count") or 0),
            like_count=int(m.get("like_count") or 0),
            view_count=int(view) if view is not None else None,
        ),
    )


def load_thread(path: Path) -> ThreadData:
    data = json.loads(path.read_text(encoding="utf-8"))
    posts: list[PostData] = []
    for pd in data.get("posts", []):
        m = pd.get("metrics") or {}
        view = m.get("view_count")
        posts.append(PostData(
            post_id=str(pd.get("post_id") or ""),
            author=str(pd.get("author") or ""),
            handle=_norm_handle(str(pd.get("handle") or "")),
            text=str(pd.get("text") or ""),
            timestamp=str(pd.get("timestamp") or ""),
            media_urls=tuple(pd.get("media_urls") or []),
            reply_to_id=_norm_id(pd.get("reply_to_id")),
            quote_of_id=_norm_id(pd.get("quote_of_id")),
            metrics=PostMetrics(
                reply_count=int(m.get("reply_count") or 0),
                repost_count=int(m.get("repost_count") or 0),
                like_count=int(m.get("like_count") or 0),
                view_count=int(view) if view is not None else None,
            ),
        ))
    return ThreadData(
        root_post_id=str(data.get("root_post_id") or ""),
        posts=tuple(posts),
        source_url=str(data.get("source_url") or ""),
    )
