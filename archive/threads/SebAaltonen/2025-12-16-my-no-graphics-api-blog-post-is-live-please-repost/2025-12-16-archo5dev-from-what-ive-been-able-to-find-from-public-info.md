---
title: "@SebAaltonen from what I've been able to find from public info, many APIs (e.g."
type: archive
source: twitter
source_url: "https://x.com/archo5dev/status/2001013865283510527"
author: "Arvīds Kokins"
handle: archo5dev
post_id: "2001013865283510527"
date: 2025-12-16
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen from what I've been able to find from public info, many APIs (e.g."
in_reply_to: ""
parent_post_id: "2001000839574643138"
---

## Source

- URL: https://x.com/archo5dev/status/2001013865283510527
- Author: Arvīds Kokins (@archo5dev)
- Posted: 2025-12-16 19:37:37

## Branch

**1/** **@archo5dev** ^2001013865283510527

**@SebAaltonen**

from what I've been able to find from public info, many APIs (e.g. the console APIs) still don't have PSOs (https://gist.github.com/archo5/53611ab2b8dcf6d784a9a032aa1b6664#not-how-gpus-do-things)

I'd say PSOs should be destroyed completely, instead opting for separate narrow per-shader optimization (DCE) functions

![](https://pbs.twimg.com/media/G8UF699W0AQFtr-?format=png&name=orig)

**2/** **@SebAaltonen** ^2001020440274461071

**@archo5dev**

You can't compile microcode for all the vendors and all their GPU models. That would bloat your shader compile times during development and shader binary size by 100x+. And vendors couldn't improve their shader codegen by patching the drivers.

**3/** **@archo5dev** ^2001023348181217522

**@SebAaltonen**

I'm not proposing compiling all vendor-specific machine code at dev time.

Instead: 1) each shader/stage is compiled separately; 2) where optimizations are needed, each compilation step is given as much of the necessary specialized context as the application is able to provide.

**4/** **@archo5dev** ^2001035724854903191

**@SebAaltonen**

basically like in the image but e.g. in the case of a vertex shader, you could optionally pass the input layout from the next stage so DCE could remove all the code that's exclusive to unused inputs
so any 2 shaders compiled with the same cross-stage layout could be used together

![](https://pbs.twimg.com/media/G8UZu94WkAQXQ6g?format=png&name=orig)

**5/** **@archo5dev** ^2001036925424046575

**@SebAaltonen**

this would also have the added benefit that if one wanted to fully optimize all shaders, there would only be as many shader compilations as there are unique input/output layouts per shader, typically less than every VS & PS combination (which is what a PSO inherently requires)

**6/** **@SebAaltonen** ^2001366852652634249

Splitting VS and PS is a good idea. In the blog post I discuss about splitting depth-stencil state object and blend state object (as those are separate command packets on most GPUs). Splitting requires defining channel masks on both the PSO and blend state. Similarly you could define the VS<->PS interface and compile those shaders separately.

**7/** **@SebAaltonen** ^2001377928404439503

**@archo5dev**

You are right that PS<->VS interface optimization isn't a big deal. It helps in some corner cases only. Would be better to separate them too. Makes validation a bit worse as validation will happen at pixel/vertex shader bind time instead of pipeline create time.

**8/** **@archo5dev** ^2001380683210723565

**@SebAaltonen**

I suspect the biggest typical benefit from the interface optimization might be with depth-only passes - but they're also very easy to DCE by hand with a preprocessor.
Overall it's hard to imagine cases which would benefit from DCE and hard to optimize manually.

**9/** **@archo5dev** ^2001381756524749307

**@SebAaltonen**

I'm thinking that validation (debug-only) would probably have to be in the first draw call with the new VS/PS pair, comparing IDs from a cross-stage layout hash table: at shader compilation time, every layout could acquire an ID unique to that layout, later they're only compared.

## Related

- Spine: [[archive/threads/SebAaltonen/2025-12-16-my-no-graphics-api-blog-post-is-live-please-repost]]
