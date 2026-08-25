---
title: "@NOTimothyLottes Very interesting \"crosstalk from voltage inversion\" artifact."
type: archive
source: twitter
source_url: "https://x.com/BlurBusters/status/1689479056448684032"
author: "Blur Busters"
handle: BlurBusters
post_id: "1689479056448684032"
date: 2023-08-10
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Very interesting \"crosstalk from voltage inversion\" artifact."
in_reply_to: ""
parent_post_id: "1688491417109196800"
---

## Source

- URL: https://x.com/BlurBusters/status/1689479056448684032
- Author: Blur Busters (@BlurBusters)
- Posted: 2023-08-10 03:29:30

## Branch

**1/**

@NOTimothyLottes Very interesting "crosstalk from voltage inversion" artifact. Some repeating patterns or flicker patterns can trigger crosstalk artifacts too. Behavior varies a lot between TN, IPS, and VA, but all of them have to alternate voltage polarity spatially and temporally.

![](https://pbs.twimg.com/media/F3I8AZmW0AEy6jn?format=png&name=orig)
![](https://pbs.twimg.com/media/F3I8BVlXoAAnuJB?format=png&name=orig)

**2/**

@NOTimothyLottes Related reads:
https://www.lagom.nl/lcd-test/inversion.php
https://forums.blurbusters.com/viewtopic.php?t=7539
http://www.techmind.org/lcd/#:~:text=Inversion

**3/**

@BlurBusters I appreciate the links. Came to the same conclusion, for LCDs when doing low scaling like 1:2x2 'CRT' emulation, I'll have to do a stylized blue noise phosphor pattern instead.

**4/**

@NOTimothyLottes @BlurBusters "VCOM inversion" -if wasn't line2line but frame2frame that'd "flicker" instead at half the refresh rate so that's why it's preferred& there's also another peculiarity of this scheme. Worth looking into, spent a few hours afternoon,it's late evening now maybe share another time.

**5/**

@Ak4115x @NOTimothyLottes Inversion algorithm is both spatial and temporal on all of them, regardless of spatial pattern of voltage inversion. Line to line is also frame to frame. (lines swaps voltage polarity in next frame)

**6/**

@BlurBusters @NOTimothyLottes LCOS has singular VCOM there's no pattern to it and no such artifact.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2023-08-07-crt-emulation-on-lcds-can-be-hard]]
