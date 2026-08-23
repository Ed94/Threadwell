# Threadwell

Recovered threads and submerged records.

An [Obsidian](https://obsidian.md) vault published with [Quartz 5](https://quartz.jzhao.xyz) to GitHub Pages. The site is a convenient host for Twitter/X threads and other material that is not reliably web-indexed.

Live (after Pages is enabled): https://ed94.github.io/Threadwell

## Layout

Open **this repo root** as the Obsidian vault. Quartz is only the publisher; it lives in `site/`.

```
archive/              # public — primary sources
  threads/<handle>/<YYYY-MM-DD-slug>/
                      # one thread: index.md is the author's chain
  sources/            # talks, pages, other records
canvases/             # public — .canvas maps
notes/                # public — authored / distilled writing
templates/            # not published
meta/                 # not published — conventions
assets/               # not published, gitignored — working media
secrets/              # not published, gitignored — cookies, host keys
private/              # not published, not pushed
publish/              # tracked overlay: quartz.config.yaml
site/                 # local Quartz clone (gitignored; own remotes)
.obsidian/
.github/workflows/deploy.yml
```

`archive/`, `canvases/`, and `notes/` are public by default. `site/` is a separate git checkout of Quartz (`origin` → `jackyzha0/quartz`). Threadwell's only remote is `Ed94/Threadwell`.

## Frontmatter

| Field | Values |
| --- | --- |
| `type` | `archive` \| `canvas` \| `note` |
| `source` | `twitter` \| `youtube` \| `odysee` \| `article` \| `original` \| `other` |
| `source_url` | original URL |
| `author` | original display name |
| `handle` | username without `@` |
| `post_id` | Twitter status id |
| `date` | original date `YYYY-MM-DD` |
| `archived` | capture date |
| `status` | `draft` \| `review` \| `published` |
| `draft` | `true` omits the page from the site |
| `tags`, `description`, `aliases` | as usual |

`draft: true` only hides a page from the **site**. A public GitHub repo still contains the file. Use `private/` for anything that must not be pushed.

Templates: `templates/archive-source.md`, `templates/authored-note.md` (Templater placeholders).

## Images and embeds

Images: absolute HTTPS URLs on your image host. Do not commit local binaries for published notes.

```md
![](https://files.catbox.moe/example.png)
```

Keep local copies in `assets/` (not committed). Do not point notes at `assets/` or `./media/`.

YouTube and tweets (Quartz Obsidian-flavored Markdown):

```md
![](https://www.youtube.com/watch?v=VIDEO_ID)
![](https://x.com/user/status/ID)
```

Odysee (iframe; copy the embed URL from Odysee share):

```html
<iframe width="560" height="315" src="https://odysee.com/$/embed/SLUG/CLAIM" allowfullscreen></iframe>
```

Remote URLs and iframes are left as-is in the static build.

## Obsidian plugins

| Plugin | Why |
| --- | --- |
| **Templater** | Fills dates/titles in the starter templates |
| **Dataview** | Local queries by `type` / `source` / `status` (not rendered on the site) |
| **Linter** | Consistent YAML |
| **Media Extended** | Better in-vault YouTube playback |
| **Advanced Canvas** | Stronger canvas editing; site still uses stock JSON Canvas |

Core: Canvas, Templates (folder `templates`), Backlinks, Graph, Properties, Page preview.

See `meta/obsidian-setup.md` and `meta/conventions.md`.

## Local preview

Needs Node 22+ and npm 10.9.2+.

```powershell
cd C:\projects\Threadwell
.\publish\setup.ps1
cd site
npx quartz build -d .. --serve
```

Open http://localhost:8080

`publish/setup.ps1` clones Quartz into `site/` if needed, then copies `publish/quartz.config.yaml` over the stock config.

## GitHub Pages

1. Repo Settings → Pages → Source: **GitHub Actions**
2. If an old `github-pages` environment blocks the first deploy, delete it under Settings → Environments. The workflow recreates it.
3. Push `main`. CI clones Quartz into `site/`, applies `publish/quartz.config.yaml`, builds with `-d ..`.
4. Site: `https://ed94.github.io/Threadwell`

`baseUrl` lives in `publish/quartz.config.yaml`. Change it if you attach a custom domain.

## Add content and republish

1. New thread: create `archive/threads/<handle>/<YYYY-MM-DD-slug>/`. Templater → `archive-source` → save as `index.md` (the author's chain). Off-spine replies get their own notes in that folder. See `notes/How threads are organized.md`.
2. Transcribe posts in order. Upload images to the image host; paste HTTPS URLs. Optional YouTube/Odysee/tweet embeds.
3. Distill in `notes/` with `authored-note`. Wikilink the archive record.
4. Set `draft: false` and `status: published` when the capture has been reviewed.
5. Preview: `cd site; npx quartz build -d .. --serve`
6. Commit and push `main` (vault + `publish/`, never `site/`, never `assets/` or `secrets/`)

Threadwell remotes: `origin` → https://github.com/Ed94/Threadwell.git only.
Quartz remotes live in `site/` (`cd site; git pull`). After a Quartz pull, re-copy `publish/quartz.config.yaml`.

## Quartz notes

Current major is **Quartz 5**. Edit `publish/quartz.config.yaml`, not the clone. Canvas uses `@quartz-community/canvas-page`. Drafts use `@quartz-community/remove-draft`.

Engine license: MIT (Quartz). Vault content: Unlicense (`LICENSE`).
