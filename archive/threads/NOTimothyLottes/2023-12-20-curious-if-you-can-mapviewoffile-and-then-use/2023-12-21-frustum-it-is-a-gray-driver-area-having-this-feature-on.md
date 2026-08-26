---
title: "@NOTimothyLottes It is a gray driver area."
type: archive
source: twitter
source_url: "https://x.com/frustum/status/1737629120492912667"
author: "Alexander Zapryagaev"
handle: frustum
post_id: "1737629120492912667"
date: 2023-12-21
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes It is a gray driver area."
in_reply_to: ""
parent_post_id: "1737618231450579351"
---

## Source

- URL: https://x.com/frustum/status/1737629120492912667
- Author: Alexander Zapryagaev (@frustum)
- Posted: 2023-12-21 00:20:40

## Branch

**1/** **@frustum** ^1737629120492912667

**@NOTimothyLottes**

It is a gray driver area. Having this feature on all GPUs would be awesome. However, it will face a serious problem known as the 4GB SSBO size limitation.

**2/** **@NOTimothyLottes** ^1737631902725537866

**@frustum**

Sure, but even for <4GiB it would be useful. However I doubt it actually works at all, because it implies page locking parts of the page cache. I'm trying just 2 MiB thus far and have not got it working. But it's Vulkan, so any number of other stupid things could go wrong.

**3/** **@frustum** ^1737634564938543253

**@NOTimothyLottes**

Our cross-GPU buffer mapping works properly. I will try to import a memory mapped file on Linux and Windows tomorrow.

**4/** **@frustum** ^1737743235769114667

**@NOTimothyLottes**

It's working pretty well with:
Nvidia DGPU Windows/Linux - ok (RW mmap)
AMD DGPU/IGPU Windows - ok (RW mmap)
Apple (Metal) - ok (R and RW mmap)

**5/** **@never_released** ^1737796103712497921

**@frustum** **@NOTimothyLottes**

Note that host pinned mem is not cacheable on the GPU side though.

On Linux w/ NVIDIA dGPUs you can also have HMM, but that’s not leverageable on gfx APIs

**6/** **@NOTimothyLottes** ^1737807709926281372

**@never_released** **@frustum**

Certainly didn't translate that one. By "not cacheable on GPU" -> {read is a forced miss, and store through the bus}? Just wondering, why would an app provided address mapping require a different GPU page mapping cache policy than a driver address mapping?

**7/** **@never_released** ^1737808182204919927

**@NOTimothyLottes** **@frustum**

It's because PCIe isn't quite a coherent interconnect, so the way to achieve coherency on it w/o page migration is to have memory accesses be uncached on the remote side (the one that doesn't have the data in its local memory).

**8/** **@NOTimothyLottes** ^1737811922722996266

**@never_released** **@frustum**

Still missing something, or my knowledge is wrong: standard VK driver practice on host-side-allocations is GPU hit-on-read. Because: 4k pass = around 128k 8x8 workgroups, if loading a constant from a host-side-allocation, with miss-on-read that's 128k misses to the same address

**9/** **@NOTimothyLottes** ^1737813509189071350

**@never_released** **@frustum**

... only coherency GPU sees on host allocations normally is at cache write-back and invalidate boundaries (explicit in command, or implicit post/pre-amble). So back to question: why would a driver force special uncached behavior for {app supplied pointer}, (vs) {driver mapping}?

**10/** **@never_released** ^1737819525712671027

**@NOTimothyLottes** **@frustum**

> ... only coherency GPU sees on host allocations normally is at cache write-back and invalidate boundaries […]

Not applicable to use of VkImportMemoryHostPointerInfoEXT on multiple drivers that I know of, where it’s just a straight map over PCIe.

**11/** **@NOTimothyLottes** ^1737820845932687825

**@never_released** **@frustum**

Certainly some mini-profiling is in order to verify what actual driver behavior is

## Related

- Spine: [[archive/threads/NOTimothyLottes/2023-12-20-curious-if-you-can-mapviewoffile-and-then-use]]
