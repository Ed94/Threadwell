---
title: "@nicbarkeragain Clang failed to recognize it should use a select op in the IR and using a ternary helped."
type: archive
source: twitter
source_url: "https://x.com/jakubtomsu_/status/1947602738478452869"
author: "Jakub Tomšů"
handle: jakubtomsu_
post_id: "1947602738478452869"
date: 2025-07-22
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - nicbarkeragain
description: "@nicbarkeragain Clang failed to recognize it should use a select op in the IR and using a ternary helped."
in_reply_to: ""
parent_post_id: "1947506500194472221"
---

## Source

- URL: https://x.com/jakubtomsu_/status/1947602738478452869
- Author: Jakub Tomšů (@jakubtomsu_)
- Posted: 2025-07-22 10:20:52

## Branch

**1/** **@jakubtomsu_** ^1947602738478452869

**@nicbarkeragain**

Clang failed to recognize it should use a select op in the IR and using a ternary helped. This gets also unrolled and vectorized and it ends up being faster.

GCC seems to always catch this, no idea why is clang being dumb even in a trivial case like this

https://godbolt.org/z/jMqazcenq

![](https://pbs.twimg.com/media/GwdEnC_XgAAlhqI?format=jpg&name=orig)

## Related

- Spine: [[archive/threads/nicbarkeragain/2025-07-22-branchless-programming-is-a-term-used-to-describe]]
