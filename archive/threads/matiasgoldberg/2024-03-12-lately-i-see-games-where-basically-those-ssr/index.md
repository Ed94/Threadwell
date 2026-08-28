---
title: "Lately I see games where basically \"those SSR reflections could've been planar reflections\"."
type: archive
source: twitter
source_url: "https://x.com/matiasgoldberg/status/1767548825407766692"
author: "Matías N. Goldberg"
handle: matiasgoldberg
post_id: "1767548825407766692"
date: 2024-03-12
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - matiasgoldberg
description: "Lately I see games where basically \"those SSR reflections could've been planar reflections\"."
in_reply_to: ""
---

## Source

- URL: https://x.com/matiasgoldberg/status/1767548825407766692
- Author: Matías N. Goldberg (@matiasgoldberg)
- Posted: 2024-03-12 13:50:54

## Thread

**1/** **@matiasgoldberg** ^1767548825407766692

Lately I see games where basically "those SSR reflections could've been planar reflections".

Way better quality IMO.
My guess is either inexperience/ignorance, the easiness of just toggling a post process, or the engine has lots of trouble issuing twice as many drawcalls

**2/** **@KasperArnklit** ^1767818373100925193

**@matiasgoldberg**

I wonder if the many optimizations made in some engines for rendering the same scene twice for VR also spilled back over into planar reflections being faster.

**3/** **@matiasgoldberg** ^1767920895576756533

**@KasperArnklit**

It never really occurred to me!

But one issue I see is that planar refl. need clipping planes, which can incur in additional penalties you may not want for the regular pass (like disabling depth compression or even early Z).

**4/** **@EricLengyel** ^1767932834730418646

**@matiasgoldberg** **@KasperArnklit**

You don't need an extra clipping plane for planar reflections! You can always change the projection matrix to clip at the reflection plane for free. (See FGED2, section 6.4.)

**5/** **@matiasgoldberg** ^1767943136146305373

**@EricLengyel** **@KasperArnklit**

Yeah, I know. But it loses depth precision and makes shadow mapping harder because the fudged projection should be ignored, making clipping planes the easier path.

Though yes, you can avoid clip planes by tweaking the near plane.

**6/** **@EricLengyel** ^1767957954689667439

**@matiasgoldberg** **@KasperArnklit**

In my extensive experience with this technique, depth precision is not a problem, especially if you're using reversed depth (which you should be), and shadow mapping is not affected in any way. Modifying vertex shaders to set up a user clipping plane is not easier.

**7/** **@JoaoBapt** ^1883701708511141934

**@EricLengyel** **@matiasgoldberg** **@KasperArnklit**

I remember reading the paper and I don’t remember why, but I found out it doesn’t work with infinite perspective projection.

**8/** **@EricLengyel** ^1883761292936380672

**@JoaoBapt** **@matiasgoldberg** **@KasperArnklit**

That is not correct. The modified projection matrix that puts the near plane wherever you want works just fine with an infinite perspective projection. The paper even specifically addresses that case on page 7.

**9/** **@JoaoBapt** ^1883761760714518991

**@EricLengyel** **@matiasgoldberg** **@KasperArnklit**

I’ll have to check my book when I get home. I actually read another paper where the mathematical derivation didn’t give me a lot of faith.

**10/** **@EricLengyel** ^1883763616358477849

**@JoaoBapt** **@matiasgoldberg** **@KasperArnklit**

What book? What paper? The math was worked out 20 years ago and is extremely well battle-tested. The near clip plane modification is used very effectively with infinite projections all the time in many engines. Are you really questioning this?

**11/** **@JoaoBapt** ^1883764421870457260

**@EricLengyel** **@matiasgoldberg** **@KasperArnklit**

Chill, I don’t learn any kind of science by just blind-faith believing an article when I read it. I do the math myself to verify and make sure I learned it properly. I got YOUR book, just didn’t get to that part yet. And tbh I don’t remember which paper I read anymore.

**12/** **@JoaoBapt** ^1883764588879176035

**@EricLengyel** **@matiasgoldberg** **@KasperArnklit**

I believe what you said is right, since you talked about it in the book, I just want to see it with my own eyes. That’s not a reason for dumb arguing.
