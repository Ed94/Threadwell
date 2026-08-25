---
title: "One of the most powerful lessons I learned as a programmer was to use combinatoric spaces to my advantage, rather than allowing them to explode into—for example—handwritten source code."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1869409243251827152"
author: "Ryan Fleury"
handle: rfleury
post_id: "1869409243251827152"
date: 2024-12-18
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "One of the most powerful lessons I learned as a programmer was to use combinatoric spaces to my advantage, rather than allowing them to explode into—for example—handwritten source code."
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/1869409243251827152
- Author: Ryan Fleury (@rfleury)
- Posted: 2024-12-18 15:47:50

## Thread

**1/** **@rfleury** ^1869409243251827152

One of the most powerful lessons I learned as a programmer was to use combinatoric spaces to my advantage, rather than allowing them to explode into—for example—handwritten source code. This required relaxing, for example, an obsession with static type checking.

Branches: [[archive/threads/rfleury/2024-12-18-one-of-the-most-powerful-lessons-i-learned-as-a/2024-12-18-TriggerCoder-unroll]], [[archive/threads/rfleury/2024-12-18-one-of-the-most-powerful-lessons-i-learned-as-a/2024-12-18-SubstrataVr-example]], [[archive/threads/rfleury/2024-12-18-one-of-the-most-powerful-lessons-i-learned-as-a/2024-12-18-pr0meteu5-any-concrete-example]], [[archive/threads/rfleury/2024-12-18-one-of-the-most-powerful-lessons-i-learned-as-a/2024-12-18-spacebat-this-reminds-me-of-games-and-simulations-where]], [[archive/threads/rfleury/2024-12-18-one-of-the-most-powerful-lessons-i-learned-as-a/2024-12-19-Walley_Alex1-i-completely-agree-i-am-interested-in-your]], [[archive/threads/rfleury/2024-12-18-one-of-the-most-powerful-lessons-i-learned-as-a/2024-12-20-wetfsdffsdasd-interesting-projection-of-combinatorics-system]], [[archive/threads/rfleury/2024-12-18-one-of-the-most-powerful-lessons-i-learned-as-a/2025-01-24-s0ulware-thank-you-for-this-thread-read-it-a-while-ago-but]]

**2/** **@rfleury** ^1869409245067882985

Instead what I learned was to use static product types to form homogeneous building blocks for large combinatoric spaces, and to organize data transforms around forming those spaces. Choosing actual points in this space becomes a completely dynamic capability.

**3/** **@rfleury** ^1869410549592989761

This is related to my comment the other day on sum types. The reason you won’t find many of them in my code is that I find that they leak combinatoric spaces into the source code itself, by forming one “axis” (1 of N types), which might be multiplied by another. That puts it in the path of non-temporal physical reality—physical code—which must either be handwritten or generated. This is either slow for the programmer, or for the computer.

**4/** **@rfleury** ^1869411240227016733

Whereas if you keep the source code looser, with homogeneous types, you can allow defining points & transitioning between points in the combinatoric space to be much more natural & trivial of a computation. In practice this means you’ve turned an O(N*M*…) into an O(N+M+…), for either yourself or the compiler, or code generator (all three are good).

**5/** **@rfleury** ^1869413198081994912

The fundamental reason for this is machine code, being representable by a transform from A -> B (where A and B are definitions of data formats, or types), must have a shape which expects/fits A as the input, and expects/fits B as the output. A|C -> B means you must have two paths: A -> B | C -> B. This suggests that, as the number of types grows, the number of codepaths must also grow. Or, put another way, the structure of types is reflected in the source code which uses those types.

**6/** **@rfleury** ^1869413521529966610

You can often see this concretely in C - a discriminated `union` implies a `switch` (or some other branching mechanism on the tag). An array can imply a loop over the indices. A linked list can imply a loop over the links. And so on.

**7/** **@rfleury** ^1869414204496871475

Thus, when someone attempts to take static type checking to the extreme, and maximally fit all potential data payloads into a format which only stores data which those payloads use (e.g. no unused fields in any case), they are not only exploding the number of types, they are also exploding the number of codepaths.

When confronted with this reality, one impulse is to force compilers or other generators to iterate the combinatoric space manually; this is perhaps preferable to doing it by hand, but what's preferable over both options is to simply avoid the combinatoric space being present in this domain at all.

**8/** **@rfleury** ^1869414867113009626

This makes distinctions in combinatoric spaces a very trivial data problem, rather than an arbitrarily difficult code problem. It makes the code small, yet the set of possible effects from the code large.

Branches: [[archive/threads/rfleury/2024-12-18-one-of-the-most-powerful-lessons-i-learned-as-a/2024-12-18-count_mascetti-maybe-you-already-wrote-this-somewhere-but-id-be]], [[archive/threads/rfleury/2024-12-18-one-of-the-most-powerful-lessons-i-learned-as-a/2024-12-18-cairnc1-at-what-point-do-you-think-you-should-convert-a]]
