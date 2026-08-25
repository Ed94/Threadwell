---
title: "@rfleury This isn't such a strong argument considering there's a \"leak\" with the regular call to `new`."
type: archive
source: twitter
source_url: "https://x.com/MoveZig4/status/1917463363300610136"
author: "Kyle"
handle: MoveZig4
post_id: "1917463363300610136"
date: 2025-04-30
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury This isn't such a strong argument considering there's a \"leak\" with the regular call to `new`."
in_reply_to: ""
parent_post_id: "1917431895786414425"
---

## Source

- URL: https://x.com/MoveZig4/status/1917463363300610136
- Author: Kyle (@MoveZig4)
- Posted: 2025-04-30 06:17:45

## Branch

**1/** **@MoveZig4** ^1917463363300610136

**@rfleury**

This isn't such a strong argument considering there's a "leak" with the regular call to `new`. To my untrained eye under clang-19 the generated assembly for unique_ptr is a bit smaller/slimmer, with less stack usage - https://godbolt.org/z/sxejEsbe4 - can't turn on -O anything sadly

## Related

- Spine: [[archive/threads/rfleury/2025-04-30-to-the-degree-this-is-true-its-only-in-a]]
