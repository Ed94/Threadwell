---
title: "@Jonathan_Blow @rflaherty71 Suggestion: focus on compile speed and small size, aka simple code generation (easy to maintain), but not necessarily runtime performance optimal."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1871645705070330266"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1871645705070330266"
date: 2024-12-24
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "@Jonathan_Blow @rflaherty71 Suggestion: focus on compile speed and small size, aka simple code generation (easy to maintain), but not necessarily runtime performance optimal."
in_reply_to: ""
parent_post_id: "1871638900554317934"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1871645705070330266
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-12-24 19:54:44

## Branch

**1/** **@NOTimothyLottes** ^1871645705070330266

**@Jonathan_Blow** **@rflaherty71**

Suggestion: focus on compile speed and small size, aka simple code generation (easy to maintain), but not necessarily runtime performance optimal. Then lean more on inline asm or intrinsic guided stuff for perf critical.

**2/** **@NOTimothyLottes** ^1871646191253152078

**@Jonathan_Blow** **@rflaherty71**

My last x86-64 compiler wasn't even byte aware in code generation. It used dummy prefix to pad out so all opcodes are 32-bit aligned. It was crazy fast to compile though, and dead simple to maintain. The runtime of compiler was still faster in my language than the same in C.

**3/** **@o__boga** ^1871665809388683564

**@NOTimothyLottes** **@Jonathan_Blow** **@rflaherty71**

Do you have the compiler source available anywhere?

## Related

- Spine: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the]]
