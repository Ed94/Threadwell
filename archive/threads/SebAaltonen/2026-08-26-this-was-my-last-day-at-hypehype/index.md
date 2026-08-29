---
title: "This was my last day at HypeHype."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/2092601949149380783"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "2092601949149380783"
date: 2026-08-26
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "This was my last day at HypeHype."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/2092601949149380783
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2026-08-26 13:15:57

## Thread

**1/** **@SebAaltonen** ^2092601949149380783

This was my last day at HypeHype. Going to take a long sabbatical to be with my family and to focus on my hobby projects. 

Lot of cool videos coming: SDFs, mass physics, fluids/lava, explosions, ray-tracing, GPGPU and fun fast paced gameplay. PC/Steam focus.

**2/** **@SebAaltonen** ^2092614858705416699

I wrote all the tech for Claybook. SDF world, fluids with erosion, GPGPU soft body/deformation simulator, etc. Optimized it to work smoothly Nintendo Switch 1 and old Intel iGPU. Steam Deck GPU has 10x more ALU (GFLOPS). So much more is possible today.

https://x.com/SebAaltonen/status/1060479645798359040?s=20

**3/** **@SebAaltonen** ^2092616205513162915

Wrote a quick prototype last week combining SDF tech with first-person shooter enemy swarm gameplay. Here the enemy swarm path finding, physics and rendering takes just 0.2ms of CPU time. And that's with single threaded render (WebGPU limitation). No AVX2 (SIMD8). Simple thread scheduler. I can easily make it 5x faster. 100,000 enemies is completely doable. Massive bosses destroying the level. Lava gun. Foam grenade, etc, etc. Fun and hectic instead of slow and boring kids game (like Claybook). 

https://x.com/SebAaltonen/status/2090543938390098141?s=20

**4/** **@SebAaltonen** ^2092617429176201597

Of course we need good visuals too. Massive amount of moving light sources (rockets, fires, bullets, emissives). Real-time GI, reflections, etc. But at the same time it must run at 240Hz on my RTX 4090. Can't be as heavy as Teardown. Must reach locked 60Hz on Steam Deck.

**5/** **@SebAaltonen** ^2092618261481300365

I will of course document the whole process in social media. Share all the tech details, profiling data and all the cool short videos. I did the same during Claybook development.

**6/** **@SebAaltonen** ^2092683216360489447

The first thing I will do is finish the Clean API prototype:
https://x.com/SebAaltonen/status/2088740095276773574?s=20

Would be nice to write the new game on top of this API, but I have to check what kind of hardware coverage we can get with it. Don't want to limit user base too much.

Branches: [[archive/threads/SebAaltonen/2026-08-26-this-was-my-last-day-at-hypehype/2026-08-27-EvilKimau-also-weird-pitch-but-if-you-managed-to-get-your]]
