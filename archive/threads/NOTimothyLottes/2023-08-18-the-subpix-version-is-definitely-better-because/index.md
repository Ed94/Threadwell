---
title: "SPC: CRT shader on the Deck."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1692559239116406864"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1692559239116406864"
date: 2023-08-18
archived: 2026-08-23
status: draft
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

**1/**

SPC: CRT shader on the Deck. This time not doing subpix render. Yet RGB vs BGR order matters still. One way it becomes possible to simulate even spaced aperture grill (removing scan fx), and the other more of the scan effect.

![](https://files.catbox.moe/mve2kr.jpg)

![](https://files.catbox.moe/vis95s.jpg)

**2/**

Comparing all methods (grille, bad convergence scan, subpix scan)

![](https://files.catbox.moe/mve2kr.jpg)

![](https://files.catbox.moe/vis95s.jpg)

![](https://files.catbox.moe/34pnhf.jpg)

**3/**

The non-subpix scan has 1-pixel separation of RGB (intentional bad convergence) to help hide scaling. The subpix scan uses 1/3-pixel separation (less visible misaligned convergence). Pixel as in output pixel.

**4/**

The subpix version is definitely better. Because of the almost 3x doubling of scanline width detail, it just perceptually feels a lot cleaner and easier to reconstruct in the mind.

![](https://files.catbox.moe/ugcsjy.jpg)

![](https://files.catbox.moe/g42t2i.jpg)
