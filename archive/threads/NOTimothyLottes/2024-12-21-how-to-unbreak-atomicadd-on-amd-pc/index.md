---
title: "__/ How to Unbreak AtomicAdd on AMD PC \\__"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1870329223455334599"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1870329223455334599"
date: 2024-12-21
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "__/ How to Unbreak AtomicAdd on AMD PC \\__"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1870329223455334599
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-12-21 04:43:30

## Thread

**1/** **@NOTimothyLottes** ^1870329223455334599

__/ How to Unbreak AtomicAdd on AMD PC \__
This thread is brought to you by @AgileJebrim who solved the problem despite not working on it!

Added another chapter to the AMD PC Compiler bugs section in the "Fixing the GPU" shared doc

![](https://pbs.twimg.com/media/GfS-aiyXsAABbCq?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2024-12-21-how-to-unbreak-atomicadd-on-amd-pc/2024-12-21-axelgneiting-i-will-never-ever-understand-how-a-company]]

**2/** **@NOTimothyLottes** ^1870329811815550995

Related bugs and workarounds
(1.) Use gl_LocalInvocationID.x and 1D dispatches
Because that value is in a VGPR at dispatch
(2.) Don't use gl_SubgroupInvocationID because that invokes 2 instructions to compute the lane
...

**3/** **@NOTimothyLottes** ^1870330281162371404

(3.) Don't use subgroupElect() ever
Because even at the beginning of the shader while the compiler knows all lanes are active, it won't just pick lane 0, instead it will do many instructions to figure out the lane count and which lane is first and branch!

![](https://pbs.twimg.com/media/GfS_ahrWcAUlWan?format=png&name=orig)

**4/** **@NOTimothyLottes** ^1870330797107851446

Those are the easy ones, now lets look at what the compiler does if you know what you are doing and predicate an atomicAdd to the first lane ... you get this monstrosity!

![](https://pbs.twimg.com/media/GfS_xqkWAAAM3rB?format=png&name=orig)

**5/** **@NOTimothyLottes** ^1870331538526601233

The compiler injects it's (anti-)"perf strategy" without doing any checks if it should be used or not

So the question is, how to robustly work around this bad behavior?

**6/** **@NOTimothyLottes** ^1870332249448587503

Workaround seems to be to take a page from @AgileJebrim 's playbook and just stop branching. Instead of predicating the atomic to one lane, set the address of the atomic dynamically to an out of bounds value for all lanes but the first lane.

![](https://pbs.twimg.com/media/GfTBNUNXMAA-AKo?format=png&name=orig)

**7/** **@NOTimothyLottes** ^1870332859614953959

**@AgileJebrim**

Some important points
(a.) I don't know if this works for an SSBO, if it might not get HW bounds checking, it won't work
(b.) This will NEVER work for general 64-bit pointers
(c.) Effectively you need to use STORAGE_TEXEL_BUFFERs

**8/** **@NOTimothyLottes** ^1870333184933581014

**@AgileJebrim**

This bad compiler behavior and it's associated workaround is yet another reason moving to 64-bit pointers is Dead on Arrival.

**9/** **@NOTimothyLottes** ^1870333747893047506

**@AgileJebrim**

So for imageStores it's a no-brainer to never predicate the store, just rely on the cacheline per clock store address coalescing behavior. At a minimum it reduces all same address stores to one store, and that store is disabled by the out-of-bounds address ...

**10/** **@NOTimothyLottes** ^1870334100550144274

**@AgileJebrim**

For atomics this relies on the HW to efficiently throw out bad address requests early before doing the same-address request replay (these are atomics), this is something I still need to profile to know for sure what HW this works well on

**11/** **@NOTimothyLottes** ^1870334592411922580

**@AgileJebrim**

If this is a robust workaround, it likely means I'd never do any lane predication at all in any shader moving forward. Strict wave-coherent execution.

Branches: [[archive/threads/NOTimothyLottes/2024-12-21-how-to-unbreak-atomicadd-on-amd-pc/2024-12-21-AgileJebrim-i-like-select-instructions-for-this-purpose-since]]
