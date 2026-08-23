"""Upload curated stills to catbox and rewrite archive notes to HTTPS.

Reads userhash from vault secrets/credentials.toml [catbox]. Never prints it.

  python lift_catbox.py --thread ASSETS_THREAD --notes ARCHIVE_THREAD --orig

--orig marks every on-disk orig row publish=true then uploads those.
Default without --orig: only rows already publish=true.

After upload, any note token that is the local filename (backticked or
bare) or a previous url for that row becomes ![](https://files.catbox.moe/…).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

API = "https://catbox.moe/user/api.php"
CREDS = Path("secrets/credentials.toml")


def load_userhash(vault: Path) -> str:
    path = vault / "secrets" / "credentials.toml"
    if not path.is_file():
        raise SystemExit(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    try:
        data = tomllib.loads(text)
        h = str((data.get("catbox") or {}).get("userhash") or "").strip()
    except tomllib.TOMLDecodeError:
        h = ""
        in_catbox = False
        for raw in text.splitlines():
            line = raw.strip()
            if line.startswith("[") and line.endswith("]"):
                in_catbox = line[1:-1].strip().lower() == "catbox"
                continue
            if in_catbox and line.lower().startswith("userhash"):
                _, _, rest = line.partition("=")
                h = rest.strip().strip("\"'")
                break
    if not h:
        raise SystemExit("credentials.toml [catbox] userhash is empty")
    return h


def upload(path: Path, userhash: str) -> str:
    cmd = [
        "curl.exe",
        "-sS",
        "-F",
        "reqtype=fileupload",
        "-F",
        f"userhash={userhash}",
        "-F",
        f"fileToUpload=@{path}",
        API,
    ]
    raw = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    url = raw.strip()
    if not url.startswith("https://"):
        raise SystemExit(f"catbox refused {path.name}: {url[:200]}")
    return url


def rewrite_notes(notes_dir: Path, old_tokens: list[str], url: str) -> int:
    embed = f"![]({url})"
    changed = 0
    for path in notes_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        new = text
        for token in old_tokens:
            if not token:
                continue
            new = new.replace(f"`{token}`", embed)
            new = new.replace(f"![]({token})", embed)
        new = re.sub(r"^Media \(not lifted\):\s*", "", new, flags=re.M)
        while True:
            split = re.sub(
                r"(!\[[^\]]*\]\([^)]+\))\s+(!\[[^\]]*\]\([^)]+\))",
                r"\1\n\n\2",
                new,
            )
            if split == new:
                break
            new = split
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed += 1
            print(f"rewrote {path.name}")
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, default=Path(r"C:\projects\Threadwell"))
    parser.add_argument("--thread", type=Path, required=True)
    parser.add_argument("--notes", type=Path, required=True)
    parser.add_argument(
        "--orig",
        action="store_true",
        help="publish+upload every orig file that exists on disk",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    media_path = args.thread / "media.json"
    data = json.loads(media_path.read_text(encoding="utf-8"))
    items = data.setdefault("items", [])
    if args.orig:
        for item in items:
            if item.get("role") == "orig":
                item["publish"] = True
                if "embed" not in item:
                    item["embed"] = True

    userhash = None if args.dry_run else load_userhash(args.vault)
    uploaded = 0
    for item in items:
        if not item.get("publish"):
            continue
        name = str(item.get("filename") or "")
        src = args.thread / name
        if not src.is_file():
            print(f"skip missing {name}")
            continue
        old = [name, str(item.get("url") or "")]
        if args.dry_run:
            print(f"would upload {name}")
            continue
        assert userhash is not None
        url = upload(src, userhash)
        item["url"] = url
        uploaded += 1
        print(f"uploaded {name} -> {url}")
        rewrite_notes(args.notes, old, url)

    if not args.dry_run:
        media_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"uploaded {uploaded}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
