---
title: "@NOTimothyLottes How reliable in your experience in code like that is the compilation to avoid branches?"
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1859375048550662580"
author: "Jebrim"
handle: AgileJebrim
post_id: "1859375048550662580"
date: 2024-11-20
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes How reliable in your experience in code like that is the compilation to avoid branches?"
in_reply_to: ""
parent_post_id: "1859369992355021246"
---

## Source

- URL: https://x.com/AgileJebrim/status/1859375048550662580
- Author: Jebrim (@AgileJebrim)
- Posted: 2024-11-20 23:15:31

## Branch

**1/**

@NOTimothyLottes How reliable in your experience in code like that is the compilation to avoid branches?

**2/**

@AgileJebrim Lots of stuff can get mapped by the compiler to V_CNDMASK_B32 instead of branching by using mix(a,b,bool) syntax. I rarely use branching because of how horrible the code generation is. No way to express that the common path stay code linear either, etc.

**3/**

@NOTimothyLottes I know in CUDA-land that it likes to create branches for ternaries if it contains more than 4 total instructions in a statement.

**4/**

@AgileJebrim But the real problem is lacking of explicit controls, and lacking implicit branch hints (wave-uniform/non-uniform, expected branch hit rate, etc). Better if we could just do explicit ASM style branch instructions and labels.

**5/**

@NOTimothyLottes Well I seek to ban branches entirely, so that’s the exact opposite of what I want.

**6/**

@AgileJebrim If your shader I$ is say 32 KiB and your instructions average say 8-bytes. You have 4 K instructions before you are streaming the program not just the data. Code size is actually important. And while micro level unroll is needed, macro level duplication is a problem with tiny I$

**7/**

@NOTimothyLottes I avoid the duplication of instruction patterns too. I feel it’s a failure to properly parallelize if you’re repeating the same instructions instead of data parallelizing further.

**8/**

@NOTimothyLottes One more reason why I avoid functions.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2024-11-21-32-oh-damn-32-should-probably-stop-now-until-next]]
