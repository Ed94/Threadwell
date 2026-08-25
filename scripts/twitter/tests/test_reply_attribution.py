from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from twitter.emit_archive import apply_relabel, format_relabel_plan, plan_relabel
from twitter.models import PostData, PostMetrics, ThreadData
from twitter.render import (
    _post_block,
    format_post_text,
    render_branch,
    render_spine,
    split_leading_mentions,
)
from twitter.tw import build_parser, cmd_relabel


def post(
    post_id: str,
    handle: str,
    text: str,
    reply_to_id: str | None,
) -> PostData:
    return PostData(
        post_id=post_id,
        author=handle,
        handle=handle,
        text=text,
        timestamp="2025-03-08 12:00:00",
        media_urls=(),
        reply_to_id=reply_to_id,
        quote_of_id=None,
        metrics=PostMetrics(0, 0, 0, None),
    )


class PostBlockAttributionTests(unittest.TestCase):
    def test_number_line_includes_handle(self) -> None:
        block = _post_block(
            19,
            post("1898440015182729598", "SebAaltonen", "WG_RR_EN", "1"),
            None,
        )
        self.assertTrue(block.startswith("**19/** @SebAaltonen\n"))
        self.assertIn("WG_RR_EN", block)

    def test_empty_handle_raises(self) -> None:
        with self.assertRaises(ValueError):
            _post_block(1, post("1", "", "text", None), None)

    def test_leading_mentions_are_their_own_line(self) -> None:
        block = _post_block(
            19,
            post(
                "1898440015182729598",
                "SebAaltonen",
                "@NOTimothyLottes I said WG_RR_EN",
                "1",
            ),
            None,
        )
        self.assertIn("**19/** @SebAaltonen\n\n@NOTimothyLottes\n\nI said WG_RR_EN", block)

    def test_format_post_text_is_idempotent(self) -> None:
        original = "@AgileJebrim @SebAaltonen The higher the occupancy"
        once = format_post_text(original)
        self.assertEqual(once, "@AgileJebrim @SebAaltonen\n\nThe higher the occupancy")
        self.assertEqual(format_post_text(once), once)
        self.assertEqual(split_leading_mentions("holy truthnuke")[0], "")


class RenderAttributionTests(unittest.TestCase):
    def test_mixed_spine_labels_each_post(self) -> None:
        thread = ThreadData(
            root_post_id="1",
            posts=(
                post("1", "rianflo", "The road to 16-bit", None),
                post("2", "NOTimothyLottes", "Explicit packed 16-bit", "1"),
                post("3", "rianflo", "Oh I know the benefits", "2"),
            ),
            source_url="https://x.com/rianflo/status/1",
        )
        text = render_spine(thread, ["1", "2", "3"], [], {}, "2026-08-25")
        self.assertIn("**1/** @rianflo", text)
        self.assertIn("**2/** @NOTimothyLottes", text)
        self.assertIn("**3/** @rianflo", text)

    def test_mixed_branch_labels_seb_and_jebrim(self) -> None:
        thread = ThreadData(
            root_post_id="root",
            posts=(
                post("root", "SebAaltonen", "Stupid hardware question", None),
                post(
                    "1898352640825651644",
                    "NOTimothyLottes",
                    "@SebAaltonen Actually this is a super important question IMO.",
                    "root",
                ),
                post(
                    "1898440015182729598",
                    "SebAaltonen",
                    "@NOTimothyLottes I said WG_RR_EN",
                    "1898352640825651644",
                ),
                post(
                    "1898385745892495810",
                    "AgileJebrim",
                    "On the flip side, it appears that using 128",
                    "1898352640825651644",
                ),
            ),
            source_url="https://x.com/SebAaltonen/status/root",
        )
        text = render_branch(
            thread,
            "1898352640825651644",
            ["1898440015182729598", "1898385745892495810"],
            "SebAaltonen",
            "2026-08-25",
        )
        self.assertIn("**1/** @NOTimothyLottes", text)
        self.assertIn("**2/** @SebAaltonen", text)
        self.assertIn("**3/** @AgileJebrim", text)
        for line in text.splitlines():
            if line.startswith("**") and "/**" in line:
                self.assertRegex(line, r"^\*\*\d+/\*\* @[A-Za-z0-9_]+$")


