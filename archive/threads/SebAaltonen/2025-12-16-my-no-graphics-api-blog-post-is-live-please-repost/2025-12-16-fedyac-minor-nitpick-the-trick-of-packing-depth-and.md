---
title: "@SebAaltonen Minor nitpick: The trick of packing depth and color into a 64-bit integer and using an atomicMin to emulate the depth test had already been used in 2014 by @pixeljetstream one year before Dreams and a long time before Nanite 😉"
type: archive
source: twitter
source_url: "https://x.com/fedyac/status/2001074930469703725"
author: "Fedy ABI-CHAHLA"
handle: fedyac
post_id: "2001074930469703725"
date: 2025-12-16
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen Minor nitpick: The trick of packing depth and color into a 64-bit integer and using an atomicMin to emulate the depth test had already been used in 2014 by @pixeljetstream one year before Dreams and a long time before Nanite 😉"
in_reply_to: ""
parent_post_id: "2001000839574643138"
---

## Source

- URL: https://x.com/fedyac/status/2001074930469703725
- Author: Fedy ABI-CHAHLA (@fedyac)
- Posted: 2025-12-16 23:40:16

## Branch

**1/** **@fedyac** ^2001074930469703725

**@SebAaltonen**

Minor nitpick: The trick of packing depth and color into a 64-bit integer and using an atomicMin to emulate the depth test had already been used in 2014 by @pixeljetstream one year before Dreams and a long time before Nanite 😉

![](https://pbs.twimg.com/media/G8U_CvqXYAIy7s2?format=jpg&name=orig)

**2/** **@SebAaltonen** ^2001198438206103958

Media Molecule Dreams presentation was at SIGGRAPH 2015. They spent years on the tech, so I would assume they used the uint64 atomic trick before 2014. I presented Ubisoft GPU-driven renderer publicly also at SIGGRAPH 2015, but had internal UDC (Ubisoft Developer Conference) presentations at 2013 and 2014. Tech like this has usually at least 2 year lead time before surfacing publicly. @mmalex also told me that they had independently came up with the same two-phase occlusion culling algorithm that I presented at SIGGRAPH 2015. Maybe Alex wants to comment on this.

**3/** **@fedyac** ^2001204502775361603

**@SebAaltonen** **@pixeljetstream**

Indeed, in this kind of situation it’s always difficult to know who is really behind the trick. It’s so simple yet so clever and in the end it hardly matters who came up with it. In fact, I just wanted to take the opportunity to highlight the great work of @pixeljetstream

## Related

- Spine: [[archive/threads/SebAaltonen/2025-12-16-my-no-graphics-api-blog-post-is-live-please-repost]]
