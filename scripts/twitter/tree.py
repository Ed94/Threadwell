from __future__ import annotations

from .models import ThreadData, PostData


def by_id(thread: ThreadData) -> dict[str, PostData]:
    return {p.post_id: p for p in thread.posts}


def children_map(thread: ThreadData) -> dict[str, list[str]]:
    ids = by_id(thread)
    kids: dict[str, list[str]] = {p.post_id: [] for p in thread.posts}
    for p in thread.posts:
        if p.reply_to_id and p.reply_to_id in ids:
            kids[p.reply_to_id].append(p.post_id)
    for parent, lst in kids.items():
        lst.sort(key=lambda i: (ids[i].timestamp, ids[i].post_id))
    return kids


def spine_ids(thread: ThreadData) -> list[str]:
    ids = by_id(thread)
    kids = children_map(thread)
    start = thread.root_post_id if thread.root_post_id in ids else thread.posts[0].post_id
    handle = ids[start].handle
    out = [start]
    cur = start
    while True:
        same = [c for c in kids[cur] if ids[c].handle == handle]
        if not same:
            break
        cur = same[0]
        out.append(cur)
    return out


def branch_roots(thread: ThreadData, spine: list[str]) -> list[str]:
    spine_set = set(spine)
    ids = by_id(thread)
    roots: list[str] = []
    for p in thread.posts:
        if p.post_id in spine_set:
            continue
        parent_on_spine = p.reply_to_id in spine_set
        parent_missing = p.reply_to_id is not None and p.reply_to_id not in ids
        if parent_on_spine or parent_missing:
            roots.append(p.post_id)
    roots.sort(key=lambda i: (ids[i].timestamp, ids[i].post_id))
    return roots


def descendants(start_id: str, kids: dict[str, list[str]]) -> list[str]:
    out: list[str] = []
    stack = list(reversed(kids.get(start_id, [])))
    while stack:
        n = stack.pop()
        out.append(n)
        stack.extend(reversed(kids.get(n, [])))
    return out
