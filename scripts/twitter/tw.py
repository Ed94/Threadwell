"""Front door for Twitter archive work.

From the vault root:

  python scripts/twitter/tw.py graph --id 1692565070583136348
  python scripts/twitter/tw.py refresh --id 1692565070583136348 --tip
  python scripts/twitter/tw.py add-branch --id 1692565070583136348 --from <reply-node>
  python scripts/twitter/tw.py ocr --id 1692565070583136348
  python scripts/twitter/tw.py locate --id 1692565070583136348

refresh = refetch + emit --force. --tip treats --id as the tip.
publish flips draft: false on an old capture. New notes already publish.
Does not commit. Never prints cookies, userhash, or the backup root.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import asdict, replace
from datetime import datetime, timezone
from pathlib import Path

_HERE: Path = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from paths import COOKIES, DUMPS, FROZEN, HERE, SCRATCH, VAULT
from models import PostData, ThreadData, load_thread

try:
    from twitter.tree import spine_from_tip, spine_ids, spine_quote_ids
except ImportError:
    sys.path.insert(0, str(_HERE.parent))
    from twitter.tree import spine_from_tip, spine_ids, spine_quote_ids

try:
    from frozen import frozen_match, load_frozen_ids, require_writable
    from backup_assets import backup_thread, load_destination_root
    from catbox_client import load_userhash, upload_file
    from emit_archive import (
        apply_relabel,
        apply_reslug_plan,
        format_relabel_plan,
        format_reslug_plan,
        plan_relabel,
        plan_reslug,
    )
    from fallback_media import activate_fallback, find_existing_fallback, restore_origin
    from media_audit import audit_thread
    from media_migrate import migrate_legacy_thread
except ImportError:  # pragma: no cover - script-mode import
    from frozen import frozen_match, load_frozen_ids, require_writable
    from backup_assets import backup_thread, load_destination_root
    from catbox_client import load_userhash, upload_file
    from emit_archive import (
        apply_relabel,
        apply_reslug_plan,
        format_relabel_plan,
        format_reslug_plan,
        plan_relabel,
        plan_reslug,
    )
    from fallback_media import activate_fallback, find_existing_fallback, restore_origin
    from media_audit import audit_thread
    from media_migrate import migrate_legacy_thread


def frozen_ids() -> set[str]:
    """Return the loaded set of frozen post_ids from the do-not-refetch list."""
    return load_frozen_ids(FROZEN)


def check_frozen(post_id: str) -> None:
    """Raise SystemExit if ``post_id`` or any of its captured descendants matches a frozen id."""
    direct = dump_dir(post_id)
    assets, _notes = locate(post_id)
    candidate = assets if assets is not None else direct
    if candidate.is_dir():
        match = frozen_match(candidate, frozen_ids())
        if match is not None:
            raise SystemExit(f"frozen: skipped ({match})")
    if post_id in frozen_ids():
        raise SystemExit(f"frozen: skipped ({post_id})")


def dump_dir(post_id: str) -> Path:
    return DUMPS / post_id


def scratch_dir(post_id: str) -> Path:
    return SCRATCH / f"refetch_{post_id}"


def locate(post_id: str) -> tuple[Path | None, Path | None]:
    """Return ``(asset_dir, note_dir)`` for the first media.json whose root or captured posts contain ``post_id``."""
    assets_root = VAULT / "assets" / "threads"
    notes_root = VAULT / "archive" / "threads"
    if not assets_root.is_dir():
        return None, None
    for media in assets_root.rglob("media.json"):
        try:
            data = json.loads(media.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        hit = data.get("root_post_id") == post_id
        if not hit:
            for item in data.get("items") or []:
                if str(item.get("post_id") or "") == post_id:
                    hit = True
                    break
        if not hit:
            td = media.parent / "thread_data.json"
            if td.is_file():
                try:
                    t = json.loads(td.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    t = {}
                if t.get("root_post_id") == post_id:
                    hit = True
                else:
                    hit = any(
                        p.get("post_id") == post_id for p in (t.get("posts") or [])
                    )
        if hit:
            rel = media.parent.relative_to(assets_root)
            notes = notes_root / rel
            return media.parent, notes if notes.is_dir() else None
    return None, None


def locate_all(post_id: str) -> list[tuple[Path, Path | None]]:
    """Return every (asset_dir, note_dir) pair whose media.json,
    thread_data.json, or captured posts contain post_id. Used by emit
    to find per-author asset dirs after a cross-author refresh."""
    assets_root = VAULT / "assets" / "threads"
    notes_root = VAULT / "archive" / "threads"
    if not assets_root.is_dir():
        return []
    out: list[tuple[Path, Path | None]] = []
    for media in assets_root.rglob("media.json"):
        try:
            data = json.loads(media.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        hit = data.get("root_post_id") == post_id
        if not hit:
            for item in data.get("items") or []:
                if str(item.get("post_id") or "") == post_id:
                    hit = True
                    break
        if not hit:
            td = media.parent / "thread_data.json"
            if td.is_file():
                try:
                    t = json.loads(td.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    t = {}
                if t.get("root_post_id") == post_id:
                    hit = True
                else:
                    hit = any(
                        p.get("post_id") == post_id for p in (t.get("posts") or [])
                    )
        if hit:
            rel = media.parent.relative_to(assets_root)
            notes = notes_root / rel
            out.append((media.parent, notes if notes.is_dir() else None))
    return out


def run(cmd: list[str]) -> None:
    print(">", " ".join(cmd))
    subprocess.check_call(cmd)


def cmd_locate(args: argparse.Namespace) -> int:
    """Print the on-disk paths (dump / scratch / assets / notes) for ``args.id``."""
    post_id = args.id
    dump = dump_dir(post_id)
    scratch = scratch_dir(post_id)
    assets, notes = locate(post_id)
    print(f"dump     {dump}  exists={dump.is_dir()}")
    print(f"scratch  {scratch}  exists={scratch.is_dir()}")
    print(f"assets   {assets}")
    print(f"notes    {notes}")
    return 0


def cmd_graph(args: argparse.Namespace) -> int:
    """Render the SSDL + ASCII graph for ``args.id`` into the scratch directory."""
    post_id = args.id
    src = scratch_dir(post_id)
    if not (src / "thread_data.json").is_file():
        src = dump_dir(post_id)
    if not (src / "thread_data.json").is_file():
        raise SystemExit(f"no thread_data.json for {post_id}")
    run([sys.executable, str(HERE / "graph_dry_run.py"), "--input", str(src)])
    return 0


def _capture_ids(post_id: str, branch_ids: list[str]) -> tuple[str, ...]:
    """Return the primary id plus distinct explicit branch tips."""
    return tuple(dict.fromkeys((post_id, *branch_ids)))


def _gallery_base_args() -> list[str]:
    """Return the shared safe, paced gallery-dl arguments."""
    return [
        "gallery-dl",
        "--cookies",
        str(COOKIES),
        "--retries",
        "0",
        "--sleep-extractor",
        "5",
        "--sleep-request",
        "5",
        "-o",
        "text-tweets=true",
        "-o",
        "conversations=true",
    ]


def _merge_gallery_files(paths: list[Path], output: Path) -> None:
    """Concatenate gallery-dl JSON arrays for local ingest."""
    merged: list[object] = []
    for path in paths:
        data: object = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise SystemExit(f"gallery-dl output is not a JSON array: {path}")
        merged.extend(data)
    output.write_text(
        json.dumps(merged, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _validate_capture_ids(path: Path, capture_ids: tuple[str, ...]) -> None:
    """Fail if gallery-dl omitted an explicitly requested tip."""
    thread = load_thread(path)
    present = {post.post_id for post in thread.posts}
    missing = [post_id for post_id in capture_ids if post_id not in present]
    if missing:
        raise SystemExit(f"requested tips missing from capture: {', '.join(missing)}")


def _select_branch_capture(
    existing: ThreadData,
    captured: ThreadData,
    from_id: str,
) -> tuple[tuple[PostData, ...], tuple[str, ...]]:
    """Select one reply node's attachment path and visible subtree."""
    captured_by = {post.post_id: post for post in captured.posts}
    if from_id not in captured_by:
        raise SystemExit(f"reply node {from_id} missing from capture")

    children: dict[str, list[str]] = {
        post.post_id: [] for post in captured.posts
    }
    for post in captured.posts:
        if post.reply_to_id in captured_by:
            children[post.reply_to_id].append(post.post_id)

    subtree_ids: set[str] = set()
    stack = [from_id]
    while stack:
        post_id = stack.pop()
        if post_id in subtree_ids:
            continue
        subtree_ids.add(post_id)
        stack.extend(reversed(children.get(post_id, [])))

    leaves = tuple(
        post.post_id
        for post in captured.posts
        if post.post_id in subtree_ids
        and not any(
            child_id in subtree_ids
            for child_id in children.get(post.post_id, [])
        )
    )

    existing_ids = {post.post_id for post in existing.posts}
    attachment_ids: set[str] = set()
    attachment_seen: set[str] = set()
    current = from_id
    while current not in existing_ids:
        if current in attachment_seen:
            raise SystemExit(
                f"reply node {from_id} does not attach to existing thread"
            )
        attachment_seen.add(current)
        post = captured_by.get(current)
        if post is None:
            raise SystemExit(
                f"reply node {from_id} does not attach to existing thread"
            )
        attachment_ids.add(current)
        if post.reply_to_id is None:
            raise SystemExit(
                f"reply node {from_id} does not attach to existing thread"
            )
        current = post.reply_to_id

    selected_ids = subtree_ids | attachment_ids
    selected = tuple(
        post for post in captured.posts if post.post_id in selected_ids
    )
    return selected, leaves


