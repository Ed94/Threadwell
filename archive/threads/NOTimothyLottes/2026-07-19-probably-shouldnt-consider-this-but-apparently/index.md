---
title: "Probably shouldn't consider this -BUT- apparently writing to ax doesn't change the other 48-bits."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2078728600912630031"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2078728600912630031"
date: 2026-07-19
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Probably shouldn't consider this -BUT- apparently writing to ax doesn't change the other 48-bits."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2078728600912630031
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-19 06:28:14

## Thread

**1/**

Probably shouldn't consider this -BUT- apparently writing to ax doesn't change the other 48-bits. So one could do a 4-byte overhead interpreter with a 64KiB aligned window of directly jumpable words like this below. [rsi]=addresses to jump to. You'd pay the false dependency stall

![](https://pbs.twimg.com/media/HNkf6ntX0AA8d1M?format=png&name=orig)

**2/**

It's interesting because it cuts interpreted source size in half. Ie a stream of 16-bit offsets instead of 32-bit addresses.

**3/**

The aim of course, keep the stuff that doesn't need to go fast optimized instead for low complexity and low size (aka interpreted forth), and keep the stuff that needs to go fast, at peak, assembly. Hits 2 extremes well.

Branches: [[archive/threads/NOTimothyLottes/2026-07-19-probably-shouldnt-consider-this-but-apparently/2026-07-19-noop_dev-these-instrs-are-anything-but-fast-and-if-you]]
