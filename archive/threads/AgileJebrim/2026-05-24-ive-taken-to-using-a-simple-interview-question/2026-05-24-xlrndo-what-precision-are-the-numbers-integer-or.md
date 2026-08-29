---
title: "What precision are the numbers? Integer or floating point? Do we care about numerical stability? Can we assume we're on an NVIDIA GPU with threads, warps, CTAs, and grids? How much memory bandwidth do we have? Is that array of numbers big or really big?"
type: archive
source: twitter
source_url: "https://x.com/xlrndo/status/2058691325302894659"
author: "xlrndo"
handle: xlrndo
post_id: "2058691325302894659"
date: 2026-05-24
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "What precision are the numbers? Integer or floating point? Do we care about numerical stability? Can we assume we're on an NVIDIA GPU with threads, warps, CTAs, and grids? How much memory bandwidth do we have? Is that array of numbers big or really big?"
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/xlrndo/status/2058691325302894659
- Author: xlrndo (@xlrndo)
- Posted: 2026-05-24 23:27:15

## Branch

**1/** **@xlrndo** ^2058691325302894659

What precision are the numbers? Integer or floating point? Do we care about numerical stability? Can we assume we're on an NVIDIA GPU with threads, warps, CTAs, and grids? How much memory bandwidth do we have? Is that array of numbers big or really big?

Too many questions to have any kind of single answer. It's not a bad interview question if it's used as a jumping off point for the candidate to demonstrate their knowledge.

**2/** **@AgileJebrim** ^2058691753851384096

**@xlrndo**

https://x.com/agilejebrim/status/2058562643158352101?s=46&t=ZbNecpPBsBMrvteeaA6IcA

**3/** **@AgileJebrim** ^2058692267641077855

**@xlrndo**

Portable across a wide range of GPU hardware. You can assume 32-wide waves, 256-wide workgroups, and 64KB shared memory. The memory bandwidth is unlikely to affect the answer.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
