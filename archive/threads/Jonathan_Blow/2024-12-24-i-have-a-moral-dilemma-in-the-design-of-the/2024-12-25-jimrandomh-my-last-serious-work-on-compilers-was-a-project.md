---
title: "(My last serious work on compilers was a project course way back in 2008, where we got as far as doing a few basic optimizations on SSA, allocating registers and doing instruction tiling for x86."
type: archive
source: twitter
source_url: "https://x.com/jimrandomh/status/1871747884145901610"
author: "Jim Babcock"
handle: jimrandomh
post_id: "1871747884145901610"
date: 2024-12-25
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "(My last serious work on compilers was a project course way back in 2008, where we got as far as doing a few basic optimizations on SSA, allocating registers and doing instruction tiling for x86."
in_reply_to: ""
parent_post_id: "1871638900554317934"
---

## Source

- URL: https://x.com/jimrandomh/status/1871747884145901610
- Author: Jim Babcock (@jimrandomh)
- Posted: 2024-12-25 02:40:45

## Branch

**1/** **@jimrandomh** ^1871747884145901610

(My last serious work on compilers was a project course way back in 2008, where we got as far as doing a few basic optimizations on SSA, allocating registers and doing instruction tiling for x86. So, take this with a grain of salt.)
What I was taught at the time was that, if you want good instruction selection, you're pretty much forced into techniques where you take the available-instruction-set as data.
(In the version I was taught, you have a graph-like representation of each EBB, you have an ISA-specific set of available instruction tiles with cost annotations, you find a covering of your EBB with the tiles, and that's your instruction selection. This is the step where compilers squeeze their memory operations and load-immediates into addressing modes.)
Instruction tiles and instructions aren't exactly the same thing, but they're similar enough that they can probably share tables and a subset of table fields. And as development continues, you'll probably come across assembler-adjacent tasks that you might not have spotted yet. Eg: working with source maps; estimating the execution cost of assembly snippets; handling CPU feature flags.
You'll also have to deal with middle stages of the compiler wanting to know the answers to awkward questions about how much a function costs to call vs to inline, whether a particular loop is worth vectorizing, etc, where the true answer depends on a model of instruction cost.
All of that said... if I were the one writing this compiler, and I also wanted to ship software with it, I would *dream* of getting rid of LLVM, but *plan* on being stuck with it forever, at least for release builds.

## Related

- Spine: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the]]
