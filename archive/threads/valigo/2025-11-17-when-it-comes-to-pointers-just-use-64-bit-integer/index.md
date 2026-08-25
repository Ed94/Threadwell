---
title: "When it comes to pointers, \"just use 64 bit integer\" is way more intuitive to me."
type: archive
source: twitter
source_url: "https://x.com/valigo/status/1990506460531601538"
author: "Valentin Ignatev"
handle: valigo
post_id: "1990506460531601538"
date: 2025-11-17
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - valigo
description: "When it comes to pointers, \"just use 64 bit integer\" is way more intuitive to me."
in_reply_to: ""
---

## Source

- URL: https://x.com/valigo/status/1990506460531601538
- Author: Valentin Ignatev (@valigo)
- Posted: 2025-11-17 19:44:56

## Thread

**1/** **@valigo** ^1990506460531601538

When it comes to pointers, "just use 64 bit integer" is way more intuitive to me. I still remember how confusing it was that "pointer + 1" actually means "+ size_of(type_we_point_to)" when I learned all this stuff. It still kinda messes me up not gonna lie.

Branches: [[archive/threads/valigo/2025-11-17-when-it-comes-to-pointers-just-use-64-bit-integer/2025-11-18-mrsteyk1-i-had-the-displeasure-of-being-exposed-to-hex]], [[archive/threads/valigo/2025-11-17-when-it-comes-to-pointers-just-use-64-bit-integer/2025-11-18-attamayte1-pointer-arithmetic-based-on-type-sizes-makes]], [[archive/threads/valigo/2025-11-17-when-it-comes-to-pointers-just-use-64-bit-integer/2025-11-18-furiouswhopper-for-real-im-parsing-through-a-binary-array-and]], [[archive/threads/valigo/2025-11-17-when-it-comes-to-pointers-just-use-64-bit-integer/2025-11-18-TheBonkMaykr-it-is-confusing-if-you-arent-used-to-it-that-is]], [[archive/threads/valigo/2025-11-17-when-it-comes-to-pointers-just-use-64-bit-integer/2025-11-18-Ron172892111531-wouldnt-this-make-working-with-arrays-more]], [[archive/threads/valigo/2025-11-17-when-it-comes-to-pointers-just-use-64-bit-integer/2025-11-25-levs57-interestingly-if-you-try-to-write-rust-in-this]]

**2/** **@onelivesleft** ^1990525482295832860

**@valigo**

Distinct syntax for pointer arithmetic would be good. i.e. 
ptr += 1; // ptr = ptr + 1;
ptr ++= 1; // ptr = ptr + 1 * size_of(type_of(ptr));

**3/** **@valigo** ^1990525680065577199

**@onelivesleft**

Not sure I agree with specific sign choice but I kinda dig the concept

**4/** **@onelivesleft** ^1990526589470482553

**@valigo**

Well, you know, only applicable for languages that don't have a ++ :P
