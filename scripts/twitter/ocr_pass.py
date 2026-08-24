"""OCR a still. Prefer Umi-OCR HTTP, then tesseract, then Windows.Media.Ocr.

Writes UTF-8 text. Optional: add a role=ocr row to media.json.

Umi-OCR must be running (HTTP :1224). Start Umi-OCR.exe once. Then:

  python ocr_pass.py --in still.png --engine umi

Uses tbpu.parser=single_code (keep indent) and English. ShareX has no OCR CLI.
"""
from __future__ import annotations

import argparse
import base64
import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UMI_URL = "http://127.0.0.1:1224/api/ocr"


def find_umi() -> str | None:
    return shutil.which("umi-ocr") or shutil.which("Umi-OCR")


def find_tesseract() -> str | None:
    return shutil.which("tesseract")


def umi_http_up() -> bool:
    try:
        urllib.request.urlopen("http://127.0.0.1:1224/api/ocr/get_options", timeout=2)
        return True
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def run_umi(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not umi_http_up():
        exe = find_umi()
        if exe:
            subprocess.Popen([exe])
        raise SystemExit(
            "Umi-OCR HTTP not on 127.0.0.1:1224. Start Umi-OCR.exe and retry."
        )
    payload = {
        "base64": base64.b64encode(src.read_bytes()).decode("ascii"),
        "options": {
            "ocr.language": "English",
            "tbpu.parser": "single_code",
            "ocr.maxSideLen": 999999,
            "data.format": "text",
        },
    }
    req = urllib.request.Request(
        UMI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    print(f"umi-http {src.name}")
    raw = urllib.request.urlopen(req, timeout=180).read()
    res = json.loads(raw.decode("utf-8"))
    code = res.get("code")
    data = res.get("data")
    if code == 100 and isinstance(data, str):
        text = data
    elif code == 101:
        text = ""
    elif isinstance(data, list):
        text = "".join(
            str(block.get("text", "")) + str(block.get("end", "")) for block in data
        )
    else:
        raise SystemExit(f"umi-ocr failed code={code} data={data!r}")
    dest.write_text(text.replace("\r\n", "\n"), encoding="utf-8")


def run_tesseract(src: Path, dest: Path) -> None:
    exe = find_tesseract()
    if not exe:
        raise SystemExit("tesseract not on PATH. scoop install tesseract")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out_base = dest.with_suffix("")
    cmd = [exe, str(src), str(out_base), "-l", "eng"]
    print(" ".join(cmd))
    subprocess.check_call(cmd)
    txt = out_base.with_suffix(".txt")
    if txt != dest:
        dest.write_text(txt.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")


def run_windows_ocr(src: Path, dest: Path) -> None:
    ps = r"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Media.Ocr, ContentType = WindowsRuntime]
function Await($op) {
  $asTask = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1
  } | Select-Object -First 1
  $task = $asTask.MakeGenericMethod($op.GetType().GenericTypeArguments[0]).Invoke($null, @($op))
  $task.Wait()
  $task.Result
}
$src = $args[0]
$dest = $args[1]
$file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($src))
$stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read))
$decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream))
$bitmap = Await ($decoder.GetSoftwareBitmapAsync())
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($null -eq $engine) { throw 'Windows OCR engine unavailable' }
$result = Await ($engine.RecognizeAsync($bitmap))
[System.IO.File]::WriteAllText($dest, $result.Text, [System.Text.UTF8Encoding]::new($false))
"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "powershell",
        "-NoProfile",
        "-Command",
        ps,
        str(src.resolve()),
        str(dest.resolve()),
    ]
    print("windows.media.ocr", src.name)
    subprocess.check_call(cmd)


def append_media_row(media_json: Path, src: Path, dest: Path) -> None:
    try:
        from media_manifest import atomic_write_json, upsert_derived_item
    except ImportError:  # pragma: no cover - script-mode import
        from .media_manifest import atomic_write_json, upsert_derived_item
    data = json.loads(media_json.read_text(encoding="utf-8"))
    if data.get("schema_version") != 2:
        raise SystemExit(
            "legacy media.json requires: tw.py migrate-media --id <id> --apply"
        )
    post_id = ""
    media_id = ""
    handle = ""
    for item in data.get("items") or []:
        if str(item.get("filename") or "") in {src.name, dest.name}:
            post_id = str(item.get("post_id") or "")
            media_id = str(item.get("media_id") or "")
            handle = str(item.get("handle") or "")
            break
    if not post_id and "_" in src.stem:
        parts = src.stem.split("_")
        post_id = parts[0]
        media_id = parts[1] if len(parts) > 1 else ""
    asset_dir = media_json.parent
    upsert_derived_item(
        data,
        post_id=post_id,
        media_id=media_id,
        handle=handle,
        role="ocr",
        filename=dest.name,
        asset_dir=asset_dir,
        now=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )
    atomic_write_json(media_json, data)
    print(f"updated {media_json}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="src", type=Path, required=True)
    parser.add_argument("--out", dest="dest", type=Path, default=None)
    parser.add_argument(
        "--engine",
        choices=("auto", "umi", "tesseract", "windows"),
        default="auto",
    )
    parser.add_argument("--media-json", type=Path, default=None)
    args = parser.parse_args(argv)

    if not args.src.is_file():
        raise SystemExit(f"missing {args.src}")
    dest = args.dest
    if dest is None:
        dest = args.src.with_name(args.src.stem.replace("_orig", "") + "_ocr.txt")
        if dest.name == args.src.stem + "_ocr.txt" and args.src.stem.endswith("_orig"):
            dest = args.src.with_name(args.src.stem[: -len("_orig")] + "_ocr.txt")

    engine = args.engine
    if engine == "auto":
        if find_umi():
            engine = "umi"
        elif find_tesseract():
            engine = "tesseract"
        else:
            engine = "windows"
    print(f"engine={engine}")
    if engine == "umi":
        run_umi(args.src, dest)
    elif engine == "tesseract":
        run_tesseract(args.src, dest)
    else:
        run_windows_ocr(args.src, dest)

    text = dest.read_text(encoding="utf-8", errors="replace")
    print(f"wrote {dest} ({len(text)} chars)")
    if args.media_json:
        append_media_row(args.media_json, args.src, dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