def _merge_branch_posts(
    existing: ThreadData,
    groups: list[tuple[PostData, ...]],
) -> tuple[ThreadData, tuple[str, ...]]:
    """Append previously absent selected posts without replacing old data."""
    posts = list(existing.posts)
    seen = {post.post_id for post in posts}
    added: list[str] = []
    for group in groups:
        for post in group:
            if post.post_id in seen:
                continue
            seen.add(post.post_id)
            posts.append(post)
            added.append(post.post_id)
    return (
        ThreadData(
            root_post_id=existing.root_post_id,
            posts=tuple(posts),
            source_url=existing.source_url,
        ),
        tuple(added),
    )


def _merge_existing_capture(
    fresh: ThreadData,
    existing: ThreadData,
    tip_id: str,
) -> tuple[ThreadData, tuple[str, ...]]:
    """Keep fresh post data while retaining archived posts it omitted."""
    if tip_id not in {post.post_id for post in fresh.posts}:
        raise SystemExit(f"spine tip {tip_id} missing from fresh capture")
    fresh_ids = {post.post_id for post in fresh.posts}
    existing_ids = {post.post_id for post in existing.posts}
    if fresh_ids.isdisjoint(existing_ids):
        raise SystemExit("fresh and existing captures are a different conversation")
    return _merge_branch_posts(fresh, [existing.posts])


