---
title: "That's pretty cool!"
type: archive
source: twitter
source_url: "https://x.com/Dark_Goldenrod/status/2098207974212686092"
author: "Dark Goldenrod"
handle: Dark_Goldenrod
post_id: "2098207974212686092"
date: 2026-09-11
archived: 2026-11-16
draft: false
tags:
  - archive
  - twitter
  - TrisH0x2A
description: "That's pretty cool!"
in_reply_to: ""
parent_post_id: "2098135741075497111"
---

## Source

- URL: https://x.com/Dark_Goldenrod/status/2098207974212686092
- Author: Dark Goldenrod (@Dark_Goldenrod)
- Posted: 2026-09-11 00:32:18

## Branch

**1/** **@Dark_Goldenrod** ^2098207974212686092

That's pretty cool!

In writing my upcoming database, I really saw just how expensive num->str can be! 
At times, it was >10% of total time for queries!

In my testing, I found that the entire penalty for the function was in the needed length calculation... it's a long enough and branchful-enough process to break your cpu predictors before returning to the parent code.
Does SQL still calculate the output length?

I tried similar lookup tables and they were always slower in practice than div+mod in a "repnz" loop, where the divisions and mods get to runahead.

Here is the unsigned version that I profiled as the fastest in practice:

sized_ptr_t simple_ustoa(uint64_t value, char* buffer)
{
    char *ptr = buffer + 32 - 1;

    do {
        *ptr-- = '0' + (value % 10);
        value /= 10;
    } while (value > 0);

    ptr++;

    return sized_ptr_t_create(ptr, 32 - (ptr - buffer));
}

Where buffer is char buffer[33]; buffer[32] = '\0'; (for null-terminated result).

There's also a signed version, which has two extra branches (one before the loop and one after) to handle the negative.

## Related

- Spine: [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits]]
