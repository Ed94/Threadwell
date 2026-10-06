---
title: "Thread: Serious talk on SteamDeck 2 speculation starting with numbers based on the nice summary here https://www.youtube.com/watch?v=QSg5pjkcg9E - TLDR, actually this is exciting if true."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2106566586819609002"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2106566586819609002"
date: 2026-10-04
archived: 2026-10-06
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Thread: Serious talk on SteamDeck 2 speculation starting with numbers based on the nice summary here https://www.youtube.com/watch?v=QSg5pjkcg9E - TLDR, actually this is exciting if true."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2106566586819609002
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-10-04 02:06:27

## Thread

**1/** **@NOTimothyLottes** ^2106566586819609002

Thread: Serious talk on SteamDeck 2 speculation starting with numbers based on the nice summary here https://www.youtube.com/watch?v=QSg5pjkcg9E - TLDR, actually this is exciting if true.

![](https://pbs.twimg.com/media/HTwFo0YXAAAyit8?format=jpg&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2026-10-04-thread-serious-talk-on-steamdeck-2-speculation/2026-10-04-SebAaltonen-funny-that-they-say-actual-fp32-compute-meaning]]

**2/** **@NOTimothyLottes** ^2106568550907552156

Lets talk 2 configurations based on Moore's Law is Dead  (MLID) and The Phawx speculation numbers,

Estimated SteamDeck 2/
RDNA3.5 3.2 GHz * 12 CU = 38.4

MLID estimate of another handheld
RDNA5 1.2-1.65 GHz * 16 CU = 19.2-26.4

Given that estimated comparison, I'd go Deck2

**3/** **@NOTimothyLottes** ^2106569141523980382

SteamDeck has historically had rather amazing power slosh ability - if they keep this with the Deck2 and focus on higher peak clocks, it will be easy to get the CPUs to idle and actually leverage what the GPU can do!

**4/** **@NOTimothyLottes** ^2106569394864148635

As for ALU:BANDWIDTH, I'll be ALU-bound, so it's ok to be thin in the bandwidth department IMO.

**5/** **@NOTimothyLottes** ^2106570564768862394

As for RDNA 3.5 vs RDNA 5 - no plublic RDNA 5 ISA guide yet. RDNA 3.5 already has the one interesting thing of scalar FP32 ops. MLID says 40-50% more "raster" for RDNA 5 vs 3.5, but I doubt it. 3.5 already has dual issue FP32. Where you going to find 50% more IPC?

**6/** **@NOTimothyLottes** ^2106571626569711985

Can easily push near 100% VALU issue on prior RDNA architectures before dual FP32 issue. With dual FP32 issue (3.5 has), get some amount above that of effective IPC. The next logical evolution is polishing some of the dual corner cases, but that won't bring 50% IPC in practice.

**7/** **@NOTimothyLottes** ^2106572522846147019

RT is effective useless on bandwidth and cache constrained portable. And ML scaling is crap. So whatever RDNA5 brings to the table for RT and ML is simply more static parasitic power draw.

**8/** **@NOTimothyLottes** ^2106573070970306793

In the end if the rumored Deck 2 specs are true, in optimized code like what I'd do, you'd see a 3x realized perf increase. And that would be way better than any RDNA5 portable that didn't have matching clock*CU count capability.

**9/** **@NOTimothyLottes** ^2106573791384215909

IMO Valve would be genius to just ship the same 800p OLED. A 3x ALU perf boost with no need to push 2x or more pixels, would make devs quite happy, something that actually feels quite a bit faster.

**10/** **@NOTimothyLottes** ^2106574254456111306

But I'd expect the obvious mistake of going to 1080p or 1440p. And I'd mitigate that with a CRT emulation scaling to simulate a lower resolution display. That would be a little perf tax, but nothing horrible like an ML TAA pass.

**11/** **@NOTimothyLottes** ^2106578083260289486

The real danger that this possible Deck 2 presents is this: it's Linux, you don't have to use Vulkan, you can go direct to the kernel driver. Someone could use AI to write a PS5 shader binary to RDNA 3.5 binary translator, and then do direct emulation of system libraries.

**12/** **@NOTimothyLottes** ^2106579520711242085

If Deck 2 would release with similar sales as Deck 1, it's past the threshold of being interesting for a single indie for a to-the-metal non-portable game too, ie something going direct to the kernel drivers with assembly shaders.

**13/** **@NOTimothyLottes** ^2106580194249281995

Also one has to wonder this, if the AI slop-gramming tools are as good as people claim they are, why use C? why use Vulkan? Why not just slop-gram direct to assembly on GPU? Challenge someone to go there.
