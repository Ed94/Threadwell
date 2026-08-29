---
title: "@AgileJebrim mapreduce."
type: archive
source: twitter
source_url: "https://x.com/tomcr2100/status/2058461731639161009"
author: "Tom Keresztes"
handle: tomcr2100
post_id: "2058461731639161009"
date: 2026-05-24
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim mapreduce."
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/tomcr2100/status/2058461731639161009
- Author: Tom Keresztes (@tomcr2100)
- Posted: 2026-05-24 08:14:55

## Branch

**1/** **@tomcr2100** ^2058461731639161009

**@AgileJebrim**

mapreduce. simple enough answer ? 😉

**2/** **@AgileJebrim** ^2058530982907490419

**@tomcr2100**

Design its implementation.

**3/** **@tomcr2100** ^2059204310630568267

**@AgileJebrim**

start with processing in N chunks, every chunk is a wave, loading wide to feed ALU, and avoid trashing cache by different wave reads.  Waves write to a fixed location in a buffer of size N. Works for sets that don't fit into memory (transfers). Overflow TBD. Out of characters👾

**4/** **@AgileJebrim** ^2059273072255844710

**@tomcr2100**

I don’t see any additions or reductions discussed, just memory loads and stores.

**5/** **@tomcr2100** ^2059311468978262438

**@AgileJebrim**

Sorry, typical twitter superficial moment. I meant each block reduces a portion of the array, multiple kernel invocations to reduce sync, and try to rely on sequential addressing d[i] + d[i + offset] to avoid bank conflicts when writing the result to global memory.

**6/** **@AgileJebrim** ^2059311961096020211

**@tomcr2100**

Can you show me what the first for loop looks like?

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
