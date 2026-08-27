---
title: "@AgileJebrim Unfortunately few know how to author programs that could fit in the GPUs tiny instruction caches."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2060536518024855743"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2060536518024855743"
date: 2026-05-30
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim Unfortunately few know how to author programs that could fit in the GPUs tiny instruction caches."
in_reply_to: ""
parent_post_id: "2060513369065754969"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2060536518024855743
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-05-30 01:39:23

## Branch

**1/** **@NOTimothyLottes** ^2060536518024855743

**@AgileJebrim**

Unfortunately few know how to author programs that could fit in the GPUs tiny instruction caches. They definitely overbuild scalar SALU capacity on AMD , if stick to wave64 for parallel vector work, there are lots of free issue slots for scalar workloads.

**2/** **@AgileJebrim** ^2060536966194556958

**@NOTimothyLottes**

This is why we’re doing our own custom visual shader language. They’ll be required to make passes of a limited instruction size and data buffers of a limited size. We can talk more about it privately.

**3/** **@NOTimothyLottes** ^2060538886539837470

**@AgileJebrim**

For one employer, one of my projects actually pushes the limit of the I$ for a complex vector workload. It requires rethinking classic GPU workload distribution.

**4/** **@NOTimothyLottes** ^2060539563378942151

**@AgileJebrim**

Traditional GPU kernel launch goes wide first. So if you have say just enough work in the kernel to fill the GPU once, you never hit good efficiency due to servicing I$ misses across all those caches.

**5/** **@NOTimothyLottes** ^2060540118390186338

**@AgileJebrim**

So small tasks on the GPU require persistent waves looping through work instead, limiting launch to say one CU and running for longer. This way enough of the workload runs in the warmed I$.

**6/** **@AgileJebrim** ^2060541173685436901

**@NOTimothyLottes**

Nah. We’re literally aiming for a single persistent dispatch to rule them all, controlling all the SMs/CUs/EUs in full shader-side. Never letting the CPU even have a chance at interfering.

**7/** **@NOTimothyLottes** ^2060542249574764955

**@AgileJebrim**

Oh I’ve gone there, always get limited by vendor shader compilers that cannot handle large shaders. Need a large tool bag of workarounds to trick the compiler into not doing common sub expression elimination (especially for memory ops)

**8/** **@NOTimothyLottes** ^2060543164994159077

**@AgileJebrim**

If the vendors just opened up gfx apis to external shader
compilation with 3rd party tool chains we could easily start a GPU programming golden age, one compiled kernel just like the CPU.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-30-i-dont-think-hardware-vendors-are-going-to]]
