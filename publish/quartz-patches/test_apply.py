from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urljoin

import apply


DEEP_REL: str = "../../../../archive/threads/notimothylottes/"
DEEP_SLUG: str = (
    "archive/threads/notimothylottes/2025-02-04-gelatinous-pixel-soup/index.html"
)
PAGE_BASE: str = (
    "/Threadwell/archive/threads/notimothylottes/2025-02-04-gelatinous-pixel-soup/"
)
SAMPLE: str = (
    "<html><head></head><body>"
    '<h2 class="page-title"><a href="./">Threadwell</a></h2>'
    f'<a class="internal" href="{DEEP_REL}">NOTimothyLottes</a>'
    "</body></html>"
)


def _write_public(root: Path, rel: str, html: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path


class ApplyBaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self._public = apply.PUBLIC
        self._tmp = tempfile.TemporaryDirectory()
        self.public = Path(self._tmp.name)
        apply.PUBLIC = self.public

    def tearDown(self) -> None:
        apply.PUBLIC = self._public
        self._tmp.cleanup()

    def test_deep_page_base_is_page_directory(self) -> None:
        path = _write_public(self.public, DEEP_SLUG, SAMPLE)
        apply.rewrite_html(path)
        text = path.read_text(encoding="utf-8")
        self.assertIn(f'<base href="{PAGE_BASE}">', text)
        self.assertNotIn('<base href="https://edsabode.dev/Threadwell/">', text)
        self.assertNotIn('<base href="/Threadwell/">', text)

    def test_deep_page_relative_link_keeps_threadwell_prefix(self) -> None:
        path = _write_public(self.public, DEEP_SLUG, SAMPLE)
        apply.rewrite_html(path)
        text = path.read_text(encoding="utf-8")
        match = re.search(r'<base href="([^"]+)">', text)
        self.assertIsNotNone(match)
        assert match is not None
        resolved = urljoin("https://edsabode.dev" + match.group(1), DEEP_REL)
        self.assertEqual(
            resolved,
            "https://edsabode.dev/Threadwell/archive/threads/notimothylottes/",
        )

    def test_homepage_base_is_site_path(self) -> None:
        path = _write_public(self.public, "index.html", SAMPLE)
        apply.rewrite_html(path)
        text = path.read_text(encoding="utf-8")
        self.assertIn('<base href="/Threadwell/">', text)

    def test_title_link_is_site_path_not_domain_root(self) -> None:
        path = _write_public(self.public, DEEP_SLUG, SAMPLE)
        apply.rewrite_html(path)
        text = path.read_text(encoding="utf-8")
        self.assertIn(
            '<h2 class="page-title"><a href="/Threadwell/">',
            text,
        )
        self.assertNotIn('href="https://edsabode.dev/Threadwell/"', text)

    def test_rewrite_replaces_site_root_base_and_stays_idempotent(self) -> None:
        html = SAMPLE.replace(
            "<head></head>",
            '<head><base href="https://edsabode.dev/Threadwell/"></head>',
        )
        path = _write_public(self.public, DEEP_SLUG, html)
        apply.rewrite_html(path)
        apply.rewrite_html(path)
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count("<base "), 1)
        self.assertIn(f'<base href="{PAGE_BASE}">', text)


if __name__ == "__main__":
    unittest.main()
