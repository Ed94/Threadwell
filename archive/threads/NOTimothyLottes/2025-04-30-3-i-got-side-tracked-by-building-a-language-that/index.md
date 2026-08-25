---
title: "@onatt0 [3] I got side tracked by building a language that could be assembled from on the GPU in SIMD."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1917646466417381426"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1917646466417381426"
date: 2025-04-30
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@onatt0 [3] I got side tracked by building a language that could be assembled from on the GPU in SIMD."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1917646466417381426
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-04-30 18:25:20

## Thread

**1/** **@NOTimothyLottes** ^1917646466417381426

**@onatt0**

[3] I got side tracked by building a language that could be assembled from on the GPU in SIMD. However now I ask myself if that is just adding "complexity", because if programs are bounded in size, why not just focus on CPU non-parallel nested factoring (aka the forth-like way)

Branches: [[archive/threads/NOTimothyLottes/2025-04-30-3-i-got-side-tracked-by-building-a-language-that/2025-04-30-onatt0-imo-code-compilation-is-inherently-sequential]]

**2/** **@NOTimothyLottes** ^1917648900556558768

**@onatt0**

[4] 2-item data stack is an interesting compromise. Something I never considered. I left off ripping out the data stack completely.

**3/** **@NOTimothyLottes** ^1917650289978454504

**@onatt0**

[5] Can do this instead,
a. Track a "top" register (number)
b. Use symbols to override top register
c. Have push (store) just advance top to next reg (in circular queue)
Gets to easy unnamed arguments

**4/** **@NOTimothyLottes** ^1917651574354030636

**@onatt0**

[6] You mentioned VK is most "form filling" which I think is an accurate description. For most "C" like APIs I like to just lay out all the arguments in memory like a tape drive in the order that functions get called and source that tape at runtime for the calls ...

**5/** **@NOTimothyLottes** ^1917652037078065160

**@onatt0**

[7] They key concept here is that "common" arguments like the device are pushed onto the tape using store duplication when they are known (after device creation). So it's preemptive scatter, so later at call time there is no argument gather.

**6/** **@NOTimothyLottes** ^1917652589358858332

**@onatt0**

[8] Likely the majority of C/C++/OOP/bloatware is just shuffling data around in argument gather to support the concept of data stacks on HW that has no physical data stack.

Branches: [[archive/threads/NOTimothyLottes/2025-04-30-3-i-got-side-tracked-by-building-a-language-that/2025-04-30-onatt0-holy-truthnuke-and-people-think-c-is-the-optimal]]

**7/** **@NOTimothyLottes** ^1917653265329594372

**@onatt0**

[9] Could just pre-layout call arguments in order of usage, leverage data compression at init-time to unpack into memory before run-time. No more code to shuffle arguments, or set registers to immediates, etc. Just a common (cached) pre-call to consume args from the "tape"

Branches: [[archive/threads/NOTimothyLottes/2025-04-30-3-i-got-side-tracked-by-building-a-language-that/2025-04-30-onatt0-simply-brilliant]]
