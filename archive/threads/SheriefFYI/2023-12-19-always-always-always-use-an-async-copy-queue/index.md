---
title: "Always always always use an async copy queue"
type: archive
source: twitter
source_url: "https://x.com/SheriefFYI/status/1737126160402665958"
author: "Sherief, FYI"
handle: SheriefFYI
post_id: "1737126160402665958"
date: 2023-12-19
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SheriefFYI
description: "Always always always use an async copy queue"
in_reply_to: ""
---

## Source

- URL: https://x.com/SheriefFYI/status/1737126160402665958
- Author: Sherief, FYI (@SheriefFYI)
- Posted: 2023-12-19 15:02:05

## Thread

**1/** **@SheriefFYI** ^1737126160402665958

Always always always use an async copy queue

**2/** **@NOTimothyLottes** ^1737161181524095352

**@SheriefFYI**

To be fair, that is only the case on PC if one can afford to delay waiting for transfer completion for a few frames (aka via cmd completion fence on VK), because queue to queue syncs (aka via VK semaphores) are perf-death-style CPU interrupt based ...

Branches: [[archive/threads/SheriefFYI/2023-12-19-always-always-always-use-an-async-copy-queue/2023-12-19-lectem-wait-is-this-an-issue-with-vk-only-or-d3d12-too]]

**3/** **@NOTimothyLottes** ^1737162074172637506

**@SheriefFYI**

... so for latency sensitive stuff, either stuff it via CPU writes to DEVICE_LOCAL+HOST_VISIBLE (or large BAR), or a limited kernel size copy shader if needing image stuffing

Branches: [[archive/threads/SheriefFYI/2023-12-19-always-always-always-use-an-async-copy-queue/2023-12-19-SheriefFYI-queue-to-queue-syncs-via-cpu-need-to-go]], [[archive/threads/SheriefFYI/2023-12-19-always-always-always-use-an-async-copy-queue/2023-12-19-_woookie_-yup-right-now-i-async-copy-mesh-and-textures-data]], [[archive/threads/SheriefFYI/2023-12-19-always-always-always-use-an-async-copy-queue/2023-12-19-pATjako-i-dont-do-async-textures-buffers-in-my-gpu]], [[archive/threads/SheriefFYI/2023-12-19-always-always-always-use-an-async-copy-queue/2023-12-20-Meetem4-whats-the-best-way-of-doing-that-if-rebar-is-not]]
