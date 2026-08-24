"""Render archive note markdown from thread JSON. Strings only; no file I/O."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from .media_refs import remote_markup
except ImportError:  # pragma: no cover - script-mode import
    if str(Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from media_refs import remote_markup

from .models import PostData, ThreadData
from .slug import date_prefix
from .tree import by_id


def render_media(url: str) -> str:
    return remote_markup(url)


def _yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _first_line(text: str) -> str:
    return (text or "").split("\n", 1)[0].rstrip("\r")


def _title_text(text: str) -> str:
    line = _first_line(text)
    idx = line.find(". ")
    if idx >= 0:
        return line[: idx + 1]
    return line


def _status_url(handle: str, post_id: str) -> str:
    return f"https://x.com/{handle}/status/{post_id}"


def _blockquote(text: str) -> str:
    lines = (text or "").split("\n")
    return "\n".join(">" if line == "" else f"> {line}" for line in lines)


def _frontmatter(
    *,
    title: str,
    source_url: str,
    author: str,
    handle: str,
    post_id: str,
    date: str,
    archived: str,
    spine_handle: str,
    in_reply_to: str,
    parent_post_id: str | None = None,
) -> str:
    lines = [
        "---",
        f"title: {_yaml_quote(title)}",
        "type: archive",
        "source: twitter",
        f"source_url: {_yaml_quote(source_url)}",
        f"author: {_yaml_quote(author)}",
        f"handle: {handle}",
        f"post_id: {_yaml_quote(post_id)}",
        f"date: {date}",
        f"archived: {archived}",
        "draft: true",
        "tags:",
        "  - archive",
        "  - twitter",
        f"  - {spine_handle}",
        f"description: {_yaml_quote(title)}",
        f"in_reply_to: {_yaml_quote(in_reply_to)}",
    ]
    if parent_post_id is not None:
        lines.append(f"parent_post_id: {_yaml_quote(parent_post_id)}")
    lines.append("---")
    return "\n".join(lines)


def _source_block(post: PostData) -> str:
    url = _status_url(post.handle, post.post_id)
    return (
        "## Source\n"
        "\n"
        f"- URL: {url}\n"
        f"- Author: {post.author} (@{post.handle})\n"
        f"- Posted: {post.timestamp}"
    )


def _post_block(
    n: int,
    post: PostData,
    media_by_post: dict[str, tuple[str, ...]] | None,
    branch_links: list[str] | None = None,
) -> str:
    parts = [f"**{n}/**", "", post.text]
    media = (media_by_post or {}).get(post.post_id) or ()
    if media:
        parts.append("")
        parts.extend(render_media(url) for url in media)
    if branch_links:
        parts.append("")
        parts.append("Branches: " + ", ".join(f"[[{name}]]" for name in branch_links))
    parts.append("")
    return "\n".join(parts)


def _foreign_parent(
    first: PostData,
    ids: dict[str, PostData],
) -> tuple[str, PostData | None]:
    parent_id = first.reply_to_id or ""
    if not parent_id:
        return "", None
    parent = ids.get(parent_id)
    if parent is None:
        return parent_id, None
    if parent.handle != first.handle:
        return parent_id, parent
    return "", None


def render_spine(
    thread: ThreadData,
    spine: list[str],
    branch_root_ids: list[str],
    branch_names: dict[str, str],
    archived: str,
    media_by_post: dict[str, tuple[str, ...]] | None = None,
) -> str:
    """branch_names maps branch-root post_id -> wikilink target (filename without .md)."""
    ids = by_id(thread)
    first = ids[spine[0]]
    spine_handle = first.handle
    in_reply_to, parent = _foreign_parent(first, ids)
    title = _title_text(first.text)
    source_url = _status_url(first.handle, first.post_id)
    chunks = [
        _frontmatter(
            title=title,
            source_url=source_url,
            author=first.author,
            handle=first.handle,
            post_id=first.post_id,
            date=date_prefix(first.timestamp),
            archived=archived,
            spine_handle=spine_handle,
            in_reply_to=in_reply_to,
        ),
        "",
        _source_block(first),
        "",
    ]
    if parent is not None:
        chunks.append(_blockquote(parent.text))
        chunks.append("")
    chunks.append("## Thread")
    chunks.append("")

    branches_under: dict[str, list[str]] = {}
    for rid in branch_root_ids:
        parent_id = ids[rid].reply_to_id
        if parent_id:
            branches_under.setdefault(parent_id, []).append(branch_names[rid])

    for n, pid in enumerate(spine, 1):
        post = ids[pid]
        chunks.append(_post_block(n, post, media_by_post, branches_under.get(pid)))

    return "\n".join(chunks).rstrip() + "\n"


def render_per_author_spine(
    handle: str,
    author_posts: list[PostData],
    ids: dict[str, PostData],
    archived: str,
    conversation_links: list[str],
    media_by_post: dict[str, tuple[str, ...]] | None = None,
) -> str:
    """Render a per-author archive note.

    `author_posts` is the author's posts in chronological order.
    Cross-author parents appear as blockquotes immediately before the
    post that replies to them. `conversation_links` is a list of
    vault-root wikilink targets for the other authors' directories
    in the same conversation; if non-empty, a `## Conversation`
    section is appended.

    The first post in `author_posts` is treated as the spine root for
    the frontmatter. Its title is derived from its first line.
    """
    if not author_posts:
        raise ValueError(
            "render_per_author_spine requires a non-empty author_posts list"
        )
    first = author_posts[0]
    title = _title_text(first.text)
    source_url = _status_url(first.handle, first.post_id)
    chunks: list[str] = [
        _frontmatter(
            title=title,
            source_url=source_url,
            author=first.author,
            handle=first.handle,
            post_id=first.post_id,
            date=date_prefix(first.timestamp),
            archived=archived,
            spine_handle=first.handle,
            in_reply_to="",
        ),
        "",
        _source_block(first),
        "",
        "## Thread",
        "",
    ]
    for n, post in enumerate(author_posts, 1):
        parent_id = post.reply_to_id
        if parent_id:
            parent = ids.get(parent_id)
            if parent is not None and parent.handle != handle:
                chunks.append(_blockquote(parent.text))
                chunks.append("")
        chunks.append(_post_block(n, post, media_by_post))
    if conversation_links:
        chunks.append("## Conversation")
        chunks.append("")
        for link in conversation_links:
            chunks.append(f"- [[{link}]]")
        chunks.append("")
    return "\n".join(chunks).rstrip() + "\n"


def render_branch(
    thread: ThreadData,
    branch_root_id: str,
    descendant_ids: list[str],
    spine_handle: str,
    archived: str,
    media_by_post: dict[str, tuple[str, ...]] | None = None,
    spine_wiki: str = "index",
) -> str:
    """descendant_ids are posts after the root, in display order (tree.descendants)."""
    ids = by_id(thread)
    root = ids[branch_root_id]
    title = _title_text(root.text)
    source_url = _status_url(root.handle, root.post_id)
    chunks = [
        _frontmatter(
            title=title,
            source_url=source_url,
            author=root.author,
            handle=root.handle,
            post_id=root.post_id,
            date=date_prefix(root.timestamp),
            archived=archived,
            spine_handle=spine_handle,
            in_reply_to="",
            parent_post_id=root.reply_to_id or "",
        ),
        "",
        _source_block(root),
        "",
        "## Branch",
        "",
    ]
    posts = [root] + [ids[i] for i in descendant_ids]
    for n, post in enumerate(posts, 1):
        chunks.append(_post_block(n, post, media_by_post))
    chunks.append("## Related")
    chunks.append("")
    chunks.append(f"- Spine: [[{spine_wiki}]]")
    chunks.append("")
    return "\n".join(chunks).rstrip() + "\n"
