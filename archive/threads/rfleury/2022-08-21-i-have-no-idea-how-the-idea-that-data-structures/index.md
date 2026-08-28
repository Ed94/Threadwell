---
title: "I have no idea how the idea that *data structures* are coupled to *layout of data structures in memory * got so pervasive with programmers."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1561488791503720448"
author: "Ryan Fleury"
handle: rfleury
post_id: "1561488791503720448"
date: 2022-08-21
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "I have no idea how the idea that *data structures* are coupled to *layout of data structures in memory * got so pervasive with programmers."
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/1561488791503720448
- Author: Ryan Fleury (@rfleury)
- Posted: 2022-08-21 23:01:53

## Thread

**1/** **@rfleury** ^1561488791503720448

I have no idea how the idea that *data structures* are coupled to *layout of data structures in memory * got so pervasive with programmers. It’s like nobody ever learned anything other than malloc’ing each node and stuffing a single tiny payload into them. Totally bizarre.

**2/** **@_plop_** ^1561711055285456897

**@rfleury**

well I have an idea, just use c++ 🤷‍♂️ it's not like the average person can easily avoid using std containers

**3/** **@rfleury** ^1561720380590419968

**@_plop_**

Custom data structures and memory management are not nearly as hard as people make them out to be. In fact, they end up being *easier* in a lot of ways. I don't think it's that difficult to teach, but maybe some good visualizers/debuggers would help make it trivial to understand.

**4/** **@_plop_** ^1561752840330219521

**@rfleury**

well I agree we should teach them more, but they do add a lot of potential for bugs, which is why a lot companies/programmers choose to rely on silly but robust std maps instead of writing their own hash maps

**5/** **@rfleury** ^1561755261567508486

**@_plop_**

I realize people *claim that* but it’s never actually measured. In practice it seems entirely false, especially with simple sanity checks and testing. It’s ridiculous, to me, that writing a hash-table is seen as unbearably difficult for professional programmers industry at large.

**6/** **@rfleury** ^1561755644868251648

**@_plop_**

Furthermore, this touches on another myth, which is that programmers “choose data structures”. Data structures are not mutually exclusive. When you restrict yourself to *choosing one* out of a standard library, you eliminate a massive space of possibilities.

**7/** **@rfleury** ^1561755778175815680

**@_plop_**

Programmers should instead learn data structure *principles* and how to mix-and-match them at will.
