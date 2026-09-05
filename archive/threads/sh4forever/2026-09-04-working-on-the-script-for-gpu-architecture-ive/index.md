---
title: "Working on the script for GPU architecture, I’ve realized it’s going to have to be multiple parts."
type: archive
source: twitter
source_url: "https://x.com/sh4forever/status/2095912093774172324"
author: "sh4"
handle: sh4forever
post_id: "2095912093774172324"
date: 2026-09-04
archived: 2026-09-05
draft: false
tags:
  - archive
  - twitter
  - sh4forever
description: "Working on the script for GPU architecture, I’ve realized it’s going to have to be multiple parts."
in_reply_to: ""
---

## Source

- URL: https://x.com/sh4forever/status/2095912093774172324
- Author: sh4 (@sh4forever)
- Posted: 2026-09-04 16:29:17

## Thread

**1/** **@sh4forever** ^2095912093774172324

Working on the script for GPU architecture, I’ve realized it’s going to have to be multiple parts. The first part is just going to be why do we actually need GPUs at all, why it’s entirely a numbers/throughput game, and some of the major decisions.

**2/** **@sh4forever** ^2095912096873762953

I am almost simultaneously working on a script for what this means on a very limited FPGA. There is a reason that TBR is so attractive on boards with such limited and high-contention DRAM. Anyway I think people will enjoy these.

**3/** **@NOTimothyLottes** ^2095925785194303899

**@sh4forever**

Looking forward to the series. Though TBDRs have such a painful perf cliff for high geo density. Often get stuck rethinking of ways to bin object bounds and do on chip object to geo expansion per tile, to avoid all geo round tripping through off chip memory.

**4/** **@sh4forever** ^2095988450277413173

**@NOTimothyLottes**

You might find this interesting, though a bunch of details are not explained here. Currently evaluating a TBR path where <2k tris can be transformed, binned, and rasterized full in SRAM/EBR. DRAM would be out of the datapath then for geometry after initial read. Still evaluating.

![](https://pbs.twimg.com/media/HRZve8EacAAXBoh?format=png&name=orig)

**5/** **@NOTimothyLottes** ^2096016120624947508

**@sh4forever**

If you plan on doing full hidden surface removal pre-shading, i'd be extremely tempted to have a fixed function alpha test using a vintage sprite-era tile map as the alpha test texture compression. Meaning alpha test gets resolved pre-shade, and at the depth test rate.

**6/** **@NOTimothyLottes** ^2096017798061306063

**@sh4forever**

Of course the next logical step would be to expand that to a full depth map, with max depth as cutout. Then do the expand the triangle to a quad, and you'd get 2.5D depth sprites, which have extremely high utility when one only has a few K of tris.
