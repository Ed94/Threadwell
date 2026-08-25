---
title: "@NOTimothyLottes My take is similar, but I also feel that a lot of processing is best done predictively in parallel across multiple future frames, one SIMD lane per future frame"
type: archive
source: twitter
source_url: "https://x.com/bmcnett/status/1883581286838919440"
author: "bmcnett"
handle: bmcnett
post_id: "1883581286838919440"
date: 2025-01-26
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes My take is similar, but I also feel that a lot of processing is best done predictively in parallel across multiple future frames, one SIMD lane per future frame"
in_reply_to: ""
parent_post_id: "1883580512171942335"
---

## Source

- URL: https://x.com/bmcnett/status/1883581286838919440
- Author: bmcnett (@bmcnett)
- Posted: 2025-01-26 18:22:28

## Branch

**1/** **@bmcnett** ^1883581286838919440

**@NOTimothyLottes**

My take is similar, but I also feel that a lot of processing is best done predictively in parallel across multiple future frames, one SIMD lane per future frame

**2/** **@NOTimothyLottes** ^1883584542851977240

**@bmcnett**

Don't necessarily want to store all predictions raw though. One of the advantages of say simple things like baked directional lightmaps is that one keeps the data for multiple "frames" (or views) in a compressed form until just right before usage, and it's mis-predict safe

**3/** **@bmcnett** ^1883585257292825064

**@NOTimothyLottes**

Yeah, you need to store many prediction outputs in compressed form, with the time dimension being one over which you compress, in addition to whatever spatial dimensions are relevant

Limited hw support for that, sadly

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-01-26-often-overlooked-aspect-of-gpu-perf-scaling]]
