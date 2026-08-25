---
title: "Stupid hardware question: Why does AMD use several counters instead of one u64 bitmask for memory ops? "
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1898272635277967509"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1898272635277967509"
date: 2025-03-08
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Stupid hardware question: Why does AMD use several counters instead of one u64 bitmask for memory ops? "
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1898272635277967509
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2025-03-08 07:20:39

## Thread

**1/** **@SebAaltonen** ^1898272635277967509

Stupid hardware question: Why does AMD use several counters instead of one u64 bitmask for memory ops? 
Each load/store would have a bit index and wait would have a bitmask (marked bits need to be set = finished).

![](https://pbs.twimg.com/media/GlgEaJDW8AA-t1l?format=jpg&name=orig)

Branches: [[archive/threads/SebAaltonen/2025-03-08-stupid-hardware-question-why-does-amd-use-several/2025-03-08-NOTimothyLottes-actually-this-is-a-super-important-question-imo]]

**2/** **@SebAaltonen** ^1898272964908359917

I am glad that RDNA4 has separate counters for sampling (long latency) and lower latency raw loads now. That's a good improvement.

**3/** **@SebAaltonen** ^1898280870462554297

Some thoughts: Compiler managed bitfield slot indices would be iffy with loops and branches. One bit per register (big bitfield) would always work, but that would be much more than 64 bits. And wait instructions would be iffy (how to describe a massive bitfield).
