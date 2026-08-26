---
title: "Good landmine to step on: AMD vs Hotz."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1880476705728655733"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1880476705728655733"
date: 2025-01-18
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Good landmine to step on: AMD vs Hotz."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1880476705728655733
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-01-18 04:45:58

## Thread

**1/** **@NOTimothyLottes** ^1880476705728655733

Good landmine to step on: AMD vs Hotz.
Speculation follows ...

Can only guess the line in the sand here is wanting access to write signed firmware. Specifically aspects of the GPU-side driver which manage compute dispatch and synchronization.

![](https://pbs.twimg.com/media/GhjLil-WsAAl5Tp?format=png&name=orig)

**2/** **@NOTimothyLottes** ^1880476956287987779

If so, likely a HW problem is single level security and putting too much functionality that shouldn't need to be secure on the signed side. Perhaps AMD both: (a.) cannot open access, (b.) nor has the willingness to partner to fix/improve the firmware on their end.

**3/** **@NOTimothyLottes** ^1880477351013937579

What I'd like to know is what aspects of the PM4 (command stream) are the actual contention point?
I bet engineering folks could bang out a solution to whatever problem there is an a short time, but instead business people get involved, words get exchanged, and stupid wins

**4/** **@NOTimothyLottes** ^1880477715700281601

I also suspect one can "fix it" without changing the command processor firmware. Perhaps the way they are trying to go about solving a problem is actually not the right way.

**5/** **@NOTimothyLottes** ^1880478110531145955

Specifically in Linux, you can layout your VA space and allocations using the existing AMD kernel driver interfaces, and with no other applications using the GPU, basically get access to do whatever you want that is describable in existing PM4 packets

**6/** **@NOTimothyLottes** ^1880478802230509835

This means they are not actually limited at all on the compiler side. Compile your own binaries. Setup your memory once on init-time and then do dispatches to keep persistent work running on the GPU without any real driver involvement at all

**7/** **@NOTimothyLottes** ^1880479856632426572

So probably I'm missing something specific with regards to multi-GPU or memory mapping which indeed isn't easily possible in today's kernel driver. Because I'm basically only thinking about gamedev stuff.

Branches: [[archive/threads/NOTimothyLottes/2025-01-18-good-landmine-to-step-on-amd-vs-hotz/2025-01-18-AgileJebrim-i-cant-speak-about-ai-but-we-do-have-genlock-to]], [[archive/threads/NOTimothyLottes/2025-01-18-good-landmine-to-step-on-amd-vs-hotz/2025-01-18-LeviathanGamer2-best-guess-from-what-they-have-said-is-they-want]], [[archive/threads/NOTimothyLottes/2025-01-18-good-landmine-to-step-on-amd-vs-hotz/2025-01-18-alifahrri2-one-thing-i-know-about-multi-gpu-is-that-tinygrad]], [[archive/threads/NOTimothyLottes/2025-01-18-good-landmine-to-step-on-amd-vs-hotz/2025-01-18-pyrek_p-also-george-started-with-rx7900-a0-silicon-so-i]]
