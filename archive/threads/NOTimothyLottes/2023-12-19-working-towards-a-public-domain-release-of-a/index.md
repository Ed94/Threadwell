---
title: "Working towards a public-domain release of a cleaned version of my Win32 Vulkan NV+AMD compute graphics platform."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1737198887914377512"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1737198887914377512"
date: 2023-12-19
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Working towards a public-domain release of a cleaned version of my Win32 Vulkan NV+AMD compute graphics platform."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1737198887914377512
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-12-19 19:51:05

## Thread

**1/**

Working towards a public-domain release of a cleaned version of my Win32 Vulkan NV+AMD compute graphics platform. What I used last for rapid prototyping (which is also IMO fine for releasable software). Won't call it an 'Engine' because it only provides tools to hang yourself ...

**2/**

Simplified the error logger today. Memory mapped file is definitely the way to go, one atomic per message, log multiple sessions, fixed size file acts like a message ring buffer. Background thread keeps the last message updating the same line on the console (for easy debug).

![](https://pbs.twimg.com/media/GBvFvOXXMAAFLXS?format=png&name=orig)
![](https://pbs.twimg.com/media/GBvFvOWX0AAxSuU?format=png&name=orig)

**3/**

Multi-session is nice, since the binary auto reloads in some cases (crash, etc), want to see why the reload happened, so don't want to clear the log. Yes, I still don't use debuggers, this logger + runtime shader recompile is all I use personally for dev work.
