---
title: "Oh, my RADV driver says vkGetShaderInfoAMD is available [GPU disassembly dumps]."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2074720328161411450"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2074720328161411450"
date: 2026-07-08
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Oh, my RADV driver says vkGetShaderInfoAMD is available [GPU disassembly dumps]."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2074720328161411450
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-08 05:00:47

## Thread

**1/** **@NOTimothyLottes** ^2074720328161411450

Oh, my RADV driver says vkGetShaderInfoAMD is available [GPU disassembly dumps]. Going to be exciting to see how RADV compiler does. Will definitely be filing optimization bugs, would like to help the RADV team make this the best AMD Vulkan driver that can exist.

**2/** **@NOTimothyLottes** ^2074721638378086822

One other concern was if RADV would support DEVICE_UNCACHED_BIT_AMD - and looks like RADV already has that, which means low-latency CPU/GPU communication should just work out of the box

![](https://pbs.twimg.com/media/HMrkGrMXwAA9Cr0?format=jpg&name=orig)

**3/** **@NOTimothyLottes** ^2074723430734111222

One of the pain points of doing header-free Vulkan is the VkPhysicalDeviceLimits structure. I avoid it completely and replace the structure with an equal size array of 63 64-bit values (504 bytes total). Then use direct byte offset for timestampPeriod (only thing useful in there)

![](https://pbs.twimg.com/media/HMrlR1cWQAAsqXD?format=png&name=orig)

**4/** **@NOTimothyLottes** ^2074724166956118253

The other component of vkGetPhysicalDeviceProperties that is useful is the vendorID, which is important for vendor specific engine permutations -> I use to enable vkGetShaderInfoAMD disassembly dumps automatically on all shaders

**5/** **@NOTimothyLottes** ^2074725506050642021

Next pre-device opening activity is choosing queue(s). Going to make another effort at beam racing, this time on Linux, so probably want a separate queue for presentation only. To fully decouple {dispatch, and swap}. Will see why later ...
