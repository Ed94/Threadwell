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
| `source` | `twitter` \| `youtube` \| `odysee` \| `article` \| `original` \| `other` | Archive + media notes |
| `source_url` | URL | Canonical original |
| `author` | string | Original author, not you |
| `date` | `YYYY-MM-DD` | Original publication date |
| `archived` | `YYYY-MM-DD` | When you captured it |
| `status` | `draft` \| `review` \| `published` | Human workflow |
| `draft` | `true` \| `false` | Quartz omit-from-site flag |
| `tags` | list | Prefer `archive`, `twitter`, `note`, topic slugs |
| `description` | string | Search / OG preview |
| `aliases` | list | Extra names |

`draft: true` hides the page from the built site. It does **not** hide the file from a public GitHub repo. Truly private material goes in `private/` (gitignored).

# Folders

| Path | Published | Role |
| --- | --- | --- |
| `archive/` | yes | Primary sources |
| `canvases/` | yes | `.canvas` maps |
| `notes/` | yes | Authored writing |
| `templates/` | no | Templater / core templates |
| `meta/` | no | Vault rules, local attachments |
| `private/` | no, gitignored | Never publish, never push |
| `site/` | no, gitignored | Local Quartz clone (own remotes) |
| `publish/` | no | Tracked Quartz overlay |

# Images

Always absolute HTTPS URLs on the image host. Do not commit local binaries for published notes.

```md
![](https://YOUR-IMAGE-HOST/archive/slug.png)
```

Scratch files may sit in `meta/attachments/` (gitignored).

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
