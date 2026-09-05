---
title: "57 lines in polished Vulkan Triangle on my minimal API."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/2095562458467287266"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "2095562458467287266"
date: 2026-09-03
archived: 2026-09-04
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "57 lines in polished Vulkan Triangle on my minimal API."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/2095562458467287266
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2026-09-03 17:19:58

## Thread

**1/** **@SebAaltonen** ^2095562458467287266

57 lines in polished Vulkan Triangle on my minimal API. With Vulkan it's 616 lines. Triangle doesn't even have any bindings or textures (I improved those the most). 11x difference.

My VkCube port is 220 lines, but is still lacking final polish. Original is 5209 lines. 24x difference. Cube has textures, vertices and draw data, which explains the much bigger difference.

![](https://pbs.twimg.com/media/HRS6_DoaAAAur-5?format=jpg&name=orig)

**2/** **@SebAaltonen** ^2095566250562945170

I will be measuring the performance difference of course. My draw call does only two API commands in total (vkCmdPushDataEXT + vkCmdDraw). No descriptor set bindings, no vertex buffer bindings. Definitely going to be faster than traditional Vulkan. On GPU side the performance difference is interesting. I have root struct as the main primitive, allowing shader compiler and driver to optimize code as well as possible. I also have direct 64-bit GPU pointers for data. There's never need for double indirection (fetch descriptors -> fetch data) on GPU side. But some GPUs require per-lane 64-bit pointer for raw memory fetch, which uses one more VGPR (temporarily) versus 32-bit offset. Also texel buffer fetch would give us free format conversion. However modern GPUs have native support for 16-bit types (int16, uint16, fp16) and it's zero cost to extract 16-bit high/low half of a register. 8-bit ALU/registers still doesn't have 100% coverage on modern GPUs, meaning that you need to sometimes waste 1 ALU instruction for convert/scale. Nvidia and AMD doubled their ALU rate recently and that got us <30% perf gains in games, meaning that most shaders today in games are not ALU bound. Paying that 1 extra ALU is likely not an issue. Raw memory loads also have faster latency than texel buffer loads, since they don't go though the format conversion hardware. The difference can be up to 3x (hot L1$ data). Our new API allows explicit data aligning and Slang has aligned load instructions, meaning that shader compiler can emit wide load4 in many cases where traditional shaders couldn't do that. So I would expect to see a slight perf improvement in the GPU side too, but it definitely depends on the shader you are running.

**3/** **@SebAaltonen** ^2095567431481655668

Also the raw load performance depends on GPU brand. Nvidia has been optimizing for CUDA/AI for long time, so they have super fast raw loads. Apple Metal is C/C++ based, so it uses 64-bit pointers everywhere too. Their hardware is perfect for that. AMD has been traditionally optimizing for texel buffers as that's the default in DX9, DX11 and DX12. But AMD has some super nice raw load instructions too. For example they can directly raw load from memory to LDS. But IIRC the PC drivers don't emit this instruction (on console you can do it). Raw load directly to LDS saves a lot of registers. I hope that will work in the future. Would be perfect with this API.
