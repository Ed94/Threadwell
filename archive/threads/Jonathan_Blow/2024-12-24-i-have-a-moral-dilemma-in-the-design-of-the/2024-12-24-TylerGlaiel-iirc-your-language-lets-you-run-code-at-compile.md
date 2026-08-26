---
title: "IIRC your language lets you run code at compile time as part of the compiling process so why not have the assembler be at that level instead of in the compiler itself and let the compile time code gen be able to output machine code directly & let the assembly instructions be part of the standard library for each specific platform instead?"
type: archive
source: twitter
source_url: "https://x.com/TylerGlaiel/status/1871642886464516129"
author: "Tyler Glaiel"
handle: TylerGlaiel
post_id: "1871642886464516129"
date: 2024-12-24
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "IIRC your language lets you run code at compile time as part of the compiling process so why not have the assembler be at that level instead of in the compiler itself and let the compile time code gen be able to output machine code directly & let the assembly instructions be part of the standard library for each specific platform instead?"
in_reply_to: ""
parent_post_id: "1871638900554317934"
---

## Source

- URL: https://x.com/TylerGlaiel/status/1871642886464516129
- Author: Tyler Glaiel (@TylerGlaiel)
- Posted: 2024-12-24 19:43:32

## Branch

**1/** **@TylerGlaiel** ^1871642886464516129

IIRC your language lets you run code at compile time as part of the compiling process so why not have the assembler be at that level instead of in the compiler itself and let the compile time code gen be able to output machine code directly & let the assembly instructions be part of the standard library for each specific platform instead?

fwiw while I've used intrinsics in C++ at least a little bit here and there, I can't remember the last time I actually needed inline asm, so a "this is a very optional thing that you bring in if you actually need it" seems like the most appropriate design to me

**2/** **@Jonathan_Blow** ^1871643831869026346

**@TylerGlaiel** **@rflaherty71**

That's what I am talking about at the beginning when I said "put the assembler in userspace" -- it would be code in the language itself rather than internally to the compiler. But we are not going to generate our *own* exe that way because it's slow and indirect.

## Related

- Spine: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the]]
