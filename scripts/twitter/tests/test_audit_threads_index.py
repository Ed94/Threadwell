from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from twitter.audit_handle_index import (
    audit_one,
    audit_threads_index,
    main,
)


def _write_handle(
    handle_dir: Path,
    wikilinks: list[str] | None,
    subdirs: list[str] | None,
) -> None:
    handle_dir.mkdir(parents=True, exist_ok=True)
    for name in subdirs or []:
        (handle_dir / name).mkdir()
    if wikilinks is not None:
        body = "\n".join(f"- [[archive/threads/{handle_dir.name}/{w}]]" for w in wikilinks)
        (handle_dir / "index.md").write_text(
            "---\ntitle: x\n---\n\n" + body + "\n",
            encoding="utf-8",
            newline="\n",
        )


def _write_threads_index(threads_root: Path, handles: list[str]) -> None:
    body = "\n".join(f"- [[archive/threads/{h}]]" for h in handles)
    (threads_root / "index.md").write_text(
        "---\ntitle: Threads\n---\n\n" + body + "\n",
        encoding="utf-8",
        newline="\n",
    )


class ThreadsIndexAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="threads_audit_"))
        self.threads_root = self.tmp / "archive" / "threads"
        self.threads_root.mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_threads_index_clean(self) -> None:
        _write_handle(self.threads_root / "alice", None, ["2024-01-01"])
        _write_handle(self.threads_root / "bob", None, ["2024-02-02"])
        _write_threads_index(self.threads_root, ["alice", "bob"])
        result = audit_threads_index(self.threads_root)
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["stale"], [])
        self.assertEqual(set(result["real"]), {"alice", "bob"})

    def test_threads_index_missing_handle(self) -> None:
        # bob exists on disk but is not wikilinked in threads index
        _write_handle(self.threads_root / "alice", None, [])
        _write_handle(self.threads_root / "bob", None, [])
        _write_threads_index(self.threads_root, ["alice"])
        result = audit_threads_index(self.threads_root)
        self.assertEqual(result["missing"], ["bob"])
        self.assertEqual(result["stale"], [])

    def test_threads_index_stale_wikilink(self) -> None:
        # ghost is wikilinked but no handle dir exists
        _write_handle(self.threads_root / "alice", None, [])
        _write_threads_index(self.threads_root, ["alice", "ghost"])
        result = audit_threads_index(self.threads_root)
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["stale"], ["ghost"])


class AuditorCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="threads_audit_cli_"))
        self.threads_root = self.tmp / "archive" / "threads"
        self.threads_root.mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_main_text_includes_threads_index_entry(self) -> None:
        _write_handle(self.threads_root / "alice", None, [])
        _write_handle(self.threads_root / "bob", None, [])
        _write_threads_index(self.threads_root, ["alice"])
        # bob is missing from the threads index; main() should flag it
        import io
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--vault", str(self.tmp)])
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        self.assertIn("alice", out)
        self.assertIn("bob", out)
        self.assertIn("threads index", out)
        self.assertIn("missing_in_index", out)


if __name__ == "__main__":
    unittest.main()