---
title: "Just adding that decompilation has \"verifiable rewards\": clang compiles source, AI tries to reverse, ASTs are compared, AI gets training signal."
type: archive
source: twitter
source_url: "https://x.com/DemetriSpanos/status/2104962978030203120"
author: "Demetri Spanos"
handle: DemetriSpanos
post_id: "2104962978030203120"
date: 2026-09-29
archived: 2026-10-06
draft: false
tags:
  - archive
  - twitter
  - DemetriSpanos
description: "Just adding that decompilation has \"verifiable rewards\": clang compiles source, AI tries to reverse, ASTs are compared, AI gets training signal."
in_reply_to: ""
---

## Source

- URL: https://x.com/DemetriSpanos/status/2104962978030203120
- Author: Demetri Spanos (@DemetriSpanos)
- Posted: 2026-09-29 15:54:16

## Thread

**1/** **@DemetriSpanos** ^2104962978030203120

Just adding that decompilation has "verifiable rewards": clang compiles source, AI tries to reverse, ASTs are compared, AI gets training signal.

It's substantially like Go/Chess/Lean, meaning ~free procedural training data: one AI creates and compiles code, another decompiles.

**2/** **@archo5dev** ^2105024366534853044

**@DemetriSpanos**

there are many ways to format the source code that would all produce the same assembly

identifying the algorithms and applying the corresponding variable names can't be verified automatically

that's if we're talking binary to human-level source, not merely any compiling source

**3/** **@DemetriSpanos** ^2105029309584818465

**@archo5dev**

It's true you can't fully recover formatting.

But you can likely recover AST (from training with clang), plausible names, and plausible comments (already seen in e.g. Cursor-style autocompletion).

Readable source that compiles the same way is all you need for AI decompilation.

**4/** **@archo5dev** ^2105035264527610094

**@DemetriSpanos**

even non-LLM decompilers (e.g. dnSpy) can produce good ASTs

but the point of that conversation was about LLM companies taking people's work

so taken together, it would mean using a LLM to decompile a binary and then feeding the "source" into a new LLM

**5/** **@DemetriSpanos** ^2105036711604445420

**@archo5dev**

I think we agree? An AI company could easily train on binaries, through decompilation (even with current conventional decompilers, or with better LLM decompilers), in order to get new source code to train future LLMs, thus absorbing previously semi-hidden information.

**6/** **@archo5dev** ^2105038580800487662

**@DemetriSpanos**

they certainly could try, I'm just not sure how useful that would be for them, and (relatedly) how much human work would need to be involved in cleaning up the decompiled code - especially for algorithms that haven't appeared anywhere else before
