---
title: "Thread: A simple explanation why AMDs 144MB 3D cache makes games run significantly faster."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1611409453806403586"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1611409453806403586"
date: 2023-01-06
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Thread: A simple explanation why AMDs 144MB 3D cache makes games run significantly faster."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1611409453806403586
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2023-01-06 17:08:46

## Thread

**1/** **@SebAaltonen** ^1611409453806403586

Thread: A simple explanation why AMDs 144MB 3D cache makes games run significantly faster.

TLDR: The working set of most games fits inside the 3D cache. All cache lines accessed during the previous frame are still present in cache. Sequential frames only differ slightly.

**2/** **@SebAaltonen** ^1611409879226269703

If you look at any recent GPU benchmarks (RTX 4090), you notice that most games run at 240Hz+ if you remove the GPU bottleneck. Run at 1080p or similar without RTX. This is enough info to calculate how much memory we can access per frame.

**3/** **@SebAaltonen** ^1611410295842291728

DDR4-3200 provides us 50GB/s theoretical bandwidth. In reality we get roughly 40GB/s, which is proven by memory benchmarks. Divide this by 240Hz, and we get 170MB/frame. That's how much we can access unique memory cache lines per frame in a game that runs at 240Hz = most games.

**4/** **@SebAaltonen** ^1611410746797080595

AMDs 128MB 3D cache is a victim cache, so it doesn't have the same pages as the smaller cache levels. Thus we can use the 144MB number as our maximum working set limit. 170MB/frame considers that game is 100% mem bound all the time. In reality it's not, thus 144MB is enough.

**5/** **@SebAaltonen** ^1611411278467334144

And this is why AMD 3D cache provides big gains for games. The CPU working set (data accessed in a single frame) fits to the 144MB cache, meaning that the next frame can read most of the data from the cache. The difference between two sequential frames is minimal.

**6/** **@SebAaltonen** ^1611411663218950152

Correction: pages -> cache lines. Victim cache doesn't keep the same cache lines as lower level caches.

**7/** **@SebAaltonen** ^1611417779474677799

Traditional MT workloads such as compiling code doesn't get as big benefits. Each .cpp file is compiled in a separate process. There's zero data sharing between them. If you have a cold start (new process) for every compiled file, there's not much a massive cache can do to help.

Branches: [[archive/threads/SebAaltonen/2023-01-06-thread-a-simple-explanation-why-amds-144mb-3d/2023-01-06-hkultala-caches-work-with-physical-addresses-all-the-code]], [[archive/threads/SebAaltonen/2023-01-06-thread-a-simple-explanation-why-amds-144mb-3d/2023-01-06-isotoxin390-seb-for-the-next-gen-consoles-what-is-your-amd]], [[archive/threads/SebAaltonen/2023-01-06-thread-a-simple-explanation-why-amds-144mb-3d/2023-01-07-morbidarne2007-well-this-is-about-to-change-in-llvm-at-least]], [[archive/threads/SebAaltonen/2023-01-06-thread-a-simple-explanation-why-amds-144mb-3d/2023-01-07-Kodiak_73-compiling-translation-units-cpp-files-dont]], [[archive/threads/SebAaltonen/2023-01-06-thread-a-simple-explanation-why-amds-144mb-3d/2023-01-08-GPUsAreMagic-very-nicely-put-together-but-one-big-omission-imo]]
