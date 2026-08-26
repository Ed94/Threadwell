---
title: "@NOTimothyLottes Humor me… have you tried entering in atomicAdd(adr,lane==0?v:0)? How bad is it relative to the rest?"
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1870948791534203086"
author: "Jebrim"
handle: AgileJebrim
post_id: "1870948791534203086"
date: 2024-12-22
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Humor me… have you tried entering in atomicAdd(adr,lane==0?v:0)? How bad is it relative to the rest?"
in_reply_to: ""
parent_post_id: "1870942850684420564"
---

## Source

- URL: https://x.com/AgileJebrim/status/1870948791534203086
- Author: Jebrim (@AgileJebrim)
- Posted: 2024-12-22 21:45:27

## Branch

**1/** **@AgileJebrim** ^1870948791534203086

**@NOTimothyLottes**

Humor me… have you tried entering in atomicAdd(adr,lane==0?v:0)? How bad is it relative to the rest?

**2/** **@NOTimothyLottes** ^1870953014481269098

**@AgileJebrim**

You cannot get that behavior because the driver will "fix" it for you. There had been so many bad programmers not predicating atomics that the IHVs had been forced to workaround (too the expense of everyone who had optimized correctly)

**3/** **@AgileJebrim** ^1870953397920129344

**@NOTimothyLottes**

The driver is going to replace my code to what?

**4/** **@AgileJebrim** ^1870954001585607042

**@NOTimothyLottes**

This is why I said humor me. I’m frankly curious to see what performance it’ll get on your test suite. Just try it.

**5/** **@NOTimothyLottes** ^1870958724476461290

**@AgileJebrim**

110% if dividing by the type of the prior worst. So it's a bunch slower than the prior worst case. But I don't have NV's disassembly, so not sure exactly what it did under the hood.

**6/** **@NOTimothyLottes** ^1870961042257236009

**@AgileJebrim**

If we look at AMD disassembly for atomicAdd'ing "gl_LocalInvocationID.x==0?256:0" you will see the AMD driver do a wave-op ADD reduction (highlighted) and I'd suspect the same from NVIDIA. Note the atomic at the end of the shader uses my trick (and sums the runtime).

![](https://pbs.twimg.com/media/Gfb82ROXIAAtJff?format=png&name=orig)

**7/** **@AgileJebrim** ^1870962166796632486

**@NOTimothyLottes**

Even though it knows it’s 0 it’ll still waste time reducing? Lame.

**8/** **@NOTimothyLottes** ^1870963440485101720

**@AgileJebrim**

There have traditionally been a lot of driver workarounds in this area (like using ballot and bitcount if the adder is 1, etc). And I remember as far back as being at NV (so more than a decade ago) and having this same problem of NV drivers breaking perf of pre-optimized shaders.

**9/** **@NOTimothyLottes** ^1870963879255101507

**@AgileJebrim**

I do find it interesting that it took me a decade to figure out a proper good workaround. So yeah, I'm the "idiot" too. But I'm one workaround less of an idiot this week, which is progress.

**10/** **@AgileJebrim** ^1870964580085555600

**@NOTimothyLottes**

It’d be nice if there were a way to configure the optimizer settings like you can do with many compilers.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2024-12-22-fixing-atomicadd-benchmarking-amd-nv]]
