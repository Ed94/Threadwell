---
title: "@rfleury individual malloc/free is a common C practice and is the fair comparison; group allocations are not the norm in most programs especially in the hand-off ownership situations where unique_ptr would apply."
type: archive
source: twitter
source_url: "https://x.com/AbstrctMachnist/status/1917754448178188666"
author: "AbstractMachinist"
handle: AbstrctMachnist
post_id: "1917754448178188666"
date: 2025-05-01
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury individual malloc/free is a common C practice and is the fair comparison; group allocations are not the norm in most programs especially in the hand-off ownership situations where unique_ptr would apply."
in_reply_to: ""
parent_post_id: "1917431895786414425"
---

## Source

- URL: https://x.com/AbstrctMachnist/status/1917754448178188666
- Author: AbstractMachinist (@AbstrctMachnist)
- Posted: 2025-05-01 01:34:25

## Branch

**1/** **@AbstrctMachnist** ^1917754448178188666

**@rfleury**

individual malloc/free is a common C practice and is the fair comparison; group allocations are not the norm in most programs especially in the hand-off ownership situations where unique_ptr would apply. In this light unique_ptr is strictly superior.

**2/** **@rfleury** ^1917776657131397142

**@AbstrctMachnist**

No, it isn’t the fair comparison, because that is not how sensible code is written.

**3/** **@AbstrctMachnist** ^1917780558878249115

**@rfleury**

Okay, well it's a like-vs-like comparison. If used as a straightforward replacement, unique_ptr is better. I concede it's not a replacement for a careful memory strategy.

**4/** **@rfleury** ^1917782019876217141

**@AbstrctMachnist**

But the equivalent code isn’t straightforward. It’s not *careful* to do something better. It’s both *easier and faster*. It is simply the superior way to not use them at all.

**5/** **@AbstrctMachnist** ^1917786181099573679

**@rfleury**

Looking at the RAD Debugger as an example (which is unfair, since you can't look at my code), the diligence of passing an allocator through every function, and being constantly mindful of which pool a given string is coming from, does not seem simple, though it is impressive.

**6/** **@rfleury** ^1917787214534390012

It isn't through every function, though. And it is not accurate to say you are "constantly mindful" about it. Layers which allocate plan for & control those allocations through a variety of strategies. Most allocations are bucketed into arenas, so the allocation occurs and is forgotten. Anyone who is passed an allocation can use the allocation, they do not have to care about where it came from.

**7/** **@AbstrctMachnist** ^1917790048071598171

**@rfleury**

Alright, but surely this is more thought than probably even 95% of programs give to such things. Nor are most programs developed with such careful attention to layers and their individual memory strategies. And I don't think they should need to, by default.

**8/** **@rfleury** ^1917791946749403159

**@AbstrctMachnist**

*Someone* has to build those layers, is the point. The high level code doesn't have to think about anything. I agree that at those layers, nobody should be having to think about anything other than their problem.

## Related

- Spine: [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a]]
