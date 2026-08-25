---
title: "How about a mega thread on the mechanics of CPU/GPU communication."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1671264312516829184"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1671264312516829184"
date: 2023-06-20
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "How about a mega thread on the mechanics of CPU/GPU communication."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1671264312516829184
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-06-20 21:10:37

## Thread

**1/**

How about a mega thread on the mechanics of CPU/GPU communication. Using AMDgpu based timing  results on the SteamDeck an example, but relating to the larger picture of PC GFX APIs like Vulkan/etc. I don't claim to know all, so experts feel free to add your wisdom :)

![](https://pbs.twimg.com/media/FzGF4owWwAMsc2I?format=png&name=orig)

**2/**

Both RADV and AMDVLK: Flush/invalidate mapped memory ranges is a NOP. So bus-crossing dGPU traffic to HOST_VISIBLE is automatically snooping CPU caches. The one without HOST_CACHED, is Write+Combined [WC] on store, and Uncached [UC] on read.  The one with HOST_CACHED is non-WC/UC

![](https://pbs.twimg.com/media/FzGG4OnWwAEu19H?format=png&name=orig)

**3/**

In AMDgpu (the kernel driver), likely DEVICE_LOCAL maps to AMDGPU_GEM_DOMAIN_VRAM (also the carve out on APUs) and the non-DEVICE_LOCAL maps to AMDGPU_GEM_DOMAIN_GTT

![](https://pbs.twimg.com/media/FzGJkkFWwAEBowR?format=png&name=orig)

**4/**

AMD+RADV added {DEVICE_COHERENT_BIT_AMD,
DEVICE_UNCACHED_BIT_AMD} variations to the core 4 memory types. Likely to support GPU crash debug. But also provides a way to avoid needing to write-back (flush) GPU caches before CPU read. Likely AMDgpu kernel flag mapping below.

![](https://pbs.twimg.com/media/FzGKZ_bWcAE3cGh?format=png&name=orig)

**5/**

This AMDGPU_GEM_CREATE_CPU_GTT_USWC appear to toggle on WriteCombine [WC] for CPU store, and Uncached [US] for CPU reads (cases of HOST_VISIBLE without HOST_CACHED)

![](https://pbs.twimg.com/media/FzGL03LXgAEeO0K?format=png&name=orig)

**6/**

For review from https://chipsandcheese.com/2023/03/05/van-gogh-amds-steam-deck-apu/ Deck bandwidths: ~71 GB/s GPU, ~43 GB/s DMA, ~34 GB/s shader copy CPU<->GPU, ~25 GB/s CPU/CPU, and damn, brutal 0.27 GB/s CPU mapped GPU buffer reads, 0.71 GB/s CPU mapped GPU buffer writes

![](https://pbs.twimg.com/media/FzGNGBuWAAA6wlr?format=png&name=orig)
![](https://pbs.twimg.com/media/FzGNlFvWwAANhH4?format=png&name=orig)

**7/**

And going direct to AMDgpu instead of VK on the Deck shows these kinds of bandwidths (non-DEVICE_LOCAL,  HOST_VISIBLE with HOST_CACHED and without). So using Write-Combined is amazingly painful for stores.

![](https://pbs.twimg.com/media/FzGO3XdWIAAQl3V?format=png&name=orig)

**8/**

Implies that the choices one might make on dGPU PC don't necessarily port over to APUs at all. Another challenge: it takes almost 7 seconds to zero-fill using a 64-bit store for() loop the 8-GiB of mapped memory. Hints at why load times are such a challenge even in the best case.

**9/**

This all hints at why PC OS derived systems are lacking in stuffing GPU VRAM. Really need some kind of bus mastered DMA (zero-copy) between non-volatile storage (disk) and GPU DRAM to avoid this CPU-touching performance tax.

Branches: [[archive/threads/NOTimothyLottes/2023-06-20-how-about-a-mega-thread-on-the-mechanics-of-cpu/2023-06-20-never_released-on-linux-nvidia-has-a-very-good-uvm-however-the]], [[archive/threads/NOTimothyLottes/2023-06-20-how-about-a-mega-thread-on-the-mechanics-of-cpu/2023-06-20-SheriefFYI-great-thread]], [[archive/threads/NOTimothyLottes/2023-06-20-how-about-a-mega-thread-on-the-mechanics-of-cpu/2023-06-20-NOTimothyLottes-or-for-an-apu-a-way-to-have-the-storage-device]]
