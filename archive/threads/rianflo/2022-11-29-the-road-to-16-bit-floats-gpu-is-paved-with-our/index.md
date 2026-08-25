---
title: "\"The road to 16-bit floats GPU is paved with our blood\""
type: archive
source: twitter
source_url: "https://x.com/rianflo/status/1597661267845865474"
author: "Florian Hoenig"
handle: rianflo
post_id: "1597661267845865474"
date: 2022-11-29
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - rianflo
description: "\"The road to 16-bit floats GPU is paved with our blood\""
in_reply_to: ""
---

## Source

- URL: https://x.com/rianflo/status/1597661267845865474
- Author: Florian Hoenig (@rianflo)
- Posted: 2022-11-29 18:38:24

## Thread

**1/** **@rianflo** ^1597661267845865474

"The road to 16-bit floats GPU is paved with our blood"
:-/

https://www.yosoygames.com.ar/wp/2022/01/the-road-to-16-bit-floats-gpu-is-paved-with-our-blood/

**2/** **@NOTimothyLottes** ^1597717009369735169

**@rianflo**

Explicit packed 16-bit works on AMD Vulkan Vega and up. I typically get up to 30% improvement on ALU bound stuff. Lots of occupancy wins. I don't use {HLSL, RenderDoc, Reflection, RADV, or VS/PS}. All constants are packed and aliased as UINT, so no coversion overheads.

**3/** **@rianflo** ^1597718146663690240

**@NOTimothyLottes**

Oh I know the benefits. Just no simple clear way to write it in GLSL for vulkan.

**4/** **@NOTimothyLottes** ^1597718560511385600

**@rianflo**

Sure there is. CAS/FSR1/etc all shipped with fantastic GLSL versions using 16-bit packed math (I wrote those), all which at the time got fantastic code generation using AMD's drivers.

**5/** **@rianflo** ^1597720097753542656

**@NOTimothyLottes**

What GLSL extension did you use?

**6/** **@rianflo** ^1597720454000541696

**@NOTimothyLottes**

Oh wait, you're saying you wrote the fp16 math manually?

**7/** **@NOTimothyLottes** ^1597798161665253376

**@rianflo**

Explicit packed 16-bit code. FSR1 example: https://github.com/GPUOpen-Effects/FidelityFX-FSR/blob/master/ffx-fsr/ffx_fsr1.h - There are different 'F' (32-bit) and 'H' and 'Hx2' (packed 16-bit) functions.


