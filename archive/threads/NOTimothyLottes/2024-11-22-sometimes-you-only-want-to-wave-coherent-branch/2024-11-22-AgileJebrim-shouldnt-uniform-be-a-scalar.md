---
title: "@NOTimothyLottes Shouldn’t uniform be a scalar?"
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1859792525218988305"
author: "Jebrim"
handle: AgileJebrim
post_id: "1859792525218988305"
date: 2024-11-22
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Shouldn’t uniform be a scalar?"
in_reply_to: ""
parent_post_id: "1859791162091110754"
---

## Source

- URL: https://x.com/AgileJebrim/status/1859792525218988305
- Author: Jebrim (@AgileJebrim)
- Posted: 2024-11-22 02:54:25

## Branch

**1/**

@NOTimothyLottes Shouldn’t uniform be a scalar?

**2/**

@AgileJebrim Well 'uniform' in GLSL is a storage qualifier, "Uniforms are so named because they DO NOT CHANGE from one shader invocation to the next within a particular rendering cal" so you probably want another term for SGPR to avoid aliasing qualifiers

**3/**

@NOTimothyLottes Within ISPC, uniform means scalar and varying means vector.

**4/**

@NOTimothyLottes Looking deeper into the definition of SGPRs. They’re uniform just across each wavefront, rather than the entire dispatch yeah?

**5/**

@AgileJebrim Yes it's a separate register file and logic unit that is per-wave instead of per-lane. Since it's introduction in Turing, NV calls them "URX for uniform registers" while AMD calls them SGPRs (scalar general purpose registers)

**6/**

@NOTimothyLottes Almost sounding like we need an alternative IR to SPIR-V. One with predicated instructions and these wavefront-uniform registers/instructions. Maybe a PTX -> RDNA backend compiler?

**7/**

@AgileJebrim As history goes, most re-writes fall into nearly the same problem as before. I'd rather have the fixes be applied to the existing stuff first (fix SPIR-V and GLSL, etc)

**8/**

@NOTimothyLottes Perhaps. That existing PTX Vulkan extension does come to mind though.

**9/**

@AgileJebrim @NOTimothyLottes Its kinda annoying to put sgpr like logic in an ir tho as they have very specific limitations on each platform.

Generalizing them in an ir might actually be a pessimisation.

**10/**

@AgileJebrim @NOTimothyLottes Amd for example can't do float ops on sgprs, so when you would allow float ops in the ir, amd has to move them to a vgpr, perform float op, move them back to sgpr for each ir-sgpr float op.

There are other examples for this.

And nvidias have even other constrains.

**11/**

@CodePotrick @NOTimothyLottes And what’s the alternative right now? Just keep it all in a VGPR all the time?

**12/**

@AgileJebrim @NOTimothyLottes Ideally you'd avoid any float ops as long as you can to keep things in sgprs if you need to save registers/want the uniformity.

If you need float ops on that var its probably best to keep it in vgprs if the alternative would be to transfer between sgpr and vgpr a lot

**13/**

@CodePotrick @NOTimothyLottes I wish I could work solely with integers all the time but if I did that on NV hardware, I’d be losing half the available ALUs.

**14/**

@CodePotrick @NOTimothyLottes I haven’t looked closely at AMD hardware since I don’t work with it much.

**15/**

@AgileJebrim @NOTimothyLottes they have their actual isa public and inspectable which is really nice to know whats actually happening.

Rga is also really good. Feels like im more in control with amd compared to nvidia.

Maybe thats just the low level gremlin in my speaking tho ;).

**16/**

@CodePotrick @NOTimothyLottes I do have access to some of NVIDIA’s NDA documentation and tools…

## Related

- Spine: [[archive/threads/NOTimothyLottes/2024-11-22-sometimes-you-only-want-to-wave-coherent-branch]]
