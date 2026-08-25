---
title: "@AgileJebrim @SebAaltonen @munohikari (3.) If you had multiple line stores collecting on a given line with ECC, you'd have the same bottleneck as fire-and-forget atomics."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1869436525869724013"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1869436525869724013"
date: 2024-12-18
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim @SebAaltonen @munohikari (3.) If you had multiple line stores collecting on a given line with ECC, you'd have the same bottleneck as fire-and-forget atomics."
in_reply_to: ""
parent_post_id: "1869436199884222515"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1869436525869724013
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-12-18 17:36:14

## Branch

**1/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari (3.) If you had multiple line stores collecting on a given line with ECC, you'd have the same bottleneck as fire-and-forget atomics. A throughput of one line modification per clock.

**2/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari (4.) Note the prior assumes a read hit! 

So at the point you get anti-atomic, you are also anti-store and anti-ECC, and anti-etc. It's the same pipelines with the same variability due to on-chip networking, different clock domain crossing, etc.

**3/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari (5.) Good GPUs have multiple ALUs doing the atomic by the last level cache. So it scales very well as a function of line collisions. Meaning if all lanes access separate addresses on a cacheline, those go in parallel.

**4/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari (6.) Atomics and regular stores have the same memory controller base-camping behavior. If all SIMDs store to addresses that hash to the same last level cache partition, they will drop efficiency just like doing all atomics to the same address.

**5/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari (7.) Anyway, while CPU atomics are serious design fail, GPU atomics on good GPUs are your best friend. They are actually a fantastic tool for getting more regular performance in many parallel algorithms.

