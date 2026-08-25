---
title: "@onatt0 Related thoughts/"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1917642786804785230"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1917642786804785230"
date: 2025-04-30
archived: 2026-08-23
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@onatt0 Related thoughts/"
in_reply_to: ""
parent_post_id: "1917613300902146419"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1917642786804785230
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-04-30 18:10:43

## Branch

**1/** @NOTimothyLottes

@onatt0 Related thoughts/
[0] Having a low upper bound on the maximum complexity allowed in a program enables so much simplification. One can always move complexity into data, while keeping tight codebases.

**2/** @NOTimothyLottes

@onatt0 [1] Seems like you group symbols into pages where each page can have a string (shared with all symbols in the page), which when pared with limited fixed maximum symbol string size, is an elegant way of effectively supporting larger naming [I'll probably steal that idea next time]

**3/** @NOTimothyLottes

@onatt0 [2] I'm also a big fan of how you used 16:9 aspect to auto render all the debug info, symbol tables, disassembly, etc, alongside the source. I think many people are probably lost in the speed at which you can manipulate and test ideas while working on the source

**4/** @NOTimothyLottes

@onatt0 [3] I got side tracked by building a language that could be assembled from on the GPU in SIMD. However now I ask myself if that is just adding "complexity", because if programs are bounded in size, why not just focus on CPU non-parallel nested factoring (aka the forth-like way)

**5/** @NOTimothyLottes

@onatt0 [4] 2-item data stack is an interesting compromise. Something I never considered. I left off ripping out the data stack completely.

**6/** @NOTimothyLottes

@onatt0 [5] Can do this instead,
a. Track a "top" register (number)
b. Use symbols to override top register
c. Have push (store) just advance top to next reg (in circular queue)
Gets to easy unnamed arguments

**7/** @NOTimothyLottes

@onatt0 [6] You mentioned VK is most "form filling" which I think is an accurate description. For most "C" like APIs I like to just lay out all the arguments in memory like a tape drive in the order that functions get called and source that tape at runtime for the calls ...

**8/** @NOTimothyLottes

@onatt0 [7] They key concept here is that "common" arguments like the device are pushed onto the tape using store duplication when they are known (after device creation). So it's preemptive scatter, so later at call time there is no argument gather.

**9/** @NOTimothyLottes

@onatt0 [8] Likely the majority of C/C++/OOP/bloatware is just shuffling data around in argument gather to support the concept of data stacks on HW that has no physical data stack.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-04-30-i-laugh-when-people-say-c-is-like-assembly-they]]
