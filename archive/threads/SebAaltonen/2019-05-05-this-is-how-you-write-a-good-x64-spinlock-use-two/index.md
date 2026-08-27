---
title: "This is how you write a good x64 spinlock: Use two stage construct."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1125064645637738496"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1125064645637738496"
date: 2019-05-05
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "This is how you write a good x64 spinlock: Use two stage construct."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1125064645637738496
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2019-05-05 15:48:08

## Thread

**1/** **@SebAaltonen** ^1125064645637738496

This is how you write a good x64 spinlock: Use two stage construct. Outer test is read. Multiple cores reading same cache line = no contention. Inner = exchange instead of CAS. Pause instruction in the loop body to save power and/or give all cycles to other logical core (SMT).

![](https://pbs.twimg.com/media/D50IVH0W0AALQ0y?format=jpg&name=orig)

**2/** **@SebAaltonen** ^1125065316650889217

Don’t use spinlock for waits. Use spinlock only to guard something that is guaranteed to return quickly. If you have an operation that is often fast but sometimes slow, use two stage spinlock with internal OS mutex.

**3/** **@SebAaltonen** ^1125067183476944896

Naive (bad) vs optimized (good) performance. See above post for code.

![](https://pbs.twimg.com/media/D50Ko4mXoAAR97L?format=jpg&name=orig)

Branches: [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two/2019-05-05-lectem-its-missing-exponential-backoff-for-mm-pause]], [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two/2019-05-05-AndrewJacksonZA-nice-code-up-above-also-https-x-com-sebaaltonen]]
