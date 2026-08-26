---
title: "__/ Raytastic Friday \\__"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1870179026213515352"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1870179026213515352"
date: 2024-12-20
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "__/ Raytastic Friday \\__"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1870179026213515352
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-12-20 18:46:40

## Thread

**1/** **@NOTimothyLottes** ^1870179026213515352

__/ Raytastic Friday \__
Thinking out of the AABB-ox ...
Rather lets press the full on crazy button
"You don't need to shade or render in screen space at all!"

Branches: [[archive/threads/NOTimothyLottes/2024-12-20-raytastic-friday/2024-12-20-mcnabbd-now-youre-talking]]

**2/** **@NOTimothyLottes** ^1870179245797802441

Start with scaling-TAAs (ML or not)
16 fetches to do good reprojection (seriously)
4 in local neighborhood & matching 4 from reprojection
+lot more to do good spatial filtering

With so much work, perhaps it would be better to reconstruct from a different domain?

**3/** **@NOTimothyLottes** ^1870179864025665854

How about reconstructing the player's view
directly from the environment probe shade cache

Assuming it has good enough density, and shading is impulse (not integrated over probe pixel ... aka aliased, like screen space would be with infinite negative mip bias)

**4/** **@NOTimothyLottes** ^1870180312623305104

All env probes must be in one atlas for this to work!
Note probes can have empty space (holes)

And if a probe only contains objects sharing the same rigid transform, one can reuse the probe without requiring re-shading even if it moves, so it really can be a cache if desired

**5/** **@NOTimothyLottes** ^1870180763842277576

Each probe pixel computes and stores projected screen position in INT16x2 (subpixel resolution of 17 steps at 4K)
More than good enough for AA reconstruction

So note AA quality is thus decoupled from shading rate and frame rate

**6/** **@NOTimothyLottes** ^1870181116797432129

Each probe pixel packs 64-bit MSBs{f(z), probe pixel atlas coord}LSBs, computes projected screen position does atomicMax()

Do some pixel-jitter on projected screen position
So any probe collisions get filtered out spatially as grain
(aka no temporal filtering in reconstruction)

**7/** **@NOTimothyLottes** ^1870181434704498917

For screen reconstruction of a pixel
Grab the neighborhood of atomic values (can be holes)
Those point back to probes
Grab a N sample neighborhood from the probes
Do reconstruction 
[costs like a scaling TAA but NOT from screen-space]
