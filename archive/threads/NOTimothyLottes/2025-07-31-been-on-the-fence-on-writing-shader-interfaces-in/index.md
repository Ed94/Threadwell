---
title: "Been on the fence on writing shader interfaces in GLSL vs something else that translates to SPIR-V."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1950935464149483683"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1950935464149483683"
date: 2025-07-31
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Been on the fence on writing shader interfaces in GLSL vs something else that translates to SPIR-V."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1950935464149483683
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-07-31 15:03:55

## Thread

**1/**

Been on the fence on writing shader interfaces in GLSL vs something else that translates to SPIR-V. Most GLSL mixed with defines can just direct port to other platforms. However these days I have hundreds of lines of macros to transform GLSL closer to assembly.

Branches: [[archive/threads/NOTimothyLottes/2025-07-31-been-on-the-fence-on-writing-shader-interfaces-in/2025-07-31-AgileJebrim-spir-v-ive-given-up-on-trying-to-massage-frontend]], [[archive/threads/NOTimothyLottes/2025-07-31-been-on-the-fence-on-writing-shader-interfaces-in/2025-08-01-olson_dan-whats-the-top-something-else-ive-been-out-of-the]]

**2/**

Meaning I write using macros that are mostly a 1:1 mapping to AMDs GCN/RDNA ISA. With workarounds for missing stuff. SPIR-V output is an intimidating level of complex verbosity. More so when navigating frequent type bit aliasing (float, int, packed 16-bit float and int).

**3/**

@NOTimothyLottes Sounds like an RDNA->SPIRV asm converter tool would be the way to go

**4/**

@JBrooksBSI I part tried to GLSL once. Using a global uint4 array as registers. But the wrapping of bit aliasing typecasts around operations is loaded with compiler perf bugs. Esp with packed 16-bit. So making it usable in practice is quite hard.

**5/**

@NOTimothyLottes What I do for console dev is write RDNA2 asm on PS5 (via wrapped shader intrinsics). 

On Xbox I have the wrappers implement C versions of the intrinsics (or HLSL intrinsics where available).

This is a technique I have been using since 2006, for PS3 SPU coding:

![](https://pbs.twimg.com/media/GxNAMxPa4AAnMRt?format=jpg&name=orig)

**6/**

@JBrooksBSI Eventually I ended up the same way (writing via instruction defines). Originally when I did FXAA it was a 1:1 line mapping to NV ISA. But without factoring through a define. But it's really the custom register allocation that I wish was universally expressible today.
