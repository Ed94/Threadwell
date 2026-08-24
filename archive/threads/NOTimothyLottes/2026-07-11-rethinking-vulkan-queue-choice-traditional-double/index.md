---
title: "Rethinking Vulkan queue choice."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2075769880092037309"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2075769880092037309"
date: 2026-07-11
archived: 2026-08-23
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Rethinking Vulkan queue choice."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2075769880092037309
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-11 02:31:20

## Thread

**1/**

Rethinking Vulkan queue choice. Traditional double-buffered games might do something like the code below. Find the queue that does {presentation,graphics,compute}. First off this seems like a lot of unnecessary work when one could just choose queue 0 and be done with it ...

Media (not lifted): `2075769880092037309_HM6desTW0AAHA_H_orig.png`

Branches: [[archive/threads/NOTimothyLottes/2026-07-11-rethinking-vulkan-queue-choice-traditional-double/2026-07-11-konrad_kubacki_-am-i-having-a-stroke-what-is-this-font-it-feels]]

**2/**

AMD on Linux (RADV) and Windows. Queue 0 just works. But note both platforms support doing present on queue 1. So on AMD I'm likely going to render via compute on queue 0 [to reduce chance of preemption] and present on queue 1. And have both decoupled (for front buffer rendering)

Media (not lifted): `2075770634349527454_HM6d5GnWAAAGOmg_orig.jpg` `2075770634349527454_HM6d8lcXsAA-8LJ_orig.jpg`

**3/**

NVIDIA is more complex. They put a DMA engine in queue 1 slot, and compute engine in queue 2 slot. Some sometimes queue 2 slot can or cannot do present (varies by driver). So maybe present on 0 (gfx queue), and dispatch on queue 2 by default for NV.

Media (not lifted): `2075771407510773906_HM6egsMWcAAkjOq_orig.jpg` `2075771407510773906_HM6ex2jXwAAkmI6_orig.jpg` `2075771407510773906_HM6e5EdXwAAuOG5_orig.jpg`
