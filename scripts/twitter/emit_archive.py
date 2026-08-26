"""Emit Threadwell archive notes from a thread_data.json dump. No fetch, no lift."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import sys
from dataclasses import asdict, dataclass, replace
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from twitter.frozen import frozen_match, load_frozen_ids
    from twitter.media_manifest import (
        _from_wire_dict,
        _item_to_wire,
        atomic_write_json,
        find_location,
        item_key,
        merge_manifest_items,
        new_original_item,
        selected_url,
    )
    from twitter.media_refs import remote_markup
    from twitter.models import MediaItem, ThreadData, load_thread
    from twitter.paths import FROZEN, SCRATCH
    from twitter.render import (
        format_post_text,
        render_branch,
        render_spine,
        split_leading_mentions,
        title_text,
    )
    from twitter.slug import branch_file_name, date_prefix, thread_dir_name
    from twitter.tree import (
        by_id,
        branch_roots,
        children_map,
        descendants,
        spine_from_tip,
        spine_ids,
        spine_quote_ids,
    )
except ImportError:  # pragma: no cover - script-mode import
    from frozen import frozen_match, load_frozen_ids
    from media_manifest import (
        _from_wire_dict,
        _item_to_wire,
        atomic_write_json,
        find_location,
        item_key,
        merge_manifest_items,
        new_original_item,
        selected_url,
    )
    from media_refs import remote_markup
    from models import MediaItem, ThreadData, load_thread
    from paths import FROZEN, SCRATCH
    from render import (
        format_post_text,
        render_branch,
        render_spine,
        split_leading_mentions,
        title_text,
    )
    from slug import branch_file_name, date_prefix, thread_dir_name
    from tree import (
        by_id,
        branch_roots,
        children_map,
        descendants,
        spine_from_tip,
        spine_ids,
        spine_quote_ids,
    )


def _frontmatter_lines(text: str) -> tuple[list[str], str]:
    """Return (frontmatter_lines, body_after_closer) for an archive note."""
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---", 4)
    if end < 0:
        return [], text
    return text[4:end].splitlines(), text[end + 4 :]


def _tag_values(lines: list[str]) -> list[str]:
    """Extract tag strings from the ``tags:`` block of a YAML frontmatter lines list."""
    tags: list[str] = []
    in_tags = False
    for line in lines:
        if line == "tags:":
            in_tags = True
            continue
        if in_tags and line.startswith("  - "):
            tags.append(line[4:])
            continue
        if in_tags and line and not line.startswith(" "):
            break
    return tags


def preserve_review_state(
    old: str,
    fresh: str,
    *,
    mechanical_tags: set[str],
) -> str:
    old_lines, _old_body = _frontmatter_lines(old)
    fresh_lines, fresh_body = _frontmatter_lines(fresh)
    if not old_lines or not fresh_lines:
        return fresh
    old_draft = next(
        (line for line in old_lines if line.startswith("draft: ")),
        "draft: true",
    )
    reviewed = [tag for tag in _tag_values(old_lines) if tag not in mechanical_tags]
    output: list[str] = []
    in_tags = False
    inserted_reviewed = False
    for line in fresh_lines:
        if line.startswith("draft: "):
            output.append(old_draft)
            continue
        if line == "tags:":
            in_tags = True
            output.append(line)
            continue
        if in_tags and line.startswith("  - "):
            output.append(line)
            continue
        if in_tags and not inserted_reviewed:
            output.extend(f"  - {tag}" for tag in reviewed if f"  - {tag}" not in output)
            inserted_reviewed = True
            in_tags = False
        output.append(line)
    if in_tags and not inserted_reviewed:
        output.extend(f"  - {tag}" for tag in reviewed if f"  - {tag}" not in output)
    return "---\n" + "\n".join(output) + "\n---" + fresh_body


def missing_local_media(items: list[MediaItem]) -> list[str]:
    missing: list[str] = []
    for item in items:
        local = find_location(item, "local")
        if local is not None and local.integrity == "missing":
            post_id, media_id, role = item_key(item)
            missing.append(f"{post_id}/{media_id}/{role}")
    return missing

_POST_ID_LINE: re.Pattern[str] = re.compile(r'^post_id:\s*"?([^"\s]+)"?\s*$')
_WIKILINK_ITEM: re.Pattern[str] = re.compile(r"^- \[\[([^\]|]+)\]\]\s*$")


@dataclass(frozen=True)
class EmitResult:
    """Outcome of one emit pass: which post+handle were written and how many branches."""
    post_id: str
    handle: str
    dir_name: str
    branch_count: int
    missing_media_count: int


def _url_media_id(url: str, index: int) -> str:
    """Derive a stable media id from the URL's last path segment, falling back to ``m<index>``."""
    segment = Path(unquote(urlparse(url).path)).name
    return segment if segment else f"m{index}"


def _url_ext(url: str) -> str | None:
    """Extract a lowercase file extension from a URL's ``?format=`` query or path suffix."""
    parsed = urlparse(url)
    fmt = parse_qs(parsed.query).get("format", [None])[0]
    if fmt:
        return fmt.lstrip(".").lower()
    suffix = Path(unquote(parsed.path)).suffix
    if suffix:
        return suffix.lstrip(".").lower()
    return None


def _media_files(media_dir: Path) -> list[Path]:
    if not media_dir.is_dir():
        return []
    return sorted(p for p in media_dir.iterdir() if p.is_file())


def _take_preferred(unused: list[Path], post_id: str, index: int) -> Path | None:
    """Pop the unused file whose stem equals ``<post_id>_<index>`` if any."""
    want = f"{post_id}_{index}"
    for path in unused:
        if path.stem == want:
            return path
    return None


def _take_fallback(unused: list[Path], post_id: str) -> Path | None:
    """Pop the first unused file whose name starts with ``<post_id>_`` if any."""
    prefix = f"{post_id}_"
    for path in unused:
        if path.name.startswith(prefix):
            return path
    return None


