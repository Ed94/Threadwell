---
title: "@NOTimothyLottes This is super cool, but why map a file and not just stdout?"
type: archive
source: twitter
source_url: "https://x.com/static_assert_0/status/1857867668289663108"
author: "static_assert(false)"
handle: static_assert_0
post_id: "1857867668289663108"
date: 2024-11-16
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes This is super cool, but why map a file and not just stdout?"
in_reply_to: ""
parent_post_id: "1857803914604618029"
---

## Source

- URL: https://x.com/static_assert_0/status/1857867668289663108
- Author: static_assert(false) (@static_assert_0)
- Posted: 2024-11-16 19:25:44

## Branch

**1/** @static_assert_0

@NOTimothyLottes

This is super cool, but why map a file and not just stdout?

**2/** @vodangkhoa873

@static_assert_0 @NOTimothyLottes

The writes can be done concurrently from many threads?

**3/** @NOTimothyLottes

@vodangkhoa873 @static_assert_0

Yes, one 'atomicAdd(atomAdr,1)&65535' to get the line number (window of 65536 max lines) then write the line individually. Only contention is on that atomicAdd CPU instruction which is as minimal as possible.

I do the atomic add instruction using simple inline ASM (below)

![](https://pbs.twimg.com/media/GciHgZzXIAAD9by?format=png&name=orig)

**4/** @static_assert_0

@NOTimothyLottes @vodangkhoa873

I love this, but are you not able to get that codegen with intrinsics or just normal C?

**5/** @NOTimothyLottes

@static_assert_0 @vodangkhoa873

I've been hand rolling intrinsics CPU-side in GCC with inline asm since the dawn of support for that. So haven't kept up with the high-level-lang mess fire since.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2024-11-16-0-what-a-horrible-term-printf-debugging]]
