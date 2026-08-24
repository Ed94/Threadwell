---
title: "GPU Programming Tip Line Thread /"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1588902081502797826"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1588902081502797826"
date: 2022-11-05
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "GPU Programming Tip Line Thread /"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1588902081502797826
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2022-11-05 14:32:31

## Thread

**1/**

GPU Programming Tip Line Thread /

**2/**

[0] Normalization fail case is 'rsq(0)=INF*0=NaN', trim out intermediate INF to fix, 'normalize_safe(x){return x*min(MAX_FLOAT,rsq(dot(x,x)));}'

**3/**

[1] PC FP16 1/denormals generates INFs which can easily eventually result in NaNs, fix positives with 'rcp(max(x,SMALLEST_NORMAL))'

**4/**

[2] 'spirv-opt -Os' (optimize for size) is your weapon against "back-before-its-done--getting-groceries" IHV compile times

**5/**

[3] Driver ignoring your '[[dont_unroll]]', 'int eatThisBuddy=1+/*hidden-zero*/constantBuffer.zero[0];for(i=0;i<1024;i+=eatThisBuddy){...'

**6/**

[4] 'Ship-One-Shader' = One SPIR-V binary, use specialization constants to select shader at PSO generation time, minimizes released shader binary size

**7/**

[5] 'Ship-One-Shader' requires 'spirv-opt -Os'

**8/**

[6] Use signed 'mask=bitfieldExtract(int(v),bit,1)' to turn bit into all 0's or 1's mask

**9/**

[7] On PC for AMD's native V_BFI_B32 (to select bits based on mask) use 'Bfi(int src,int ins,int mask){return (ins&mask)|(src&(~mask));}'

**10/**

[8] Use 'bitfieldInsert(,,0,compileTimeImmediate)' hits fast V_BFI_B32 on AMD, and portable to other vendors

**11/**

[9] AMD ONLY: clamp(a,b,c) is implemented as med3(a,b,c), so can get V_MED3_* without an extension (in a non-portable way)

**12/**

[10] Bools as 0|1 floats '(a&b)|c' can be done via 'saturate(a*b+c)'

**13/**

[11] Bools as 0|1 floats '!(a&b)' can be done via '(-a)*b+1.0'

**14/**

[12] Convert INFs to NaNs via 'x*0.0+x'

**15/**

[13] Semi-persistent workgroup opt = reusing the workgroup for more work before exit (ie processing four 8x8 tiles in a 16x16 footprint using a 64-wide group)

**16/**

[14] Semi-persistent workgroups can be good for up to 10% perf on AMD (YMMV) ... assuming compiler doesn't fail VGPR allocation, check your disassembly

**17/**

[15] Semi-persistent workgroups gain by keeping more local work on the same L0, by factoring out wait for store on wave exit, and better scheduling

**18/**

[16] Merge passes to avoid round trip through DRAM, often huge wins there

**19/**

[17] Sometimes serial dependent passes can be merged into one shader to keep work in L2 for >10% gains, requires "unsafe you-shouldnt-do-that" logic that works

**20/**

[18] Proper double rate "packed" 16-bit can provides gains up to 30% depending on workload/platform (except NV)

**21/**

[19] Even without double rate 16-bit, 16-bit is the most important tool for managing register pressure problems, esp with smaller HW register limits or compiler troubles
