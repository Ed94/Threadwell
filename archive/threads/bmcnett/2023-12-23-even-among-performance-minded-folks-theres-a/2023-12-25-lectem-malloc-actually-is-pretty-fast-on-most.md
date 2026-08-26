---
title: "@bmcnett @forked_franz malloc() actually is pretty fast on most implementation."
type: archive
source: twitter
source_url: "https://x.com/lectem/status/1739179298383142915"
author: "Clément Grégoire"
handle: lectem
post_id: "1739179298383142915"
date: 2023-12-25
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - bmcnett
description: "@bmcnett @forked_franz malloc() actually is pretty fast on most implementation."
in_reply_to: ""
parent_post_id: "1738591742541414523"
---

## Source

- URL: https://x.com/lectem/status/1739179298383142915
- Author: Clément Grégoire (@lectem)
- Posted: 2023-12-25 07:00:31

## Branch

**1/** **@lectem** ^1739179298383142915

**@bmcnett** **@forked_franz**

malloc() actually is pretty fast on most implementation.
free() on the other hand... Can be random.

The main problem with mem allocations often is that it does allocations at all, when they could be skipped.
As always "it depends" of the context (OS, allocator, sizes,count, ...)

## Related

- Spine: [[archive/threads/bmcnett/2023-12-23-even-among-performance-minded-folks-theres-a]]