class RelabelPatchTests(unittest.TestCase):
    def _vault(self, raw: str) -> tuple[Path, Path, Path]:
        root = Path(raw)
        asset = (
            root / "assets" / "threads" / "SebAaltonen" / "2025-03-08-amd"
        )
        notes = (
            root / "archive" / "threads" / "SebAaltonen" / "2025-03-08-amd"
        )
        asset.mkdir(parents=True)
        notes.mkdir(parents=True)
        (asset / "thread_data.json").write_text(
            """{
  "root_post_id": "root",
  "source_url": "https://x.com/SebAaltonen/status/root",
  "posts": [
    {
      "post_id": "root",
      "author": "SebAaltonen",
      "handle": "SebAaltonen",
      "text": "Stupid hardware question",
      "timestamp": "2025-03-08 07:20:39",
      "media_urls": [],
      "reply_to_id": null,
      "quote_of_id": null,
      "metrics": {"reply_count": 0, "repost_count": 0, "like_count": 0, "view_count": 1}
    },
    {
      "post_id": "1898440015182729598",
      "author": "SebAaltonen",
      "handle": "SebAaltonen",
      "text": "@NOTimothyLottes I said WG_RR_EN",
      "timestamp": "2025-03-08 18:00:00",
      "media_urls": [],
      "reply_to_id": "1898352640825651644",
      "quote_of_id": null,
      "metrics": {"reply_count": 0, "repost_count": 0, "like_count": 0, "view_count": 1}
    },
    {
      "post_id": "1898385745892495810",
      "author": "AgileJebrim",
      "handle": "AgileJebrim",
      "text": "On the flip side, it appears that using 128",
      "timestamp": "2025-03-08 17:00:00",
      "media_urls": [],
      "reply_to_id": "1898352640825651644",
      "quote_of_id": null,
      "metrics": {"reply_count": 0, "repost_count": 0, "like_count": 0, "view_count": 1}
    }
  ]
}
""",
            encoding="utf-8",
            newline="\n",
        )
        (asset / "media.json").write_text(
            '{"schema_version": 2, "root_post_id": "root", "items": []}\n',
            encoding="utf-8",
            newline="\n",
        )
        (notes / "index.md").write_text(
            "---\ndraft: false\ntags:\n  - archive\n  - vulkan\n---\n\n"
            "## Thread\n\n"
            "**1/**\n\n"
            "Stupid hardware question\n",
            encoding="utf-8",
            newline="\n",
        )
        (notes / "branch.md").write_text(
            "---\ndraft: false\n---\n\n"
            "## Branch\n\n"
            "**19/**\n\n"
            "@NOTimothyLottes I said WG_RR_EN\n\n"
            "**33/**\n\n"
            "On the flip side, it appears that using 128\n\n"
            "## Visible chain\n\n"
            "1. **Onat Turkcuoglu** (@onatt0) - Apr 30\n"
            "   holy truthnuke\n",
            encoding="utf-8",
            newline="\n",
        )
        return root, asset, notes

    def test_plan_rewrites_unlabeled_number_lines(self) -> None:
        with TemporaryDirectory() as raw:
            vault, asset, notes = self._vault(raw)
            plan = plan_relabel(vault)
            states = {item.path.name: item.state for item in plan.items}
            self.assertEqual(states["index.md"], "rewrite")
            self.assertEqual(states["branch.md"], "rewrite")
            self.assertTrue(all(item.path.suffix == ".md" for item in plan.items))
            self.assertFalse(
                any(item.path.name == "thread_data.json" for item in plan.items)
            )
            json_before = (asset / "thread_data.json").read_bytes()
            apply_relabel(plan)
            self.assertEqual((asset / "thread_data.json").read_bytes(), json_before)
            self.assertEqual((asset / "media.json").read_bytes(), (
                b'{"schema_version": 2, "root_post_id": "root", "items": []}\n'
            ))
            branch = (notes / "branch.md").read_text(encoding="utf-8")
            self.assertIn("**19/** @SebAaltonen", branch)
            self.assertIn("**33/** @AgileJebrim", branch)
            self.assertIn("1. **Onat Turkcuoglu** (@onatt0) - Apr 30", branch)
            index = (notes / "index.md").read_text(encoding="utf-8")
            self.assertIn("**1/** @SebAaltonen", index)
            self.assertIn("  - vulkan", index)
            self.assertIn("draft: false", index)

    def test_already_labeled_is_noop(self) -> None:
        with TemporaryDirectory() as raw:
            vault, _asset, notes = self._vault(raw)
            (notes / "index.md").write_text(
                "---\ndraft: false\n---\n\n**1/** @SebAaltonen\n\n"
                "Stupid hardware question\n",
                encoding="utf-8",
                newline="\n",
            )
            (notes / "branch.md").write_text(
                "---\ndraft: false\n---\n\n"
                "**19/** @SebAaltonen\n\n"
                "@NOTimothyLottes\n\n"
                "I said WG_RR_EN\n\n"
                "**33/** @AgileJebrim\n\n"
                "On the flip side, it appears that using 128\n",
                encoding="utf-8",
                newline="\n",
            )
            plan = plan_relabel(vault)
            self.assertTrue(all(item.state == "noop" for item in plan.items))
            before = (notes / "index.md").read_bytes()
            apply_relabel(plan)
            self.assertEqual((notes / "index.md").read_bytes(), before)

    def test_patch_splits_leading_mentions(self) -> None:
        from twitter.emit_archive import patch_note_text

        posts = (
            post(
                "1898440015182729598",
                "SebAaltonen",
                "@NOTimothyLottes I said WG_RR_EN",
                None,
            ),
        )
        text = (
            "**19/** @SebAaltonen\n\n"
            "@NOTimothyLottes I said WG_RR_EN\n"
        )
        new, state, reason = patch_note_text(text, posts)
        self.assertEqual(state, "rewrite")
        self.assertEqual(reason, "")
        self.assertIn("@NOTimothyLottes\n\nI said WG_RR_EN", new)
        again, state2, _reason = patch_note_text(new, posts)
        self.assertEqual(state2, "noop")
        self.assertEqual(again, new)

    def test_duplicate_first_line_same_handle_rewrites(self) -> None:
        from twitter.emit_archive import patch_note_text

        posts = (
            post("1", "simplex_fx", "How big?", None),
            post("2", "simplex_fx", "How big?", "1"),
        )
        text = "**30/**\n\nHow big?\n\n**31/**\n\nHow big?\n"
        new, state, reason = patch_note_text(text, posts)
        self.assertEqual(state, "rewrite")
        self.assertEqual(reason, "")
        self.assertIn("**30/** @simplex_fx", new)
        self.assertIn("**31/** @simplex_fx", new)

    def test_empty_handle_is_conflict(self) -> None:
        with TemporaryDirectory() as raw:
            vault, asset, notes = self._vault(raw)
            text = (asset / "thread_data.json").read_text(encoding="utf-8")
            (asset / "thread_data.json").write_text(
                text.replace('"handle": "SebAaltonen"', '"handle": ""', 1),
                encoding="utf-8",
            )
            plan = plan_relabel(vault)
            self.assertTrue(any(item.state == "conflict" for item in plan.items))
            before = (notes / "index.md").read_bytes()
            apply_relabel(plan)
            self.assertEqual((notes / "index.md").read_bytes(), before)

    def test_parser_and_dry_run_do_not_apply(self) -> None:
        args = build_parser().parse_args(["relabel", "--all"])
        self.assertFalse(args.apply)
        args = build_parser().parse_args(["relabel", "--all", "--apply"])
        self.assertTrue(args.apply)
        with TemporaryDirectory() as raw:
            vault, _asset, notes = self._vault(raw)
            before = (notes / "branch.md").read_bytes()
            with patch("twitter.tw.VAULT", vault):
                code = cmd_relabel(
                    build_parser().parse_args(["relabel", "--all"])
                )
            self.assertEqual(code, 0)
            self.assertEqual((notes / "branch.md").read_bytes(), before)


class RelabelFormatTests(unittest.TestCase):
    def test_format_lists_states(self) -> None:
        from twitter.emit_archive import RelabelItem, RelabelPlan

        plan = RelabelPlan(
            vault=Path("v"),
            items=(
                RelabelItem(Path("v/a.md"), "rewrite", ""),
                RelabelItem(Path("v/b.md"), "noop", ""),
            ),
        )
        text = format_relabel_plan(plan)
        self.assertIn("rewrite", text)
        self.assertIn("noop", text)


if __name__ == "__main__":
    unittest.main()
