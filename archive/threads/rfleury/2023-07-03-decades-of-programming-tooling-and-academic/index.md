---
title: "Decades of programming tooling and academic curriculum were built in an entirely different hardware landscape."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1675846329527062531"
author: "Ryan Fleury"
handle: rfleury
post_id: "1675846329527062531"
date: 2023-07-03
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "Decades of programming tooling and academic curriculum were built in an entirely different hardware landscape."
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/1675846329527062531
- Author: Ryan Fleury (@rfleury)
- Posted: 2023-07-03 12:37:55

## Thread

**1/** **@rfleury** ^1675846329527062531

Decades of programming tooling and academic curriculum were built in an entirely different hardware landscape. The hardware has changed, which means everything from an algorithm implementation’s structure, to “micro-optimizations”, to high level abstractions must also change.

**2/** **@rfleury** ^1675846331871670272

Many programmers were taught the myth that a solid abstraction can remain intact while the implementation is adapted to new constraints indefinitely—thus, there is some misconception that tooling and abstraction advice from before can still be somewhat viable.

**3/** **@rfleury** ^1675846333343875072

But this view is mistaken. It ignores how an abstraction’s interface forces constraints on its implementation. These constraints may require a violation of other important constraints. If you want a simpler and faster implementation, a new interface may be necessary.

**4/** **@rfleury** ^1675846335071944705

The future’s competitive toolchains, programming strategies, and academic curricula ought to be rebuilt from the ground up to account for this.

**5/** **@rfleury** ^1675890755351760896

One example is memory management. In 2016, I found @handmade_hero, and I learned that virtually everything I had been taught about managing memory was wrong. With a new mindset and approach, it feels ~as easy in C as in garbage collected languages.

**6/** **@rfleury** ^1675890759793520641

(I wrote about this here: https://www.rfleury.com/p/untangling-lifetimes-the-arena-allocator)

**7/** **@rfleury** ^1675890764235276288

This is one reason I find it worth sticking with languages like C or @odinlang. While C has its own flaws & legacy cruft, and while neither are at the hardware level, by using them you remove decades of nonsense, allowing you to think clearly about problems from first principles.

**8/** **@AgileJebrim** ^1675893653313560577

**@rfleury** **@odinlang**

ISPC needs a lot more attention in my opinion. C, Odin, Zig, etc. don’t even come close in performance because they’re still scalar-based languages when the underlying hardware is actually vector-based.
