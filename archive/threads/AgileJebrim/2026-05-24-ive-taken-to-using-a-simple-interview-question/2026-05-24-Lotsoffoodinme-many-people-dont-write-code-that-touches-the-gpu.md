---
title: "@AgileJebrim many people don't write code that touches the gpu"
type: archive
source: twitter
source_url: "https://x.com/Lotsoffoodinme/status/2058454499828904170"
author: "el jack"
handle: Lotsoffoodinme
post_id: "2058454499828904170"
date: 2026-05-24
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim many people don't write code that touches the gpu"
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/Lotsoffoodinme/status/2058454499828904170
- Author: el jack (@Lotsoffoodinme)
- Posted: 2026-05-24 07:46:11

## Branch

**1/** **@Lotsoffoodinme** ^2058454499828904170

**@AgileJebrim**

many people don't write code that touches the gpu

**2/** **@AgileJebrim** ^2058531033809580044

**@Lotsoffoodinme**

We’re changing that.

**3/** **@Lotsoffoodinme** ^2058534577136967750

**@AgileJebrim**

Out of interest, is it something drastically different to dividing it up into many slices and summing from there? I’m envisioning something like a map reduce

**4/** **@AgileJebrim** ^2058539551895834686

**@Lotsoffoodinme**

It’s in that direction but I need greater details.

**5/** **@Lotsoffoodinme** ^2058554249488064571

**@AgileJebrim**

As I don’t write code that targets the gpu I can’t. Is this a particularly complicated question? It seems to a complete lay person that it shouldn’t be too complicated.

**6/** **@AgileJebrim** ^2058554931980705979

**@Lotsoffoodinme**

How would you answer this for a multicore CPU?

**7/** **@Lotsoffoodinme** ^2058559658827382904

Im assuming it’s a big enough set of numbers that chunking it makes sense. Maybe it’s hand wavy, but I’m also going to assume it fits in a 64bit number.

Gameplan would be to chunk by core count, then have each core iterate over its slice. I rarely explicitly write vectorised code, but I’m reasonably confident I’d want more than one accumulator. By that I mean each iteration of the loop might do 4 additions at once and then increment by 32 or whatever the cpu supports.

At the end reduce the accumulators and then reduce the threads.

I hope that’s not a terrible answer.

**8/** **@AgileJebrim** ^2058560525810692312

**@Lotsoffoodinme**

You can scale a lot more than just 4-wide SIMD.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
