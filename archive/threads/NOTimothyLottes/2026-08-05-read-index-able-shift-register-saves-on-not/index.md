---
title: "Read index-able shift register saves on not needing address lines for the store, just need a clock enable bit."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2084817993213583512"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2084817993213583512"
date: 2026-08-05
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Read index-able shift register saves on not needing address lines for the store, just need a clock enable bit."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2084817993213583512
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-08-05 01:45:18

## Thread

**1/** **@NOTimothyLottes** ^2084817993213583512

Read index-able shift register saves on not needing address lines for the store, just need a clock enable bit. Makes it temping for a bank of a register file, and a SLICEM gets 32-bit/s LUT, simple-dual-port on ultrascale+ peaks at 7/8ths that.

**2/** **@NOTimothyLottes** ^2084818888043135455

Array of shift registers can function as both an operand and result cache simultaneously. It can also provide sub-word addressing, depending on how operand and result bits are programmibly distributed across shift registers (for SIMD, requiring complex instruction encoding).

**3/** **@NOTimothyLottes** ^2084819391850377635

Of course the side effect of using a set of sub-word addressable multi-bank shift registers as a flexible register file, the index of their contents changes on each clock-enable. Meaning a human needs help programming ...

**4/** **@NOTimothyLottes** ^2084821615636836684

For context, yes it would be easy to just use 3 BRAMs to produce a 3 bank configuration for operand fetch, but then the BRAM:DSP ratio would be 3:1 which ultimately wouldn't be good utilization of a machine that has a physical 1:2 BRAM:DSP ratio.
