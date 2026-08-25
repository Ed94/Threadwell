---
title: "Significant amount of bloat dropped :-) 🎉🥳🎈"
type: archive
source: twitter
source_url: "https://x.com/rianflo/status/2001080321802977727"
author: "Florian Hoenig"
handle: rianflo
post_id: "2001080321802977727"
date: 2025-12-17
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rianflo
description: "Significant amount of bloat dropped :-) 🎉🥳🎈"
in_reply_to: ""
---

## Source

- URL: https://x.com/rianflo/status/2001080321802977727
- Author: Florian Hoenig (@rianflo)
- Posted: 2025-12-17 00:01:41

## Thread

**1/** @rianflo

Significant amount of bloat dropped :-) 🎉🥳🎈

I’d move it all to the GPU though. A single kernel that launches your pipeline steps per frame or per whatever. Pretty sure NV can do it. AMD I have no deep knowledge. @NOTimothyLottes ?

**2/** @NOTimothyLottes

@rianflo

From my perspective being compute-only for graphics, few reasons to launch kernels because I'd always use a fixed amount of VGPRs. The larger problem is compilers that cannot keep up with the large program sizes (in compile time or register allocation).

Branches: [[archive/threads/rianflo/2025-12-17-significant-amount-of-bloat-dropped/2025-12-17-rianflo-question-is-how-much-overhead-of-course-even-not]]

**3/** @NOTimothyLottes

@rianflo

Huge amount of pitfalls with compute-side dynamic dispatch of work (NV had it back when I worked there BTW), from long latency chains, to overheads tracking work completion, preemption, state restore, etc. It's not the golden answer people think it is. It is a slow path.

**4/** @NOTimothyLottes

@rianflo

There are however a bunch of things we could trivially do GPU side that are currently CPU side, like computing best tiling modes for images, computing image {size, alignment, etc}, building descriptors, etc. Lots of other driver stuff could be done on the GPU for sure.

**5/** @NOTimothyLottes

@rianflo

My plan for 2026 is actually to build my open source AMD SteamOS/Linux driver for a future compute-graphics API, and it will be doing some radical stuff since I'm also doing shader binary code generation too :) Hopefully you all get live examples.

**6/** @bkaradzic

@NOTimothyLottes @rianflo

Can't wait! This compute-graphics API is something like compute + meshlets + fragment shaders only graphics API?

**7/** @NOTimothyLottes

@bkaradzic @rianflo

Compute as in only compute shader dispatches, no fixed function graphics (no fragment/etc). And graphics via pure compute.

**8/** @Nicolas_Lopez_

@NOTimothyLottes @bkaradzic @rianflo

Considering how much we already software rasterize, we are not so far from it :)

**9/** @rianflo

@Nicolas_Lopez_ @NOTimothyLottes @bkaradzic

yeah but then someone insists on a couple of large triangles and wants to access the rasterizer hw again, which is supposedly too small of die area to be even worth ripping it out.
