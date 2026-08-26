---
title: "@SebAaltonen Make it happen! What shader format are you thinking? Spir-V? I like that in OpenGL i can easily write a tool that generates shaders without the need to be dependent on a compiler library to use it, but i would assume that time has passed."
type: archive
source: twitter
source_url: "https://x.com/EskilSteenberg/status/2001077725734240398"
author: "Eskil Steenberg"
handle: EskilSteenberg
post_id: "2001077725734240398"
date: 2025-12-16
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen Make it happen! What shader format are you thinking? Spir-V? I like that in OpenGL i can easily write a tool that generates shaders without the need to be dependent on a compiler library to use it, but i would assume that time has passed."
in_reply_to: ""
parent_post_id: "2001000839574643138"
---

## Source

- URL: https://x.com/EskilSteenberg/status/2001077725734240398
- Author: Eskil Steenberg (@EskilSteenberg)
- Posted: 2025-12-16 23:51:22

## Branch

**1/** **@EskilSteenberg** ^2001077725734240398

**@SebAaltonen**

Make it happen! What shader format are you thinking? Spir-V? I like that in OpenGL i can easily write a tool that generates shaders without the need to be dependent on a compiler library to use it, but i would assume that time has passed.

**2/** **@JoaoBapt** ^2001551866682052865

**@EskilSteenberg** **@SebAaltonen**

That could probably be implemented on top of amdgpu directly, or Mesa, not sure, but it would only work on Linux and AMD, since Nvidia has their own proprietary drivers.

**3/** **@SebAaltonen** ^2001558855592157294

**@JoaoBapt** **@EskilSteenberg**

The biggest issue on building it on top of Vulkan is that GLSL/HLSL don't have pointers. Vulkan BDA extension is using raw 64-bit integers and the BDA syntax in GLSL is messy. C/C++ based shading language similar to CUDA and MSL would be nice. Or a Rust based if you prefer that.

**4/** **@SebAaltonen** ^2001559152737366107

**@JoaoBapt** **@EskilSteenberg**

SPIRV supports pointers just fine. That's not the limitation. We just need a new shader language, or somebody needs to write MSL->SPIRV tooling. The other way exists already.

**5/** **@EskilSteenberg** ^2001570355497046520

**@SebAaltonen** **@JoaoBapt**

If C would have added vectors when SIMD became common in CPUs 25 years ago, C would be the dominant shading language. I still think thats the right way to go. Just use C and add an extension for vectors.

**6/** **@SebAaltonen** ^2001574372524331051

CUDA, OpenCL and Metal MSL are all C/C++ based languages. They are still used. GLSL/HLSL are only relevant for graphics shaders. Nvidia is 90% AI company today. CUDA is more relevant than graphics for them. I think we should leverage the AI ecosystems more instead of writing ad-hoc graphics shader languages. GLSL/HLSL have practically no library ecosystem.

**7/** **@EskilSteenberg** ^2001577597948563735

**@SebAaltonen** **@JoaoBapt**

Id like it to be ISO C with an extension, rather than C-like to leverage existing C tooling. (And perhaps make shader language like vectors defacto standard in C)

## Related

- Spine: [[archive/threads/SebAaltonen/2025-12-16-my-no-graphics-api-blog-post-is-live-please-repost]]
