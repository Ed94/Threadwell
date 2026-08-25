---
title: "One of the downsides of V_CNDMASK_B32 on AMD is that you burn the SGPRs on the VCC bool, so if you are selecting between constants, those require extra V_MOV_B32 ops."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1876093937632600106"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1876093937632600106"
date: 2025-01-06
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "One of the downsides of V_CNDMASK_B32 on AMD is that you burn the SGPRs on the VCC bool, so if you are selecting between constants, those require extra V_MOV_B32 ops."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1876093937632600106
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-01-06 02:30:25

## Thread

**1/** @NOTimothyLottes

One of the downsides of V_CNDMASK_B32 on AMD is that you burn the SGPRs on the VCC bool, so if you are selecting between constants, those require extra V_MOV_B32 ops. Would be much better to have fused cmp+mask so this limitation would be lifted!

![](https://pbs.twimg.com/media/Ggk5dIQWkAAoCWn?format=png&name=orig)

**2/** @NOTimothyLottes

Another night, another round of AMD compiler bugs. Sometimes AMD fails 'uint32_t packFloat2x16(f16vec2 v)' ... I'm seeing the 16-bit MSB cleared in this constant (yeah it's the slow V_CNDMASK_B32 case in the prior tweet)

![](https://pbs.twimg.com/media/Ggk7SBBXQAAJNbo?format=png&name=orig)

**3/** @NOTimothyLottes

Workaround is to use 'pack32(halfBitsToUint16(a))' instead (ie first convert the packed 16-bit float to packed 16-bit integer, then convert to 32-bit integer) ...

![](https://pbs.twimg.com/media/Ggk72RLXEAA0EH5?format=png&name=orig)

**4/** @NOTimothyLottes

One of my favorite AMD instructions V_BFI_B32 is unfortunately one that no intrinsic exists for on PC, and one that the AMD compiler often messes up the pattern matching for, sometimes it reduces to {AND,ADD} instead

![](https://pbs.twimg.com/media/GglKA6nW4AEtOIC?format=png&name=orig)
![](https://pbs.twimg.com/media/GglKXy4XcAAA_Og?format=png&name=orig)

**5/** @NOTimothyLottes

Just looking at the next 5 lines of disassembly shows another 2 perf bugs: the compiler transforms 3 operations into 5 operations because it cannot handle mixed packed and unpacked stuff. The 2 V_ANDs can be merged, and the LSHL and CVT should just be one op

![](https://pbs.twimg.com/media/GglQsALXYAAEfWI?format=png&name=orig)

**6/** @NOTimothyLottes

No way to work around those problems. Looks like bitfieldExtract 'v4' back-propagates something where the compiler ignores the .y in the packed logic, and then makes a mess of things scalarizing it. BFE only uses the 5-bit LSB of 'v4', so it's safe to leave junk in the other bits

![](https://pbs.twimg.com/media/GglWWmEX0AAO1ON?format=png&name=orig)
