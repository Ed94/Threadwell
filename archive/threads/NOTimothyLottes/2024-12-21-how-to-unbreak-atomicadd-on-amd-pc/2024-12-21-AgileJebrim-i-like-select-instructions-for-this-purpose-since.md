---
title: "@NOTimothyLottes I like select instructions for this purpose since all sides are guaranteed to execute."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1870336609322934725"
author: "Jebrim"
handle: AgileJebrim
post_id: "1870336609322934725"
date: 2024-12-21
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes I like select instructions for this purpose since all sides are guaranteed to execute."
in_reply_to: ""
parent_post_id: "1870334592411922580"
---

## Source

- URL: https://x.com/AgileJebrim/status/1870336609322934725
- Author: Jebrim (@AgileJebrim)
- Posted: 2024-12-21 05:12:51

## Branch

**1/** **@AgileJebrim** ^1870336609322934725

**@NOTimothyLottes**

I like select instructions for this purpose since all sides are guaranteed to execute. Still not sure about this whole negative indexing bit though. I may still want to just do a redundant thing like atomicAdd(0) for those other lanes to prevent leveraging undefined behavior.

**2/** **@NOTimothyLottes** ^1870337466630029780

**@AgileJebrim**

You certainly don't want atomicAdd(adr,0), esp if the zero is dynamic generated. Because the HW has to loop through 64 requests on wave64 (say AMD's HW). You'd stall out your vector memory pipeline completely.

**3/** **@NOTimothyLottes** ^1870338068739207619

**@AgileJebrim**

In the slim chance the out-of-bounds disable is done during the HW loop instead of before the loop (aka bad vs good HW design), there is a second workaround ...

**4/** **@NOTimothyLottes** ^1870338498445897775

**@AgileJebrim**

You make the atomicAdd(adr,0) where adr is incrementing by 4-bytes (for a 32-bit atomic) and they all stay on the same cacheline (assuming wave32 and systems that have 128-bit cachelines like NV+AMD) ...

**5/** **@NOTimothyLottes** ^1870338840319398031

**@AgileJebrim**

This is not as good because the atomics will be sent (take time/power), but the atomic units do all 32-bit words on one line in parallel (on good AMD/NV HW) so it won't be as bad as 32|64 atomics to the same address (which get serialized in request and execution)

## Related

- Spine: [[archive/threads/NOTimothyLottes/2024-12-21-how-to-unbreak-atomicadd-on-amd-pc]]
