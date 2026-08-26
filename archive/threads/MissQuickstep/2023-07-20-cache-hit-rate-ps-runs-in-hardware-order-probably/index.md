---
title: "Cache hit rate - PS runs in hardware order (probably Morton Z-Order), CS runs in linear order."
type: archive
source: twitter
source_url: "https://x.com/MissQuickstep/status/1682066496304955393"
author: "Layla Mah @missquickstep@mastodon.gamedev.place"
handle: MissQuickstep
post_id: "1682066496304955393"
date: 2023-07-20
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - MissQuickstep
description: "Cache hit rate - PS runs in hardware order (probably Morton Z-Order), CS runs in linear order."
in_reply_to: ""
---

## Source

- URL: https://x.com/MissQuickstep/status/1682066496304955393
- Author: Layla Mah @missquickstep@mastodon.gamedev.place (@MissQuickstep)
- Posted: 2023-07-20 16:34:38

## Thread

**1/** **@MissQuickstep** ^1682066496304955393

Cache hit rate - PS runs in hardware order (probably Morton Z-Order), CS runs in linear order.

Branches: [[archive/threads/MissQuickstep/2023-07-20-cache-hit-rate-ps-runs-in-hardware-order-probably/2023-07-21-sopyer-could-be-but-with-linear-order-and-linear-layour]], [[archive/threads/MissQuickstep/2023-07-20-cache-hit-rate-ps-runs-in-hardware-order-probably/2023-07-21-kenpex-not-only-on-lots-of-hw-the-rop-caches-can-be]]

**2/** **@vassvik** ^1682134652050452488

**@MissQuickstep**

Shouldn't make a big difference in practice.  A compute shader has spatial grouping where most waves/warps will sample adjacent memory and hit relatively high bandwidth and cache utilization even in the naive implementations. 

No way 512x512 is BW/cache bound, though

**3/** **@NOTimothyLottes** ^1682136826553745408

**@vassvik** **@MissQuickstep**

You can look at what I did for CAS/FSR1/etc: Simplified {64,1,1} to {8x8} lane remapping (so 4x1 lanes map to a 2x2), semi-persistent waves to avoid wait on store complete for wave relaunch and get better L0$2work mapping, etc. Have to make sure DCC matches (PS vs CS paths). Etc.
