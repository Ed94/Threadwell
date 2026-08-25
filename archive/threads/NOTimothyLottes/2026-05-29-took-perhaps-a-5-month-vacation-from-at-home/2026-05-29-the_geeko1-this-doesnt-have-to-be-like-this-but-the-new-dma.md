---
title: "@NOTimothyLottes this doesn't have to be like this .."
type: archive
source: twitter
source_url: "https://x.com/the_geeko1/status/2060203539775869114"
author: "عَبْدُالهَادِي"
handle: the_geeko1
post_id: "2060203539775869114"
date: 2026-05-29
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes this doesn't have to be like this .."
in_reply_to: ""
parent_post_id: "2060198133905199300"
---

## Source

- URL: https://x.com/the_geeko1/status/2060203539775869114
- Author: عَبْدُالهَادِي (@the_geeko1)
- Posted: 2026-05-29 03:36:15

## Branch

**1/** @the_geeko1

@NOTimothyLottes

this doesn't have to be like this .. but the new DMA-buf changes are not upstreamed yet on linux .. if that's done I would love to upstream my changes to the AMD KMD so u can have actual physical addresses of VRAM exported.

**2/** @the_geeko1

@NOTimothyLottes

on the other side u could assign vfio-pci driver to the other device and write the drivers on user-space on both CPU/GPU and cut out the kernel drivers out the picture which is quite nice.

**3/** @NOTimothyLottes

@the_geeko1

This reminds me, I don't actually know how GPU audio (HDMI out) works, but I've always assumed it was a private onboard memory where regular shader load/store doesn't have access. The bandwidth though is tiny, so that round trip through the CPU is mostly just a latency concern

**4/** @NOTimothyLottes

@the_geeko1

And by latency, it's mostly a question of how to get a consistent small workload through the GPU at a periodic schedule (feed the data to the CPU right before it's needed for the copy back to the GPU)

**5/** @NOTimothyLottes

@the_geeko1

Networking is interesting, in that one could do a SALU/SMEM approach to processing packets, or one could do something like work with only fixed size UDP packets and process them using VALU/VMEM, in which case the CPU could interleave/deinterleave the dwords for good GPU access

**6/** @NOTimothyLottes

@the_geeko1

With the SALU/SMEM approach, having direct communication with the network card could be nice, but I doubt the linux folks want to allow raw UDP header/payload DMA scatter/gather bypassing all the OS layers

**7/** @the_geeko1

@NOTimothyLottes

It's always an option to drop the kernel driver and assign the vfio-pci driver and write a custom driver on user space .. also there some NICs with a programmable chip on them .. they could be programmed to DMA some packets into CPU memory like normal and some into the GPU

**8/** @the_geeko1

@NOTimothyLottes

Nvidia calls them DPU I think ? those are also useful for GPUs to share data if on the same network .. and I think that is the main driver behind Nvidia's work on restructuring how the DMA-bufs work on linux.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2026-05-29-took-perhaps-a-5-month-vacation-from-at-home]]
