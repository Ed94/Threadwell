---
title: "Working towards a new bring up of front-buffering on NV via VK."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1858709400791261630"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1858709400791261630"
date: 2024-11-19
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Working towards a new bring up of front-buffering on NV via VK."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1858709400791261630
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-11-19 03:10:28

## Thread

**1/** @NOTimothyLottes

Working towards a new bring up of front-buffering on NV via VK. My last implementation had been tuned on AMD and didn't work on NV any more. NV does seem to accept a 1-deep swap with IMMEDIATE presentation at least on latest drivers, so that is a good start.

**2/** @NOTimothyLottes

Since my image resources are static after init time, only swap images change when the driver kills the swap chain (which once upon a time seemed to happen on ALT+TAB maybe). So it's one descriptor set always bound.

**3/** @NOTimothyLottes

Stopped using VK_DESCRIPTOR_SET_LAYOUT_CREATE_UPDATE_AFTER_BIND_POOL_BIT_EXT (god awful naming length people), because I think it could be a perf hit on NV due to extra indirection. NV driver is free to bake down the single set now before the command buffer is sent over.

**4/** @NOTimothyLottes

At this stage, to the point of having everything loaded and swap chain created, it's 2700 lines of engine code. That includes embedding headers (no external includes), so it's a one file compile. People claim rolling your own engine is hard? Not really if you keep it focused.

**5/** @NOTimothyLottes

So far it's a 0.25 sec hot load time on this NV dGPU laptop. Includes mapping a 4 MiB 'cart' file from pagecache, doing a 512 MiB buffer for GPU usage, hits on all PSOs, allocating some images, and kicking the command buffer that copies in the cart, and clears everything.

**6/** @NOTimothyLottes

Everything at load-time is multi-threaded to try to minimize start to in-game time. This is in sharp contrast to runtime where the only multi-threading being used is to separate things that are blocking.

**7/** @NOTimothyLottes

I get some utility on parallelizing {vulkan instance creation, mapping the cart file, warming the TLBs by walking all the pages, bringing up the window} it's about 0.08 seconds in at that point

**8/** @NOTimothyLottes

After VK device is open, I signal a background thread to load the SPIR-V module, while building the descriptor set layout, which then unblocks PSO compile on background threads. And the rest of the VK setup runs in parallel. Working towards swap creation.
