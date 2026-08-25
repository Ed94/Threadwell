---
title: "@rfleury Too much words, but unique_ptr is*really* zero cost."
type: archive
source: twitter
source_url: "https://x.com/Pps831/status/1917545684372447392"
author: "Pps831"
handle: Pps831
post_id: "1917545684372447392"
date: 2025-04-30
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury Too much words, but unique_ptr is*really* zero cost."
in_reply_to: ""
parent_post_id: "1917431895786414425"
---

## Source

- URL: https://x.com/Pps831/status/1917545684372447392
- Author: Pps831 (@Pps831)
- Posted: 2025-04-30 11:44:52

## Branch

**1/** @Pps831

@rfleury

Too much words, but unique_ptr is*really* zero cost. There is no way to go negative in cost there, no matter how much you wish for it 🤣

**2/** @rfleury

@Pps831

I recommend you learn to read

**3/** @Pps831

@rfleury

I’m ok. But you should at least try to validate if unique_par is zero cost or not. Also, in case you were really complaining about shared_ptr - try to cook something equivalent in c (not just “smart” ptr with ref count, but equivalent)

**4/** @rfleury

@Pps831

It isn’t zero cost.

**5/** @Pps831

@rfleury

Shared_ptr? Off course, it’s really heavy, but it has incredibly useful functionality.

**6/** @rfleury

@Pps831

No, both of them. Neither are useful compared to the alternatives.

**7/** @Pps831

@rfleury

If you “really” need the functionality - then it’s great. Most uses don’t really need shared_ptr. If you don’t use it along with “weak_ptr” then you don’t really need it. If you complain about all the allocations, it has solution for the problem: enable_shared_from_this

## Related

- Spine: [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a]]
