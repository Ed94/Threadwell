---
title: "Fixed all our Vulkan bugs:"
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1869350790487523825"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1869350790487523825"
date: 2024-12-18
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Fixed all our Vulkan bugs:"
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1869350790487523825
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2024-12-18 11:55:33

## Thread

**1/** **@SebAaltonen** ^1869350790487523825

Fixed all our Vulkan bugs:
- ARM: BGR swapchain handled incorrectly (our bug)
- Qualcomm: SSAO quad flicker (driver bug)
- PowerVR: material index rounding issue (our bug)
- Intel (iGPU): subpass barriers don't work (driver bug)

Now we are ready to ship Vulkan for end users.

![](https://pbs.twimg.com/media/GfFDoE5XYAAprel?format=jpg&name=orig)

**2/** **@SebAaltonen** ^1869361815454699648

Our Vulkan backend has been in internal production for 1.5 years already. We were just waiting for Google to ship the Vulkan renderer on Flutter. We have a custom Flutter version that allows us to run our engine in the side. I carved holes to get their Vulkan device ptr, etc.
