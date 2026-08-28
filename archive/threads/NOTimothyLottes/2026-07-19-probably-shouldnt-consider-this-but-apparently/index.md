---
title: "Probably shouldn't consider this -BUT- apparently writing to ax doesn't change the other 48-bits."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2078728600912630031"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2078728600912630031"
date: 2026-07-19
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Probably shouldn't consider this -BUT- apparently writing to ax doesn't change the other 48-bits."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2078728600912630031
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-19 06:28:14

## Thread

**1/** **@NOTimothyLottes** ^2078728600912630031

Probably shouldn't consider this -BUT- apparently writing to ax doesn't change the other 48-bits. So one could do a 4-byte overhead interpreter with a 64KiB aligned window of directly jumpable words like this below. [rsi]=addresses to jump to. You'd pay the false dependency stall

![](https://pbs.twimg.com/media/HNkf6ntX0AA8d1M?format=png&name=orig)

**2/** **@NOTimothyLottes** ^2078729020900823089

It's interesting because it cuts interpreted source size in half. Ie a stream of 16-bit offsets instead of 32-bit addresses.

**3/** **@NOTimothyLottes** ^2078729662021111958

The aim of course, keep the stuff that doesn't need to go fast optimized instead for low complexity and low size (aka interpreted forth), and keep the stuff that needs to go fast, at peak, assembly. Hits 2 extremes well.

**4/** **@noop_dev** ^2078763409403683061

**@NOTimothyLottes**

These instrs are anything but fast and if you want both "fast" and compact you run a separate decoding pass where you expand custom bytecode into target instructions that suck less.

**5/** **@NOTimothyLottes** ^2078851948543910353

**@noop_dev**

Basic truth: if the program is tiny and dependency free (ie intrinsically not just glue for libraries) it’s probably already fast even if the machine isn’t. And for the things that need perf there is always assembly

**6/** **@noop_dev** ^2078853226967781591

**@NOTimothyLottes**

Anyway, I am trying you to sell the idea of bytecode-driven macroassembler that expands "macros" on load. Like I did with 4K atari 2600 emu ~20 years ago.. some demosceners I knew also adopted the idea..

**7/** **@NOTimothyLottes** ^2078856306811691388

**@noop_dev**

Many of my other systems had been such that interpreted source generates raw code then executes the code (all at once after code is fully processed). Effectively forth as a macro language and instruction generator, runtime assembler.

**8/** **@NOTimothyLottes** ^2078858446409978111

**@noop_dev**

But for cold cache stuff it’s easy to burn more time in binary generation than it would cost to do simple interpreter.

**9/** **@noop_dev** ^2078860015323038149

**@NOTimothyLottes**

Not sure I can understand how cold cache matters for a linear transformation of a relatively small # of bytes.

**10/** **@NOTimothyLottes** ^2078861504284074431

**@noop_dev**

If it’s a byte that indexes into say a fixed size physical instruction, yeah it’s just a decompression of source code, sure easy to do fast. Im talking more the multi-branch miss per instruction stuff.

**11/** **@NOTimothyLottes** ^2078862606517895324

**@noop_dev**

Meaning “mov edi,[rax-0x32]” could be generated from 4 symbol lookups (2 for regs, one for offset, one for instruction). Also my intent here is for GPU code generation for AMD GPUs where youd have sometimes 8+ bitfields in an opcode. So the simple stuff won’t work there …
