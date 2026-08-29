---
title: "@AgileJebrim They need to know how GPU shaders are organized to even answer this."
type: archive
source: twitter
source_url: "https://x.com/stikves/status/2058434571608490047"
author: "sukru tikves"
handle: stikves
post_id: "2058434571608490047"
date: 2026-05-24
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim They need to know how GPU shaders are organized to even answer this."
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/stikves/status/2058434571608490047
- Author: sukru tikves (@stikves)
- Posted: 2026-05-24 06:27:00

## Branch

**1/** **@stikves** ^2058434571608490047

**@AgileJebrim**

They need to know how GPU shaders are organized to even answer this.

But I hope nobody came with "I would write a simple for loop..."

**2/** **@AgileJebrim** ^2058534593200894022

**@stikves**

Actually the correct answer does involve one or more for loops in the answer.

**3/** **@stikves** ^2058680013483049048

**@AgileJebrim**

(Going down the rabbit hole)

Yes, it would of course. 
Some context goes out in short replies here.

**4/** **@AgileJebrim** ^2058680437787041994

**@stikves**

You can comment longer. :P

**5/** **@stikves** ^2058682097506931028

**@AgileJebrim**

I could... 

Yet, at doing those at midnight usually backfires.
"What was a thread block again? Or was it a..."

**6/** **@AgileJebrim** ^2058684292662735191

**@stikves**

Here’s your hardware target. You have an arbitrary number of these SMs and a L2 cache and global memory available for cross communication between them. Describe how you would do it in relation to the hardware described here.

![](https://pbs.twimg.com/media/HJHqc7dWkAEra7E?format=jpg&name=orig)

**7/** **@stikves** ^2058687794470592548

**@AgileJebrim**

Since they work independently, you start from the nearest (register file) and move up (shared mem) to intra SM (L2)

Though to be fair, for standard operations I would look this up

Why?

There is usually one corner case the prior art discovered but not obvious at first sight

**8/** **@stikves** ^2058688045059301875

**@AgileJebrim**

(The standard solution to binary search for example had a off by one bug in the books for over a decade.

Can I write binary search from the tip of my head?
Of course, did 100s of times

Will I actually do it for production?
No)

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
