---
title: "Nothing changes the physical reality of the inefficiency of a vector of 64-bit pointers on the GPU."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2095864387957412044"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2095864387957412044"
date: 2026-09-04
archived: 2026-09-04
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Nothing changes the physical reality of the inefficiency of a vector of 64-bit pointers on the GPU."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2095864387957412044
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-09-04 13:19:44

## Thread

**1/** **@NOTimothyLottes** ^2095864387957412044

Nothing changes the physical reality of the inefficiency of a vector of 64-bit pointers on the GPU. It will always take double the register file space, double the ALU ops to manipulate compared to using HW shifted 32-bit indexes.

**2/** **@NOTimothyLottes** ^2095865683745632563

4-byte type with a shifted 32-bit index supports a 16 GiB address window of buffer access. A 16-byte type with a shifted 32-bit index supports a 64 GiB address windows of buffer access. More than enough given where {cost,thermal,power,perf} scales to in a human lifetime.

**3/** **@NOTimothyLottes** ^2095866371796058560

Nothing changes the reality that 64-bit pointer loads of packed types like {shared exponent}, {11,11,10 float}, {8:8:8:8 sRGB}, and even {10:10:10:2 unorm} are effectively too slow to be of any use due to ALU overhead to decode.

**4/** **@NOTimothyLottes** ^2095866785899659649

So the argument to say raw non-typed 64-bit pointers are future forward is to say discard the very basic of compressed types in buffer storage, ie the foundation of programmable vertex fetch. That is just stupid.

**5/** **@NOTimothyLottes** ^2095867642342941073

To argue that peak always hit in the cache performance of say raw 32-bit values grabbed from 64-bit pointers on any architecture is what correlates with actual performance in real complex programs is also totally naive.

**6/** **@NOTimothyLottes** ^2095868058485068266

If you are bandwidth bound, then it is often the HW type conversion that is important. If you are ALU bound, then it is getting logic off the ALU that is important (that 2x pointer math cost, or type conversion cost, etc), and if you are latency bound, then the 2x vgpr cost kills
