---
title: "@BelgianRenderer @KostasAAA @Nicolas_Lopez_ Apparently uniformity analysis is hard."
type: archive
source: twitter
source_url: "https://x.com/MyNameIsMJP/status/1782636381720006711"
author: "Matt Pettineo"
handle: MyNameIsMJP
post_id: "1782636381720006711"
date: 2024-04-23
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - MyNameIsMJP
description: "@BelgianRenderer @KostasAAA @Nicolas_Lopez_ Apparently uniformity analysis is hard."
in_reply_to: ""
---

## Source

- URL: https://x.com/MyNameIsMJP/status/1782636381720006711
- Author: Matt Pettineo (@MyNameIsMJP)
- Posted: 2024-04-23 05:03:27

## Thread

**1/**

@BelgianRenderer @KostasAAA @Nicolas_Lopez_ Apparently uniformity analysis is hard. 🙁

**2/**

@MyNameIsMJP @BelgianRenderer @Nicolas_Lopez_ If uniformity can't be deduced, the compiler could be conservative and assume divergence. If it guessed wrong, the waterfall loop won't be executed and all threads will use the same index. Also, the shader author could help the compiler with a UniformResourceIndex qualifier.

**3/**

@KostasAAA @BelgianRenderer @Nicolas_Lopez_ Yeah I tend to agree that assuming non-uniformity by default for descriptor indexing would have been a better path, with some better language support for explicit tagging of uniform variables. Maybe in HLSL 2027. 🙂

**4/**

@MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ Uniformity is the fast path, it would be horrible to tax the fast path for the sake of things designed to be slow (aka using resource divergence). The right thing to do is place in explicit uniform/nonuniform qualifiers into the languages so it's explicit.

**5/**

@NOTimothyLottes @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ We do nuri for almost all our access (we sometimes turn it off because of badly readable Isa on amd). However the performance impact is in the noise, not all hw resolves this in the shader cores.

**6/**

@JasperBekkers @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ NV doesn't advertise this: 32-byte sector size (even with 128-byte lines) mixed with per lane IPs (so you can pipeline latency of divergent accesses) is all about shifting the perf cliff of bad behavior enough to win benchmarks, it is still a cliff (look at ALU utilization) ...

**7/**

@JasperBekkers @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ AMD never invested in pipelining divergent latency, and their compiler compounds this by serializing a lot of other things that shouldn't be serialized ...

**8/**

@JasperBekkers @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ If one is already into the perf cliff, it's easy on AMD to compound perf debt to the point something can never be optimized, and maybe that's ok if time-to-market/ease-of-use/etc is the primary goal ...

**9/**

@JasperBekkers @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ There are cases where AMD's compiler is still failing hard on UNIFORM (aka wave coherent) multi-resource access: zero latency hiding -> every resource is a worst case serialization of {fetch descriptor, wait, sample} with zero pipelining ... example below

![](https://pbs.twimg.com/media/GL7p5vJXUAECnVi?format=png&name=orig)

**10/**

@JasperBekkers @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ Or this case where the images get batched, but the descriptors accesses are serialized (below) ... so it's easy sometimes to assume NURI is not that expensive because the compiler already shot itself in the face (which is quite common in high complexity material shading).

![](https://pbs.twimg.com/media/GL7rS7uWsAEebjc?format=png&name=orig)

**11/**

@NOTimothyLottes @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ Most of the time for us the resource access is uniform,  so the overhead is just a few waves to test this though.

**12/**

@JasperBekkers @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ If the whole shader coherently branches into uniform vs non-uniform material paths, sure that can work if the non-uniform path is almost never used, and the compiler doesn't choak on the register pressure of the non-uniform code path.

**13/**

@JasperBekkers @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ At least for the sake of learnings for others, I'll continue down the compiler rabbit hole a little more ... even serialized latency of K$ (constant) HITs (all in the cache) will destroy shader perf (a single hit is like 30 some clocks). This pattern happens on AMD today still.

![](https://pbs.twimg.com/media/GL7uT1wXoAA7CQj?format=png&name=orig)

**14/**

@JasperBekkers @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ And as for 'fixing' bad programmer behavior via the compiler, lets look at atomicAdd() behavior. First the compiler will burn the overhead to elect an active lane even when the compiler statically knows lane zero is active (simple example below).

![](https://pbs.twimg.com/media/GL7wLb8WgAEicQD?format=png&name=orig)

**15/**

@JasperBekkers @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ Try to out smart it like this,

int k=readOnlySsbo[1];
if(int(gl_LocalInvocationID.x)==0){atomicAdd(adr, k);}

It fights back, and makes something even worse. [RED] ... see the multiply by active lane count ...

![](https://pbs.twimg.com/media/GL7xh8ZWsAArlkO?format=png&name=orig)

**16/**

@JasperBekkers @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ And sometimes it gets really squirrly and throws in a full wave reduction (see the DPP ops). When the good dev is just trying to do an already predicated to lane zero atomic ADD ...

![](https://pbs.twimg.com/media/GL7yB5cXIAACo5E?format=png&name=orig)

**17/**

@JasperBekkers @MyNameIsMJP @KostasAAA @BelgianRenderer @Nicolas_Lopez_ So if any solution depends on trusting a compiler to implicitly do the right thing, I'd be very very concerned, because they don't. Compiler size perf 'fixes' are brittle, break easy, and become massive nightmares for programmers who know what they are doing.
