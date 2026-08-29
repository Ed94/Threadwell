---
title: "@AgileJebrim Easy."
type: archive
source: twitter
source_url: "https://x.com/kechogarcia/status/2058522912731123861"
author: "Kecho"
handle: kechogarcia
post_id: "2058522912731123861"
date: 2026-05-24
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim Easy."
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/kechogarcia/status/2058522912731123861
- Author: Kecho (@kechogarcia)
- Posted: 2026-05-24 12:18:02

## Branch

**1/** **@kechogarcia** ^2058522912731123861

**@AgileJebrim**

Easy. WaveActiveSum, then LDS atomic sum, then global memory sum between groups (if GPU has intrinsica) then finally dram atomics. 
Always go in cache hierarchy -> wave, LDS, global mem, vram

Never do an atomic per thread.

Also you can do it all in one persistent dispatch .

**2/** **@AgileJebrim** ^2058524431547306220

**@kechogarcia**

Say you have many more data elements than you have SIMD lanes across the hardware. How are you handling that?

**3/** **@kechogarcia** ^2058535071947145503

**@AgileJebrim**

Do it all in a persistent dispatch. Dispatch and fill the machine, then consume input.

**4/** **@AgileJebrim** ^2058539350262989272

**@kechogarcia**

What I’m looking for an answer to is what the for loop inside the persistent dispatch is doing at the smallest level. Are you looping over WaveActiveSums?

**5/** **@kechogarcia** ^2058546836697149904

**@AgileJebrim**

No. If you pad the buffer to wave size, just accumulate on 4 registers, 4 loads at a time. Or whatever the hw can do best. When you run out of work, then the problem is a cache hierarchical reduction. You can do it all in a single dispatch, no fancy  multipass bin reduction.

**6/** **@kechogarcia** ^2058548990413504538

**@AgileJebrim**

ldsV = 0;
GroupBarrier();
float4 a = 0;
while(has work())
     a += load4(popnext());

float4 perGroup = WaveActiveSum(a);

if (is first lane(() atomicAdd(ldsV, perGroup);

if (threadID == 0)
    atomicAdd(ldsV, dramBuffer[0];

Group mem shenanigans I have to read manual.

**7/** **@AgileJebrim** ^2058550742453989755

Okay good. I was looking for the partial sums per lane answer. You had left that out entirely in your initial answer. Reductions in a loop would be expensive.

If I told you there were 16m unsigned integer elements to sum up, what other requirement would necessarily need to exist (or otherwise be addressed) and what other optimization opportunities would arise as a result of that knowledge?

**8/** **@kechogarcia** ^2058558465270755676

**@AgileJebrim**

Hmmm. Means you could easily overflow, so now we gotta use 64 bits for accumulation? But this means we could double the number of sums on each thread by loading 64 bit primitives? Not sure I gotta think harder if you are looking for something else

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
