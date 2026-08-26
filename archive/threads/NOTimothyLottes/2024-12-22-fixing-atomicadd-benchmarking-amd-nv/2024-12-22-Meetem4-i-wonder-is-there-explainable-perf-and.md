---
title: "@NOTimothyLottes I wonder is there explainable perf and algorithmic different between atomicAdd on uint cell vs incrementing a buffer counter (for append/consume buffer)"
type: archive
source: twitter
source_url: "https://x.com/Meetem4/status/1870944398839620087"
author: "Meetem"
handle: Meetem4
post_id: "1870944398839620087"
date: 2024-12-22
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes I wonder is there explainable perf and algorithmic different between atomicAdd on uint cell vs incrementing a buffer counter (for append/consume buffer)"
in_reply_to: ""
parent_post_id: "1870942850684420564"
---

## Source

- URL: https://x.com/Meetem4/status/1870944398839620087
- Author: Meetem (@Meetem4)
- Posted: 2024-12-22 21:27:59

## Branch

**1/** **@Meetem4** ^1870944398839620087

**@NOTimothyLottes**

I wonder is there explainable perf and algorithmic different between atomicAdd on uint cell vs incrementing a buffer counter (for append/consume buffer)

**2/** **@NOTimothyLottes** ^1870946922233749918

**@Meetem4**

So I don't use the "fixed function" atomic counters (which are going to be emulated likely with global atomics), nor do I use the "fixed function" append or consume of graphics. However ...

**3/** **@NOTimothyLottes** ^1870947271568973944

**@Meetem4**

Some platforms probably optimized append and consume by parallelizing the global atomics to multiple L2 partitions (had parallel counters). Which of course one can do in software too.

**4/** **@NOTimothyLottes** ^1870947546987647064

**@Meetem4**

And at least AMD traditionally had GDS which could be used, but that is the great serializer, so not sure if that is wise for huge GPU appending (multiple append queues is probably better, in theory)

**5/** **@Meetem4** ^1870947985351483769

**@NOTimothyLottes**

Well, yeah, I was expecting some form of optimization here, because the counter is only valid for the current thread, according to D3D specification, which raises the suspicion that some higher level optimization can be applied

## Related

- Spine: [[archive/threads/NOTimothyLottes/2024-12-22-fixing-atomicadd-benchmarking-amd-nv]]