**6/** @SebAaltonen

@NOTimothyLottes @AgileJebrim @munohikari Indeed. Many CPU programmers have the wrong belief that GPU atomics are slow and unusable. They are fantastic. Bump allocator is your best friend on CPU side. On GPU you do atomic add to implement a bump allocator. As simple as that. It's super fast.

**7/** @AgileJebrim

@SebAaltonen @NOTimothyLottes @munohikari I know NVIDIA did a really good atomicAdd, especially if you don’t use the result of the atomicAdd(). If you use it, then it forces it down a significantly slower path. But it’s all implementation-specific and different vendors will do different things yes?

**8/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari Atomics come in two forms
(1.) fire-and-forget (aka you don't use the return) - the compiler will flag it for no-return, so it behaves like a store
(2.) read the return - it behaves like a {store, and read} simultaneously with layout "coherent"

**9/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari Good GPUs have address coalescing on writes and atomics. So a wave wide store is reduced to a cost that scales with the number of total cachelines all waves touch, with byte-write-mask so there is no read-modify-write

**10/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari ... atomics have the same but if any wave lane's addresses collide it will bump those to another request (for the same cacheline). Possible that some HW implements a HW reduction for collisions of some kinds of atomics locally before the requests go out, but don't assume that

**11/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari ... it's more likely that some compilers try to fix stupid behavior by doing a wave-reduction in software, and that causes hell for those of us who already write good code

**12/** @AgileJebrim

@NOTimothyLottes @SebAaltonen @munohikari Thoughts on atomic compare exchange? I use similar functionality on CPUs to globally synchronize threads and I figured I’d give it a shot attempting to do that on GPUs.

**13/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari Compare and exchange since it takes 2 values, it could have half the peak rate through on-chip network. Personally I have always used algorithms that do better things without the cmpswap atomic. You always can get the return (value pre-atomic), so cmpswap utility is less

**14/** @AgileJebrim

@NOTimothyLottes @SebAaltonen My CPU sync mechanism works by stalling each thread until it reaches a multiple of the total number of threads to be synced, only incrementing an integer (swapping) when it reaches its specific thread index.

**15/** @NOTimothyLottes

@AgileJebrim @SebAaltonen I assume you are using a futex then on Linux to block? But the GPU doesn't have such a thing exposed in software. Instead you'd be effectively polling using serial global memory atomic latency as your rate limiter and 'blocking'

**16/** @NOTimothyLottes

@AgileJebrim @SebAaltonen Serializing workgroups on the GPU in this way has a very high latency granularity. There is also the issue of preemption on PCs, there is no guarantee of forward progress due to no guarantee all workgroups get restored

**17/** @NOTimothyLottes

@AgileJebrim @SebAaltonen So you can deadlock post preemption if the workgroup that needs to do the atomic to unblock those spinning cannot get back on the machine

**18/** @NOTimothyLottes

@AgileJebrim @SebAaltonen Now, the important part, there is one compromise rule that has the highest chance of being possible, that is an ask that if there is a partial restore, that it restores the oldest launched workgroups first ...

**19/** @NOTimothyLottes

@AgileJebrim @SebAaltonen And with that you can have some forward progress if an algorithm only has dependencies on workgroups launched before it (like lower kernel global workgroup index), food for thought for algorithm design

**20/** @NOTimothyLottes

@AgileJebrim @SebAaltonen on the CPU side, you'd futex block to get the thread off being scheduled so the dependent one could get on the machine to avoid deadlock, it isn't efficient by any means but works, the GPU's exposed only voluntary method to get off the machine is to exit the workgroup ...

**21/** @NOTimothyLottes

@AgileJebrim @SebAaltonen So if you uber-task, meaning just keep launching the same dispatch, and the workgroup finds what it needs to do (instead of working off kernel global index), then you can workaround preemption that way too ...

**22/** @NOTimothyLottes

@AgileJebrim @SebAaltonen Blocking becomes just workgroup exit. And the next workgroup gets lower schedule priority than existing active workgroups which helps solve of the scheduling issues

**23/** @AgileJebrim

@NOTimothyLottes @SebAaltonen I’m not using a Linux futex. Could you look over my code here?

**24/** @simplex_fx

@AgileJebrim @NOTimothyLottes @SebAaltonen Hey Jeb, have you considered hitting the funny L shaped button on the right of your keyboard more frequently? 😅

**25/** @AgileJebrim

@simplex_fx @NOTimothyLottes @SebAaltonen Enter? Nah

**26/** @simplex_fx

@AgileJebrim @NOTimothyLottes @SebAaltonen

![](https://pbs.twimg.com/media/GfG1cCJW8AAXcDg?format=jpg&name=orig)

**27/** @AgileJebrim

@simplex_fx @NOTimothyLottes @SebAaltonen If I don’t have to scroll right…

**28/** @simplex_fx

@AgileJebrim @NOTimothyLottes @SebAaltonen Dude, stop with that WQHD bullshit, buy a proper tv and limit yourself to 80-120

**29/** @AgileJebrim

@simplex_fx @NOTimothyLottes @SebAaltonen Nty. The hell do I need a tv for? I have several monitors.

**30/** @simplex_fx

@AgileJebrim @NOTimothyLottes @SebAaltonen How big?

**31/** @AgileJebrim

@simplex_fx @NOTimothyLottes @SebAaltonen Big enough to maximize a window on each.

**32/** @simplex_fx

@AgileJebrim @NOTimothyLottes @SebAaltonen If you go too wide, you will just kill your neck on the long run

**33/** @AgileJebrim

@simplex_fx @NOTimothyLottes @SebAaltonen I have 4 monitors

**34/** @simplex_fx

@AgileJebrim @NOTimothyLottes @SebAaltonen How big?

**35/** @NOTimothyLottes

@simplex_fx @AgileJebrim @SebAaltonen Ideally one of these

![](https://pbs.twimg.com/media/GfHntpaWYAAGnOk?format=png&name=orig)

**36/** @AgileJebrim

@NOTimothyLottes @simplex_fx @SebAaltonen Not big enough. Evans & Sutherland still makes planetariums. We have smaller scale 360 degree domes. I think they’re about 14ft high.

**37/** @SebAaltonen

@AgileJebrim @NOTimothyLottes Same is true for everything. All memory loads on GPUs are highly vendor specific. On GTX 1080 (Pascal) your memory load goes through sampler, which is around 85 cycles of latency. While on Turing your raw load is only 28 cycles of latency (CUDA benchmarks).

**38/** @AgileJebrim

@SebAaltonen @NOTimothyLottes For sure, but my focus is more on how deterministic and predictable these are. I’ll take 85 if it’s always 85 over something that might vary unpredictably between 28 and 100.

**39/** @SebAaltonen

@AgileJebrim @NOTimothyLottes Nvidia has big L1$, so they are more predictable. Texture samplers are shared with all waves running on the same compute unit. They are not really predictable. You wait until the unit is ready. There's quite a lot of fluctuation. That's why you have 8x-10x hyperthreading per CU.

**40/** @SebAaltonen

@AgileJebrim @NOTimothyLottes The idea is to keep the SIMD running all the time. Wave execution time variance hasn't been a big optimization goal. There's always more work coming, so it's not a problem if some wave takes 10x time to execute compared to others.

**41/** @SebAaltonen

@AgileJebrim @NOTimothyLottes Basically if the SIMD is executing instructions all the time, then your workload runs at predictable amount of instructions per cycle. The problem is barriers. You wait for longest wave to finish. You can't to batch barriers to avoid turning latency into real lost SIMD cycles.

**42/** @AgileJebrim

@SebAaltonen @NOTimothyLottes If they all take the same amount of time then there shouldn’t be much idling of hardware for waiting on the longest wave.

**43/** @SebAaltonen

@AgileJebrim @NOTimothyLottes That's true. But they don't take the same amount of time due to caches. That's where the 10x hyper-threading kicks in. As long as the SIMD is fed all the time, there's no visible issue with fluctuating wave lengths. Barriers make that visible. Minimal amount of barriers = good.

**44/** @AgileJebrim

@NOTimothyLottes @SebAaltonen @munohikari Would you implement a prefix sum compaction algorithm using atomicAdd?

**45/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari Standard optimizations apply, like doing wave-reductions first.

**46/** @AgileJebrim

@NOTimothyLottes @SebAaltonen @munohikari Okay so you don’t just blanket throw an atomicAdd on it then.

**47/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari No. For things like scanning a 1-bit value, it's a wave masked bit count op in software, followed by predicating the atomic to just lane 0 of the wave. For scanning uint32s it's a log2 wave reduction, then predicating the add to lane 0. And so on

## Related

- Spine: [[archive/threads/AgileJebrim/2024-12-18-you-left-out-the-bit-where-i-also-said-no]]
