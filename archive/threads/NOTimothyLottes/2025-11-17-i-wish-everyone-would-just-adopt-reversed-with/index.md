---
title: "I wish everyone would just adopt \"reversed with infinite far\" projection matrixes so I could only optimize for the fastest and highest precision option, but I'm guessing people haven't all migrated over :("
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1990260050485797063"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1990260050485797063"
date: 2025-11-17
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "I wish everyone would just adopt \"reversed with infinite far\" projection matrixes so I could only optimize for the fastest and highest precision option, but I'm guessing people haven't all migrated over :("
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1990260050485797063
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-11-17 03:25:47

## Thread

**1/** @NOTimothyLottes

I wish everyone would just adopt "reversed with infinite far" projection matrixes so I could only optimize for the fastest and highest precision option, but I'm guessing people haven't all migrated over :(

![](https://pbs.twimg.com/media/G57SXPJW8AAvEhh?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2025-11-17-i-wish-everyone-would-just-adopt-reversed-with/2025-11-17-terekhov_de-ive-never-had-real-depth-precision-issues-in-our]], [[archive/threads/NOTimothyLottes/2025-11-17-i-wish-everyone-would-just-adopt-reversed-with/2025-11-17-bgolus-many-are-still-on-opengles-and-webgl-which-dont]], [[archive/threads/NOTimothyLottes/2025-11-17-i-wish-everyone-would-just-adopt-reversed-with/2025-11-18-Alecazam123-infinite-far-doesnt-apply-to-ortho-and-many-of]], [[archive/threads/NOTimothyLottes/2025-11-17-i-wish-everyone-would-just-adopt-reversed-with/2025-11-19-stainless_code-i-havent-really-done-graphics-in-a-while-but-ive]]

**2/** @AgileJebrim

Reversed is a significant improvement but it still has its limitations when doing planetary-scale rendering that needs good precision up both close and far away. Your options there are either a logarithmic depth buffer to linearize things (albeit losing early z), your own integer-based depth test system in compute shaders, or a stack of multiple frustums layered on top of one another.

**3/** @NOTimothyLottes

@AgileJebrim

Yes for my non-tri stuff I'm log depth already. This is just for games, not simulation.

**4/** @AgileJebrim

Simulation can usually localize enough that reverse Z is good enough. Google Earth style geospatial visualization is where things get trickier.

Another option is to dynamically change the far plane, moving it closer as you get closer to the terrain and further back as you move further back. I don’t think I tried this one but I imagine it requires a lot of tuning.
