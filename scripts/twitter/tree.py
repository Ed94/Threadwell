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
    """Walk the OP's own chain down through `children_map`.

    At each level, prefer a same-handle child (to continue the OP's
    own chain) over any child. Fall back to the earliest child when
    no same-handle child exists.

    The OP is the post with `reply_to_id == None`. The returned
    list is the OP's chain: the OP at index 0, then same-author
    replies in chronological order. Cross-author replies to spine
    posts are branches (rendered as separate files by the emit).

    For a thread where the OP has no self-replies but cross-author
    replies (e.g., a post that attracted only outside replies), the
    walker picks the earliest child to start a chain — that branch
    becomes the only spine entry after the OP, and any other
    children of the OP become branches.
    """
    ids = by_id(thread)
    kids = children_map(thread)
    ops = [p.post_id for p in thread.posts if p.reply_to_id is None]
    if ops:
        start = ops[0]
    else:
        start = thread.posts[0].post_id
    handle = ids[start].handle
    out = [start]
    cur = start
    while True:
        children = kids.get(cur, [])
        if not children:
            break
        same = [c for c in children if ids[c].handle == handle]
        cur = same[0] if same else children[0]
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
