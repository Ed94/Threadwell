---
title: "@NOTimothyLottes SPIR-V."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1950936023447302584"
author: "Jebrim"
handle: AgileJebrim
post_id: "1950936023447302584"
date: 2025-07-31
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes SPIR-V."
in_reply_to: ""
parent_post_id: "1950935464149483683"
---

## Source

- URL: https://x.com/AgileJebrim/status/1950936023447302584
- Author: Jebrim (@AgileJebrim)
- Posted: 2025-07-31 15:06:09

## Branch

**1/**

@NOTimothyLottes SPIR-V. I’ve given up on trying to massage frontend compilers to do exactly what I want. I’m just letting others write in whatever shader language they want and then taking the SPIR-V it generates and reoptimizing it the way I want it.

**2/**

@NOTimothyLottes One of the motivating factors is the fact that people already have a bunch of existing code, so the less work needed on their part to rewrite it, the better.

**3/**

@AgileJebrim If IHV compilers all handled well the case where the SPIR-V skips most SSA and leverages OpLoad/Store to global shader data (as in registers not memory), it might be a lot more tractable to go direct to SPIR-V.

**4/**

@NOTimothyLottes I’m forcing the case where each invocation has access to a full 256 registers, which should hopefully limit the whole SSA/register spill problem. I haven’t tried intentionally breaking SSA though. Even if I did, there’s no way such UB would ever be certifiable.

**5/**

@AgileJebrim I don't know of any case where 256 registers had acceptable performance. And that includes IHV hand assembly. Full unrolling on GCN needed at least 2 waves/SIMD (128 regs max). And I personally target around 64 for anything going through a compiler.

**6/**

@AgileJebrim Note on some newer AMD GPUs they increased the regfile by 50% I think, which would be a 96 max reg target

**7/**

@AgileJebrim Some of the larger problems with compilers is common sub-expression elimination. Meaning they will take out intentional recoputation or reloads and add register pressure. Often one has to fake a different value by ORing to a dynamic loaded zero (not known at compiler time)

**8/**

@AgileJebrim Meaning at medium levels of complexity the compilers are always going way over the register budget you'd target with hand written ASM. SSA ensures this. There are no aliasing hints in the IR.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-07-31-been-on-the-fence-on-writing-shader-interfaces-in]]
