---
title: "__/ Fixing AtomicAdd - Benchmarking AMD+NV \\__"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1870942850684420564"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1870942850684420564"
date: 2024-12-22
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "__/ Fixing AtomicAdd - Benchmarking AMD+NV \\__"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1870942850684420564
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-12-22 21:21:50

## Thread

**1/** **@NOTimothyLottes** ^1870942850684420564

__/ Fixing AtomicAdd - Benchmarking AMD+NV \__
RTX 3060
100% - if(lane==0) atomicAdd(adr,v*lanes) ... smart
84% - atomicAdd(adr,v) ... stupid
82% - atomicAdd(lane==0?adr:-4,v*lanes) ... mine

NV's compiler has same "bug" as AMD :)
My workaround is faster than their compiler too!

Branches: [[archive/threads/NOTimothyLottes/2024-12-22-fixing-atomicadd-benchmarking-amd-nv/2024-12-22-Meetem4-i-wonder-is-there-explainable-perf-and]], [[archive/threads/NOTimothyLottes/2024-12-22-fixing-atomicadd-benchmarking-amd-nv/2024-12-22-AgileJebrim-humor-me-have-you-tried-entering-in-atomicadd-adr]], [[archive/threads/NOTimothyLottes/2024-12-22-fixing-atomicadd-benchmarking-amd-nv/2024-12-22-RouaniJihad-im-not-going-to-pretend-i-understand-a-lick-of]]

**2/** **@NOTimothyLottes** ^1870943585388110229

Review/
So NV and AMD share the same "optimization" that works as an "anti-optimization" if you predicate the atomic to one lane. Neither checks if the dev actually knows what they are doing and had already predicated to just one lane ...

**3/** **@NOTimothyLottes** ^1870944106463031312

The best workaround however is to rely on BUFFER bounds checking: instead of predicating to one lane, conditionally set the lanes to disable to out-of-bounds addresses instead!

Because then the compiler silly behavior is disabled. And that actually is faster too!

**4/** **@NOTimothyLottes** ^1870944638183538927

My easy access AMD machine is an APU right now, and the numbers were not rock stable like the NV dGPU. So I didn't get exact % (as my test wasn't written with long enough runtimes). But the AMD behavior looks similar.

**5/** **@NOTimothyLottes** ^1870945104586035589

If anyone is wondering how I tested: I wrapped the code with clockRealtimeEXT() and then summed the total runtimes across all waves. I find that is often better than trying to invoke some external profiler. I also have live shader editing so I can watch the behavior live too :)
