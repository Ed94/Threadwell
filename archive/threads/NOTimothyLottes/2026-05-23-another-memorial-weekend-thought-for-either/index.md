---
title: "Another memorial weekend thought: for either "
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2058159498716463375"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2058159498716463375"
date: 2026-05-23
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Another memorial weekend thought: for either "
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2058159498716463375
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-05-23 12:13:57

## Thread

**1/**

Another memorial weekend thought: for either 
(a.) single use code - [majority of slopware]
(b.) cold cache code - [also typical of slopware]
the CPU loading the code is a significant amount of the burned memory bandwidth ...

**2/**

Meaning in C/C++ land where "programmers" (or rather slop-rammers) mostly sniff argument sloshing glue, moving to a scatter instead of gather based language with a single common "call" that just overreads all the register args, would likely be significantly faster ...

**3/**

The analog for the syscall side is to work from a 'tape' pointer read the 7 registers (syscall number in rax, and the 6 max args) always from a linear stream, but advance the read pointer by the number of actual registers used. So the overfetch is just a linear prefetch ...

**4/**

If working with only 32-bit args (see the MAP_32BIT comment), it would be efficient. Add a post-syscall address to call in the common syscall loop, the part that does post-syscall logic like scattering data to future argument read slots (aka the scatter part) ...

**5/**

Now if it was possible to uber-op the post call logic, meaning a fixed logic block that is just data configurable, that call goes away, and it's all probably executing instructions out of the cache (at some level) ...

**6/**

Effectively you'd have an 'initialization language' which is designed to workaround cold execution paths, but with linear CPU prefetch friendly data access for reads, and random scatter for stores (where latency don't matter) ...

**7/**

Most crap-o-grammers today in the user-space C++ bloat-ware domain have not really optimized for performance, rather they optimized for maximum bloat generation. Just add up how much the installed libraries weigh in MiB on a clean OS install.
