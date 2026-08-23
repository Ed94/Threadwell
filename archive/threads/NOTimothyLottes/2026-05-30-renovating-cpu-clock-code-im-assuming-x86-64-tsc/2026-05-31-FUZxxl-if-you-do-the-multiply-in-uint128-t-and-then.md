---
title: "@NOTimothyLottes If you do the multiply in uint128_t and then right-shift by 64 places, the compiler should do the right thing."
type: archive
source: twitter
source_url: "https://x.com/FUZxxl/status/2060885487858880689"
author: "Robert Clausecker"
handle: FUZxxl
post_id: "2060885487858880689"
date: 2026-05-31
archived: 2026-08-23
status: draft
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes If you do the multiply in uint128_t and then right-shift by 64 places, the compiler should do the right thing."
in_reply_to: ""
parent_post_id: "2060730425929080874"
---

## Source

- URL: https://x.com/FUZxxl/status/2060885487858880689
- Author: Robert Clausecker (@FUZxxl)
- Posted: 2026-05-31 00:46:04

## Branch

**1/**

@NOTimothyLottes If you do the multiply in uint128_t and then right-shift by 64 places, the compiler should do the right thing.

**2/**

@FUZxxl “Should” is exactly why I prefer the actual instruction instrinsics or just inline asm (which is what I use on C CPU land)

**3/**

@NOTimothyLottes Have fun with a solution that the compiler optimises worse and that is not portable.

## Related

- Spine: [[index]]