def collect_media(
    thread: ThreadData,
    input_dir: Path,
    dest_dir: Path,
    *,
    now: str,
) -> list[MediaItem]:
    """Copy each post's media files from ``input_dir/media`` into ``dest_dir`` and build canonical MediaItems."""
    unused = _media_files(input_dir / "media")
    items: list[MediaItem] = []
    for post in thread.posts:
        for index, url in enumerate(post.media_urls, start=1):
            media_id = _url_media_id(url, index)
            src = _take_preferred(unused, post.post_id, index)
            if src is None:
                src = _take_fallback(unused, post.post_id)
            if src is not None:
                unused.remove(src)
                ext = src.suffix.lstrip(".") or _url_ext(url) or "bin"
            else:
                ext = _url_ext(url) or "bin"
            filename = f"{post.post_id}_{media_id}_orig.{ext}"
            local_path = dest_dir / filename
            if src is not None:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, local_path)
            items.append(
                new_original_item(
                    post_id=post.post_id,
                    media_id=media_id,
                    handle=post.handle,
                    origin_url=url,
                    filename=filename,
                    local_path=local_path,
                    now=now,
                )
            )
    return items


def selected_media_by_post(
    items: list[MediaItem],
) -> dict[str, tuple[str, ...]]:
    """Group embedded items by post_id, returning the HTTPS URL of each visible location."""
    grouped: dict[str, list[str]] = {}
    for item in items:
        if not item.embed:
            continue
        url = selected_url(item)
        if url is not None:
            grouped.setdefault(item.post_id, []).append(url)
    return {post_id: tuple(urls) for post_id, urls in grouped.items()}


