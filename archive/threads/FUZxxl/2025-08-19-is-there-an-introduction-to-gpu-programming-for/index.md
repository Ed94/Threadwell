---
title: "Is there an introduction to GPU programming for the seasoned assembly programmer?  All tutorials I can find start with a dozen layers of abstraction and never really seem to get down to the metal."
type: archive
source: twitter
source_url: "https://x.com/FUZxxl/status/1957729589326709116"
author: "Robert Clausecker"
handle: FUZxxl
post_id: "1957729589326709116"
date: 2025-08-19
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - FUZxxl
description: "Is there an introduction to GPU programming for the seasoned assembly programmer?  All tutorials I can find start with a dozen layers of abstraction and never really seem to get down to the metal."
in_reply_to: ""
---

## Source

- URL: https://x.com/FUZxxl/status/1957729589326709116
- Author: Robert Clausecker (@FUZxxl)
- Posted: 2025-08-19 09:01:21

## Thread

**1/** **@FUZxxl** ^1957729589326709116

Is there an introduction to GPU programming for the seasoned assembly programmer?  All tutorials I can find start with a dozen layers of abstraction and never really seem to get down to the metal.

**2/** **@FUZxxl** ^1957733225297580231

Ideally I'd want to program the GPU in assembly, but I have been repeatedly told that this is not how you do things on GPUs and that you shall go through the abstraction layer for it is blessed yadda yadda

**3/** **@AgileJebrim** ^1957762928129495481

Unlike CPUs that have maintained a stable ISA for decades, GPU ISAs are in constant flux (and are not publicly documented in the case of NVIDIA and Apple). They vary significantly between vendors and even generations of hardware from the same vendor. This means you essentially have to work at the IR level for portability purposes.

These are a few choices: PTX (CUDA), SPIR-V (Vulkan), DXIL (Direct3D), HIP (ROCm), and NIR (Mesa3D).

If you really want to write GPU assembly for one very specific card, bypassing even the IR, then AMD is the probably the easiest available to do so with. They publicly publish their ISA and open source drivers exist to read from and modify.

The easiest way in my head to do something like this in user space would be to identify the code in one of these drivers that generates the pipeline caches when compiling Vulkan SPIR-V shaders. Extract that out as an offline application and then you ought to be able to embed GPU ISA-specific code directly into a pipeline cache binary that can then be loaded directly into Vulkan on another machine with identical hardware and drivers.

Probably not worth it in practice though due to how limiting that is and how quickly it’ll become obsolete. Even a driver update can break that. I’ve personally just embraced working with SPIR-V instead. It’s very portable, is popular, and has a long life ahead of it that is matched only by NVIDIA’s PTX.

SPIR-V is better for real-time graphics and compute workloads. PTX is generally used in offline HPC workloads. There is also an extension available to use PTX from within Vulkan but there’s some lack of tooling support due to how niche that is. I don’t know of any project actually using it.

Another thing to note about SPIR-V vs PTX is that the former is stored as a 32-bit word bytecode, whereas the latter is straight up ASCII. It does, however, provide some lower level access to NVIDIA-specific cache controls, guard predicates, and other features that may not be available to SPIR-V.

Let me know any other questions you might have.

**4/** **@JamesAnder73326** ^1957911572795244920

**@AgileJebrim** **@FUZxxl**

can you respond to this @FUZxxl instead of sperging out at other people cause this is what you wanted to know right?

**5/** **@AgileJebrim** ^1957915096060928106

**@JamesAnder73326** **@FUZxxl**

He might like the Vulkan + PTX combo with compute shaders. It’ll him get the closest to the hardware that he’s looking for if he’s got an NVIDIA GPU. More importantly, it’s something that shouldn’t take an enormous amount of time trying to get set up.

https://registry.khronos.org/vulkan/specs/latest/man/html/VK_NV_cuda_kernel_launch.html

**6/** **@JamesAnder73326** ^1958200864377606476

**@AgileJebrim** **@FUZxxl**

ngl man I feel bad you wrote out all this stuff for a retard that's ragebaiting without even having Twitter blue

**7/** **@FUZxxl** ^1958201341521629544

**@JamesAnder73326** **@AgileJebrim**

If you feel I'm ragebaiting you, that says more about than anything.  I just want to program my GPU in assembly, how hard can it be?

**8/** **@AgileJebrim** ^1958204246265856288

**@FUZxxl** **@JamesAnder73326**

Reverse engineer (or find an open source tool to generate) a pipeline cache binary for a specific piece of hardware/driver, create an assembler for that, and submit it to Vulkan. That’s my final answer. That’s as low level as you can go.

**9/** **@FUZxxl** ^1958204515288551711

**@AgileJebrim** **@JamesAnder73326**

People have done that before, with great success.  However, the resources remain scattered about and sparse.  Hence my question asking for a good tutorial.

**10/** **@AgileJebrim** ^1958211355170963716

Within Mesa3D, you have RADV, AMDVLK, and NVK as open source options. The first two for AMD, the latter for NVIDIA. They take SPIR-V and output GPU ISA and pipeline cache binaries. They’re not designed to work as custom assemblers and you’d have some work to try to extract the code within to create an assembler for a specific GPU ISA.

**11/** **@AgileJebrim** ^1958211444987789763

**@FUZxxl** **@JamesAnder73326**

In the CUDA world, there do appear to be some open source tools available:

https://github.com/daadaada/turingas

Branches: [[archive/threads/FUZxxl/2025-08-19-is-there-an-introduction-to-gpu-programming-for/2025-08-20-AgileJebrim-another-one-here-https-github-com-cloudcores]]
