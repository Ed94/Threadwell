---
title: "@rfleury Do you have any example of this?"
type: archive
source: twitter
source_url: "https://x.com/slendidev/status/1917745453656940712"
author: "Slendi"
handle: slendidev
post_id: "1917745453656940712"
date: 2025-05-01
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury Do you have any example of this?"
in_reply_to: ""
parent_post_id: "1917431895786414425"
---

## Source

- URL: https://x.com/slendidev/status/1917745453656940712
- Author: Slendi (@slendidev)
- Posted: 2025-05-01 00:58:40

## Branch

**1/** @slendidev

@rfleury

Do you have any example of this?

**2/** @rfleury

@xslendix

Example of what?

**3/** @slendidev

@rfleury

Of where stripping the smart pointers and other RAII stuff leads to simpler memory management (less allocations, less computation)

**4/** @rfleury

@xslendix

I have written several 100K LOC that is completely public that you can go look at and compare with other approaches

**5/** @slendidev

@rfleury

From looking at RADDbg, most of those allocations are avoided by using an arena. How is this any different from passing in an arena to a string for example instead of using the standard allocator?

**6/** @rfleury

@xslendix

It’s completely flipped from the usual RAII approach. Allocated things do not manage themselves. They don’t “know” about their allocator. Everything is just data organized into large buckets. As such, there are no destructors to insert, because there is no freeing to do.

**7/** @slendidev

@rfleury

You can just make the free method of the allocator be empty. If the arena is block based (growing arena) then you can also absolutely use that free method to re-use memory in previous blocks.

**8/** @rfleury

@xslendix

There’s no point.

**9/** @slendidev

@rfleury

Sure, but then you can still make that free method empty

**10/** @rfleury

@xslendix

Or you can just not do any of this ridiculous RAII nonsense at all.

**11/** @slendidev

@rfleury

At that point it’s just personal preference on wether you want your frees explicit or not in the code. Don’t think having an empty free method adds any overhead either since the compiler can just exclude the destructor entirely because of inlining

## Related

- Spine: [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a]]
