---
title: "Re-FPGA-land ALUs - I'm firmly distracted by an alternative history of the unexplored left justified extreme fixed point."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2083757874686161259"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2083757874686161259"
date: 2026-08-02
archived: 2026-08-23
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Re-FPGA-land ALUs - I'm firmly distracted by an alternative history of the unexplored left justified extreme fixed point."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2083757874686161259
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-08-02 03:32:46

## Thread

**1/**

Re-FPGA-land ALUs - I'm firmly distracted by an alternative history of the unexplored left justified extreme fixed point. Where signed integer numbers represent {-1.0 to <1.0}. Where the primary IMAD op includes a huge fixed signed right shift ...

**2/**

For those planted in the right-justified current fixed point timeline, your bytes get loaded into the LSBs, and your addressing uses the LSBs. The idea of doing the reverse of this is probably completely alien -> loading smaller bit types into the MSBs first ...

**3/**

Meaning standard integer thinking is to start with small things like an index and scale that by the stride into a larger number. But with what I'm suggesting you start with something large and instead make it smaller.

**4/**

In a traditional right-justified CPU, you'd have three ops {MUL, ADD, SHR} which could be reduced to {IMAD, SHR}, but would be just one op on a left justified machine. Meaning doing 'fixed point' stuff is a bit faster.

**5/**

32-bit left justified machine, can easily leverage say a 18-bit * 25-bit multiplier (Xlinix DSP) because the MSBs are always fed in, and the useful MSBs are always pulled out of the accumulator (P). Right justified machines really need that full 32-bit x 32-bit MUL

**6/**

Left justified variable bit-width loads make a lot more sense, partly because the LSBs index into bits (or sub-bits depending on mapping) effectively (instead of bytes), and one can do {4/8/16/32-bit} extraction with 8 SLICES and one CLB deep [a lot easier than right-justified]

![](https://pbs.twimg.com/media/HOsENEBXEAAoWlx?format=png&name=orig)
**7/**

The core normalized IMAD can easily be made -/+ symmetrical simply by feeding in truncated LSBs of the add operand with simple logic based on MSBs of mul operands. In the example below the {-4} represents {-1.0}. Of course -4*-4 overflows to -4 [2's comp]

![](https://pbs.twimg.com/media/HOsFs-nWAAAUlTy?format=png&name=orig)
**8/**

Predicate/bool logic becomes {0.0, -1.0} based, can leverage {a+b} wrap around to implement XOR, and -(a*b) to implement AND.

![](https://pbs.twimg.com/media/HOsG3VBXAAA92kz?format=png&name=orig)
**9/**

Doing a "perspective divide" {s=x/z} can be transformed into a scaled perspective divide {s=x*(a/z)} to work around the {-1.0 to <1.0} range limitation. And one can transform the divide into a binary search for 's' - specifically largest 's' where {s*z<=x*a}

![](https://pbs.twimg.com/media/HOsIBCBWcAA79PL?format=png&name=orig)
**10/**

Notice this binary search test takes just one IMAD {s*z+t} where t=-x*a. Meaning a smart machine can do a test step in 2 ops on a DSP (one IMAD for the test, the next to ADD to 's' for the next search step) ...

**11/**

Which requires the opcode ISA to have a latched delayed write to the register file that is conditional on the sign bit of a later IMAD op. This can make binary search for things like sqrt(x) also just as fast.

**12/**

I think there are ways to transcend typical integer machine IPCs by having uber ops in the ISA (this left-justified machine has a 1-clock {MUL,ADD,SHIFT,+ signed conditional register STORE,+ extra modifiers (like NOT)}. But still have extremely simple implementations.
