---
title: "SAR on a control word can in theory grab 3 values."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2077241596869751029"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2077241596869751029"
date: 2026-07-15
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "SAR on a control word can in theory grab 3 values."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2077241596869751029
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-15 03:59:24

## Thread

**1/**

SAR on a control word can in theory grab 3 values.
SF (sign flag) is set to MSB bit
CF (carry flag) is set to what shifts into bit -1
and output

The SF and CF can be used for CMOVcc
Output can be used for another shift (after CMOVccs)
