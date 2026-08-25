---
title: "1st SPC project: to be based on vintage 640x480 render (VGA style), +fallback to 640x240 for 15 KHz arcade CRTs (PGM-esk), and CRT shader scaling on Deck and OLED/LCD."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1688018382543597568"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1688018382543597568"
date: 2023-08-06
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "1st SPC project: to be based on vintage 640x480 render (VGA style), +fallback to 640x240 for 15 KHz arcade CRTs (PGM-esk), and CRT shader scaling on Deck and OLED/LCD."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1688018382543597568
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-08-06 02:45:18

## Thread

**1/**

1st SPC project: to be based on vintage 640x480 render (VGA style), +fallback to 640x240 for 15 KHz arcade CRTs (PGM-esk), and CRT shader scaling on Deck and OLED/LCD. Use mix of render pixel aspect changes, running less than 480 lines, and letter-box to keep integer Y scaling.

![](https://pbs.twimg.com/media/F20LgFtWQAAMtcv?format=png&name=orig)

**2/**

My 15 KHz CRT output path when docked is HD Fury Nano (won't do <480p) doing HDMI to VGA, with a sync combiner (to workaround GBS-C bug), into GBS-C which line drops 480p ~60Hz to 240p ~60Hz and outputs component. The 640 width gets maintained even if some CRTs cannot resolve it.

**3/**

Presents issues for UI, namely that my bitmap fonts need to look good in both 480p and 240p modes, so for editor (assembler) I'm going with a font that uses right angles and designed around 2x2 stroke width, in a 8x16 (pow2) bitmap, so 640x240p still gets a readable 8x8 (below)

![](https://pbs.twimg.com/media/F20Ogh8XoAAq7hR?format=png&name=orig)

**4/**

The next challenge is overscan safety, since real non-VGA CRTs will be used in development. The Y axis has an easy fix, simply keep cursor pinned in the 'safe' zone, but still print lines in the overscan area (so they can be seen when attached to non-overscan CRTs/etc too).