def _copy_selected_media(
    source: Path,
    destination: Path,
    post_ids: set[str],
) -> tuple[Path, ...]:
    """Copy media whose filename begins with a selected post id."""
    source_media = source / "media"
    destination_media = destination / "media"
    if not source_media.is_dir() or not post_ids:
        return ()
    if source_media.resolve() == destination_media.resolve():
        return ()
    prefixes = tuple(f"{post_id}_" for post_id in sorted(post_ids))
    destination_media.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for path in sorted(source_media.iterdir()):
        if not path.is_file() or not path.name.startswith(prefixes):
            continue
        output = destination_media / path.name
        shutil.copy2(path, output)
        copied.append(output)
    return tuple(copied)


def _write_thread(path: Path, thread: ThreadData) -> None:
    """Atomically write one typed thread to scratch JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(path.suffix + ".part")
    partial.write_text(
        json.dumps(asdict(thread), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    partial.replace(path)


def cmd_refetch(args: argparse.Namespace) -> int:
    """Capture one spine tip plus explicit branch tips into one dump."""
    post_id = args.id
    capture_ids = _capture_ids(post_id, args.branch)
    for capture_id in capture_ids:
        check_frozen(capture_id)
    if not COOKIES.is_file():
        raise SystemExit(f"missing {COOKIES}")

    out = scratch_dir(post_id)
    out.mkdir(parents=True, exist_ok=True)
    capture_paths: list[Path] = []
    for capture_id in capture_ids:
        capture = out / f"gallery_{capture_id}.json"
        url = f"https://x.com/i/status/{capture_id}"
        with capture.open("w", encoding="utf-8") as fh:
            subprocess.check_call(
                [*_gallery_base_args(), "--dump-json", url],
                stdout=fh,
            )
        capture_paths.append(capture)

    gallery = out / "gallery.json"
    _merge_gallery_files(capture_paths, gallery)
    source_url = f"https://x.com/i/status/{post_id}"
    run(
        [
            sys.executable,
            str(HERE / "ingest_gallery.py"),
            "--json",
            str(gallery),
            "--out",
            str(out / "thread_data.json"),
            "--source-url",
            source_url,
            "--root",
            post_id,
        ]
    )
    _validate_capture_ids(out / "thread_data.json", capture_ids)

    media = out / "media"
    media.mkdir(parents=True, exist_ok=True)
    for capture_id in capture_ids:
        url = f"https://x.com/i/status/{capture_id}"
        run([*_gallery_base_args(), "-D", str(media), url])

    print(f"refetch -> {out}")
    return 0


def cmd_add_branch(args: argparse.Namespace) -> int:
    """Merge visible reply subtrees into an existing emitted thread."""
    post_id = args.id
    check_frozen(post_id)
    assets, notes = locate(post_id)
    if assets is None or notes is None:
        raise SystemExit(f"no emitted thread for {post_id} — refresh first")
    existing_path = assets / "thread_data.json"
    if not existing_path.is_file():
        raise SystemExit(f"missing {existing_path}")
    existing = load_thread(existing_path)
    if existing.root_post_id != post_id:
        raise SystemExit(
            f"{post_id} is not the stored spine tip {existing.root_post_id}"
        )
    if post_id not in {post.post_id for post in existing.posts}:
        raise SystemExit(f"spine tip {post_id} not present in existing thread")

    from_ids = tuple(dict.fromkeys(args.from_ids))
    selected_groups: list[tuple[PostData, ...]] = []
    capture_sources: list[tuple[Path, tuple[PostData, ...]]] = []
    leaf_groups: list[tuple[str, tuple[str, ...]]] = []
    for from_id in from_ids:
        cmd_refetch(argparse.Namespace(id=from_id, branch=[]))
        capture_dir = scratch_dir(from_id)
        captured = load_thread(capture_dir / "thread_data.json")
        selected, leaves = _select_branch_capture(existing, captured, from_id)
        selected_groups.append(selected)
        capture_sources.append((capture_dir, selected))
        leaf_groups.append((from_id, leaves))

    merged, added_ids = _merge_branch_posts(existing, selected_groups)
    added_set = set(added_ids)
    output_dir = scratch_dir(post_id)
    for capture_dir, selected in capture_sources:
        selected_added = {
            post.post_id for post in selected if post.post_id in added_set
        }
        _copy_selected_media(capture_dir, output_dir, selected_added)
    _write_thread(output_dir / "thread_data.json", merged)
    cmd_emit(argparse.Namespace(
        id=post_id,
        tip=True,
        slug=None,
        preserve_existing=False,
    ))

    added_text = ",".join(added_ids) if added_ids else "-"
    leaf_text = ";".join(
        f"{from_id}:{','.join(leaves) if leaves else '-'}"
        for from_id, leaves in leaf_groups
    )
    print(f"add-branch added={added_text} visible_leaves={leaf_text}")
    return 0


def cmd_emit(args: argparse.Namespace) -> int:
    """Run ``emit_archive.py`` for ``args.id`` and merge non-orig rows back into every per-author asset dir."""
    post_id = args.id
    tip = args.tip
    slug = args.slug
    check_frozen(post_id)
    src = scratch_dir(post_id)
    if not (src / "thread_data.json").is_file():
        src = dump_dir(post_id)
    if not (src / "thread_data.json").is_file():
        raise SystemExit(f"no thread_data.json for {post_id}")
    if args.preserve_existing:
        assets, _notes = locate(post_id)
        if assets is None:
            raise SystemExit(f"no existing emitted thread for {post_id}")
        existing_path = assets / "thread_data.json"
        if not existing_path.is_file():
            raise SystemExit(f"missing {existing_path}")
        fresh = load_thread(src / "thread_data.json")
        existing = load_thread(existing_path)
        merged, retained_ids = _merge_existing_capture(
            fresh,
            existing,
            post_id,
        )
        _write_thread(src / "thread_data.json", merged)
        retained = ",".join(retained_ids) if retained_ids else "-"
        print(f"preserve-existing retained={retained}")
    cmd = [
        sys.executable,
        str(HERE / "emit_archive.py"),
        "--input",
        str(src),
        "--vault",
        str(VAULT),
        "--force",
    ]
    if tip:
        cmd.extend(["--tip", post_id])
    if slug:
        cmd.extend(["--slug", slug])
    for raw in getattr(args, "attach", []) or []:
        cmd.extend(["--attach", raw])
    if getattr(args, "allow_broken_walk", False):
        cmd.append("--allow-broken-walk")
    if getattr(args, "retire_old_dir", False):
        cmd.append("--retire-old-dir")
    run(cmd)
    # Cross-author threads emit one asset dir per author. The tip's
    # post_id is only in the tip's author's asset dir; the other
    # authors' per-author dirs are missed by a tip-only lookup.
    # Iterate every post in the source dump and union the matches.
    seen: set[Path] = set()
    try:
        thread_data = json.loads(
            (src / "thread_data.json").read_text(encoding="utf-8")
        )
        post_ids = {
            str(p.get("post_id"))
            for p in thread_data.get("posts") or []
        }
    except (json.JSONDecodeError, OSError):
        post_ids = {post_id}
    for pid in post_ids:
        for asset_dir, _ in locate_all(pid):
            if asset_dir in seen:
                continue
            seen.add(asset_dir)
            run(
                [
                    sys.executable,
                    str(HERE / "media_merge.py"),
                    "--thread",
                    str(asset_dir),
                ]
            )
    return 0


def cmd_lift(args: argparse.Namespace) -> int:
    """Retired. Point the operator at ``fallback``."""
    del args
    raise SystemExit(
        "lift is retired; use fallback --confirm-origin-unavailable"
    )


def cmd_ocr(args: argparse.Namespace) -> int:
    """OCR every ``*_orig.{png,jpg}`` in the thread assets dir and write matching ``*_ocr.txt`` files."""
    post_id = args.id
    engine = args.engine
    assets, _notes = locate(post_id)
    if assets is None:
        raise SystemExit(f"no assets thread for {post_id}")
    media_json = assets / "media.json"
    n = 0
    for png in sorted(assets.glob("*_orig.png")) + sorted(assets.glob("*_orig.jpg")):
        dest = png.with_name(png.name.replace("_orig.png", "_ocr.txt").replace("_orig.jpg", "_ocr.txt"))
        run(
            [
                sys.executable,
                str(HERE / "ocr_pass.py"),
                "--in",
                str(png),
                "--out",
                str(dest),
                "--engine",
                engine,
                "--media-json",
                str(media_json),
            ]
        )
        n += 1
    print(f"ocr files {n}")
    return 0


def cmd_merge(args: argparse.Namespace) -> int:
    """Run ``media_merge.py`` for ``args.id`` to restore non-orig rows after an ``emit --force``."""
    post_id = args.id
    check_frozen(post_id)
    assets, _notes = locate(post_id)
    if assets is None:
        raise SystemExit(f"no assets thread for {post_id}")
    run([sys.executable, str(HERE / "media_merge.py"), "--thread", str(assets)])
    return 0


def overlay_quote_of_ids(current: ThreadData, previous: ThreadData) -> ThreadData:
    """Keep previous ``quote_of_id`` when the current post has none."""
    prev_by = {post.post_id: post for post in previous.posts}
    posts: list[PostData] = []
    for post in current.posts:
        old = prev_by.get(post.post_id)
        if (not post.quote_of_id) and old is not None and old.quote_of_id:
            post = replace(post, quote_of_id=old.quote_of_id)
        posts.append(post)
    return replace(current, posts=tuple(posts))


def chase_spine_quotes(
    thread: ThreadData,
    *,
    tip: bool,
    tip_id: str,
) -> None:
    """Refresh each missing spine ``quote_of_id`` as a root. One hop."""
    spine = spine_from_tip(thread, tip_id) if tip else spine_ids(thread)
    for qid in spine_quote_ids(thread, spine):
        assets, _notes = locate(qid)
        if assets is not None:
            continue
        try:
            check_frozen(qid)
        except SystemExit:
            continue
        inner = argparse.Namespace(
            id=qid,
            branch=[],
            tip=False,
            slug=None,
            preserve_existing=False,
            attach=[],
            allow_broken_walk=False,
            retire_old_dir=False,
            no_quotes=True,
        )
        try:
            cmd_refresh(inner)
        except (SystemExit, subprocess.CalledProcessError) as exc:
            print(f"quote-capture failed {qid}: {exc}")


def cmd_refresh(args: argparse.Namespace) -> int:
    """Convenience: ``refetch`` + quote chase + ``graph`` + ``emit --force``."""
    check_frozen(args.id)
    cmd_refetch(args)
    src = scratch_dir(args.id) / "thread_data.json"
    if getattr(args, "preserve_existing", False):
        assets, _notes = locate(args.id)
        if assets is not None and (assets / "thread_data.json").is_file():
            fresh = load_thread(src)
            existing = load_thread(assets / "thread_data.json")
            merged, retained_ids = _merge_existing_capture(
                fresh,
                existing,
                args.id,
            )
            _write_thread(src, merged)
            retained = ",".join(retained_ids) if retained_ids else "-"
            print(f"preserve-existing retained={retained}")
    assets, _notes = locate(args.id)
    if (
        assets is not None
        and (assets / "thread_data.json").is_file()
        and src.is_file()
    ):
        current = load_thread(src)
        previous = load_thread(assets / "thread_data.json")
        _write_thread(src, overlay_quote_of_ids(current, previous))
    cmd_graph(args)
    if not getattr(args, "no_quotes", False) and src.is_file():
        chase_spine_quotes(
            load_thread(src),
            tip=bool(getattr(args, "tip", False)),
            tip_id=args.id,
        )
    cmd_emit(args)
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    """Rebuild handle-index wikilinks from actual folder listing.

    Use after manual edits or a stale state. Idempotent.
    """
    handle = args.handle
    root = VAULT / "archive" / "threads"
    targets = [root / handle] if handle else None
    changed = 0
    skipped = 0
    for handle_dir in targets or sorted(root.iterdir()):
        if not handle_dir.is_dir() or handle_dir.name.startswith("."):
            continue
        idx = handle_dir / "index.md"
        if not idx.is_file():
            continue
        text = idx.read_text(encoding="utf-8")
        end = text.find("\n---", 3)
        if end < 0:
            # Frontmatter isn't closed — fall back to a fresh one rather
            # than silently skipping.
            fm = (
                f"---\n"
                f"title: {handle_dir.name}\n"
                f"type: note\n"
                f"draft: false\n"
                f"description: Archived threads by {handle_dir.name}.\n"
                f"tags:\n"
                f"  - archive\n"
                f"  - twitter\n"
                f"  - {handle_dir.name}\n"
                f"---\n"
            )
            skipped += 1
            print(f"rebuilt frontmatter for {handle_dir.name}")
        else:
            fm = text[: end + 4]
        dirs = sorted(d.name for d in handle_dir.iterdir() if d.is_dir())
        links = "\n".join(f"- [[archive/threads/{handle_dir.name}/{d}]]" for d in dirs)
        new = fm + "\n\n" + links + "\n"
        if new != text:
            idx.write_text(new, encoding="utf-8", newline="\n")
            changed += 1
            print(f"rewrote {handle_dir.name}: {len(dirs)} dirs")
        else:
            print(f"ok {handle_dir.name}: {len(dirs)} dirs")
    print(f"changed {changed}, skipped {skipped}")
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    """Flip ``draft: true`` to ``draft: false`` on the thread index (no-op if already published)."""
    post_id = args.id
    check_frozen(post_id)
    _assets, notes = locate(post_id)
    if notes is None:
        raise SystemExit(f"no vault thread for {post_id}")
    path = notes / "index.md"
    if not path.is_file():
        raise SystemExit(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    new = text
    new = new.replace("draft: true", "draft: false")
    new = new.replace("status: draft", "status: published")
    if "draft: false" not in new:
        raise SystemExit(f"no draft field in {path}")
    if new == text:
        print(f"already published {path}")
        return 0
    path.write_text(new, encoding="utf-8", newline="\n")
    print(f"draft: false -> {path}")
    return 0


def _now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def cmd_migrate_media(args: argparse.Namespace) -> int:
    """Dispatch the per-thread ``migrate_legacy_thread`` (dry-run by default; ``--apply`` to write)."""
    if bool(args.id) == bool(args.all_root):
        raise SystemExit("migrate-media requires exactly one of --id or --all")
    if args.id:
        asset = DUMPS / args.id / "thread_data.json"
        if not asset.is_file():
            scratch = SCRATCH / f"refetch_{args.id}"
            if not (scratch / "thread_data.json").is_file():
                raise SystemExit(f"no thread_data.json for {args.id}")
        assets, note_dir = locate(args.id)
        if assets is None or note_dir is None:
            raise SystemExit(f"no vault thread for {args.id}")
        check_frozen(args.id)
        result = migrate_legacy_thread(assets, note_dir, now=_now_iso(), apply=args.apply)
        print(result)
        return 0 if result.state != "blocked" else 2
    if not args.apply:
        print("dry-run: explicit --apply required to write")
        return 0
    print("corpus-wide migrate-media --apply is not implemented")
    return 0


def cmd_audit_media(args: argparse.Namespace) -> int:
    """Run ``audit_thread`` for ``args.id`` and print issues (non-zero exit if any found)."""
    assets, note_dir = locate(args.id)
    if assets is None or note_dir is None:
        raise SystemExit(f"no vault thread for {args.id}")
    report = audit_thread(assets, note_dir, load_frozen_ids(FROZEN))
    if report.issues:
        for issue in report.issues:
            print(issue)
        return 1
    print("audit ok")
    return 0


def cmd_backup(args: argparse.Namespace) -> int:
    """Mirror ``args.id``'s asset dir into the configured destination via ``backup_thread``."""
    check_frozen(args.id)
    assets, note_dir = locate(args.id)
    if assets is None or note_dir is None:
        raise SystemExit(f"no vault thread for {args.id}")
    destination_root = load_destination_root(VAULT, args.destination)
    result = backup_thread(
        assets,
        assets_root=VAULT / "assets" / "threads",
        destination_root=destination_root,
        destination_id=args.destination,
        now=_now_iso(),
        require_destination_root=True,
    )
    print(result.state)
    if result.error:
        print(result.error)
    return 0 if result.state == "synced" else 2


