---
title: "@simplex_fx @NOTimothyLottes I briefly discussed this topic in my SIGGRAPH 2022 talk."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1890383966600888652"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1890383966600888652"
date: 2025-02-14
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - simplex_fx
description: "@simplex_fx @NOTimothyLottes I briefly discussed this topic in my SIGGRAPH 2022 talk."
in_reply_to: ""
parent_post_id: "1890348863287943363"
---

## Source

- URL: https://x.com/SebAaltonen/status/1890383966600888652
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2025-02-14 12:53:53

## Branch

**1/**

@simplex_fx @NOTimothyLottes I briefly discussed this topic in my SIGGRAPH 2022 talk.  The problem is that if you write a completely custom renderer for each platform, you have LOTS of platform specific code, which is super hard to maintain when your requirements change. 5x work for refactor is not fun.

**2/**

@simplex_fx @NOTimothyLottes Also with good design, you can almost 1:1 wrap Vulkan/Metal/DX12 under the same thin wrapper, so you don't end up wasting performance in a wrapper. Now you can write your low level rendering code once.

**3/**

@simplex_fx @NOTimothyLottes Good design == use placement heaps everywhere, use argument buffers (also in Metal) so that your memory management and binding model is identical. This way you don't need to send any data though the API wrapper. Write data directly to GPU memory, then call the wrapper to draw.

**4/**

@simplex_fx @NOTimothyLottes Also separating CPU->GPU data upload completely from drawing allows you to upload data at change frequency instead of draw frequency. Many big engines are slow as they upload data per draw call. That's bad design. Couples upload/draw tightly together. Must pay for both.

**5/**

@SebAaltonen @simplex_fx @NOTimothyLottes I've seen advised to use graphics queue (supporting transfer) for cpu write once gpu draw once data (immediate data recreated every frame).
Then use separate data upload for data that suffers less frequent update (like per-instance scene data of a level editor).
Is it bad advice?

**6/**

@SebAaltonen @simplex_fx @NOTimothyLottes Would this work for mobile phones?
I thought that keeping the scene resident on the GPU relies on indirect draws with a count buffer (filled by a GPU culling computer shader) and bindless resources.
IIRC, these two are not well supported on mobile phones.

## Related

- Spine: [[archive/threads/simplex_fx/2025-02-14-hey-gpu-guys-like-sebaaltonen-notimothylottes-why]]
