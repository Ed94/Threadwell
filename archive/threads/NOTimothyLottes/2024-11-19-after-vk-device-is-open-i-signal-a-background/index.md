---
title: "After VK device is open, I signal a background thread to load the SPIR-V module, while building the descriptor set layout, which then unblocks PSO compile on background threads."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1858715434436227544"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1858715434436227544"
date: 2024-11-19
archived: 2026-08-23
status: draft
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "After VK device is open, I signal a background thread to load the SPIR-V module, while building the descriptor set layout, which then unblocks PSO compile on background threads."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1858715434436227544
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-11-19 03:34:27

## Thread

**1/**

After VK device is open, I signal a background thread to load the SPIR-V module, while building the descriptor set layout, which then unblocks PSO compile on background threads. And the rest of the VK setup runs in parallel. Working towards swap creation.
