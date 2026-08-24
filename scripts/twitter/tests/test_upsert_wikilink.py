from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path

from twitter.emit_archive import _upsert_wikilink


_WIKILINK_LINE = re.compile(r"^\s*-\s+\[\[([^\]|]+)\]\]\s*$")


def _read_wikilink_lines(idx: Path) -> list[str]:
    text = idx.read_text(encoding="utf-8")
    out: list[str] = []
    for line in text.splitlines():
        m = _WIKILINK_LINE.match(line)
        if m:
            out.append("- [[" + m.group(1) + "]]")
    return out


class UpsertWikilinkTests(unittest.TestCase):
    def _build(self, subdirs: list[str], wikilinks: list[str]) -> Path:
        """Build a temp vault with one handle containing `subdirs` and an
        index.md whose body is the given wikilinks (one per line)."""
        raw = tempfile.mkdtemp(prefix="upsert_wikilink_")
        self.addCleanup(shutil.rmtree, raw, ignore_errors=True)
        root = Path(raw)
        handle_dir = root / "archive" / "threads" / "handle"
        handle_dir.mkdir(parents=True)
        for name in subdirs:
            (handle_dir / name).mkdir()
        idx = handle_dir / "index.md"
        body = "\n".join(wikilinks)
        idx.write_text(
            "---\ntitle: handle\ndraft: false\n---\n\n" + body + "\n",
            encoding="utf-8",
            newline="\n",
        )
        return idx

    def test_preserves_existing_wikilink_whose_dir_still_exists(self) -> None:
        """Upserting a target whose dir already exists must keep every
        other real-directory wikilink in the index."""
        idx = self._build(
            ["2024-01-01-foo", "2024-02-02-bar"],
            [
                "- [[archive/threads/handle/2024-01-01-foo]]",
                "- [[archive/threads/handle/2024-02-02-bar]]",
            ],
        )
        _upsert_wikilink(idx, "archive/threads/handle/2024-01-01-foo")
        self.assertEqual(
            _read_wikilink_lines(idx),
            [
                "- [[archive/threads/handle/2024-01-01-foo]]",
                "- [[archive/threads/handle/2024-02-02-bar]]",
            ],
        )

    def test_drops_wikilink_whose_dir_no_longer_exists(self) -> None:
        """Upserting must drop a wikilink whose subdirectory is gone and
        leave the new target in its place."""
        idx = self._build(
            ["2024-01-01-foo"],
            [
                "- [[archive/threads/handle/9999-99-99-missing]]",
            ],
        )
        _upsert_wikilink(idx, "archive/threads/handle/2024-01-01-foo")
        self.assertEqual(
            _read_wikilink_lines(idx),
            [
                "- [[archive/threads/handle/2024-01-01-foo]]",
            ],
        )

    def test_adds_new_target_when_missing_from_index(self) -> None:
        """Upserting a target that is not in the index must add it while
        preserving the existing real-directory wikilinks."""
        idx = self._build(
            ["2024-01-01-foo", "2024-02-02-bar"],
            [
                "- [[archive/threads/handle/2024-02-02-bar]]",
            ],
        )
        _upsert_wikilink(idx, "archive/threads/handle/2024-01-01-foo")
        self.assertEqual(
            _read_wikilink_lines(idx),
            [
                "- [[archive/threads/handle/2024-01-01-foo]]",
                "- [[archive/threads/handle/2024-02-02-bar]]",
            ],
        )

    def test_does_not_duplicate_target_already_in_index(self) -> None:
        """Upserting a target that is already in the index must not
        produce a duplicate wikilink line."""
        idx = self._build(
            ["2024-01-01-foo"],
            [
                "- [[archive/threads/handle/2024-01-01-foo]]",
            ],
        )
        _upsert_wikilink(idx, "archive/threads/handle/2024-01-01-foo")
        self.assertEqual(
            _read_wikilink_lines(idx),
            [
                "- [[archive/threads/handle/2024-01-01-foo]]",
            ],
        )


if __name__ == "__main__":
    unittest.main()