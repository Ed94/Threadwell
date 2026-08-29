---
title: "@Jonathan_Blow What would that actually mean, in terms of hardware? I assume you don't mean that the GPU would have a CPU on package, because that's really no different than a Strix Halo or Core Ultra, etc."
type: archive
source: twitter
source_url: "https://x.com/cmuratori/status/2060486879263555907"
author: "Casey Muratori"
handle: cmuratori
post_id: "2060486879263555907"
date: 2026-05-29
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "@Jonathan_Blow What would that actually mean, in terms of hardware? I assume you don't mean that the GPU would have a CPU on package, because that's really no different than a Strix Halo or Core Ultra, etc."
in_reply_to: ""
parent_post_id: "2060476161805971555"
---

## Source

- URL: https://x.com/cmuratori/status/2060486879263555907
- Author: Casey Muratori (@cmuratori)
- Posted: 2026-05-29 22:22:08

## Branch

**1/** **@cmuratori** ^2060486879263555907

**@Jonathan_Blow**

What would that actually mean, in terms of hardware? I assume you don't mean that the GPU would have a CPU on package, because that's really no different than a Strix Halo or Core Ultra, etc.

**2/** **@Jonathan_Blow** ^2060493241863274529

**@cmuratori**

I mean the GPU is certainly a turing machine that could just run everything. But the amount of friction to overcome to make this happen is pretty close to infinity.

**3/** **@AgileJebrim** ^2060515438220431409

No actual physical hardware is a Turing machine…

Programming languages just simulate a TM as a VM target. Frankly it’s an absurd notion imo and it is a common misunderstanding that a TM is even required to be able to compute anything. TMs can’t even compute when they’ll halt when other types of machines can. 😂

**4/** **@Jonathan_Blow** ^2061125697062727995

**@AgileJebrim** **@cmuratori**

Sir, this is a Wendy’s.

**5/** **@cmuratori** ^2060557646038749535

**@Jonathan_Blow**

It's a turing machine but it's in-order, 1/3rd the clock rate, and has much higher L2 cache latency. So if you tried to execute any of the code people currently run on their computers, I imagine it would slow down by a massive factor? Not sure how to ballpark it - maybe 1/200?

**6/** **@Jonathan_Blow** ^2060633711738331288

**@cmuratori**

Yeah, I just think you could do some small things to reduce that factor by a lot, without having to make a whole CPU on the GPU. But it's not what they are doing, so it doesn't matter.

**7/** **@raggi** ^2060799423781945385

**@Jonathan_Blow** **@cmuratori**

Still not clear on the desire though? Do you want gpu style isa? You want uma with gpu memory? You want more parallelism closer to main?

**8/** **@Jonathan_Blow** ^2061125198917845451

**@raggi** **@cmuratori**

I want the massive massive shit pile to be slightly smaller.

**9/** **@raggi** ^2061125393399370080

**@Jonathan_Blow** **@cmuratori**

don’t we all :-)

## Related

- Spine: [[archive/threads/Jonathan_Blow/2026-05-29-usually-i-would-expect-this-to-be-lame]]
