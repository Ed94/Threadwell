"""Front door for common Twitter archive ops.

  python C:\\projects\\Threadwell\\scripts\\twitter\\tw.py graph --id 1692565070583136348
  python C:\\projects\\Threadwell\\scripts\\twitter\\tw.py refresh --id 1692565070583136348 --tip
  python C:\\projects\\Threadwell\\scripts\\twitter\\tw.py lift --id 1692565070583136348 --orig
  python C:\\projects\\Threadwell\\scripts\\twitter\\tw.py ocr --id 1692565070583136348
  python C:\\projects\\Threadwell\\scripts\\twitter\\tw.py locate --id 1692565070583136348

refresh = refetch + emit --force (--tip uses the --id as tip).
Does not commit. Does not flip draft. Never prints cookies or userhash.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = Path(r"C:\projects\Threadwell")
DUMPS = Path(r"C:\projects\manual_slop\docs\twitter")
SCRATCH = Path(r"C:\projects\Threadwell-ai\scratch")
COOKIES = VAULT / "secrets" / "twitter_cookies.txt"
FROZEN = HERE / "do_not_refetch.txt"


def frozen_ids() -> set[str]:
    out: set[str] = set()
    if not FROZEN.is_file():
        return out
    for line in FROZEN.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            out.add(s)
    return out


def check_frozen(post_id: str) -> None:
    if post_id in frozen_ids():
        raise SystemExit(f"frozen Onat dump {post_id} — will not refetch/overwrite")


def dump_dir(post_id: str) -> Path:
    return DUMPS / post_id


def scratch_dir(post_id: str) -> Path:
    return SCRATCH / f"refetch_{post_id}"


def locate(post_id: str) -> tuple[Path | None, Path | None]:
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


def run(cmd: list[str]) -> None:
    print(">", " ".join(cmd))
    subprocess.check_call(cmd)


def cmd_locate(post_id: str) -> int:
    dump = dump_dir(post_id)
    scratch = scratch_dir(post_id)
    assets, notes = locate(post_id)
    print(f"dump     {dump}  exists={dump.is_dir()}")
    print(f"scratch  {scratch}  exists={scratch.is_dir()}")
    print(f"assets   {assets}")
    print(f"notes    {notes}")
    return 0


def cmd_graph(post_id: str) -> int:
    src = scratch_dir(post_id)
    if not (src / "thread_data.json").is_file():
        src = dump_dir(post_id)
    if not (src / "thread_data.json").is_file():
        raise SystemExit(f"no thread_data.json for {post_id}")
    run([sys.executable, str(HERE / "graph_dry_run.py"), "--input", str(src)])
    return 0


def cmd_refetch(post_id: str) -> int:
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


def cmd_emit(post_id: str, tip: bool, slug: str | None) -> int:
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
    assets, _notes = locate(post_id)
    if assets is not None:
        run([sys.executable, str(HERE / "media_merge.py"), "--thread", str(assets)])
    return 0


def cmd_lift(post_id: str, orig: bool) -> int:
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


def cmd_ocr(post_id: str, engine: str) -> int:
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


def cmd_merge(post_id: str) -> int:
    assets, _notes = locate(post_id)
    if assets is None:
        raise SystemExit(f"no assets thread for {post_id}")
    run([sys.executable, str(HERE / "media_merge.py"), "--thread", str(assets)])
    return 0


def cmd_refresh(post_id: str, tip: bool, slug: str | None) -> int:
    cmd_refetch(post_id)
    cmd_graph(post_id)
    cmd_emit(post_id, tip=tip, slug=slug)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("locate", "graph", "refetch", "emit", "lift", "ocr", "merge", "refresh"):
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
    args = parser.parse_args(argv)
    post_id = args.id
    if args.cmd == "locate":
        return cmd_locate(post_id)
    if args.cmd == "graph":
        return cmd_graph(post_id)
    if args.cmd == "refetch":
        return cmd_refetch(post_id)
    if args.cmd == "emit":
        return cmd_emit(post_id, tip=args.tip, slug=args.slug)
    if args.cmd == "lift":
        return cmd_lift(post_id, orig=args.orig)
    if args.cmd == "ocr":
        return cmd_ocr(post_id, engine=args.engine)
    if args.cmd == "merge":
        return cmd_merge(post_id)
    if args.cmd == "refresh":
        return cmd_refresh(post_id, tip=args.tip, slug=args.slug)
    raise SystemExit(f"unknown {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
