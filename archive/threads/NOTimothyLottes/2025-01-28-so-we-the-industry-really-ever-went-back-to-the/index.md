---
title: "So we (the industry) really ever went back to the MSAA based TAA combinations and applied everything we learned in the past decade ..."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1884282476195110998"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1884282476195110998"
date: 2025-01-28
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "So we (the industry) really ever went back to the MSAA based TAA combinations and applied everything we learned in the past decade ..."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1884282476195110998
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-01-28 16:48:45

## Thread

**1/**

So we (the industry) really ever went back to the MSAA based TAA combinations and applied everything we learned in the past decade ...

Branches: [[archive/threads/NOTimothyLottes/2025-01-28-so-we-the-industry-really-ever-went-back-to-the/2025-01-28-NOTimothyLottes-just-raw-spatial-scaling-in-a-custom-resolve]]

**2/**

@NOTimothyLottes Hey that’s literally what our VRS is doing with all those tricks and more. We just don’t call it an upsampler ; )
On PC we resolve MSAA to texture2DArray to retain plane separation benefits for bandwidth and coherency

**3/**

@MichalDrobot Larger differences are
(1.) Your VRS is PSL'ing to a regular grid? (need the actual 8x pattern for what I'm suggesting)
(2.) Sounds like you are getting benefit from FMASK due to the soft VRS, but for what I'm suggesting the NV flat+DCC layout is way better

**4/**

@NOTimothyLottes 1) it’s 4xMSAA but we DRS only on X axis which is matching your case I believe. Similar how it was done it Killzone Shadowfall.
8xMSAA we could explore XY scaling
2) depends. On PC it’s flat /w DCC. On gen8 it’s fmask packed. Gen9 is FMask with DCC plane0/1

**5/**

@NOTimothyLottes But sure I agree that 8x is the way to go for 4K. Our challenge is that we still have gen8 with 1k target and at those resolutions 8x scales really sub linear due to quad occupancy

**6/**

@MichalDrobot I guess the question then is if you implement variable spatial scaling in the custom resolve, is the 8xMSAA loss something that can easily be covered by increased spatial scale on the low end HW? 8x area scaling at 8xMSAA is still likely good for 3xAA on edges at spatial-only

Branches: [[archive/threads/NOTimothyLottes/2025-01-28-so-we-the-industry-really-ever-went-back-to-the/2025-01-28-NOTimothyLottes-my-mindset-is-more-tuned-towards-rendering]]

**7/**

@NOTimothyLottes If low end hw is decent with MSAA AND you can control triangle density effectively to combat quad occupancy loss (we can’t) - that’s the best there is imo.
FWIW that’s why we use stencil even for geo edges for MSAA - because we get too many interior edges that don’t do anything

**8/**

@MichalDrobot I see, yes once authoring pushes tri/pix density then what makes sense changes. I was thinking more of the way things had been authored in the relief mapping era.

**9/**

@NOTimothyLottes Then you need invest heavily into visbuffer for “simple draws” and pay setup price to compensate those deficiencies.  involved pipeline that is not portable
I can totally see your plan working for specific art styles or more retro gaming. There is a huge Indy market for this

**10/**

@MichalDrobot If tri/pix density is high, even if there are some huge triangles left, without substantially good multi-scale LOD (meaning cluster count scaling), I think soft culling alone falls off the !/$ curve for scaling - hints perhaps past the crossover for non-triangle rendering

**11/**

@MichalDrobot At that stage I'd have transitioned to direct final view reconstruction from object space domain. Walking object space, atomicMin(MSB{z,ref}LSB) at some good enough density into the final projected space, then use a neighborhood of 'refs' to get back to object space neighborhoods

**12/**

@MichalDrobot ... for the filtering. One can effectively cancel atomics per lane based on local projected screen-space density to deal with domain stretch (skinning), so it gets to be highly scalable.

**13/**

@MichalDrobot The TAA reconstructions all crossed that threshold of cost where it's easy to swap in reconstruction from something other than screen-space. And with no disocclusion trouble, object space is much less of a challenge to go from.
