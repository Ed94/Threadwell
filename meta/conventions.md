---
title: Conventions
type: note
status: draft
draft: true
---

# Frontmatter

| Field | Values | Notes |
| --- | --- | --- |
| `type` | `archive` \| `canvas` \| `note` | Required |
| `source` | `twitter` \| `discord` \| `youtube` \| `odysee` \| `article` \| `original` \| `other` | Archive + media notes |
| `source_url` | URL | This note's post, not always the thread root |
| `author` | string | Display name |
| `handle` | string | Username without `@` |
| `post_id` | string | Twitter status id (spine root or branch root) |
| `date` | `YYYY-MM-DD` | Original publication date |
| `archived` | `YYYY-MM-DD` | When you captured it |
| `status` | `draft` \| `review` \| `published` | Human workflow |
| `draft` | `true` \| `false` | Quartz omit-from-site flag |
| `tags` | list | Ingest: `archive`, `twitter`, handle. Topics by hand |
| `description` | string | Search / OG preview |
| `aliases` | list | Extra names |
| `in_reply_to` | string | Foreign parent of a spine, if any |
| `parent_post_id` | string | Branch notes only: post this branch replies to |

`draft: true` hides the page from the built site. It does **not** hide the file from a public GitHub repo. Truly private material goes in `private/` (gitignored).

# Folders

| Path | Published | Role |
| --- | --- | --- |
| `archive/` | yes | Primary sources |
| `archive/threads/<handle>/<YYYY-MM-DD-slug>/` | yes | One Twitter thread. `index.md` is the author's chain |
| `canvases/` | yes | `.canvas` maps |
| `notes/` | yes | Authored writing |
| `templates/` | no | Templater / core templates |
| `meta/` | no | Vault rules, local attachments |
| `assets/` | no, gitignored | Working media before upload |
| `secrets/` | no, gitignored | Cookies and image-host credentials |
| `scripts/` | no | Tracked tooling. Quartz-ignored |
| `private/` | no, gitignored | Never publish, never push |
| `site/` | no, gitignored | Local Quartz clone (own remotes) |
| `publish/` | no | Tracked Quartz overlay |

A thread folder holds `index.md` (spine) and one markdown file per off-spine reply tree. Reading guide: `notes/How threads are organized.md`.

# Images

Always absolute HTTPS URLs from the original provider when possible (`pbs.twimg.com`, `video.twimg.com`). The vault also retains a local, unpublished copy under `assets/` using the same relative taxonomy as the archive. A separately requested backup may mirror those assets to configured storage; alternative-host uploads are a manual fallback used only after the origin is confirmed unavailable, and the original URL and every fallback URL remain recorded in `media.json`. Do not commit local binaries for published notes. Working files sit in `assets/` (gitignored), not in `meta/attachments/` except unrelated Obsidian drops.

```md
![](https://files.catbox.moe/example.png)
```

# Video

YouTube / tweet (Quartz OFM):

```md
![](https://www.youtube.com/watch?v=VIDEO_ID)
![](https://youtu.be/VIDEO_ID)
![](https://x.com/user/status/ID)
```

Odysee (raw iframe; survives the static build):

```html
<iframe width="560" height="315" src="https://odysee.com/$/embed/SLUG/CLAIM" allowfullscreen></iframe>
```

Get the embed URL from Odysee share → embed. Do not use the watch URL as the iframe `src`.
