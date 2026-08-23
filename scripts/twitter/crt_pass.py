"""Apply a stock RetroArch slang preset to a still via librashader-cli.

Does not patch shaders. Does not invent PixelSize. Your ShaderGlass .sgp files
are the look reference; this only runs the same .slangp with the listed params.

Manual look you are matching:
  1. Nearest-upscale the orig (Affinity zoom). 300% => 3x.
  2. Overlay ShaderGlass with the .sgp (Cyclon PixelSize 6, Lottes PixelSize 4).
  3. Snapshot, then crop.

This script can do step 1 (ffmpeg neighbor) and a stock slang render of the
result. It cannot reproduce ShaderGlass window capture. If the plate is wrong,
do it in ShaderGlass and drop the PNG next to the orig as *_crt.png.

Presets:
  lottes  crt-lottes-multipass.slangp
          LOTTES_CODE_(LOTTES_MULTIPASS 2X) V2.sgp
  cyclon  crt-Cyclon.slangp
          LOTTES_CRT_CODE_(CYCLON 6X).sgp

auto: cyclon if max(w,h) <= --auto-max (default 720), else lottes.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

LOTTES_SGP = Path(
    r"C:\Users\Ed\Downloads\ShaderGlass-1.2.2-win-x64"
    r"\LOTTES_CODE_(LOTTES_MULTIPASS 2X) V2.sgp"
)
CYCLON_SGP = Path(
    r"C:\Users\Ed\Downloads\ShaderGlass-1.2.2-win-x64"
    r"\LOTTES_CRT_CODE_(CYCLON 6X).sgp"
)
SLANG_LOTTES = Path(
    r"C:\Users\Ed\scoop\apps\retroarch\1.22.2\shaders"
    r"\shaders_slang\crt\crt-lottes-multipass.slangp"
)
SLANG_CYCLON = Path(
    r"C:\Users\Ed\scoop\apps\retroarch\1.22.2\shaders"
    r"\shaders_slang\crt\crt-Cyclon.slangp"
)
CLI_DEFAULT = Path(r"C:\Users\Ed\scoop\apps\librashader\0.12.0\librashader-cli.exe")

# Knobs copied from the .sgp files. Not a substitute for PixelSize.
LOTTES_PARAMS = (
    "hardScan=-19,hardPix=-7,warpX=0,warpY=0,maskDark=1.3,maskLight=1.3,"
    "shadowMask=4,brightBoost=1.15,bloomAmount=0,shape=1.9"
)
CYCLON_PARAMS = (
    "SCANLINE=0.2,INTERLACE=0,M_TYPE=0,SLOT=0,SLOTW=2,Maskl=0.55,Maskh=1,"
    "bzl=0,ambient=0,REFLECT=0,WARPX=0,WARPY=0,BR_DEP=0,BRIGHTNESS_=1.05,"
    "BLACK=0.01,vig=0"
)


def probe_size(path: Path) -> tuple[int, int]:
    raw = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "json",
            str(path),
        ],
        text=True,
    )
    stream = json.loads(raw)["streams"][0]
    return int(stream["width"]), int(stream["height"])


def pick_preset(width: int, height: int, name: str, auto_max: int) -> tuple[str, Path, Path, str]:
    if name == "auto":
        name = "cyclon" if max(width, height) <= auto_max else "lottes"
    if name == "lottes":
        return name, LOTTES_SGP, SLANG_LOTTES, LOTTES_PARAMS
    if name == "cyclon":
        return name, CYCLON_SGP, SLANG_CYCLON, CYCLON_PARAMS
    raise SystemExit(f"unknown preset {name}")


def find_cli(explicit: Path | None) -> Path:
    if explicit is not None:
        if not explicit.is_file():
            raise SystemExit(f"missing --cli {explicit}")
        return explicit
    which = shutil.which("librashader-cli")
    if which:
        return Path(which)
    if CLI_DEFAULT.is_file():
        return CLI_DEFAULT
    raise SystemExit(
        "librashader-cli not on PATH. Install or pass --cli. "
        "Stock binary lives at "
        r"C:\Users\Ed\scoop\apps\librashader\0.12.0\librashader-cli.exe"
    )


def parse_crop(spec: str) -> str | None:
    if spec in ("none", "", "off"):
        return None
    if spec == "auto":
        return "auto"
    parts = [int(p) for p in spec.replace(" ", "").split(",")]
    if len(parts) != 4:
        raise SystemExit("--crop wants auto, none, or L,T,R,B")
    left, top, right, bottom = parts
    return f"crop=iw-{left + right}:ih-{top + bottom}:{left}:{top}"


def detect_crop(path: Path) -> str | None:
    proc = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(path),
            "-vf",
            "cropdetect=limit=24:round=2:reset=0",
            "-frames:v",
            "1",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    crop = None
    for line in (proc.stderr or "").splitlines():
        if "crop=" in line:
            crop = line.rsplit("crop=", 1)[-1].strip()
    return f"crop={crop}" if crop else None


def run_ffmpeg(src: Path, dest: Path, vf: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(src),
            "-vf",
            vf,
            "-frames:v",
            "1",
            "-update",
            "1",
            str(dest),
        ]
    )


def run_librashader(
    cli: Path,
    slang: Path,
    src: Path,
    dest: Path,
    *,
    runtime: str,
    dimensions: str,
    params: str,
) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(cli),
        "render",
        "-r",
        runtime,
        "-d",
        dimensions,
        "--params",
        params,
        "-p",
        str(slang),
        "-i",
        str(src),
        "-o",
        str(dest),
    ]
    print(" ".join(cmd))
    subprocess.check_call(cmd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="src", type=Path, required=True)
    parser.add_argument("--out", dest="dest", type=Path, required=True)
    parser.add_argument("--preset", choices=("auto", "lottes", "cyclon"), default="auto")
    parser.add_argument(
        "--nn",
        type=int,
        default=1,
        help="nearest integer pre-scale (Affinity zoom). 1 = none, 3 = 300%%",
    )
    parser.add_argument(
        "--shader-scale",
        default="100%",
        help="librashader -d on the (possibly nn-scaled) image. 100%%, 300%%, 600%%, or WIDTHxHEIGHT",
    )
    parser.add_argument("--runtime", default="d3d11")
    parser.add_argument("--auto-max", type=int, default=720)
    parser.add_argument("--crop", default="none", help="auto | none | L,T,R,B")
    parser.add_argument("--cli", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--shaderglass",
        action="store_true",
        help="launch ShaderGlass with the matching .sgp (manual snapshot)",
    )
    parser.add_argument(
        "--nn-only",
        action="store_true",
        help="only do the neighbor pre-scale; do not call librashader",
    )
    args = parser.parse_args(argv)

    if not args.src.is_file():
        raise SystemExit(f"missing {args.src}")
    if args.nn < 1:
        raise SystemExit("--nn must be >= 1")

    width, height = probe_size(args.src)
    name, sgp, slang, params = pick_preset(width, height, args.preset, args.auto_max)
    print(f"size {width}x{height} preset={name} nn={args.nn} shader-scale={args.shader_scale}")
    print(f"sgp {sgp}")
    print(f"slang {slang}")

    work = args.src
    tmp_nn: Path | None = None
    if args.nn > 1:
        tmp_nn = args.dest.with_name(args.dest.stem + f"_nn{args.nn}.png")
        vf = f"scale=iw*{args.nn}:ih*{args.nn}:flags=neighbor,format=rgba"
        print("ffmpeg", "-i", work, "-vf", vf, tmp_nn)
        if not args.dry_run:
            run_ffmpeg(work, tmp_nn, vf)
        work = tmp_nn

    if args.nn_only:
        if tmp_nn is None:
            raise SystemExit("--nn-only needs --nn > 1")
        if not args.dry_run:
            shutil.copy2(tmp_nn, args.dest)
        print(f"wrote {args.dest} (nn only)")
        return 0

    cli = None if args.dry_run else find_cli(args.cli)
    if args.dry_run:
        print(
            "librashader-cli render",
            "-r",
            args.runtime,
            "-d",
            args.shader_scale,
            "--params",
            params,
            "-p",
            slang,
            "-i",
            work,
            "-o",
            args.dest,
        )
    else:
        assert cli is not None
        if not slang.is_file():
            raise SystemExit(f"missing slang {slang}")
        run_librashader(
            cli,
            slang,
            work,
            args.dest,
            runtime=args.runtime,
            dimensions=args.shader_scale,
            params=params,
        )

    crop_spec = parse_crop(args.crop)
    if crop_spec == "auto" and not args.dry_run:
        crop_filter = detect_crop(args.dest)
        if crop_filter:
            cropped = args.dest.with_name(args.dest.stem + "_crop.png")
            run_ffmpeg(args.dest, cropped, crop_filter)
            shutil.move(str(cropped), str(args.dest))
    elif crop_spec and crop_spec != "auto" and not args.dry_run:
        cropped = args.dest.with_name(args.dest.stem + "_crop.png")
        run_ffmpeg(args.dest, cropped, crop_spec)
        shutil.move(str(cropped), str(args.dest))

    print(f"wrote {args.dest}")
    if args.shaderglass:
        exe = shutil.which("shaderglass") or shutil.which("ShaderGlass")
        if not exe:
            raise SystemExit("shaderglass not on PATH")
        subprocess.Popen([exe, str(sgp)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
