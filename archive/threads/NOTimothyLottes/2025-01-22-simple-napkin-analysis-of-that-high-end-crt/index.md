---
title: "Simple napkin analysis of that high-end CRT scalar (monochome one) ..."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1881908248544166159"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1881908248544166159"
date: 2025-01-22
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Simple napkin analysis of that high-end CRT scalar (monochome one) ..."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1881908248544166159
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-01-22 03:34:25

## Thread

**1/** **@NOTimothyLottes** ^1881908248544166159

Simple napkin analysis of that high-end CRT scalar (monochome one) ... notes about cleaning up the code.

I track state usage throughout the code to ballpark expected max VGPR count. This needs around 57 VGPRs mid way through. Note <=64 VGPRs is often important.

![](https://pbs.twimg.com/media/Gh3hVTEXQAAaDT8?format=png&name=orig)

**2/** **@NOTimothyLottes** ^1881908646743097773

So yeah packed 16-bit is the reason complex shaders like this are possible on PC GPUs. It is the way to single pass and avoid multiple trips through DRAM.

**3/** **@NOTimothyLottes** ^1881909208339357745

This code does 2 parallel kernels, but also breaks the computation of each kernel into 4 weighted sums. This is done for 2 reasons: (a.) possibly higher precision, (b.) to enable parallel work to hide VALU latency (ILP)!

![](https://pbs.twimg.com/media/Gh3iXwJX0AAfa2p?format=png&name=orig)

**4/** **@NOTimothyLottes** ^1881909849006715306

This shader needs roughly
410 VALU op clocks
And 253 of those (more than half)
are in the load latency window
So this shader will trivially hide a lot of latency without getting to high wave/CU counts

**5/** **@NOTimothyLottes** ^1881910192495022093

BUT
Traditionally this has been a curse, because AMD's oldest wave first scheduling breaks down when the oldest is ultra high VALU load without stalls! The other waves often cannot get forward progress to get loads out to debubble the memory sub-system

**6/** **@NOTimothyLottes** ^1881910835708383328

Worst case (no scaling, no compression) this would use 6-bytes/pixel of bandwidth (damn), and amortize closer to 4-bytes/pixel with scaling. And GPUs have capacity often for 32 VALU op clocks per byte. So this is certain to be VALU bound (410+ VALU clocks)

**7/** **@NOTimothyLottes** ^1881911435691008317

But things like Strix Halo (laptops) are quite a bit more bandwidth starved, so generally I try to stay VALU bound to be friendly towards scaling down

**8/** **@NOTimothyLottes** ^1881912737896534188

Estimation that something like a 7900 XT would be able to do over 10,000 of these passes at 4K per second, so this technique is good for 480 Hz! Of course I don't have a 7900 XT, and my only working AMD GPU laptop (the other has bad HDMI port) refuses to profile, so numbers later

**9/** **@NOTimothyLottes** ^1881915941455593681

Writing code (below, note FMA_MIX is the hot ticket for free FP32->FP16 conversion) with instruction intrinsic macros (that unfortunately map to high-level shader code). But it at least enables me to ballpark instruction counts. With one exception I count transcendentals as 4 ops

![](https://pbs.twimg.com/media/Gh3oMLCXcAErmE-?format=png&name=orig)

**10/** **@NOTimothyLottes** ^1881917527951122766

Can compare guesses with actuals on the disassembly/

76 VGPRs! haha, decade+ and AMD still cannot manage basic VGPR allocation well. This is using roughly 30% more VGPRs than needed. Historically AMD HW has bumped up the VGPR count and added NSA to fix their SW problems ...

![](https://pbs.twimg.com/media/Gh3pJhqXUAAgRLb?format=png&name=orig)

**11/** **@NOTimothyLottes** ^1881918542943297646

I use 13 transcendentals so adjusting my 410 count by -13*3 I get 371 VALU ops. The actual shader uses 438 (and is VALU bound) an extra 18% extra slop somewhere. Some of that is that I didn't count the CS swizzle logic (but that won't account for most of the extra 67 ops) ...

**12/** **@NOTimothyLottes** ^1881919883832959169

Some of the slop, it's not using NSA (this is GFX9), so lots of extra V_MOV_B32s. The gather offsets are packed in an extra VGPR so even if the base {v34,v35} are shared across all the gather4s, it's duplicating those VGPR pairs 8 extra times (no NSA here).

![](https://pbs.twimg.com/media/Gh3rlnsXcAAgKWR?format=png&name=orig)

**13/** **@NOTimothyLottes** ^1881923400882647110

GFX9 is Vega, so no NSA here, and 1 SGPR read per operation. It was RDNA1 that introduced the good stuffs (NSA and 2 SGPRs/op).

Can see below cases where 2 SGPRs are needed Vega will introduce extra V_MOV_B32 ops to put one in a VGPR.

![](https://pbs.twimg.com/media/Gh3vGmZWUAA0bwJ?format=png&name=orig)
![](https://pbs.twimg.com/media/Gh3vMCgXIAAAAoM?format=png&name=orig)
![](https://pbs.twimg.com/media/Gh3vR4UXAAAtGyK?format=png&name=orig)

**14/** **@NOTimothyLottes** ^1881925349245858028

Now some actual compiler bugs,
(1.) Vega has V_MAD_MIX, but the compiler won't use it, instead it wastes extra V_CVT_PKRTZ_F16_F32 ops
(2.) Compiler fails basic pattern matching with {x,-x} and instead issues extra V_PACK_B32_F16 ops

![](https://pbs.twimg.com/media/Gh3wpv9XQAAXJw1?format=png&name=orig)
![](https://pbs.twimg.com/media/Gh3xGSYWcAASW9Z?format=png&name=orig)
