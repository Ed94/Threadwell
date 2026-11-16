---
title: "@AgileJebrim Why would you do this."
type: archive
source: twitter
source_url: "https://x.com/MrJayLC/status/2110067671874327005"
author: "John"
handle: MrJayLC
post_id: "2110067671874327005"
date: 2026-10-13
archived: 2026-11-16
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim Why would you do this."
in_reply_to: ""
parent_post_id: "2110051793379975227"
---

## Source

- URL: https://x.com/MrJayLC/status/2110067671874327005
- Author: John (@MrJayLC)
- Posted: 2026-10-13 17:58:30

## Branch

**1/** **@MrJayLC** ^2110067671874327005

**@AgileJebrim**

Why would you do this.
Jitter would be the variance observed between frame times.
Predictability is the match between estimated and measured jitter.
Determinism means that a given input produces a given output 100% of the time.

Isochrony is a new one for me.

**2/** **@AgileJebrim** ^2110068785361084841

**@MrJayLC**

It’s predictably within a target time. If you’re early you can just busy-spin or do something else until you reach the predicted time and then interrupt. This is what traditional hard real-time generally targets but it’s also much harder to verify what the worst-case actually is.

**3/** **@AgileJebrim** ^2110069372878279122

**@MrJayLC**

Determinism in the context of timing means that a given data input executes with the same timing 100% of the time. A different data input may have a different timing.

Isochrony is the same timing every periodic tick every single time regardless of the data inputs or lackthereof.

**4/** **@AgileJebrim** ^2110069846046048412

It’s cheap to verify worst-case because you do not need to identify what the worst-case actually is. It’s already known. The others require complex analysis of a program to identify the worst-case state. This can become a very difficult combinatorics problem and be hardware-specific.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-10-13-definitions-we-use-when-timing-hard-real-time]]
