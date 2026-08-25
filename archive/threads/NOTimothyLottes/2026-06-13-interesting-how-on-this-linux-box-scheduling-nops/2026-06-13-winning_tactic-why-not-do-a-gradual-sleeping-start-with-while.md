---
title: "Why not do a gradual sleeping? Start with"
type: archive
source: twitter
source_url: "https://x.com/winning_tactic/status/2065896862129733922"
author: "OZ"
handle: winning_tactic
post_id: "2065896862129733922"
date: 2026-06-13
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Why not do a gradual sleeping? Start with"
in_reply_to: ""
parent_post_id: "2065840191340707905"
---

## Source

- URL: https://x.com/winning_tactic/status/2065896862129733922
- Author: OZ (@winning_tactic)
- Posted: 2026-06-13 20:39:29

## Branch

**1/** @winning_tactic

Why not do a gradual sleeping? Start with
while (spin--) {
    asm volatile("pause" ::: "memory");
}
then yield()
then yield 'til timer fire
gradually approaching longer spans?
You can have power modes that sets a lower threshhold to always yield and not spin e.g. or to have the particular levels based on eco/perf, and also it depends on the rest of the system to ensure spinning isn't a waste of cycles.

But I've never considered a write to a dummy file as a legitimate yield/wait trigger. I wonder how that would fit in to my solution...

**2/** @NOTimothyLottes

@winning_tactic I don’t design around waiting for a specific point in time, I do other things, but talk about them when I can easily show the results

**3/** @winning_tactic

Correct. But that's the point of gradually backoff, active spinlocking, then green thread yielding (cooperative other tasks, maybe even the one contesting) then kernel_poke (I guess that's what I would call that writing to file its a return from kernel-land immediately) then timer fired, the idea isn't to wait on a time, it's wait on an increasing value that changes tactics from the previous waits so that you don't really have to keep track of when what happens.
https://gitlab.com/qsrc.net/Lampyr/-/blob/dev/rt/time.c?ref_type=heads#L78
But I've got to work on the power stuff and steal your idea of course.

**4/** @NOTimothyLottes

@winning_tactic Ahh the illusion of nonblocking execution on consumer devices. The moment the os decides to preempt your thread, there no longer exists a non blocking interface. A single thread never gets a guarantee of execution, so waiting for some exact point in time is failed design

**5/** @winning_tactic

@NOTimothyLottes It's green threads multiplexed on pinned threads both cooperatively and preemptively. I beg your pardon!~
https://gitlab.com/qsrc.net/Lampyr/-/blob/dev/rt/task.c?ref_type=heads
But, that particular version is a WIP, multiple impl and messy.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2026-06-13-interesting-how-on-this-linux-box-scheduling-nops]]
