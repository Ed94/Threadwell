---
title: "@SebAaltonen TATAS (read-only inner-loop) is a much better pattern for a multicore system with multiple caches (https://github.com/concurrencykit/ck/blob/master/include/spinlock/fas.h#L77)."
type: archive
source: twitter
source_url: "https://x.com/0xF390/status/1125432870510759937"
author: "Samy Al Bahra"
handle: 0xF390
post_id: "1125432870510759937"
date: 2019-05-06
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen TATAS (read-only inner-loop) is a much better pattern for a multicore system with multiple caches (https://github.com/concurrencykit/ck/blob/master/include/spinlock/fas.h#L77)."
in_reply_to: ""
parent_post_id: "1125064645637738496"
---

## Source

- URL: https://x.com/0xF390/status/1125432870510759937
- Author: Samy Al Bahra (@0xF390)
- Posted: 2019-05-06 16:11:20

## Branch

**1/** **@0xF390** ^1125432870510759937

**@SebAaltonen**

TATAS (read-only inner-loop) is a much better pattern for a multicore system with multiple caches (https://github.com/concurrencykit/ck/blob/master/include/spinlock/fas.h#L77).

**2/** **@SebAaltonen** ^1125617029438947328

**@0xF390**

This is TATAS too. It does standard read until read returns unlocked (|| is short circuited -> exchange doesn’t run when outer test succeeds). Your code has extra CAS outer case. Not needed. Just makes fast path (no lock) slower.

**3/** **@0xF390** ^1125624687663427584

**@SebAaltonen**

Edits. You're right! I read the wrong block. Regarding the Concurrency Kit code, which CAS outer-case are you referring to? There is none, FAS = xchg.

## Related

- Spine: [[archive/threads/SebAaltonen/2019-05-05-this-is-how-you-write-a-good-x64-spinlock-use-two]]
