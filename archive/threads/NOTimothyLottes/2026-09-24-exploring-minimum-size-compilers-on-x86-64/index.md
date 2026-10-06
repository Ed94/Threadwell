---
title: "Exploring minimum size compilers on x86-64, specifically branch-free logic (one predicted jnz to loop per input token)."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2103076419379339498"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2103076419379339498"
date: 2026-09-24
archived: 2026-10-06
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Exploring minimum size compilers on x86-64, specifically branch-free logic (one predicted jnz to loop per input token)."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2103076419379339498
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-09-24 10:57:46

## Thread

**1/** **@NOTimothyLottes** ^2103076419379339498

Exploring minimum size compilers on x86-64, specifically branch-free logic (one predicted jnz to loop per input token). A minimum forth-like language can be built with a 17-instruction/token loop. Source uses {2-bit tag, 14-bit dictionary index}.

**2/** **@NOTimothyLottes** ^2103078363422146662

So the instructions of the compiler itself fits on one x86-64 cacheline, less than 64 bytes total.

**3/** **@NOTimothyLottes** ^2103079055113195747

From a data perspective, it's 16384 entry dictionary that contains direct 32-bit chunks of pre-compiled instructions that can be spiced together.

**4/** **@NOTimothyLottes** ^2103079963658469860

2-bit tag/token,
00 : write value from dictionary 'V'
01 : write V-nextInstructionPointer (for call/jmp)
02 : ignore (for comments)
03 : write instructionPointer into dictionary (for define)

So like a direct mapped tiny color-forth

**5/** **@NOTimothyLottes** ^2103081099068899412

Haven't timed code generation speed, but it's probably peaks around 1/2 GB/sec of code gen on a 2 GHz x86-64. Meaning fast enough to support recompiling the whole program each frame if you wanted to.

**6/** **@NOTimothyLottes** ^2103082320853094619

Designing the language around making something forth-like to be the macro assembler for GPU binary generation, but also fast enough to be the entire x86-64 code as well. Meaning can do x86-64 assembly too for important raw loops.

**7/** **@NOTimothyLottes** ^2103083570550223191

Apparently AMD's Zen line doesn't have sub-register stalls like Intel, so one can take advantage. Also used the 2-for-1 {SAR ax,15} trick, which produces a full 0/~0 mask along with putting the last shifted out bit 14 in CF. Quite useful for branch-free logic (like cmovCC ops).

**8/** **@NOTimothyLottes** ^2103084229420597601

x86-64 is actually really poor ISA for branch-free logic for many reasons, like cmovCC doesn't have an IMM operand form so you burn registers for immediate constants, and not having a separate destination register means extra MOVs to duplicate, with some exceptions like LEA.

**9/** **@NOTimothyLottes** ^2103084603682562173

Anyway this whole system was another exploration of a minimal x86-64 based setup. Last I was trying a text interpretered one (with branches), and I think this new one is substantially better.

**10/** **@NOTimothyLottes** ^2103085001730658640

There is also a lot of nice things about working in Linux and having the easy ability to guarantee code/data in the lower 32-bit address space. This is for no-library execution (meaning only kernel interfaces, including for the GPU).
