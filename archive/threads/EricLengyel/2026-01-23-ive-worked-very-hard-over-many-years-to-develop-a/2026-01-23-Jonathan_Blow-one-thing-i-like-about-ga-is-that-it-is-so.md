---
title: "One thing I like about GA is that it is so systemic and makes so much sense when it comes to linear stuff."
type: archive
source: twitter
source_url: "https://x.com/Jonathan_Blow/status/2014821856772292614"
author: "Jonathan Blow"
handle: Jonathan_Blow
post_id: "2014821856772292614"
date: 2026-01-23
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - EricLengyel
description: "One thing I like about GA is that it is so systemic and makes so much sense when it comes to linear stuff."
in_reply_to: ""
parent_post_id: "2014810110493884650"
---

## Source

- URL: https://x.com/Jonathan_Blow/status/2014821856772292614
- Author: Jonathan Blow (@Jonathan_Blow)
- Posted: 2026-01-23 22:05:38

## Branch

**1/** **@Jonathan_Blow** ^2014821856772292614

One thing I like about GA is that it is so systemic and makes so much sense when it comes to linear stuff. The conformal stuff just kind of loses me though, at first glance it always looks like a lot of added complexity for small gain. What should I look at to convince myself I am wrong here?

**2/** **@EricLengyel** ^2014843525083627609

You're not wrong about the conformal stuff. While I find it convenient for expressing a small set of geometric calculations, I don't think it's very useful in general, and it certainly isn't a monument to efficiency. My book is very candid about this, going as far as calling parts of it "computationally absurd". (I also think just about all traditional presentations of CGA are quite poor and fail to convey any intuition whatsoever, which does contribute something to its lack of practical utility.)

What I find most useful in GA is not the conformal stuff but the 4D projective algebra that encompasses homogeneous coordinates, planes, Plücker coordinates, quaternions, and dual quaternions all in one nice neat framework.

The projective algebra is fully contained inside the conformal algebra, so it doesn't hurt to just have the extra conformal tools available in case you want to use them here and there. This does not require any changes to geometric representations for things not in the conformal algebra, so you wouldn't have to do anything stupid like storing five components for every point.

**3/** **@Oktahedro** ^2014971292714140079

**@EricLengyel** **@Jonathan_Blow**

wow, you are wrong on this point. PGA is fine but CGA is ultrafine. Our Universe is eminently conformal. Take a deep breath and look at the quantum level for instance.

**4/** **@EricLengyel** ^2014989505061958101

**@Oktahedro** **@Jonathan_Blow**

I’m aware. Jon and I work in the same industry, and as such, I think there is an implicit understanding between us that we’re talking about practical utility in computer graphics, collision detection, etc., and not theoretical physics. My comment does not apply universally.

## Related

- Spine: [[archive/threads/EricLengyel/2026-01-23-ive-worked-very-hard-over-many-years-to-develop-a]]
