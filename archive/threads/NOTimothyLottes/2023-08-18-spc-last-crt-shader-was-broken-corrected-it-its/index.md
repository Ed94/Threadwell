---
title: "SPC: Last CRT shader was broken."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1692395128739057844"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1692395128739057844"
date: 2023-08-18
archived: 2026-08-23
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "SPC: Last CRT shader was broken."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1692395128739057844
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-08-18 04:36:56

## Thread

**1/**

SPC: Last CRT shader was broken. Corrected it. It's energy conserving now, and correctly doing sub-pixel line width raster using the individual channels. Cell camera  shots below at different zooms.

Media (not lifted): `1692395128739057844_F3yYY1iXYAAaAlE_orig.jpg` `1692395128739057844_F3yYZQwXcAABFvi_orig.jpg` `1692395128739057844_F3yYZo5WAAA0aRS_orig.jpg`

**2/**

Each scan line is simulated with only 3 pixels. But you get 9 sub-pixels to play with, so that is where the quality comes from. It reaches 7/8th of the display peak brightness, this compromise was so there is always some amount of perceptual scan effect.

**3/**

The scan line thickness is adaptive proportional to linear brightness. When the scan thins out it is energy conserving and increases the thin pixel brightness to compensate. When it needs to go bright, it blooms the line. Lines have some overlap in bloom.

**4/**

One human perceptual reason CRTs feel like they have more contrast than they do, is because an individual scan line is super bright when in focus. So the black surround feels darker to the mind.
