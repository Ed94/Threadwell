---
title: "\"Buffer zoo\" is more about the silly season of things needed on the Vulkan shader side to do what you actually want which is just get instruction intrinsics."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1868444111390249140"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1868444111390249140"
date: 2024-12-15
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "\"Buffer zoo\" is more about the silly season of things needed on the Vulkan shader side to do what you actually want which is just get instruction intrinsics."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/868444111390249140
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-12-15 23:52:44

## Thread

**1/**

"Buffer zoo" is more about the silly season of things needed on the Vulkan shader side to do what you actually want which is just get instruction intrinsics. Just the layout and SSBO aliasing (below) hints at brutal stupid API/shader design

![](https://pbs.twimg.com/media/Ge4LfQvWwAAwgwz?format=png&name=orig)

**2/**

@NOTimothyLottes Dxc hlsl sm 6.5 lets you index into ResourceDescriptorHeap directly and cast to whatever resource type. That and mutable vulkan descriptors, you wouldn't need to go the buffer Zoo route.... But then dxc spirv ...

**3/**

@kechogarcia Read<32,64,128>(uint64_t base, uint32_t offset, uint32_t immediate, uint32_t cacheControl, uint32_t format);

And be done with this stupid mess

**4/**

@NOTimothyLottes @kechogarcia NVidia can't just do random format conversions without it being a texture descriptor I thought?

**5/**

@axelgneiting @kechogarcia Can get the non-conversion {signed/unsigned short/int/long and half/float/double, of {1-4} components}. Which is good enough to start the interface. Then yes for NV you'd need to alias via a storage_texel_buffer to get {10:11:11,10:10:10:2,<u/s>norm*}

**6/**

@axelgneiting @kechogarcia Then there are rough edges to TEXEL_BUFFER

9-bit shared 5-bit E -> read only NV, no AMD
sRGB -> yes NV, no AMD

And a big one: NV limits to 128 M elements
{512 MiB,1GiB,2GiB} buffer size limits for {32,64,128}-bits respectively

Branches: [[archive/threads/NOTimothyLottes/2024-12-15-buffer-zoo-is-more-about-the-silly-season-of/2024-12-16-axelgneiting-im-well-aware-its-really-curious-they-still-stick]]
