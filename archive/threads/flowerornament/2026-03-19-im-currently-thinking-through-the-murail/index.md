---
title: "I'm currently thinking through the Murail \"programming language\"—and it's a weird one."
type: archive
source: twitter
source_url: "https://x.com/flowerornament/status/2034584048606273988"
author: "Flower"
handle: flowerornament
post_id: "2034584048606273988"
date: 2026-03-19
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - flowerornament
description: "I'm currently thinking through the Murail \"programming language\"—and it's a weird one."
in_reply_to: ""
---

## Source

- URL: https://x.com/flowerornament/status/2034584048606273988
- Author: Flower (@flowerornament)
- Posted: 2026-03-19 10:53:32

## Thread

**1/** **@flowerornament** ^2034584048606273988

I'm currently thinking through the Murail "programming language"—and it's a weird one.

"Named sparse recurrence" is what it calls itself. Let's unpack that:

Named
A Murail program is simply a set of named equations.

Programs are a lot like writing math, which its intended users are familiar with:

osc.phase = self@1 + freq / sr
osc.out = sin(osc.phase * 2 * pi)

This is a program for a sinusoidal oscillator. It defines two nodes in a graph.

Compared to a normal programming language, this is a bit like defining a function, but Murail is neither imperative nor functional, so functions are never explicitly "called."

A named equation is instantly running as soon as it's written. There's no "on" or "off". In this way, it's a bit like a circuit. If you wanted to turn a function off, you'd have to write a switch after it.

This may seem very limited and unfamiliar, but it's a lot like the most popular programming language in the world: spreadsheets.

It's also very much like Max/MSP, and you can think of Murail as something like Max/MSP, but more general. Instead of "signals" and "control," nodes are connected by streams of matrices, which can flow at any rate. If the rate is fast—like, audio rate—they get automatically prioritized and run fast like optimized C code.

On top of this simple scheme, we layer some concepts for abstraction. This is what I'm working on now. There are "templates" you can use to group equations, simple pattern matching, constructions for branching, a "do" keyword for pseudo-imperative stuff, and more.

But this is all syntax sugar over named equations.

Sparse
Murail programs are, basically, graphs. You write equations, but those equations are automatically connected together. The thing that tells the compiler which things to connect to which other things is mediated by the names.

So, the above oscillator example actually turns into something like:

[osc.phase] -> [osc.out]

But the crazy part is that this compiles to a matrix operation. In "BSM" form, something like:

[y]      [2π  2π] [ω]
[φ] = [  1     1  ] [φ] + sin(y)

So, "sparse" refers to the fact that what we're really defining is a huge set of matrices related by a sparse matrix, which defines the connections between them.

Recurrence
This matrix is evaluated "in time." In a normal programming language, you don't think about time specifically—or if you do, it's a choice. Normally, you just want everything to execute as fast as possible.

In Murail, everything is executed together at a specific rate. If you're doing audio, then it's something like 48khz.

But the graph aka matrix is executed over a "rate lattice," which means different parts of the graph are executed at divisions of the fastest rate.

On top of this, "now" is variable. You can alway write `self@1`, which refers to the current value, but one step in the past.

In this sense, Murail is a "strongly timed" language. You cannot do anything without explicitly or implicitly defining how often it happens per second.

Design
The hard part of a language like this is getting it to also do things people are used to doing in a programming language.

I'm not actually sure if Murail is Turing complete—but what's more important is that it's decidedly *not* lambda calculus.

As such, it's been an interesting exercise to find out how exactly to provide the right set of features such that you can fluently write DSP code that looks like math, but also do more "sequential" things like write a sequencer, or an HTTP server, or load a file.

It turns out you can do a lot more of this than I thought at first, and quite elegantly. The primitives are just different.

In fact, they're not *that* weird. They're just more like what you find in a language like APL (or J, or K).

branch, fold, scan, select, match

If you're used to Max/MSP, you'll be familiar with this type of stuff. Strangely named operations that split, combine, interleave, and shape streams of data.

The concept of "externals" from Max/MSP is also essential here for certain things. In Urbit or PLAN, they're called "jets."

Ultimately, you can't get around the fact that the rest of your computer isn't inside the graph itself. As such, the runtime needs to provide certain special functions that do things like read files or take input from the external world and inject them into equations.

We'll have to wait for the PLAN computer for a world where your OS is just one uniform substrate interacting with itself. But, even there, you need some systems code at the edge.

That's probably enough for one post. Perhaps more to come.

Branches: [[archive/threads/flowerornament/2026-03-19-im-currently-thinking-through-the-murail/2026-03-19-hastuc_dibtux-fwiw-youre-speed-running-shader-dev-in-modern-aaa]], [[archive/threads/flowerornament/2026-03-19-im-currently-thinking-through-the-murail/2026-03-19-renart973-you-may-want-to-reach-pedro-domingos-in-case-you]], [[archive/threads/flowerornament/2026-03-19-im-currently-thinking-through-the-murail/2026-04-05-eshear-the-more-i-read-about-murail-the-more-i-would]]
