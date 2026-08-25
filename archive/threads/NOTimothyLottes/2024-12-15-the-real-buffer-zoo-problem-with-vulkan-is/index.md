---
title: "The real \"buffer zoo\" problem with Vulkan is needing to make your HW instruction emulation macros with overcomplete both {offset, and index} inputs so the emulation can choose the correct one based on whatever crap path is required {SSBO, TEXEL_BUFFER, future pointer}"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1868435545736782009"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1868435545736782009"
date: 2024-12-15
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "The real \"buffer zoo\" problem with Vulkan is needing to make your HW instruction emulation macros with overcomplete both {offset, and index} inputs so the emulation can choose the correct one based on whatever crap path is required {SSBO, TEXEL_BUFFER, future pointer}"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1868435545736782009
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-12-15 23:18:42

## Thread

**1/** @NOTimothyLottes

The real "buffer zoo" problem with Vulkan is needing to make your HW instruction emulation macros with overcomplete both {offset, and index} inputs so the emulation can choose the correct one based on whatever crap path is required {SSBO, TEXEL_BUFFER, future pointer}

**2/** @NOTimothyLottes

TEXEL_BUFFER is needed for whatever formats one cannot load from SSBOs, and both of those require 'indexes', and whenever the IHVs actually correctly optimize the pointer extension, one needs the byte offsets instead. So deadcode removal nightmare land wins today :(
