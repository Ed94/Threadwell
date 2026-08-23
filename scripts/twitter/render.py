"""Render archive note markdown from thread JSON. Strings only; no file I/O."""

from __future__ import annotations

from .models import PostData, ThreadData
from .slug import date_prefix
from .tree import by_id

_PROVENANCE = (
    "> [!info] Provenance\n"
    "> Primary source record. Do not editorialize here. "
    "Interpretation goes in a `notes/` page."
)


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
        "status: draft",
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
        parts.append("Media (not lifted): " + " ".join(f"`{fn}`" for fn in media))
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
        _PROVENANCE,
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


def render_branch(
    thread: ThreadData,
    branch_root_id: str,
    descendant_ids: list[str],
    spine_handle: str,
    archived: str,
    media_by_post: dict[str, tuple[str, ...]] | None = None,
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
        _PROVENANCE,
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
    chunks.append("- Spine: [[index]]")
    chunks.append("")
    return "\n".join(chunks).rstrip() + "\n"
