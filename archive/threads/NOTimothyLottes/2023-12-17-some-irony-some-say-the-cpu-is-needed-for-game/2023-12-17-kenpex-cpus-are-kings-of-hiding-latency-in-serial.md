---
title: "@NOTimothyLottes CPUs are kings of hiding latency in serial workloads."
type: archive
source: twitter
source_url: "https://x.com/kenpex/status/1736451627148845441"
author: "c0de517e/AngeloPesce"
handle: kenpex
post_id: "1736451627148845441"
date: 2023-12-17
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes CPUs are kings of hiding latency in serial workloads."
in_reply_to: ""
parent_post_id: "1736360606612038098"
---

## Source

- URL: https://x.com/kenpex/status/1736451627148845441
- Author: c0de517e/AngeloPesce (@kenpex)
- Posted: 2023-12-17 18:21:44

## Branch

**1/** **@kenpex** ^1736451627148845441

**@NOTimothyLottes**

CPUs are kings of hiding latency in serial workloads. GPUs hide latency only when dealing w/massively parallel workloads, with much more items than cores!

**2/** **@NOTimothyLottes** ^1736476434191782262

**@kenpex**

Remember, a GPU doesn't have to do only uniform workloads, it is still possible to hide serial work inside a sea of parallel work.

**3/** **@kenpex** ^1736484359082033158

**@NOTimothyLottes**

You're suggesting, if I get it, to hide some serial/logic work in tiny async dispatches. That would work and not too horribly inefficient, but are you then getting really bad wallclock perf? Remember that as a rule of thumb, the serial part of a game is ~= the GPU frametime.

**4/** **@kenpex** ^1736484904307937546

**@NOTimothyLottes**

It is true that one could structure a game to be much more parallel than the average game is, thus reducing the serial logic to not much more than the coordination of a bunch of parallel for, but even with a lot of effort you'll not be near the amount of parallelism of a GPU

**5/** **@kenpex** ^1736485762349387942

**@NOTimothyLottes**

That's just because of the nature of work and work expansion. You have what, 100, 1000 entities as part of gameplay? And most do a bunch of ad-hoc, brancy work, with interdeps etc. On a GPU you have say 10k draws that spawn 10mil vtx/pixel work that is mostly uniform.

**6/** **@AgileJebrim** ^1736487589618520265

You clearly don’t know how to leverage batching if you’re doing 10k draws lol.

I’m able to handle complex behaviors for hundreds of thousands of entities just fine on a GPU. You can do a ton of work in a single dispatch and only really need multiple if you need the synchronization beyond what you can achieve with a thread group.

Remember Amdahl’s Law. Your performance will be constrained by the workload you fail to parallelize.

**7/** **@SebAaltonen** ^1736506369245589658

**@AgileJebrim** **@kenpex** **@NOTimothyLottes**

You can batch, we can already push 10k actual draw calls at 60 fps on 99$ Android phones. Close to 1 million draw calls are doable at 60 fps on Steam Deck (Vulkan). 10k draws is nothing today if your CPU code is fast enough. Changing the PSO 100k times/frame at 60 is fine too.

**8/** **@kenpex** ^1736511576382099798

**@SebAaltonen** **@AgileJebrim** **@NOTimothyLottes**

Sure, but that isn't the point.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2023-12-17-some-irony-some-say-the-cpu-is-needed-for-game]]
