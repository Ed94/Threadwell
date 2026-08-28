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

Branches: [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two/2019-05-05-SebAaltonen-dont-use-spinlock-for-waits-use-spinlock-only-to]], [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two/2019-05-05-romzr-got-a-link-to-the-slide-deck]], [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two/2019-05-05-pATjako-i-would-love-to-see-a-comparison-to-arm64-from]], [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two/2019-05-05-ArvidGerstmann-interesting-ive-been-using-xchg-over-cmpxchg-for]], [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two/2019-05-06-morfar-its-a-shame-there-is-no-mm-pause-in-the-bad-case]], [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two/2019-05-06-matiasgoldberg-i-have-one-suggestion-1st-stage-you-measure-how]], [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two/2019-05-06-0xF390-you-can-find-many-implementations-here-including]], [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two/2019-05-06-0xF390-tatas-read-only-inner-loop-is-a-much-better]]

**2/** **@SebAaltonen** ^1125622264819605504

Important clarification: Using basic load works only on x86/64. Better use atomic load. It will result in the exactly same compiled code on x64 and work also on ARM64. Also gives compiler more info to avoid unwanted optimizations.

**3/** **@SebAaltonen** ^1125622526250508289

For more info watch this: https://x.com/sebaaltonen/status/1125084734365872129?s=21
