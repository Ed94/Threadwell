---
title: "I was and still am a big proponent of address registers for GPU ISAs."
type: archive
source: twitter
source_url: "https://x.com/CUDAHandbook/status/2095988395440791875"
author: "Nicholas Wilt"
handle: CUDAHandbook
post_id: "2095988395440791875"
date: 2026-09-04
archived: 2026-11-16
draft: false
tags:
  - archive
  - twitter
  - CUDAHandbook
description: "I was and still am a big proponent of address registers for GPU ISAs."
in_reply_to: ""
---

## Source

- URL: https://x.com/CUDAHandbook/status/2095988395440791875
- Author: Nicholas Wilt (@CUDAHandbook)
- Posted: 2026-09-04 21:32:29

## Thread

**1/** **@CUDAHandbook** ^2095988395440791875

I was and still am a big proponent of address registers for GPU ISAs. Put them in a special RAM, size with the virtual address width, opcodes for address operands mean you can fetch concurrently with the data registers participating.. fewer instructions both static and dynamic.

**2/** **@NOTimothyLottes** ^2096012267162571176

**@CUDAHandbook**

for my FPGA stuff,
a.) opcode bit:store IMAD result to address reg
b.) XOR based immediate offsets, instead of ADD, no carry chain
c.) 4-bit nibble granularity addressing
d.) Automatic bitfield extraction based on MSBs of address (window gives size)
e.) prefetch on adr reg change

Branches: [[archive/threads/CUDAHandbook/2026-09-04-i-was-and-still-am-a-big-proponent-of-address/2026-09-05-CUDAHandbook-at-the-instruction-level-i-think-both-memory]]
