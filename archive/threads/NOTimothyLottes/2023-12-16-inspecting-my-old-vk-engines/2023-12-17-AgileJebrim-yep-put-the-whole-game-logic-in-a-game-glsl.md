---
title: "@NOTimothyLottes Yep put the whole game logic in a game.glsl compute shader."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1736232422528709002"
author: "Jebrim"
handle: AgileJebrim
post_id: "1736232422528709002"
date: 2023-12-17
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Yep put the whole game logic in a game.glsl compute shader."
in_reply_to: ""
parent_post_id: "1736157335058300999"
---

## Source

- URL: https://x.com/AgileJebrim/status/1736232422528709002
- Author: Jebrim (@AgileJebrim)
- Posted: 2023-12-17 03:50:41

## Branch

**1/**

@NOTimothyLottes Yep put the whole game logic in a game.glsl compute shader.

**2/**

If doing a large open world game, set up a paging system to stream data to the GPU in tiles, particularly static data. All dynamic data should be handled on the GPU. If leveraging  server, you can pass along the network packets as they are. CPU shouldn’t really be doing much for a game client. It certainly shouldn’t be varying due to scene complexity.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2023-12-16-inspecting-my-old-vk-engines]]
