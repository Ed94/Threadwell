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

`index.md` is only what the author posted as a single chain: each post replies to the previous one of theirs. Posts are numbered **1/** **2/** in that order. Other people do not appear in this numbering.

If the first post is a reply to someone else, that other tweet is quoted at the top as context. It is not numbered as part of the spine.

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
