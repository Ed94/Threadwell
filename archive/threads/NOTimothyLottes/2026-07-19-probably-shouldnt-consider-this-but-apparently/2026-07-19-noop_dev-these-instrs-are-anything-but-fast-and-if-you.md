---
title: "@NOTimothyLottes These instrs are anything but fast and if you want both \"fast\" and compact you run a separate decoding pass where you expand custom bytecode into target instructions that suck less."
type: archive
source: twitter
source_url: "https://x.com/noop_dev/status/2078763409403683061"
author: "Boris Chuprin"
handle: noop_dev
post_id: "2078763409403683061"
date: 2026-07-19
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes These instrs are anything but fast and if you want both \"fast\" and compact you run a separate decoding pass where you expand custom bytecode into target instructions that suck less."
in_reply_to: ""
parent_post_id: "2078729662021111958"
---

## Source

- URL: https://x.com/noop_dev/status/2078763409403683061
- Author: Boris Chuprin (@noop_dev)
- Posted: 2026-07-19 08:46:33

## Branch

**1/** **@noop_dev** ^2078763409403683061

**@NOTimothyLottes**

These instrs are anything but fast and if you want both "fast" and compact you run a separate decoding pass where you expand custom bytecode into target instructions that suck less.

**2/** **@NOTimothyLottes** ^2078851948543910353

**@noop_dev**

Basic truth: if the program is tiny and dependency free (ie intrinsically not just glue for libraries) it’s probably already fast even if the machine isn’t. And for the things that need perf there is always assembly

**3/** **@noop_dev** ^2078853226967781591

**@NOTimothyLottes**

Anyway, I am trying you to sell the idea of bytecode-driven macroassembler that expands "macros" on load. Like I did with 4K atari 2600 emu ~20 years ago.. some demosceners I knew also adopted the idea..

**4/** **@NOTimothyLottes** ^2078856306811691388

**@noop_dev**

Many of my other systems had been such that interpreted source generates raw code then executes the code (all at once after code is fully processed). Effectively forth as a macro language and instruction generator, runtime assembler.

**5/** **@NOTimothyLottes** ^2078858446409978111

**@noop_dev**

But for cold cache stuff it’s easy to burn more time in binary generation than it would cost to do simple interpreter.

**6/** **@noop_dev** ^2078860015323038149

**@NOTimothyLottes**

Not sure I can understand how cold cache matters for a linear transformation of a relatively small # of bytes.

**7/** **@NOTimothyLottes** ^2078861504284074431

**@noop_dev**

If it’s a byte that indexes into say a fixed size physical instruction, yeah it’s just a decompression of source code, sure easy to do fast. Im talking more the multi-branch miss per instruction stuff.

**8/** **@NOTimothyLottes** ^2078862606517895324

**@noop_dev**

Meaning “mov edi,[rax-0x32]” could be generated from 4 symbol lookups (2 for regs, one for offset, one for instruction). Also my intent here is for GPU code generation for AMD GPUs where youd have sometimes 8+ bitfields in an opcode. So the simple stuff won’t work there …

## Related

- Spine: [[archive/threads/NOTimothyLottes/2026-07-19-probably-shouldnt-consider-this-but-apparently]]
