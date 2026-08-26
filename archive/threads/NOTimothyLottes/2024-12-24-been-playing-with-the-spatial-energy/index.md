---
title: "Been playing with the spatial energy redistribution for half a decade for CRT-stylized scaling."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1871630300222259212"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1871630300222259212"
date: 2024-12-24
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Been playing with the spatial energy redistribution for half a decade for CRT-stylized scaling."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1871630300222259212
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-12-24 18:53:31

## Thread

**1/** **@NOTimothyLottes** ^1871630300222259212

Been playing with the spatial energy redistribution for half a decade for CRT-stylized scaling. Solving 2x area scaling was hard, had to use a 3-pixel vertical pattern. Example shader here: https://www.shadertoy.com/view/lfcBDs (left=bilinear, middle=CRT-scaling, right=nearest)

![](https://pbs.twimg.com/media/Gflc8p_XsAA1MfA?format=png&name=orig)

**2/** **@NOTimothyLottes** ^1871630994505138543

We can engineer CRT-inspired spatial scaling techniques that make it more acceptable to render at lower resolutions without leaning on either {scaling-TAAs like DLSS2+, or scalars like FSR1}, instead just try to make the panel actually look like a lower resolution panel!

**3/** **@NOTimothyLottes** ^1871631608023028007

Nearest 1:2x2 scaling tends to fail in that it amplifies the step function, which sets off all sorts of alarms in the mind with false edges. Where just inserting near black lines and correcting for the energy loss, tends to invoke the brain to reconstruct the image instead

**4/** **@NOTimothyLottes** ^1871633634383565128

Interesting to see positive reviews for a scaling TAA in 2024 that wouldn't do well at 4x area, but hits a better balance at 1440p-2-4K, in less temporal flicker and less ghosting. Seems like people actually favor stability more than they realize consciously or want to admit

**5/** **@NOTimothyLottes** ^1871634266867822680

So many games are now designing around high scaling-TAAs, and I think it's time people seriously consider the other options, actually making no-ghosting no-thin-flicker a priority and finding other ways to scale output, that's why I built that DBM scalar (as an example option)
