"""Emit Threadwell archive notes from a thread_data.json dump. No fetch, no lift."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from twitter.models import ThreadData, load_thread
from twitter.render import render_branch, render_spine
from twitter.slug import branch_file_name, date_prefix, thread_dir_name
from twitter.tree import by_id, branch_roots, children_map, descendants, spine_ids


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


def render_gaps(thread: ThreadData, spine: list[str]) -> str:
    ids = by_id(thread)
    suggested = spine[-1] if spine else ""
    quote_ids = [p.post_id for p in thread.posts if p.quote_of_id]
    missing = [
        p.post_id
        for p in thread.posts
        if p.reply_to_id is not None and p.reply_to_id not in ids
    ]
    empty = [p.post_id for p in thread.posts if not (p.text or "").strip()]

    lines = [
        "# gaps",
        "input: root",
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


def emit(
    input_dir: Path,
    vault: Path,
    slug: str | None,
    archived: str,
) -> None:
    src = input_dir / "thread_data.json"
    if not src.is_file():
        raise SystemExit(f"missing {src}")

    thread = load_thread(src)
    if not thread.posts:
        raise SystemExit(f"no posts in {src}")

    spine = spine_ids(thread)
    roots = branch_roots(thread, spine)
    ids = by_id(thread)
    kids = children_map(thread)
    first = ids[spine[0]]
    handle = first.handle
    first_line = (first.text or "").split("\n", 1)[0]
    dir_name = thread_dir_name(date_prefix(first.timestamp), first_line, slug)

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

    note_dir = vault / "archive" / "threads" / handle / dir_name
    asset_dir = vault / "assets" / "threads" / handle / dir_name
    note_dir.mkdir(parents=True, exist_ok=True)
    asset_dir.mkdir(parents=True, exist_ok=True)

    items, media_by_post = collect_media(thread, input_dir, asset_dir)

    (note_dir / "index.md").write_text(
        render_spine(
            thread,
            spine,
            roots,
            branch_names,
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
                handle,
                archived,
                media_by_post,
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
        render_gaps(thread, spine),
        encoding="utf-8",
        newline="\n",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Emit Threadwell archive notes from a thread_data.json dump. "
            "No fetch, no lift."
        ),
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Dump directory containing thread_data.json",
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
        help="Optional slug override for the thread directory",
    )
    parser.add_argument(
        "--archived",
        default=date.today().isoformat(),
        help="Archive date YYYY-MM-DD (default: today local)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    emit(args.input, args.vault, args.slug, args.archived)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
