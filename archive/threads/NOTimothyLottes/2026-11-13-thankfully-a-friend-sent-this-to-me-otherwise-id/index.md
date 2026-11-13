---
title: "Thankfully a friend sent this to me otherwise I'd have missed it."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2121244702649532667"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2121244702649532667"
date: 2026-11-13
archived: 2026-11-13
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Thankfully a friend sent this to me otherwise I'd have missed it."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2121244702649532667
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-11-13 14:12:02

## Thread

**1/** **@NOTimothyLottes** ^2121244702649532667

Thankfully a friend sent this to me otherwise I'd have missed it. Apparently I've angered one of the CUDA GODs because I'm "dense with misrepresentations". Lets fix this with a deep dive into the HW that everyone interested in GPU programming can learn from!

![](https://pbs.twimg.com/media/HXAsbzxW0AEcNDb?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2026-11-13-thankfully-a-friend-sent-this-to-me-otherwise-id/2026-11-13-damianGray-you-could-have-been-wrong-but-the-arrogance-of]]

**2/** **@NOTimothyLottes** ^2121245244662411629

CDP1 exposes nested parallelism. Parent kernel can launch a child kernel on the GPU without the CPU. When execution doesn't return to the parent that is "fire-and-forget". Otherwise execution can return to the parent kernel when the child(ren) finish.

![](https://pbs.twimg.com/media/HXAs_vGWQAEIzr8?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2026-11-13-thankfully-a-friend-sent-this-to-me-otherwise-id/2026-11-13-AmosAnon-was-this-related-to-iepm-i-dont-remember-cdp-but]]

**3/** **@NOTimothyLottes** ^2121245946956632392

This system implies a new HW feature at the time,
ability to kick off a kernel dispatch from inside the shader. Now lets discuss how one might implement CDP on the hardware. This will be for nested (not fire-and-forget) parallelism.

**4/** **@NOTimothyLottes** ^2121246595542921485

This first implementation is covered in the attached image. This leverages wave level global atomics to do work completion tracking. We can then dive into the latency and issues with the associated implementation.

![](https://pbs.twimg.com/media/HXAuL2_WAAAdwyv?format=png&name=orig)

**5/** **@NOTimothyLottes** ^2121246934975328502

Mem barrier (2.) requires round trip from SIMD to L2 and back. With ECC on for DRAM, there is no byte write mask. This is important today because at high clocks,
ECC needs to be on to avoid errors. So if one does (0.) wrong, you'd get a read-line-modify.

![](https://pbs.twimg.com/media/HXAumr5WoAEHb8x?format=png&name=orig)

**6/** **@NOTimothyLottes** ^2121247311787360760

So if one does (0.) wrong, you'd get a read-line-modify (ECC enabled). Meaning you'd have a DRAM round trip that (2.) could wait on. If you write the full cacheline in (0.) good HW would be able to avoid the read.

![](https://pbs.twimg.com/media/HXAu5osXYAAmD3L?format=png&name=orig)

**7/** **@NOTimothyLottes** ^2121247827162493103

If the kernel execution involves a branch before child kernel launch (3.), there is a possibility that instruction pre-fetch didn't capture it. Meaning round trip through DRAM if the compiler people are stupid. If HW supports  more advanced I$ prefetching, there are gains here.

![](https://pbs.twimg.com/media/HXAvQ-zWwAAO_3a?format=png&name=orig)

**8/** **@NOTimothyLottes** ^2121248098286481894

Note in (3.) depending on HW design, you likely have a hidden SIMD to L2 round trip. Ie write a record of the kernel launch commands into a queue in memory. Then a memory barrier to guarantee that record is written.
Followed by inserting (store) a pointer to the record in a queue

![](https://pbs.twimg.com/media/HXAvt9lXAAAfSEP?format=png&name=orig)

**9/** **@NOTimothyLottes** ^2121248472309407775

... Note if the API hides this (kernel launch record writes), the programmer couldn't easily factor the hidden round trip out. For example to do it with another memory barrier that already exists in the shader! Typically compilers cannot because of branches/etc.

![](https://pbs.twimg.com/media/HXAv_cDWMAAubSB?format=png&name=orig)

**10/** **@NOTimothyLottes** ^2121248962023735367

If parent kernel fills the machine, must wait until (4.) save state is kicked off (stores all queued) before kernels can exit, leaving room for child kernel(s) (6.) to launch. While this is mostly an NV conversation, I'm going to add in some important AMD details too next.

![](https://pbs.twimg.com/media/HXAwS_6XgAE382p?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2026-11-13-thankfully-a-friend-sent-this-to-me-otherwise-id/2026-11-13-Colonthreee-how-about-persistent-threads]]

**11/** **@NOTimothyLottes** ^2121249487515771121

On old AMD HW, stores need to complete (ACK) before kernel can exit. Early AMD HW, there is a full SIMD to L2 and back delay here. If register state won't fit in L2, then there are DRAM round trips involved. Register saves could cause back-pressure in memory for dependent child.

![](https://pbs.twimg.com/media/HXAwv5fXIAAAoCK?format=png&name=orig)

**12/** **@NOTimothyLottes** ^2121249874670956764

At (6.) you have initial DRAM round trip to warm the I$ pathway. Meaning child kernels start slow. Clearly if the GPU IHV has added better ways to warm I$ and uses that, this could be mitigated assuming I$ wasn't already pushed to it's limit on parent kernel execution.

![](https://pbs.twimg.com/media/HXAxOS9WwAE2oWT?format=png&name=orig)

**13/** **@NOTimothyLottes** ^2121250099317915771

The atomic in (8.) require a round trip from CU to L2 and back. This is assuming C is still in L2 cache.
If C got evicted you'd have a full DRAM trip in there too for the first miss. But that would be pipelined if the kernel was big. So this mostly takes effect for tiny child.

![](https://pbs.twimg.com/media/HXAxl_HXYAEscfq?format=png&name=orig)

**14/** **@NOTimothyLottes** ^2121250473709637682

The problem with (8.) is you have a lot of atomics.
And they are base camping at one L2 (not distributed across the machine)! So it can cause asymmetric loading of L2 and the internal on-chip network.

![](https://pbs.twimg.com/media/HXAxykcWYAAYzNE?format=png&name=orig)

**15/** **@NOTimothyLottes** ^2121250678572200403

Then you have the latency of dependent launch of (9.)
Which includes the parent kernel running slow due to DRAM round trip for I$ warming.

![](https://pbs.twimg.com/media/HXAyIIpWUAAeTmF?format=png&name=orig)

**16/** **@NOTimothyLottes** ^2121251028146454644

Now take all that and realize that nested parallelism allows for multiple dependent child kernel launches before the parent kernel can complete. Meaning child kernels might have to check multiple counters, before the parents can be restarted. Meaning branch to scheduling=I$ miss

![](https://pbs.twimg.com/media/HXAyRGOXwAAsuG1?format=png&name=orig)

**17/** **@NOTimothyLottes** ^2121251159361097820

Also this can be nested, so the children themselves might be parents, greatly amplifying the total latency!!!!!

![](https://pbs.twimg.com/media/HXAym5YWgAAJt5N?format=png&name=orig)

**18/** **@NOTimothyLottes** ^2121251701831188905

So if you read between the lines, when high level OOP folks engineer workgraph garbage (CDP) the while process is loaded with land mines of latency and efficiency issues.

![](https://pbs.twimg.com/media/HXAyw4JWUAA2nN7?format=png&name=orig)

**19/** **@NOTimothyLottes** ^2121252779599810735

Originally at NVIDIA I was hired into Daniel Wexler's group, and at the time I naturally complained that the intended design was a garbage fire. And I offered a workaround to try to mitigate some of the issues that could be solved via creative reuse of the HW.

![](https://pbs.twimg.com/media/HXA0IE_WUAET-d1?format=jpg&name=orig)

**20/** **@NOTimothyLottes** ^2121253265018949886

GPU HW already has a mechanism to track when kernels finish. Traditionally used for things like writing timestamps when a dispatch is finished. So we don't actually need to do atomics at the end of the child kernels. Instead we could do a separate scheduling kernel.

Branches: [[archive/threads/NOTimothyLottes/2026-11-13-thankfully-a-friend-sent-this-to-me-otherwise-id/2026-11-13-AgileJebrim-did-this-still-synchronize-all-threads-before]]

**21/** **@NOTimothyLottes** ^2121253799096656041

Now I paid a high price for fighting with the NV staff at the time and pointing out what would fail and how to fix it. Dan's group got disbanded. I got relocated to devtech, and was told I'm on probation for "poor work performance" - either show benefit or get fired!

**22/** **@NOTimothyLottes** ^2121254407128170757

After that I built FXAA in my free time at home, and brought it into work when it was working well, then released it inside NVIDIA. This wasn't a project that I was assigned to work on at the time.

**23/** **@NOTimothyLottes** ^2121256496659087378

I think it's a funny story. And many other humans in the giant corporate machine probably either had to deal with an asshole like myself, or had similar stories of the negative effects of fighting against established seniors.

Branches: [[archive/threads/NOTimothyLottes/2026-11-13-thankfully-a-friend-sent-this-to-me-otherwise-id/2026-11-13-Colonthreee-appeal-to-authority-is-a-logical-fallacy-it]]

**24/** **@NOTimothyLottes** ^2121259314627195297

Some of those who got this far are probably realizing now the parallels here - CDP, on-GPU workgraphs, Ray Tracing, they all have horrible designs - all designed to hook the high level thinkers - make the worst way of doing something faster, but never teaching the good stuff.

**25/** **@NOTimothyLottes** ^2121260463732453668

My suggestion is always the same, profile, look at your sources of latency and memory bandwidth, and re-work your thinking from first principles from the bottom up instead. Minimize everything, what doesn't need to be there, remove that.
