---
title: "Virtualized-xMas <thread>"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1739304851270459649"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1739304851270459649"
date: 2023-12-25
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Virtualized-xMas <thread>"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1739304851270459649
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-12-25 15:19:25

## Thread

**1/** **@NOTimothyLottes** ^1739304851270459649

Virtualized-xMas <thread>

[0] If one is going to pay the HW VM tax, might as well be able to actually use it via the techniques below, so we can exit this medieval dark age.

**2/** **@NOTimothyLottes** ^1739305164060721321

[1] Ability to get portable same virtual addresses so data can be directly streamed into same address without any need to relink pointers.

[2] Ability to use huge virtual address spaces for big data, with pipelined page table updates so execution need not stall during streaming

**3/** **@NOTimothyLottes** ^1739305283061416168

[3] Ability to map memory with the same zero page to avoid crashes on accessing memory outside the VA.

[4] Ability to use large pages without admin rights, with an os/driver that can defragment to build them.

**4/** **@NOTimothyLottes** ^1739305434509382019

[5] Ability to construct ring buffers that repeat the same physical pages in the virtual address space to avoid wrapping overheads.

[6] Ability to alias the same physical memory at different virtual addresses to avoid having to flush the virtual tagged caches on dependent passes

**5/** **@NOTimothyLottes** ^1739305541975875925

[7] Ability to lock pages to ensure quality of service.

[8] Ability to specify which physical pages should be recycled, and explicit map shared zero page where the address space has holes.

**6/** **@NOTimothyLottes** ^1739305653821133143

[9] Ability to control where page updates happen in time and also where TLB flushes happen with respect to the application's address space.

[10] Ability to map IO buffers direct into the GPU/CPU address space, like audio ring buffers, network IO, and solid state storage.
