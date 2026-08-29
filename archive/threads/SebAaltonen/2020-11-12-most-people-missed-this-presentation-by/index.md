---
title: "Most people missed this presentation by @LottesTimothy in GDC 2019:"
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1326843999911555078"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1326843999911555078"
date: 2020-11-12
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Most people missed this presentation by @LottesTimothy in GDC 2019:"
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1326843999911555078
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2020-11-12 11:07:15

## Thread

**1/** **@SebAaltonen** ^1326843999911555078

Most people missed this presentation by @LottesTimothy in GDC 2019:

https://gpuopen.com/gdc-presentations/2019/gdc-2019-s5-blend-of-gcn-optimization-and-color-processing.pdf

It was about image kernels and their memory access patterns. Filled with GCN architecture specifics, but the most noteworthy detail was the LDS sliding window algorithm.

Thread...

**2/** **@SebAaltonen** ^1326844481556144128

Blur kernels are very popular, and the most annoying part about writing one is how you avoid fetching the neighborhood again and again. Tiny changes in execution order can have massive effect in cache utilization. The problem is especially tricky in separable X/Y gaussian blurs.

**3/** **@SebAaltonen** ^1326844975963926528

Naive separable gaussian blur fetches a long strip along X axis. Each pixel does the same. Pixel Y and Y+n share zero input pixels with each other. Pixels along the X axis share inputs. But if the kernel is wide enough it's hard to keep all of that data reliably in caches.

**4/** **@SebAaltonen** ^1326845530358632448

GPUs store pixels in roughly morton order. An aligned 4x4, 4x8 or 8x8 tile of RGBA8 data represents a GPU cache line (depending on GPU cache line size). Thus reading a long strip in one direction only utilizes a fetched cache line partially. GPU caches are tiny. Rest will be lost

**5/** **@SebAaltonen** ^1326846335321071616

Common workarounds to this problem: reduce occupancy (to minimize cache trashing), use long/wide compute kernels (32x8/8x32), assuming linear group order, doing 90 deg logical order rotation in Y pass, etc. None of these are perfect.

**6/** **@SebAaltonen** ^1326846682441592833

The sliding window algorithm GUARANTEES that each cache line will be read once, and written once. Data in every cache line is either fully read at once or fully written at once. There's no dice rolling with tiny GPU caches. Let me explain why this works.

**7/** **@SebAaltonen** ^1326847420697808896

Aligned 8x8 tile of RGBA8 pixels is 256 bytes. Thus it's dividable by 64/128/256 cache line sizes. We are loading/storing a full 8x8 tile to/from memory to groupshared memory at once. This data is never referred again, thus caches don't matter.

**8/** **@SebAaltonen** ^1326847965852545024

Simplied algorithm for X blur: Load 8x8 tiles to a ring buffer in groupshared memory until the blur kernel fits. Then process those tiles and write them. Load another tile (over the first tile in the ring buffer). Process one more tile and write it. Repeat until X scanline ends.

**9/** **@SebAaltonen** ^1326849218292674560

If we are assuming a wave size of 32 and 8x8 tiles, we have only 540 waves active at once (4K resolution). Each processing a Nx8 strip. This is not good. So instead we use wider groups. 512 threads is a nice group size. That gives us 64x8 groups. 4320 waves active at once!

**10/** **@SebAaltonen** ^1326850030825852929

Now we have 512 threads per GPU compute unit. To get great occupancy we try to fit four of them at once. If we assume 64 KB groupshared memory, we get 16 KB for each group. 64x8xRGBA8 = 2 KB. Thus we fit 8 tile ring buffer. And the maximum blur width is 512 pixels.

**11/** **@SebAaltonen** ^1326851592281354240

If you are implementing a box blur instead of gaussian, you can use a 32 bit integer accumulator for each X scanline. Add the new X pixel and subtract the removed (last) one as the kernel moves forward in X direction. This gives you constant time blur with perfect access pattern.

**12/** **@SebAaltonen** ^1326852595336536065

Typofix: 

"Now we have 512 threads per GPU compute unit" 
->
"Now we have 512 threads per group"

**13/** **@SebAaltonen** ^1326853553621770247

For wider formats such as RGBA16F, use Nx4 tile size instead. We want the Y width of the tile to be aligned to the texture cache lines (morton tiles). 4x4*RGBA16F = 128 bytes.  Only make the tile as large in Y direction as you absolutely need. Otherwise you waste groupshared mem.

**14/** **@SebAaltonen** ^1326854322068578304

You can implement a more complex NxM sliding window algorithm too. Or use write tiles instead of read tiles (accumulate to them directly), or both. Timothy's presentation has some info about these. My example here is simply the most trivial case of a separable blur.
