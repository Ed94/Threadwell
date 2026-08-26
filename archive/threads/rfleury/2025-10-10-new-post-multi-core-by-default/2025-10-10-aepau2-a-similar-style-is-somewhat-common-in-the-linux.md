---
title: "@rfleury A similar style is somewhat common in the Linux server world, where it is called \"thread-per-core\"."
type: archive
source: twitter
source_url: "https://x.com/aepau2/status/1976774348905365806"
author: "aeesz4"
handle: aepau2
post_id: "1976774348905365806"
date: 2025-10-10
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury A similar style is somewhat common in the Linux server world, where it is called \"thread-per-core\"."
in_reply_to: ""
parent_post_id: "1976458516325073141"
---

## Source

- URL: https://x.com/aepau2/status/1976774348905365806
- Author: aeesz4 (@aepau2)
- Posted: 2025-10-10 22:18:26

## Branch

**1/** **@aepau2** ^1976774348905365806

**@rfleury**

A similar style is somewhat common in the Linux server world, where it is called "thread-per-core".
Each threads gets a separate event loop and socket it listens to, but the event loop sockets share the same ip/listening port via SO_REUSEPORT, and the kernel does the balancing.

## Related

- Spine: [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default]]
