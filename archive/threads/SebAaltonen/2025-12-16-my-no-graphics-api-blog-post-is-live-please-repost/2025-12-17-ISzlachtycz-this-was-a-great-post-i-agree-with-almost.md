---
title: "@SebAaltonen This was a great post! I agree with almost everything you wrote."
type: archive
source: twitter
source_url: "https://x.com/ISzlachtycz/status/2001201742650716164"
author: "Ihor_Szlachtycz 🇺🇦"
handle: ISzlachtycz
post_id: "2001201742650716164"
date: 2025-12-17
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen This was a great post! I agree with almost everything you wrote."
in_reply_to: ""
parent_post_id: "2001000839574643138"
---

## Source

- URL: https://x.com/ISzlachtycz/status/2001201742650716164
- Author: Ihor_Szlachtycz 🇺🇦 (@ISzlachtycz)
- Posted: 2025-12-17 08:04:10

## Branch

**1/** **@ISzlachtycz** ^2001201742650716164

**@SebAaltonen**

This was a great post! I agree with almost everything you wrote. One thing that really frustrates me about the industry is how everyone has to write their own basic debugging features, most of which suck. 1/n

**2/** **@ISzlachtycz** ^2001202055973597425

**@SebAaltonen**

As a starter, DX13 needs shader printfs. Ideally, you could choose a target memory address to write to, or use an exposed default backing buffer created by the driver that persists even after device reset. 2/n

**3/** **@ISzlachtycz** ^2001202284735221949

**@SebAaltonen**

I believe that in DX12 you can allocate pages such that writing to a GPU buffer automatically writes to a file on disk. This is essential for any real logging framework. Breadcrumbs in my mind arent enough 3/n

**4/** **@ISzlachtycz** ^2001202381699027019

**@SebAaltonen**

It would also be nice to finally have some level of debugger support, even if it requires having a second gpu to avoid TDR issues. This ties in with forward progress guarantees, but ill start with debugging. For me, there are 3 classes of gpu problems we want to debug: 4/n

**5/** **@ISzlachtycz** ^2001202495004061968

**@SebAaltonen**

1) Single thread debugging: we mainly care about debugging the logic of a single thread thats not interacting in a direct way with other threads. This i think covers 80% of debugging needs. 5/n

**6/** **@ISzlachtycz** ^2001202670372004027

**@SebAaltonen**

2) thread group level sync problems: this is for problems were your shader writes to lds or does some wave ops. In this case, you need to simulate or run a whole thread group and you want to provide the user with its state to understand how its syncing/executing. 6/n

**7/** **@ISzlachtycz** ^2001202978527531260

**@SebAaltonen**

3) Gpu wide sync problems: this is for problems where youre using global atomics to sync across all or many thread groups. In this case, you need your entire workload frozen, in order to debug correctly. This can cause nasty TDR/freezing issues but is not very common a problem7/n

**8/** **@ISzlachtycz** ^2001203120706081231

**@SebAaltonen**

For 1 and 2, you can pin those workloads onto the gpu, and as long as you have WGP/CU level forward progress guarantees, this wont hang your system and other processes can keep executing and finishing work.  8/n

**9/** **@ISzlachtycz** ^2001203192948826407

**@SebAaltonen**

For 3, you would need something like on CPUs where waves/warps can be saved to memory, and restored later when you step or F5. I dont think anyone supports that now, so youd probably need a second gpu for that kind of workload. 9/n

**10/** **@ISzlachtycz** ^2001203696642740295

**@SebAaltonen**

Right now, writing a spin lock is undefined behavior in hlsl. With forward progress, thats not a problem, and you can even add a intrinsic to sleep the wave in a lock, to let other waves do work. 10/n

**11/** **@ISzlachtycz** ^2001203767539081561

**@SebAaltonen**

With proper debugger support, you can traps for asserts that arent weird hacks but just part of the api and detected correctly by debuggers. 11/n

**12/** **@ISzlachtycz** ^2001203919821680757

**@SebAaltonen**

For 3), if we have proper logging in the apis by default (or atleast supported on a lang level), that can already give you traces to debug if youre on a single gpu setup, which at least gives you some feedback. 12/n

**13/** **@ISzlachtycz** ^2001204089200210407

**@SebAaltonen**

Its just crucial these buffers exist after the gpu TDRs in whatever way, so you dont lose all the data. End of rant 13/13. Again, great post, was a pleasent read :)

**14/** **@SebAaltonen** ^2001210417339654420

**@ISzlachtycz**

Yeah, debugging should indeed be improved. Hopefully somebody else has the time and energy to write a blog post about that topic. The shader framework also needs a big discussion.

## Related

- Spine: [[archive/threads/SebAaltonen/2025-12-16-my-no-graphics-api-blog-post-is-live-please-repost]]
