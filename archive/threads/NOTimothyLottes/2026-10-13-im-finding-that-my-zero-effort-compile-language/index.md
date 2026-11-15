---
title: "I'm finding that my zero effort compile language which is effectively precompiled 32-bit words of binary x86-64 code that get taped together interleaved with flexible 32-bit immediates or rip relative addresses, is converging to something 6502 like."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2109857584937062679"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2109857584937062679"
date: 2026-10-13
archived: 2026-11-14
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "I'm finding that my zero effort compile language which is effectively precompiled 32-bit words of binary x86-64 code that get taped together interleaved with flexible 32-bit immediates or rip relative addresses, is converging to something 6502 like."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2109857584937062679
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-10-13 04:03:42

## Thread

**1/** **@NOTimothyLottes** ^2109857584937062679

I'm finding that my zero effort compile language which is effectively precompiled 32-bit words of binary x86-64 code that get taped together interleaved with flexible 32-bit immediates or rip relative addresses, is converging to something 6502 like.

**2/** **@NOTimothyLottes** ^2109858227764461593

In that I have an accumulator, and 2 other operands, not {X and Y}, but more like {operand, and data stack pointer}. Where a "dictionary" acts like named variable in the zero-page.

**3/** **@NOTimothyLottes** ^2109858871657545805

At the point where a virtual ISA has a tiny opcode bitwidth, it becomes amenable to factoring out code generation. But it also maps a space (tiny opcodes) similar to the constraints the 6502 engineers played in.

**4/** **@NOTimothyLottes** ^2109859256287531455

The domain becomes, instant compile, slightly slower, but still native like performance for a simple virtual ISA, and then ability to go easily directly to the physical machine for anything that needs raw assembly.

**5/** **@NOTimothyLottes** ^2109859799454330995

Taken a few weeks of not working on the project to progress to a point where the syntax of the language is human friendly enough to be easily usable for simultaneous usage as a virtualized language and a powerful macro assembly (for CPU and GPU) at the same time.

Branches: [[archive/threads/NOTimothyLottes/2026-10-13-im-finding-that-my-zero-effort-compile-language/2026-10-13-Colonthreee-this-is-fascinate-is-this-a-bit-like-spir-v]], [[archive/threads/NOTimothyLottes/2026-10-13-im-finding-that-my-zero-effort-compile-language/2026-10-13-leonard_coder-do-you-have-some-source-code-exemple-to-share]]
