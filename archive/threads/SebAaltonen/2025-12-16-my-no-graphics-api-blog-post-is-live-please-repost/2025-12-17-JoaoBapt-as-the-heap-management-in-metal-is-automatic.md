---
title: "@SebAaltonen “As the heap management in Metal is automatic, users can’t allocate texture descriptors in contiguous ranges.”"
type: archive
source: twitter
source_url: "https://x.com/JoaoBapt/status/2001189382359781675"
author: "João Baptista 🇧🇷"
handle: JoaoBapt
post_id: "2001189382359781675"
date: 2025-12-17
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen “As the heap management in Metal is automatic, users can’t allocate texture descriptors in contiguous ranges.”"
in_reply_to: ""
parent_post_id: "2001000839574643138"
---

## Source

- URL: https://x.com/JoaoBapt/status/2001189382359781675
- Author: João Baptista 🇧🇷 (@JoaoBapt)
- Posted: 2025-12-17 07:15:03

## Branch

**1/** **@JoaoBapt** ^2001189382359781675

**@SebAaltonen**

“As the heap management in Metal is automatic, users can’t allocate texture descriptors in contiguous ranges.”

Check out texture view pools, they allow for *some* manual manipulation of the texture heap: https://developer.apple.com/documentation/metal/mtltextureviewpool?language=objc

**2/** **@SebAaltonen** ^2001247130011492521

**@JoaoBapt**

I'll check. Seems to be a brand new iOS26/MacOS26 feature. 

The main idea of DX12 SM6.6 heap is that it's global. User never needs to bind it. All shaders see all textures all the time and shaders can calculate indices in the way that's most optimal.

**3/** **@SebAaltonen** ^2001256866203230585

**@JoaoBapt**

The new iOS26/MacOS26 TextureViewPool seems promising indeed. Can you create a single big pool for all your textures, similar to a SM6.6 descriptor heap? Is it performance optimal way to access all textures?

**4/** **@SebAaltonen** ^2001258734165619189

If I understood it correctly, your driver internally allocates N contiguous descriptors for each TextureViewPool in your driver's internal descriptor heap. I can ask the gpuResourceID of the first texture in the pool to know the pool's base offset in the driver managed descriptor heap?

MSL now allows adding integer offset to texture2d<T> like it was a pointer?

Basically implementing DX12 SM6.6 style heap would be possible if I allocate a one massive Metal 4 TextureViewPool and ask the gpuResourceID of the first slot. I route this baseTextureID to the shader using some side channel and add it to the texture heap index. This should work?

**5/** **@SebAaltonen** ^2001262834152612344

**@JoaoBapt**

Can't find any information of adding a integer index on a base texture2d<T> in the shader. It's definitely doable in CPU side, but seems that it's not available in the shader? Shader indexing is the crucial piece for implementing SM6.6-style global descriptor heap.

**6/** **@SebAaltonen** ^2001343034387239257

**@JoaoBapt**

As expected, that's not supported. Oh well. Almost there. CPU can do heap indexing in Metal 4.0 with this, but GPU can't. Hopefully support added soon!

**7/** **@TellowKrinkle** ^2002419484129382779

**@SebAaltonen** **@JoaoBapt**

Depends on how much you like abusing UB
This generates the expected ISA when compiled, and given that the in-memory layout is set in stone (from the CPU side), it doesn't seem too likely to break...

![](https://pbs.twimg.com/media/G8oFYbjWEAAUOeN?format=jpg&name=orig)

## Related

- Spine: [[archive/threads/SebAaltonen/2025-12-16-my-no-graphics-api-blog-post-is-live-please-repost]]
