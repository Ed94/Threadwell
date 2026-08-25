---
title: "Just for Fun: Started to look into \"Cardinal Cubic O-MOMS\" for resampling, some refs:"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1877208278632955949"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1877208278632955949"
date: 2025-01-09
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Just for Fun: Started to look into \"Cardinal Cubic O-MOMS\" for resampling, some refs:"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1877208278632955949
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-01-09 04:18:25

## Thread

**1/**

Just for Fun: Started to look into "Cardinal Cubic O-MOMS" for resampling, some refs:
https://hhoppe.com/proj/filtering/supp/
https://hhoppe.com/proj/filtering/supp/sample_code.cpp
The source paper is math salad:
https://www.ee.cuhk.edu.hk/~tblu/monsite/pdfs/blu0101.pdf

**2/**

Results are quite nice in repeated reprojection: 
https://w3.impa.br/~diego/publications/NehHop14.pdf
[BLUE] From that PDF
Lanczos is of course not stable (if you reproject enough with a fast lanczos approximation, it will converge to a black and white image) so it needs non-linear control

![](https://pbs.twimg.com/media/Gg0va37XEAAQz9S?format=jpg&name=orig)

**3/**

However O-MOMS appears to need a pre-pass on the data before running the simple cubic filter. That simple cubic would otherwise blur bad (no negative lobes). So this is about where I stopped dissecting the math salad, and started looking at the code salad

![](https://pbs.twimg.com/media/Gg0w_aGWoAAaUif?format=png&name=orig)

**4/**

That prepass seems to work with 9 coefs in 1 dimension. So this starts to look mighty expensive??? for GPU-side implementation (compared to the existing option of limiting lanczos to make it stable).

![](https://pbs.twimg.com/media/Gg0xjpcXAAEg3cl?format=png&name=orig)

**5/**

Anyway if anyone knows of a less salad-like example of cubic O-MOMS, please post

**6/**

So if you reproject rotate in linear using a bilinear filter, after 16 reprojections you get this slop (very blurry), which is why the old simple TAA's started to look bad very fast

![](https://pbs.twimg.com/media/Gg00ZBZXMAAX4bY?format=png&name=orig)

**7/**

Compared to say this with a clamped approximate lanczos (same 16 reprojections, and linear filtering). The min/max for the clamp is of the inner 2x2 quad of the 4x4 filter window

![](https://pbs.twimg.com/media/Gg008NMXwAA1uiZ?format=png&name=orig)

**8/**

So even after 16 frames, clamped lanczos approximation is already significantly less sharp than source (below). Thing most of the shader TAAs screw up is that even with great reprojection filtering, still need error-correction sharpening on the reprojection to keep it dialed in

![](https://pbs.twimg.com/media/Gg01iQFW8AAuwBC?format=png&name=orig)

**9/**

Some don't limit the kernel approximation that has negative lobes, because it's not differentiable, leading to the classic trailing edge halo (dark outline typically seen in DLSS2 at least). After close to 64 frames of reprojection (rotation), easy to see that effect

![](https://pbs.twimg.com/media/Gg02p6SXsAEStmt?format=png&name=orig)

**10/**

Letting that go too long and well it converges to a high contrast black and white mess

![](https://pbs.twimg.com/media/Gg03IwkXIAAIb97?format=png&name=orig)

**11/**

The non-linear limiter (simple clamping) keeps it mostly stable in color, even if the detail still converged to noodles

![](https://pbs.twimg.com/media/Gg03eLtWgAA3X7L?format=png&name=orig)

**12/**

Also if you overcook your negative lobes in the approximation (using the RED curve below), it speeds up the noodling process (that is the same 16 reprojections as prior)

![](https://pbs.twimg.com/media/Gg09FUDXMAAt47h?format=jpg&name=orig)
![](https://pbs.twimg.com/media/Gg09PRNWYAAsJ10?format=png&name=orig)
