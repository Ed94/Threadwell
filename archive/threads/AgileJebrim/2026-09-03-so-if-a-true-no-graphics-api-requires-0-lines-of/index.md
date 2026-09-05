---
title: "So if a true “No Graphics API” requires 0 lines of user CPU code, does that make it infinitely better than this? Asking for a friend."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/2095604397602382070"
author: "Jebrim"
handle: AgileJebrim
post_id: "2095604397602382070"
date: 2026-09-03
archived: 2026-09-04
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "So if a true “No Graphics API” requires 0 lines of user CPU code, does that make it infinitely better than this? Asking for a friend."
in_reply_to: ""
---

## Source

- URL: https://x.com/AgileJebrim/status/2095604397602382070
- Author: Jebrim (@AgileJebrim)
- Posted: 2026-09-03 20:06:37

## Thread

**1/** **@AgileJebrim** ^2095604397602382070

So if a true “No Graphics API” requires 0 lines of user CPU code, does that make it infinitely better than this? Asking for a friend.

**2/** **@NOTimothyLottes** ^2095649154076709316

**@AgileJebrim**

If a new gfx API can be implemented over current graphics APIs, it is by definition not adding anything useful (it’s a lower common denominator software architecture). One shouldn’t try to confuse a project’s abstraction layer with what is actually needed to do something new.

**3/** **@ozeniken** ^2095654079586324657

**@NOTimothyLottes** **@AgileJebrim**

seb's api requires vulkan extensions published THIS year. it's not lowest common denominator and it's not (much of) an abstraction layer, it's a refined subset of what you need on modern gpus. full vulkan is the lowest common denominator because it has to support gpus from 2012

**4/** **@NOTimothyLottes** ^2095656131473412099

**@ozeniken** **@AgileJebrim**

What we have actually needed for GPUs since the first GCN isn’t available via extensions today. For example no extension fixes anything broken in the common way both Windows and Linux handle multi queue sync primitives with coalesced CPU interrupts.

**5/** **@NOTimothyLottes** ^2095657109291438332

**@ozeniken** **@AgileJebrim**

No extension provides a way to use a precompiled GPU binary generated with external assembler or compiler. Meaning all the existing documented shader side issues that haven’t been fixed in a decade plus are still there.

**6/** **@NOTimothyLottes** ^2095658814972264736

**@ozeniken** **@AgileJebrim**

Also sebbbi tends to be a proponent for the slowest way to access buffers on all the AMD based consoles, using generic 64-bit pointers, and likely that new extension you are referring to is to get this HW buffer slow path.

**7/** **@NOTimothyLottes** ^2095661843813396514

**@ozeniken** **@AgileJebrim**

Back when I worked at AMD I covered the HW fast paths for binding/etc via a bind everything once/frame model using giant DYNAMIC buffer to get the USER SGPR preload. Later “extensions” had been more modeled on slower DX12 like portability and actually dont support HW fast path.

**8/** **@NOTimothyLottes** ^2095663350071930982

**@ozeniken** **@AgileJebrim**

Best interface on all GCN and RDNA for vector buffer access is TBUFFER instructions which to this day has no extension support for from AMD. HW path: one preloaded descriptor can access any type with just a 32-bit index and tons of free HW address generation features.

**9/** **@NOTimothyLottes** ^2095665044050629025

**@ozeniken** **@AgileJebrim**

No one PC side ever exposed a proper interface to LDS. Which is why when you look at the disassembly it’s littered with ALU waste to map a implicit scaled index based shader language to a byte offset based HW ISA and no API reskin is set to fix this mess either

**10/** **@NOTimothyLottes** ^2095665525351129571

**@ozeniken** **@AgileJebrim**

Or for real horrors look at all the disassembly of shaders that use atomics where the compiler force inserts all sorts of stupid programmer workarounds which de-optimize fast algorithms. Again no gfx API reskin is set to fix these problems.

**11/** **@ozeniken** ^2095666556445356123

**@NOTimothyLottes** **@AgileJebrim**

these are valid criticisms but you're missing the point, this is a forward looking api. https://x.com/SebAaltonen/status/2095567431481655668?s=20
