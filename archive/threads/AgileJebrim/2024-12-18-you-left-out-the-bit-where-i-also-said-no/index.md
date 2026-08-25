---
title: "@munohikari @SebAaltonen You left out the bit where I also said no graphics pipeline."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1869397269956673662"
author: "Jebrim"
handle: AgileJebrim
post_id: "1869397269956673662"
date: 2024-12-18
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@munohikari @SebAaltonen You left out the bit where I also said no graphics pipeline."
in_reply_to: ""
---

## Source

- URL: https://x.com/AgileJebrim/status/1869397269956673662
- Author: Jebrim (@AgileJebrim)
- Posted: 2024-12-18 15:00:15

## Thread

**1/** @AgileJebrim

@munohikari @SebAaltonen You left out the bit where I also said no graphics pipeline. :P

**2/** @SebAaltonen

@AgileJebrim @munohikari Computer shaders are a can of worms for old mobile GPUs too. Some have fast groupshared memory (could be tiny), some emulate it. Some have wave intrinsics, some don't. 64-bit atomic support is nonexistent (for MM Dreams / Native style Z+payload packing).

**3/** @SebAaltonen

@AgileJebrim @munohikari Also compute shader writes are not compressed (pixel shader framebuffer writes have HW lossless compressor). You pay full memory bandwidth cost, which causes phone to heat (drain battery) and eventually throttle.

**4/** @AgileJebrim

@SebAaltonen @munohikari Alternative approach is to do all rendering in screen space in a fragment shader.

**5/** @SebAaltonen

@AgileJebrim @munohikari If you intend to do distance field ray-tracing using volume textures, worth noting that most mobile GPUs don't do proper 3d tiling layout for volume textures. Instead they use legacy 2d sliced layout, which results in significantly more L1$ trashing. Can 5x your mem BW use.

**6/** @AgileJebrim

@SebAaltonen @munohikari Raycasting, no bouncing, using cubic textured bricks that emulate voxel surfaces via a parallax occlusion map approach measuring distances to each voxel surface.

If I’m writing something for an avionics cockpit, I’d be either using an Arm Mali-G78AE or NVIDIA DRIVE AGX Thor GPU.

**7/** @AgileJebrim

@SebAaltonen @munohikari I’d also be using Vulkan SC, which I believe disables atomics entirely. :P

**8/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari Disabling atomics is like chopping off both legs because someone thinks one tow has a blister when it actually doesn't.

**9/** @AgileJebrim

@NOTimothyLottes @SebAaltonen @munohikari You can still implement a comparable feature yourself.

Branches: [[archive/threads/AgileJebrim/2024-12-18-you-left-out-the-bit-where-i-also-said-no/2024-12-18-SebAaltonen-yes-but-its-going-to-be-much-slower-you-can-do]]

**10/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari No actually you cannot. No method of software (or even HW) implemented lock-line algorithm survives the kind of latency in the GPU memory system. There is a big reason atomics on GPUs are done right by the last level of cache (the coherent memory domain)

**11/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari Something you really need to understand for your own benefit:
(1.) There are a lot of more expensive things happening in the GPU memory system than atomics. For instance DCC compression. It requires metadata access (to get the state of memory just to do the compression on store).

**12/** @NOTimothyLottes

@AgileJebrim @SebAaltonen @munohikari (2.) Think of GPU atomics as a read-modify-write op. It's effectively the same behavior as a partial cacheline write-through STORE operation on HW using ECC. Because ECC eats the bits used for byte-write-mask.

Branches: [[archive/threads/AgileJebrim/2024-12-18-you-left-out-the-bit-where-i-also-said-no/2024-12-18-NOTimothyLottes-3-if-you-had-multiple-line-stores-collecting-on-a]]
