"""Turn gallery-dl --dump-json into thread_data.json. No vault writes."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from twitter.models import PostData, PostMetrics, ThreadData


def _find_tweet_meta(entry: Any) -> dict[str, Any] | None:
    if isinstance(entry, dict):
        if "tweet_id" in entry or ("content" in entry and "author" in entry):
            return entry
        return None
    if isinstance(entry, (list, tuple)):
        for item in entry:
            meta = _find_tweet_meta(item)
            if meta is not None:
                return meta
    return None


def _media_url_from_entry(entry: Any) -> str:
    if isinstance(entry, (list, tuple)):
        for item in entry:
            if isinstance(item, str) and (
                "pbs.twimg.com" in item or "video.twimg.com" in item
            ):
                return item
    return ""


def _post_from_meta(meta: dict[str, Any]) -> PostData:
    author = meta.get("author") or {}
    if isinstance(author, dict):
        author_name = str(author.get("nick") or author.get("name") or "")
        handle = str(author.get("name") or author.get("nick") or "")
    else:
        author_name = str(author)
        handle = str(author)
    view = meta.get("view_count")
    reply = meta.get("reply_id")
    quote = meta.get("quote_id")
    return PostData(
        post_id=str(meta.get("tweet_id") or meta.get("id") or ""),
        author=author_name,
        handle=handle,
        text=str(meta.get("content") or ""),
        timestamp=str(meta.get("date") or ""),
        media_urls=(),
        reply_to_id=str(reply) if reply else None,
        quote_of_id=str(quote) if quote else None,
        metrics=PostMetrics(
            reply_count=int(meta.get("reply_count") or 0),
            repost_count=int(meta.get("retweet_count") or 0),
            like_count=int(meta.get("favorite_count") or 0),
            view_count=int(view) if view is not None else None,
        ),
    )


def posts_from_gallery(data: Any) -> list[PostData]:
    by: dict[str, PostData] = {}
    media: dict[str, list[str]] = {}
    order: list[str] = []
    entries = data if isinstance(data, list) else []
    for entry in entries:
        meta = _find_tweet_meta(entry)
        if meta is None:
            continue
        tid = str(meta.get("tweet_id") or meta.get("id") or "")
        if not tid:
            continue
        if tid not in by:
            by[tid] = _post_from_meta(meta)
            media[tid] = []
            order.append(tid)
        url = _media_url_from_entry(entry)
        if url:
            media[tid].append(url)
    posts: list[PostData] = []
    for tid in order:
        base = by[tid]
        posts.append(PostData(
            post_id=base.post_id,
            author=base.author,
            handle=base.handle,
            text=base.text,
            timestamp=base.timestamp,
            media_urls=tuple(media[tid]),
            reply_to_id=base.reply_to_id,
            quote_of_id=base.quote_of_id,
            metrics=base.metrics,
        ))
    return posts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--root", required=True)
    args = parser.parse_args(argv)
    data = json.loads(args.json.read_text(encoding="utf-8"))
    posts = posts_from_gallery(data)
    thread = ThreadData(
        root_post_id=args.root,
        posts=tuple(posts),
        source_url=args.source_url,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(asdict(thread), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"posts={len(posts)} -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
