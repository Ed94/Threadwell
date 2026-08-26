---
title: "Check your compiler."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1888416459132395792"
author: "Jebrim"
handle: AgileJebrim
post_id: "1888416459132395792"
date: 2025-02-09
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "Check your compiler."
in_reply_to: ""
---

## Source

- URL: https://x.com/AgileJebrim/status/1888416459132395792
- Author: Jebrim (@AgileJebrim)
- Posted: 2025-02-09 02:35:43

## Thread

**1/** **@AgileJebrim** ^1888416459132395792

Check your compiler. Do not trust crap advice like this. Compilers do a piss poor job performing if conversion down to select instructions. From my testing, mix() in GLSL is absolutely the most reliable way of getting a select op as a result.

step() isn’t necessary however. https://t.co/ianYUdKGcc

https://x.com/iquilezles/status/1888409333182218691
[[archive/threads/iquilezles/2025-02-09-hey-dont-optimize-conditional-moves-with-mix-step]]

**2/** **@mcnabbd** ^1888418494666227843

**@AgileJebrim**

i always say: measure it. no way to know for sure except to measure the perf. seen way too many "optimizations" that aren't

**3/** **@AgileJebrim** ^1888420217979543781

Measure can be hit or miss depending upon your data set or other bottlenecks. I also focus on what my final outcome goal actually is, which is a flat profile regardless of data contents, very different from what most folks optimizing are aiming for.

Therefore, I focus more on instruction output from the compiler. Eliminate all branches, even divergent ones, as modern GPUs use various tricks to try to speed these up under specific scenarios (which I don’t want). If a jump exists to anything but to the top of a fixed-length loop, then the code is invalid and should produce an error.

The other key requirement is careful control over caches and bypassing them when needed, but that’s another topic.

**4/** **@mcnabbd** ^1888422707118924065

**@AgileJebrim**

my position is that these machines are so phenomenally complex, and only getting more so, that the only thing i can trust is the final measurement.

**5/** **@mcnabbd** ^1888423105733009877

**@AgileJebrim**

i'll also add that i rarely get to this level of optimization because there are much larger gains to be had at the higher levels. like find a way to not do the thing in the first place

**6/** **@AgileJebrim** ^1888423591064072366

**@mcnabbd**

I don’t view this as an optimization in the first place. It’s not done for raw throughput purposes. It’s done for determinism purposes. To have highly predictable execution times. That’s of greater importance to me than just throughput alone is.

**7/** **@AgileJebrim** ^1888424019046576600

**@mcnabbd**

I design systems where it’s impossible for data contents to trigger performance degradation. It decouples performance from actions taken by content creators or end users. It ensures a stutter-free experience regardless of whatever people do.

**8/** **@NOTimothyLottes** ^1888429813297242393

**@AgileJebrim** **@mcnabbd**

I don't really know what step() is (never used it), but for AMD HW mix(a,b,bool) is a direct map to the HW V_CNDMASK_B32 op and works nice with multi-component a and b. So yeah mix(,,bool) is the right way to do things IMO.

**9/** **@NOTimothyLottes** ^1888433376773743074

**@AgileJebrim** **@mcnabbd**

Here is a simple example and the disassembly which shows mix(,,bool) form works well (using 4-component form in my example)

![](https://pbs.twimg.com/media/GjUPvYTX0AAQkb8?format=png&name=orig)
![](https://pbs.twimg.com/media/GjUP5JsWMAAxRw2?format=png&name=orig)

**10/** **@NOTimothyLottes** ^1888433983718871431

**@AgileJebrim** **@mcnabbd**

Maybe something stupid happens in shadertoy because it is going through a browser that mangles it probably from GLSL ES to HLSL. But at least on PC AMD through Vulkan the mix(,,bool) form is great.

**11/** **@AgileJebrim** ^1888434156310315447

**@NOTimothyLottes** **@mcnabbd**

I doubt it. I think he’s just talking out of his ass and hasn’t actually checked anything.

**12/** **@NOTimothyLottes** ^1888435874137768288

**@AgileJebrim** **@mcnabbd**

Inigo is a very smart man, I'm sure he has some reasonable examples where his advice holds, and likely for his shadertoy (which does show FPS) which is as I say before browser mangled and running on {mobile through PC}. So advice may be different.

**13/** **@mcnabbd** ^1888436341203255304

**@NOTimothyLottes** **@AgileJebrim**

agreed. if Inigo says it, i assume it's right until proven otherwise

**14/** **@NOTimothyLottes** ^1888437808743710947

**@mcnabbd** **@AgileJebrim**

Today there are too many compiler/tools bugs to full generalize shader advice. The industry could fix this though, if they supplied platform specific HW ISA intrinsics for all chipsets. Then ISVs could setup translation headers to guarantee the right fast path on all platforms

**15/** **@AgileJebrim** ^1888439754917609574

**@NOTimothyLottes** **@mcnabbd**

I’ve tried GLSL, HLSL, and Slang. They’re all unreliable. Here is GLSLANG failing immediately at the SPIR-V level for everything but mix(). The use of min() instead of for && also successfully avoids a branch here.

At the very least get the SPIR-V right before it goes past that.

![](https://pbs.twimg.com/media/GjUV8eBWAAEROgw?format=jpg&name=orig)

**16/** **@NOTimothyLottes** ^1888440863044284563

**@AgileJebrim** **@mcnabbd**

IHV compilers are quite good at taking well formed SPIR-V and transforming it into a nightmare GPU binary. The only way to ever know anything is to look at the actual driver disassembly. Unfortunately even with 3T$ NV cannot match VK_AMD_shader_info disassembly dumps.

**17/** **@AgileJebrim** ^1888441108499148862

**@NOTimothyLottes** **@mcnabbd**

I can see NV’s SASS dumps just fine. 🤷‍♂️

**18/** **@AgileJebrim** ^1888441385268727832

**@NOTimothyLottes** **@mcnabbd**

Of course that’s with their NDA tools. However, CUDA on godbolt will also let you see their SASS dumps as well.
