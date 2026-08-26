---
title: "LLVM does what you want, you just need to learn what the MC layer is all about."
type: archive
source: twitter
source_url: "https://x.com/clattner_llvm/status/1872213611076276706"
author: "Chris Lattner"
handle: clattner_llvm
post_id: "1872213611076276706"
date: 2024-12-26
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "LLVM does what you want, you just need to learn what the MC layer is all about."
in_reply_to: ""
parent_post_id: "1871638900554317934"
---

## Source

- URL: https://x.com/clattner_llvm/status/1872213611076276706
- Author: Chris Lattner (@clattner_llvm)
- Posted: 2024-12-26 09:31:23

## Branch

**1/** **@clattner_llvm** ^1872213611076276706

LLVM does what you want, you just need to learn what the MC layer is all about. Solved years ago for those in the know.

LLVM’s mid-level optimizations are not great for many reasons (see mojo talks at the llvm dev meetings) but it’s codegen is unmatched, particularly when you get to the vagaries of SIMD, ai instructions and all the other things that unlock the flops on modern cpus.

Lots of people observe (correctly) that llvm is annoying and imagine the fun part of building a code generator, only to forget the actually hard part.

**2/** **@Jonathan_Blow** ^1872381307587592486

As I mentioned somewhere in that giant wall of text, we just can't take on LLVM as a core dependency because it is too big and cumbersome and slow at compiling. This is mostly not your fault, much of it happened more recently, but it is what it is.

We already have a code generator for x86, it just doesn't do the hard part yet. Yay.

**3/** **@lmcanavals** ^1872396117855650223

**@Jonathan_Blow** **@clattner_llvm** **@rflaherty71**

Aw, man I got my hopes up for an epic cross over

## Related

- Spine: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the]]
