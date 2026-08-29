---
title: "Imagine language that has NO {stack, calls, returns, conditional branches, explicit jumps, functions with arguments and returns}"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1985584015290913044"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1985584015290913044"
date: 2025-11-04
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Imagine language that has NO {stack, calls, returns, conditional branches, explicit jumps, functions with arguments and returns}"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1985584015290913044
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-11-04 05:44:54

## Thread

**1/** **@NOTimothyLottes** ^1985584015290913044

Imagine language that has NO {stack, calls, returns, conditional branches, explicit jumps, functions with arguments and returns}

Instead has argument-and-return-free subroutines and an array of sub addresses to call. So it's self-modification of that array to control execution

![](https://pbs.twimg.com/media/G44098XWcAAy4hT?format=png&name=orig)

**2/** **@NOTimothyLottes** ^1985584758613483634

Idea repurposes the x86-64 stack to only POP to read off the next subroutine, and each subroutine jumps to the next. If one wants to repeat something N times, it gets inserted in the 'tape' array N times.

**3/** **@NOTimothyLottes** ^1985585233031209262

While it is a jmp by register, the register value is known long in advance, but not sure if current x86-64 chips can use actual register values if available soon enough and ignore possible incorrect branch prediction.
