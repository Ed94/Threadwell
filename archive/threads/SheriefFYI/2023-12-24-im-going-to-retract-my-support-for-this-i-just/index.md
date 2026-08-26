---
title: "I'm going to retract my support for this - I just profiled a scenario where I generate geometry on the CPU every frame, upload it via a copy queue, then have the gfx queue do clears + some work before waiting for same-frame copy."
type: archive
source: twitter
source_url: "https://x.com/SheriefFYI/status/1738800602568638492"
author: "Sherief, FYI"
handle: SheriefFYI
post_id: "1738800602568638492"
date: 2023-12-24
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SheriefFYI
description: "I'm going to retract my support for this - I just profiled a scenario where I generate geometry on the CPU every frame, upload it via a copy queue, then have the gfx queue do clears + some work before waiting for same-frame copy."
in_reply_to: ""
---

## Source

- URL: https://x.com/SheriefFYI/status/1738800602568638492
- Author: Sherief, FYI (@SheriefFYI)
- Posted: 2023-12-24 05:55:43

## Thread

**1/** **@SheriefFYI** ^1738800602568638492

I'm going to retract my support for this - I just profiled a scenario where I generate geometry on the CPU every frame, upload it via a copy queue, then have the gfx queue do clears + some work before waiting for same-frame copy. Delay is ~50us from signal to gfx queue resuming.

Branches: [[archive/threads/SheriefFYI/2023-12-24-im-going-to-retract-my-support-for-this-i-just/2023-12-24-lectem-sorry-i-didnt-have-time-to-do-this-during-the]], [[archive/threads/SheriefFYI/2023-12-24-im-going-to-retract-my-support-for-this-i-just/2023-12-24-NOTimothyLottes-2x-faster-today-perhaps-prior-on-amd-i-had-rgp]]

**2/** **@SheriefFYI** ^1738801049228411350

I profiled this in multiple cases - vsync on and frame taking < 16ms the wait is longer but that's because other parts of the system clock down, so you still hit your vsync window. At no point was this cross-queue wait a significant cause of delay / missing frame time.

**3/** **@SheriefFYI** ^1738801643108413737

Sample data:

![](https://pbs.twimg.com/media/GCF2xqxXQAAAYb3?format=png&name=orig)
