"""Print a tip-choice graph for a thread_data.json. No vault writes."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from twitter.models import PostData, ThreadData, load_thread
from twitter.paths import SCRATCH
from twitter.slug import slugify
from twitter.tree import branch_roots, by_id, children_map, descendants, spine_ids


def _one_line(text: str, n: int = 56) -> str:
    s = " ".join((text or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def _node(post: PostData) -> str:
    return f"[I:{post.handle}:{post.post_id}]"


def render_ssdl(thread: ThreadData) -> str:
    ids = by_id(thread)
    kids = children_map(thread)
    spine = spine_ids(thread)
    lines: list[str] = []
    lines.append("# SSDL (adapted): [I:handle:id] instruction, -> spine, => sibling fan-out")
    lines.append("# [B:…] branch root off the spine. [T] last spine post = default suggested_tip")
    spine_parts = [_node(ids[i]) for i in spine]
    lines.append("SPINE: " + " -> ".join(spine_parts) + " -> [T]")
    for sid in spine:
        off = [c for c in kids.get(sid, []) if c not in set(spine)]
        if not off:
            continue
        bits = []
        for cid in off:
            p = ids[cid]
            desc = descendants(cid, kids)
            extra = f" +{len(desc)}" if desc else ""
            bits.append(f"[B:{p.handle}:{p.post_id}{extra}]")
        lines.append(f"  fanout {sid}: " + " => ".join(bits))
    return "\n".join(lines)


def render_ascii(thread: ThreadData) -> str:
    ids = by_id(thread)
    kids = children_map(thread)
    spine = spine_ids(thread)
    spine_set = set(spine)
    roots = branch_roots(thread, spine)
    lines: list[str] = []
    lines.append("# ASCII tree  time  handle  id  slug  first-line")
    lines.append(f"# dump_root={thread.root_post_id}  suggested_tip={spine[-1]}  posts={len(thread.posts)}")
    lines.append(f"# source={thread.source_url}")

    def walk(pid: str, prefix: str, is_last: bool, on_spine: bool) -> None:
        p = ids[pid]
        mark = "S" if pid in spine_set else ("B" if pid in roots else " ")
        branch = "└─" if is_last else "├─"
        slug = slugify(p.text)
        lines.append(
            f"{prefix}{branch}[{mark}] {p.timestamp}  @{p.handle}  {p.post_id}  {slug}"
        )
        lines.append(f"{prefix}{'    ' if is_last else '│   '}    {_one_line(p.text)}")
        childs = kids.get(pid, [])
        nxt = prefix + ("    " if is_last else "│   ")
        for i, c in enumerate(childs):
            walk(c, nxt, i == len(childs) - 1, c in spine_set)

    # forest: posts with no in-dump parent first
    tops = [p.post_id for p in thread.posts if not p.reply_to_id or p.reply_to_id not in ids]
    if thread.root_post_id in ids and thread.root_post_id not in tops:
        tops.insert(0, thread.root_post_id)
    seen: set[str] = set()
    ordered = []
    for t in tops:
        if t not in seen:
            ordered.append(t)
            seen.add(t)
    for i, t in enumerate(ordered):
        walk(t, "", i == len(ordered) - 1, t in spine_set)
    lines.append("")
    lines.append("# copy-paste ids")
    lines.append(f"SPINE_IDS={' '.join(spine)}")
    lines.append(f"SUGGESTED_TIP={spine[-1]}")
    lines.append("BRANCH_ROOTS=" + " ".join(roots))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dry-run thread graph for tip choice.")
    parser.add_argument("--input", type=Path, required=True, help="dump dir or thread_data.json")
    args = parser.parse_args(argv)
    path = args.input
    if path.is_dir():
        path = path / "thread_data.json"
    thread = load_thread(path)
    text = render_ssdl(thread) + "\n\n" + render_ascii(thread) + "\n"
    out = args.input if args.input.is_dir() else args.input.parent
    dest = SCRATCH / f"graph_{thread.root_post_id}.txt"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    sys.stdout.buffer.write((str(dest) + "\n").encode("ascii", "replace"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
