from __future__ import annotations
import re

_MENTION = re.compile(r"^(@[A-Za-z0-9_]+(\s+|$))+")
_APOS = re.compile(r"['\u2019\u2018]")
_NON_SLUG = re.compile(r"[^a-z0-9]+")

def date_prefix(timestamp: str) -> str:
    if len(timestamp) >= 10 and timestamp[4] == "-" and timestamp[7] == "-":
        return timestamp[:10]
    return "unknown-date"

def slugify(text: str, max_len: int = 50) -> str:
    s = _MENTION.sub("", (text or "").strip()).lower()
    s = _APOS.sub("", s)
    s = _NON_SLUG.sub("-", s).strip("-")
    if not s:
        return "thread"
    if len(s) <= max_len:
        return s
    cut = s[:max_len]
    if cut.endswith("-"):
        return cut.rstrip("-")
    cut = cut.rstrip("-")
    if "-" in cut:
        cut = cut.rsplit("-", 1)[0]
    return cut or s[:max_len]

def thread_dir_name(date: str, first_spine_line: str, override: str | None) -> str:
    slug = override.strip() if override else slugify(first_spine_line)
    return f"{date}-{slug}"

def branch_file_name(date: str, handle: str, first_line: str) -> str:
    return f"{date}-{handle}-{slugify(first_line)}.md"
