---
title: "@EricLengyel trying to use the structure buffer described in FGED2 and having big troubles with the eye space depth storage.."
type: archive
source: twitter
source_url: "https://x.com/no1zex/status/1216882677476884480"
author: "Kamil N"
handle: no1zex
post_id: "1216882677476884480"
date: 2020-01-14
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - no1zex
description: "@EricLengyel trying to use the structure buffer described in FGED2 and having big troubles with the eye space depth storage.."
in_reply_to: ""
---

## Source

- URL: https://x.com/no1zex/status/1216882677476884480
- Author: Kamil N (@no1zex)
- Posted: 2020-01-14 00:40:13

## Thread

**1/** **@no1zex** ^1216882677476884480

**@EricLengyel**

trying to use the structure buffer described in FGED2 and having big troubles with the eye space depth storage.. I'm using OpenGL but should not be much different, yet I get a very visible banding when visualising buffer (and also problems in SSAO and other techs)

![](https://pbs.twimg.com/media/EOM8V74WkAAvNjq?format=png&name=orig)

**2/** **@no1zex** ^1216883067740217345

**@EricLengyel**

Any idea what could be wrong there? I'm using GL counterparts to convert between float<>uint, splitting it with a mask then reconstructing, but the banding persists - I spent week on this and I'm running out of ideas.. the depth I use is: -(viewMatrix * (modelMatrix * vertPos)).z

**3/** **@no1zex** ^1216884175661404165

**@EricLengyel**

![](https://pbs.twimg.com/media/EOM9tRMXkAAElrk?format=png&name=orig)

**4/** **@EricLengyel** ^1216889215436279810

**@no1zex**

Please try using

float eyeDepth = 1.0 / gl_FragCoord.w;

just to make sure you've got the right values. This is what I use in the Tombstone Engine.

**5/** **@no1zex** ^1216889878786592770

**@EricLengyel**

Ah, I used it before and just today I converted it to the formula I posted above - I wasn't 100% sure I'm using the right output. So I can confirm that I get exact same results when using 1.0 / gl_FragCoord.w :/ Something else must be off - vectorScale calculation?

**6/** **@no1zex** ^1216890281481601026

**@EricLengyel**

![](https://pbs.twimg.com/media/EONDQppWkAUSBsL?format=png&name=orig)

**7/** **@no1zex** ^1216891743343382529

**@EricLengyel**

Filled it with intermediate results:

![](https://pbs.twimg.com/media/EONElv-XUAI9MP6?format=png&name=orig)

**8/** **@EricLengyel** ^1216892829781282816

**@no1zex**

Hmm. Your depth image looks right to me, so I would think the problem is completely in the SSAO part. For reference, here are some quick captures I just made. The first shows the depth in the structure buffer, and the second shows the values in the occlusion buffer.

<video controls src="https://video.twimg.com/ext_tw_video/1216892726026752001/pu/vid/1280x720/EyQhnd6tWPYIgjwZ.mp4?tag=10"></video>

**9/** **@EricLengyel** ^1216892960849059840

**@no1zex**

<video controls src="https://video.twimg.com/ext_tw_video/1216892867722919936/pu/vid/1280x720/BMvR-Kh8fe4Cx7ha.mp4?tag=10"></video>

**10/** **@EricLengyel** ^1216893458952015872

**@no1zex**

I would characterize what I see in your occlusion image more as "streaking" instead of "banding" because it looks like the values are inaccurate as opposed to merely imprecise. Let me look a little closer, and I'll see if I can come up with some things to check...

**11/** **@no1zex** ^1216894303785639936

**@EricLengyel**

Sure, thanks a lot! I can provide debug outputs from any value in SSAO shader, but it mainly breaks in the sampling of one of 4th neighbours. And like I mentioned, changing 1.0/scale to 1.0/z0 actually gives me any results, instead of very incorrect artifacts

**12/** **@no1zex** ^1216895252595924995

**@EricLengyel**

Also worth mentioning that what you see is using the scale = 1.0 / z0, which is different than in books. When I use scale - 1.0 / scale (line after normal calculation) it breaks really bad, I'll show video

**13/** **@no1zex** ^1216896049400467457

**@EricLengyel**

<video controls src="https://video.twimg.com/ext_tw_video/1216895942881894400/pu/vid/1148x720/vec33F6z0uJY2qf2.mp4?tag=10"></video>

**14/** **@no1zex** ^1216896113774600192

**@EricLengyel**

The above is with

![](https://pbs.twimg.com/media/EONIkJHX4AAeiKM?format=png&name=orig)

**15/** **@EricLengyel** ^1216896803745882112

**@no1zex**

I checked your value of vectorScale, and it is fine. That's not the problem.

**16/** **@no1zex** ^1216897457260548096

**@EricLengyel**

What is really interesting is that the output from SSAO changes really abruptly when moving camera while using scale=1/scale line, the calculated v vector for the sample is also very unstable, changing with every camera movement.. I assume the pixelCoord is just 0..1 frag uv?

**17/** **@EricLengyel** ^1216898637348737029

**@no1zex**

No, pixelCoord is gl_FragCoord.xy, which ranges over the resolution of the render target at pixel centers. So the x coordinate should be 0.5 through 1679.5, for example.

**18/** **@EricLengyel** ^1216899302749962241

**@no1zex**

Your shader code is essentially identical to what I use in the Tombstone Engine. I don't see a problem there.

**19/** **@no1zex** ^1216899513492873219

**@EricLengyel**

Really weird. But when I use gl_FragCoord I only get blinking screen which changes values for whole render target. So basically pixelCoord = gl_FragCoord.xy

**20/** **@no1zex** ^1216899901172469760

**@EricLengyel**

I suppose maybe it assumes the texture is in repeat mode?

**21/** **@EricLengyel** ^1216900742629343232

**@no1zex**

Just to make sure, your structure buffer and occlusion buffers are all being treated as GL_TEXTURE_RECTANGLE textures, right?

**22/** **@no1zex** ^1216901582614355968

**@EricLengyel**

Ouch.. no, that's just GL_TEXTURE_2D... I guess I missed some information somewhere then, I'll quickly write support for this and see how it behaves with GL_TEXTURE_RECTANGLE instead, will get back to you in few minutes.

**23/** **@no1zex** ^1216904207900532738

**@EricLengyel**

After enabling TEXTURE_RECTANGLE for structure buffer and mapping to [0, 1] range

![](https://pbs.twimg.com/media/EONP7JPWkAA0V_Y?format=jpg&name=orig)

**24/** **@EricLengyel** ^1216906365962092544

**@no1zex**

That looks better. (Using rectangle textures is just a lot easier, IMO. You could use 2D textures, but you'd have to divide the texcoords by the render target dimensions each time you accessed the structure buffer.)

**25/** **@no1zex** ^1216914610382688258

**@EricLengyel**

Ok took me a while as I didn't have Rect support in my engine... now it looks a bit more stable though the occlusion is uglier than it was, especially when zoomed out a bit:

![](https://pbs.twimg.com/media/EONZYp6XsAEe8PK?format=png&name=orig)

**26/** **@no1zex** ^1216915590532780032

**@EricLengyel**

Samplers for these RECTANGLE textures should be GL_NEAREST and GL_CLAMP_TO_EDGE yes?

**27/** **@no1zex** ^1216917126126231552

**@EricLengyel**

Hmm, got this... looks a bit more like it but still something is off...

![](https://pbs.twimg.com/media/EONbq4LX4AAvKpN?format=jpg&name=orig)

**28/** **@no1zex** ^1216917192131993602

**@EricLengyel**

![](https://pbs.twimg.com/media/EONbvAMX4AIHvsp?format=png&name=orig)

**29/** **@no1zex** ^1216920995321335808

**@EricLengyel**

ok, I broke sampling rotations when I changed everything to RECT and used NEAREST instead of LINEAR which helps with blurring... now it looks pretty good!

![](https://pbs.twimg.com/media/EONfMIeWsAIsclR?format=jpg&name=orig)

**30/** **@no1zex** ^1216921240520351746

**@EricLengyel**

although I still can see some artifacts sneaking in when I zoom out above the castle - you can see the "streaks of "occlusion" that should not be there

![](https://pbs.twimg.com/media/EONfaefXUAEi67z?format=jpg&name=orig)

**31/** **@EricLengyel** ^1216921727453687809

**@no1zex**

Looking much better!

To clarify about the rotation texture -- You do want that to be 2D, and it will be repeated a lot so that every little 4x4 neighborhood gets the same pattern.

The streaks in the far away shots definitely are not right.

**32/** **@no1zex** ^1216923404181409792

**@EricLengyel**

Yeah they're way less invasive than before, and when actually used as final ambient factor they appear as a slightly darker "band" from far away - I'd really like to find what's causing this. But after switching to rectangle textures it works much more stable and better

**33/** **@no1zex** ^1216923767093460992

**@EricLengyel**

Thanks for all the help, much appreciated - I would never figure out that switching to rectangle textures can help. Somehow I missed the "rect" mentions in book shaders, or considered this irrelevant as I never used rectangle textures before.

**34/** **@no1zex** ^1216924603039342593

**@EricLengyel**

from very far away these get much more visible

![](https://pbs.twimg.com/media/EONieObWoAABAoo?format=jpg&name=orig)

**35/** **@EricLengyel** ^1216950620055162880

**@no1zex**

Unfortunately, I don't have an ideas at the moment about what might be causing those streaks. I'll let you know if anything pops into my head.

**36/** **@EricLengyel** ^1216952720147374081

**@no1zex**

This kind of problem is very typical of computer graphics development. Sometimes you just have to stare at it for a while and think about every little detail until you finally stumble upon the answer. Once in a while, I'll be stumped for days at a time over a simple oversight.

**37/** **@no1zex** ^1217172959628009473

**@EricLengyel**

Oh yeah, it is :) I think, after looking at all possible ways to debug it and trying things, that the vectorScale is slightly wrong. I tweaked it for radians, for degrees and there are cases where this almost works correctly, without banding.

**38/** **@no1zex** ^1217173682730274818

**@EricLengyel**

Unfortunately the full equation for vectorScale was never derived in full, could you maybe show how you calculate it in your engine, doesn't have to be more than the calculation itself + units used (radians/degrees etc if anything like this matters)

**39/** **@no1zex** ^1217181666759843847

**@EricLengyel**

![](https://pbs.twimg.com/media/EORMRQEXkAA2zNA?format=jpg&name=orig)

**40/** **@EricLengyel** ^1217206798890881024

**@no1zex**

Looking back at your calculation, your fovy calculation is missing some factors of 2, but you don't really need that. Using Equation (6.1), just calculate g from fovx:

g = aspectRatio * tan(fovx * 0.5);

If fovx = 90 degrees, then g = aspectRatio.

**41/** **@EricLengyel** ^1217207312479186944

**@no1zex**

I calculate vectorScale as 2.0 / (screenSize.y * g). This is the same thing you're doing since screenSize.y = screenSize.x / aspectRatio.
