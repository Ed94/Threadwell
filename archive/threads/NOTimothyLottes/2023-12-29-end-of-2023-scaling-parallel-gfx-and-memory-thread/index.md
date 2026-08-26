---
title: "End of 2023 Scaling: Parallel Gfx and Memory <thread>"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1740754498883121242"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1740754498883121242"
date: 2023-12-29
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "End of 2023 Scaling: Parallel Gfx and Memory <thread>"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1740754498883121242
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-12-29 15:19:48

## Thread

**1/** **@NOTimothyLottes** ^1740754498883121242

End of 2023 Scaling: Parallel Gfx and Memory <thread>

**2/** **@NOTimothyLottes** ^1740754767557607756

[0] One could argue that with increasing transistor costs that large scaling is done. But what is perhaps more accurate is the context, its just scaling out of today's local minima.

**3/** **@NOTimothyLottes** ^1740754860021354891

[1] There are avenues to continue to scale, by breaking the conventions that don't scale. The harder truth to accept: that it requires altas to drop that globe of technical debt too.

**4/** **@NOTimothyLottes** ^1740755174581572010

[2] Lets take a simplified view of on-chip power. Power burned for memory access is roughly proportional to latency. Latency (aka distance) is the number of clocks. Computation is 'cheap' roughly because ALU latency is so small in comparison with global memory access.

**5/** **@NOTimothyLottes** ^1740755280898740231

[3] For the most part, today's graphics processing round trips through a global memory. Effectively all misses are same worst cost in latency and power. This doesn't continue to scale well.

**6/** **@NOTimothyLottes** ^1740755423626723461

[4] At some point non-uniform-memory-access NUMA for graphics is inevitable, it provides the tool which enables scaling the cost of memory access. And simplifies scaling the cost of the processor via chiplets.

**7/** **@NOTimothyLottes** ^1740755517683937761

[5] For read, ideally one wants short distance access (lower latency and lower power). Reads are typically on the critical path, where state is parked waiting for computation.

**8/** **@NOTimothyLottes** ^1740755868151607379

[6] Final store can support long distance travel. Because computation is done, and thus latency is no longer on the critical path. Ideally during the store the data would be deposited in local memory it is needed next. This concept is what breaks backwards convention for graphics

**9/** **@NOTimothyLottes** ^1740756036305518649

[7] Initially store to local memory perhaps scales by under 50%, in that the savings is '(local+remote)/(2*remote)' cost scaling.

**10/** **@NOTimothyLottes** ^1740756175556342181

[8] Another key insight is that if the tech is designed to keep locality, most of the stores should go local as well. Which approaches 'local/remote' cost scaling.

**11/** **@NOTimothyLottes** ^1740756517983224166

[9] And that (see [8]) is what enables the next tech revolution after NUMA, which is placing the ALU and memory closer together in HW. Making 'local' even lower cost than 'remote'.

**12/** **@NOTimothyLottes** ^1740756830547321220

[10] The GPU atomic, computed in the local last-level-cache partition, is one simplified manifestation of the prior concept. This is a big reason why GPU atomics scale on {NV/AMD}, and CPU atomics don't scale.

**13/** **@NOTimothyLottes** ^1740756958247051593

[11] Another aspect of store is multicast, or broadcast, neither are supported in today's hardware. The idea of saving power by depositing the data in multiple memories along it's path.

**14/** **@NOTimothyLottes** ^1740757285679284431

[12] One very important question, how to evolve today's graphics engines in such a way that they can transparently support this evolution in the future. HW vendors hands are tied, they mostly accelerate existing software.

**15/** **@NOTimothyLottes** ^1740757684356563103

[13] As software devs, we do carry some of the burden for solving the chicken and egg problem. And with that comes some responsibility to understand the physical limits of what can be done in hardware engineering.

Branches: [[archive/threads/NOTimothyLottes/2023-12-29-end-of-2023-scaling-parallel-gfx-and-memory-thread/2023-12-30-MissQuickstep-yup-ive-been-arguing-somewhat-prematurely-it]]
