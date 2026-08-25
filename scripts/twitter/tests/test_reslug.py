"""Focused tests for the one-time bulk thread-directory reslug plumbing.

These tests exercise the small planning, pair-rename, recursive-rewrite,
apply, and format helpers added to ``emit_archive``. They use compact local
fixtures under a ``TemporaryDirectory`` and never touch the real vault.
"""

from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from twitter.emit_archive import (
    ReslugConflict,
    ReslugMove,
    ReslugPlan,
    apply_reslug_plan,
    format_reslug_plan,
    plan_reslug,
    rename_thread_pair,
    rewrite_archive_paths,
)


def _write_pair(
    vault: Path,
    *,
    handle: str = "example",
    directory: str = "2026-08-24-wrong",
    title: str = "Canonical title.",
    date: str = "2026-08-24",
    post_id: str = "100",
) -> tuple[Path, Path]:
    """Build a paired archive/asset directory with a thread_data + media json."""
    archive = vault / "archive" / "threads" / handle / directory
    assets = vault / "assets" / "threads" / handle / directory
    archive.mkdir(parents=True, exist_ok=True)
    assets.mkdir(parents=True, exist_ok=True)
    (archive / "index.md").write_text(
        "---\n"
        f"title: {json.dumps(title)}\n"
        f"handle: {handle}\n"
        f'post_id: "{post_id}"\n'
        f"date: {date}\n"
        "draft: true\n"
        "tags:\n"
        "  - archive\n"
        "  - twitter\n"
        f"  - {handle}\n"
        "---\n\n**1/**\n\nFixture body.\n",
        encoding="utf-8",
        newline="\n",
    )
    (assets / "thread_data.json").write_text(
        json.dumps(
            {
                "root_post_id": post_id,
                "source_url": f"https://x.com/{handle}/status/{post_id}",
                "posts": [
                    {
                        "post_id": post_id,
                        "author": handle,
                        "handle": handle,
                        "text": title,
                        "timestamp": f"{date} 12:00:00",
                        "media_urls": [],
                        "reply_to_id": None,
                        "quote_of_id": None,
                        "metrics": {},
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (assets / "media.json").write_text(
        json.dumps(
            {
                "schema_version": 2,
                "root_post_id": post_id,
                "items": [],
                "mirrors": [],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return archive, assets


class ReslugPlanTests(unittest.TestCase):
    def test_plan_computes_expected_dir_from_frontmatter(self) -> None:
        """Title/date frontmatter must yield the canonical dir name."""
        with TemporaryDirectory() as raw:
            vault = Path(raw) / "vault"
            _write_pair(vault)
            plan = plan_reslug(vault, set())
            self.assertFalse(plan.conflicts)
            self.assertEqual(len(plan.moves), 1)
            self.assertEqual(plan.moves[0].new_dir_name, "2026-08-24-canonical-title")
            self.assertEqual(plan.moves[0].old_dir_name, "2026-08-24-wrong")
            self.assertEqual(plan.moves[0].handle, "example")

    def test_exact_match_is_noop(self) -> None:
        """A directory whose name already matches must be reported as a no-op."""
        with TemporaryDirectory() as raw:
            vault = Path(raw) / "vault"
            _write_pair(vault, directory="2026-08-24-canonical-title")
            plan = plan_reslug(vault, set())
            self.assertEqual(len(plan.noops), 1)
            self.assertFalse(plan.moves)
            self.assertFalse(plan.conflicts)
            self.assertTrue(plan.can_apply)

    def test_occupied_destination_blocks_entire_plan(self) -> None:
        """An occupied archive or asset destination must surface as a conflict."""
        with TemporaryDirectory() as raw:
            vault = Path(raw) / "vault"
            _write_pair(vault)
            _write_pair(vault, directory="2026-08-24-canonical-title", post_id="200")
            plan = plan_reslug(vault, set())
            self.assertTrue(plan.conflicts)
            self.assertFalse(plan.can_apply)
            self.assertFalse(plan.moves)

    def test_mismatched_frozen_pair_is_skipped_and_tracked(self) -> None:
        """A mismatched frozen pair is skipped and its archive dir is excluded."""
        with TemporaryDirectory() as raw:
            vault = Path(raw) / "vault"
            _write_pair(vault, post_id="300")
            plan = plan_reslug(vault, {"300"})
            self.assertEqual(len(plan.frozen), 1)
            self.assertEqual(len(plan.frozen_dirs), 1)
            self.assertFalse(plan.moves)
            self.assertFalse(plan.conflicts)
            self.assertTrue(plan.can_apply)

    def test_missing_asset_pair_becomes_conflict(self) -> None:
        """An archive dir with no asset partner is a blocking conflict."""
        with TemporaryDirectory() as raw:
            vault = Path(raw) / "vault"
            archive = vault / "archive" / "threads" / "example" / "2026-08-24-wrong"
            archive.mkdir(parents=True)
            (archive / "index.md").write_text(
                "---\n"
                'title: "Canonical title."\n'
                'handle: example\n'
                'post_id: "100"\n'
                "date: 2026-08-24\n"
                "draft: true\n"
                "tags:\n"
                "  - archive\n"
                "---\n\n**1/**\n\nFixture.\n",
                encoding="utf-8",
                newline="\n",
            )
            plan = plan_reslug(vault, set())
            self.assertTrue(plan.conflicts)
            self.assertFalse(plan.moves)


class ReslugRenameTests(unittest.TestCase):
    def test_rename_moves_both_dirs(self) -> None:
        """rename_thread_pair must move assets first and archive second."""
        with TemporaryDirectory() as raw:
            vault = Path(raw) / "vault"
            _write_pair(vault)
            plan = plan_reslug(vault, set())
            move = plan.moves[0]
            rename_thread_pair(move)
            self.assertFalse(move.archive_old.exists())
            self.assertFalse(move.asset_old.exists())
            self.assertTrue(move.archive_new.is_dir())
            self.assertTrue(move.asset_new.is_dir())

    def test_archive_failure_rolls_asset_back(self) -> None:
        """An injected archive rename failure must move the asset back and re-raise."""
        with TemporaryDirectory() as raw:
            vault = Path(raw) / "vault"
            _write_pair(vault)
            move = plan_reslug(vault, set()).moves[0]
            original_rename = Path.rename

            def fail_archive(path: Path, destination: Path) -> Path:
                if path == move.archive_old:
                    raise OSError("injected archive failure")
                return original_rename(path, destination)

            with patch.object(Path, "rename", fail_archive):
                with self.assertRaisesRegex(OSError, "injected"):
                    rename_thread_pair(move)
            self.assertTrue(move.archive_old.is_dir())
            self.assertTrue(move.asset_old.is_dir())
            self.assertFalse(move.asset_new.exists())


class ReslugRewriteTests(unittest.TestCase):
    def test_recursive_rewrite_updates_markdown_canvas_and_branch_paths(self) -> None:
        """Markdown and Canvas files inside and outside the thread dir must update."""
        with TemporaryDirectory() as raw:
            root = Path(raw)
            vault = root / "vault"
            _write_pair(vault)
            old = "archive/threads/example/2026-08-24-wrong"
            new = "archive/threads/example/2026-08-24-canonical-title"
            inbound = vault / "notes" / "inbound.md"
            canvas = vault / "canvases" / "map.canvas"
            inbound.parent.mkdir(parents=True)
            canvas.parent.mkdir(parents=True)
            inbound.write_text(
                f"[[{old}/branch]] and [[{old}|alias]]\n",
                encoding="utf-8",
            )
            canvas.write_text(
                json.dumps({"edges": [{"file": f"{old}/branch.md"}]}),
                encoding="utf-8",
            )
            archive_branch = vault / "archive" / "threads" / "example" / "2026-08-24-wrong" / "branch.md"
            archive_branch.write_text(f"link: [[{old}/index]]\n", encoding="utf-8")
            changed = rewrite_archive_paths(vault, root / "scratch", {old: new}, ())
            self.assertIn(new + "/branch", inbound.read_text(encoding="utf-8"))
            self.assertIn(new + "/branch.md", canvas.read_text(encoding="utf-8"))
            self.assertIn(new + "/index", archive_branch.read_text(encoding="utf-8"))
            self.assertIn(canvas, changed)
            self.assertIn(inbound, changed)
            self.assertIn(archive_branch, changed)

    def test_replacement_is_one_pass_and_non_cascading(self) -> None:
        """Both keys must be applied in one pass; longest key wins at overlap."""
        with TemporaryDirectory() as raw:
            vault = Path(raw) / "vault"
            inbound = vault / "notes" / "inbound.md"
            inbound.parent.mkdir(parents=True)
            inbound.write_text(
                "[[archive/threads/example/old]] and [[archive/threads/example/old-x]]\n",
                encoding="utf-8",
            )
            rewrite_archive_paths(
                vault,
                Path(raw) / "scratch",
                {
                    "archive/threads/example/old": "archive/threads/example/new",
                    "archive/threads/example/old-x": "archive/threads/example/new-x",
                },
                (),
            )
            self.assertEqual(
                inbound.read_text(encoding="utf-8"),
                "[[archive/threads/example/new]] and [[archive/threads/example/new-x]]\n",
            )

    def test_excluded_top_level_dirs_and_frozen_dirs_are_byte_identical(self) -> None:
        """site/, assets/, secrets/, .git/, node_modules/, and frozen dirs must not change."""
        with TemporaryDirectory() as raw:
            root = Path(raw)
            vault = root / "vault"
            _write_pair(vault)
            old = "archive/threads/example/2026-08-24-wrong"
            new = "archive/threads/example/2026-08-24-canonical-title"
            frozen_archive, _ = _write_pair(
                vault,
                handle="frozen_author",
                directory="2024-01-01-locked",
                title="Locked title.",
                date="2024-01-01",
                post_id="999",
            )
            frozen_index = frozen_archive / "index.md"
            frozen_bytes = frozen_index.read_bytes()
            for excluded in ("site", "assets", "secrets", "node_modules", ".git"):
                excluded_dir = vault / excluded / "nested"
                excluded_dir.mkdir(parents=True, exist_ok=True)
                (excluded_dir / "note.md").write_text(
                    f"see {old} for context\n",
                    encoding="utf-8",
                )
            rewrite_archive_paths(
                vault,
                root / "scratch",
                {old: new},
                (frozen_archive,),
            )
            self.assertEqual(frozen_index.read_bytes(), frozen_bytes)
            for excluded in ("site", "assets", "secrets", "node_modules", ".git"):
                txt = (vault / excluded / "nested" / "note.md").read_text(encoding="utf-8")
                self.assertIn(old, txt)
                self.assertNotIn(new, txt)


class ReslugApplyTests(unittest.TestCase):
    def test_apply_refuses_conflicts_before_any_move(self) -> None:
        """apply_reslug_plan must raise before touching disk when conflicts exist."""
        with TemporaryDirectory() as raw:
            root = Path(raw)
            vault = root / "vault"
            old_archive, old_assets = _write_pair(vault)
            _write_pair(vault, directory="2026-08-24-canonical-title", post_id="200")
            plan = plan_reslug(vault, set())
            with self.assertRaisesRegex(RuntimeError, "conflict"):
                apply_reslug_plan(plan, root / "scratch")
            self.assertTrue(old_archive.is_dir())
            self.assertTrue(old_assets.is_dir())

    def test_apply_moves_pairs_and_rewrites_inbound_links(self) -> None:
        """apply_reslug_plan must move both dirs and rewrite inbound links."""
        with TemporaryDirectory() as raw:
            root = Path(raw)
            vault = root / "vault"
            _write_pair(vault)
            old = "archive/threads/example/2026-08-24-wrong"
            new = "archive/threads/example/2026-08-24-canonical-title"
            inbound = vault / "notes" / "inbound.md"
            inbound.parent.mkdir(parents=True)
            inbound.write_text(f"see [[{old}/index]]\n", encoding="utf-8")
            plan = plan_reslug(vault, set())
            rewritten = apply_reslug_plan(plan, root / "scratch")
            self.assertTrue((vault / "archive" / "threads" / "example" / "2026-08-24-canonical-title").is_dir())
            self.assertTrue((vault / "assets" / "threads" / "example" / "2026-08-24-canonical-title").is_dir())
            self.assertIn(new, inbound.read_text(encoding="utf-8"))
            self.assertIn(inbound, rewritten)


class ReslugFormatTests(unittest.TestCase):
    def test_format_output_is_deterministic_and_complete(self) -> None:
        """format_reslug_plan must enumerate noop/rename/conflict lines plus counts deterministically."""
        with TemporaryDirectory() as raw:
            vault = Path(raw) / "vault"
            _write_pair(vault, directory="2026-08-24-canonical-title")
            _write_pair(
                vault,
                handle="other",
                directory="2024-01-01-old",
                title="Other title.",
                date="2024-01-01",
                post_id="500",
            )
            _write_pair(
                vault,
                handle="busy",
                directory="2024-05-05-old",
                title="Busy title.",
                date="2024-05-05",
                post_id="600",
            )
            _write_pair(
                vault,
                handle="busy",
                directory="2024-05-05-busy-title",
                title="Busy title.",
                date="2024-05-05",
                post_id="700",
            )
            plan = plan_reslug(vault, set())
            first = format_reslug_plan(plan)
            second = format_reslug_plan(plan)
            self.assertEqual(first, second, "format must be deterministic")
            lines = first.splitlines()
            noop_lines = [line for line in lines if line.startswith("[noop]")]
            rename_lines = [line for line in lines if line.startswith("[rename]")]
            conflict_lines = [line for line in lines if line.startswith("[conflict]")]
            self.assertGreaterEqual(len(noop_lines), 1)
            self.assertEqual(len(rename_lines), 1)
            self.assertEqual(len(conflict_lines), 1)
            noop_text = "\n".join(noop_lines)
            self.assertIn(
                "archive/threads/example/2026-08-24-canonical-title",
                noop_text,
            )
            self.assertIn("archive/threads/other/2024-01-01-old", rename_lines[0])
            self.assertIn(
                "archive/threads/other/2024-01-01-other-title",
                rename_lines[0],
            )
            self.assertIn("->", rename_lines[0])
            self.assertIn("archive/threads/busy", conflict_lines[0])
            self.assertIn("2024-05-05-old", conflict_lines[0])
            self.assertTrue(lines[-1].startswith("summary: "))
            self.assertIn("moves=", lines[-1])
            self.assertIn("noops=", lines[-1])
            self.assertIn("conflicts=", lines[-1])
            self.assertTrue(first.endswith("\n"))


class ReslugModuleOrderTests(unittest.TestCase):
    def test_reslug_definitions_appear_before_main_guard(self) -> None:
        """The reslug block must sit above ``if __name__ == "__main__"``."""
        module_path = Path(__file__).resolve().parent.parent / "emit_archive.py"
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        names: set[str] = {
            "ReslugMove",
            "ReslugConflict",
            "ReslugPlan",
            "plan_reslug",
            "format_reslug_plan",
            "rename_thread_pair",
            "rewrite_archive_paths",
            "apply_reslug_plan",
        }
        main_line: int | None = None
        for node in tree.body:
            if not isinstance(node, ast.If):
                continue
            test = node.test
            if (
                isinstance(test, ast.Compare)
                and len(test.ops) == 1
                and isinstance(test.ops[0], ast.Eq)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
            ):
                main_line = node.lineno
                break
        self.assertIsNotNone(main_line, "if __name__ == '__main__' block not found")
        first_def_line: dict[str, int] = {}
        for node in ast.walk(tree):
            if isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ) and node.name in names:
                first_def_line.setdefault(node.name, node.lineno)
        for name in sorted(names):
            self.assertIn(name, first_def_line, f"{name} not defined in module")
            self.assertLess(
                first_def_line[name],
                main_line,
                f"{name} defined at line {first_def_line[name]} "
                f"is after main guard at line {main_line}",
            )


class ReslugNoopRewriteTests(unittest.TestCase):
    def test_nonfrozen_noop_is_not_frozen_and_links_still_rewrite(self) -> None:
        """A canonical nonfrozen noop must NOT enter frozen_dirs and its links must still rewrite."""
        with TemporaryDirectory() as raw:
            root = Path(raw)
            vault = root / "vault"
            # Thread A: nonfrozen mismatched -> rename
            archive_a, _ = _write_pair(
                vault,
                handle="author_a",
                directory="2024-01-01-old",
                title="A title.",
                date="2024-01-01",
                post_id="111",
            )
            # Thread B: canonical nonfrozen noop with a cross-thread link to A's old prefix
            archive_b, _ = _write_pair(
                vault,
                handle="author_b",
                directory="2024-02-02-b-title",
                title="B title.",
                date="2024-02-02",
                post_id="222",
            )
            (archive_b / "index.md").write_text(
                "---\n"
                'title: "B title."\n'
                "handle: author_b\n"
                'post_id: "222"\n'
                "date: 2024-02-02\n"
                "draft: true\n"
                "tags:\n"
                "  - archive\n"
                "  - twitter\n"
                "  - author_b\n"
                "---\n\n"
                "See [[archive/threads/author_a/2024-01-01-old/index]] for context.\n",
                encoding="utf-8",
                newline="\n",
            )
            plan = plan_reslug(vault, set())
            self.assertIn(archive_b, plan.noops)
            self.assertNotIn(archive_b, plan.frozen_dirs)
            self.assertNotIn(archive_b, plan.frozen)
            rewritten = apply_reslug_plan(plan, root / "scratch")
            new_text = (archive_b / "index.md").read_text(encoding="utf-8")
            self.assertIn(
                "[[archive/threads/author_a/2024-01-01-a-title/index]]",
                new_text,
            )
            self.assertNotIn("2024-01-01-old", new_text)
            self.assertIn(archive_b / "index.md", rewritten)


if __name__ == "__main__":
    unittest.main()
