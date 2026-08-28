---
title: "M64, the physical FPGA+PSRAM hardware offers such an extremely challenging problem to solve for a neo-vintage retro machine design."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2083774527255740917"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2083774527255740917"
date: 2026-08-02
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "M64, the physical FPGA+PSRAM hardware offers such an extremely challenging problem to solve for a neo-vintage retro machine design."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2083774527255740917
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-08-02 04:38:56

## Thread

**1/** **@NOTimothyLottes** ^2083774527255740917

M64, the physical FPGA+PSRAM hardware offers such an extremely challenging problem to solve for a neo-vintage retro machine design. One has the capacity for an extreme amount of DSPs paired with relatively low on-chip memory and still limited off-chip bandwidth ...

**2/** **@NOTimothyLottes** ^2083774870630928444

M64/MiSTer and others burn up nearly everything on emulation, but we have yet to see what a bespoke engineering effort would look like if it was unleashed on those FGPAs

**3/** **@NOTimothyLottes** ^2083775826303021409

The obvious stuff, like on M64, you have >200x {36-bit x 512 entry} memories, and double that number in IMAD units (DSPs), doesn't really map well to vintage single CPU or even old simple multi-chip designs. Meaning a bespoke parallel machine could likely knock some socks off ...

**4/** **@NOTimothyLottes** ^2083777028449263884

Most of the 3D HW that sits firmly in the post 2D to 3D transition region that has low enough clocks to FPGA emulate, seems quite strangled. Meaning an evolved sprite super-scalar (perhaps depth sprites) might actually have been a better alternative timeline to go after ...

Branches: [[archive/threads/NOTimothyLottes/2026-08-02-m64-the-physical-fpga-psram-hardware-offers-such/2026-08-02-mbur82-wasnt-that-pretty-much-what-the-saturn-did]]

**5/** **@NOTimothyLottes** ^2083778960945562067

Most of the puzzle of targeting a machine with massive ALU capacity is a compression problem, how to have a small number of 'things' transform into a lot of 'stuff' without round-tripping through memory
