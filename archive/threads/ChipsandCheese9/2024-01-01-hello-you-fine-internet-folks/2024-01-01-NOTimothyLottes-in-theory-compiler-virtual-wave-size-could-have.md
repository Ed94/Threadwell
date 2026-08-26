---
title: "@ChipsandCheese9 In theory compiler virtual wave size could have perf affects on modern Intel arch."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1741876953345405010"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1741876953345405010"
date: 2024-01-01
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - ChipsandCheese9
description: "@ChipsandCheese9 In theory compiler virtual wave size could have perf affects on modern Intel arch."
in_reply_to: ""
parent_post_id: "1741871612960600471"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1741876953345405010
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-01-01 17:40:02

## Branch

**1/** **@NOTimothyLottes** ^1741876953345405010

**@ChipsandCheese9**

In theory compiler virtual wave size could have perf affects on modern Intel arch. I always try for 16-wide on Intel.

**2/** **@lamchester** ^1742027618818683331

**@NOTimothyLottes** **@ChipsandCheese9**

Intel's compiler used wave16 for most of the main test loop. Unfortunately I don't know of a way to tell the compiler to use a certain wave size.

![](https://pbs.twimg.com/media/GCzslNKaEAAzNmg?format=png&name=orig)

**3/** **@0x22h** ^1742464332439634405

**@lamchester** **@NOTimothyLottes** **@ChipsandCheese9**

You can set the wave width through HLSL 6.6. However, Intel's new driver has removed Wave8 support for GPUs before DG2, and older drivers can still use Wave8.

**4/** **@lamchester** ^1742578005405507676

**@0x22h** **@NOTimothyLottes** **@ChipsandCheese9**

HLSL is a DirectX thing, not OpenCL. Also there's no way to guarantee a particular wave size is available on a particular GPU. Different architectures have different supported wave sizes

## Related

- Spine: [[archive/threads/ChipsandCheese9/2024-01-01-hello-you-fine-internet-folks]]
