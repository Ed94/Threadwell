---
title: "@onatt0 The big industry mistake was factoring into thousands of functions in code, instead of just baking all that into a \"protocol\" of data structures in memory."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1917661939469111373"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1917661939469111373"
date: 2025-04-30
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
  - registers
  - data-oriented
description: "@onatt0 The big industry mistake was factoring into thousands of functions in code, instead of just baking all that into a \"protocol\" of data structures in memory."
in_reply_to: "1917659010024587634"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1917661939469111373
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-04-30 19:26:49

## Thread

**1/** **@NOTimothyLottes** ^1917661939469111373

**@onatt0**

The big industry mistake was factoring into thousands of functions in code, instead of just baking all that into a "protocol" of data structures in memory. Like OOP member functions to load or mutate one variable = vomit.

**2/** **@NOTimothyLottes** ^1917662460716212239

**@onatt0**

I do all my custom CPU side stuff more like treating the register file like a "memory" of which the contents are aliased to different shared structures for different purposes across time

**3/** **@NOTimothyLottes** ^1917662813817835551

**@onatt0**

So the register file is more like an aliased global namespace. And "functions" are free of arguments and free of returns. This way of working with the HW is way better and easier than the 'C' model.

**4/** **@NOTimothyLottes** ^1917663219289559511

**@onatt0**

In the few cases where you need to reuse small code patterns, those end up a compile time macros that inline to different registers, larger patterns are already better factored to data

## Related

- [[archive/threads/onatt0/2025-04-30-holy-truthnuke-and-people-think-c-is-the-optimal-state-of]]
