---
title: "@rfleury At what point do you think you should convert a switch statement to \"behavior flags\"? Suppose there are N entity types and K behaviors."
type: archive
source: twitter
source_url: "https://x.com/cairnc1/status/1869448847807898074"
author: "cairno"
handle: cairnc1
post_id: "1869448847807898074"
date: 2024-12-18
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury At what point do you think you should convert a switch statement to \"behavior flags\"? Suppose there are N entity types and K behaviors."
in_reply_to: ""
parent_post_id: "1869414867113009626"
---

## Source

- URL: https://x.com/cairnc1/status/1869448847807898074
- Author: cairno (@cairnc1)
- Posted: 2024-12-18 18:25:12

## Branch

**1/** @cairnc1

@rfleury

At what point do you think you should convert a switch statement to "behavior flags"? Suppose there are N entity types and K behaviors. There should be optimal values of N, K and number of shared behaviors. At least for the purpose of source code length.

**2/** @rfleury

@cairnc1

The problem is that the definition of the problem changes. Assuming there are "entity types" at all is partly the problem. If there is only one entity type, but N possible features for each entity, then there are 2^N possibilities for each individual entity's features.

**3/** @rfleury

@cairnc1

Personally I have found I only very rarely want the switch. I instead want a single type at the bottom, which expands out into these large 2^N spaces, so that a great deal is possible via small changes in data.

**4/** @cairnc1

@rfleury

I prefer behavior flags in theory but I find myself often having very bespoke indecomposable behaviors that correspond 1:1 with a "object". Is it because I am too OOP brained? Fwiw I've only ever programmed in C. I guess it is still a win since sharing behaviors is still easier

**5/** @rfleury

Yeah, I think that is still preferable to "object types". It also makes it much lower friction to decompose them, if/when you see how that should happen. If it never happens, doesn't really matter. For heavier data payloads associated with those specific features, just store them out-of-band.

**6/** @cairnc1

@rfleury

Btw organizing logic this way really makes me wish C had metagen built-in. 😔 I guess we still have X macros

**7/** @rfleury

@cairnc1

Yeah, I get that, although once you have your own general-purpose codebase, it is not a big deal, because *you do* have metagen built in then :)

## Related

- Spine: [[archive/threads/rfleury/2024-12-18-one-of-the-most-powerful-lessons-i-learned-as-a]]
