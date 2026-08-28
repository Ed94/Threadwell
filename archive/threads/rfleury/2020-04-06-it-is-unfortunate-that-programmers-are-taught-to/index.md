---
title: "It is unfortunate that programmers are taught to ignore memory in favor of using RAII/GC/ARC/etc., despite that using memory constraints to one's advantage can dramatically improve speed, improve reliability, improve debuggability and reduce code complexity."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1247299604690829313"
author: "Ryan Fleury"
handle: rfleury
post_id: "1247299604690829313"
date: 2020-04-06
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "It is unfortunate that programmers are taught to ignore memory in favor of using RAII/GC/ARC/etc., despite that using memory constraints to one's advantage can dramatically improve speed, improve reliability, improve debuggability and reduce code complexity."
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/1247299604690829313
- Author: Ryan Fleury (@rfleury)
- Posted: 2020-04-06 23:06:14

## Thread

**1/** **@rfleury** ^1247299604690829313

It is unfortunate that programmers are taught to ignore memory in favor of using RAII/GC/ARC/etc., despite that using memory constraints to one's advantage can dramatically improve speed, improve reliability, improve debuggability and reduce code complexity.

**2/** **@rfleury** ^1247299606440038402

It seems that the idea that memory requirements should be abstracted away from the programmer, instead of being a tool to solve a problem, is one of the biggest mistakes of the status quo in software engineering.

**3/** **@rfleury** ^1247299608268509185

I was once told to use the CRT's allocator instead of my own linear allocator for a problem because there would be no way that I write a hand-rolled routine that would beat malloc. The fallacy is that the authors of CRT's malloc for my compiler and I were solving two problems.

**4/** **@rfleury** ^1247299609954668544

Allocating off of a linear allocator is simple. You return a pointer and increment the allocation position. At the end, you just reset that position to 0. This not only simplifies allocation code (batch freeing), it also is dramatically faster than a generic malloc...

**5/** **@rfleury** ^1247299611435257856

...and yet in both education and (*some* places in) the industry, programmers are discouraged from taking advantage of situations like this, to ensure nobody is "re-inventing the wheel".

**6/** **@rfleury** ^1247299612886487041

What do you get for not "re-inventing the wheel"? Worse reliability, worse speed, more complicated code. Where is the tradeoff?

Branches: [[archive/threads/rfleury/2020-04-06-it-is-unfortunate-that-programmers-are-taught-to/2020-04-07-felixzsh-im-that-kind-of-person-who-asks-the-why-of-things]], [[archive/threads/rfleury/2020-04-06-it-is-unfortunate-that-programmers-are-taught-to/2020-04-07-felixzsh-nowadays-there-are-a-lot-of-software-done-and]], [[archive/threads/rfleury/2020-04-06-it-is-unfortunate-that-programmers-are-taught-to/2020-04-08-SasLuca-just-a-conversation-on-this-topic-today]]