def merge_existing_media(
    dest_dir: Path,
    items: list[MediaItem],
) -> list[MediaItem]:
    """Merge existing derived/fallback rows with fresh canonical items."""
    old_path = dest_dir / "media.json"
    if not old_path.is_file():
        return items
    try:
        old = json.loads(old_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return items
    if old.get("schema_version") != 2:
        raise SystemExit(
            "legacy media.json requires: tw.py migrate-media --id <id> --apply"
        )
    existing = _from_wire_dict(old).items
    return list(merge_manifest_items(existing, tuple(items)))


def _legacy_emit_message(*args: object, **kwargs: object) -> None:
    raise SystemExit(
        "legacy media.json requires: tw.py migrate-media --id <id> --apply"
    )


def missing_parent_ids(thread: ThreadData) -> list[str]:
    ids = by_id(thread)
    found: list[str] = []
    seen: set[str] = set()
    for post in thread.posts:
        parent = post.reply_to_id
        if parent is None or parent in ids or parent in seen:
            continue
        seen.add(parent)
        found.append(parent)
    return found


def empty_text_ids(thread: ThreadData) -> list[str]:
    return [p.post_id for p in thread.posts if not (p.text or "").strip()]


def render_gaps(
    thread: ThreadData,
    spine: list[str],
    *,
    input_kind: str = "root",
    missing_quote_of: list[str] | None = None,
) -> str:
    """Render a gaps report. ``missing_quote_of`` is quoted ids with no archive."""
    ids = by_id(thread)
    suggested = spine[-1] if spine else ""
    quote_ids = list(missing_quote_of) if missing_quote_of is not None else []
    missing = [
        p.post_id
        for p in thread.posts
        if p.reply_to_id is not None and p.reply_to_id not in ids
    ]
    empty = empty_text_ids(thread)
    lines = [
        "# gaps",
        f"input: {input_kind}",
        f"suggested_tip: {suggested}",
    ]
    if quote_ids:
        lines.append("quote_of:")
        lines.extend(quote_ids)
    else:
        lines.append("quote_of: unset")
    lines.append("missing_reply_to:")
    lines.extend(missing)
    lines.append("empty_text:")
    lines.extend(empty)
    return "\n".join(lines) + "\n"


def archive_for_post(vault: Path, post_id: str) -> tuple[Path | None, Path | None]:
    """Return ``(asset_dir, note_dir)`` for the thread that contains ``post_id``."""
    assets_root = vault / "assets" / "threads"
    notes_root = vault / "archive" / "threads"
    if not assets_root.is_dir():
        return None, None
    for td in assets_root.rglob("thread_data.json"):
        try:
            data = json.loads(td.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        posts = data.get("posts") or []
        hit = str(data.get("root_post_id") or "") == post_id
        if not hit:
            hit = any(str(p.get("post_id") or "") == post_id for p in posts)
        if not hit:
            continue
        rel = td.parent.relative_to(assets_root)
        notes = notes_root / rel
        return td.parent, notes if notes.is_dir() else None
    return None, None


def quote_ref_for(vault: Path, quote_of_id: str) -> tuple[str, str | None]:
    """Return ``(status_url, wikilink_target_or_none)`` for a quoted id."""
    assets, notes = archive_for_post(vault, quote_of_id)
    if assets is None or not (assets / "thread_data.json").is_file():
        return f"https://x.com/i/status/{quote_of_id}", None
    quoted_thread = load_thread(assets / "thread_data.json")
    quoted_ids = by_id(quoted_thread)
    quoted_post = quoted_ids.get(quote_of_id)
    handle = quoted_post.handle if quoted_post is not None else "i"
    url = f"https://x.com/{handle}/status/{quote_of_id}"
    if notes is None:
        return url, None
    wiki = f"archive/threads/{notes.parent.name}/{notes.name}"
    ops = [p.post_id for p in quoted_thread.posts if p.reply_to_id is None]
    op_id = ops[0] if ops else quoted_thread.root_post_id
    if quote_of_id != op_id:
        wiki = f"{wiki}#^{quote_of_id}"
    return url, wiki


def _frontmatter_block(text: str) -> str:
    """Return the raw YAML block between the ``---`` fences, or ``""`` if not parseable."""
    if not text.startswith("---"):
        return ""
    rest = text[3:]
    if rest.startswith("\n"):
        rest = rest[1:]
    end = rest.find("\n---")
    if end < 0:
        return ""
    return rest[:end]


def _frontmatter_post_id(text: str) -> str | None:
    """Pull ``post_id`` out of an archive note's YAML frontmatter (returns ``None`` if absent)."""
    for line in _frontmatter_block(text).splitlines():
        match = _POST_ID_LINE.match(line.strip())
        if match:
            return match.group(1)
    return None


def collect_existing_ids(vault: Path) -> tuple[set[str], dict[str, Path]]:
    """Return every archive post_id and spine dirs keyed by spine post_id."""
    threads = vault / "archive" / "threads"
    ids: set[str] = set()
    spines: dict[str, Path] = {}
    if not threads.is_dir():
        return ids, spines
    for md in threads.rglob("*.md"):
        pid = _frontmatter_post_id(md.read_text(encoding="utf-8"))
        if not pid:
            continue
        ids.add(pid)
        if md.name == "index.md" and md.parent.parent.parent == threads:
            spines[pid] = md.parent
    return ids, spines


def _split_frontmatter(text: str) -> tuple[str, str]:
    """Split an archive note into (frontmatter_with_closing_fence, body). Returns ``("", text)`` if no fence."""
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end < 0:
        return "", text
    closer = end + 4
    fm = text[:closer]
    body = text[closer:]
    if body.startswith("\n"):
        fm += "\n"
        body = body[1:]
    elif not fm.endswith("\n"):
        fm += "\n"
    return fm, body


def _upsert_wikilink(path: Path, target: str) -> None:
    """Insert or move a wikilink target on the handle index.

    If the handle folder contains a directory whose name matches `target`,
    any other wikilink whose basename does not match a real directory is
    dropped. This keeps the handle index in sync when a folder is reused
    with a new slug (e.g., a tip-climb refresh renames the folder).
    """
    text = path.read_text(encoding="utf-8")
    fm, body = _split_frontmatter(text)
    if not fm.strip():
        # Frontmatter got nuked by a hand edit. Don't silently emit a
        # bare wikilink list — fall back to a fresh standard frontmatter
        # so the file remains a complete page.
        handle = path.parent.name
        fm = (
            f"---\n"
            f"title: {handle}\n"
            f"type: note\n"
            f"draft: false\n"
            f"description: Archived threads by {handle}.\n"
            f"tags:\n"
            f"  - archive\n"
            f"  - twitter\n"
            f"  - {handle}\n"
            f"---\n"
        )
    kept: list[str] = []
    names: list[str] = []
    handle_dir = path.parent
    real_dirs = {d.name for d in handle_dir.iterdir() if d.is_dir()} if handle_dir.is_dir() else set()
    for line in body.splitlines():
        match = _WIKILINK_ITEM.match(line)
        if match:
            name = match.group(1)
            # wikilinks are vault-root paths; compare the basename to real_dirs
            if name.rsplit("/", 1)[-1] in real_dirs or not real_dirs:
                if name not in names:
                    names.append(name)
        else:
            kept.append(line)
    if target not in names:
        names.append(target)
    names.sort()
    while kept and kept[0] == "":
        kept.pop(0)
    while kept and kept[-1] == "":
        kept.pop()
    parts: list[str] = []
    if kept:
        parts.extend(kept)
        parts.append("")
    parts.extend(f"- [[{name}]]" for name in names)
    parts.append("")
    body_text = "\n".join(parts)
    path.write_text(fm.rstrip() + "\n\n" + body_text, encoding="utf-8", newline="\n")


def wiki_thread(handle: str, dir_name: str) -> str:
    """Build the vault-root wikilink target for a thread spine folder."""
    return f"archive/threads/{handle}/{dir_name}"


def wiki_branch(handle: str, dir_name: str, name: str) -> str:
    """Build the vault-root wikilink target for one branch file."""
    return f"archive/threads/{handle}/{dir_name}/{name}"


def parse_attach(raw: str) -> tuple[str, str]:
    """Parse ``child:parent``. Ids have no colon."""
    if raw.count(":") != 1:
        raise SystemExit(f"attach must be child:parent, got {raw}")
    child_id, parent_id = raw.split(":")
    if not child_id or not parent_id:
        raise SystemExit(f"attach must be child:parent, got {raw}")
    return child_id, parent_id


def apply_attaches(
    thread: ThreadData,
    attaches: tuple[tuple[str, str], ...],
) -> ThreadData:
    """Set each child's ``reply_to_id`` to the named parent. Both ids must exist."""
    by_post = {post.post_id: post for post in thread.posts}
    for child_id, parent_id in attaches:
        if child_id not in by_post:
            raise SystemExit(f"attach child missing: {child_id}")
        if parent_id not in by_post:
            raise SystemExit(f"attach parent missing: {parent_id}")
        by_post[child_id] = replace(by_post[child_id], reply_to_id=parent_id)
        print(f"attach {child_id} -> {parent_id}")
    return ThreadData(
        root_post_id=thread.root_post_id,
        posts=tuple(by_post[post.post_id] for post in thread.posts),
        source_url=thread.source_url,
    )


def write_thread_json(path: Path, thread: ThreadData) -> None:
    """Write one thread_data.json from a typed thread."""
    payload = {
        "root_post_id": thread.root_post_id,
        "source_url": thread.source_url,
        "posts": [asdict(post) for post in thread.posts],
    }
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def foreign_owner_dirs(
    thread: ThreadData,
    handle: str,
    spines: dict[str, Path],
) -> tuple[Path, ...]:
    """Archive dirs that hold this thread's posts under a different handle."""
    found: list[Path] = []
    seen: set[Path] = set()
    for post in thread.posts:
        candidate = spines.get(post.post_id)
        if candidate is None or candidate.parent.name == handle:
            continue
        if candidate in seen:
            continue
        seen.add(candidate)
        found.append(candidate)
    return tuple(found)


def rewrite_handle_index_from_dirs(path: Path) -> None:
    """Rebuild handle-index wikilinks from remaining thread folders."""
    if not path.is_file():
        return
    handle = path.parent.name
    real = sorted(item.name for item in path.parent.iterdir() if item.is_dir())
    text = path.read_text(encoding="utf-8")
    fm, body = _split_frontmatter(text)
    kept = [
        line for line in body.splitlines() if not _WIKILINK_ITEM.match(line)
    ]
    links = [f"- [[{wiki_thread(handle, name)}]]" for name in real]
    parts = [line for line in kept if line.strip()] + links
    path.write_text(
        fm.rstrip() + "\n\n" + "\n".join(parts) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def ensure_handle_index(vault: Path, handle: str, dir_name: str) -> None:
    """Create the per-handle index.md if missing, otherwise upsert the new thread wikilink."""
    path = vault / "archive" / "threads" / handle / "index.md"
    target = wiki_thread(handle, dir_name)
    if not path.is_file():
        front = (
            "---\n"
            f"title: {handle}\n"
            "type: note\n"
            "draft: false\n"
            f"description: Archived threads by {handle}.\n"
            "tags:\n"
            "  - archive\n"
            "  - twitter\n"
            f"  - {handle}\n"
            "---\n"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            front + f"\n- [[{target}]]\n",
            encoding="utf-8",
            newline="\n",
        )
        return
    _upsert_wikilink(path, target)


def ensure_threads_index(vault: Path, handle: str) -> None:
    """Create the top-level archive/threads/index.md if missing, otherwise upsert the handle wikilink."""
    path = vault / "archive" / "threads" / "index.md"
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            (
                "---\n"
                "title: Threads\n"
                "type: note\n"
                "draft: false\n"
                "description: Archived Twitter/X threads and similar sequential posts.\n"
                "tags:\n"
                "  - archive\n"
                "---\n"
                "\n"
                "Threads are filed by author handle, then by date and title. "
                "The main note in each folder is that author's own chain. "
                "Replies live beside it.\n"
                "\n"
                "How to read a folder: [[How threads are organized]].\n"
                "\n"
                "Example of the note shape (single spine, no branches): "
                "[[How to archive a thread]]\n"
                "\n"
                f"- [[archive/threads/{handle}]]\n"
            ),
            encoding="utf-8",
            newline="\n",
        )
        return
    _upsert_wikilink(path, f"archive/threads/{handle}")


def discover_dumps(root: Path) -> list[Path]:
    """Return the sorted list of dump subdirectories that contain ``thread_data.json``."""
    dumps = [
        path for path in root.iterdir()
        if path.is_dir() and (path / "thread_data.json").is_file()
    ]
    dumps.sort(key=lambda path: path.name)
    return dumps


def _gap_line(
    post_id: str,
    handle: str,
    missing: list[str],
    empty: list[str],
) -> str:
    miss = ",".join(missing) if missing else "-"
    empt = ",".join(empty) if empty else "-"
    return f"{post_id} {handle} root {miss} {empt}"


def emit(
    input_dir: Path,
    vault: Path,
    slug: str | None,
    archived: str,
    *,
    force: bool = False,
    reuse_dir: Path | None = None,
    tip: str | None = None,
    reconcile_scratch: Path = SCRATCH,
    frozen_ids: set[str] | None = None,
    attaches: tuple[tuple[str, str], ...] = (),
    allow_broken_walk: bool = False,
    retire_old_dir: bool = False,
) -> EmitResult:
    src = input_dir / "thread_data.json"
    if not src.is_file():
        raise SystemExit(f"missing {src}")

    thread = load_thread(src)
    if not thread.posts:
        raise SystemExit(f"no posts in {src}")
    if attaches:
        thread = apply_attaches(thread, attaches)
        write_thread_json(src, thread)

    if tip:
        spine = spine_from_tip(thread, tip)
        input_kind = "tip"
        print("spine-walk " + " <- ".join(reversed(spine)))
        missing = by_id(thread)[spine[0]].reply_to_id
        if missing:
            message = f"spine-walk stops missing_parent={missing}"
            if not allow_broken_walk:
                raise SystemExit(message)
            print(message)
    else:
        spine = spine_ids(thread)
        input_kind = "root"
    roots = branch_roots(thread, spine)
    ids = by_id(thread)
    kids = children_map(thread)
    first = ids[spine[0]]
    handle = first.handle
    rendered_title = title_text(first.text)
    desired_dir_name = thread_dir_name(date_prefix(first.timestamp), rendered_title, slug)

    _existing_ids, spines = collect_existing_ids(vault)
    leftovers = foreign_owner_dirs(thread, handle, spines)
    if leftovers:
        listed = ", ".join(str(path) for path in leftovers)
        if not retire_old_dir:
            raise SystemExit(f"leftover dir {listed}; pass --retire-old-dir")
        for old in leftovers:
            asset_old = (
                vault / "assets" / "threads" / old.parent.name / old.name
            )
            shutil.rmtree(old)
            if asset_old.is_dir():
                shutil.rmtree(asset_old)
            rewrite_handle_index_from_dirs(old.parent / "index.md")
            print(f"retire-old-dir {old}")
        _existing_ids, spines = collect_existing_ids(vault)

    if reuse_dir is None and force:
        # Only accept a candidate whose parent handle matches the
        # OP handle. A thread previously archived at a different
        # author's dir (e.g. an old tip-as-root archive of a cross-
        # author conversation) is treated as orphan, not a reuse.
        candidate = spines.get(thread.root_post_id)
        if candidate is not None and candidate.parent.name == handle:
            reuse_dir = candidate
        if reuse_dir is None:
            for post in thread.posts:
                candidate = spines.get(post.post_id)
                if candidate is not None and candidate.parent.name == handle:
                    reuse_dir = candidate
                    break
        if reuse_dir is None and slug:
            candidate = vault / "archive" / "threads" / handle / slug
            if candidate.is_dir():
                reuse_dir = candidate

    if reuse_dir is not None:
        handle = reuse_dir.parent.name
        dir_name = reuse_dir.name
        note_dir = reuse_dir
        asset_dir = vault / "assets" / "threads" / handle / dir_name
        if dir_name != desired_dir_name:
            active_frozen_ids = (
                frozen_ids if frozen_ids is not None else load_frozen_ids(FROZEN)
            )
            match = frozen_match(asset_dir, active_frozen_ids)
            if match is not None:
                raise SystemExit(f"frozen: skipped ({match})")
            new_archive = vault / "archive" / "threads" / handle / desired_dir_name
            new_asset = vault / "assets" / "threads" / handle / desired_dir_name
            move = ReslugMove(
                handle=handle,
                old_dir_name=dir_name,
                new_dir_name=desired_dir_name,
                archive_old=reuse_dir,
                archive_new=new_archive,
                asset_old=asset_dir,
                asset_new=new_asset,
            )
            rename_thread_pair(move)
            frozen_dirs = plan_reslug(vault, active_frozen_ids).frozen_dirs
            old_prefix = f"archive/threads/{handle}/{dir_name}"
            new_prefix = f"archive/threads/{handle}/{desired_dir_name}"
            rewrite_archive_paths(
                vault,
                reconcile_scratch,
                {old_prefix: new_prefix},
                frozen_dirs,
            )
            dir_name = desired_dir_name
            note_dir = new_archive
            asset_dir = new_asset
    else:
        dir_name = desired_dir_name
        note_dir = vault / "archive" / "threads" / handle / dir_name
        asset_dir = vault / "assets" / "threads" / handle / dir_name
        if note_dir.exists() or asset_dir.exists():
            raise SystemExit(f"destination occupied: {note_dir}")

    branch_names: dict[str, str] = {}
    for rid in roots:
        branch = ids[rid]
        fname = branch_file_name(
            date_prefix(branch.timestamp),
            branch.handle,
            branch.text,
        )
        name = fname[:-3] if fname.endswith(".md") else fname
        branch_names[rid] = name

    note_dir.mkdir(parents=True, exist_ok=True)
    asset_dir.mkdir(parents=True, exist_ok=True)

    now = archived + "T12:00:00Z"
    fresh_items = collect_media(thread, input_dir, asset_dir, now=now)
    items = merge_existing_media(asset_dir, fresh_items)
    media_by_post = selected_media_by_post(items)
    missing_keys = missing_local_media(items)

    branch_links = {
        rid: wiki_branch(handle, dir_name, name)
        for rid, name in branch_names.items()
    }
    quote_refs: dict[str, tuple[str, str | None]] = {}
    for pid in spine:
        quote_id = ids[pid].quote_of_id
        if quote_id:
            quote_refs[pid] = quote_ref_for(vault, quote_id)

    spine_text = render_spine(
        thread,
        spine,
        roots,
        branch_links,
        archived,
        media_by_post,
        quote_refs,
    )
    spine_path = note_dir / "index.md"
    if spine_path.is_file():
        spine_text = preserve_review_state(
            spine_path.read_text(encoding="utf-8"),
            spine_text,
            mechanical_tags={"archive", "twitter", handle},
        )
    spine_path.write_text(spine_text, encoding="utf-8", newline="\n")

    for rid in roots:
        branch_path = note_dir / f"{branch_names[rid]}.md"
        branch_text = render_branch(
            thread,
            rid,
            descendants(rid, kids),
            first.handle,
            archived,
            media_by_post,
            spine_wiki=wiki_thread(handle, dir_name),
        )
        if branch_path.is_file():
            branch_text = preserve_review_state(
                branch_path.read_text(encoding="utf-8"),
                branch_text,
                mechanical_tags={"archive", "twitter", handle},
            )
        branch_path.write_text(branch_text, encoding="utf-8", newline="\n")

    keep = {spine_path.name}
    keep.update(f"{name}.md" for name in branch_names.values())
    for path in note_dir.glob("*.md"):
        if path.name not in keep:
            path.unlink()

    shutil.copy2(src, asset_dir / "thread_data.json")
    media_doc = {
        "schema_version": 2,
        "root_post_id": thread.root_post_id,
        "items": [_item_to_wire(item) for item in items],
        "mirrors": [],
    }
    atomic_write_json(asset_dir / "media.json", media_doc)
    missing_quotes = [
        qid
        for qid in spine_quote_ids(thread, spine)
        if archive_for_post(vault, qid)[0] is None
    ]
    gaps_text = render_gaps(
        thread,
        spine,
        input_kind=input_kind,
        missing_quote_of=missing_quotes,
    )
    if missing_keys:
        gaps_text += "\nmissing_media_local:\n" + "\n".join(missing_keys) + "\n"
    (asset_dir / "gaps.md").write_text(
        gaps_text,
        encoding="utf-8",
        newline="\n",
    )

    ensure_handle_index(vault, handle, dir_name)
    ensure_threads_index(vault, handle)

    return EmitResult(
        post_id=thread.root_post_id,
        handle=handle,
        dir_name=dir_name,
        branch_count=len(roots),
        missing_media_count=len(missing_keys),
    )


def emit_all(
    dumps_root: Path,
    vault: Path,
    archived: str,
    force: bool,
) -> tuple[int, int, int, int]:
    dumps = discover_dumps(dumps_root)
    existing_ids, spines = collect_existing_ids(vault)
    lines: list[str] = []
    skipped = 0
    written = 0
    errors = 0

    for dump in dumps:
        src = dump / "thread_data.json"
        try:
            thread = load_thread(src)
            if not thread.posts:
                raise ValueError(f"no posts in {src}")
            spine = spine_ids(thread)
            handle = by_id(thread)[spine[0]].handle
            missing = missing_parent_ids(thread)
            empty = empty_text_ids(thread)
            post_id = thread.root_post_id
        except Exception as exc:
            logger.warning("emit_all: skipping %s: %s", dump, exc)
            lines.append(f"{dump.name} ? error - -")
            errors += 1
            continue

        lines.append(_gap_line(post_id, handle, missing, empty))

        if post_id in existing_ids and not force:
            skipped += 1
            continue

        reuse = spines.get(post_id) if force else None
        try:
            emit(
                dump,
                vault,
                None,
                archived,
                force=force,
                reuse_dir=reuse,
            )
        except Exception as exc:
            logger.warning("emit_all: skipping %s: %s", dump, exc)
            errors += 1
            continue

        written += 1
        existing_ids.add(post_id)

    out = vault / "assets" / "threads" / "_batch_gaps.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return len(dumps), skipped, written, errors


# --- relabel (patch **N/** lines with @handle from on-disk JSON) ---


_NUMBER_LINE: re.Pattern[str] = re.compile(
    r"^(\*\*(\d+)/\*\*)(?: +(?:\*\*)?@([A-Za-z0-9_]+)(?:\*\*)?)?(?: +\^([A-Za-z0-9_]+))?[ \t]*$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class RelabelItem:
    """One note's in-place number-line patch outcome."""
    path: Path
    state: str
    reason: str


@dataclass(frozen=True)
class RelabelPlan:
    """Corpus plan for patching ``**N/**`` lines. Notes only."""
    vault: Path
    items: tuple[RelabelItem, ...]

    @property
    def can_apply(self) -> bool:
        return not any(item.state == "conflict" for item in self.items)


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _extract_post_body(after_number_line: str) -> str:
    """Text after a ``**N/**`` line, stopping at media, branches, or a heading."""
    lines: list[str] = []
    for line in after_number_line.lstrip("\n").splitlines():
        if line.startswith("![") or line.startswith("<video"):
            break
        if line.startswith("Branches:"):
            break
        if line.startswith("## "):
            break
        if _NUMBER_LINE.match(line):
            break
        lines.append(line)
    return "\n".join(lines).strip()


def _frontmatter_handle(text: str) -> str:
    """Return the note-root ``handle:`` value, or empty."""
    in_front = False
    for line in text.splitlines():
        if line.strip() == "---":
            if in_front:
                return ""
            in_front = True
            continue
        if in_front and line.startswith("handle:"):
            return line.split(":", 1)[1].strip()
    return ""


def _frontmatter_post_id(text: str) -> str:
    """Return the note-root ``post_id:`` value, or empty."""
    in_front = False
    for line in text.splitlines():
        if line.strip() == "---":
            if in_front:
                return ""
            in_front = True
            continue
        if in_front and line.startswith("post_id:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return ""


def _body_match_keys(body: str) -> set[str]:
    """Keys used to pair a note body with ``post.text`` before or after mention split."""
    mentions, rest = split_leading_mentions(body)
    keys: set[str] = set()
    if rest:
        rest_first = _first_nonempty_line(rest)
        if rest_first:
            keys.add(rest_first)
            if mentions:
                keys.add(f"{mentions} {rest_first}")
    else:
        first = _first_nonempty_line(body)
        if first:
            keys.add(first)
    return keys


def _post_match_keys(text: str) -> set[str]:
    mentions, rest = split_leading_mentions(text)
    keys: set[str] = set()
    first = _first_nonempty_line(text)
    if first:
        keys.add(first)
    if rest:
        rest_first = _first_nonempty_line(rest)
        if rest_first:
            keys.add(rest_first)
            if mentions:
                keys.add(f"{mentions} {rest_first}")
    return keys


def match_post_for_body(
    body: str,
    posts: tuple,
    used: set[str],
) -> object | None:
    """Return one unused post whose text matches ``body``.

    Duplicate first lines are fine when every hit has the same handle.
    Mixed-handle collisions return ``None``.
    """
    keys = _body_match_keys(body)
    if not keys:
        return None
    hits = [
        post
        for post in posts
        if post.post_id not in used and keys & _post_match_keys(post.text)
    ]
    if not hits:
        return None
    handles = {str(post.handle or "") for post in hits}
    if len(handles) > 1:
        return None
    hits.sort(key=lambda post: (post.timestamp, post.post_id))
    return hits[0]


def patch_note_text(text: str, posts: tuple) -> tuple[str, str, str]:
    """Patch ``**N/**`` lines in ``text``. Returns ``(new_text, state, reason)``."""
    matches = list(_NUMBER_LINE.finditer(text))
    if not matches:
        return text, "noop", "no number lines"
    pieces: list[str] = []
    last = 0
    changed = False
    unmatched: list[str] = []
    used: set[str] = set()
    root_handle = _frontmatter_handle(text)
    for index, match in enumerate(matches):
        pieces.append(text[last:match.start()])
        number = match.group(2)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = _extract_post_body(text[match.end():end])
        post = match_post_for_body(body, posts, used)
        handle = ""
        post_id = ""
        if post is not None:
            handle = str(post.handle or "")
            post_id = str(post.post_id or "")
            if handle:
                used.add(post.post_id)
        if not handle and index == 0 and root_handle:
            handle = root_handle
            post_id = _frontmatter_post_id(text)
        region = text[match.end():end]
        if not handle:
            unmatched.append(f"**{number}/**")
            pieces.append(match.group(0).rstrip())
            pieces.append(region)
            last = end
            continue
        new_line = f"**{number}/** **@{handle}**"
        if post_id:
            new_line += f" ^{post_id}"
        if new_line != match.group(0).rstrip():
            changed = True
        formatted = format_post_text(body)
        if body and formatted != body:
            region = region.replace(body, formatted, 1)
            changed = True
        pieces.append(new_line)
        pieces.append(region)
        last = end
    pieces.append(text[last:])
    new_text = "".join(pieces)
    reason = ",".join(unmatched)
    if unmatched and not changed:
        return text, "conflict", reason
    if changed:
        return new_text, "rewrite", reason
    return text, "noop", ""


def plan_relabel(vault: Path) -> RelabelPlan:
    """Walk on-disk ``thread_data.json`` and classify each thread note."""
    assets_root = vault / "assets" / "threads"
    notes_root = vault / "archive" / "threads"
    items: list[RelabelItem] = []
    if not assets_root.is_dir():
        return RelabelPlan(vault, ())
    for data_path in sorted(assets_root.rglob("thread_data.json")):
        relative = data_path.parent.relative_to(assets_root)
        note_dir = notes_root / relative
        if not note_dir.is_dir():
            items.append(RelabelItem(note_dir, "conflict", "missing note dir"))
            continue
        try:
            thread = load_thread(data_path)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            items.append(RelabelItem(data_path, "conflict", str(exc)[:200]))
            continue
        notes = sorted(path for path in note_dir.glob("*.md") if path.is_file())
        if not notes:
            items.append(RelabelItem(note_dir, "conflict", "no notes"))
            continue
        for note_path in notes:
            text = note_path.read_text(encoding="utf-8")
            _new, state, reason = patch_note_text(text, thread.posts)
            items.append(RelabelItem(note_path, state, reason))
    return RelabelPlan(vault, tuple(items))


def apply_relabel(plan: RelabelPlan) -> None:
    """Write ``rewrite`` notes. Leave conflicts and JSON/media untouched."""
    assets_root = plan.vault / "assets" / "threads"
    notes_root = plan.vault / "archive" / "threads"
    for item in plan.items:
        if item.state != "rewrite":
            continue
        try:
            relative = item.path.parent.relative_to(notes_root)
        except ValueError:
            continue
        data_path = assets_root / relative / "thread_data.json"
        if not data_path.is_file():
            continue
        thread = load_thread(data_path)
        text = item.path.read_text(encoding="utf-8")
        new_text, state, _reason = patch_note_text(text, thread.posts)
        if state != "rewrite":
            continue
        item.path.write_text(new_text, encoding="utf-8", newline="\n")


def format_relabel_plan(plan: RelabelPlan) -> str:
    """Print one line per note plus counts."""
    lines: list[str] = []
    counts = {"rewrite": 0, "noop": 0, "conflict": 0}
    for item in plan.items:
        counts[item.state] = counts.get(item.state, 0) + 1
        extra = f" {item.reason}" if item.reason else ""
        lines.append(f"{item.state} {item.path}{extra}")
    lines.append(
        f"rewrite={counts.get('rewrite', 0)} "
        f"noop={counts.get('noop', 0)} "
        f"conflict={counts.get('conflict', 0)}"
    )
    return "\n".join(lines) + "\n"


# --- reslug (one-time bulk title/path reconciliation) ---


@dataclass(frozen=True)
class ReslugMove:
    """One paired archive/asset directory rename."""
    handle: str
    old_dir_name: str
    new_dir_name: str
    archive_old: Path
    archive_new: Path
    asset_old: Path
    asset_new: Path


@dataclass(frozen=True)
class ReslugConflict:
    """One bulk preflight failure surfaced before any rename."""
    path: Path
    reason: str


@dataclass(frozen=True)
class ReslugPlan:
    """Small immutable one-time corpus repair plan."""
    vault: Path
    moves: tuple[ReslugMove, ...]
    noops: tuple[Path, ...]
    frozen: tuple[Path, ...]
    frozen_dirs: tuple[Path, ...]
    conflicts: tuple[ReslugConflict, ...]

    @property
    def can_apply(self) -> bool:
        return not self.conflicts


_TITLE_LINE: re.Pattern[str] = re.compile(r"^title:\s*(.+?)\s*$")
_DATE_LINE: re.Pattern[str] = re.compile(r"^date:\s*(\d{4}-\d{2}-\d{2})\s*$")


def _yaml_scalar_value(raw: str) -> str:
    """Decode a single-line YAML scalar that is either JSON-quoted or unquoted."""
    s = raw.strip()
    if len(s) >= 2 and s.startswith('"') and s.endswith('"'):
        body = s[1:-1]
        body = body.replace("\\\\", "\x00").replace('\\"', '"').replace("\x00", "\\")
        return body
    return s


def _frontmatter_title_date(text: str) -> tuple[str, str] | None:
    """Return (title, date) from an archive note's frontmatter or ``None`` when unparseable."""
    block = _frontmatter_block(text)
    if not block:
        return None
    title: str | None = None
    date_value: str | None = None
    for line in block.splitlines():
        stripped = line.strip()
        if title is None:
            match = _TITLE_LINE.match(line)
            if match:
                title = _yaml_scalar_value(match.group(1))
                continue
        if date_value is None:
            match = _DATE_LINE.match(line)
            if match:
                date_value = match.group(1)
                continue
    if title is None or date_value is None:
        return None
    return title, date_value


_RESLUG_EXCLUDED_TOP_LEVEL: tuple[str, ...] = (
    ".git",
    "site",
    "assets",
    "secrets",
    "node_modules",
)


def plan_reslug(vault: Path, frozen_ids: set[str]) -> ReslugPlan:
    """Build an immutable repair plan for ``archive/threads/<handle>/<thread>`` directories."""
    moves: list[ReslugMove] = []
    noops: list[Path] = []
    frozen_entries: list[Path] = []
    frozen_dirs: list[Path] = []
    conflicts: list[ReslugConflict] = []

    threads_root = vault / "archive" / "threads"
    assets_root = vault / "assets" / "threads"

    if not threads_root.is_dir():
        return ReslugPlan(vault, (), (), (), (), ())

    for handle_dir in sorted(threads_root.iterdir(), key=lambda p: p.name):
        if not handle_dir.is_dir():
            continue
        handle = handle_dir.name
        for thread_dir in sorted(handle_dir.iterdir(), key=lambda p: p.name):
            if not thread_dir.is_dir():
                continue
            old_dir_name = thread_dir.name
            index_path = thread_dir / "index.md"
            asset_dir = assets_root / handle / old_dir_name
            try:
                if not index_path.is_file():
                    conflicts.append(
                        ReslugConflict(thread_dir, "missing index.md")
                    )
                    continue
                try:
                    text = index_path.read_text(encoding="utf-8")
                except OSError as exc:
                    conflicts.append(
                        ReslugConflict(index_path, f"unreadable frontmatter: {exc}")
                    )
                    continue
                parsed = _frontmatter_title_date(text)
                if parsed is None:
                    conflicts.append(
                        ReslugConflict(
                            index_path,
                            "missing or malformed frontmatter title/date",
                        )
                    )
                    continue
                title, date_value = parsed
                if not asset_dir.is_dir():
                    conflicts.append(
                        ReslugConflict(
                            index_path,
                            f"missing asset pair at {asset_dir}",
                        )
                    )
                    continue
                thread_data = asset_dir / "thread_data.json"
                media_json = asset_dir / "media.json"
                if not thread_data.is_file():
                    conflicts.append(
                        ReslugConflict(index_path, "missing thread_data.json")
                    )
                    continue
                if not media_json.is_file():
                    conflicts.append(
                        ReslugConflict(index_path, "missing media.json")
                    )
                    continue
                try:
                    json.loads(thread_data.read_text(encoding="utf-8"))
                except (OSError, ValueError) as exc:
                    conflicts.append(
                        ReslugConflict(
                            index_path,
                            f"invalid thread_data.json: {exc}",
                        )
                    )
                    continue
                try:
                    json.loads(media_json.read_text(encoding="utf-8"))
                except (OSError, ValueError) as exc:
                    conflicts.append(
                        ReslugConflict(
                            index_path,
                            f"invalid media.json: {exc}",
                        )
                    )
                    continue
                expected = thread_dir_name(date_value, title, None)
                match = frozen_match(asset_dir, frozen_ids)
                if old_dir_name == expected:
                    noops.append(thread_dir)
                    if match is not None:
                        frozen_dirs.append(thread_dir)
                    continue
                if match is not None:
                    frozen_entries.append(thread_dir)
                    frozen_dirs.append(thread_dir)
                    continue
                new_archive = threads_root / handle / expected
                new_asset = assets_root / handle / expected
                if new_archive.exists():
                    conflicts.append(
                        ReslugConflict(
                            thread_dir,
                            f"destination occupied: {new_archive}",
                        )
                    )
                    continue
                if new_asset.exists():
                    conflicts.append(
                        ReslugConflict(
                            thread_dir,
                            f"destination occupied: {new_asset}",
                        )
                    )
                    continue
                moves.append(
                    ReslugMove(
                        handle=handle,
                        old_dir_name=old_dir_name,
                        new_dir_name=expected,
                        archive_old=thread_dir,
                        archive_new=new_archive,
                        asset_old=asset_dir,
                        asset_new=new_asset,
                    )
                )
            except OSError as exc:
                conflicts.append(
                    ReslugConflict(thread_dir, f"filesystem error: {exc}")
                )
                continue

    moves.sort(key=lambda m: str(m.archive_old))
    noops.sort(key=str)
    frozen_entries.sort(key=str)
    frozen_dirs.sort(key=str)
    conflicts.sort(key=lambda c: str(c.path))
    return ReslugPlan(
        vault,
        tuple(moves),
        tuple(noops),
        tuple(frozen_entries),
        tuple(frozen_dirs),
        tuple(conflicts),
    )


def rename_thread_pair(move: ReslugMove) -> None:
    """Validate, rename assets first, then archive; roll the asset back on archive failure."""
    if not move.archive_old.is_dir() or not move.asset_old.is_dir():
        raise RuntimeError(f"source pair missing: {move.archive_old}")
    if move.archive_new.exists() or move.asset_new.exists():
        raise RuntimeError(f"destination occupied: {move.archive_new}")
    move.asset_old.rename(move.asset_new)
    try:
        move.archive_old.rename(move.archive_new)
    except OSError:
        move.asset_new.rename(move.asset_old)
        raise


def rewrite_archive_paths(
    vault: Path,
    scratch: Path,
    replacements: dict[str, str],
    frozen_dirs: tuple[Path, ...],
) -> tuple[Path, ...]:
    """Recursively rewrite exact vault-root prefixes in mutable Markdown and Canvas files."""
    if not replacements:
        return ()

    keys = sorted(replacements.keys(), key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(key) for key in keys))

    changed: list[Path] = []
    stage_dir = scratch / "reslug_text"
    sequence = 0
    for path in sorted(vault.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in (".md", ".canvas"):
            continue
        try:
            rel_parts = path.relative_to(vault).parts
        except ValueError:
            continue
        if rel_parts and rel_parts[0] in _RESLUG_EXCLUDED_TOP_LEVEL:
            continue
        skip = False
        for frozen in frozen_dirs:
            try:
                path.relative_to(frozen)
                skip = True
                break
            except ValueError:
                continue
        if skip:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        new_text = pattern.sub(lambda m: replacements[m.group(0)], text)
        if new_text == text:
            continue
        stage_dir.mkdir(parents=True, exist_ok=True)
        stage_path = stage_dir / f"{sequence}.tmp"
        sequence += 1
        stage_path.write_text(new_text, encoding="utf-8", newline="\n")
        os.replace(stage_path, path)
        changed.append(path)

    try:
        stage_dir.rmdir()
    except OSError:
        pass

    changed.sort(key=str)
    return tuple(changed)


def apply_reslug_plan(plan: ReslugPlan, scratch: Path) -> tuple[Path, ...]:
    """Run every rename, then recursively rewrite mutable paths; refuse on conflict."""
    if plan.conflicts:
        reasons = ", ".join(c.reason for c in plan.conflicts)
        raise RuntimeError(
            f"reslug blocked by {len(plan.conflicts)} conflict(s): {reasons}"
        )
    replacements: dict[str, str] = {}
    for move in plan.moves:
        rename_thread_pair(move)
        old_prefix = f"archive/threads/{move.handle}/{move.old_dir_name}"
        new_prefix = f"archive/threads/{move.handle}/{move.new_dir_name}"
        replacements[old_prefix] = new_prefix
        print(f"renamed -> {move.archive_new}")
    rewritten = (
        rewrite_archive_paths(
            plan.vault,
            scratch,
            replacements,
            plan.frozen_dirs,
        )
        if plan.moves
        else ()
    )
    for path in rewritten:
        print(f"rewrote -> {path}")
    return rewritten


def format_reslug_plan(plan: ReslugPlan) -> str:
    """Return a deterministic human-readable summary of a repair plan."""
    lines: list[str] = []
    for path in plan.noops:
        lines.append(f"[noop] {path.as_posix()}")
    for move in plan.moves:
        lines.append(
            f"[rename] {move.archive_old.as_posix()} -> {move.archive_new.as_posix()}"
        )
    for path in plan.frozen:
        lines.append(f"[frozen] {path.as_posix()}")
    for conflict in plan.conflicts:
        lines.append(f"[conflict] {conflict.path.as_posix()}: {conflict.reason}")
    lines.append(
        f"summary: moves={len(plan.moves)} noops={len(plan.noops)} "
        f"frozen={len(plan.frozen)} conflicts={len(plan.conflicts)}"
    )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Emit Threadwell archive notes from a thread_data.json dump. "
            "No fetch, no lift."
        ),
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--input",
        type=Path,
        help="Dump directory containing thread_data.json",
    )
    source.add_argument(
        "--all",
        dest="all_root",
        type=Path,
        metavar="DUMPS_ROOT",
        help="Convert every dump directory under this root",
    )
    parser.add_argument(
        "--vault",
        required=True,
        type=Path,
        help="Threadwell vault root",
    )
    parser.add_argument(
        "--slug",
        default=None,
        help="Optional slug override for a single --input (ignored with --all)",
    )
    parser.add_argument(
        "--archived",
        default=date.today().isoformat(),
        help="Archive date YYYY-MM-DD (default: today local)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Emit even if post_id already exists in the vault",
    )
    parser.add_argument(
        "--tip",
        default=None,
        help="Climb reply_to from this post_id for the spine (same handle)",
    )
    parser.add_argument(
        "--attach",
        action="append",
        default=[],
        metavar="CHILD:PARENT",
        help="set child.reply_to_id to parent before the spine walk; repeatable",
    )
    parser.add_argument(
        "--allow-broken-walk",
        action="store_true",
        help="emit even if the tip walk stops on a missing parent",
    )
    parser.add_argument(
        "--retire-old-dir",
        action="store_true",
        help="delete archive/asset dirs for this thread under another handle",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.all_root is not None:
        seen, skipped, written, errors = emit_all(
            args.all_root,
            args.vault,
            args.archived,
            args.force,
        )
        print(
            f"dumps seen={seen} skipped={skipped} "
            f"written={written} errors={errors}"
        )
        return 0 if errors == 0 else 1
    emit(
        args.input,
        args.vault,
        args.slug,
        args.archived,
        force=args.force,
        tip=args.tip,
        attaches=tuple(parse_attach(raw) for raw in args.attach),
        allow_broken_walk=args.allow_broken_walk,
        retire_old_dir=args.retire_old_dir,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
