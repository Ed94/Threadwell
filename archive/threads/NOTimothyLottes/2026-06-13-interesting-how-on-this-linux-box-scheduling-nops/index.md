---
title: "Interesting how on this Linux box, scheduling NOPs like nanosleep of 0 and futex waiting on an already set memory location … both take around 60 microseconds, cannot afford to do many of those per millisecond."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2065840191340707905"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2065840191340707905"
date: 2026-06-13
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Interesting how on this Linux box, scheduling NOPs like nanosleep of 0 and futex waiting on an already set memory location … both take around 60 microseconds, cannot afford to do many of those per millisecond."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2065840191340707905
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-06-13 16:54:17

## Thread

**1/** **@NOTimothyLottes** ^2065840191340707905

Interesting how on this Linux box, scheduling NOPs like nanosleep of 0 and futex waiting on an already set memory location … both take around 60 microseconds, cannot afford to do many of those per millisecond. Food for thought for high fps targets

Branches: [[archive/threads/NOTimothyLottes/2026-06-13-interesting-how-on-this-linux-box-scheduling-nops/2026-06-13-rflaherty71-seems-like-people-trying-to-push-high-frame-rates]], [[archive/threads/NOTimothyLottes/2026-06-13-interesting-how-on-this-linux-box-scheduling-nops/2026-06-13-raggi-nanosleep-0-will-sleep-for-the-timer-slack-mm]], [[archive/threads/NOTimothyLottes/2026-06-13-interesting-how-on-this-linux-box-scheduling-nops/2026-06-13-winning_tactic-why-not-do-a-gradual-sleeping-start-with-while]], [[archive/threads/NOTimothyLottes/2026-06-13-interesting-how-on-this-linux-box-scheduling-nops/2026-06-13-BonbliStar-most-futex-impls-ive-seen-check-for-that-and]]

**2/** **@NOTimothyLottes** ^2065840616148193294

A write of zero bytes is closer to say 6 microseconds in contrast, so just the user/kernel transition is expensive but 10x faster
