---
title: "@Triang3l That clause based arch was interesting in many ways, mem clause articulates the boundary for write combining."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2084996454175612983"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2084996454175612983"
date: 2026-08-05
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - Triang3l
description: "@Triang3l That clause based arch was interesting in many ways, mem clause articulates the boundary for write combining."
in_reply_to: ""
parent_post_id: "2084985800836477433"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2084996454175612983
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-08-05 13:34:26

## Branch

**1/** @NOTimothyLottes

@Triang3l That clause based arch was interesting in many ways, mem clause articulates the boundary for write combining. Was also easy to engineer slow perf by fine granularity predication too.

**2/** @Triang3l

@NOTimothyLottes But what is even a memory clause when MEM_RAT is a control flow instruction, or did the GPU group consecutive MEM_RATs into an implicit "clause"? I also wonder when you can mix RAT and RAT_CACHELESS (the OpenCL compiler apparently just stops using DB at all if CB is ever needed).

**3/** @NOTimothyLottes

@Triang3l My understanding is that youd need UNCACHED for both write and read. So wouldn’t be all that useful perf wise. My guess is the transition from MEM_EXPORT to MEM_RD (where youd do UNCACHED) implicitly waits for uncached write visibility.

**4/** @Triang3l

@NOTimothyLottes Yeah, I really hope so… But I guess I should just look at D3D11/GL/CL shader dumps. So many scary things involved, like WAIT_ACK, and that mention of SCOption_R800_UAV_NONUAV_SYNC_WORKAROUND_BUG216513_1 in disassembly. Unless they just fall back to RAT NOP_RTN for all loads 🤷‍♂️

**5/** @NOTimothyLottes

@Triang3l Haha oops, very foggy, sounds like it is explicit via WAIT_ACK, rather than implicit. Fees like the predecessor to s_waitcnt in many respects.

**6/** @NOTimothyLottes

@Triang3l There are a lot of good cases to have the same memory bound as read and write simultaneously, but under an implicit contract of no r/w overlap for a given cache line . Then dont need uncached reads, but probly would need WAIT_ACK still if write order visibility matters.

## Related

- Spine: [[archive/threads/Triang3l/2026-08-05-writes-have-write-only-caches-that-are]]
