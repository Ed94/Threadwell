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
status: draft
draft: true
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

**1/**

Working on the Linux thread priority code. Linux doesn't allow sched_attr.size to be minimized to just what is required for the scheduling mode (my prior bug). So I statically allocate the structures already filled in and cacheline aligned ...

Media (not lifted): `2071937360288235902_HMD_iq0XcAASnSn_orig.png`

**2/**

Theory says: better for size, worse for perf! Global structure will miss the cache. The alternative is to allow the code to generate the structure on the stack, which is likely in cache, and burn a few more cachelines of code (which gets linear prefetch).

**3/**

Clearly the default linux won't allow my non-blessed user to get SCHED_FIFO, and it also seems like my nice(-20) SCHED_OTHER backup is also not allowed either. Damn. More stuff to workaround.

Media (not lifted): `2071938677584863448_HMEBJNuW4AE8JUV_orig.png`
