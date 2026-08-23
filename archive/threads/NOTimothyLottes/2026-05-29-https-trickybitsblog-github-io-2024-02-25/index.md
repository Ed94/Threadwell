---
title: "https://trickybitsblog.github.io/2024/02/25/timestamps.html is a nice related read, also I'm a little late to the https://ntdoc.m417z.com/system_hypervisor_user_shared_data party, but will have that sorted soon as well"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2060191401883619479"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2060191401883619479"
date: 2026-05-29
archived: 2026-08-23
status: draft
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "https://trickybitsblog.github.io/2024/02/25/timestamps.html is a nice related read, also I'm a little late to the https://ntdoc.m417z.com/system_hypervisor_user_shared_data party, but will have that sorted soon as well"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2060191401883619479
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-05-29 02:48:01

## Thread

**1/**

https://trickybitsblog.github.io/2024/02/25/timestamps.html is a nice related read, also I'm a little late to the https://ntdoc.m417z.com/system_hypervisor_user_shared_data party, but will have that sorted soon as well

**2/**

Other thought, I typically mmap an extra LOG file, and write via atomic to grab a fixed width line. No stdout. The log wraps around and exists for multiple executions or even parallel processes. It's the way to do it ... BUT ...

**3/**

... I think I'm going to just move the LOG file into the first N KiB of the CART file. So mmap'ed on CPU and GPU, and I can just bank on how "less" doesn't actually load the entire file while printing, so I can still see output on a console if needed for debug.

**4/**

And another random thought, can you force de-power the CPU by abusing the https://www.felixcloutier.com/x86/pause instruction for things that are not spin-loops :) Going to have to try this one at some point.

**5/**

Pushing data to GPU is really a no-brainer (write-combined stores), minus possibility of non-atomic write visibility, so I do simple stuff like always having a ring buffer of packets available where the GPU can validate each entry with a HASH, taking the latest valid one to use

**6/**

Also AMD exports non-cached memory in VK, so it's possible to poll on data the CPU pushes (via write combined stores to VRAM) on AMD a few times per frame even.

**7/**

The workaround for NVIDIA is if one wants to read N times per frame, then the CPU needs to duplicate the packet ring to N separate lines. Then the GPU is free to poll, but using separate cachelines each time.

**8/**

The route back for IO that needs to be routed through the CPU {audio out, network out} is a lot more unfun. AMD again has the nice uncached memory support, so that part is easy. NVIDIA well, would have to take the crappy mid-frame L2 writeback (likely) making CPU-read available

**9/**

Those who have tread here before with driver side logic (DMA transfers/etc) got screwed, Win+Linux driver idiots and their CPU interrupt based scheduling = completely useless. So getting the driver out of the picture is the way to go
