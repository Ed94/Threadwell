from __future__ import annotations

import os
import re
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path


MEDIA_LINE = re.compile(r"(?m)^Media \(not lifted\):\s*(?P<body>.+?)\s*$")
BACKTICK = re.compile(r"`([^`]+)`")
IMAGE_LINE = re.compile(r"(?m)^!\[[^\]]*\]\((?P<url>https://[^)]+)\)\s*$")


@dataclass(frozen=True)
class FileRewrite:
    path: Path
    before: str
    after: str


@dataclass(frozen=True)
class RewritePlan:
    files: tuple[FileRewrite, ...]
    issues: tuple[str, ...]


def remote_markup(url: str) -> str:
    path = url.split("?", 1)[0].lower()
    if path.endswith(".mp4") or "video.twimg.com" in url:
        return f'<video controls src="{url}"></video>'
    return f"![]({url})"


def _fallback_urls(text: str) -> list[str]:
    return [
        match.group("url")
        for match in IMAGE_LINE.finditer(text)
        if "files.catbox.moe" in match.group("url")
    ]


def plan_thread_rewrites(
    note_dir: Path,
    *,
    filename_origins: dict[str, str],
    fallback_origins: dict[str, list[str]],
) -> RewritePlan:
    paths = sorted(note_dir.glob("*.md"), key=lambda path: (path.name != "index.md", path.name))
    texts = {path: path.read_text(encoding="utf-8") for path in paths}
    fallback_counts = Counter(
        url for text in texts.values() for url in _fallback_urls(text)
    )
    fallback_files: dict[str, set[Path]] = {}
    for path, text in texts.items():
        for url in _fallback_urls(text):
            fallback_files.setdefault(url, set()).add(path)

    issues: list[str] = []
    for url, count in sorted(fallback_counts.items()):
        candidates = fallback_origins.get(url)
        if not candidates:
            issues.append(f"untracked fallback reference: {url}")
        elif len(candidates) != count:
            issues.append(f"fallback occurrence mismatch: {url} expected={len(candidates)} actual={count}")
        elif len(candidates) > 1 and len(fallback_files[url]) > 1:
            issues.append(f"fallback spans multiple notes: {url}")
    if issues:
        return RewritePlan((), tuple(issues))

    fallback_queues = {
        url: deque(origins) for url, origins in fallback_origins.items()
    }
    rewrites: list[FileRewrite] = []
    for path in paths:
        before = texts[path]

        def replace_media_line(match: re.Match[str], _path=path) -> str:
            names = BACKTICK.findall(match.group("body"))
            if not names:
                return match.group(0)
            urls: list[str] = []
            for name in names:
                origin = filename_origins.get(name)
                if origin is None:
                    issues.append(f"untracked local reference: {name}")
                    return match.group(0)
                urls.append(origin)
            return "\n\n".join(remote_markup(url) for url in urls)

        after = MEDIA_LINE.sub(replace_media_line, before)

        def replace_image_line(match: re.Match[str], _path=path) -> str:
            url = match.group("url")
            queue = fallback_queues.get(url)
            if not queue:
                return match.group(0)
            return remote_markup(queue.popleft())

        after = IMAGE_LINE.sub(replace_image_line, after)
        if after != before:
            rewrites.append(FileRewrite(path, before, after))
    if issues:
        return RewritePlan((), tuple(sorted(set(issues))))
    return RewritePlan(tuple(rewrites), ())


def atomic_write_text(path: Path, text: str) -> None:
    temp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temp.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def apply_rewrite_plan(plan: RewritePlan) -> None:
    if plan.issues:
        raise ValueError("cannot apply a rewrite plan with issues")
    for rewrite in plan.files:
        atomic_write_text(rewrite.path, rewrite.after)