def cmd_fallback(args: argparse.Namespace) -> int:
    """Upload (or reuse) a fallback for ``args.id``/``args.media_id`` and rewrite the note references."""
    if not args.confirm_origin_unavailable:
        raise SystemExit("fallback requires --confirm-origin-unavailable")
    check_frozen(args.id)
    assets, note_dir = locate(args.id)
    if assets is None or note_dir is None:
        raise SystemExit(f"no vault thread for {args.id}")
    userhash = load_userhash(VAULT)
    assets_root = VAULT / "assets" / "threads"

    def _upload(path: Path) -> str:
        return upload_file(path, userhash)

    def _lookup(provider: str, content_hash: str) -> str | None:
        return find_existing_fallback(assets_root, provider, content_hash)

    result = activate_fallback(
        assets,
        note_dir,
        media_id=args.media_id,
        role=args.role,
        provider=args.provider,
        confirm_origin_unavailable=True,
        now=_now_iso(),
        upload=_upload,
        lookup=_lookup,
    )
    print(result)
    return 0


def cmd_restore_origin(args: argparse.Namespace) -> int:
    """Switch ``args.id``/``args.media_id`` back to the original X URL and rewrite the note references."""
    check_frozen(args.id)
    assets, note_dir = locate(args.id)
    if assets is None or note_dir is None:
        raise SystemExit(f"no vault thread for {args.id}")
    restore_origin(assets, note_dir, media_id=args.media_id, now=_now_iso())
    print("restored origin")
    return 0


