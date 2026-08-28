---
title: "Assuming the risk of appearing extremely dumb in front of everyone here but, how would you find and explain your rationale for the value of the angle β in the diagram below? Someone told me that my approach is wrong so I just want to check that I'm not going crazy."
type: archive
source: twitter
source_url: "https://x.com/pikuma/status/1960444602227269928"
author: "pikuma.com"
handle: pikuma
post_id: "1960444602227269928"
date: 2025-08-26
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - pikuma
description: "Assuming the risk of appearing extremely dumb in front of everyone here but, how would you find and explain your rationale for the value of the angle β in the diagram below? Someone told me that my approach is wrong so I just want to check that I'm not going crazy."
in_reply_to: ""
---

## Source

- URL: https://x.com/pikuma/status/1960444602227269928
- Author: pikuma.com (@pikuma)
- Posted: 2025-08-26 20:49:51

## Thread

**1/** **@pikuma** ^1960444602227269928

Assuming the risk of appearing extremely dumb in front of everyone here but, how would you find and explain your rationale for the value of the angle β in the diagram below? Someone told me that my approach is wrong so I just want to check that I'm not going crazy. 😐

![](https://pbs.twimg.com/media/GzTl-eyXwAAxMV0?format=jpg&name=orig)

**2/** **@EricLengyel** ^1960464041023070434

I see nothing wrong with thinking of β as the angle rotated away from the −x axis as you open the field of view from the z axis by the angle fov/2 = β. But if it's the normal vector you're ultimately after, I think it's best to compute with the aspect ratio s = w/h and focal length g = s / tan(fov/2). The unit-length inward-pointing normal vector of the right frustum plane is then simply (−g, 0, s) / sqrt(g² + s²). The other three side planes have similarly simple forms in terms of g and s. See FGED2, Section 6.1 for more details.

**3/** **@pikuma** ^1960471322858770840

**@EricLengyel**

Thank you. 💪 This was recorded years ago and I'm thinking of re-designing this module. I'll definitely consider your take. Even though this is just computed once I salwe the sqrts so I want to think about proper cost tomorrow with a bit more time and with a clear mind.

**4/** **@KentoAsashima** ^1960778289288765939

**@pikuma** **@EricLengyel**

Why not the Gribb and Hartmann method as outlined by @rygorous where we use the perspective matrix axes? See https://fgiesen.wordpress.com/2012/08/31/frustum-planes-from-the-projection-matrix/

The extremes of our frustum are where the different axis components will be 1 or -1 thus we can use the corresponding axes directly.

Branches: [[archive/threads/pikuma/2025-08-26-assuming-the-risk-of-appearing-extremely-dumb-in/2025-08-27-EricLengyel-you-could-but-the-information-needed-to-construct]]
