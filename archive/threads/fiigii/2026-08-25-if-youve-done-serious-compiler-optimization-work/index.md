---
title: "If you’ve done serious compiler optimization work on a product with a sufficiently large user base, you’ve almost certainly seen bug reports like this:"
type: archive
source: twitter
source_url: "https://x.com/fiigii/status/2092398653797490972"
author: "Fei Peng"
handle: fiigii
post_id: "2092398653797490972"
date: 2026-08-25
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - fiigii
description: "If you’ve done serious compiler optimization work on a product with a sufficiently large user base, you’ve almost certainly seen bug reports like this:"
in_reply_to: ""
---

## Source

- URL: https://x.com/fiigii/status/2092398653797490972
- Author: Fei Peng (@fiigii)
- Posted: 2026-08-25 23:48:08

## Thread

**1/** **@fiigii** ^2092398653797490972

If you’ve done serious compiler optimization work on a product with a sufficiently large user base, you’ve almost certainly seen bug reports like this:

“Why does this code compile into this assembly? There’s an obvious optimization opportunity here. Loop unrolling, LICM, etc. Why didn’t the compiler do it? If it did, my program would be faster. Please change the compiler so my program runs faster.”

Very often, the answer is:

“This isn’t really a compiler bug. It’s a heuristic. The transformation you’re asking for may indeed improve your program, but it could hurt performance in other cases or for other users. A compiler may have thousands or millions of users, and it has to preserve performance across an enormous variety of workloads. We can’t change an optimization policy just to make one program faster."

This answer is 200% correct. I’ve lost count of how many times I’ve given some version of it myself.

And yet, every time I say it, it’s one of the moments when I hate my job the most.

As a user, why should I care about the compiler’s internal heuristics? Why should I care about the performance of everyone else’s programs? Why should I have to pay for something I don’t need?

This needs to change.

Branches: [[archive/threads/fiigii/2026-08-25-if-youve-done-serious-compiler-optimization-work/2026-08-26-btopoweroftwo-llvm-is-flexible-you-can-have-custom-passess-and]], [[archive/threads/fiigii/2026-08-25-if-youve-done-serious-compiler-optimization-work/2026-08-26-FUZxxl-e-graphs-seem-to-be-one-way-to-address-this]], [[archive/threads/fiigii/2026-08-25-if-youve-done-serious-compiler-optimization-work/2026-08-26-pelavarre-this-needs-to-change-we-must-lift-the-rule-that]], [[archive/threads/fiigii/2026-08-25-if-youve-done-serious-compiler-optimization-work/2026-08-26-__dwr__-more-language-tier-facilities-to-drive-it-stuff]], [[archive/threads/fiigii/2026-08-25-if-youve-done-serious-compiler-optimization-work/2026-08-26-theblazehen-why-should-i-care-about-the-performance-of]], [[archive/threads/fiigii/2026-08-25-if-youve-done-serious-compiler-optimization-work/2026-08-26-EgorBo-in-our-case-its-also-often-just-blocked-by-the]], [[archive/threads/fiigii/2026-08-25-if-youve-done-serious-compiler-optimization-work/2026-08-26-amoswap-dont-worry-it-exists-they-call-it-pgo-we-had-it]], [[archive/threads/fiigii/2026-08-25-if-youve-done-serious-compiler-optimization-work/2026-08-26-thedevbirb-i-think-inline-assembly-should-be-the-right]], [[archive/threads/fiigii/2026-08-25-if-youve-done-serious-compiler-optimization-work/2026-08-26-keshen754041-very-true]]
