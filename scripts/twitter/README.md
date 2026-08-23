# twitter

Emit Threadwell archive notes from a `thread_data.json` dump. No fetch, no lift.

## One dump

```
python C:\projects\Threadwell\scripts\twitter\emit_archive.py --input C:\projects\manual_slop\docs\twitter\2064858927829745887 --vault C:\projects\Threadwell --slug steamos-init --archived 2026-08-23
```

`--input` is the dump directory. `--vault` is the Threadwell root. `--slug` overrides the directory slug. `--archived` is `YYYY-MM-DD` and defaults to today.

## All dumps

```
python C:\projects\Threadwell\scripts\twitter\emit_archive.py --all C:\projects\manual_slop\docs\twitter --vault C:\projects\Threadwell --archived 2026-08-23
```

Skips a dump whose `post_id` already exists in the vault unless `--force`. No fetch, no lift.

The converter writes the spine and branch notes under `archive/threads/<handle>/<date-slug>/` and a working copy under `assets/threads/<handle>/<date-slug>/` (`thread_data.json`, `media.json`, `gaps.md`, and any local media). Media is not published.
