# twitter

Front door: `tw.py`. Run from the vault root.

```
python scripts/twitter/tw.py graph --id <snowflake>
python scripts/twitter/tw.py refresh --id <spine-tip> --tip
python scripts/twitter/tw.py refresh --id <spine-tip> --tip --branch <branch-tip>
python scripts/twitter/tw.py add-branch --id <original-spine-tip> --from <reply-node>
python scripts/twitter/tw.py emit --id <spine-tip> --tip --preserve-existing
python scripts/twitter/tw.py audit-media --id <snowflake>
python scripts/twitter/tw.py publish --id <snowflake>
python scripts/twitter/tw.py sync --handle <handle>
python scripts/twitter/tw.py backup --id <snowflake>
python scripts/twitter/tw.py fallback --id <snowflake> --media-id <id> --role <role> --confirm-origin-unavailable
python scripts/twitter/tw.py restore-origin --id <snowflake> --media-id <id>
python scripts/twitter/tw.py migrate-media --id <snowflake>
python scripts/twitter/tw.py reslug --all
python scripts/twitter/tw.py reslug --all --apply
python scripts/twitter/tw.py relabel --all
python scripts/twitter/tw.py relabel --all --apply
```

`paths.py` finds the vault two parents above this file. Dumps live at `../manual_slop/docs/twitter`. Scratch lives at `../Threadwell-ai/scratch`.

## Capture

`refresh` is refetch + ingest + emit `--force` + media merge. `--tip` treats `--id` as the tip and walks back to the opening post. If that tip is the OP, same-handle self-replies stay on the spine and foreign replies are branches. Repeat `--branch <tip-id>` to capture extra tips into the same `thread_data.json`. It does not invent replies. Captures run one at a time. gallery-dl retries are off. Extractor and request sleeps are five seconds. Re-emit deletes branch notes that are no longer roots.

Each thread writes one archive folder. The owner is the opening post (`reply_to_id` is empty). Other authors stay in that folder. New notes set `draft: false`. The command does not commit. Frozen ids abort.

For a thread already on disk, stage with `refetch`, compare ids, then:

```
python scripts/twitter/tw.py emit --id <spine-tip> --tip --preserve-existing
```

Fresh records win for ids the provider returned. Posts only in the existing `thread_data.json` stay if both captures share a conversation root. That stops an incomplete gallery-dl run from deleting archived replies.

`add-branch` extends an emitted thread. `--id` is the stored spine tip. Each `--from <reply-node>` is captured once. The command keeps that node's missing attachment path and the visible descendant subtree, merges new posts, downloads their media, and re-emits with the spine unchanged. Existing media rows stay. New media get origin and local-copy rows. A visible leaf is only the deepest reply that capture returned.

Usual path:

1. `tw.py graph --id …` — confirm tip vs root.
2. `tw.py refresh --id … --tip` if the dump stored a tip as root.
3. `tw.py audit-media --id …` — confirm origin URLs are selected.

Site wikilinks must be `[[archive/threads/<handle>/<date-slug>]]`. Short `[[slug]]` 404s.

## Media

Published images cite the original host URL. A local copy stays under `assets/threads/<handle>/<date-slug>/`. `backup` copies that tree to the configured store. `fallback` uploads one file after the origin is gone. `media.json` keeps the origin URL and every fallback URL.

`lift` is retired. Use `fallback` for one item, or `restore-origin` to select the original URL again.

Frozen threads (any captured post id listed in `do_not_refetch.txt`) are read-only for refetch, refresh, emit, migration, rewrite, fallback, and backup. `audit-media` may still inspect them.

## Thread directories

A thread folder is named from the title in `index.md`: `<YYYY-MM-DD>-<slug>`. `reslug --all` reports every mapping. `reslug --all --apply` preflights, refuses the whole apply on any non-frozen conflict, and moves assets first. If the archive move fails, assets roll back. An occupied destination aborts. Frozen ids are reported and skipped.

Later emits use that same title for the folder and the frontmatter. Move both sides together. Each old archive prefix is replaced once in mutable `*.md` and `*.canvas` outside `.git/`, `site/`, `assets/`, `secrets/`, `node_modules/`, and frozen archive dirs.

`relabel --all` patches existing `**N/**` lines to `**N/** @handle` from on-disk `thread_data.json`. No scrape. No folder rename. `--apply` writes notes only.

## Secrets

`secrets/twitter_cookies.txt` and `secrets/credentials.toml` stay on the machine that runs the capture. The scripts read them. They never print them. The Catbox hash goes in an HTTPS form body, not on a process command line. The backup command prints `synced` or `error`, not the destination path.

## Pieces

| Script | Job |
|---|---|
| `tw.py` | locate / graph / refetch / add-branch / emit / refresh / ocr / merge / sync / publish / migrate-media / backup / fallback / restore-origin / reslug / relabel |
| `graph_dry_run.py` | tip graph, no vault writes |
| `ingest_gallery.py` | gallery-dl JSON → `thread_data.json` |
| `emit_archive.py` | JSON → notes + assets. `--force` keeps derived and fallback rows |
| `media_migrate.py` | old `media.json` → location records, dry-run or apply |
| `media_audit.py` | local integrity, reference counts, mirror freshness, optional origin check |
| `media_manifest.py` | schema, validation, merge, selection, atomic I/O |
| `media_refs.py` | media-aware markup and note rewrite planning |
| `backup_assets.py` | hash-verified copy of one thread asset dir |
| `catbox_client.py` | one Catbox upload |
| `fallback_media.py` | fallback activation and restore-origin |
| `frozen.py` | resolve frozen ids against every captured post id |
| `lift_catbox.py` | retired. Use `tw.py fallback` |
| `ocr_pass.py` | Umi HTTP `:1224` / tesseract / Windows OCR |
| `media_embed.py` | `--attach-ocr` only |
| `media_merge.py` | restore derived rows |
| `crt_pass.py` | stock slang only. ShaderGlass is the look reference |
| `do_not_refetch.txt` | frozen id list |
| `tests/` | isolated unit tests |
| `unfinished_bloat/` | leftover probe code. Not the front door |
