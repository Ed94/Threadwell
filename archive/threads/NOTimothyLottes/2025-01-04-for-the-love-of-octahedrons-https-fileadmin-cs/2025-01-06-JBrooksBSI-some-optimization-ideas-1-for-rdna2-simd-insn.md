---
title: "@NOTimothyLottes Some optimization ideas:"
type: archive
source: twitter
source_url: "https://x.com/JBrooksBSI/status/1876298864736801016"
author: "John Brooks"
handle: JBrooksBSI
post_id: "1876298864736801016"
date: 2025-01-06
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Some optimization ideas:"
in_reply_to: ""
parent_post_id: "1875583660545732960"
---

## Source

- URL: https://x.com/JBrooksBSI/status/1876298864736801016
- Author: John Brooks (@JBrooksBSI)
- Posted: 2025-01-06 16:04:43

## Branch

**1/**

@NOTimothyLottes Some optimization ideas:

1) For RDNA2 simd, insn-dependency stalls make it unlikely to achieve 100% VALU utilization. Try unrolling 2x or 4x

2) bit-per-thread data like float signs can often be done as 64x SALU var at 2x VALU speed

3) If FP16 range is ok, gives 2x VALU speed

**2/**

@JBrooksBSI Lack of ABS modifiers on V_PK ops basically kills FP16 benefit here unfortunately. I do unroll when not VGPR limited (favorite optimization). Wary though of SALU/VALU crossings due to latency + scheduling behavior (loss of operand cache, etc). VCC probably has special forwarding

**3/**

@NOTimothyLottes I did an approx equal-area mapping to a 2D texture in 2018

Approach was to map sphere to Archimedean solid rhombicuboctahedron (triangles and squares) packed into a 2D texture

https://en.wikipedia.org/wiki/Rhombicuboctahedron

Lookup of 3D unit vec used small static cubemap to convert to 2D texture U,V

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-01-04-for-the-love-of-octahedrons-https-fileadmin-cs]]
