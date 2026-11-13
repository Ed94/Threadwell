---
title: "If the Deck 1 did >4M units, you'd only need a 2.5% attach rate to hit 100k unit sales."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2106583907928064260"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2106583907928064260"
date: 2026-10-04
archived: 2026-10-06
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "If the Deck 1 did >4M units, you'd only need a 2.5% attach rate to hit 100k unit sales."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2106583907928064260
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-10-04 03:15:16

## Thread

**1/** **@NOTimothyLottes** ^2106583907928064260

If the Deck 1 did >4M units, you'd only need a 2.5% attach rate to hit 100k unit sales. Scale that by your sale price and subtract off dev costs. I think Valve already cross the threshold for being a sustainable platform for 2-the-metal exclusives for a single person dev team.

**2/** **@NOTimothyLottes** ^2106585155179561310

Doing RNDA2 + RDNA3.5 (speculation for Deck2) shaders would be trivially easy in asm. I don't know if the command packet structure changed across those gens, but if you only really do a few minor things like {flush, dispatch, bottom of pipe events, etc} for compute ...

**3/** **@NOTimothyLottes** ^2106585655870697702

Could spin up an AMD GPU based SteamOS to-the-metal-driver in a very short time for Deck1 and Deck2 and AMD RDNA GPU'ed Linux portability. All kernel interfaces (no usermode libraries).

**4/** **@NOTimothyLottes** ^2106586686197203439

It would present trouble for Valve, because it would need master DRM access to the VT and would bypass the Wayland layer completely (and bypass Valve's compositor). Interesting question if they would support these kinds of to-the-metal platform exclusives or not.

**5/** **@NOTimothyLottes** ^2106588702273401120

I've personally been looking for an excuse to drop Windows completely for development, and maybe doing a AMD Linux + Deck 1/2 exclusive is the right transition point. The world does deserve too see what vintage hard core humans can do in assembly before we are all wiped out
