---
title: "@SebAaltonen What do you think are the chances—any chances at all—that, say, the Vulkan 2.0 API would look the way you're suggesting?"
type: archive
source: twitter
source_url: "https://x.com/Jurgus007/status/2086212585884438702"
author: "Łukasz I"
handle: Jurgus007
post_id: "2086212585884438702"
date: 2026-08-08
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen What do you think are the chances—any chances at all—that, say, the Vulkan 2.0 API would look the way you're suggesting?"
in_reply_to: ""
parent_post_id: "2086035003360583907"
---

## Source

- URL: https://x.com/Jurgus007/status/2086212585884438702
- Author: Łukasz I (@Jurgus007)
- Posted: 2026-08-08 22:06:55

## Branch

**1/** **@Jurgus007** ^2086212585884438702

**@SebAaltonen**

What do you think are the chances—any chances at all—that, say, the Vulkan 2.0 API would look the way you're suggesting?

**2/** **@SebAaltonen** ^2086372792463724961

Remove descriptor sets and descriptor pools. Make descriptor heap extension the basis for descriptors. BDA needs to be standard and GLSL BDA syntax and type safety needs work (64-bit pointers instead of integers). Also unified image layouts for barriers as default, and I really hope that resource lists in barriers could be removed. For backwards compatibility reasons they would likely keep buffer descriptors. There's still some real use cases for them. Texel buffers have type conversion and many GPUs are lacking 32-bit per-lane index for 64-bit pointer raw memory loads. You need 64-bit pointer per lane (which bloats register use slightly). Providing root data with the new push data extension is fine, but having a 64-bit pointer instead as root data would be nicer. Not a deal breaker.

**3/** **@Jurgus007** ^2086410941202084255

**@SebAaltonen**

Having watched your video again, two things are still worrying me. 1) To create a GPU pipeline, you need to specify a vertex/mesh + pixel shader combo. So we’re still faced with the ‘combination problem’ of these two graphics stages.

**4/** **@Jurgus007** ^2086411284040348143

**@SebAaltonen**

2) Sampling textures of various types, formats, etc. is ‘hidden’ within the texture descriptor, and that’s fine. shader code always looks the same, yet you can sample different types of textures. As far as I understand, this is no longer the case with the Vertex Buffer and IA.

**5/** **@Jurgus007** ^2086411457516695853

**@SebAaltonen**

Now you have to “decode” the data format in the primitive vertices yourself. This means you have to write this part of the code yourself and take responsibility for it. The consequence is that vertex shaders must be combined solely for the purpose of decoding vertex attributes.

## Related

- Spine: [[archive/threads/SebAaltonen/2026-08-08-extended-2x-version-of-my-siggraph-2026-talk]]
