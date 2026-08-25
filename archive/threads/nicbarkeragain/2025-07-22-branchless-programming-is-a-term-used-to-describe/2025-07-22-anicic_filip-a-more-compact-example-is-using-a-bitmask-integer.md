---
title: "@nicbarkeragain A more compact example is using a bitmask integer."
type: archive
source: twitter
source_url: "https://x.com/anicic_filip/status/1947536063959839200"
author: "Filip Aničić"
handle: anicic_filip
post_id: "1947536063959839200"
date: 2025-07-22
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - nicbarkeragain
description: "@nicbarkeragain A more compact example is using a bitmask integer."
in_reply_to: ""
parent_post_id: "1947506500194472221"
---

## Source

- URL: https://x.com/anicic_filip/status/1947536063959839200
- Author: Filip Aničić (@anicic_filip)
- Posted: 2025-07-22 05:55:55

## Branch

**1/** **@anicic_filip** ^1947536063959839200

**@nicbarkeragain**

A more compact example is using a bitmask integer. It's a good way to learn bitshifting and you don't need to update the look up table when you update the enum

![](https://pbs.twimg.com/media/GwcJPSnWgAM_y5U?format=png&name=orig)

**2/** **@nicbarkeragain** ^1947536361520828795

**@anicic_filip**

Agreed, I made the assumption that people who haven’t heard of branchless before might struggle a little with the more compact approaches 🙂

**3/** **@anicic_filip** ^1947538090689528008

**@nicbarkeragain**

Look up table is a good introductory example. 
The logic of CPUs doing multiplications faster than boolean comparisons is bonkers.

Is it releated to SIMD compiler optimizations or does this apply to non-AVX supporting CPUs?

**4/** **@Ashkan_GC** ^1947554067011838054

**@anicic_filip** **@nicbarkeragain**

Branches are slower because they need to be predicted and predictions can be wrong and cause stalls in instruction processing

**5/** **@anicic_filip** ^1947565036106313960

**@Ashkan_GC** **@nicbarkeragain**

So the CPU having to switch between doing a sum or not doing a sum based on the if is slowing it down, while doing a constant workload of multiply and then sum is more predictable, so also faster?
Does this mean that older CPUs with worse to none prediction would suffer the most?

## Related

- Spine: [[archive/threads/nicbarkeragain/2025-07-22-branchless-programming-is-a-term-used-to-describe]]
