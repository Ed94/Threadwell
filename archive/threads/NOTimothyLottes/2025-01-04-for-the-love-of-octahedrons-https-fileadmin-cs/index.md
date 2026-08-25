---
title: "For the love of octahedrons: https://fileadmin.cs.lth.se/graphics/research/papers/2008/simdmapping/clarberg_simdmapping08_preprint.pdf"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1875582899996782889"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1875582899996782889"
date: 2025-01-04
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "For the love of octahedrons: https://fileadmin.cs.lth.se/graphics/research/papers/2008/simdmapping/clarberg_simdmapping08_preprint.pdf"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1875582899996782889
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-01-04 16:39:44

## Thread

**1/** **@NOTimothyLottes** ^1875582899996782889

For the love of octahedrons: https://fileadmin.cs.lth.se/graphics/research/papers/2008/simdmapping/clarberg_simdmapping08_preprint.pdf

Mapping this well to the GPU follows ...

![](https://pbs.twimg.com/media/GgdoSaxXYAAwbTz?format=png&name=orig)

**2/** **@NOTimothyLottes** ^1875583660545732960

At some point the standard Octahedron mapping leaves a lot to be desired due to highly variable texel sizing, so have been using that paper's equal area mapping instead. Spent some time optimizing today, got to this which is in theory just 31ops for the 2D to 3D transform

![](https://pbs.twimg.com/media/GgdpMDiXMAEEL8y?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2025-01-04-for-the-love-of-octahedrons-https-fileadmin-cs/2025-01-06-JBrooksBSI-some-optimization-ideas-1-for-rdna2-simd-insn]]

**3/** **@NOTimothyLottes** ^1875584449674637486

AMD's latest driver actually does mostly a good job compiling that (32 op clocks compiled, just 1 more instruction somewhere). I'm surprised actually it's now picking up 'cos(x*2pi)' and pattern matching that to just V_COS_F32!

![](https://pbs.twimg.com/media/Ggdp6iCWcAAYubj?format=png&name=orig)

**4/** **@NOTimothyLottes** ^1875585990687125782

And the inverse which should also be around 32 op clk (VALU). This uses the Horner form for the papers atan approximation. Could perhaps make that less or more accurate if desired.

![](https://pbs.twimg.com/media/GgdrTPnWYAABHUm?format=png&name=orig)

**5/** **@NOTimothyLottes** ^1875586260875800870

AMD's compiler also does a good job there.

![](https://pbs.twimg.com/media/GgdrucxXQAAPQfe?format=png&name=orig)

**6/** **@NOTimothyLottes** ^1875587579938242661

If AMD evolved to a fused floating point compare and select instead of a separate V_CMP* and V_CNDMASK_B32, it would shave a few cycles. Also if they could push 2 results into a result cache in 1 clk, doing the MIN and MAX in one op would shave a cycle.

**7/** **@NOTimothyLottes** ^1875589737282679108

Related> Great ref for fast atan2: https://mazzo.li/posts/vectorized-atan2.html
I'm using the simplest form from the 1955 paper in horner form scaled by /pi for cylindrical view projection code

Branches: [[archive/threads/NOTimothyLottes/2025-01-04-for-the-love-of-octahedrons-https-fileadmin-cs/2025-01-04-marc_b_reynolds-its-pretty-amazing-how-good-the-hastings]], [[archive/threads/NOTimothyLottes/2025-01-04-for-the-love-of-octahedrons-https-fileadmin-cs/2025-01-06-pixelmager-i-was-looking-at-a-very-similar-problem-for-hemi]]
