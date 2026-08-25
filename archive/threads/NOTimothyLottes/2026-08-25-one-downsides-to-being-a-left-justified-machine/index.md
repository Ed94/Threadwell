---
title: "One downsides to being a left justified machine and emulated on a FPGA is that one cannot use the built-in DSP's rounding capability through CIN."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2092088375205359693"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2092088375205359693"
date: 2026-08-25
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "One downsides to being a left justified machine and emulated on a FPGA is that one cannot use the built-in DSP's rounding capability through CIN."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2092088375205359693
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-08-25 03:15:12

## Thread

**1/** @NOTimothyLottes

One downsides to being a left justified machine and emulated on a FPGA is that one cannot use the built-in DSP's rounding capability through CIN. So the end of accumulation requires a long latency feedback of the MSB of P to effect LSB bits of C for final add before right shift

**2/** @NOTimothyLottes

Yields 2 options - that accumulation + expensive post accumulation rounding --OR-- round after each MUL by setting the shifted out LSBs of C based on XOR(A,B) MSBs and don't accumulate (no P) which means always a fixed 4 clk ALU latency [with forwarding]

**3/** @NOTimothyLottes

For reference - Left-justified signed IMAD: Reduced to a 3-bit machine with a 16-bit accumulator for testing [below], being used as a C model proxy for a 24-bit A expanded to 7 series 25-bits (the LSB 0), with a 18-bit B, and 24-bit C (and extracted 24-bit result in same slot).

![](https://pbs.twimg.com/media/HQiZnwQXIAAFcvO?format=png&name=orig)

**4/** @NOTimothyLottes

This is for a vector SIMD (a soft GPU). Effectively a 32-bit memory driving a 24-bit ALU with variable sub-word size {24,16,8,4} as inline compression/decompression HW. Noticed sub-word extraction gets less expensive if one uses SR on the registering flip-flop for LSB zeros.

**5/** @NOTimothyLottes

Been working on my little FPGA GPU project for quite some time, mostly trying to engineer out enough of the pipeline as mapped to CLBs/DSPs/dRAMs/bRAMs with basic rules like one CLB deep per pipeline stage per registering and no cascading, etc, to target peak frequency ...

**6/** @NOTimothyLottes

I'm engineering some horribly unconventional things, like a one instruction SIMD VLIW ALU (IMAD) with modifiers and surrounding support for binary searching "a*b/c" and "sqrt", etc, paired to a sub-word bit extraction/packing unit, sign conditional swap store to banked reg file
