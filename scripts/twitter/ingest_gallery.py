"""Turn gallery-dl --dump-json into thread_data.json. No vault writes."""
from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from dataclasses import asdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from twitter.models import PostData, PostMetrics, ThreadData


def _parse_wire_post(meta: Any) -> PostData | None:
    """Boundary: parse an MCP wire entry into a typed PostData.

    A wire entry may be a dict (tweet meta) or a nested list/tuple
    containing the meta dict. Recursively walks to find the first
    tweet-meta dict (one with ``tweet_id`` or both ``content`` and
    ``author``) and converts it to PostData. Returns ``None`` if no
    tweet-meta dict is found in the entry — that entry is then
    dropped by the caller, matching the prior ``_find_tweet_meta``
    skip-on-None behavior.
    """
    result: PostData | None = None

    def build_post(meta_dict: Mapping[str, object]) -> PostData:
        author = meta_dict.get("author") or {}
        if isinstance(author, dict):
            author_name = str(author.get("nick") or author.get("name") or "")
            handle = str(author.get("name") or author.get("nick") or "")
        else:
            author_name = str(author)
            handle = str(author)
        view = meta_dict.get("view_count")
        reply = meta_dict.get("reply_id")
        quote = meta_dict.get("quote_id")
        return PostData(
            post_id=str(meta_dict.get("tweet_id") or meta_dict.get("id") or ""),
            author=author_name,
            handle=handle,
            text=str(meta_dict.get("content") or ""),
            timestamp=str(meta_dict.get("date") or ""),
            media_urls=(),
            reply_to_id=str(reply) if reply else None,
            quote_of_id=str(quote) if quote else None,
            metrics=PostMetrics(
                reply_count=int(meta_dict.get("reply_count") or 0),
                repost_count=int(meta_dict.get("retweet_count") or 0),
                like_count=int(meta_dict.get("favorite_count") or 0),
                view_count=int(view) if view is not None else None,
            ),
        )

    def walk(node: object) -> None:
        nonlocal result
        if result is not None:
            return
        if isinstance(node, dict):
            if "tweet_id" in node or ("content" in node and "author" in node):
                result = build_post(node)
            return
        if isinstance(node, (list, tuple)):
            for item in node:
                if result is not None:
                    return
                walk(item)

    walk(meta)
    return result


def _media_urls_from_entry(entry: object) -> tuple[str, ...]:
    """Walk a wire entry to collect ``pbs.twimg.com`` / ``video.twimg.com`` URL strings.

    Mirrors the recursive descent of the boundary parser (without the
    dict-detection short-circuit) so a single walk collects both the
    tweet meta (in the boundary) and any media URLs in the same shape.
    """
    urls: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, (list, tuple)):
            for item in node:
                if isinstance(item, str) and (
                    "pbs.twimg.com" in item or "video.twimg.com" in item
                ):
                    urls.append(item)
                else:
                    walk(item)

    walk(entry)
    return tuple(urls)


def posts_from_gallery(data: object) -> list[PostData]:
    by: dict[str, PostData] = {}
    media: dict[str, list[str]] = {}
    order: list[str] = []
    entries = data if isinstance(data, list) else []
    for entry in entries:
        post = _parse_wire_post(entry)
        if post is None or not post.post_id:
            continue
        tid = post.post_id
        if tid not in by:
            by[tid] = post
            media[tid] = list(_media_urls_from_entry(entry))
            order.append(tid)
        else:
            for url in _media_urls_from_entry(entry):
                if url not in media[tid]:
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
