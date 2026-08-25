---
title: "All {0-6} argument syscall options in 32-bytes."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2078347557474849137"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2078347557474849137"
date: 2026-07-18
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "All {0-6} argument syscall options in 32-bytes."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2078347557474849137
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-18 05:14:06

## Thread

**1/**

All {0-6} argument syscall options in 32-bytes. The plan is to embed the interpreter inside the words with a 3-byte overhead {AD (lodsd), FF E0 (jmp rax)} so levering lots of x86-64 stuff for minimal size

![](https://pbs.twimg.com/media/HNfFmXoXkAAMHM9?format=png&name=orig)

**2/**

Everything forced in lower 32-bit, but still building around 64-bit support. Since I'm not using x86-64 CALL/RET I can free up the stack ops strictly for the data stack.

![](https://pbs.twimg.com/media/HNfGRZvXEAEtaKH?format=png&name=orig)

**3/**

I realized at some point I can have most interpreted forth-style words in an aligned 8-bytes. So can make a very small interpreter.

![](https://pbs.twimg.com/media/HNfHl-dXcAAf6Om?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2026-07-18-all-0-6-argument-syscall-options-in-32-bytes/2026-07-18-noop_dev-even-smaller-code-size-possible-with-custom]]
