---
title: "@NOTimothyLottes IMO code compilation is inherently sequential+ \"execution contextual\", dynamic logic execution to get the binary as the essence vs a static lang"
type: archive
source: twitter
source_url: "https://x.com/onatt0/status/1917651417487036446"
author: "on@☦️"
handle: onatt0
post_id: "1917651417487036446"
date: 2025-04-30
archived: 2026-08-23
status: draft
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes IMO code compilation is inherently sequential+ \"execution contextual\", dynamic logic execution to get the binary as the essence vs a static lang"
in_reply_to: ""
parent_post_id: "1917646466417381426"
---

## Source

- URL: https://x.com/onatt0/status/1917651417487036446
- Author: on@☦️ (@onatt0)
- Posted: 2025-04-30 18:45:00

## Branch

**1/**

@NOTimothyLottes IMO code compilation is inherently sequential+ "execution contextual", dynamic logic execution to get the binary as the essence vs a static lang

codegen with execution on GPU could work as 2-items(vreg)/stack and 32K cells per lane for AI to map code to data instead of weights?

**2/**

@onatt0 So for x86 I've many times written code gen with extra nop-prefix padding to fix all instructions to a multiple of known 32-bits. Which means you know in advance sizing of everything, then you can easily do parallel code generation. So need not necessarily all be serial

**3/**

@onatt0 However I'm often building then instantly using code while generating a baked binary to use later, so that regard much is inherently serially dependent. This bootstrapping technique is perhaps one the great things to learn from things like color forth IMO.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-04-30-3-i-got-side-tracked-by-building-a-language-that]]
