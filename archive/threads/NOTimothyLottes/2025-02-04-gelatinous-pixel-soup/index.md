---
title: "__/ \"GELATINOUS PIXEL SOUP!\" \\__"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1886572405176345062"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1886572405176345062"
date: 2025-02-04
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "__/ \"GELATINOUS PIXEL SOUP!\" \\__"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1886572405176345062
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-02-04 00:28:06

## Thread

**1/** **@NOTimothyLottes** ^1886572405176345062

__/ "GELATINOUS PIXEL SOUP!" \__
Another spicy Threat Interactive video
https://www.youtube.com/watch?v=KEtb0punTHk

Someone willing to challenge the status quo
Lets talk about some of his topics ...

**2/** **@NOTimothyLottes** ^1886573153826038114

Finally someone posting ms/frame breakdown!
Appears to be using an actual mid-range GPU

[BLUE]
Ray-reconstruction [RR] is 13x more expensive than the CNN TAA
And already over the 120Hz frame budget
Even at 60Hz you'd be giving up the majority of your frame budget to AI

![](https://pbs.twimg.com/media/Gi50Il6XwAAHdo2?format=jpg&name=orig)

**3/** **@NOTimothyLottes** ^1886574332505198960

[ORANGE]
Transformer model being almost 2x the cost of the prior CNN model. Double the cost for less ghosting.

Note STP (non-ML) was targeting 1/3 to 1/2 of the cost of that old CNN model with an analytical model which removed the ghosting on opaque geometry with motion vectors.

![](https://pbs.twimg.com/media/Gi50lS_WMAEXEZC?format=png&name=orig)

**4/** **@NOTimothyLottes** ^1886578272135504258

It is certainly possible to engineer a bunch of very low cost and high quality human written shader solutions for scaling-TAAs that do better than the ML ones in !/$ for the non-ray-reconstruction cases

**5/** **@NOTimothyLottes** ^1886580107097080317

NV banking on poorly optimized PC titles though is NOT a new thing: lets rewind to 2012!

2011> AMD 7970 = 3.8 Tflop/s 264 GB/s
2012> NV 680 = 3.1 Tflop/s 192 GB/s

NV is way under-powered!
Yet NV wins because of game-ready drivers

![](https://pbs.twimg.com/media/Gi5585sWcAAPpw-?format=png&name=orig)

**6/** **@NOTimothyLottes** ^1886581250359529845

NVIDIA was always about enabling dev laziness, the RT+AI+Fake era is just the ultimate form of that, where the lazy dev is marginalized to a few % of the total frame budget with AI taking the majority.

**7/** **@NOTimothyLottes** ^1886583358110552360

Others playing "follow-the-leader" unfortunately still didn't catch on to the most important point, that Jensen's plan forces consumers to buy into only high-end cards to fix all the PC game problems. Nothing about the AI future scales down!

![](https://pbs.twimg.com/media/Gi582LwWMAA4JBz?format=png&name=orig)

**8/** **@NOTimothyLottes** ^1886584084031213672

Jensen's "Low-End" = 5070 is 1/3 the VALU of a 5090 

But something like SteamDeck vs 5070
is 1/19 the VALU and 1/7.6 the bandwidth 

Already today, without scaling-TAAs on 5080, many "high-end" PC games either struggle to hit 60Hz at 4K or cannot make it to 120Hz ... ouch

**9/** **@NOTimothyLottes** ^1886585534115381520

So Jensen's AI future depends on big GPU$$$$

And all other non-NV IHVs and OEMs build substantially smaller GPUs (Apple) or focus on value (everyone else)

Following Jensen's path is suicide, because they won't have the baseline GPU mass required to play

**10/** **@NOTimothyLottes** ^1886586038870798570

Should feel extra sorry for someone like Qualcomm who though they could just make an RT core and follow the baseline HW requirements, but completely missed the point that NV would just raise the ray-reconstruction cost to a place Qualcomm could never get to

**11/** **@NOTimothyLottes** ^1886589607846019114

AMD/others can easily extend out 1-fake frame to N-fake frames, and they all have timewarp for VR experience, so doing the fake latency thing is trivial too. And maybe FSR4/etc ML based non-RR scaling-TAAs hit DLSS parity soon

But NVIDIA has already pivoted to ray reconstruction

**12/** **@NOTimothyLottes** ^1886590953328181652

At the end of the day, it is actually unreasonable to expect IHVs to do anything other than follow NVIDIA if PC engines just eat up RT and get bottle-fed on AI. Even if AMD or anyone makes awesome divergent tech, if it isn't mass market engine adoption it will go no where

**13/** **@NOTimothyLottes** ^1886592037329289661

Likewise how can we expect major AAA engines to take on the uncertainty and insane R&D challenge of getting off their current NV evolution paths and do something radically different, it's just too high risk

**14/** **@NOTimothyLottes** ^1886592291030126732

So the industry is somewhat in a live lock condition where it won't make forward progress

**15/** **@NOTimothyLottes** ^1886597785148924309

Related story. So the reason I left AMD for Unity was because Unity was spinning up an R&D team for scalable high-end graphics. And our target was mobile through high-end PC. And left alone we would have got there. But the stock crashed and we got axed or forced out.

**16/** **@NOTimothyLottes** ^1886602718900359233

I think ultimately those in the industry who don't like the current status quo, it's on you to build the tech yourself and ship it in an game to prove it is possible. Because it isn't likely that anyone has the pockets deep enough to fund a new general purpose engine on risky R&D

**17/** **@0xpatrickhan** ^1886699325553828171

**@NOTimothyLottes**

What are some problem areas you think need to be tackled? I’ve read some of what you’ve written in response to some of the gripes of modern day temporal supersampling/AA. What else? Anything that IHVs would be uniquely positioned to do?

**18/** **@NOTimothyLottes** ^1886741205423128997

**@0xpatrickhan**

There is a laundry list of things IHVs dont expose or expose very poorly for basic compute shaders, making it quite difficult or impossible to get a compiler to do the right thing. Fix those and devs like myself could easily build better than AI tech options
