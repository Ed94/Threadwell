---
title: "[0] Been wanting to do this for a long time, a thread on hard-core shader development."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1859368974351274470"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1859368974351274470"
date: 2024-11-20
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "[0] Been wanting to do this for a long time, a thread on hard-core shader development."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1859368974351274470
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-11-20 22:51:23

## Thread

**1/**

[0] Been wanting to do this for a long time, a thread on hard-core shader development. Something that digs into what I've learned and applied over the years. Along with the evolution of the strange syntax I use when writing shaders ...

**2/**

[1] Lets start at one of the early ones, FXAA 3.11. Someone is hosting that here: https://gist.github.com/kosua20/0c506b81b3812ac900048059d2383126 ... most lines, it's an easy map to NV's arch which has predicated instructions (red is the predicate). Many lines are 1:1 mappings with physical HW instructions.

![](https://pbs.twimg.com/media/Gc3OqZkWsAAeP9s?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2024-11-20-0-been-wanting-to-do-this-for-a-long-time-a/2024-11-20-AgileJebrim-how-reliable-in-your-experience-in-code-like-that]]

**3/**

[2] Looking at FSR1: https://github.com/GPUOpen-Effects/FidelityFX-FSR/blob/master/ffx-fsr/ffx_fsr1.h - that had 3 permutations {32-bit, 16-bit unpacked, 16-bit packed}, where the packed one maps to how AMD's packed instructions work (everything explicitly packed)

![](https://pbs.twimg.com/media/Gc3QjEiWYAADo14?format=png&name=orig)

**4/**

[3] Onto STP: https://github.com/Unity-Technologies/Graphics/blob/27341ce4f5c8853d7f15e9420bff499f1087aceb/Packages/com.unity.render-pipelines.core/Runtime/STP/Stp.hlsl - A different set of permutations {32-bit, packed 16-bit} then {implicit mediump vs explicit} in the 32-bit (generic) permutation via types like StpMF4 which aim to allow a compiler on mobile to get some 16-bit register savings

![](https://pbs.twimg.com/media/Gc3SFXTXoAEt4tX?format=png&name=orig)

**5/**

[4] Notice for 16-bit path, everything again is explicitly packed (unlike the 32-bit path). And GLSL to SPIR-V would get explicit packing to the IHV driver since SPIR-V has explicit vector types (unlike DX, which was an insane problem). Example, the reprojection filtering below.

![](https://pbs.twimg.com/media/Gc3SmjPWMAEMX_d?format=png&name=orig)

**6/**

[5] Then STP had defines to work out differences in sampling capability (like supporting MIN/MAX sampling with UINT or not, or supporting immediate offsets or not). Example in the code doing {z,motion} UINT32 packed nearest dilation:

![](https://pbs.twimg.com/media/Gc3TW0oWIAArDjw?format=png&name=orig)

**7/**

[6] The largest portability nightmare was mixing explicit FP16 with wave ops! So many compiler bugs across vendors = so many permutations in the code. The 32-bit path had to have a conversion from 'StpMF4' (possible implicit medium precision), to 'StpF4' explicit 32-bit.

![](https://pbs.twimg.com/media/Gc3UTC_WcAAyc5J?format=png&name=orig)

**8/**

[7] Some of perf death problems had been that DXIL didn't have bitfield ops (unlike SPIR-V), HLSL depends on IHV compilers somehow finding and pattern matching stuff like the crap below (which is MANY OPS to 1 OPCODE). So pre-processing through HLSL on non-Xbox platforms = fail!

![](https://pbs.twimg.com/media/Gc3V5wGW8AADAju?format=png&name=orig)

**9/**

[8] Go into the shader which is doing wave ops, and the true nightmare of platform workarounds becomes apparent https://github.com/Unity-Technologies/Graphics/blob/27341ce4f5c8853d7f15e9420bff499f1087aceb/Packages/com.unity.render-pipelines.core/Runtime/STP/StpSetup.compute - LSD/waveop permutations, 32-bit/16-bit in 16-bit path, etc

![](https://pbs.twimg.com/media/Gc3W143XEAEq6LS?format=png&name=orig)

**10/**

[9] So yeah, even in modern times you can hit paths in compilers and toolchains that well never got tested because no one had tried it and tried shipping with it. And I think this might hint that relatively few actually do this level of crazy

**11/**

[10] Part of the formula for getting great gains with 16-bit is simply the register savings. It wouldn't be possible to do good 4x4 kernel lanczos inside a TAA without packed 16-bit support (it's 64 values on load without thinking about all the other mid-algorithm data) ...

**12/**

[11] Looking at STP again, there is a dering, which works with the {min,max} of the near 2x2. If the HW has MIN/MAX sampling, it can fetch that, which means a lot more than 64 values, and if not they need intermediate ALU min/max, which is extra state ...

![](https://pbs.twimg.com/media/Gc3Ze31XAAA94Y1?format=png&name=orig)

**13/**

[12] Mobile hardware is so register starved (probably due to all that SRAM area going to tiles) that it wasn't possible to do good reprojection filtering PERIOD even with FP16. So STP had a crippled compromise that did bilinear in one direction, and lanczos in the other axis

![](https://pbs.twimg.com/media/Gc3afacXQAAFX-c?format=png&name=orig)

**14/**

[13] Huge wake up call to mobile HW vendors, if you don't match VGPR capacity of PCs, you can never take on where PC workloads will get to. Now given both NV and AMD have packed 16-bit, it is a great time to push pass merging and avoid DRAM traffic by doing more in one shader

**15/**

[14] Another part of the 16-bit perf puzzle is to not use 16-bit FP16 in constants explicitly, but only package them up as aliased as UINT32 binary blobs. And for portable systems that still need 32-bit fallbacks, always build both a packed 16-bit and 32-bit set of constants.

**16/**

[15] So many people tried to 16-bit permute things working from 32-bit float constants, and on PC that is instant perf death. Sure some mobile hardware can do the conversions for lower cost, and some mobile HW could pre-amble the conversions if not, but that isn't perf portable

**17/**

[16] Switching gears. So STP didn't get the most hardcore way I like to write shaders, and I've had a bunch of different permutations of ideas tried over the years ... specifically how to make the code more like GPU assembly!

**18/**

[17] Looking like assembly as in making it exactly clear what the lines map to in HW OPCODEs, and what the variable map to in REGISTERS. So you are designing to what the hardware could do, even if the compiler cannot keep up

**19/**

[18] Now it's true that NV and AMD HW are quite different in some respects (NV is predicated, and has generic 3 op logic ops, etc), so ultimately one has to pick their shader language abstraction based on what they want to target the most https://docs.nvidia.com/cuda/cuda-binary-utilities/index.html#instruction-set-reference (NV ISA docs)

**20/**

[19] Since AMD's docs are more complete, and I like to make sure a console port is possible and would be as fast as possible, I prefer to think through all my shaders as if they are getting direct mapped to AMD's RDNA2 these days: https://www.amd.com/content/dam/amd/en/documents/radeon-tech-docs/instruction-set-architectures/rdna2-shader-instruction-set-architecture.pdf

**21/**

[20] So I usually do a define that maps logic directly to what the associated instruction would be. Some of these actually map to shading language intrinsics already like fma() or bitfieldExtract(). Then write all my shader code using these defines. Example below for the defines

![](https://pbs.twimg.com/media/Gc3fKzqXUAAGnBQ?format=png&name=orig)

**22/**

[21] Like to use ASM like convention for {signed, unsigned}, that all integers are unsigned, and only get converted to signed when required inside the define for a specific opcode (like signed or unsigned bitfield extract). Bit casting (aliasing) is done via SI1_I1() style macros

![](https://pbs.twimg.com/media/Gc3gGUTWQAAZwyX?format=png&name=orig)

**23/**

[22] And I reduce all types to very simple 3 letter macros of which are described below. I use the same naming convention in CPU land as well. This helps keep code compact and easy to read IMO (highly subjective yes)

![](https://pbs.twimg.com/media/Gc3gna_XcAA7PXx?format=png&name=orig)

**24/**

[23] One thing I struggle with to this day is compiler bitcast aliasing perf bugs. Meaning once I tried to always only use UINT4 types everywhere, and then wrap all OPCODE defines in bitcasting defines, that didn't go so well (looking at disassembly on AMD PC).

**25/**

[24] Compilers depend a lot on pattern matching to NOP stuff, and well there are bugs, lots of bugs. So for the sake of portability, with the exception of {unsigned/signed} bitcasting, I use the native types when possible (no packed-16-bit/32-bit aliasing) exception of waveops

**26/**

[25] Another aspect of compiler problems is argument passing to function calls causing SSA state explosions, because it's "copy semantics" as defined in the langs. Once I did inout uint4[16] (all VGPRs) as my only argument to all functions. Didn't end well!

**27/**

[26] Someone on twitter (or was it bsky or mast?) had been doing a one shader game. And addressing these kinds of problems, and reminded us, YES the shader languages support global variables. No need to pass them into function! (bingo)

**28/**

[27] We have been so seasoned to dislike globals in the past few decades due to well probably early mutli-window programming styles, that it is easy to forget you can just do globals, and they are fast at tool/compile time.

**29/**

[28] I think the next level up of this design is to go to mostly global variables, but since the shader languages don't support global unions, then have different sets of globals when one needs to do type bitcast aliasing (which is very common with packed 16-bit and 64-bit logic)

**30/**

[29] I still think the 'fix' for the shader compiler SSA state explosion mapping back to registers problem is to pass in explicit aliasing hints to the vendor compilers, so they have a better base guess at register allocation. But I doubt vendors would get on board with that

**31/**

[30] My personal x86-64 languages typically worked with unions of structs on globals. Where each struct in the union was a different aliased meaning to the HW registers, and functions had been associated with a given struct in the union. So no stacks or argument passing.

**32/**

[31] That kind of setup for the GPU is ideal IMO (at least for the type of stuff I do). You can link. Because the union struct for the registers is the calling ABI, and never moves (no stack). So code sharing works amazingly well. And avoiding register state explosion is built in

**33/**

[32] oh damn [32], should probably stop now, until next time.
