---
title: "@AgileJebrim i see it as a convolution task."
type: archive
source: twitter
source_url: "https://x.com/noinodev/status/2058439885619622196"
author: "noino🔸"
handle: noinodev
post_id: "2058439885619622196"
date: 2026-05-24
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim i see it as a convolution task."
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/noinodev/status/2058439885619622196
- Author: noino🔸 (@noinodev)
- Posted: 2026-05-24 06:48:07

## Branch

**1/** **@noinodev** ^2058439885619622196

**@AgileJebrim**

i see it as a convolution task. gather per thread in registers, gather in local thread group shmem, and atomic add assuming atomics are available. repeat for all cells, then keep scheduler happy by not going over register or thread limits. is there more to it than that?

**2/** **@AgileJebrim** ^2058534147061109052

**@noinodev**

Give more details on each step. Assume more data elements than parallel hardware.

**3/** **@AgileJebrim** ^2058534304808902987

**@noinodev**

Don’t assume you can use atomics.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
