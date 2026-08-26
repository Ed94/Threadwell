---
title: "Two great graphs from https://chipsandcheese.com/2023/12/23/nintendo-switchs-igpu-maxwell-nerfed-edition/ - Why I always manually vectorize 16-bit code, and also why you always need to manually check disassembly."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1738744404414759381"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1738744404414759381"
date: 2023-12-24
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Two great graphs from https://chipsandcheese.com/2023/12/23/nintendo-switchs-igpu-maxwell-nerfed-edition/ - Why I always manually vectorize 16-bit code, and also why you always need to manually check disassembly."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1738744404414759381
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-12-24 02:12:24

## Thread

**1/** **@NOTimothyLottes** ^1738744404414759381

Two great graphs from https://chipsandcheese.com/2023/12/23/nintendo-switchs-igpu-maxwell-nerfed-edition/ - Why I always manually vectorize 16-bit code, and also why you always need to manually check disassembly.

![](https://pbs.twimg.com/media/GCFBbyUWIAAaWoR?format=png&name=orig)
![](https://pbs.twimg.com/media/GCFBdy9WEAE0JYk?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2023-12-24-two-great-graphs-from-https-chipsandcheese-com/2023-12-24-BrettRidel-do-you-know-other-equivalent-graphs-or-ressources]]

**2/** **@AgileJebrim** ^1738750536302670083

**@NOTimothyLottes**

Why are float16s so much faster than int16s?

**3/** **@NOTimothyLottes** ^1738756633738522752

**@AgileJebrim**

Same bit width, FMA needs smaller multipler than IMAD. Thus HW mul24 fast paths that never get exposed. But 16-bit is small enough already. I thought on AMD, packed 16-bit int or float are the same perf. Some vendors though try area savings by de-throughputing integer/etc ALUs

**4/** **@AgileJebrim** ^1738757938376761652

**@NOTimothyLottes**

Oh are you only comparing FMA? If it was just additions, would they be on par?
