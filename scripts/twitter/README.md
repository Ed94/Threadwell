# twitter

Emit Threadwell archive notes from a `thread_data.json` dump. No fetch. Lift and CRT snapshot are still manual.

## Emit

```
python C:\projects\Threadwell\scripts\twitter\emit_archive.py --input C:\projects\manual_slop\docs\twitter\2064858927829745887 --vault C:\projects\Threadwell --slug steamos-init --archived 2026-08-23
```

`--tip <id>` climbs same-handle `reply_to` and uses that chain as `index.md`.

`--all` skips a dump whose `post_id` already exists unless `--force`.

`--force` rewrites `media.json` to orig-only. Restore CRT/OCR rows with `media_merge.py`.

## Tip graph (no vault writes)

```
python C:\projects\Threadwell\scripts\twitter\graph_dry_run.py --input C:\projects\manual_slop\docs\twitter\<id>
```

## CRT (stock slang only)

`crt_pass.py` nearest-scales, then runs **unpatched** `crt-lottes-multipass.slangp` / `crt-Cyclon.slangp` via `librashader-cli`. It does not edit shaders. ShaderGlass snapshot is still the look reference.

```
python C:\projects\Threadwell\scripts\twitter\crt_pass.py --in ORIG.png --out CRT.png --preset cyclon --nn 3 --shader-scale 100% --dry-run
```

`--nn 3` is Affinity 300%. `--shader-scale` is librashader `-d`. `--shaderglass` only launches the .sgp.

If the plate is wrong, snapshot ShaderGlass yourself and drop `*_crt.png` next to the orig, then `media_merge.py`.

## OCR

```
python C:\projects\Threadwell\scripts\twitter\ocr_pass.py --in ORIG.png --media-json THREAD\media.json
```

Prefers `umi-ocr` (`scoop install extras/umi-ocr`), then tesseract, then Windows.Media.Ocr. Writes `*_ocr.txt`. ShareX has no OCR CLI.

## Select CRT vs orig in the note

```
python C:\projects\Threadwell\scripts\twitter\media_embed.py --thread ASSETS_THREAD --notes ARCHIVE_THREAD --media-id GBgHT_2WIAAKuNq --show crt
python C:\projects\Threadwell\scripts\twitter\media_embed.py --thread ASSETS_THREAD --notes ARCHIVE_THREAD --media-id GBgHT_2WIAAKuNq --attach-ocr
```

## Lift to catbox

```
python C:\projects\Threadwell\scripts\twitter\lift_catbox.py --thread ASSETS_THREAD --notes ARCHIVE_THREAD --orig
```

Reads `[catbox] userhash` from `secrets/credentials.toml`. Never prints it. Rewrites `Media (not lifted): \`file\`` to `![](https://files.catbox.moe/…)`.

## Restore extra media.json rows

```
python C:\projects\Threadwell\scripts\twitter\media_merge.py --thread ASSETS_THREAD
```

## Frozen Onat

`do_not_refetch.txt` — do not overwrite those three dumps.
