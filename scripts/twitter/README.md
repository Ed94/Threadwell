# twitter

Front door: `tw.py`. Individual scripts still work.

From the vault root:

```
python C:\projects\Threadwell\scripts\twitter\tw.py graph   --id <snowflake>
python C:\projects\Threadwell\scripts\twitter\tw.py refresh --id <snowflake> --tip
python C:\projects\Threadwell\scripts\twitter\tw.py audit-media --id <snowflake>
python C:\projects\Threadwell\scripts\twitter\tw.py publish --id <snowflake>
python C:\projects\Threadwell\scripts\twitter\tw.py sync    --handle <handle>
python C:\projects\Threadwell\scripts\twitter\tw.py backup  --id <snowflake>
python C:\projects\Threadwell\scripts\twitter\tw.py fallback --id <snowflake> --media-id <media-id> --role <role> --confirm-origin-unavailable
python C:\projects\Threadwell\scripts\twitter\tw.py restore-origin --id <snowflake> --media-id <media-id>
python C:\projects\Threadwell\scripts\twitter\tw.py migrate-media --id <snowflake>
python C:\projects\Threadwell\scripts\twitter\tw.py migrate-media --all --apply
```

`paths.py` sets vault = two parents above this file, dumps = `../manual_slop/docs/twitter`, scratch = `../Threadwell-ai/scratch`.

`refresh` = refetch (cookies) + ingest + emit `--force` + media_merge. `--tip` treats `--id` as the tip (climb same-handle `reply_to`). Does not flip `draft`. Does not commit. Frozen ids abort.

Usual publish path after you like the note:

1. `tw.py graph --id …` — confirm tip vs root.
2. `tw.py refresh --id … --tip` if the dump stored a tip as root.
3. `tw.py audit-media --id …` — confirm origin URLs are selected.
4. `tw.py publish --id …` sets `draft: false`. You commit.

Site wikilinks must be `[[archive/threads/<handle>/<date-slug>]]`. Short `[[slug]]` 404s.

## Media policy

Published Twitter/X media cites the original provider's HTTPS URL by default. The vault also retains a local, unpublished copy under `assets/threads/<handle>/<date-slug>/` using the same relative taxonomy as the archive. A separately requested backup may mirror those assets to configured storage. Alternative-host uploads are a manual fallback used only after the origin is confirmed unavailable; the original URL and every fallback URL remain recorded in `media.json`.

The `lift` command is retired. Use `fallback` for a single media item after explicit confirmation, or `restore-origin` to select the immutable provider URL again. The Catbox userhash and backup destination id/root are read from `secrets/credentials.toml` by the script. Never paste them into chat.

Frozen threads (ids listed in `do_not_refetch.txt`, matched against every captured post id) are read-only across refetch, refresh, emit, manifest migration, note rewrite, fallback, publication selection, and tracked backup operations. Read-only `audit-media` may still inspect them.

## Pieces

| Script | Job |
|---|---|
| `tw.py` | locate / graph / refetch / emit / refresh / ocr / merge / sync / publish / migrate-media / backup / fallback / restore-origin |
| `graph_dry_run.py` | tip graph, no vault writes |
| `ingest_gallery.py` | gallery-dl JSON → `thread_data.json` |
| `emit_archive.py` | JSON → notes + assets. Uses canonical media locations. `--force` preserves derived/fallback rows |
| `media_migrate.py` | legacy `media.json` → canonical locations, dry-run or apply |
| `media_audit.py` | local integrity, reference counts, mirror freshness, optional origin check |
| `media_manifest.py` | schema, validation, merge, selection, atomic I/O |
| `media_refs.py` | media-aware markup and note rewrite planning |
| `backup_assets.py` | sparse, hash-verified copy of one thread asset dir |
| `catbox_client.py` | one sanitized Catbox upload; no batching or retry |
| `fallback_media.py` | confirm-origin fallback activation and restore-origin |
| `frozen.py` | resolve frozen ids against every captured post id |
| `lift_catbox.py` | retired entry; points operators to `tw.py fallback` |
| `ocr_pass.py` | Umi HTTP `:1224` / tesseract / Windows OCR |
| `media_embed.py` | `--attach-ocr` only; refuses `--show crt` |
| `media_merge.py` | restore derived rows under canonical API |
| `crt_pass.py` | stock slang only; ShaderGlass is the look reference |
| `do_not_refetch.txt` | frozen id list |
| `tests/` | isolated, deterministic unit tests |

Secrets: `secrets/twitter_cookies.txt`, `secrets/credentials.toml` `[catbox] userhash` and `[backup] id`/`root`. The script reads them; never paste into chat, tests, or commits.