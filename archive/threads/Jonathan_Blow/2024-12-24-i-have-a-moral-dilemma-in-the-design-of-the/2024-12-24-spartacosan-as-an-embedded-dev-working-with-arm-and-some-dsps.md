---
title: "As an embedded dev working with ARM and some DSPs, I vote for keeping the assembler inside the compiler but stripped down."
type: archive
source: twitter
source_url: "https://x.com/spartacosan/status/1871643969660293329"
author: "Mr. Spartaco"
handle: spartacosan
post_id: "1871643969660293329"
date: 2024-12-24
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "As an embedded dev working with ARM and some DSPs, I vote for keeping the assembler inside the compiler but stripped down."
in_reply_to: ""
parent_post_id: "1871638900554317934"
---

## Source

- URL: https://x.com/spartacosan/status/1871643969660293329
- Author: Mr. Spartaco (@spartacosan)
- Posted: 2024-12-24 19:47:50

## Branch

**1/** **@spartacosan** ^1871643969660293329

As an embedded dev working with ARM and some DSPs, I vote for keeping the assembler inside the compiler but stripped down. My assembly use is small - interrupt vectors, context switches, and cache operations (mostly).

SIMD abstraction through assembly or fixed intrinsics is a waste. Better to build a clean IR that expresses vector operations and let your backend pick the implementation. I've seen this work on products where you need to target both Cortex-M and DSP cores.

These days I only drop to assembly for few hardware-specific bits.

## Related

- Spine: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the]]
