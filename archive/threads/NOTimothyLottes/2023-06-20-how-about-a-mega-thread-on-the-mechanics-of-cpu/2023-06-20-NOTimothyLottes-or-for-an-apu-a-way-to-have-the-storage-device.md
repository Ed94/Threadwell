---
title: "Or for an APU, a way to have the storage device write direct to DRAM in pages setup for use on the GPU, because anything the CPU writes that the GPU reads is stuck on the strangled snooping bus or the strangled WC buffer limit on store."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1671279693104914434"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1671279693104914434"
date: 2023-06-20
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Or for an APU, a way to have the storage device write direct to DRAM in pages setup for use on the GPU, because anything the CPU writes that the GPU reads is stuck on the strangled snooping bus or the strangled WC buffer limit on store."
in_reply_to: ""
parent_post_id: "1671276990987370501"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1671279693104914434
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-06-20 22:11:44

## Branch

**1/** @NOTimothyLottes

Or for an APU, a way to have the storage device write direct to DRAM in pages setup for use on the GPU, because anything the CPU writes that the GPU reads is stuck on the strangled snooping bus or the strangled WC buffer limit on store.

**2/** @NOTimothyLottes

If the app tried to manage GPU memory oversubscription via these strangled CPU mappings you'd literally see many second stalls. One can only assume the kernel can do storage<->DRAM DMA for managing GPU DRAM oversubscription?

**3/** @NOTimothyLottes

Even if could fill VRAM in 1 sec, just 2x oversubscription of VRAM implies 1 sec delay to context switch (assuming 2 apps accessing all meM). So classic VM multitasking is useless. Only single app focus model with pinned memory makes any useful sense. Release pin on focus change.

**4/** @NOTimothyLottes

The trend is massive res massive VRAM paired with tiny IO bus. So the case for pinned memory and bus master transfers only grows importance as things evolve.

**5/** @NOTimothyLottes

Back to SteamDeck numbers: GTT (HOST_VISIBLE) + USWC (non-HOST_CACHED) takes 1 sec for 1st 4 GiB BO alloc, but *30 sec* for 2nd 4 GiB alloc. Kernel driver time for memory allocation (maybe page table related) can be brutal (general comment for PCs too).

**6/** @NOTimothyLottes

Related, I think Chips&Cheese CPU/GPU link DMA and Compute Bandwidths are only measured to a GTT+USWC buffer (only supporting useless uncached CPU reads). Bandwidth exceeds the CPU's bus capacity, implies it is 'garlic' or GPU bus only accesses, direct to DRAM ...

![](https://pbs.twimg.com/media/FzHOnZ_X0AEW7CE?format=png&name=orig)

**7/** @NOTimothyLottes

Since RADV+AMDVLK don't support user-space CPU mapped flush | invalidate, this implies the only supported mapping to read from DRAM direct is USWC (uncached R and write+combine W) ...

**8/** @NOTimothyLottes

Doing GPU stores to a CPU mapped GTT without USWC would be crippingly slow (limited by the snooping bus rate). But this is unfortunately the only option available for CPU read back. So if doing a shader store, it better be only a few waves and running in parallel.

**9/** @NOTimothyLottes

"Use GTT because it's as fast as VRAM on the Deck", could only work if GTT+USWC, as that would be only way to get Garlic (direct to DRAM high bandwidth bus). GTT without USWC would need Onion (slow snooping bus) because AMDgpu's only no-CPU map option is for VRAM!

![](https://pbs.twimg.com/media/FzHTDxCX0AADoM1?format=png&name=orig)

**10/** @NOTimothyLottes

Summary of the theory on best Steam Deck practices. This is the plan for my deck-compute-only driver too. Theory -> as in I haven't yet verified the GPU-side parts (my driver isn't that far along yet).

![](https://pbs.twimg.com/media/FzHZ_ZiWwAAdEkd?format=png&name=orig)

**11/** @NOTimothyLottes

Possible to do better? MAYBE! CPU readback actually has 2 problems, 1st the slow GPU-side copy (4 GiB copy via snooping bus could be almost 4 sec, but direct to DRAM via USWC might be just 160 ms). Also CPU only has 4 MiB of L3, so the majority of 4 GiB will be uncached later ...

**12/** @NOTimothyLottes

Believe UC MTYPE (uncached) forces the CPU into serialized behavior. My test was single thread 8-byte/access reads. https://uops.info/html-instr/VMOVDQA_M256_YMM.html#ZEN2 Looks like Zen2 might be able to get 32-byte/access via VMOVDQA, and going multi-threaded (8 thread), that might be a 32x speed up ..

**13/** @NOTimothyLottes

If so might be able to approach under a GB/s for the CPU-side part (UC multithread via VMOVDQA), which would be close enough to the non-USWC running single threaded using the cache.

**14/** @NOTimothyLottes

What you'd really want here as a band-aid workaround is ability for the GPU to act as if the CPU map was USWC (so go direct to DRAM), but have the CPU map act as non-USWC, so it goes through the cache. Then some kind of hack to flush the tiny 4 MiB L3 and lower caches on the CPU.

**15/** @NOTimothyLottes

CPU readback (reading and summing 8-byte) GTT without USWC:

1.16 GiB/s  1 thread
1.42 GiB/s  4 threads
1.48 GiB/s  8 threads

Going multi-core on cached readback doesn't really help much. Proper test, parked threads waiting on futex, signal, last-1st active core timing.

**16/** @NOTimothyLottes

Now CPU readback GTT+USWC

0.13 GiB/s 4 threads 8-byte reads
0.24 GiB/s 8 threads 8-byte reads
1.15 GiB/s 8 threads 32-byte MOVNTDQA

So measurements match theory, going multi-core with MOVNTDQA uncached read on GTT+USWC can be made to match 1 thread GTT (without USWC)

**17/** @NOTimothyLottes

Both those results above had been using a pair of 4 GiB allocations. The GTT+USWC one used one 4 GiB GTT+USWC for timing, and one 4 GiB GTT (unused). And that test suffered from a 30 sec GTT BO allocation. So something was going very wrong in the page mapping ...

**18/** @NOTimothyLottes

When I rerun same test with just one 4 GiB GTT+USWC allocation, the 30 sec stall is gone, and the performance also changes:

18.34 GiB/s - 8 threads x 32-byte MOVNTDQA (UC)

Oh!

Perhaps there is some resource limit that kills perf if too much memory gets mapped, page faults?

**19/** @NOTimothyLottes

Top with thread cumulative results doesn't show anything significantly different between the 4 GiB and 8 GiB runs in terms of page faults ... suggests it must be something else

![](https://pbs.twimg.com/media/FzJ9YrHXsAIfCOg?format=jpg&name=orig)
![](https://pbs.twimg.com/media/FzJ9Y5LWwAYyyjt?format=jpg&name=orig)

**20/** @NOTimothyLottes

And yet there is obviously a bug in my multi-core tests, you can tell directly from the page fault numbers, only one thread is taking all the faults. So it is back to finding my coding error (fail).

**21/** @NOTimothyLottes

Lunch break and fixed the bug. Two runs now and leaving threads open to get TOP results. First run definitely soaks up the page faults, second run is page fault free (expected). Both around only 7 GB/s.

![](https://pbs.twimg.com/media/FzKPZxUWABQ6oQJ?format=jpg&name=orig)

**22/** @NOTimothyLottes

And the 8 GiB of BO mapped, but only 4 GiB used run. The first pass gets only 1 GiB/s and the second gets 7 GiB/s. Page fault number is similar to last run, can only conclude page fault costs exploded?

![](https://pbs.twimg.com/media/FzKRF1OXsAE7c0-?format=jpg&name=orig)

**23/** @NOTimothyLottes

30 sec BO alloc time + super low bandwidth on 1st pass only (where page faults happen) suggest that Linux Kernel logic explodes in cost if too many pages are used in this way ...

**24/** @NOTimothyLottes

~8K faults for 512 MiB accessed / thread = 64 KiB/fault ... X86-64 has either 4 KiB or 2 MiB for page size. So not using large pages (fail). Probably mapping 16 pages per fault. Not sure if this implies anything about GPU page size (but certainly hoping it isn't 4 KiB, ouch).

**25/** @NOTimothyLottes

Some other very rough measured numbers of GTT+USWC with 8 cores splitting 4 GiB of BO.

~7 GiB/s R
~10 GiB/s W then R
~15 GiB/s W

I think these seem plausable now (so maybe no more code bugs).

**26/** @NOTimothyLottes

One takeaways of all this, is that you need to pre-warm the page tables for large mapped buffers (by touching all pages) when the user isn't waiting on results. And if you are doing batch jobs that {open device, send data to GPU, get data back, close device} you are screwed!

**27/** @NOTimothyLottes

And lastly (maybe) comparison of GTT and GTT+USWC both 8 threads splitting streaming through 4 GiB of mapping (second pass, no page fault issues):

R> ~14 GiB/s (GTT) and ~7 GiB/s (GTT+USWC)
W+R> ~14 GiB/s (GTT) and ~10 GiB/s (GTT+USWC)
W> ~13 GiB/s (GTT) and ~15 GiB/s (GTT+USWC)

**28/** @NOTimothyLottes

So an alternative option summary for those who don't want the extra GPU-side GPU to CPU mapped buffer copy step.

![](https://pbs.twimg.com/media/FzKlE0NXoAI74IA?format=png&name=orig)

**29/** @NOTimothyLottes

If anyone is looking to repro the 30 sec stall: amdgpu_bo_alloc() one 4 GiB GTT+USWC, then one 4 GiB GTT buffer, the second alloc causes the Deck to become unresponsive for 30 seconds

**30/** @NOTimothyLottes

madvise() with MADV_HUGEPAGE on mapped 4 GiB region doesn't do anything (still faults at 64 KiB granularity), and none of these MADV_{WILLNEED|POPULATE_READ|POPULATE_WRITE} have any effect either (still waits until use before faulting, causing low initial effective bandwidth)

**31/** @NOTimothyLottes

64KiB strided write through 4 GiB GTT+USWC (to pre-fault) costs the same as writing full 4 GiB, roughly 3 seconds. So it is quite literally massive page fault overhead for 1st access. No possible workaround found at this time for initial load time problems.

**32/** @NOTimothyLottes

If doing two 4 GiB GTT+USWC allocations, there is also a 30 second BO allocate cost on the 2nd one. And this makes the initial page fault cost for access to the first 4 GiB take another 30 seconds. Effectively hangs the machine for a full minute.

**33/** @NOTimothyLottes

Doing two 4 GiB GTT allocations (without USWC), doesn't incure any of the 30 second stalls. So that problem is specific to big USWC allocations. However the initial access page fault problem (extra 3 seconds) is there, so a 2ndary problem with just mapping lots of APU memory.

**34/** @NOTimothyLottes

Allocation of one 4 GiB GTT first then a 4 GiB GTT+USWC doesn't see the 30 second allocation stall. Almost like anything post a big USWC alloc is poisioned. And after mapping both, then accessing the GTT only, the 30 second time for page faulting comes back.

**35/** @NOTimothyLottes

Continuing from before, even if you don't map the 2nd GTT+USWC, the 30 second initial page faulting time is still there, so the act of mapping doesn't matter, simply doing the BO allocation had already doomed the Linux page management.

**36/** @NOTimothyLottes

Despite header docs which imply flag only works on DOMAIN_VRAM, using DOMAIN_GTT+AMDGPU_GEM_CREATE_NO_CPU_ACCESS is apparently what you want for non-mapped GTT allocations. Mapped 4 GiB GTT with 4 GiB GTT+NO_CPU, drops the initial page fault time from 30 seconds to 3 sec.

![](https://pbs.twimg.com/media/FzOqwUfXsAEsmC9?format=png&name=orig)

**37/** @DaveAirlie

@NOTimothyLottes

the problem there is usually tiling, GPUs expect graphicy things in VRAM to be tiled in very specific ways, it's hard to have a storage device do that. Using a transfer engine that can tile/detile makes a lot more sense.

**38/** @NOTimothyLottes

@DaveAirlie

The obvious elephant is an engine using only buffers for resource streaming and doing its own GPU-side decompression. This is practical NOW and portable too. But the lack of a bus master no-CPU direct storage transfer is a serious problem for throughput.

**39/** @NOTimothyLottes

@DaveAirlie

See raw texture streaming (even with lossless compression) is way less interesting now given modern massive data tech direction, u want substantially better lossy compression simply to fit in launch constraints. So really, buffers are the way to go anyway :)

## Related

- Spine: [[archive/threads/NOTimothyLottes/2023-06-20-how-about-a-mega-thread-on-the-mechanics-of-cpu]]
