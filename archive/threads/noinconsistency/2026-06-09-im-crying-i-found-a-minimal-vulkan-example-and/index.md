---
title: "i'm crying i found a \"minimal\" vulkan example and the file has 2,000 lines of C++"
type: archive
source: twitter
source_url: "https://x.com/noinconsistency/status/2064363755668980006"
author: "♡ mari/cohe ♡"
handle: noinconsistency
post_id: "2064363755668980006"
date: 2026-06-09
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - noinconsistency
description: "i'm crying i found a \"minimal\" vulkan example and the file has 2,000 lines of C++"
in_reply_to: ""
---

## Source

- URL: https://x.com/noinconsistency/status/2064363755668980006
- Author: ♡ mari/cohe ♡ (@noinconsistency)
- Posted: 2026-06-09 15:07:28

## Thread

**1/** **@noinconsistency** ^2064363755668980006

i'm crying i found a "minimal" vulkan example and the file has 2,000 lines of C++

**2/** **@AgileJebrim** ^2064749095428751374

**@noinconsistency**

It’s possible to do it in about 300-400 lines.

**3/** **@0xglitchbyte** ^2064792413512569284

**@AgileJebrim** **@noinconsistency**

VulkanHPP?

**4/** **@AgileJebrim** ^2064796581363122390

**@0xglitchbyte** **@noinconsistency**

-

Compute shaders

**5/** **@0xglitchbyte** ^2064815411229520276

**@AgileJebrim** **@noinconsistency**

While technically possible, arent shaders usually for compute intensive tasks such as physics simulations or image manipulation? Seem overkill to render a triangle

**6/** **@AgileJebrim** ^2064817916806037992

**@0xglitchbyte** **@noinconsistency**

Why assume it has to be a triangle? A simple screen space gradient would suffice.

**7/** **@AgileJebrim** ^2064818925162861033

**@0xglitchbyte** **@noinconsistency**

Compute shaders can be used for anything. Vertex and fragment shaders are really just abstractions built on top of them.

**8/** **@0xglitchbyte** ^2065421752511942912

**@AgileJebrim** **@noinconsistency**

Triangles seems to be the “hello world” of graphics programming. 

I’ll explore this.

**9/** **@AgileJebrim** ^2065422960085598261

**@0xglitchbyte** **@noinconsistency**

Only because the interface they’re using is one based around triangular rasterization. If you ditch the triangle-based pipeline, then it’s not really suitable as a Hello World. Here’s a screen space alternative.

![](https://pbs.twimg.com/media/HKnbPEaWUAANEIv?format=jpg&name=orig)
