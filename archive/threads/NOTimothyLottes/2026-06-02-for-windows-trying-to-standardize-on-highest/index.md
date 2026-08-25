---
title: "For Windows trying to standardize on HIGHEST_PRIORITY_CLASS, mixed with THREAD_PRIORITY_{IDLE,NORMAL,TIME_CRITICAL}."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2061937134756380682"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2061937134756380682"
date: 2026-06-02
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "For Windows trying to standardize on HIGHEST_PRIORITY_CLASS, mixed with THREAD_PRIORITY_{IDLE,NORMAL,TIME_CRITICAL}."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2061937134756380682
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-06-02 22:24:56

## Thread

**1/** @NOTimothyLottes

For Windows trying to standardize on HIGHEST_PRIORITY_CLASS, mixed with THREAD_PRIORITY_{IDLE,NORMAL,TIME_CRITICAL}. Which maps to {1, 13, 15} respectively. Then trying "Pro Audio" hack with AVRT to get whatever that gives in the 16-31 fake "realtime" bracket for highest.

**2/** @NOTimothyLottes

Linux mapping will be {SCHED_IDLE, SCHED_OTHER with 2 settings of nice} to match. Unfortunately SCHED_FIFO is locked out by default, but if the user blesses the right permissions will get better audio latency. Maybe pause/unpause will trigger auto latency re-adaption.
