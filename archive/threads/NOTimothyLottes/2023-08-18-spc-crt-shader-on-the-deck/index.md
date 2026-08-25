---
title: "SPC: CRT shader on the Deck."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1692559239116406864"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1692559239116406864"
date: 2023-08-18
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "SPC: CRT shader on the Deck."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1692559239116406864
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-08-18 15:29:03

## Thread

**1/** @NOTimothyLottes

SPC: CRT shader on the Deck. This time not doing subpix render. Yet RGB vs BGR order matters still. One way it becomes possible to simulate even spaced aperture grill (removing scan fx), and the other more of the scan effect.

![](https://pbs.twimg.com/media/F30tppDWwAAA-8J?format=jpg&name=orig)
![](https://pbs.twimg.com/media/F30tqE8XYAAgrFv?format=jpg&name=orig)

**2/** @NOTimothyLottes

Comparing all methods (grille, bad convergence scan, subpix scan)

![](https://pbs.twimg.com/media/F30uJoSWcAA7ICE?format=jpg&name=orig)
![](https://pbs.twimg.com/media/F30uKJdXkAA4PV8?format=jpg&name=orig)
![](https://pbs.twimg.com/media/F30uKouWQAAvY0q?format=jpg&name=orig)

**3/** @NOTimothyLottes

The non-subpix scan has 1-pixel separation of RGB (intentional bad convergence) to help hide scaling. The subpix scan uses 1/3-pixel separation (less visible misaligned convergence). Pixel as in output pixel.

Branches: [[archive/threads/NOTimothyLottes/2023-08-18-spc-crt-shader-on-the-deck/2023-08-18-tomcr2100-i-am-not-quite-sure-what-do-you-mean-by-subpixel]]

**4/** @NOTimothyLottes

The subpix version is definitely better. Because of the almost 3x doubling of scanline width detail, it just perceptually feels a lot cleaner and easier to reconstruct in the mind.

![](https://pbs.twimg.com/media/F30y9HPWUAAbmmw?format=jpg&name=orig)
![](https://pbs.twimg.com/media/F30y9h3WAAETuui?format=jpg&name=orig)
