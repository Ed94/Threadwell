---
title: "At the risk of saying something wrong on the internet in hopes of getting corrected, I think one of the best things Nvidia has ever done is the qmd dependent ptr."
type: archive
source: twitter
source_url: "https://x.com/mike64_t/status/2121365444632457412"
author: "mike"
handle: mike64_t
post_id: "2121365444632457412"
date: 2026-11-13
archived: 2026-11-14
draft: false
tags:
  - archive
  - twitter
  - mike64_t
description: "At the risk of saying something wrong on the internet in hopes of getting corrected, I think one of the best things Nvidia has ever done is the qmd dependent ptr."
in_reply_to: ""
---

## Source

- URL: https://x.com/mike64_t/status/2121365444632457412
- Author: mike (@mike64_t)
- Posted: 2026-11-13 22:11:49

## Thread

**1/** **@mike64_t** ^2121365444632457412

At the risk of saying something wrong on the internet in hopes of getting corrected, I think one of the best things Nvidia has ever done is the qmd dependent ptr.
as far as i can tell, in 2012 the dependent QMD exists in hardware, with no user-facing API beyond whatever the CDP runtime did with it internally.
in 2018, cuda graphs re-abstracts the mechanism to use dependent chains to drive down inter-kernel latency.
In 2022, PDL on Hopper hides the cold I$ issue of dependent kernels with overlap.
In 2026, Vera Rubin fixes the remaining issue of uneven completion with tile-level triggering.
Now I think the dependent ptr and the decrement dependence counters in QMD are one of the best things nvidia has ever done and I think an under-appreciated aspect of what makes CUDA great despite nobody being consciously aware of it... 
now I am cautiously awaiting on which side this places me in this debate 😳

**2/** **@NOTimothyLottes** ^2121442149736788275

**@mike64_t**

Perhaps move deeper a few levels, why break up problem solving into multiple kernel dispatches? No need to do that in CPU-land, why do it in GPU-land? Must of the unnecessary complexity was added under the theory that one needs to vary registers/wave (thus launch new kernel) ...

**3/** **@NOTimothyLottes** ^2121442736213778793

**@mike64_t**

Yet maximizing waves/CU does not bring max perf, rather you want to minimize waves/CU to maximize cache/work but stop at the point of still being able to hide latency. And there is another axis of work ILP, where a lane can do N things in parallel instead of 1 ...

**4/** **@NOTimothyLottes** ^2121443260962947076

**@mike64_t**

Turns out ILP is what you need anyway to hide ALU latency. Etc. Etc. Meaning one can simply fix registers/wave, adapting N to how much work fits in fixed register space, and therefore not need to launch waves any more ...

**5/** **@NOTimothyLottes** ^2121443822123286667

**@mike64_t**

At that stage one could treat the GPU just like a CPU, running one program. Now people trying to get the last few percent of perf out of the GPU, get kicked down by the variability and volatility of HW scheduling ...

**6/** **@mike64_t** ^2121454911003254919

right, I think you just arrived at the mega kernel discourse from first principles, but register allocation etc is not the only reason why you want to split things into multiple kernels. I think in general composing workloads from kernels when everything has to be one giant binary is a big problem. It's the same dillema as having to recompile a PSO just because you changed some rasterizer state. Your application needs to be able to decide fast and it needs to do so along certain granularities. You already die from data type kernel variant combinatorial explosion just trying to make GEMM-likes work, now think about the possible schedules of orchestrating work for say an NN forward and backward pass. Your hyper parameters are at the end of the day runtime state and you cannot afford to actually compile all those out. I'm not sure I see any other way there than to have a JIT/graph compiler, which I am generally opposed to. I just don't see the mega kernel reacting to config state and then doing the equivalent of control flow on the GPU. That just seems bad. Glueing kernels together with a graph just happens to be a very very good paradigm to get the best of both worlds, not actually needing to have logic to decide what to do next within the kernerls, thus being able to reuse them. Also, a PDL edge is not actually that slow compared to a grid sync. I suspect most mega kernels are wasting more time managing their intra-kernel task-calling convention than they realize.
And not being able to do this is actively holding alternative hardware back to run actual training workloads. I think hardware that thinks "megakernels are the future" only win under a narrow subset of futures where flexibility of no concern while the performance benefits are close to zero. Now, hardware scheduling might sound less appealing depending on what it is you want to do, but if you view cuda graphs as a time-sharing + schedule declaration / overlap api, I think the design space is just more appealing than having to do any of this in isa space. I believe any piece of hardware that thinks this layer of scheduling must happen in ISA is creating unnecessary trouble and self-sabotaging themselves. Having *both* hardware scheduling and instruction level scheduling available to you does create *more* freedom in how you write and orchestrate kernels. There is no reason to double down on any one principle out of a sense of purism. There are cases where you just want to split things into two kernels and eat the PDL edge at a well understood point. say kernel A has associated work in kernel B, and A dependent kernel C, but C does not depend on B. Just get it out of the critical path and b can take however long it takes and you don't need to worry about the "lifetime" of A being long enough to encompass that.

**7/** **@NOTimothyLottes** ^2121457929328980217

**@mike64_t**

Man the blue check crowd has a serious advantage in text capacity :) I'm for 100% free form (not language or API limited) access to the HW. Solve problems any way you want. But APIs have evolved more to force people into certain ways of doing things, not a fan

**8/** **@mike64_t** ^2121459529997320399

**@NOTimothyLottes**

Hahah true true. Not looking back on thread splitting xD
i guess its my observation that a very good property seems to have emerged by accident here… or not so much as an accident (?)
