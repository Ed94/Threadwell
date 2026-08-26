---
title: "Seems like one of the pain points with Xlinix DSPs that if you want either a 32-bit ADD or a MAD you need to CLB the A B inputs differently due to how the ADD path takes A:B and the MUL takes A,B."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2085365714412556730"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2085365714412556730"
date: 2026-08-06
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Seems like one of the pain points with Xlinix DSPs that if you want either a 32-bit ADD or a MAD you need to CLB the A B inputs differently due to how the ADD path takes A:B and the MUL takes A,B."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2085365714412556730
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-08-06 14:01:45

## Thread

**1/** **@NOTimothyLottes** ^2085365714412556730

Seems like one of the pain points with Xlinix DSPs that if you want either a 32-bit ADD or a MAD you need to CLB the A B inputs differently due to how the ADD path takes A:B and the MUL takes A,B.

**2/** **@NOTimothyLottes** ^2085366833033392185

In my case the top 4-bit MSBs of operands already use a 8:1 mux so im out of single pipeline stage CLB. Puts the design back into the slow burn on break rethink mode …

Branches: [[archive/threads/NOTimothyLottes/2026-08-06-seems-like-one-of-the-pain-points-with-xlinix/2026-08-06-NOTimothyLottes-at-least-with-ultrascale-if-you-can-afford-to-run]]

**3/** **@NOTimothyLottes** ^2085369523838787831

The aim was to place a sub-word decode pipeline stage (CLB) between a direct mapped shift register (SLICEM) to DSP inputs for operand fetch. With shift register getting a program controlled MUX as input/clk …

**4/** **@NOTimothyLottes** ^2085370511807136007

… that mux taking things like bits of P, operands conditional to the sign bit of P (for 1 clk compare and swap), BRAM read, etc. But each of the 3 gets separate CE and mux choice. So functions like 32 entry 3 bank registers file.

**5/** **@NOTimothyLottes** ^2085371367000563887

So in register sorting actually works out at 1 clk per compareswap. Because it’s a 3 bank store, and one can bank swap too on the swap.

**6/** **@NOTimothyLottes** ^2085372781026283653

In some ways this is an evolution of forth where the data stack transforms into multi bank and one replaces the stack with an indexable looping queue (without a pop).

**7/** **@NOTimothyLottes** ^2085390994212565000

Note sub-word extract is right justified (fills MSBs) and left side gets zero fill. Far better than the left justified zero/sign extraction, but requires a IMAD fixed shift (fixed point op).
