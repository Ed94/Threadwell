---
title: "@NOTimothyLottes Is that possible when you have a linear dependency chain with no independent work? I can't think of anything other thanks splitting up the workload even more, which doesn't sound great"
type: archive
source: twitter
source_url: "https://x.com/jakubtomsu_/status/1946485199006498933"
author: "Jakub Tomšů"
handle: jakubtomsu_
post_id: "1946485199006498933"
date: 2025-07-19
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Is that possible when you have a linear dependency chain with no independent work? I can't think of anything other thanks splitting up the workload even more, which doesn't sound great"
in_reply_to: ""
parent_post_id: "1946453750085808492"
---

## Source

- URL: https://x.com/jakubtomsu_/status/1946485199006498933
- Author: Jakub Tomšů (@jakubtomsu_)
- Posted: 2025-07-19 08:20:10

## Branch

**1/** **@jakubtomsu_** ^1946485199006498933

**@NOTimothyLottes**

Is that possible when you have a linear dependency chain with no independent work? I can't think of anything other thanks splitting up the workload even more, which doesn't sound great

**2/** **@NOTimothyLottes** ^1946572986628108566

**@jakubtomsu_**

Even the typical serially dependent post processing passes can be chunked spatially to re-introduce pipelining.

**3/** **@NOTimothyLottes** ^1946574786861121592

**@jakubtomsu_**

Besides cutting groups into pipelinable subsets, one could unfactor the global barrier counter into the objects. So that a queue can start on pairs early if they have completed before the whole independent group finishes.

**4/** **@AgileJebrim** ^1946575640368709944

The problem with pipelining is that you still get idleness as it’s only as fast as the slowest pipeline stage. It makes it difficult to optimize and improve overall performance if the thing you’re optimizing isn’t what’s bottlenecking the system. A more purely data parallel approach allows for any stage to be optimized and have an improvement on the entire tick’s execution time.

**5/** **@NOTimothyLottes** ^1946582048224768487

**@AgileJebrim** **@jakubtomsu_**

One cannot maintain high utilization in a problem with high non-pipelined global barriers. Period. And as the presentation showed extremely well, as core count increases mixed with the natural irregular thread completion times, the whole machine idle time gets quite big.

**6/** **@NOTimothyLottes** ^1946584861713584280

**@AgileJebrim** **@jakubtomsu_**

Long ago during my time at a GPU IHV, I had implemented a driver perf strategy that uid'ed barriers per title and selectively ignored them. Running the games at very low resolutions to get conservative set. Even back then one could find double digit perf returns in trace replays.

**7/** **@NOTimothyLottes** ^1946586982311707005

**@AgileJebrim** **@jakubtomsu_**

Fast forward to modern times, it wouldn't be surprising to see GPUs with under 50% whole frame utilization of both ALU and MEM due to lack of keeping the work flowing well in the machine.

**8/** **@NOTimothyLottes** ^1946588772419719389

**@AgileJebrim** **@jakubtomsu_**

And in that, some good amount is non pipelined barriers, mixed with other bottlenecks. This poor utilization is likely why IHVs are burning area on fine grain clock gaiting which wouldn't help if devs all authored like power virus

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-07-19-peanut-gallery-vs-parallelizing-the-physics-solver]]
