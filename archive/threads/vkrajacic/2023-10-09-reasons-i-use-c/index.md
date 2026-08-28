---
title: "Reasons I use C:"
type: archive
source: twitter
source_url: "https://x.com/vkrajacic/status/1711389580018979139"
author: "Vjekoslav Krajačić"
handle: vkrajacic
post_id: "1711389580018979139"
date: 2023-10-09
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - vkrajacic
description: "Reasons I use C:"
in_reply_to: ""
---

## Source

- URL: https://x.com/vkrajacic/status/1711389580018979139
- Author: Vjekoslav Krajačić (@vkrajacic)
- Posted: 2023-10-09 14:34:06

## Thread

**1/** **@vkrajacic** ^1711389580018979139

Reasons I use C:
- It's a small and simple language.
- It's stable and changes infrequently.
- It provides low-level, manual memory management.
- I can see actual CPU instructions.
- It has a decades-old development ecosystem.
- It works everywhere.
- It allows for direct interaction with major operating systems, which expose low-level APIs in C or C++.
- I want my code to remain runnable 10-20 years from now.

Not the reasons I use C:
- Because I believe it's perfect.
- Because I'm a "fan" of it.
- Because I think it has all the features I need.

I write in C because I believe it's still the best choice for developing native applications (not just embedded software). This conveys a lot about my sentiments towards other languages, including C++, C#, Rust etc.
 
New is not always better.

**2/** **@simplex_fx** ^1711416943935103027

**@vkrajacic**

however, you CAN write almost all the features not present in them, if needed :D

**3/** **@vkrajacic** ^1711456818164019443

Yes, I had to write a fair amount of "base" code, such as memory primitives, UTF-8 length-based strings, math, UI, etc. However, once you have these components in place, it's much better than using higher-level languages with numerous libraries that you might not fully comprehend.

**4/** **@thembeddevguy** ^1711468670860312694

**@vkrajacic** **@simplex_fx**

That’s the task of a standard library. It’s a shame and not a feature if all of these must be written. It’s not a must to include stdio or any standard lib and you can use your custom libs. That’s why I’m shifting to golang, really feels like the modern C we need so far.

**5/** **@rfleury** ^1711571034829476347

**@thembeddevguy** **@vkrajacic** **@simplex_fx**

The weird thing about this argument is that it somehow presupposes that a new language & toolchain was necessary for a new standard library. Neither are necessary. If you want a new standard library, make one. It doesn't need to be standardized at the programming language level.

**6/** **@thembeddevguy** ^1711637670240174253

**@rfleury** **@vkrajacic** **@simplex_fx**

A standard library for me always was a “here are super common tasks and no one shall “solve” that over and over again, here, have a reviewed and tested solution, go focus on the important parts” thing. Relying on 3rd party stuff is exactly the opposite of this.

Branches: [[archive/threads/vkrajacic/2023-10-09-reasons-i-use-c/2023-10-10-thembeddevguy-i-would-trust-a-builtin-solution-1000-times-more]]
