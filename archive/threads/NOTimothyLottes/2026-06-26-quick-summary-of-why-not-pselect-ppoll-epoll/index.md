---
title: "Quick summary of why not {pselect, ppoll, epoll_pwait2} style non-TCP IO [it can amplify kernel transitions]."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2070337342854832468"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2070337342854832468"
date: 2026-06-26
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Quick summary of why not {pselect, ppoll, epoll_pwait2} style non-TCP IO [it can amplify kernel transitions]."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2070337342854832468
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-06-26 02:44:22

## Thread

**1/** **@NOTimothyLottes** ^2070337342854832468

Quick summary of why not {pselect, ppoll, epoll_pwait2} style non-TCP IO [it can amplify kernel transitions]. For UDP stuff blocking {sendmmsg,recvmmsg (with timeout)} amortizes out kernel transitions.

![](https://pbs.twimg.com/media/HLtP4RgWgAADbir?format=png&name=orig)
Branches: [[archive/threads/NOTimothyLottes/2026-06-26-quick-summary-of-why-not-pselect-ppoll-epoll/2026-06-26-AgileJebrim-sendmmsg-recvmmsg-can-only-work-with-1024-packets]], [[archive/threads/NOTimothyLottes/2026-06-26-quick-summary-of-why-not-pselect-ppoll-epoll/2026-06-26-BigP4P4Smurf-take-a-look-at-http-lalists-stanford-edu-lad-2001]]
