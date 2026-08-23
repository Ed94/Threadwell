"""Emit Threadwell archive notes from a thread_data.json dump. No fetch, no lift."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from twitter.models import ThreadData, load_thread
from twitter.render import render_branch, render_spine
from twitter.slug import branch_file_name, date_prefix, thread_dir_name
from twitter.tree import (
    by_id,
    branch_roots,
    children_map,
    descendants,
    spine_from_tip,
    spine_ids,
)

_POST_ID_LINE = re.compile(r'^post_id:\s*"?([^"\s]+)"?\s*$')
_WIKILINK_ITEM = re.compile(r"^- \[\[([^\]|]+)\]\]\s*$")


@dataclass(frozen=True)
class EmitResult:
    post_id: str
    handle: str
    dir_name: str
    branch_count: int


def _url_media_id(url: str, index: int) -> str:
    segment = Path(unquote(urlparse(url).path)).name
    return segment if segment else f"m{index}"


def _url_ext(url: str) -> str | None:
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
    want = f"{post_id}_{index}"
    for path in unused:
        if path.stem == want:
            return path
    return None


def _take_fallback(unused: list[Path], post_id: str) -> Path | None:
    prefix = f"{post_id}_"
    for path in unused:
        if path.name.startswith(prefix):
            return path
    return None


def collect_media(
    thread: ThreadData,
    input_dir: Path,
    dest_dir: Path,
) -> tuple[list[dict[str, object]], dict[str, tuple[str, ...]]]:
    unused = _media_files(input_dir / "media")
    items: list[dict[str, object]] = []
    by_post: dict[str, list[str]] = {}

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
            if src is not None:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest_dir / filename)
            items.append({
                "post_id": post.post_id,
                "media_id": media_id,
                "handle": post.handle,
                "role": "orig",
                "filename": filename,
                "publish": False,
                "url": None,
            })
            by_post.setdefault(post.post_id, []).append(filename)

    media_by_post = {pid: tuple(names) for pid, names in by_post.items()}
    return items, media_by_post


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


def render_gaps(thread: ThreadData, spine: list[str], *, input_kind: str = "root") -> str:
    ids = by_id(thread)
    suggested = spine[-1] if spine else ""
    quote_ids = [p.post_id for p in thread.posts if p.quote_of_id]
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


def _frontmatter_block(text: str) -> str:
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


def unique_dir_name(parent: Path, base: str) -> str:
    if not (parent / base).exists():
        return base
    n = 2
    while (parent / f"{base}-{n}").exists():
        n += 1
    return f"{base}-{n}"


def _split_frontmatter(text: str) -> tuple[str, str]:
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
    text = path.read_text(encoding="utf-8")
    fm, body = _split_frontmatter(text)
    kept: list[str] = []
    names: list[str] = []
    for line in body.splitlines():
        match = _WIKILINK_ITEM.match(line)
        if match:
            name = match.group(1)
            if name not in names:
                names.append(name)
        else:
            kept.append(line)
    if target not in names:
        names.append(target)
    short = target.rsplit("/", 1)[-1]
    names = [n for n in names if n == target or n != short]
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
    if fm:
        path.write_text(fm.rstrip() + "\n\n" + body_text, encoding="utf-8", newline="\n")
    else:
        path.write_text(body_text, encoding="utf-8", newline="\n")


def wiki_thread(handle: str, dir_name: str) -> str:
    return f"archive/threads/{handle}/{dir_name}"


def wiki_branch(handle: str, dir_name: str, name: str) -> str:
    return f"archive/threads/{handle}/{dir_name}/{name}"


def ensure_handle_index(vault: Path, handle: str, dir_name: str) -> None:
    path = vault / "archive" / "threads" / handle / "index.md"
    target = wiki_thread(handle, dir_name)
    if not path.is_file():
        front = (
            "---\n"
            f"title: {handle}\n"
            "type: note\n"
            "status: published\n"
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
    path = vault / "archive" / "threads" / "index.md"
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            (
                "---\n"
                "title: Threads\n"
                "type: note\n"
                "status: published\n"
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
) -> EmitResult:
    src = input_dir / "thread_data.json"
    if not src.is_file():
        raise SystemExit(f"missing {src}")

    thread = load_thread(src)
    if not thread.posts:
        raise SystemExit(f"no posts in {src}")

    if tip:
        spine = spine_from_tip(thread, tip)
        input_kind = "tip"
    else:
        spine = spine_ids(thread)
        input_kind = "root"
    roots = branch_roots(thread, spine)
    ids = by_id(thread)
    kids = children_map(thread)
    first = ids[spine[0]]
    handle = first.handle
    first_line = (first.text or "").split("\n", 1)[0]

    if reuse_dir is None and force:
        _existing_ids, spines = collect_existing_ids(vault)
        reuse_dir = spines.get(thread.root_post_id)

    if reuse_dir is not None:
        dir_name = reuse_dir.name
        handle = reuse_dir.parent.name
        note_dir = reuse_dir
        asset_dir = vault / "assets" / "threads" / handle / dir_name
    else:
        dir_name = thread_dir_name(date_prefix(first.timestamp), first_line, slug)
        if slug is None:
            dir_name = unique_dir_name(
                vault / "archive" / "threads" / handle,
                dir_name,
            )
        note_dir = vault / "archive" / "threads" / handle / dir_name
        asset_dir = vault / "assets" / "threads" / handle / dir_name

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

    items, media_by_post = collect_media(thread, input_dir, asset_dir)

    branch_links = {
        rid: wiki_branch(handle, dir_name, name)
        for rid, name in branch_names.items()
    }
    (note_dir / "index.md").write_text(
        render_spine(
            thread,
            spine,
            roots,
            branch_links,
            archived,
            media_by_post,
        ),
        encoding="utf-8",
        newline="\n",
    )
    for rid in roots:
        (note_dir / f"{branch_names[rid]}.md").write_text(
            render_branch(
                thread,
                rid,
                descendants(rid, kids),
                first.handle,
                archived,
                media_by_post,
                spine_wiki=wiki_thread(handle, dir_name),
            ),
            encoding="utf-8",
            newline="\n",
        )

    shutil.copy2(src, asset_dir / "thread_data.json")
    media_doc = {
        "root_post_id": thread.root_post_id,
        "items": items,
    }
    (asset_dir / "media.json").write_text(
        json.dumps(media_doc, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (asset_dir / "gaps.md").write_text(
        render_gaps(thread, spine, input_kind=input_kind),
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
        except Exception:
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
        except Exception:
            errors += 1
            continue

        written += 1
        existing_ids.add(post_id)

    out = vault / "assets" / "threads" / "_batch_gaps.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return len(dumps), skipped, written, errors


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
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
