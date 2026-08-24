"""Front door for common Twitter archive ops.

From the vault root:

  python scripts/twitter/tw.py graph --id 1692565070583136348
  python scripts/twitter/tw.py refresh --id 1692565070583136348 --tip
  python scripts/twitter/tw.py lift --id 1692565070583136348 --orig
  python scripts/twitter/tw.py ocr --id 1692565070583136348
  python scripts/twitter/tw.py locate --id 1692565070583136348

refresh = refetch + emit --force (--tip uses the --id as tip).
publish = draft: false on the thread index (the only switch).
Does not commit. Never prints cookies or userhash.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path

_HERE: Path = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from paths import COOKIES, DUMPS, FROZEN, HERE, SCRATCH, VAULT

try:
    from frozen import frozen_match, load_frozen_ids, require_writable
    from backup_assets import backup_thread, load_destination_root
    from catbox_client import load_userhash, upload_file
    from fallback_media import activate_fallback, find_existing_fallback, restore_origin
    from media_audit import audit_thread
    from media_migrate import migrate_legacy_thread
except ImportError:  # pragma: no cover - script-mode import
    from frozen import frozen_match, load_frozen_ids, require_writable
    from backup_assets import backup_thread, load_destination_root
    from catbox_client import load_userhash, upload_file
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


def cmd_refetch(args: argparse.Namespace) -> int:
    """gallery-dl a thread into the scratch dir, then run ``ingest_gallery.py`` to materialize thread_data.json."""
    post_id = args.id
    check_frozen(post_id)
    if not COOKIES.is_file():
        raise SystemExit(f"missing {COOKIES}")
    out = scratch_dir(post_id)
    media = out / "media"
    media.mkdir(parents=True, exist_ok=True)
    url = f"https://x.com/i/status/{post_id}"
    gallery = out / "gallery.json"
    with gallery.open("w", encoding="utf-8") as fh:
        subprocess.check_call(
            [
                "gallery-dl",
                "--cookies",
                str(COOKIES),
                "--dump-json",
                "-o",
                "text-tweets=true",
                "-o",
                "conversations=true",
                url,
            ],
            stdout=fh,
        )
    run(
        [
            "gallery-dl",
            "--cookies",
            str(COOKIES),
            "-D",
            str(media),
            "-o",
            "text-tweets=true",
            "-o",
            "conversations=true",
            url,
        ]
    )
    run(
        [
            sys.executable,
            str(HERE / "ingest_gallery.py"),
            "--json",
            str(gallery),
            "--out",
            str(out / "thread_data.json"),
            "--source-url",
            url,
            "--root",
            post_id,
        ]
    )
    print(f"refetch -> {out}")
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
    """Invoke ``lift_catbox.py`` to swap fallback URLs into the notes for ``args.id`` (with ``--orig`` to restore)."""
    post_id = args.id
    orig = args.orig
    assets, notes = locate(post_id)
    if assets is None or notes is None:
        raise SystemExit(f"no vault thread for {post_id} — emit first")
    cmd = [
        sys.executable,
        str(HERE / "lift_catbox.py"),
        "--thread",
        str(assets),
        "--notes",
        str(notes),
    ]
    if orig:
        cmd.append("--orig")
    run(cmd)
    return 0


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


def cmd_refresh(args: argparse.Namespace) -> int:
    """Convenience: ``refetch`` + ``graph`` + ``emit --force`` for ``args.id``."""
    check_frozen(args.id)
    cmd_refetch(args)
    cmd_graph(args)
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
    print("corpus migrate-media --apply not yet implemented; awaiting Task 11")
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
    print(result)
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
        if name in ("emit", "refresh"):
            p.add_argument("--tip", action="store_true", help="use --id as tip")
            p.add_argument("--slug", default=None)
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

    return parser


_COMMANDS: dict[str, Callable[[argparse.Namespace], int]] = {
    "locate": cmd_locate,
    "graph": cmd_graph,
    "refetch": cmd_refetch,
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
}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = _COMMANDS[args.cmd]
    return handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
