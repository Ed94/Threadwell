---
title: "I think ffmpeg is one of the large & prolific open source projects that maintains huge segments of hand written assembly code, and they maintain separate assembly code for arm (aarch64) and x86."
type: archive
source: twitter
source_url: "https://x.com/hasen_95dx/status/1871744458913710329"
author: "ハセン حسن"
handle: hasen_95dx
post_id: "1871744458913710329"
date: 2024-12-25
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "I think ffmpeg is one of the large & prolific open source projects that maintains huge segments of hand written assembly code, and they maintain separate assembly code for arm (aarch64) and x86."
in_reply_to: ""
parent_post_id: "1871638900554317934"
---

## Source

- URL: https://x.com/hasen_95dx/status/1871744458913710329
- Author: ハセン حسن (@hasen_95dx)
- Posted: 2024-12-25 02:27:08

## Branch

**1/** **@hasen_95dx** ^1871744458913710329

I think ffmpeg is one of the large & prolific open source projects that maintains huge segments of hand written assembly code, and they maintain separate assembly code for arm (aarch64) and x86.

They are so serious about performance, they are willing to take the maintenance burden.

Can there be, in principle, a high level variant of assembly that would satisfy their needs? Doubtful.

How many such project are there? Maybe OS kernels and device drivers, but again, it's doubtful that they would want to use a high level assembly.

There is probably a medium number of projects that would want to write a medium size amount of code in assembly for some critical bottle necks.

For those people, what would serve them better? High level assembly, or builtin support for SIMD?

## Related

- Spine: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the]]
