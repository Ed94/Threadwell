---
title: "Garbage collection is still unfit for demanding games:"
type: archive
source: twitter
source_url: "https://x.com/meesedev/status/2051611535999426655"
author: "A Flock of Meese"
handle: meesedev
post_id: "2051611535999426655"
date: 2026-05-05
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - meesedev
description: "Garbage collection is still unfit for demanding games:"
in_reply_to: ""
---

## Source

- URL: https://x.com/meesedev/status/2051611535999426655
- Author: A Flock of Meese (@meesedev)
- Posted: 2026-05-05 10:34:41

## Thread

**1/** **@meesedev** ^2051611535999426655

Garbage collection is still unfit for demanding games:
1. GC requires ~2x the memory footprint to achieve equivalent performance to an game using manual memory management.
2. GC consumes extra threads and memory bandwidth that could've been used for the game.
3. ZGC trades off throughput for latency. In layman's terms, your game will run slower, but at least you won't have lag spikes.

**2/** **@meesedev** ^2051615475994423760

Correction: ZGC reduces the chance of hitching. It does not fully eliminate hitching.
