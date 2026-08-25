---
title: "<long thread> "
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1735622924571201674"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1735622924571201674"
date: 2023-12-15
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "<long thread> "
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1735622924571201674
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-12-15 11:28:46

## Thread

**1/** **@NOTimothyLottes** ^1735622924571201674

<long thread> 
Holiday GPU thoughts as a recovering pc/mobile/etc cross platform dev-holic ...

**2/** **@NOTimothyLottes** ^1735623225860583609

[0] Early STP prototypes: had standard-PC-practice multi-dispatch 32-bit version, and hyper-optimized packed-16-bit semi-persistent single-dispatch-ubershader that got L2 reuse. Optimized one was 40% faster in profiling (VK RNDA2 GPU)! Industry has huge untapped opt potential

**3/** **@NOTimothyLottes** ^1735623600344813976

[1] Even for PC, 16-bit is required for optimization because: almost double the amount of register state a shader can leverage. Holds true even when platform lacks double rate 16-bit. Top optimization is pass merging, PC went bandwidth starved. Mobile is actually ALU starved ...

**4/** **@NOTimothyLottes** ^1735623707001753932

[2] Double rate 16-bit done right, is typically good for the smaller of {30% perf, return to non-ALU bound}, can make a GPU feel at least one HW generation faster.

**5/** **@NOTimothyLottes** ^1735623832549916904

[3] For PC, I'd personally draw my compatibility line where platforms support 16-bit, and only ship explicit packed 16-bit shaders instead of a separate 32-bit/16-bit shader permutation. AMD it's Vega up, for NV note Maxwell/Pascal's HFMA2: https://docs.nvidia.com/cuda/cuda-binary-utilities/index.html#maxwell-and-pascal-instruction-set

**6/** **@NOTimothyLottes** ^1735623992961081680

[4] Suggest doing dev work on a platform with great packed 16-bit support: AMD PC Vulkan on RDNA2, and don't filter through the DXC deoptimizer, so it is actually possible to see the value. Then hammer on vendors who still have spotty compiler related issues.

**7/** **@NOTimothyLottes** ^1735624151283478999

[5] Gather4 is the hot optimization for packed 16-bit because data is returned in SoA form. Always explicitly pack 16-bit and alias to/from UINT32 when passing constants to shader (best to alias eight 16-bit values as uint4). Etc.

**8/** **@NOTimothyLottes** ^1735624428581429681

[6] Trick for good 16-bit is range management. Sometimes pre-scaling is needed to avoid overflow,
and make sure to bring max values out of denormal before using rcp.

**9/** **@NOTimothyLottes** ^1735624590997573967

[7] Power is a function of data movement. "Touch it Once" is the top optimization, all the "Split it into a Graph, Pipeline Stage it" people are walking themselves towards high-power.

**10/** **@NOTimothyLottes** ^1735624799378923763

[8] Majority of GPU workloads are whole-pass serially dependent, but in practice temporally independent with exception of small localized serial dependency. If you "stick it into a frame graph" you cut off your ability to optimize.

**11/** **@NOTimothyLottes** ^1735624946414501895

[9] Resolution growth is slowing. Mobile's high DPI is beyond good enough. 8k won't be successfull because of the extra 4x scaling TAA tax, or it won't matter because people will just integer scale on scanout.

**12/** **@NOTimothyLottes** ^1735625312350642210

[10] Scaling TAA will converge to consistent higher quality over time, thus PC is likely to locally converge to 720p|1080p rendering for 4k (for high|med FPS). This implies that the industry should hit a point where large L3 can hold full render targets ...

**13/** **@NOTimothyLottes** ^1735625572040994994

[11] TAA scaling, full render targets in L3: Maybe RDNA2 128 MiB L3 was spot on actually, and RNDA3's L3 drop in capacity, and the no L3 consoles had this wrong Tracing and big nets probably need that L3 too.

**14/** **@NOTimothyLottes** ^1735625818288558341

[12] Lots of value getting a good 8x area scale for 4K 120 Hz. Yet devs won't see value until they make the non-pixel costs scale well, and move post before scaling.

**15/** **@NOTimothyLottes** ^1735626224188243980

[13] Triangles are not needed any more. Hint 8x area scaling doesn't know any connectivity. Connectivity is inferred by likeness to accumulated feedback. Shaded samples from non-triangles -> scaling TAA still works. Hint 2: scaling TAA raster is mostly just tri culling.

**16/** **@NOTimothyLottes** ^1735626424956895544

[14] TAA gets quality limited at high scaling because it can only infer correct behavior from geometry similar to what is rendered. Geometric aliasing drops too much thin geo. Fix for that is to change the standard practice, which will obsolete all black boxes.

**17/** **@NOTimothyLottes** ^1735626636509208780

[15] Stratified sampling is good for at least 2x the geo density compared to regular grid ... frame viewport jitter is end-of-life for quality.

**18/** **@NOTimothyLottes** ^1735626794491949057

[16] TAA's ability to correctly infer reprojection validity on skinned objects is crippled by lack of correct forward projection. Fixing that will break the black boxes.

**19/** **@NOTimothyLottes** ^1735627033844085045

[17] Shading density will end up variable, TAA's disocclusion and convergence logic needs to be out of the black box, and deeply integrated into shading systems too (because it points where to shade more). This evolution will break all the black boxes.

**20/** **@NOTimothyLottes** ^1735627294377456031

[18] Per-pixel ML people have it wrong, your net is multi-pass, all the top optimizations require less passes. Don't matter if you optimize the matrix math, power is burned in the bandwidth, and you cannot reduce your bandwidth enough to compete with the better options.

**21/** **@NOTimothyLottes** ^1735627982763385283

[19] GI needs a surface shade cache, might as well object space shade at that point, which enables NUMA, which enables more HW scaling.

**22/** **@NOTimothyLottes** ^1735628284979777660

[20] HW RT people had it very wrong, top optimization is non-ray-traversal ordered access. Follows: occlusion testing is neighbor-coherent, no trace, just test shared occluders. GI reduces to high frequency occlusion of some lower frequency probe domain.

**23/** **@NOTimothyLottes** ^1735628590094385329

[21] HW RT's skin-all re-tree before trace won't scale ever. Only stratified visibility gets log scaling on animated geo. HW RT has no system for bounding costs, while stratified visibility does. Think out of the black box, GPU got programmability decade back now.

**24/** **@NOTimothyLottes** ^1735631826427732305

[22] Love HW people, but they opt for a $ train even as it is derailing: they need to build HW, make it faster, it's what they do. But leave a trail of back-compat debris TS/ROV/GS/etc after each gfx fad. Vote with your engineering, general purpose CS, just say no to black boxes.

Branches: [[archive/threads/NOTimothyLottes/2023-12-15-long-thread/2023-12-15-SebAaltonen-they-design-one-api-for-each-separate-use-case]]

**25/** **@NOTimothyLottes** ^1735650294552203454

[23] Scaling TAAs want sparse data each frame, more like a low-frequency pixel control cage displacing a high-frequency reprojected feedback. No pixel centers any more, no need to interpolate before shading. Rather want striped data, so the cachelines group spaced-out samples ...
