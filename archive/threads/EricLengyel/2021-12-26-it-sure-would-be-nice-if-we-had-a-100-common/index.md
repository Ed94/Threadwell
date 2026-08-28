---
title: "It sure would be nice if we had a 100% common language syntax and function library instead of a bunch of random differences among GLSL, HLSL, and PSSL."
type: archive
source: twitter
source_url: "https://x.com/EricLengyel/status/1475217195193942018"
author: "Eric Lengyel"
handle: EricLengyel
post_id: "1475217195193942018"
date: 2021-12-26
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - EricLengyel
description: "It sure would be nice if we had a 100% common language syntax and function library instead of a bunch of random differences among GLSL, HLSL, and PSSL."
in_reply_to: ""
---

## Source

- URL: https://x.com/EricLengyel/status/1475217195193942018
- Author: Eric Lengyel (@EricLengyel)
- Posted: 2021-12-26 21:29:22

## Thread

**1/** **@EricLengyel** ^1475217195193942018

It sure would be nice if we had a 100% common language syntax and function library instead of a bunch of random differences among GLSL, HLSL, and PSSL. Anybody know why Cg didn't work out? I remember it being very well done.

**2/** **@EricLengyel** ^1475217797504327683

HLSL and PSSL have float, float2, float3, and float4.
GLSL has float, vec2, vec3, and vec4.

HLSL and PSSL have lerp().
GLSL has mix().

HLSL and PSSL have frac().
GLSL has fract().

HLSL and PSSL have ddx() and ddy().
GLSL has dFdx() and dFdy().

**3/** **@EricLengyel** ^1475218316696252418

HLSL has Texture2DArray.
PSSL has Texture2D_Array.
GLSL has sampler2DArray.

**4/** **@EricLengyel** ^1475244563203719169

HLSL has bool frontFacing : SV_IsFrontFace.
PSSL has float frontFacing : S_FRONT_FACE.
GLSL has bool gl_FrontFacing.

Branches: [[archive/threads/EricLengyel/2021-12-26-it-sure-would-be-nice-if-we-had-a-100-common/2021-12-26-hakimshafaei-wgsl-webgpu-has-its-own-story-as-well]], [[archive/threads/EricLengyel/2021-12-26-it-sure-would-be-nice-if-we-had-a-100-common/2021-12-27-Dennis_A_Landi-it-looks-like-a-wrapper-interface-needs-to-be]], [[archive/threads/EricLengyel/2021-12-26-it-sure-would-be-nice-if-we-had-a-100-common/2021-12-27-KeelanStuart-iirc-there-is-also-a-difference-with-saturate-and]]
