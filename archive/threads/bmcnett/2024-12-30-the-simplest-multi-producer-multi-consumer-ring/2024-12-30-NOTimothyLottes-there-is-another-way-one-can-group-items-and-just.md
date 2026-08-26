---
title: "@bmcnett There is another way, one can group items and just do counting per group, release the whole group only when all items in group are ready"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1873749894437187586"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1873749894437187586"
date: 2024-12-30
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - bmcnett
description: "@bmcnett There is another way, one can group items and just do counting per group, release the whole group only when all items in group are ready"
in_reply_to: ""
parent_post_id: "1873744231719956872"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1873749894437187586
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-12-30 15:16:02

## Branch

**1/** **@NOTimothyLottes** ^1873749894437187586

**@bmcnett**

There is another way, one can group items and just do counting per group, release the whole group only when all items in group are ready

**2/** **@bmcnett** ^1873752260020404449

**@NOTimothyLottes**

that's trivial for a multi producer single consumer, how do you do it simply for a multi consumer?

**3/** **@NOTimothyLottes** ^1873823299819758004

**@bmcnett**

Here is an idea how to do it via minimal atomics. 2M max items per frame. Tune group size to machine, and have the producers start ahead enough, and the (lock-free) spins likely won't happen in practice ... (if on GPU then optimize the atomicAdd()'s, etc)

![](https://pbs.twimg.com/media/GgEn-GCWwAAZm7I?format=png&name=orig)

**4/** **@bmcnett** ^1873830067270541695

**@NOTimothyLottes**

ah, ok i get it now. i don't spin inside API, so user can decide when they want to be wait-free

**5/** **@NOTimothyLottes** ^1873831867499381145

**@bmcnett**

Yeah, exactly that, there are many optimizations possible. Like producers can amortize to one atomic per group to advance ready. Producers could queue the group locally if it isn't active and keep going. Etc.

## Related

- Spine: [[archive/threads/bmcnett/2024-12-30-the-simplest-multi-producer-multi-consumer-ring]]
