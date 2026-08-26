---
title: "RDNA3 ISA Guide Comments"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1604260386659880961"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1604260386659880961"
date: 2022-12-17
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "RDNA3 ISA Guide Comments"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1604260386659880961
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2022-12-17 23:40:56

## Thread

**1/** **@NOTimothyLottes** ^1604260386659880961

RDNA3 ISA Guide Comments
(1.) Driver: Instead of padding 256 bytes with S_CODE_END, how about putting the next shader in there (looking at you post process passes, with consistent temporal ordering).

Branches: [[archive/threads/NOTimothyLottes/2022-12-17-rdna3-isa-guide-comments/2022-12-19-abductee_org-cool-any-similar-comments-on-cuda12-ptx-sass]]

**2/** **@NOTimothyLottes** ^1604263778106892292

(2.) VGPR increase: Traditionally with 8 VGPR allocation granularity the target would be 64 VGPRs/wave or under. Now with 12 granularity a compiler can likely miss the 64 VGPR target and get to 96 without seeing a problem in those cases.

**3/** **@NOTimothyLottes** ^1604265437281271809

(3.) S_MEMREALTIME went to S_SENDMSG_RTN+S_WAITCNT (side effect, more opcode space), these would include a code motion barrier anyway. Would like a VK extension to query the "typically 100 MHz" fixed frequency amount: lots of nice things you can do with a real shader wallclock!

**4/** **@NOTimothyLottes** ^1604267130299596803

(4.) Really nice cache control via {SRD llc_noalloc, opcode DLC/SLC/GLC}. Wish there was a way to access using layout qualifier aliasing in VK. Esp 'STREAM' on loads, to avoid cache pollution when no reuse is known by the developer.

**5/** **@NOTimothyLottes** ^1604268044464930817

(5.) "Dealloc VGPRs" - CS waves need to wait until all pending stores return "finished" before the wave exits. But now the VGPRs can be returned before waiting (to be used by a new workgroup). However, persistent or semi-persistent waves is still the way to go IMO.

**6/** **@NOTimothyLottes** ^1604485986234388481

(6.) V_PERMLANE64 - Likely no more V_READLANE waterfall for dynamic index shuffle in Wave64 mode (don't have a RDNA3 to dump disassembly), but will LDS still be faster than the complex sequence of {PERMLANE16, PERMLANEX16, PERMLANE64} related logic?
