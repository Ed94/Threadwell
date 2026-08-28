---
title: "Don’t use spinlock for waits."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1125065316650889217"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1125065316650889217"
date: 2019-05-05
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Don’t use spinlock for waits."
in_reply_to: ""
parent_post_id: "1125064645637738496"
---

## Source

- URL: https://x.com/SebAaltonen/status/1125065316650889217
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2019-05-05 15:50:48

## Branch

**1/** **@SebAaltonen** ^1125065316650889217

Don’t use spinlock for waits. Use spinlock only to guard something that is guaranteed to return quickly. If you have an operation that is often fast but sometimes slow, use two stage spinlock with internal OS mutex.

**2/** **@SebAaltonen** ^1125067183476944896

Naive (bad) vs optimized (good) performance. See above post for code.

![](https://pbs.twimg.com/media/D50Ko4mXoAAR97L?format=jpg&name=orig)

## Related

- Spine: [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two]]
