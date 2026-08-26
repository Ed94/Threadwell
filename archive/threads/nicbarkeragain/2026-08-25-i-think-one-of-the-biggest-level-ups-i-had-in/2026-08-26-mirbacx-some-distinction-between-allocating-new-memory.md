---
title: "some distinction between allocating new memory, copying src->dst, and then freeing src."
type: archive
source: twitter
source_url: "https://x.com/mirbacx/status/2092402560745570814"
author: "mirbacx"
handle: mirbacx
post_id: "2092402560745570814"
date: 2026-08-26
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - nicbarkeragain
description: "some distinction between allocating new memory, copying src->dst, and then freeing src."
in_reply_to: ""
parent_post_id: "2092391605882028391"
---

## Source

- URL: https://x.com/mirbacx/status/2092402560745570814
- Author: mirbacx (@mirbacx)
- Posted: 2026-08-26 00:03:40

## Branch

**1/** **@mirbacx** ^2092402560745570814

some distinction between allocating new memory, copying src->dst, and then freeing src. copying/moving is expensive.

updating pointers (to point to elsewhere in already allocated memory) is different.

there's also the matter of data locality. the cpu prefetches data (from RAM) onto caches. only so much can fit closest to the CPU (L1), so you don't want your algos accessing memory all over the place (eg, linked lists). "cache misses"

## Related

- Spine: [[archive/threads/nicbarkeragain/2026-08-25-i-think-one-of-the-biggest-level-ups-i-had-in]]
