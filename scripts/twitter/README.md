# twitter

Front door: `tw.py`. Individual scripts still work.

From the vault root:

```
python scripts/twitter/tw.py locate  --id <snowflake>
python scripts/twitter/tw.py graph   --id <snowflake>
python scripts/twitter/tw.py refresh --id <snowflake> --tip
python scripts/twitter/tw.py lift    --id <snowflake> --orig
python scripts/twitter/tw.py ocr     --id <snowflake>
```

`paths.py` sets vault = two parents above this file, dumps = `../manual_slop/docs/twitter`, scratch = `../Threadwell-ai/scratch`.

`refresh` = refetch (cookies) + ingest + emit `--force` + media_merge. `--tip` treats `--id` as the tip (climb same-handle `reply_to`). Does not flip `draft`. Does not commit. Frozen Onat ids abort.

Usual publish path after you like the note:

1. `tw.py graph --id …` — confirm tip vs root.
2. `tw.py refresh --id … --tip` if the dump stored a tip as root.
3. `tw.py lift --id … --orig` — catbox + rewrite `![](https://…)`.
4. You set `draft: false` and commit.

Site wikilinks must be `[[archive/threads/<handle>/<date-slug>]]`. Short `[[slug]]` 404s.

## Pieces

| Script | Job |
|---|---|
| `tw.py` | locate / graph / refetch / emit / refresh / lift / ocr / merge |
| `graph_dry_run.py` | tip graph, no vault writes |
| `ingest_gallery.py` | gallery-dl JSON → `thread_data.json` |
| `emit_archive.py` | JSON → notes + assets. `--force` now keeps CRT/OCR rows and prior catbox URLs |
| `lift_catbox.py` | upload `publish: true` (or `--orig`) |
| `ocr_pass.py` | Umi HTTP `:1224` / tesseract / Windows OCR |
| `media_embed.py` | `--show crt` / `--attach-ocr` |
| `media_merge.py` | restore extra rows if you still need it |
| `crt_pass.py` | stock slang only; ShaderGlass is the look reference |
| `do_not_refetch.txt` | Onat freeze list |

Secrets: `secrets/twitter_cookies.txt`, `secrets/credentials.toml` `[catbox] userhash`. Never print them.
