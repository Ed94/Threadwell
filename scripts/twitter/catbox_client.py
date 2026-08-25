"""Load the Catbox userhash and upload one file.

The hash is read from ``secrets/credentials.toml``. It never appears on a
process command line or in printed output.
"""
from __future__ import annotations

import ssl
import tomllib
from pathlib import Path
from secrets import token_hex
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API: str = "https://catbox.moe/user/api.php"
TIMEOUT_SECS: int = 180


def load_userhash(vault: Path) -> str:
    """Return the Catbox ``userhash`` from ``vault/secrets/credentials.toml``."""
    path = vault / "secrets" / "credentials.toml"
    if not path.is_file():
        raise RuntimeError(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    try:
        data = tomllib.loads(text)
        value = str((data.get("catbox") or {}).get("userhash") or "").strip()
    except tomllib.TOMLDecodeError:
        value = ""
        in_catbox = False
        for raw in text.splitlines():
            line = raw.strip()
            if line.startswith("[") and line.endswith("]"):
                in_catbox = line[1:-1].strip().lower() == "catbox"
                continue
            if in_catbox and line.lower().startswith("userhash"):
                _key, _equals, remainder = line.partition("=")
                value = remainder.strip().strip("\"'")
                break
    if not value:
        raise RuntimeError("credentials.toml [catbox] userhash is empty")
    return value


def _encode_multipart(
    fields: list[tuple[str, str]],
    file_field: str,
    file_path: Path,
) -> tuple[bytes, str]:
    """Build a multipart body. Field values stay in the body, not in argv."""
    boundary = "----Threadwell" + token_hex(16)
    chunks: list[bytes] = []
    for name, value in fields:
        chunks.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{name}"\r\n'
                f"\r\n"
                f"{value}\r\n"
            ).encode("utf-8")
        )
    filename = file_path.name.replace('"', "_")
    chunks.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{file_field}"; '
            f'filename="{filename}"\r\n'
            f"Content-Type: application/octet-stream\r\n"
            f"\r\n"
        ).encode("utf-8")
    )
    chunks.append(file_path.read_bytes())
    chunks.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def upload_file(path: Path, userhash: str) -> str:
    """POST ``path`` to catbox.moe and return the public HTTPS URL."""
    body, content_type = _encode_multipart(
        [("reqtype", "fileupload"), ("userhash", userhash)],
        "fileToUpload",
        path,
    )
    request = Request(API, data=body, method="POST")
    request.add_header("Content-Type", content_type)
    try:
        with urlopen(
            request,
            timeout=TIMEOUT_SECS,
            context=ssl.create_default_context(),
        ) as resp:
            url = resp.read().decode("utf-8", errors="replace").strip()
    except HTTPError as exc:
        raise RuntimeError(
            f"catbox upload failed for {path.name} (HTTP {exc.code})"
        ) from None
    except URLError:
        raise RuntimeError(f"catbox upload failed for {path.name}") from None
    if not url.startswith("https://"):
        raise RuntimeError(f"catbox refused {path.name}: non-URL response")
    return url
