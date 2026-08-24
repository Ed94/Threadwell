"""Catbox userhash loader and uploader (curl.exe wrapper)."""
from __future__ import annotations

import subprocess
import tomllib
from pathlib import Path


def load_userhash(vault: Path) -> str:
    """Load the catbox ``userhash`` from ``vault/secrets/credentials.toml`` (TOML or lenient line scan)."""
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


def upload_file(path: Path, userhash: str) -> str:
    """Upload ``path`` to catbox.moe via curl.exe and return the public HTTPS URL."""
    cmd = [
        "curl.exe",
        "-sS",
        "--max-time",
        "180",
        "--limit-rate",
        "200k",
        "-F",
        "reqtype=fileupload",
        "-F",
        f"userhash={userhash}",
        "-F",
        f"fileToUpload=@{path}",
        "https://catbox.moe/user/api.php",
    ]
    try:
        raw = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"catbox upload failed for {path.name} (curl exit {exc.returncode})"
        ) from None
    url = raw.strip()
    if not url.startswith("https://"):
        raise RuntimeError(f"catbox refused {path.name}: non-URL response")
    return url