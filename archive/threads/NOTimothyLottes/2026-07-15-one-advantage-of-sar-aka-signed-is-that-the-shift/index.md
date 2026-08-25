---
title: "One advantage of SAR (aka signed '>>') is that the shift-by operand HW uses only the 5|6 LSBs automatically."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2077224595858280506"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2077224595858280506"
date: 2026-07-15
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "One advantage of SAR (aka signed '>>') is that the shift-by operand HW uses only the 5|6 LSBs automatically."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2077224595858280506
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-15 02:51:51

## Thread

**1/** **@NOTimothyLottes** ^2077224595858280506

One advantage of SAR (aka signed '>>') is that the shift-by operand HW uses only the 5|6 LSBs automatically. So if you have a mixed used control word, you don't have to mask out the MSBs. Can save an instruction.

**2/** **@NOTimothyLottes** ^2077225347049767246

Working through an idea of a single uber-instruction interpreted language for code generation. Meaning something that never misses the instruction cache and executes fully out of the micro-op cache. Fully data driven with a direct map 64k entry symbol table.

**3/** **@NOTimothyLottes** ^2077227411112870280

Borrows some ideas from SIMD GPU programming. Like instead of branching/predicating to avoid stores, just store to a discarded area (like a negative offset on the GPU, or a designated trash address on the CPU).

**4/** **@NOTimothyLottes** ^2077234537302556898

Don't want exit condition logic in the infinite loop, so exit will have to be having the program store an exit value into a set address, and an external watchdog polling for exit at some sleep frequency.

**5/** **@NOTimothyLottes** ^2077241596869751029

SAR on a control word can in theory grab 3 values.
SF (sign flag) is set to MSB bit
CF (carry flag) is set to what shifts into bit -1
and output

The SF and CF can be used for CMOVcc
Output can be used for another shift (after CMOVccs)
