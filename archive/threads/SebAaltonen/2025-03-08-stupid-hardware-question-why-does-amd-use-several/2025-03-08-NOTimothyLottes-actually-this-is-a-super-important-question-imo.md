---
title: "@SebAaltonen Actually this is a super important question IMO."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1898352640825651644"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1898352640825651644"
date: 2025-03-08
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen Actually this is a super important question IMO."
in_reply_to: ""
parent_post_id: "1898272635277967509"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1898352640825651644
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-03-08 12:38:33

## Branch

**1/** **@NOTimothyLottes** ^1898352640825651644

**@SebAaltonen**

Actually this is a super important question IMO. 

For a review of how this works on NVIDIA: https://arxiv.org/pdf/1903.07486
6 physical dependency barriers
opcodes have {6-bit wait barrier mask, 3-bit read barrier index, 3-bit write barrier index}

So don't need a u64 bitmask

**2/** **@NOTimothyLottes** ^1898354182895145287

**@SebAaltonen**

AMD pre-GCN was a fixed TEX/ALU clause based arch. GCN went to their counter system (decade+ back). So there is a very long compiler & HW design technical debt inertia probably keeping the HW design on this counter based evolutionary tract

**3/** **@NOTimothyLottes** ^1898355207085412488

**@SebAaltonen**

K$ loads are out of order, so the only counter that makes any sense is 0, ie waiting until all prior loads have finished.

VMEM loads had traditionally been in-order only so counter made more sense. AMD's compiler would trickle-feed waits so tiny bits of VALU could move forward..

**4/** **@NOTimothyLottes** ^1898355695017201734

**@SebAaltonen**

Vs say pre-GCN which was all-or-nothing. And vs NV which is all (for the mask of 6 barriers or nothing). So I think the counter design mixed with in-order VMEM was an attempt to reduce latency at the time

**5/** **@NOTimothyLottes** ^1898356057782571048

**@SebAaltonen**

And also keep in mind TEX$ had traditionally been very small with respect to the number of clients (waves). So cacheline life was quite short, so in-order with counter like this might have had line-life benefits

**6/** **@NOTimothyLottes** ^1898356807229174069

**@SebAaltonen**

However in modern times TEX$ is bigger, and ALU issue is faster (compared to GCN's round robin wave64 on simd16). Also modern GPUs have operand caching. And trickle feeding waitcnts would break operand caching (more irregular switching to other waves) ...

**7/** **@NOTimothyLottes** ^1898357381806850073

**@SebAaltonen**

And at the point where vector memory requests can go out-of-order (hit-under-miss, etc), counters are just legacy baggage that might not really make sense any more ...

**8/** **@NOTimothyLottes** ^1898358090556211565

**@SebAaltonen**

Also the elephant in the room, dynamic wave scheduling. In theory with a chunky granularity design like NVIDIA, NVIDIA could build in hardware wave scheduling something that tries to keep waves at similar barriers! ->

**9/** **@NOTimothyLottes** ^1898358611874549939

**@SebAaltonen**

-> Meaning better uniform forward progress of groups of waves. Trying to keep higher cache reuse. Where as AMD oldest first does allow the older wave(s) to get extremely out-of-sync with possible cache reuse across waves

**10/** **@NOTimothyLottes** ^1898359204911448387

**@SebAaltonen**

On AMD I've always wanted to try to play with waitcnt placement for better dynamic scheduling (chunky vs fine-granularity, etc) BUT AMD refuses to ever allow ASM shaders in CS VK (even though ROCm supports ASM shaders without VK) ->

**11/** **@NOTimothyLottes** ^1898360479778545879

**@SebAaltonen**

I do know traditionally that AMD often has a lot of trouble getting to 100% utilization of ALU-bound stuff. Typically sitting in the low 90%s instead, all due to wave scheduling (oldest first VALU base camping, preventing other waves to get VMEM issue out = bubbles) ->

**12/** **@NOTimothyLottes** ^1898361569982984570

**@SebAaltonen**

AMD also wouldn't provide any access to s_setprio via intrinsics. So the two most important scheduling tools {waitcnt placement/grouping,setprio} are simply non-accessible to us "idiots" (who could never actually responsibly use intrinsics)

**13/** **@NOTimothyLottes** ^1898362253230903368

**@SebAaltonen**

So what we actually do on AMD, is to do semi-persistent (or fully persistent) waves that instead of exiting, loop through groups of work instead. And this can sometimes actually fix HW scheduling issues by depending on oldest-first schedule behavior ->

**14/** **@NOTimothyLottes** ^1898362581913411642

**@SebAaltonen**

Effectively the more scheduling one takes away from the dynamic HW scheduler and places instead into the static scheduling of a compiler, often seriously improves behavior by removing the worst case dynamic irregular behavior at runtime ->

**15/** **@NOTimothyLottes** ^1898362900479094936

**@SebAaltonen**

I say "sometimes" because if you get out of I$ you hit perf death. And if the compiler explodes VGPR count then typically it can also be perf-death too

**16/** **@NOTimothyLottes** ^1898363452063728020

**@SebAaltonen**

Historically the highest utilization stuff on AMD hardware would be 4-2 waves/SIMD actually [multiple work/wave] ... which will come to a surprise to UE material shader people who are dead in the water on performance at that wave count [single work/wave] ...

**17/** **@NOTimothyLottes** ^1898364719573971083

**@SebAaltonen**

[IRONY] those who actually know what they are doing on AMD are fixed high-register-count low-wave-count persistent-wave folks with unrolling and static scheduling-focused (VS) the masses are lower-register-count high-wave-count non-persistent-wave dynamic-sched focused

**18/** **@NOTimothyLottes** ^1898365132591247490

**@SebAaltonen**

One other point: in HW, how many waves should one actually keep live? The answer is only enough to reach high highest perf. But how does one build hardware to do that? With NVIDIA's design I think it is a lot easier, with the chunky barriers

**19/** **@SebAaltonen** ^1898440015182729598

**@NOTimothyLottes**

I said WG_RR_EN (round-robin arbitration) in the RDNA4 ISA-docs, but no explanation. Wondering what this is.

**20/** **@NOTimothyLottes** ^1898448182566076787

**@SebAaltonen**

I think it means oldest-workgroup first scheduling with round-robin scheduling across waves in the workgroups at the given workgroup priorities.

**21/** **@AgileJebrim** ^1898365622955786473

**@NOTimothyLottes** **@SebAaltonen**

What about losing shader occupancy and the latency-hiding benefits it provides for memory ops?

**22/** **@NOTimothyLottes** ^1898366617559482567

**@AgileJebrim** **@SebAaltonen**

The higher the occupancy the higher the clients on the caches = the lower the cache/client. So you never actually want highest occupancy, you want lowest occupancy that enables just enough latency hiding to keep highest utilization ...

**23/** **@NOTimothyLottes** ^1898367105537306918

**@AgileJebrim** **@SebAaltonen**

... To be more detailed, what you really really want, is to keep the memory requests grouped by locality (for highest cache hit rate) and NO unnecessary bubbles in the memory request queues that would result in ALU stalling !!! - this is basic real-world supply chain management

**24/** **@AgileJebrim** ^1898369377801581028

**@NOTimothyLottes** **@SebAaltonen**

Now what if you want to reuse the same shared memory buffer for a larger workgroup rather than needlessly duplicating it with many smaller workgroups? Wouldn’t that be an argument for a larger workgroup size than 64,1,1?

**25/** **@NOTimothyLottes** ^1898370376486236270

**@AgileJebrim** **@SebAaltonen**

Right, that is the CU-sized workgroup. Something that takes over the full CU. That is one of the persistent-wave usage models. But a CU-sized workgroup for non-persistent work is perf-death, because of the idle time during workgroup barriers (horrible with oldest-wave sched)

**26/** **@AgileJebrim** ^1898371880400163008

**@NOTimothyLottes** **@SebAaltonen**

I’m not as well versed in AMD. 4 SIMDs per CU, so do 64x4 = 256 invocations per workgroup?

**27/** **@NOTimothyLottes** ^1898374853507346826

**@AgileJebrim** **@SebAaltonen**

That topic gets complex with RDNA: CU vs WGP mode, wave32 vs wave64, 8 vs 12 VGPRs per allocation granularity, etc

**28/** **@AgileJebrim** ^1898378086829236447

**@NOTimothyLottes** **@SebAaltonen**

Managed to get this info out of Grok.

![](https://pbs.twimg.com/media/GlhkzywXMAAQJQf?format=jpg&name=orig)

**29/** **@AgileJebrim** ^1898379236173320496

**@NOTimothyLottes** **@SebAaltonen**

Oh.

![](https://pbs.twimg.com/media/Glhl2ruXUAA1bhu?format=jpg&name=orig)

**30/** **@AgileJebrim** ^1898379449038500054

**@NOTimothyLottes** **@SebAaltonen**

Seems like just using 128 is a safe bet for most hardware?

**31/** **@NOTimothyLottes** ^1898382213080605002

**@AgileJebrim** **@SebAaltonen**

Yeah safe bet like one-size-fits-all unisex underwear

**32/** **@AgileJebrim** ^1898382509865382170

**@NOTimothyLottes** **@SebAaltonen**

😆

**33/** **@AgileJebrim** ^1898385745892495810

On the flip side, it appears that using 128 would only use half the register file capacity on each. If we did 256 instead, then when the hardware scheduler became active, I imagine it’d only have a single choice to choose from for another thread to schedule and can use 255-256 registers each?

![](https://pbs.twimg.com/media/GlhrxYPWMAAAAY0?format=jpg&name=orig)
![](https://pbs.twimg.com/media/GlhrxYRXQAEamW5?format=jpg&name=orig)

**34/** **@AgileJebrim** ^1898386242405834880

**@NOTimothyLottes** **@SebAaltonen**

I’m imagining scheduler going back and forth between the same two SIMDs but dunno if such even distribution is what would actually happen in practice?

## Related

- Spine: [[archive/threads/SebAaltonen/2025-03-08-stupid-hardware-question-why-does-amd-use-several]]
