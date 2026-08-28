---
title: "Unsigned Integer divide by zero, x/0=?, what answer is preferred {x (nop), 0, or 0xffffffff (max integer)}?"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2066678716206289353"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2066678716206289353"
date: 2026-06-16
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Unsigned Integer divide by zero, x/0=?, what answer is preferred {x (nop), 0, or 0xffffffff (max integer)}?"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2066678716206289353
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-06-16 00:26:17

## Thread

**1/** **@NOTimothyLottes** ^2066678716206289353

Unsigned Integer divide by zero, x/0=?, what answer is preferred {x (nop), 0, or 0xffffffff (max integer)}?

**2/** **@NOTimothyLottes** ^2066690080098451916

So I went with a NOP, and things get more interesting with signed divide, because on x86 there are 2 cases that will interrupt. So my div wrappers fix both cases to NOPs. Logically it works more like abs and neg in cases of overflow. Details in photo.

![](https://pbs.twimg.com/media/HK5bq_uWkAA7xdU?format=jpg&name=orig)

**3/** **@NOTimothyLottes** ^2066690873706836163

I do agree it’s too bad x86 forces the interrupt, and I want zero chance of interrupt crash. In that regard same as others. However, interesting that I ended up in the opposite solution space as everyone else ;)
