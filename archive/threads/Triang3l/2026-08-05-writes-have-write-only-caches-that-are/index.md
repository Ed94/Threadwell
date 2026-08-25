---
title: "\"writes … have write-only caches that are invalidated, and all update bits are sent to memory AT THE END OF A CLAUSE\""
type: archive
source: twitter
source_url: "https://x.com/Triang3l/status/2084985800836477433"
author: "🔺 TriΔng3l 🔺 🐸"
handle: Triang3l
post_id: "2084985800836477433"
date: 2026-08-05
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - Triang3l
description: "\"writes … have write-only caches that are invalidated, and all update bits are sent to memory AT THE END OF A CLAUSE\""
in_reply_to: ""
---

## Source

- URL: https://x.com/Triang3l/status/2084985800836477433
- Author: 🔺 TriΔng3l 🔺 🐸 (@Triang3l)
- Posted: 2026-08-05 12:52:06

## Thread

**1/** **@Triang3l** ^2084985800836477433

"writes … have write-only caches that are invalidated, and all update bits are sent to memory AT THE END OF A CLAUSE"

Like whaaat, do I need an ALU NOP to read what I've just written to an SSBO?

Far easier to list what makes sense in TeraScale compute shaders than what doesn't

Branches: [[archive/threads/Triang3l/2026-08-05-writes-have-write-only-caches-that-are/2026-08-05-NOTimothyLottes-that-clause-based-arch-was-interesting-in-many]]

**2/** **@Triang3l** ^2084987573382824214

A clause is a sequence of ALU, buffer/texture SRV fetch, or LDS/GDS instructions.

However, UAV writes are "control flow" export instructions outside clauses.

But you can read from buffer UAVs via uncached SRVs (quicker), but what if you read in the first clause after the write?

**3/** **@Triang3l** ^2084991034807750781

(Though it's pretty pointless to read back the value just written to an SSBO, but with storage texel buffers that may be done for format conversion.)
