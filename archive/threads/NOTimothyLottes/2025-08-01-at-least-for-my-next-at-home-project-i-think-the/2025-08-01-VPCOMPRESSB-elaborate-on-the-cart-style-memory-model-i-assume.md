---
title: "elaborate on the \"CART\"-style memory model?"
type: archive
source: twitter
source_url: "https://x.com/VPCOMPRESSB/status/1951359238787186957"
author: "/i:'mɪər/"
handle: VPCOMPRESSB
post_id: "1951359238787186957"
date: 2025-08-01
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "elaborate on the \"CART\"-style memory model?"
in_reply_to: ""
parent_post_id: "1951346857017250014"
---

## Source

- URL: https://x.com/VPCOMPRESSB/status/1951359238787186957
- Author: /i:'mɪər/ (@VPCOMPRESSB)
- Posted: 2025-08-01 19:07:51

## Branch

**1/** @VPCOMPRESSB

elaborate on the "CART"-style memory model?

i assume you initialize with the default start-up state that's maybe loaded from disk into a static buffer (the "CART"). you read from the CART, then perform transformations in a separate region of [dynamic] memory (the pool), and periodically copy data from the pool back into the CART (the snapshots)?

saving the game would then just be copying a region to disk contiguously—zero fragmentation. which means you can stream-in data linearly, provided that the layout of the CART maps to the ordering of the transformation stages. you can also compress the data in the CART quiet well i imagine. you can implement this as a double buffering system? the CART used strictly for rendering, and the pool strictly for transformations?

**2/** @NOTimothyLottes

@VPCOMPRESSB

There is a Vulkan extension on PC that enables one to take a mapped file (aka the page cache) and access it from the GPU directly.

**3/** @AgileJebrim

@NOTimothyLottes @VPCOMPRESSB @VPCOMPRESSB

I believe the benefit here is that it avoids an extra copy.

https://registry.khronos.org/vulkan/specs/latest/man/html/VK_EXT_external_memory_host.html

**4/** @VPCOMPRESSB

@AgileJebrim @NOTimothyLottes

that API seems very opaque. how can a person tell/preset the size and behavior of the page cache? would i just need to manage it similar to managing the CPU's cache?

**5/** @AgileJebrim

@VPCOMPRESSB @NOTimothyLottes

There’s a win32 version too but yeah I would just generally assume that pages are 4096 bytes unless I have reason to believe otherwise. Apparently the intent that Timothy had is to use CreateFileMappingA() as well.

**6/** @NOTimothyLottes

@AgileJebrim @VPCOMPRESSB

In an ideal world the OS would allow pinning the file's pages. Since there is no guarantee, I can walk (read) the first cache line of the 4 kb pages periodically to try to force pinned behavior.

**7/** @AgileJebrim

@NOTimothyLottes @VPCOMPRESSB

VirtualLock()?

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-08-01-at-least-for-my-next-at-home-project-i-think-the]]
