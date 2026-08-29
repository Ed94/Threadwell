---
title: "@flowerornament FWIW you’re speed running shader dev in modern AAA, they do a hacky emulation of a rate lattice type idea bc GI and fog etc need to be amortised over several frames."
type: archive
source: twitter
source_url: "https://x.com/hastuc_dibtux/status/2034587177233908079"
author: "Dr. Oskar Sarkon"
handle: hastuc_dibtux
post_id: "2034587177233908079"
date: 2026-03-19
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - flowerornament
description: "@flowerornament FWIW you’re speed running shader dev in modern AAA, they do a hacky emulation of a rate lattice type idea bc GI and fog etc need to be amortised over several frames."
in_reply_to: ""
parent_post_id: "2034584048606273988"
---

## Source

- URL: https://x.com/hastuc_dibtux/status/2034587177233908079
- Author: Dr. Oskar Sarkon (@hastuc_dibtux)
- Posted: 2026-03-19 11:05:58

## Branch

**1/** **@hastuc_dibtux** ^2034587177233908079

**@flowerornament**

FWIW you’re speed running shader dev in modern AAA, they do a hacky emulation of a rate lattice type idea bc GI and fog etc need to be amortised over several frames. Should definitely look at demo scene stuff also if you haven’t

**2/** **@flowerornament** ^2034591920706781196

That's correct pattern matching, but the innovation here is not that I'm inventing new concepts—the design only aims to *formalize* many known techniques. Moving between audio programming, control, and neural networks is just a parameterization, with computations dispatched to whatever hardware runs them best.

It remains to be seen whether this thing can subsume graphics too (despite all the overlap), but for now it doesn't because scatter has unbounded cost, and that's just a different aesthetic.

**3/** **@hastuc_dibtux** ^2034599017405972632

**@flowerornament**

Can you elaborate on the scatter thing wrt video

**4/** **@flowerornament** ^2034780263855923467

Graphics has a gather / scatter concept. Rasterization (scatter) writes into unknown / unbounded memory space, so you can't guarantee performance characteristics by construction in advance. This is somewhat fine on GPUs, but at the end of the day you need to just build and test to see if it works (that's how the whole industry works today ... why there are C++ gray beards running everything). Murail's whole concept is that downstream performance characteristics are *known* in the type system, so you can guarantee something will run in real-time at compile time. This makes it safe / easy for a novice to write performant code.

There is a middle ground possible, but not a priority for me right now.

**5/** **@flowerornament** ^2034780576029512153

> Graphics has a gather/scatter split. Texture sampling is gather — read from computed addresses — and GPUs do it natively. Rasterization is scatter — one triangle writes to many pixels, fanout is data-dependent and unbounded. That scatter path requires dedicated fixed-function hardware (rasterizers, ROPs) that doesn’t exist in the compute/tensor pipeline (currently).

## Related

- Spine: [[archive/threads/flowerornament/2026-03-19-im-currently-thinking-through-the-murail]]
