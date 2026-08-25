---
title: "How about removing {call,return,branch,conditional-branch}."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2033376425760215474"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2033376425760215474"
date: 2026-03-16
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "How about removing {call,return,branch,conditional-branch}."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2033376425760215474
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-03-16 02:54:52

## Thread

**1/** **@NOTimothyLottes** ^2033376425760215474

How about removing {call,return,branch,conditional-branch}. Replacing with keeping code in lower 32-bit, then,
(1.) REG=Fetch 32-bit and advance
..do work..
(2.) Branch to REG
Loops=repeat address
Big loops=hierarchical
Conditional=change addresses
Self-modifying data (vs code)

Branches: [[archive/threads/NOTimothyLottes/2026-03-16-how-about-removing-call-return-branch-conditional/2026-03-16-mbur82-on-x86-the-mov-instruction-is-turing-complete]]

**2/** **@NOTimothyLottes** ^2033377244123472291

Effectively you layout a linear array of the address of subroutines to call. And each subroutine advances the read pointer. Can adapt at runtime to do new stuff by writing addresses of what to do, and modify addresses for conditional execution. Easy to make portable.

**3/** **@NOTimothyLottes** ^2033379760768705013

*Forth (and others) way of de-conditionalizing loops is to say do a computed branch to skip into a stream of calls. But that is horrible for the CPUs that exist. Moving from streams of physical call opcodes, to addresses actually fixes that problem quite nicely.

**4/** **@NOTimothyLottes** ^2033381450859319628

The other thing here is this, if you are doing something that is effectively a portable assembly level thing, one of the huge differences across ISAs is {calls,conditional branch relative immediate offset sizes, etc}, so this thread's construct removes all that crap.
