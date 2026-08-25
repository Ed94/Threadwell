---
title: "A good way to evaluate one axis of quality of an abstraction is to inline every function call, and see how much duplicate work you can either deduplicate or turn into a loop (rather than several independent function calls)."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/2085786822387609939"
author: "Ryan Fleury"
handle: rfleury
post_id: "2085786822387609939"
date: 2026-08-07
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "A good way to evaluate one axis of quality of an abstraction is to inline every function call, and see how much duplicate work you can either deduplicate or turn into a loop (rather than several independent function calls)."
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/2085786822387609939
- Author: Ryan Fleury (@rfleury)
- Posted: 2026-08-07 17:55:05

## Thread

**1/** @rfleury

A good way to evaluate one axis of quality of an abstraction is to inline every function call, and see how much duplicate work you can either deduplicate or turn into a loop (rather than several independent function calls). This also restructures the code such that you can consider work as batches of identically shaped work, rather than either (a) being in shallow callstack code and dealing with a list of abstract, opaque function calls, or (b) being in deep callstack code and not understanding the context you're being called within.

Branches: [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-07-JaceCear-if-you-got-a-concrete-example-of-this-it-might-be]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-07-tralamazza-couldnt-resist]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-07-davidvaughn006-this-seems-like-such-good-advice-and-hard-to]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-07-adam_bobowski-overall-ive-noticed-that-inlining-is-just-amazing]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-07-sandovin34721-btw-this-sounds-like-a-nice-feature-for-a]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-07-borrowck_novel-assuming-o3-if-you-compare-the-assembly-output]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-07-calvinalkan-do-you-have-a-favorite-example-from-raddbg-to]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-07-zygohistoprepro-i-did-this-process-to-linearise-the-mutually]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-07-jsuarez-this-is-the-first-thing-i-do-in-every-big-refactor]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-08-patrickgwsmith-some-people-will-say-that-a-good-abstraction-lets]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-08-TylerCLaprade-john-carmack-wrote-about-this-http-number-none]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-08-rep_movsd-the-fundamental-property-of-abstraction-is-to]], [[archive/threads/rfleury/2026-08-07-a-good-way-to-evaluate-one-axis-of-quality-of-an/2026-08-09-dvygh-makes-me-wonder-why-we-dont-have-a-tool-do-we-to]]

**2/** @niftynathanj

@rfleury

distance from main sequence
