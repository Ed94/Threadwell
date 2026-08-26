---
title: "Yes, you should use malloc sparingly."
type: archive
source: twitter
source_url: "https://x.com/EskilSteenberg/status/1738667314436816968"
author: "Eskil Steenberg"
handle: EskilSteenberg
post_id: "1738667314436816968"
date: 2023-12-23
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - bmcnett
description: "Yes, you should use malloc sparingly."
in_reply_to: ""
parent_post_id: "1738591742541414523"
---

## Source

- URL: https://x.com/EskilSteenberg/status/1738667314436816968
- Author: Eskil Steenberg (@EskilSteenberg)
- Posted: 2023-12-23 21:06:05

## Branch

**1/** **@EskilSteenberg** ^1738667314436816968

Yes, you should use malloc sparingly. I see a lot of people making multiple calls for multiple buffers, when they could be combined to one malloc.

However, a big advantage of malloc, is that you can use realloc. realloc relies on being in control of the address space, and being able to remap memory pages in address space to avoid copying. This is not something you can do in userspace yourself.

A lot of times you don't in advance know how much memory you will need for a task (say parsing a file), so you may be forced to either, break it up in lots of small allocations, or do a pass just to determine how much memory will be needed, so that you can allocate once and then do the computation. realloc enables you to speculatively guess how much memory will be needed, and then in case you need more, realloc on the fly. If you do a good job of guessing you will rarely need that realloc, but the ability to extend memory simplifies memory management significantly.

## Related

- Spine: [[archive/threads/bmcnett/2023-12-23-even-among-performance-minded-folks-theres-a]]
