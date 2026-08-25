---
title: "@GustavSterbrant So I don't know that SPIR-V vs OpTypeInt 24 question, but if someone didn't write tests for that it's likely never been setup to be pattern matched."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1868712285675671711"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1868712285675671711"
date: 2024-12-16
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@GustavSterbrant So I don't know that SPIR-V vs OpTypeInt 24 question, but if someone didn't write tests for that it's likely never been setup to be pattern matched."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1868712285675671711
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-12-16 17:38:22

## Thread

**1/** @NOTimothyLottes

@GustavSterbrant

So I don't know that SPIR-V vs OpTypeInt 24 question, but if someone didn't write tests for that it's likely never been setup to be pattern matched. Most of the problems I see cannot be fixed just by bypassing GLSL and doing SPIR-V directly. So not yet tempted to write a new SL

**2/** @AgileJebrim

@NOTimothyLottes @GustavSterbrant

If you’re targeting a console with AMD hardware, why don’t you just rewrite the backend compiler? I assume you have the source for it too, so it’s more tweaking an existing compiler than anything else?

**3/** @NOTimothyLottes

@AgileJebrim @GustavSterbrant

At-home stuff (aka non-employer) targets Vulkan Windows mostly (unfortunately). No interface in AMD's Windows driver to load binary shaders into Vulkan. If SteamOS ever fully took over PC gaming, then certainly I'd just go direct to the AMD kernel driver and bypass user-mode VK

**4/** @NOTimothyLottes

@AgileJebrim @GustavSterbrant

Also I wouldn't just modify an existing compiler, I'd just write an assembler specific for GCN/RDNA/whateversNext family.

Branches: [[archive/threads/NOTimothyLottes/2024-12-16-so-i-dont-know-that-spir-v-vs-optypeint-24/2024-12-16-AgileJebrim-fair-enough-current-compilers-are-a-bloated-mess]]
