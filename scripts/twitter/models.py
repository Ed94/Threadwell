from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class PostMetrics:
    reply_count: int
    repost_count: int
    like_count: int
    view_count: int | None


@dataclass(frozen=True)
class PostData:
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
    root_post_id: str
    posts: tuple[PostData, ...]
    source_url: str


def _norm_handle(raw: str) -> str:
    h = (raw or "").strip()
    return h[1:] if h.startswith("@") else h


def _norm_id(raw: object) -> str | None:
    if raw is None:
        return None
    s = str(raw).strip()
    return s or None


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
