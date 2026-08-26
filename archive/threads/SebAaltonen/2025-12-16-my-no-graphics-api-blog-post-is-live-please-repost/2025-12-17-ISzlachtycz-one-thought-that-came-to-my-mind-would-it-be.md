---
title: "@SebAaltonen One thought that came to my mind, would it be preferable to have something akin to virtual alloc vs malloc for gpus? Its not a huge difference, but it does open up some opportunities (easy arenas, sparse buffers, extra mapped ring buffers, etc)?"
type: archive
source: twitter
source_url: "https://x.com/ISzlachtycz/status/2001218056467484857"
author: "Ihor_Szlachtycz 🇺🇦"
handle: ISzlachtycz
post_id: "2001218056467484857"
date: 2025-12-17
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen One thought that came to my mind, would it be preferable to have something akin to virtual alloc vs malloc for gpus? Its not a huge difference, but it does open up some opportunities (easy arenas, sparse buffers, extra mapped ring buffers, etc)?"
in_reply_to: ""
parent_post_id: "2001000839574643138"
---

## Source

- URL: https://x.com/ISzlachtycz/status/2001218056467484857
- Author: Ihor_Szlachtycz 🇺🇦 (@ISzlachtycz)
- Posted: 2025-12-17 09:09:00

## Branch

**1/** **@ISzlachtycz** ^2001218056467484857

**@SebAaltonen**

One thought that came to my mind, would it be preferable to have something akin to virtual alloc vs malloc for gpus? Its not a huge difference, but it does open up some opportunities (easy arenas, sparse buffers, extra mapped ring buffers, etc)?

**2/** **@SebAaltonen** ^2007110514221134175

**@ISzlachtycz**

Yes. I had thoughts about virtual malloc, but removed in cleanup. GPU vendors have different page sizes and tiled textures have different layouts. Lots of complexity there. Would need deeper dive on that topic and I just didn't have time to do write about that. Scope bloat...

## Related

- Spine: [[archive/threads/SebAaltonen/2025-12-16-my-no-graphics-api-blog-post-is-live-please-repost]]
