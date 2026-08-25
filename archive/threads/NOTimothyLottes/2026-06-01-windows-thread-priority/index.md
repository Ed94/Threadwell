---
title: "Windows thread priority."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2061416116694442141"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2061416116694442141"
date: 2026-06-01
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Windows thread priority."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2061416116694442141
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-06-01 11:54:36

## Thread

**1/**

Windows thread priority. SeIncreaseBasePriorityPrivilege required to play in the (fake)"Realtime" class -BUT- apparently there is AvSetMmThreadCharacteristics() for "Pro Audio" and AvSetMmThreadPriority() which can bring up priority into realtime. Curious if games using today?

Branches: [[archive/threads/NOTimothyLottes/2026-06-01-windows-thread-priority/2026-06-02-iamwhosiam-i-dont-think-your-even-suppose-to-change-your]]

**2/**

Either way NtSetInformationThread() seems to be the way to just set {1-15} (non-realtime class) priority directly without the silly clamp(priorityClassBase+threadPriority,1,15) business
