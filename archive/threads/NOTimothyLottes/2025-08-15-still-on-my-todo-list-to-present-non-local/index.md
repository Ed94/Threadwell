---
title: "Still on my TODO list to present non-local mapping talk at some point."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1956164955742343330"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1956164955742343330"
date: 2025-08-15
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Still on my TODO list to present non-local mapping talk at some point."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1956164955742343330
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-08-15 01:24:03

## Thread

**1/** **@NOTimothyLottes** ^1956164955742343330

Still on my TODO list to present non-local mapping talk at some point. But in the meantime, an interesting take on tone-mapping from Polyphony Digital: https://blog.selfshadow.com/publications/s2025-shading-course/pdi/s2025_pbs_pdi_slides.pdf

**2/** **@NOTimothyLottes** ^1956165533860061349

The followup to the VDR talk that they referenced in their talk is here: https://gpuopen.com/download/gdc-2019-s5-blend-of-gcn-optimization-and-color-processing.pdf - Interesting similarities of problem space: how to shape color in the highlight compression region, how to manage maintaining stable color in the mid-tones ...

**3/** **@NOTimothyLottes** ^1956166150590468573

So I wonder how much of the desire for the linear mid-tone region is motivated by preservation of color during separate RGB channel tonemaps. I felt I didn't need a linear region because I separated luma and choma and preserved color ratio (regardless of luma remapping)

**4/** **@NOTimothyLottes** ^1956166742369034419

Think maybe the LPM source ended up with a not great solution for the highlight path, but the theory I still feel is sound. Polyphony found another interesting way to shape color on overexposure, which is nice to see

**5/** **@NOTimothyLottes** ^1956167243139551742

I really like the focus on dual adaption, and I personally would go to extents to have rod-dominate scene view with it's desaturation and grain. But I think I'd still skip UCS and keep in RGB as color I feel is still too locally dependent to use global remappers

**6/** **@NOTimothyLottes** ^1956167580567121976

Which is a great point to terminate on, that if I do another shader package for tonemapping and an associated talk (likely just on youtube) it will only be talking about going all in on local adaption, no more global stuff for me

**7/** **@NOTimothyLottes** ^1956169397116060053

And also in Polyphony's credits: Troy, you continue to be an inspiration: https://hg2dc.com best F*n reference to color :)
