---
title: "@Jonathan_Blow @rflaherty71 FWIW I implement SIMD for Dlang."
type: archive
source: twitter
source_url: "https://x.com/auburnsounds/status/1873092710263079401"
author: "Auburn Sounds"
handle: auburnsounds
post_id: "1873092710263079401"
date: 2024-12-28
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "@Jonathan_Blow @rflaherty71 FWIW I implement SIMD for Dlang."
in_reply_to: ""
parent_post_id: "1871638900554317934"
---

## Source

- URL: https://x.com/auburnsounds/status/1873092710263079401
- Author: Auburn Sounds (@auburnsounds)
- Posted: 2024-12-28 19:44:37

## Branch

**1/** **@auburnsounds** ^1873092710263079401

**@Jonathan_Blow** **@rflaherty71**

FWIW I implement SIMD for Dlang. D has inline assembly, but minimal use. inline asm end up almost always slower than intrinsics. The exception to that is LLVM and GCC __asm that can inline in caller, and works in debug mode since no optimize needed. Else intrinsics win.

## Related

- Spine: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the]]
