---
title: "@rfleury Shouldn’t single-core array summation be faster than multi-core, since summing is bottlenecked not by computation but memory fetching?"
type: archive
source: twitter
source_url: "https://x.com/Nlitened/status/1976588924287074522"
author: "Timur Latypoff"
handle: Nlitened
post_id: "1976588924287074522"
date: 2025-10-10
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury Shouldn’t single-core array summation be faster than multi-core, since summing is bottlenecked not by computation but memory fetching?"
in_reply_to: ""
parent_post_id: "1976458516325073141"
---

## Source

- URL: https://x.com/Nlitened/status/1976588924287074522
- Author: Timur Latypoff (@Nlitened)
- Posted: 2025-10-10 10:01:37

## Branch

**1/** **@Nlitened** ^1976588924287074522

**@rfleury**

Shouldn’t single-core array summation be faster than multi-core, since summing is bottlenecked not by computation but memory fetching?

If so, then it’s a terrible example teaching how to overcomplicate a solution to gain nothing but bugs.

**2/** **@rfleury** ^1976608527599714352

No. A subscription to Computer Enhance will clear up your misunderstanding. Casey covers a similar summation loop in the introduction of the series.

http://computerenhance.com

But in any case, your reply seems to completely miss the point of the post? The post is about architecture, and simply structuring code to take advantage of serial independence. The same mechanisms can apply to a variety of other problems. I picked a summation loop because it’s very trivial, so I could introduce it quickly and focus on the surrounding architecture.

**3/** **@Nlitened** ^1976616473784189337

Thank you for the recommendation, I will check it out. I am very interested in filling my knowledge gap on how multithreading achieves faster summation.

I am sorry for the tone — I’ve noticed you being dismissive of other commenters in replies, so I kinda got fired up a little. I shouldn’t have, it’s my fault.

I think I understand the general idea of this thread, it’s an important concept for beginners. Though it breeds Python coders littering codebase with multithreaded summation (no-GIL Python here we go) instead of using numpy — because in my opinion the most important part of multithreading is benchmarking the tradeoffs, and I think no tradeoffs were being discussed here.

**4/** **@Nlitened** ^1976621396739391959

**@rfleury**

Looks like I was wrong, a single CPU core, although much faster, cannot saturate DRAM with fetch requests for architectural reason, so splitting into two-three cores would help with getting the last theoretically possible 30—40% speedup. Good to know!

## Related

- Spine: [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default]]
