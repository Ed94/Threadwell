---
title: "@simplex_fx @SebAaltonen Yeah it's a common problem, thin wrapper interfaces reduced to the worst platform's caps then called at high frequency ..."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1890421311962239323"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1890421311962239323"
date: 2025-02-14
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - simplex_fx
description: "@simplex_fx @SebAaltonen Yeah it's a common problem, thin wrapper interfaces reduced to the worst platform's caps then called at high frequency ..."
in_reply_to: ""
parent_post_id: "1890348863287943363"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1890421311962239323
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-02-14 15:22:17

## Branch

**1/** @NOTimothyLottes

@simplex_fx @SebAaltonen Yeah it's a common problem, thin wrapper interfaces reduced to the worst platform's caps then called at high frequency ... it's the recipe for poor software engineering

**2/** @NOTimothyLottes

@simplex_fx @SebAaltonen Arguments like: we cannot do bindless at the engine interface level because our Intel iGPU binding limits are too low, etc. Just another sign the engine interface failed when all platforms are crippled for the LCD, better if only the LCD platforms are crippled

**3/** @NOTimothyLottes

@simplex_fx @SebAaltonen My interfaces are like @simplex_fx perhaps, I only do either extremely high-level, or extremely low-level. So my graphics API is just this below ...

![](https://pbs.twimg.com/media/GjwlQgIXMAAu8Va?format=png&name=orig)

**4/** @simplex_fx

@NOTimothyLottes @SebAaltonen what is the mark-unmark thing?

**5/** @NOTimothyLottes

@simplex_fx @SebAaltonen It is a 1:1 map to VkEvents. Mark:set signal after all prior launched dispatches have completed, unmark:clear signal,  wait: wait for signal

**6/** @simplex_fx

@NOTimothyLottes @SebAaltonen Do you have plans to publish your render?

Seems like some super nice and lightweight stuff.

**7/** @NOTimothyLottes

@simplex_fx @SebAaltonen The game/rendering side of my current project is too wild/game-specific to be of general usage, but the shell of the engine without the content, that I might release at some point into open source as an example

**8/** @AgileJebrim

@NOTimothyLottes @simplex_fx @SebAaltonen What’s the game?

**9/** @NOTimothyLottes

@AgileJebrim @simplex_fx @SebAaltonen Across many years of working for IHVs and ISVs, I've been doing my own side project personal R&D prototypes geared towards solving all the key systems of a game I'd like to actually put into production some day

**10/** @AgileJebrim

@NOTimothyLottes @simplex_fx @SebAaltonen A combat flight sim MMO?

**11/** @NOTimothyLottes

@AgileJebrim @simplex_fx @SebAaltonen Probably split it up into two: a single player vs world (low scope), then use that to fund what I really want to do which involves multi-player (high scope).

**12/** @NOTimothyLottes

@AgileJebrim @simplex_fx @SebAaltonen FPS-like (more like 3D Descent [DOS], instead of fixed planar), trying to break ground more in world-scope simulation/thinking/destruction but not just thin on-planet-surface stuff, more like full planetoid interior [BLAME! style, an out-of-control world-building machine]

**13/** @NOTimothyLottes

@AgileJebrim @simplex_fx @SebAaltonen Rewinding time, there have been some interesting milestones in PC gaming
(1.) Command HQ (and similar) - Modem connected real-time multi-player world scale battle simulation with fog of war ...

![](https://pbs.twimg.com/media/Gj133GjXAAEjf7m?format=png&name=orig)

**14/** @NOTimothyLottes

@AgileJebrim @simplex_fx @SebAaltonen (2.) Starflight https://www.filfre.net/2014/10/starflight/ - procedural universe generation, but with persistent interaction, they actually saved game state back to the floppy disk ... might say today "No Man's Sky" is like a modern version of that procedural universe generation

![](https://pbs.twimg.com/media/Gj15ToNWMAI5q9d?format=png&name=orig)

**15/** @NOTimothyLottes

@AgileJebrim @simplex_fx @SebAaltonen Forwarding in time a lot
(3.) Teardown - expanding the lego-style chunky voxel engine with fully dynamic destruction, while still maintaining a high quality render

![](https://pbs.twimg.com/media/Gj16icuW4AArsmT?format=jpg&name=orig)

**16/** @NOTimothyLottes

@AgileJebrim @simplex_fx @SebAaltonen But there are a lot of barriers that feel like speed-of-sound barriers (possible) vs speed-of-light (impossible) with PC game tech, examples
(1.) Voxel games - they stay mostly chunky (you have games like Voxile pushing this a little, with in-voxel details)

![](https://pbs.twimg.com/media/Gj17wiCXEAAyyfh?format=jpg&name=orig)

**17/** @NOTimothyLottes

@AgileJebrim @simplex_fx @SebAaltonen (2.) Physical simulation. NV PhyX had some absolutely amazing demos of destruction, but not really anything that went all in on massive destruction BECAUSE the game is still on the CPU, and the GPU is limited to just graphics ... seems like still a massive opportunity

**18/** @NOTimothyLottes

@AgileJebrim @simplex_fx @SebAaltonen (3.) And the biggest one IMO: many do procedural generation and stop there. But it is the MIX of procedural rules and simulation that actually generates interesting behavior and content, that is very under-explored

**19/** @NOTimothyLottes

@AgileJebrim @simplex_fx @SebAaltonen So the inflection point IMO was GPUs getting fast enough compute where triangle rendering wasn't required, and then getting large enough memory, where one could devote it to {high/low frequency simulation,persistence,etc} instead of "textures"

## Related

- Spine: [[archive/threads/simplex_fx/2025-02-14-hey-gpu-guys-like-sebaaltonen-notimothylottes-why]]
