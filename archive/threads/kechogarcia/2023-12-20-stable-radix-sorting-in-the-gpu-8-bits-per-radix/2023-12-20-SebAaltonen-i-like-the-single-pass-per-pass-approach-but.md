---
title: "@kechogarcia I like the single pass (per pass) approach."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1737372016905204175"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1737372016905204175"
date: 2023-12-20
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - kechogarcia
description: "@kechogarcia I like the single pass (per pass) approach."
in_reply_to: ""
parent_post_id: "1737288039603269648"
---

## Source

- URL: https://x.com/SebAaltonen/status/1737372016905204175
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2023-12-20 07:19:02

## Branch

**1/** **@SebAaltonen** ^1737372016905204175

**@kechogarcia**

I like the single pass (per pass) approach. But unfortunately it's not doable using general API due to tight loops not having forward progress guarantees ("sufficiently fair scheduling"). Also doable on AMD consoles using ordered count instructions.

https://developer.download.nvidia.com/video/gputechconf/gtc/2020/presentations/s21572-a-faster-radix-sort-implementation.pdf

**2/** **@kechogarcia** ^1737456119511973917

**@SebAaltonen**

There's a very neat trick from AMD folk to sync groups. You do an interlockadd(1) to a dword in ram after group is done, and the last thread finished gets gets thread count. Have to use globalcoherent on the uavs you want to sync across. Haven't experimented w this but looks cool

**3/** **@SebAaltonen** ^1737463338509152338

**@kechogarcia**

Yes the last group gets the group count if you do that and it knows it's the last group, but other groups are dead already. They can't spin waiting until all other groups have finished.

**4/** **@kechogarcia** ^1737464423080427897

**@SebAaltonen**

Yeah spinning is fishy. In nanite culling they do sort of spin however, they just move to other work. Their persistant culling shader is basically polling a globalcoherent buffer to get more work from the intermediate nodes of the DAG🙈and hiding the spin with other work.

**5/** **@SebAaltonen** ^1737466890753069229

**@kechogarcia**

That only works if you never spin waiting for work. If work runs out and you still spin, then you can deadlock. It's possible that the same CU has the actual work producer and the consumer, and consumer wave spinning gets all the execution time in the SIMD. The other wave waits.

**6/** **@kechogarcia** ^1737480192749187544

**@SebAaltonen**

I think horizon guys, for vertex processing of vegetation, have a ring buffer in turn & don't spin, but wait on a label on the GPU. Something which can't be done on PC hlsl :(

**7/** **@NOTimothyLottes** ^1737485387637940347

**@kechogarcia** **@SebAaltonen**

Persistent waves on PC: {dispatch A, dispatch B} -> workgroups of A get on GPU before workgroups of B start. If both A and B run the same shader, if one needs a spinning wait in A, the wave could exit, then depend on relaunch in B to fix wave priorities to get forward progress...

**8/** **@NOTimothyLottes** ^1737486229631827979

**@kechogarcia** **@SebAaltonen**

... so N dispatches in theory provides ability to run N spinninging waits per wave ... the wave exit and relaunch priority shift would in theory avoid burning cost on the busy wait ... of course this all assumes the wait is at a stateless point in execution :)

**9/** **@SebAaltonen** ^1737542645059031420

**@NOTimothyLottes** **@kechogarcia**

Yes, but there's no API in DirectX or Vulkan for relaunching waves.

**10/** **@NOTimothyLottes** ^1737555411941958063

**@SebAaltonen** **@kechogarcia**

Either launch more workgroups than you need (or do extra dispatches). Either way though, this needs some dynamic adaption to avoid the overlaunch overhead.

## Related

- Spine: [[archive/threads/kechogarcia/2023-12-20-stable-radix-sorting-in-the-gpu-8-bits-per-radix]]
