---
title: "SPC: Using 8 deep swap all aliasing same BO (image) fixes Game Mode crash with external display."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1687062786273062912"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1687062786273062912"
date: 2023-08-03
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "SPC: Using 8 deep swap all aliasing same BO (image) fixes Game Mode crash with external display."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1687062786273062912
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-08-03 11:28:07

## Thread

**1/**

SPC: Using 8 deep swap all aliasing same BO (image) fixes Game Mode crash with external display. Pipelined load gets to black screen in 2 ms. Takes 460 ms to allocate 4 GiB GTT video ram, 558 ms to copy 256 MiB cart from page cache to USWC (page faults), all in parallel.

![](https://pbs.twimg.com/media/F2mmqYXWoAAG3fj?format=jpg&name=orig)

**2/**

Clearing page cache to simulate a cold launch: Takes 1.5 sec to read 256 MiB from the stock SSD. This is worst case load time in desktop mode. Won't be any compile/etc after this. So literally in game at this point. Speed of light. This is how it is done.

**3/**

Forgot the timing capture ... Load from SSD.

![](https://pbs.twimg.com/media/F2mpszoXMAE00Hy?format=jpg&name=orig)

**4/**

There are only 3 threads on load: (1.) to open X11 then spin doing present/keyboard, (2.) to open the AMDgpu device, SDMA copy after CART read, and then eventually spin doing dispatchs, (3.) one to load the CART from disk to mapped USWC GTT via read().

**5/**

Something I don't know: does read() since it's kernel- side automatically get some multi-core parallelism? Not a good idea to manually thread the read() because SSD needs linear reads to be fast. Not possible to know if the reads are page cache hits in advance either ...
