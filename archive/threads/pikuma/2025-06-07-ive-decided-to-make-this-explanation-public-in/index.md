---
title: "I've decided to make this explanation public, in case someone else is also interested."
type: archive
source: twitter
source_url: "https://x.com/pikuma/status/1931455040965009503"
author: "pikuma.com"
handle: pikuma
post_id: "1931455040965009503"
date: 2025-06-07
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - pikuma
description: "I've decided to make this explanation public, in case someone else is also interested."
in_reply_to: ""
---

## Source

- URL: https://x.com/pikuma/status/1931455040965009503
- Author: pikuma.com (@pikuma)
- Posted: 2025-06-07 20:55:41

## Thread

**1/** **@pikuma** ^1931455040965009503

I've decided to make this explanation public, in case someone else is also interested.

First, let's write down the operations on z without the matrix:
Pay attention to how we have a multiplication and a subtraction. Let's look at the multiplication first.
Our goal is to normalize the original z values so they are all from 0 to 1, where znear is 0 and zfar is 1.
Keep in mind that we are not showing here the perspective divide (division by the original z). The actual normalization (from 0 to 1) will occur after we divide things by the original z later. In other words, because the normalized z value will (in the perspective divide) still be divided by the original z value, it is normalized between 0 and zfar. The division by the original z value (inside w) will make it actually normalized between 0 and 1.

Therefore, the first thing we do is to normalize values between znear and zfar. This can be achieved using the fraction 1/(zfar-znear).
 At the same time, we want our z values that are equal to zfar to be transformed to zfar, since the perspective divide is going to normalize that back to 1. We can accomplish this by scaling things by zfar. This gives us an intermediate result of zfar/(zfar-znear).
These steps take care of the zfar mapping and explain the multiplication part of our formula.

...continues 👇

![](https://pbs.twimg.com/media/Gs3l5rdWcAALHS6?format=png&name=orig)
![](https://pbs.twimg.com/media/Gs3mAbnW4AAW3WJ?format=jpg&name=orig)
![](https://pbs.twimg.com/media/Gs3mdZgXcAArODD?format=png&name=orig)
![](https://pbs.twimg.com/media/Gs3mmdXWcAAZ57r?format=png&name=orig)

**2/** **@pikuma** ^1931455044877971797

Finally, we also want the z values that are equal to znear to be transformed to 0. We can accomplish that by offsetting (subtracting) *something* from the previous intermediate result. This is what we called the "difference between the eye and the near plane" in our lecture.

Imagine for a second that we have a z value that is exactly znear. If we multiply this value with the previous intermediate result zfar/(zfar-znear), we get (znear*zfar) / (zfar - znear). Therefore, this is the "correction" we need to apply to transform our z values that are equal to znear to be equal to 0.
All of these steps will give us the final entries of the projection matrix to help us perform the desired z normalization.
In our lectures, I also chose to call zfar/(zfar-znear) as lambda (λ). This is just notation and does not change anything in the meaning of our z normalization formula.
After we multiply our vertex with the projection matrix we proceed to do the perspective divide (division by the original depth value, which is saved inside w). Only after the perspective divide is that our z value will be in the range [0,1] for depth values between znear and zfar.

I hope this breakdown helps you connect things. I like to discuss things in a high-level and postpone an actual algebraic derivation if possible. If you want a proper derivation of the perspective projection matrix, one of our students created a great video with his explanation of it: https://www.youtube.com/watch?v=k_L6edKHKfA.

![](https://pbs.twimg.com/media/Gs3nNX5WUAAHfSs?format=png&name=orig)
![](https://pbs.twimg.com/media/Gs3nk5oWEAA-q_K?format=png&name=orig)

**3/** **@EricLengyel** ^1931542043433836638

**@pikuma**

Please note that ever since z buffers have been floating-point (about a decade now), the best practice is to map znear to 1 and zfar to 0 and use a reversed depth test. This gives you much greater depth precision for objects rendered far from the camera. See FGED2, Chapter 6.

**4/** **@pikuma** ^1931669715165860205

**@EricLengyel**

Right on! I was discussing this on a Discord server with HiddenAsbestos a couple of months ago for his flight sim experiments. :)
