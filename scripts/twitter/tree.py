"""Tree-walking helpers for thread spine and branch construction."""
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


def spine_from_tip(thread: ThreadData, tip_id: str) -> list[str]:
    """Walk back from `tip_id` through `reply_to_id` to the OP (the
    post with `reply_to_id == None` or a missing parent). Returns
    all post ids on the linear chain in chronological order: OP at
    index 0, tip at last.

    The walk crosses handle boundaries. For a chain that alternates
    authors, every post is included. The archive dir for the
    thread is owned by the OP at index 0.
    """
    ids = by_id(thread)
    if tip_id not in ids:
        raise ValueError(f"tip {tip_id} not in dump")
    chain = [tip_id]
    cur = tip_id
    while True:
        parent = ids[cur].reply_to_id
        if not parent or parent not in ids:
            break
        chain.append(parent)
        cur = parent
    chain.reverse()
    return chain


def spine_ids(thread: ThreadData) -> list[str]:
    """Walk the linear reply chain from the OP (the post with
    `reply_to_id == None`) down through `children_map`, picking the
    first child at each level (already sorted by `(timestamp,
    post_id)`).

    The walk crosses handle boundaries. For a chain that alternates
    authors (e.g., rianflo ↔ NOTimothyLottes), every post on the
    chain is included. The archive dir for the thread is owned by
    the OP — the first post in the returned list.

    If no post has `reply_to_id == None`, the first post in
    `thread.posts` is used as a fallback start.
    """
    ids = by_id(thread)
    kids = children_map(thread)
    ops = [p.post_id for p in thread.posts if p.reply_to_id is None]
    if ops:
        start = ops[0]
    else:
        start = thread.posts[0].post_id
    out = [start]
    cur = start
    while True:
        children = kids.get(cur, [])
        if not children:
            break
        cur = children[0]
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
