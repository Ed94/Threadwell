---
title: "@SebAaltonen Very nice."
type: archive
source: twitter
source_url: "https://x.com/Dispatch_Graph/status/2086066890128888053"
author: "Amélie Heinrich"
handle: Dispatch_Graph
post_id: "2086066890128888053"
date: 2026-08-08
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen Very nice."
in_reply_to: ""
parent_post_id: "2086035003360583907"
---

## Source

- URL: https://x.com/Dispatch_Graph/status/2086066890128888053
- Author: Amélie Heinrich (@Dispatch_Graph)
- Posted: 2026-08-08 12:27:58

## Branch

**1/** **@Dispatch_Graph** ^2086066890128888053

**@SebAaltonen**

Very nice. I'm surprised you didn't talk about raytracing at all in your post/talk though! I think there's quite a few issues with the RT APIs as we speak...

Like Vulkan/Metal not exposing AS memory, so you can't store BLASes on disk, no indirect TLAS build...

**2/** **@Dispatch_Graph** ^2086067095993774585

**@SebAaltonen**

One thing I'd love to see in a new shading language and API is the concept of shader function pointers -- they respect a certain signature (return type, parameters), and instead of SBT madness, you can assign a BLAS instance a pointer to a GPU function

**3/** **@Dispatch_Graph** ^2086069530854387959

**@SebAaltonen**

Something like this would be awesome. Would solve the whole material classification fiasco you need to go through with V-Buffer, it would eliminate the need for SBTs/Uber-shader approaches for RT reflections/ReSTIR etc. Shader graph/custom materials could work for raster AND RT

![](https://pbs.twimg.com/media/HPM1GzdWwAA-lWl?format=jpg&name=orig)

**4/** **@GaySpaceAngel** ^2086511860896112987

**@Dispatch_Graph** **@SebAaltonen**

Something very similar to this API shape exists with Shader Subroutine Linkage (GL)/Dynamic Shader Linkage (D3D11). Unfortunately I think the function pointer has to be uniform so it’s an almost worthless feature in practice.

## Related

- Spine: [[archive/threads/SebAaltonen/2026-08-08-extended-2x-version-of-my-siggraph-2026-talk]]
