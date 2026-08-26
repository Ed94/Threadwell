---
title: How threads are organized
type: note
source: original
date: 2026-08-23
draft: false
tags:
  - note
  - how-to
description: How archived Twitter/X threads are filed and read.
---

Threads are grouped by **author handle**, then by **date and a short title**.

```
archive/threads/<handle>/<YYYY-MM-DD-slug>/
  index.md              ← the author's own chain (the spine)
  YYYY-MM-DD-who-slug.md  ← one file per reply that left that chain
```

## Spine

`index.md` is the opening author's chain. Posts are numbered **1/** **2/**. Each number line names who spoke: `**1/** @SebAaltonen`. Reply `@handles` sit on the next line. The tweet text starts after that. A mention inside the tweet is not the author.

Cross-author spines list every post in time order. The handle on the number line is who spoke.

If the first post is a reply to someone else, that other tweet is quoted at the top as context. It is not numbered as part of the spine.

If a spine post quotes another tweet, the quoted tweet has its
own thread folder. Under the quoting post: the x.com status URL,
then a link to that folder. The shortened t.co link in the tweet
stays as written.

## Branches

A reply from someone else, or a second chain the author started from an earlier post, is its own note in the same folder. Follow-ups on that reply stay in that note, including if the original author answers there.

The spine links out under the post that grew the branch. Each branch note links back to `index`.

## Cross-author conversations

When a thread alternates between authors, the folder belongs to the opening post. The spine walks every post in time order. Replies stay in that folder. The other authors do not get a second copy.

## Tags

Every thread starts with `archive`, `twitter`, and the author's handle. Topic tags (`vulkan`, `crt`, `alsa`, …) are added by hand when the thread is reviewed.

## Images

Pictures on the site are the original host URLs. Working copies live outside what GitHub Pages serves. A note still being prepared is marked `draft: true` and stays off the site.

## Reading

Start at [[archive/threads/index|Threads]], pick a handle, then a date. The spine is the essay. Branch files are the conversation around it.

On the site: click an image to enlarge it (Esc or click to close). Use **Wide** to grow the reading column.

To point a note at one reply, wikilink the block id on that post:

`[[archive/threads/SebAaltonen/2025-03-08-stupid-hardware-question-why-does-amd-use-several/2025-03-08-NOTimothyLottes-actually-this-is-a-super-important-question-imo#^1898440015182729598]]`
