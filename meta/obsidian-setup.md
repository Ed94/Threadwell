---
title: Obsidian setup
type: note
status: draft
draft: true
---

Open **`C:\\projects\\Threadwell`** as the vault (the repo root). `site/` is a local Quartz checkout and is hidden from the file explorer.

# Core plugins

Enable: Files, Search, Quick switcher, Graph, Backlinks, Canvas, Outgoing links, Tags, Page preview, Templates, Note composer, Command palette, Properties, Word count, File recovery.

Templates folder: `templates`.

# Community plugins

| Plugin | Why |
| --- | --- |
| Templater | Date/title fill-in for the two starter templates |
| Dataview | Local queries over `type`, `source`, `status` (not rendered by Quartz) |
| Linter | YAML key order and tag consistency |
| Media Extended | Better YouTube/timestamp playback inside Obsidian |
| Advanced Canvas | Groups, presentation, nicer maps; Quartz still reads stock JSON Canvas |

Install from Community Plugins using `.obsidian/community-plugins.json`.

# Templater

Template folder: `templates`. Enable "Trigger Templater on new file creation" if you want folder templates later.

# Linter (suggested)

- YAML: insert `date` as `YYYY-MM-DD`
- Deduplicate and sort tags
- Do not rewrite wikilinks to markdown links

# Link settings

Already set in `app.json`: wikilinks, shortest path, update links on rename.
