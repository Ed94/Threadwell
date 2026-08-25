---
title: "I'll mark this down a more code obfustication for most humans, but for me it's another useful shorthand."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2076492543622107480"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2076492543622107480"
date: 2026-07-13
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "I'll mark this down a more code obfustication for most humans, but for me it's another useful shorthand."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2076492543622107480
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-13 02:22:56

## Thread

**1/**

I'll mark this down a more code obfustication for most humans, but for me it's another useful shorthand.
define X_ return
define G_(x) goto x

![](https://pbs.twimg.com/media/HNEuyadXoAAVxgG?format=png&name=orig)

**2/**

Not been happy with traditional C style {if,while,do,switch,for} so moving to more assembly style {if,goto} instead. This way static branch prediction {backward=taken,forward=not_taken} is more explicit in the code. Prototyping it in the Library loader below

![](https://pbs.twimg.com/media/HNExHNRWIAAimHM?format=png&name=orig)

**3/**

Another quality of life change, exit with error now triggers the background console render thread to actually quit, so it always draws the console, then draws the error code, then exits.
