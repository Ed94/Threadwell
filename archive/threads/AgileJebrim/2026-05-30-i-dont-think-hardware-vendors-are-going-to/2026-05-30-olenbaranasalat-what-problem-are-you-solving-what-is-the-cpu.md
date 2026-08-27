---
title: "What problem are you solving? What is the CPU lacking, and what does the GPU offer when the OS is ported to it? And I’m curious to know how you deal with stalls."
type: archive
source: twitter
source_url: "https://x.com/olenbaranasalat/status/2060552308052615363"
author: "Гала Перидоловна 🇳🇵"
handle: olenbaranasalat
post_id: "2060552308052615363"
date: 2026-05-30
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "What problem are you solving? What is the CPU lacking, and what does the GPU offer when the OS is ported to it? And I’m curious to know how you deal with stalls."
in_reply_to: ""
parent_post_id: "2060513369065754969"
---

## Source

- URL: https://x.com/olenbaranasalat/status/2060552308052615363
- Author: Гала Перидоловна 🇳🇵 (@olenbaranasalat)
- Posted: 2026-05-30 02:42:08

## Branch

**1/** **@olenbaranasalat** ^2060552308052615363

What problem are you solving? What is the CPU lacking, and what does the GPU offer when the OS is ported to it? And I’m curious to know how you deal with stalls. Have you written your own branch predictor and are you manually inserting something into each Warp? I’m also curious to know how you handle threads. Do all threads run sequentially on each Warp?

**2/** **@AgileJebrim** ^2060557227581112684

“What problem are you solving?”

Hard real-time guarantees are too difficult and expensive to verify in the safety-critical market and usually requires leveraging expensive and dated custom hardware and software toolchains. This is doubly so when needing high performance requirements for stuff like computer vision, sensor fusion, autonomous vehicles, enhanced flight vision systems, HWIL sims, robotics, etc.

We’re looking to make it cheap to produce such high performance safety-critical systems on existing affordable COTS hardware.

“What is the CPU lacking, and what does the GPU offer when the OS is ported to it?”

CPU lacks a programmer-managed cache. GPUs have scratchpad memory. They also cannot be arbitrarily interrupted. We don’t pursue a preemption-based design but instead actually target having EVERYTHING on the GPU meet the real-time deadline, thereby avoiding the problem entirely. This is achieved through a custom compiler we’re building that guarantees isochronous (constant time) execution, minimizing jitter. This also works very well with SIMD.

Your later questions have too many false premises. We don’t have a branch predictor because nothing ever branches or diverges to begin with. All hardware runs the same code, syncs, then runs the next bit of code. No warp specialization is planned at this time.

**3/** **@AgileJebrim** ^2060557537863139453

**@olenbaranasalat**

The other problem we’re solving is data, not just code. Changing the data should not require recertifying anything. It should just work with the same execution times as any other data input.

**4/** **@olenbaranasalat** ^2060719310603972993

How do you prove constant-time execution in the presence of global memory, barriers, bank conflicts, DRAM arbitration, TLB/IOMMU behavior? Is your model a general RTOS, or more like a statically scheduled synchronous dataflow runtime? Is your GPU-native RTOS mainly meant for deterministic high-performance perception/data processing, rather than replacing the cheaper and well-understood MCU/FPGA layer for physical hard real-time control?

**5/** **@AgileJebrim** ^2060764703186460992

Great questions!

We do not allow for random access memory. Everything from global memory is linearly streamed in. Random access lookups are only allowed to occur within shared memory on 64KB tiles or shuffles within a warp. To avoid bank conflicts in shared memory, we utilize warp-uniform techniques.

Barriers are a potential source of slight jitter fluctuations, especially when globally syncing, but they are data-independent, few in number, and well-bounded. It helps a lot that all threads have equal execution times.

We have techniques to avoid getting bottlenecked by CPU-side interference. It’s important to not directly share resources with them at arbitrary points. We treat the CPU as unreliable low priority background threads to be safe.

You can get both experiences. The former is supported via a scripting language where we interpret bytecode dynamically at runtime with a fixed amount of cycles per task, sacrificing throughput to achieve arbitrary code execution. The latter is precompiled in with a static schedule.

It’ll all still be relatively static compared to a typical RTOS simply because RTOSes are not actually guaranteeing all threads within them are high criticality. They’re assuming some are low priority; we don’t have that problem. We dedicate 100% of all GPU hardware to a single task before moving on to the next. No preemption.

Both. Competing against FPGAs is one of my biggest goals with this. We can achieve their isochronous behavior but with much higher bandwidth, all on cheap COTS hardware that people already have.

I’m going quite broadly with the applications I have in mind of supporting. You could do sensor fusion, computer vision, and autonomous driving with this, sure, but you could also use it to power a metaverse or social media app like X. Reduce your costs by replacing distributed microservices with SIMT lanes.

**6/** **@olenbaranasalat** ^2060772978128814271

**@AgileJebrim**

Not gonna lie, I’m a bit jealous — this sounds like an insanely fun systems problem to work on.

**7/** **@AgileJebrim** ^2060774071479013674

**@olenbaranasalat**

What’s your rate? We can dm.

**8/** **@olenbaranasalat** ^2060781078843957541

Thank you, but I only interview candidates for roles related to GPUs, so I’ve had to familiarise myself with how GPUs work. My main specialism is I/O virtualisation. I have little production experience writing code for GPUs - at most, I’ve run tests to assess inference performance in virtual machines. I’m unlikely to be the right fit for you :)

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-30-i-dont-think-hardware-vendors-are-going-to]]
