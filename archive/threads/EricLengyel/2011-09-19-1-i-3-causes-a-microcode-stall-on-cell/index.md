---
title: "@max_mcguire (1 << i) & 3 causes a microcode stall on Cell."
type: archive
source: twitter
source_url: "https://x.com/EricLengyel/status/115927553398685696"
author: "Eric Lengyel"
handle: EricLengyel
post_id: "115927553398685696"
date: 2011-09-19
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - EricLengyel
description: "@max_mcguire (1 << i) & 3 causes a microcode stall on Cell."
in_reply_to: ""
---

## Source

- URL: https://x.com/EricLengyel/status/115927553398685696
- Author: Eric Lengyel (@EricLengyel)
- Posted: 2011-09-19 23:17:37

## Thread

**1/** **@EricLengyel** ^115927553398685696

**@max_mcguire**

(1 << i) & 3 causes a microcode stall on Cell. A faster alternative, even though 2X the instrs, is (i + 1) & ((i - 2) >> 1).
