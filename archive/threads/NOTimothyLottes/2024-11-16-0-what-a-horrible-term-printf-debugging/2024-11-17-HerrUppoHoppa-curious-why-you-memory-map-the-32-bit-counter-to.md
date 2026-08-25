---
title: "@NOTimothyLottes Curious why you memory map the 32 bit counter to the file."
type: archive
source: twitter
source_url: "https://x.com/HerrUppoHoppa/status/1858039804551663740"
author: "Pontus"
handle: HerrUppoHoppa
post_id: "1858039804551663740"
date: 2024-11-17
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Curious why you memory map the 32 bit counter to the file."
in_reply_to: ""
parent_post_id: "1857804669994565771"
---

## Source

- URL: https://x.com/HerrUppoHoppa/status/1858039804551663740
- Author: Pontus (@HerrUppoHoppa)
- Posted: 2024-11-17 06:49:44

## Branch

**1/**

@NOTimothyLottes Curious why you memory map the 32 bit counter to the file. Also why does it get half the file as opposed to just the end of the mapped region?

**2/**

@HerrUppoHoppa It's pow2 message lines so fixing wrap is AND(cnt,lines-1). Counter after that and needs to take a page minimum. So yes I could make the size slightly smaller, but just lazy. Counter in file because then multiple runs accumulate in the file for comparison.

**3/**

@NOTimothyLottes Ah I see, interesting solution!

## Related

- Spine: [[archive/threads/NOTimothyLottes/2024-11-16-0-what-a-horrible-term-printf-debugging]]
