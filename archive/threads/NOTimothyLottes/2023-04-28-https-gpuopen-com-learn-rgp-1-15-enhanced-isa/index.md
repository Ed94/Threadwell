---
title: "https://gpuopen.com/learn/rgp-1-15-enhanced-isa-view/ Nice Disasm View :) - However op  latency isn't useful."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1651938781610508288"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1651938781610508288"
date: 2023-04-28
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "https://gpuopen.com/learn/rgp-1-15-enhanced-isa-view/ Nice Disasm View :) - However op  latency isn't useful."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1651938781610508288
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-04-28 13:17:51

## Thread

**1/** **@NOTimothyLottes** ^1651938781610508288

https://gpuopen.com/learn/rgp-1-15-enhanced-isa-view/ Nice Disasm View :) - However op  latency isn't useful. Need to see multiwave instruction trace across time, colored by instruction type, enhanced with mark if wave is waiting to issue a given functional unit. Only then will great optimization be possible.

**2/** **@NOTimothyLottes** ^1651939770350678019

It would also be best to see overlay of board power (because !/W is the end goal), and an overlay of exactly where there are bubbles in DRAM traffic. Because anything memory bound, the goal is to minimize DRAM bubbles. Need to see how they form dynamically over time to fix ...

**3/** **@NOTimothyLottes** ^1651941119075164162

For GPU profilers, might see say {92% ALU, 50% TEX, 21% L2}, then wonder, where is 8% I'm missing. And only way to start to understand that, is to be seeing how waves are executing instruction wise against each other. CPU-profiler-like averages per disassembly line won't cut it.

**4/** **@NOTimothyLottes** ^1651945376847392769

Parallel machines can only be understood by seeing the parallel execution. I still have examples today of taking a vanila 32-bit shader (already designed to be fast) and getting 30% returns on all micro optimizations.

**5/** **@NOTimothyLottes** ^1651946306737250304

Lastly, side with enabling. Remember people can learn too. And there is typically super skilled people seeded at all companies that teach others how to use advanced tools when they are available.
