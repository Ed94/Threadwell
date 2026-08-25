---
title: "Inspecting my old VK engines."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1736147815829565624"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1736147815829565624"
date: 2023-12-16
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Inspecting my old VK engines."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1736147815829565624
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-12-16 22:14:30

## Thread

**1/**

Inspecting my old VK engines. On start I would warm all the pages. Code pages get a read, and data pages got an atomic add of a non-compiler known zero. An attempt to improve initial load time. But in the end nothing helps the 2.6 seconds or so required to just open the VK device

![](https://pbs.twimg.com/media/GBgHT_2WIAAKuNq?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2023-12-16-inspecting-my-old-vk-engines/2023-12-17-SheriefFYI-two-point-six-seconds-d3d12createdevice-on-my]]

**2/**

Since I almost never get crashes I forgot about this, but had written a system to auto relaunch the app on crash or special case exit. No complex error handling, just bank on fast relaunch instead.

![](https://pbs.twimg.com/media/GBgJ1y5W0AArwSt?format=png&name=orig)

**3/**

The hope of single PSO in VK was scrapped because IHV compile times explode. However I did maintain single SPIR-V file, and use spec constants to choose individual shaders. The threads doing compile dump compile times and disassembly in DEV mode.

![](https://pbs.twimg.com/media/GBgMbMEWkAAOd_d?format=png&name=orig)

**4/**

I'm a fan of single file applications. So when not in DEV mode the one SPIR-V file gets pulled from the EXE. Compiling PSOs is always the critical path, the moment the "bind everything once" layout is done, PSO compile goes wide on the machine.

![](https://pbs.twimg.com/media/GBgOQRiXoAAX2k6?format=png&name=orig)

**5/**

"Bind-Everything-Once" in Vulkan looks like this. Bindings {1}=CPU pushing to GPU, {2}=buffer (more on that next), {3}=as UAVs, {4}=as TEX ... No binding logic at runtime ever. Access anything in the most efficient way any time.

![](https://pbs.twimg.com/media/GBgPDhAWUAAzhEi?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2023-12-16-inspecting-my-old-vk-engines/2025-08-08-VPCOMPRESSB-so-youre-preallocating-every-type-of-descriptor]]

**6/**

Did something silly but fast for buffers. Here is an example from a dummy test app. The main SSBO gets aliased as 4 structures, each with the same data accessable with four types {uint, uint4, float, float4}. So same binding layout aliasing chooses load type and K$ or V$ access.

![](https://pbs.twimg.com/media/GBgQ0xlWQAA7Yks?format=png&name=orig)

**7/**

Literally the CPU does almost nothing. All game input gets pushed to the GPU for game logic. Some major advantages in input latency to do player logic on the GPU instead. And it's dead easy.

![](https://pbs.twimg.com/media/GBgRu3wXoAAp_K7?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2023-12-16-inspecting-my-old-vk-engines/2023-12-17-AgileJebrim-yep-put-the-whole-game-logic-in-a-game-glsl]]

**8/**

This requires context, I build programs in a hardware style, fixed resources, fixed shaders, and all logic expressed in the data itself. No code or resource variation, no runtime issues period. So another dummy program example, I can just list my resources on load in a table ...

![](https://pbs.twimg.com/media/GBgTCgJXsAEPH3W?format=png&name=orig)

**9/**

Radically simplicity is how I roll personally. Easy to confuse the idea that one needs complexity to express a complex system. It's more like one needs complexity to express a complex solution -> abstractions and hierachical meta feeds on itself until tech debt freezes progess.

**10/**

If there is anything to learn for programming, it is to be more critical of your own ideas than all else, be ruthless, trim until what is left is only what is actually required, question everything constantly.
