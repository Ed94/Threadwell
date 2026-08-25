from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.request import Request

from twitter.catbox_client import load_userhash, upload_file


class _FakeResponse:
    def __init__(self, body: bytes) -> None:
        self._body = body

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, *_args: object) -> bool:
        return False


class CatboxClientTests(unittest.TestCase):
    def test_load_userhash_reads_toml(self) -> None:
        with TemporaryDirectory() as raw:
            vault = Path(raw)
            (vault / "secrets").mkdir()
            (vault / "secrets" / "credentials.toml").write_text(
                '[catbox]\nuserhash = "test-hash"\n',
                encoding="utf-8",
            )
            self.assertEqual(load_userhash(vault), "test-hash")

    def test_load_userhash_rejects_empty(self) -> None:
        with TemporaryDirectory() as raw:
            vault = Path(raw)
            (vault / "secrets").mkdir()
            (vault / "secrets" / "credentials.toml").write_text(
                "[catbox]\nuserhash = \"\"\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "userhash is empty"):
                load_userhash(vault)

    def test_upload_posts_form_without_subprocess(self) -> None:
        with TemporaryDirectory() as raw:
            src = Path(raw) / "still.png"
            src.write_bytes(b"png")
            captured: dict[str, object] = {}

            def fake_urlopen(
                request: Request,
                timeout: int,
                context: object,
            ) -> _FakeResponse:
                captured["data"] = request.data
                captured["timeout"] = timeout
                return _FakeResponse(b"https://files.catbox.moe/abc.png")

            with patch("twitter.catbox_client.urlopen", fake_urlopen):
                url = upload_file(src, "test-hash")
            self.assertEqual(url, "https://files.catbox.moe/abc.png")
            body = captured["data"]
            assert isinstance(body, bytes)
            self.assertIn(b"test-hash", body)
            self.assertIn(b"reqtype", body)
            self.assertIn(b"png", body)
            self.assertEqual(captured["timeout"], 180)

    def test_error_message_omits_userhash(self) -> None:
        with TemporaryDirectory() as raw:
            src = Path(raw) / "still.png"
            src.write_bytes(b"png")

            def boom(
                request: Request,
                timeout: int,
                context: object,
            ) -> _FakeResponse:
                del request, timeout, context
                raise URLError("refused")

            with patch("twitter.catbox_client.urlopen", boom):
                with self.assertRaises(RuntimeError) as ctx:
                    upload_file(src, "test-hash")
            self.assertNotIn("test-hash", str(ctx.exception))

    def test_http_error_omits_userhash(self) -> None:
        with TemporaryDirectory() as raw:
            src = Path(raw) / "still.png"
            src.write_bytes(b"png")

            def boom(
                request: Request,
                timeout: int,
                context: object,
            ) -> _FakeResponse:
                del timeout, context
                raise HTTPError(
                    request.full_url,
                    500,
                    "server",
                    hdrs=None,  # type: ignore[arg-type]
                    fp=None,
                )

            with patch("twitter.catbox_client.urlopen", boom):
                with self.assertRaises(RuntimeError) as ctx:
                    upload_file(src, "test-hash")
            self.assertNotIn("test-hash", str(ctx.exception))
            self.assertIn("HTTP 500", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
