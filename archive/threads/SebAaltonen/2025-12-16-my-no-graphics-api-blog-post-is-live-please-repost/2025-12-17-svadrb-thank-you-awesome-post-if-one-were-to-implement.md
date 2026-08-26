---
title: "@SebAaltonen Thank you! Awesome post."
type: archive
source: twitter
source_url: "https://x.com/svadrb/status/2001197309011394894"
author: "svadrb"
handle: svadrb
post_id: "2001197309011394894"
date: 2025-12-17
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen Thank you! Awesome post."
in_reply_to: ""
parent_post_id: "2001000839574643138"
---

## Source

- URL: https://x.com/svadrb/status/2001197309011394894
- Author: svadrb (@svadrb)
- Posted: 2025-12-17 07:46:33

## Branch

**1/** **@svadrb** ^2001197309011394894

**@SebAaltonen**

Thank you! Awesome post.

If one were to implement this API on top of existing API/driver, is it doable or is something missing?

**2/** **@SebAaltonen** ^2001201043548364996

**@svadrb**

You could implement it on top of Vulkan, if you had a custom shading language. Unfortunately there's no MSL (Metal Shading Language) to SPIRV tools yet. That's today possible with Vulkan BDA extension. But we'd need to add a the texture descriptor heap on top of it somehow.

**3/** **@SebAaltonen** ^2001201352047796713

**@svadrb**

Metal's biggest limitation for implementing this API would be the lack of user visible texture descriptor heap. Everything else is there. And DirectX 12s biggest limitation is lack of 64-bit GPU pointers in HLSL. DirectX 12 handles 64-bit GPU pointers in the CPU side in some APIs

**4/** **@SebAaltonen** ^2001202721785790591

And if you want best possible performance for the root struct, you'd have to write some reflection to convert the root struct to API specific root struct build calls, and at draw time you need to setup the data that the shader expects. This is the biggest PITA. 

Or you can simply ignore that and pass one pointer as the root struct and don't get root prefetch optimizations. This is trivial, but the code runs slightly slower on the GPU.

## Related

- Spine: [[archive/threads/SebAaltonen/2025-12-16-my-no-graphics-api-blog-post-is-live-please-repost]]
