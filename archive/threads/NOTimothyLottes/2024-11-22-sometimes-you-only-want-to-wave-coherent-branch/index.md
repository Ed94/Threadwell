---
title: "Sometimes you only want to wave-coherent branch to something extremely rarely."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1859788005445414927"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1859788005445414927"
date: 2024-11-22
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Sometimes you only want to wave-coherent branch to something extremely rarely."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1859788005445414927
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-11-22 02:36:28

## Thread

**1/**

Sometimes you only want to wave-coherent branch to something extremely rarely. There is no good way in GLSL to describe that. You always get one branch and one disruption of the linear path [RED]. What you want is [GREEN], common path is linear and branch-free. Gotos would enable

![](https://pbs.twimg.com/media/Gc9K3dEXIAA7tGy?format=png&name=orig)

**2/**

In theory wave-coherent branch hint and then providing say a 99% taken branch taken compile hint could enable a compiler to know how to do proper code gen here

**3/**

The other thing, if you know a path is always taken by some of the lanes, and thus on AMD you want NO branches, and instead just EXEC changing, there is no way to express that either. Doing mix(,,bool) could add extra overhead vs simple EXEC masking

**4/**

This second example is why you want to be able to mix 'always-lane-divergent' branch hint, with '50% probability' meaning the HW needs to always execute both paths, and thus use EXEC masking without physical branching (assuming a good compiler)

**5/**

Also the lack of an explicit 'scalar' (aka SGPR) qualifier on variables. The compiler gets this wrong, a qualifier just fixes that problem. Non-SGPR platforms can just ignore the qualifier. And sgpr=readlane(maybeSgpr,0) can sometimes actually become a readlane (fail)

Branches: [[archive/threads/NOTimothyLottes/2024-11-22-sometimes-you-only-want-to-wave-coherent-branch/2024-11-22-AgileJebrim-shouldnt-uniform-be-a-scalar]]

**6/**

Other big thing on AMD's PC side, the HW has all these nice SALU ops which set the SCC (scalar flags register), and there is no good way to trick the compiler to doing basic stuff like branch on SALU overflow ...

**7/**

I tried using GLSL's uaddCarry() but it at the time pushed the whole operation from SALU back to VALU making the code extra horrible, and uaddCarry() and friends = basic fail, the carry is a bool in HW not an integer, silly lack of good pattern matching there applies

**8/**

Anyway this stuff is easily fixable if people just actually cared about it. It's not like you need to scrap the API or invent a new language. Just fix what we have, and people like me will use it, and teach others how to use it well too.

**9/**

Also for obvious reasons, at least provide a PRAGMA "not-stupid" that we can place in shaders to avoid all the overhead generating crap that deoptimizes code to check for junior programmer mistakes at runtime, this stuff is bloody hard (and sometimes) impossible to bypass today

**10/**

Lets add another thing, if(subgroupElect()){} to try to make stuff SALU is broken. Because subgroupElect() will do all the overhead to find the lowest active lane (even in cases the compiler should know otherwise). And if(gl_SubgroupID==0) for that also isn't well optimized

**11/**

Maybe another time we should dive into the problems with shading languages mixing branching with loads and killing all the latency hiding. But too much for this thread...