def cmd_reslug(args: argparse.Namespace) -> int:
    """Audit or apply the one-time corpus-wide thread-directory rename."""
    plan = plan_reslug(VAULT, load_frozen_ids(FROZEN))
    print(format_reslug_plan(plan), end="")
    if plan.conflicts:
        return 2
    if not args.apply:
        print("dry-run: explicit --apply required to write")
        return 0
    apply_reslug_plan(plan, SCRATCH)
    return 0


def cmd_relabel(args: argparse.Namespace) -> int:
    """Patch ``**N/**`` lines from on-disk JSON. Notes only."""
    if not args.all_threads:
        raise SystemExit("relabel requires --all")
    plan = plan_relabel(VAULT)
    print(format_relabel_plan(plan), end="")
    conflicts = any(item.state == "conflict" for item in plan.items)
    if not args.apply:
        return 2 if conflicts else 0
    apply_relabel(plan)
    return 2 if conflicts else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in (
        "locate",
        "graph",
        "refetch",
        "emit",
        "lift",
        "ocr",
        "merge",
        "refresh",
        "publish",
    ):
        p = sub.add_parser(name)
        p.add_argument("--id", required=True)
        if name in ("refetch", "refresh"):
            p.add_argument(
                "--branch",
                action="append",
                default=[],
                metavar="TIP_ID",
                help="capture and merge this explicit branch tip; repeatable",
            )
        if name in ("emit", "refresh"):
            p.add_argument("--tip", action="store_true", help="use --id as tip")
            p.add_argument("--slug", default=None)
            p.add_argument(
                "--preserve-existing",
                action="store_true",
                help="retain archived posts omitted by the fresh capture",
            )
            p.add_argument(
                "--attach",
                action="append",
                default=[],
                metavar="CHILD:PARENT",
                help="set child.reply_to_id to parent before the spine walk",
            )
            p.add_argument(
                "--allow-broken-walk",
                action="store_true",
                help="emit even if the tip walk stops on a missing parent",
            )
            p.add_argument(
                "--retire-old-dir",
                action="store_true",
                help="delete this thread's archive under another handle",
            )
        if name == "refresh":
            p.add_argument(
                "--no-quotes",
                action="store_true",
                help="do not capture quoted tweets on the spine",
            )
        if name == "lift":
            p.add_argument("--orig", action="store_true")
        if name == "ocr":
            p.add_argument(
                "--engine",
                default="umi",
                choices=("auto", "umi", "tesseract", "windows"),
            )
    sync = sub.add_parser(
        "sync", help="rebuild handle-index wikilinks from actual folder listing"
    )
    sync.add_argument("--handle", default=None, help="single handle, else all")

    migrate = sub.add_parser(
        "migrate-media", help="convert legacy media.json to canonical locations"
    )
    migrate.add_argument("--id", default=None)
    migrate.add_argument("--all", dest="all_root", action="store_true")
    migrate.add_argument("--apply", action="store_true")

    audit = sub.add_parser(
        "audit-media", help="local integrity and reference check"
    )
    audit.add_argument("--id", required=True)
    audit.add_argument("--check-origin", action="store_true")
    audit.add_argument("--record-checks", action="store_true")

    backup_p = sub.add_parser(
        "backup", help="sparse, hash-verified copy of one thread asset dir"
    )
    backup_p.add_argument("--id", required=True)
    backup_p.add_argument("--destination", default="cozy")

    fallback = sub.add_parser(
        "fallback", help="upload one confirmed fallback host selection"
    )
    fallback.add_argument("--id", required=True)
    fallback.add_argument("--media-id", required=True)
    fallback.add_argument("--role", default="orig")
    fallback.add_argument(
        "--provider", default="catbox", choices=("catbox",)
    )
    fallback.add_argument(
        "--confirm-origin-unavailable", action="store_true"
    )

    restore = sub.add_parser(
        "restore-origin", help="select the immutable origin again"
    )
    restore.add_argument("--id", required=True)
    restore.add_argument("--media-id", required=True)

    add_branch = sub.add_parser(
        "add-branch",
        help="merge visible reply subtrees into an existing emitted thread",
    )
    add_branch.add_argument("--id", required=True)
    add_branch.add_argument(
        "--from",
        dest="from_ids",
        action="append",
        required=True,
        metavar="REPLY_ID",
        help="capture this reply node's visible subtree; repeatable",
    )

    reslug = sub.add_parser(
        "reslug",
        help="audit or apply canonical thread directory names",
    )
    reslug.add_argument("--all", dest="all_threads", action="store_true", required=True)
    reslug.add_argument("--apply", action="store_true")

    relabel = sub.add_parser(
        "relabel",
        help="patch **N/** lines with @handle from on-disk JSON",
    )
    relabel.add_argument("--all", dest="all_threads", action="store_true", required=True)
    relabel.add_argument("--apply", action="store_true")

    return parser


_COMMANDS: dict[str, Callable[[argparse.Namespace], int]] = {
    "locate": cmd_locate,
    "graph": cmd_graph,
    "refetch": cmd_refetch,
    "add-branch": cmd_add_branch,
    "emit": cmd_emit,
    "lift": cmd_lift,
    "ocr": cmd_ocr,
    "merge": cmd_merge,
    "refresh": cmd_refresh,
    "publish": cmd_publish,
    "sync": cmd_sync,
    "migrate-media": cmd_migrate_media,
    "audit-media": cmd_audit_media,
    "backup": cmd_backup,
    "fallback": cmd_fallback,
    "restore-origin": cmd_restore_origin,
    "reslug": cmd_reslug,
    "relabel": cmd_relabel,
}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = _COMMANDS[args.cmd]
    return handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
