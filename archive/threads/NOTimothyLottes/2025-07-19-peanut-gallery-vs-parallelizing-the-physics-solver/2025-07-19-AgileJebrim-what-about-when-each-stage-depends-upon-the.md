---
title: "@NOTimothyLottes What about when each stage depends upon the results of the previous stage?"
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1946573560840958248"
author: "Jebrim"
handle: AgileJebrim
post_id: "1946573560840958248"
date: 2025-07-19
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes What about when each stage depends upon the results of the previous stage?"
in_reply_to: ""
parent_post_id: "1946453750085808492"
---

## Source

- URL: https://x.com/AgileJebrim/status/1946573560840958248
- Author: Jebrim (@AgileJebrim)
- Posted: 2025-07-19 14:11:17

## Branch

**1/** **@AgileJebrim** ^1946573560840958248

**@NOTimothyLottes**

What about when each stage depends upon the results of the previous stage?

**2/** **@AgileJebrim** ^1946574048575533243

**@NOTimothyLottes**

I guess that’s the same question as this. I think it’s still fine to have some gaps when syncing but to better aim for more evenly distributed execution times between cores and to keep these sync points to a minimum.

https://x.com/jakubtomsu_/status/1946485199006498933?s=46&t=ZbNecpPBsBMrvteeaA6IcA

**3/** **@NOTimothyLottes** ^1946576354905911587

**@AgileJebrim**

What do you do if a worker in a wide-multithread dependency chain gets preempted? The house of cards should fall right? Or one can offer self healing, instead of waiting on a specific fine grain dependency, use work duplication to avoid waiting.

**4/** **@AgileJebrim** ^1946577376915120212

**@NOTimothyLottes**

You just don’t allow for preemption to occur. I assume we’re talking OS/CPUs at this point rather than GPUs. You pin threads to cores and assign them the highest criticality/priority. On Linux we use the FIFO scheduler and isolate the OS, drivers, and IRQs to non-critical cores.

**5/** **@AgileJebrim** ^1946577673179861353

**@NOTimothyLottes**

There’s a bit of OS configuration involved to achieve this.

**6/** **@AgileJebrim** ^1946578113657237820

**@NOTimothyLottes**

Disabling SMT/hyperthreading is another one.

**7/** **@AgileJebrim** ^1946578976064835720

**@NOTimothyLottes**

All of this works fine if you control the hardware and system yourself but is more problematic if you don’t. This is one of many reasons why I’d prefer living within a GPU dispatch instead. Much harder to get interrupted by anything and much more portable on end user machines.

**8/** **@NOTimothyLottes** ^1946596411513954798

**@AgileJebrim**

Unfortunately consumer platforms with GPUs have OEM overlords who take over the GPU with irregular behavior for their purposes. Things like multi-monitor with OS windowing compositors are norm and highly irregular behavior.

**9/** **@AgileJebrim** ^1946596970304278694

**@NOTimothyLottes**

Even NVIDIA’s DriveOS/Tegra platform with Vulkan SC is using a compositor. That surprised me.

**10/** **@AgileJebrim** ^1946597247954612264

**@NOTimothyLottes**

Ironically their non-certified Vulkan SC driver on Windows does not and completely bypasses it with direct to display.

**11/** **@AgileJebrim** ^1946598012152959081

**@NOTimothyLottes**

Quite frankly, I think we in the flight sim industry should consider using direct-to-display. See this extension:

VK_KHR_display

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-07-19-peanut-gallery-vs-parallelizing-the-physics-solver]]
