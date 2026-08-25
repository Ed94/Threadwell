---
title: "@NOTimothyLottes I'd add:"
type: archive
source: twitter
source_url: "https://x.com/JBrooksBSI/status/1912487286190797257"
author: "John Brooks"
handle: JBrooksBSI
post_id: "1912487286190797257"
date: 2025-04-16
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes I'd add:"
in_reply_to: ""
parent_post_id: "1912483968563269946"
---

## Source

- URL: https://x.com/JBrooksBSI/status/1912487286190797257
- Author: John Brooks (@JBrooksBSI)
- Posted: 2025-04-16 12:44:35

## Branch

**1/**

@NOTimothyLottes I'd add:

Standardized, documented ISA that enables compatibility across multiple GPU generations (& max 256 VGPRs).

WGP (WorkGroup Processor) mode which doubles the # of SIMD units executing a single threadgroup, halving latency for bottleneck operations.

**2/**

@JBrooksBSI Personally I still don't like the WGP+wave32 stuff. Limited dual issue instructions with less operand flexibility (wave64 back to back issue IMO is better, just HW dual pipe transcendentals). WGP's two L0 cache and related resource split issues.

**3/**

@NOTimothyLottes WGP mode and wave32 are separate features. WGP mode schedules waves within a threadgroup across both CUs (4x SIMDs) in each WGP instead of limiting waves to a single CU (2x SIMD).

**4/**

@JBrooksBSI Yeah so it's more the wave32 that I don't like

**5/**

@NOTimothyLottes I'd like to discuss this in more detail, as I have found wave32 to be faster than wave64 for everything except some vertex shaders.

I think the reason wave64 can be faster for vertex shaders is that only half the VS waves get launched, so more occupancy for PS/CS waves per WGP.

**6/**

@NOTimothyLottes The reasons Wave64 has been slower for me:
1) More VGPR pressure = less occupancy
2) More GL0/LDS pressure = more stalls
3) 64-lane scalar logic is slower than scalar 32
4) Cross-lane ops only support 32 lanes

I spot-unroll 2x-4x for more intra-wave parallelism as needed.

**7/**

@JBrooksBSI Re
1) With what I do, high occupancy is often slower
2) I rarely use LDS
3) It's half the K$ loads for wave64
4) I use DPP16 at most (no dynamic shuffle)

**8/**

@NOTimothyLottes Wow, that is wildly different from what I do.

Why is high occupancy slower? (VGPR pressure? Cache pressure?)

Why not use LDS? I design my algorithms from the ground up around LDS.

K$ is rarely used for me as the focus is on SIMD32 vectors & LDS.

I shuffle to keep lanes full.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-04-16-cs-optimization-brain-dumping]]
