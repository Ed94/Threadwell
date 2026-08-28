---
title: "Thinking about visible pipelining in the ISA."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2092844404004266058"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2092844404004266058"
date: 2026-08-27
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Thinking about visible pipelining in the ISA."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2092844404004266058
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-08-27 05:19:23

## Thread

**1/** **@NOTimothyLottes** ^2092844404004266058

Thinking about visible pipelining in the ISA.
For example,
IMAD p=a*b+c
Use {A,B} reg file indexes from instruction[0]
Use {C} reg file indexes from instruction[1]
To save on flipflops (CLBs), one less pipeline stage for C
C has 1 less clock of input latency

**2/** **@NOTimothyLottes** ^2092845415980826677

My plan for conditionals is to have a {U,V} register which is pipelined in parallel with the DSP, and a CLB between DSP.p and dRAM stores. The CLB conditionally selects the store between {mux(u,v) based on P.MSB, and P}. With {U,V} update conditional on opcode bits (CE control).

**3/** **@NOTimothyLottes** ^2092845964029521939

Meaning one can save a prior value into U or V, and then later do the test which sets a sign bit which controls which bank gets the U vs the V. So one can get a full compare and swap in one clock. Or store just one and discard the other (for predicated logic).

**4/** **@NOTimothyLottes** ^2092846391387193766

Meaning single clock store simultaneous min and max, etc. Stuff today's GPUs don't even have.
