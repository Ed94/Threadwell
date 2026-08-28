---
title: "Think about it - the M64 is probably going to be one of the best FPGA device platforms for custom fantasy HW platform development."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2082496468720521510"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2082496468720521510"
date: 2026-07-29
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Think about it - the M64 is probably going to be one of the best FPGA device platforms for custom fantasy HW platform development."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2082496468720521510
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-29 16:00:23

## Thread

**1/** **@NOTimothyLottes** ^2082496468720521510

Think about it - the M64 is probably going to be one of the best FPGA device platforms for custom fantasy HW platform development.

![](https://pbs.twimg.com/media/HOaDf8xWEAEOfhU?format=jpg&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2026-07-29-think-about-it-the-m64-is-probably-going-to-be/2026-07-29-aussetg-can-you-run-your-own-code-without-hacking-it]]

**2/** **@NOTimothyLottes** ^2082501415977566241

Anyone want to guess on what size FPGA they used?

![](https://pbs.twimg.com/media/HOaHoR7XQAAazym?format=png&name=orig)

**3/** **@NOTimothyLottes** ^2082502244348358790

Hint just pin count:

![](https://pbs.twimg.com/media/HOaIvwtWcAA_iqE?format=jpg&name=orig)

**4/** **@NOTimothyLottes** ^2082506788927054144

Looks like an FFVB676 package, which means it is at least an AU10P (cannot be the AU7P)

![](https://pbs.twimg.com/media/HOaMRaFXYAAyfnA?format=png&name=orig)

**5/** **@NOTimothyLottes** ^2082521843479543861

Looks like AP Memory 24-pin PSRAMs. If it was DDR it might be 16-bit per clock, so effectively a "64-bit bus" perhaps at 133 MHz - so very rough guess ballpark paper spec peak around 1 GiB/s.

![](https://pbs.twimg.com/media/HOaWvq7XwAAQBA0?format=jpg&name=orig)
![](https://pbs.twimg.com/media/HOaZ844XEAAcfem?format=jpg&name=orig)

**6/** **@NOTimothyLottes** ^2082527433958285351

Looks like the FPGA in the M64 is an AU15P

![](https://pbs.twimg.com/media/HOafQ28XEAADcYX?format=png&name=orig)
![](https://pbs.twimg.com/media/HOafpgWXQAAFbA_?format=png&name=orig)

**7/** **@NOTimothyLottes** ^2082531267094917151

So ballpark FPGA capacity is like
{32 CLBs + 2 DSPs, per 2KiB BRAM} x 288 BRAMs
