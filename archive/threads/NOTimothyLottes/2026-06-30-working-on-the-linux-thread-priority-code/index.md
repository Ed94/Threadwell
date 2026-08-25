---
title: "Working on the Linux thread priority code."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2071937360288235902"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2071937360288235902"
date: 2026-06-30
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Working on the Linux thread priority code."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2071937360288235902
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-06-30 12:42:16

## Thread

**1/** @NOTimothyLottes

Working on the Linux thread priority code. Linux doesn't allow sched_attr.size to be minimized to just what is required for the scheduling mode (my prior bug). So I statically allocate the structures already filled in and cacheline aligned ...

![](https://pbs.twimg.com/media/HMD_iq0XcAASnSn?format=png&name=orig)
**2/** @NOTimothyLottes

Theory says: better for size, worse for perf! Global structure will miss the cache. The alternative is to allow the code to generate the structure on the stack, which is likely in cache, and burn a few more cachelines of code (which gets linear prefetch).

**3/** @NOTimothyLottes

Clearly the default linux won't allow my non-blessed user to get SCHED_FIFO, and it also seems like my nice(-20) SCHED_OTHER backup is also not allowed either. Damn. More stuff to workaround.

![](https://pbs.twimg.com/media/HMEBJNuW4AE8JUV?format=png&name=orig)