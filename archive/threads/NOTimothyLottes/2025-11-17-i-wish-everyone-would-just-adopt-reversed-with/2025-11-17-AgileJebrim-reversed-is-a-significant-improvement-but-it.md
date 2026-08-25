---
title: "Reversed is a significant improvement but it still has its limitations when doing planetary-scale rendering that needs good precision up both close and far away."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1990260754688172298"
author: "Jebrim"
handle: AgileJebrim
post_id: "1990260754688172298"
date: 2025-11-17
archived: 2026-08-23
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Reversed is a significant improvement but it still has its limitations when doing planetary-scale rendering that needs good precision up both close and far away."
in_reply_to: ""
parent_post_id: "1990260050485797063"
---

## Source

- URL: https://x.com/AgileJebrim/status/1990260754688172298
- Author: Jebrim (@AgileJebrim)
- Posted: 2025-11-17 03:28:35

## Branch

**1/** @AgileJebrim

Reversed is a significant improvement but it still has its limitations when doing planetary-scale rendering that needs good precision up both close and far away. Your options there are either a logarithmic depth buffer to linearize things (albeit losing early z), your own integer-based depth test system in compute shaders, or a stack of multiple frustums layered on top of one another.

**2/** @NOTimothyLottes

@AgileJebrim Yes for my non-tri stuff I'm log depth already. This is just for games, not simulation.

**3/** @AgileJebrim

Simulation can usually localize enough that reverse Z is good enough. Google Earth style geospatial visualization is where things get trickier.

Another option is to dynamically change the far plane, moving it closer as you get closer to the terrain and further back as you move further back. I don’t think I tried this one but I imagine it requires a lot of tuning.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-11-17-i-wish-everyone-would-just-adopt-reversed-with]]
