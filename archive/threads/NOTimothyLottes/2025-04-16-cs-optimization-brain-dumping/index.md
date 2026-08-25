---
title: "__/ CS OPTIMIZATION BRAIN DUMPING \\__"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1912475720103649326"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1912475720103649326"
date: 2025-04-16
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "__/ CS OPTIMIZATION BRAIN DUMPING \\__"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1912475720103649326
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-04-16 11:58:38

## Thread

**1/** @NOTimothyLottes

__/ CS OPTIMIZATION BRAIN DUMPING \__
(1.) Sometimes branching can disrupt otherwise regular execution flow leading to a performance regression,
while it might be counter intuitive to always do more work, it can sometimes be faster too ->

**2/** @NOTimothyLottes

WHY> Branching can cause: I$ misses, branch delays, wave switches that kill operand cache, poor register allocation, extra VALU overheads on the rejoin to move VGPRs, and most importantly poor VMEM behavior (not able to hoist out a speculative load earlier)

**3/** @NOTimothyLottes

(2.) Time a shader in isolation, tend to see 3 regions of execution: {cold-start, warm-cache, drain} regions.
Early waves are missing through {I$,K$,L0$}, warm-cache waves have lower runtime.

For this reason it is very important to pipeline (overlap) workloads.

**4/** @NOTimothyLottes

Serially dependent workloads should be broken up spatially and pipelined!

I've never seen a dev do this correctly (look at their serially dependent post passes)! Split those into a few independent pieces.

Branches: [[archive/threads/NOTimothyLottes/2025-04-16-cs-optimization-brain-dumping/2025-04-16-BoganBits-i-would-be-interested-to-see-a-concrete-example]], [[archive/threads/NOTimothyLottes/2025-04-16-cs-optimization-brain-dumping/2025-04-16-BoganBits-could-a-shader-compiler-not-do-this-i-e-detect]]

**5/** @NOTimothyLottes

(3.) If a shader is only going to run a small number of waves on say one CU (like a material used on a few pixels) then budget bandwidth for it's full {shader and constants} (which might be more costly than the textures themselves).

**6/** @NOTimothyLottes

(4.) Back to {cold,warm,drain} -> for small workloads or large 'cold/drain-region' workloads, it is better to force that onto one CU and loop through work (semi or full) persistent waves, to ensure high cache locality and reuse.

**7/** @NOTimothyLottes

... Note, might want to use large CU filling workgroups, because single-wave workgroups might get tossed on different low-level caches.

**8/** @NOTimothyLottes

(5.) For what should be VALU bound stuff, usually the problem on AMD is locally clustered VMEM caused by oldest first scheduling, causing memory bubbles. What you really want is steady VMEM keeping memory working well in parallel with execution ...

**9/** @NOTimothyLottes

... This can be very hard to fix. Sometimes you need to use more VALU to decode better compressed data to go faster (counter intuitive), or even reduce the waves running in parallel (for better cache/wave ratio) [also counter intuitive] ...

**10/** @NOTimothyLottes

There are shader source level transforms which can help too. Meaning you might see a difference batching say by groups of 2x2 (part kernel) instead of say the full kernel size. Yes sometimes the shader compiler will radically re-order, other times not (depends on VGPR pressure)

**11/** @NOTimothyLottes

(6.) The two most important things AMD ever did IMO to their architecture
(a.) Packed 16-bit (with double rate)
(b.) Bumping up VGPR capacity/wave (64 to 96 with good occupancy)
...

Branches: [[archive/threads/NOTimothyLottes/2025-04-16-cs-optimization-brain-dumping/2025-04-16-JBrooksBSI-id-add-standardized-documented-isa-that-enables]]

**12/** @NOTimothyLottes

... The reasons being that it becomes possible to reduce round trips through memory by pass merging and other techniques -> resulting in shaders with massive state fitting in VGPRs without spilling

Branches: [[archive/threads/NOTimothyLottes/2025-04-16-cs-optimization-brain-dumping/2025-04-16-DjMolehill-branching-cache-locality-and-memory-handling-are]]
