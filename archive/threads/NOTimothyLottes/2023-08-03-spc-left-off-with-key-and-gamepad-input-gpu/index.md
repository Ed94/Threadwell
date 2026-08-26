---
title: "SPC: Left off with KEY and GAMEPAD input GPU-accessable."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1687250591813079041"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1687250591813079041"
date: 2023-08-03
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "SPC: Left off with KEY and GAMEPAD input GPU-accessable."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1687250591813079041
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-08-03 23:54:23

## Thread

**1/** **@NOTimothyLottes** ^1687250591813079041

SPC: Left off with KEY and GAMEPAD input GPU-accessable. NOP design, no functions, no API, just a fixed VA address and data format to read, dead easy.

![](https://pbs.twimg.com/media/F2pRdu9WgAABCLE?format=jpg&name=orig)
![](https://pbs.twimg.com/media/F2pReKsXoAAPvow?format=jpg&name=orig)

**2/** **@NOTimothyLottes** ^1687251721032978432

Wrote some console data dumping to aid in bringing up HID parsers for Deck and three generations of PlayStation controllers. Apparently XBox controllers aren't HIDs so not sure how one is supposed to access those.

![](https://pbs.twimg.com/media/F2pSfIHXcAMI-IQ?format=jpg&name=orig)
![](https://pbs.twimg.com/media/F2pSfzAWcAMo6t7?format=jpg&name=orig)

**3/** **@NOTimothyLottes** ^1687252813468852225

Supporting hot plug was a bit of a mess, just trying to open devices every second. Adding open devices to an epoll. {Product, vendor} isn't enough to ID a device, too much aliasing, so I use packet size as well.

![](https://pbs.twimg.com/media/F2pTfekWYAAAwSi?format=jpg&name=orig)

**4/** **@NOTimothyLottes** ^1687253442643755008

Open devices with matching packet size get set in a bit array, and I collect up to 4 of those device outputs to sent to the GPU. Special logic to always place Steam Deck controls last to make docking work well.

![](https://pbs.twimg.com/media/F2pUEG0XwAEwYvP?format=jpg&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2023-08-03-spc-left-off-with-key-and-gamepad-input-gpu/2023-08-04-sanjeetsuhag-i-gotta-ask-why-use-such-condensed-formatting-for]]

**5/** **@NOTimothyLottes** ^1687254511239221249

I'll have to tackle audio at some point, but I'm skipping networking for version 1. But otherwise SPC is good to move on to the next step, which is to build out the GPU side assembler & data editor. Which will be written in binary at first.

**6/** **@NOTimothyLottes** ^1687255546372493313

Project is roughly 2000 lines of C at this point. With no includes. Anyone have any suggestions for hosting let me know. Source will be released.

**7/** **@NOTimothyLottes** ^1687257354490818561

For anyone tuning in now, SPC is kind of like a Pico8, but instead of being a portable fantasy console, SPC turns the Steam Deck into an actual console for exclusive GPU assembly projects. The way consoles had been done before silly portability became the only focus.
