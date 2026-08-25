---
title: "Operands/time = Perf"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2091652388184572155"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2091652388184572155"
date: 2026-08-23
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Operands/time = Perf"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2091652388184572155
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-08-23 22:22:45

## Thread

**1/** **@NOTimothyLottes** ^2091652388184572155

Operands/time = Perf
Mitigating amplifiers
a. Register reuse [avoid load]
b. Operand caching [avoid reg file access]
c. Destination reuse [forwarding]
d. Scalar constants + SIMD [broadcast]
e. Parallel subword extraction [inline decompression]

**2/** **@NOTimothyLottes** ^2091655502786699296

f. Banking [for multi-port]

If reg file supports only 1 store source/port/clk then you'd need forwarding to open a clock to do a parallel load (with alu) for the given port. Likewise you'd need an isa "last use" (avoid reg write) to get parallel store [into reg file] (with alu).

**3/** **@NOTimothyLottes** ^2091657447425380701

Seems like the best one can do on a xilinx fpga is 6 clock pipeline
[lutRAM]->[CLB1]->[DSP.ab]->[DSP.m]->[DSP.p]->[CLB2]->[lutRAM]
Where CLB1 does {DSP.p to multiplier operand forwarding to get 4 clock IMAD latency}. And accumulation uses internal c=p routing for "no" latency.

**4/** **@NOTimothyLottes** ^2091659049242599769

CLB2 is injection for loads from BRAM (when regfile port store isn't needed for DSP.p). If register file is 3 way banked, and direct mapped (bank 0 -> CLB -> DSP.A), then there are 3 reads/clk and 3 writes/clk ... given a value is not needed in all banks, lots of pipelinabiliy

**5/** **@NOTimothyLottes** ^2091659554413064445

But most FPGA SIMD soft processors stick to even longer pipelines, direct regfile in BRAM, and no usage of DSP P->C forwarding (accumulation). Which means they have heavy dilution of their memory/time (too many parallel tasks).

**6/** **@NOTimothyLottes** ^2091660056156647719

I think it's better to hand unroll parallel tasks into one assembled instruction stream, expose variable latency {forwarded vs round-trip through reg file} --vs-- the alternative of HW managed multi-threading.

**7/** **@NOTimothyLottes** ^2091660458864296247

However, how many arch have actual instruction stream compression? None? (x86 doesn't really count). If you build around massive unrolling, you are doing the same stuff with offset'ed operands -> so obviously wants compression, else a tiny I$ won't survive

**8/** **@NOTimothyLottes** ^2091661084079878540

Ok, I lied, there are some historic examples of multi-component + SIMD which leverage a {1,2,3,4} ISA bitfield to repeat the op/compent, or SIMD itself via looping instruction -- which technically is a great example of "compression"

**9/** **@NOTimothyLottes** ^2091661665175482794

Getting the 3x local memory vs operand data rate amplifier, along with memory hierarchy pipelining, sorted is perhaps the most important thing for realized IPC, but there is still the 100x operand vs external bandwidth mitigation which defines the platform ...
