---
title: "Renovating CPU clock code."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2060730425929080874"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2060730425929080874"
date: 2026-05-30
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Renovating CPU clock code."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2060730425929080874
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-05-30 14:29:54

## Thread

**1/**

Renovating CPU clock code. I'm assuming x86-64 TSC is always >= 1 GHz so that conversion of clock counter diff to nanoseconds is simply a MUL instruction fetching the RDX high 64-bit result (of the 128-bit computed). But figuring out how to do the inline asm was a pain.

![](https://pbs.twimg.com/media/HJku0L4WkAAZk5a?format=png&name=orig)
Branches: [[archive/threads/NOTimothyLottes/2026-05-30-renovating-cpu-clock-code/2026-05-31-FUZxxl-if-you-do-the-multiply-in-uint128-t-and-then]]

**2/**

Looks like NtQuerySystemInformation() with SystemHypervisorSharedPageInformation (aka 0xc5) gives 64-bit scalar for TSC that converts time to units of 10 MHz. So the smart way is to work in units of TSC, then do a subtraction of TSC terms, then MULHI to get {ms, us, or ns} time

**3/**

https://gist.github.com/pmttavara/6f06fc5c7679c07375483b06bb77430c - A great reference for getting TSC scaling multipliers on Linux and Windows
