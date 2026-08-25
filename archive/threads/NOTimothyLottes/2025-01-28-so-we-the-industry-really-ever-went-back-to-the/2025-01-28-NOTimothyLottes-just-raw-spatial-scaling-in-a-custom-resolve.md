---
title: "Just raw spatial scaling in a custom resolve/"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1884283764068737420"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1884283764068737420"
date: 2025-01-28
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Just raw spatial scaling in a custom resolve/"
in_reply_to: ""
parent_post_id: "1884282476195110998"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1884283764068737420
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-01-28 16:53:52

## Branch

**1/** @NOTimothyLottes

Just raw spatial scaling in a custom resolve/
4xMSAA at 2.25x area is 2.66xAA on edges
8xMSAA at 2.25x area scale is 5.33xAA on edges
8xMSAA at 4x area scale is 4xAA on edges <--- bingo

**2/** @NOTimothyLottes

Take 8xMSAA with a view-port jitter pattern (or even PSL) which always maintains the same sample vs axis intersections! <--- double bingo

Sub-pixel detail is now mostly stable, will show up in all frames in the local neighborhood = stable temporally

**3/** @NOTimothyLottes

Bottom line/
8xMSAA + smart jitter (or PSL)
+ temporal feedback
+ 4x area spatial scaling
ALL in one custom resolve pass

Something one could make temporally stable without ghosting and still maintain 4xAA (on edges at output resolution) on the worst case in disocclusions

**4/** @NOTimothyLottes

It would destroy DLSS4 in terms of classic image quality

**5/** @NOTimothyLottes

Note one can inline something like CAS/RCAS (what I did at AMD) into the custom MSAA resolve, by modulating a negative lobe based on a local min/max kernel's min distance to signal peak {0 or 1}. Meaning it's possible to get really sharp output from this combo.

**6/** @dankbaker

@NOTimothyLottes

Is there an example shader that does that custom resolve?

**7/** @NOTimothyLottes

@dankbaker

Probably not in the config you are interested in (I'm assuming spatial with no scaling?) Feel free to DM me. Most of these things need adaption specific to the config. Last one I did was huge spatial scaling for a CRT-styled scalar using this kernel,

![](https://pbs.twimg.com/media/GiZv5SFWYAAyv2W?format=jpg&name=orig)

**8/** @NOTimothyLottes

@dankbaker

My project is monochome so the kernel blending logic is single channel, and the content is designed to handle a huge amount of negative lobe well so I don't constrain ringing (BLUE, replace with 'm.y*RINGING'), and everything in linear of course ... but it should provide an idea

![](https://pbs.twimg.com/media/GiZxt_6X0AARcFR?format=png&name=orig)

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-01-28-so-we-the-industry-really-ever-went-back-to-the]]
