---
title: "@NOTimothyLottes nanosleep(0) will sleep for the timer slack"
type: archive
source: twitter
source_url: "https://x.com/raggi/status/2065865513608307103"
author: "James Tucker"
handle: raggi
post_id: "2065865513608307103"
date: 2026-06-13
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes nanosleep(0) will sleep for the timer slack"
in_reply_to: ""
parent_post_id: "2065840191340707905"
---

## Source

- URL: https://x.com/raggi/status/2065865513608307103
- Author: James Tucker (@raggi)
- Posted: 2026-06-13 18:34:55

## Branch

**1/** @raggi

@NOTimothyLottes

nanosleep(0) will sleep for the timer slack

_mm_pause() if you want to avoid a context switch and keep your scheduler quantum

**2/** @NOTimothyLottes

@raggi

I do that via inline asm to save power. This was more a comment on the cost of actually using the futex system call, need to be careful about the call frequency

## Related

- Spine: [[archive/threads/NOTimothyLottes/2026-06-13-interesting-how-on-this-linux-box-scheduling-nops]]
