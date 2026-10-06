---
title: "Evening project - building a spiritual successor language to what could pass as a replacement for C64 boot BASIC boot but on a x86-64 machine ..."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2099688997194711371"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2099688997194711371"
date: 2026-09-15
archived: 2026-09-15
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Evening project - building a spiritual successor language to what could pass as a replacement for C64 boot BASIC boot but on a x86-64 machine ..."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2099688997194711371
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-09-15 02:37:21

## Thread

**1/** **@NOTimothyLottes** ^2099688997194711371

Evening project - building a spiritual successor language to what could pass as a replacement for C64 boot BASIC boot but on a x86-64 machine ...

**2/** **@NOTimothyLottes** ^2099690063755870582

Constraints
(1.) Must directly interpret from ascii txt
(2.) Must be tiny, core language fits in a few hundred bytes [fraction of I$]
(3.) Sticking with similar double character max string size for 'variable' name
(4.) But swapping BASIC for something FORTH like instead

**3/** **@NOTimothyLottes** ^2099690978298786054

I'm using 128-bytes for ascii reordering (so 0-F is 0-F, etc). Doing a byte[128] sized lookup for the interpreter which gets converted to a jump table for 7-bit characters. So each character is a branch, and likely some get predicted (like when using hex literals).

**4/** **@NOTimothyLottes** ^2099691470043103730

Yet this language is actually a serious effort, something trivial to understand, and powerful enough to use for system level scripting (doing syscalls) and function as a macro assembler for CPU+GPU code. Also something fast enough to be effectively free for iteration-time

**5/** **@NOTimothyLottes** ^2099692261399248990

I've got a crazy useful system for comments,
ThisPartIsIgnored_gg
The _ clears the string (prefix comment)
The 'gg' is the physical index to the dictionary entry
So it's possible to comment all the abbreviations

**6/** **@NOTimothyLottes** ^2099693204312404281

Tooling is just writing it out in binary form.
I use https://defuse.ca/online-x86-assembler.htm#disassembly to grab disassembly bytes to write into a hex stream. And https://ref.x86asm.net/coder64.html for x86-64 opcode reference.

**7/** **@NOTimothyLottes** ^2099693914085016007

Probably going to merge this into my prior effort for a Linux self modifying binary, as it's language. Then just need to build out the in-binary editor for a complete working dev platform for Linux x86-64 that fits in a few KiB.

**8/** **@NOTimothyLottes** ^2099694772260675908

The x86-64 self modifying binary shell with not the smallest ELF header is currently clocked in at 290 bytes. So yeah not joking, a full hardcore Linux dev env in a few KiB (language, editor, debugger).

**9/** **@NOTimothyLottes** ^2099695168253284559

The irony being this would be portable, no library support, everything in raw system calls. So will need to roll over my prior user-space AMD compute GPU driver as well.
