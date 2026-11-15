---
title: "Not a joke: I'm re-trying development through direct 32-bit hex editing of a binary, with a layer of annotation which consists of 9 character comment per 32-bits, and a 1-bit tag if a 32-bit value is an opcode."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2119112267648094671"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2119112267648094671"
date: 2026-11-07
archived: 2026-11-14
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Not a joke: I'm re-trying development through direct 32-bit hex editing of a binary, with a layer of annotation which consists of 9 character comment per 32-bits, and a 1-bit tag if a 32-bit value is an opcode."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2119112267648094671
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-11-07 16:58:30

## Thread

**1/** **@NOTimothyLottes** ^2119112267648094671

Not a joke: I'm re-trying development through direct 32-bit hex editing of a binary, with a layer of annotation which consists of 9 character comment per 32-bits, and a 1-bit tag if a 32-bit value is an opcode. This is one layer more hardcore than assembly programming.

**2/** **@NOTimothyLottes** ^2119112827591860340

I've made a subset of x86-64 where I use extra prefix bytes to make all "opcodes" 32-bit, as well as making it direct 1:1 map to different 32-bit values in ARM64, but with the same function. Meaning I can transcode simply if need be.

**3/** **@NOTimothyLottes** ^2119113469702352935

32-bit opcode to human readable string (9-characters) is a search through a lookup table, and happens only at edit time. A human readable string to 32-bit opcode is also just a lookup table search at edit time. As simple as it gets. Everything factored into data, almost no code.

**4/** **@NOTimothyLottes** ^2119113969030095287

Editor style is simply direct binary edits at runtime, with ability to see all memory live. Effectively the minimal hardcore dev environment.

**5/** **@NOTimothyLottes** ^2119115446121111908

I've ditched RIP relative addressing and RIP relative call/jmp. Meaning I only do call/jmp to register. That was the core simplification. I still have conditional branching by a multiple of 4 bytes with a signed 8-bit immediate, for the few cases I might need that.

**6/** **@NOTimothyLottes** ^2119115894148473152

So I don't need any relinking on edit motion, instead I stick the few 32-bit branch addresses (forced lower 32-bit runtime) in a lookup table and load then call. Call pointers are simply part of the data layout specification instead of being baked into source.

**7/** **@NOTimothyLottes** ^2119117987462443034

Early in this path I was inspired by the ideas of Charles Moore and friends, but it was the sourceless direction rather than color forth itself that was most interesting to me personally - https://www.ultratechnology.com/prog.htm

**8/** **@NOTimothyLottes** ^2119118979444699291

Getting this project finished is probably the point at which I'll be out of temporary home project retirement ... maybe will do a video blog on this one. Still refining the 32-bit subset and tables (the part that takes the longest time as it's like a mini virtual ISA design).

**9/** **@NOTimothyLottes** ^2119121301592060301

Some useful references used in this project: 
https://ref.x86asm.net/coder64.html
https://defuse.ca/online-x86-assembler.htm
https://www.felixcloutier.com/x86/
https://www.scs.stanford.edu/~zyedidia/arm64/index.html

**10/** **@NOTimothyLottes** ^2119122239224271302

My hardware targets are similar to before, to the metal dedicated stuff for either x86-64 or ARM64 and AMD GPUs on Linux. So any associated AMD based Steam HW platform.

**11/** **@NOTimothyLottes** ^2119122622684238254

No user-space libraries. Only kernel interfaces, not running in X/Wayland, and instead going direct to the AMD kernel driver from a VT session.

**12/** **@NOTimothyLottes** ^2119122982983651379

I'll be treating this as a vintage to the metal console platform with assembly-level dev for CPU/GPU. Bringing back a memory of how things had been, but on modern HW. Something more of an actual console than anything you'd see from MS/Sony/Nintendo.
