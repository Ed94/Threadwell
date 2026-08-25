---
title: "To the degree this is true, it’s only in a technical sense."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1917431895786414425"
author: "Ryan Fleury"
handle: rfleury
post_id: "1917431895786414425"
date: 2025-04-30
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "To the degree this is true, it’s only in a technical sense."
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/1917431895786414425
- Author: Ryan Fleury (@rfleury)
- Posted: 2025-04-30 04:12:42

## Thread

**1/** **@rfleury** ^1917431895786414425

To the degree this is true, it’s only in a technical sense. When you actually force yourself to inline all of the extra nonsense that is implicitly happening in modern C++ codebases, it quickly becomes obvious that something is wrong, and it’s an enormously subpar solution.

Yes, if you had handwritten all of the heap allocations, reference counts, checks, and lifetime management by hand in regular C, then you’d just be doing exactly what std::unique_ptr is doing, and this allows them to sell it as “zero cost”.

The difference is that when you strip all that extra stuff away, you are in an enormously better position to design much simpler memory allocation solutions that conform much better to the reality of your problem. As a consequence, your final solution does, in fact, have dramatically fewer heap allocations, many fewer computations, and there is simply a lot less going on—it’s a much more transparent system to you.

Not to mention the fact that your compile times become way faster, all of your data structures are much simpler, and they’re much more easily inspected in the debugger.

Branches: [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-04-30-AnthonyPatch15-saw-a-casey-muratori-video-about-people-who-think]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-04-30-shwadev78-also-people-will-say-this-garbage-and-then-show]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-04-30-MoveZig4-this-isnt-such-a-strong-argument-considering]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-04-30-KirillKiriche11-i-miss-the-point-you-are-trying-to-make]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-04-30-DomWitczak-there-is-exactly-zero-pain-in-debugging-unique]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-04-30-anilcanglk12-i-bet-std-comitee-wrote-thousands-of-lines-for]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-04-30-mikejt4-my-experience-has-been-different-every-piece-of-c]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-04-30-Wouter_Bijlsma-generated-assembly-or-other-supposedly-better]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-04-30-Pps831-too-much-words-but-unique-ptr-is-really-zero-cost]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-04-30-eclectocrat-id-use-c-more-if-attribute-cleanup-was-standard]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-05-01-slendidev-do-you-have-any-example-of-this]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-05-01-wmcoyne-well-said-zero-overhead-in-the-abstract-isnt-the]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-05-01-AbstrctMachnist-individual-malloc-free-is-a-common-c-practice-and]], [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a/2025-05-01-RokCej-look-at-any-large-codebase-and-youll-see-a-bunch]]

**2/** **@SubstrataVr** ^1917436352578347222

**@rfleury**

I think you may be thinking of shared_ptr, which does reference counting.  unique_ptr doesn't need to.

**3/** **@rfleury** ^1917436636163706994

**@SubstrataVr**

You’re right about the reference counts, my mistake. The other points still stand however.

**4/** **@static_assert_0** ^1917583100604813710

**@rfleury** **@SubstrataVr**

In general maybe, but I don’t really see how any of this stands for unique_ptr - it literally is just a struct around a pointer with a deleted copy constructor to give you a compile error when you try to share it?

Now the debugger argument that this adds extra noise is valid

**5/** **@rfleury** ^1917586421050925263

**@static_assert_0** **@SubstrataVr**

I wear certainly conflating the two (I do not use these features) but the argument stands, given that the places where you actually have “owned pointers” should be extremely small. This is seen as useful when you have 1000s of these. But you shouldn’t.

**6/** **@AbstrctMachnist** ^1917756459321786491

**@rfleury** **@static_assert_0** **@SubstrataVr**

I think this is a perspective difference between game developers, who have natural shared memory lifetimes in the form of frames, data batches, or update ticks, and general purpose developers where it's normal to have many operations in-flight with no common enclosing lifetime.

**7/** **@rfleury** ^1917776947574366253

**@AbstrctMachnist** **@static_assert_0** **@SubstrataVr**

This is not true. There are lifetimes all over the place in all fields. Everyone just lumps me into “game developers”, but I don’t even work on games professionally? How does your theory account for that? Do you think group lifetimes are somehow unique to games?
