---
title: "@SebAaltonen One of the biggest roadblocks when I was trying to learn Vulkan was the descriptor API."
type: archive
source: twitter
source_url: "https://x.com/JoaoBapt/status/1595315606349307904"
author: "João Baptista 🇧🇷"
handle: JoaoBapt
post_id: "1595315606349307904"
date: 2022-11-23
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen One of the biggest roadblocks when I was trying to learn Vulkan was the descriptor API."
in_reply_to: ""
parent_post_id: "1595091915472764928"
---

## Source

- URL: https://x.com/JoaoBapt/status/1595315606349307904
- Author: João Baptista 🇧🇷 (@JoaoBapt)
- Posted: 2022-11-23 07:17:34

## Branch

**1/** **@JoaoBapt** ^1595315606349307904

**@SebAaltonen**

One of the biggest roadblocks when I was trying to learn Vulkan was the descriptor API. I never fully understood them, and tbh the way Direct3D and Metal do is way cleaner and simpler (the argument buffers not that much, but you get it).

**2/** **@SebAaltonen** ^1595316396346540039

**@JoaoBapt**

Descriptor sets and argument buffers simply abstract a linear chunk of memory (pointer + size) containing descriptors. But the abstractions make this look super complicated. The idea is that you can change the pointer quickly at runtime (to change materials bindings, etc).

**3/** **@JoaoBapt** ^1595317094375215104

**@SebAaltonen**

Yeah, that part I got, you could even set the root constants and descriptors on D3D or just *plain write to them with the CPU* on the PS5. The argument buffer API is nice as well, though having to ‘useResource’ every one of them seems to me as defeating the point entirely.

**4/** **@SebAaltonen** ^1595318728840855553

**@JoaoBapt**

You want to use heaps instead of calling useResource separately for each argument buffer.

https://developer.apple.com/documentation/metal/mtlrendercommandencoder/3043402-useheap?language=objc

**5/** **@JoaoBapt** ^1595355410210357248

**@SebAaltonen**

Yeah, I forgot that they existed 😅 it’s been being a nightmare to learn all three APIs, especially because I skipped D3D11 (learned OpenGL instead), so it’s been quite a journey.

**6/** **@SebAaltonen** ^1595359995012517890

**@JoaoBapt**

Yeah. Metal heaps is more similar to Vulkan. Have sub-allocate things manually. Going to be reusing a lot of my memory management code from the Vulkan backend in the Metal backend.

**7/** **@JoaoBapt** ^1595360142727548928

**@SebAaltonen**

Makes sense. Though in this case you probably can try to repurpose VMA for that?

## Related

- Spine: [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics]]
