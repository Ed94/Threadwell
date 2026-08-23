---
title: "Did manage to get ALSA to function without SNDRV_PCM_IOCTL_HW_REFINE and only with SNDRV_PCM_IOCTL_HW_PARAMS."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2072194202851549432"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2072194202851549432"
date: 2026-07-01
archived: 2026-08-23
status: draft
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Did manage to get ALSA to function without SNDRV_PCM_IOCTL_HW_REFINE and only with SNDRV_PCM_IOCTL_HW_PARAMS."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2072194202851549432
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-01 05:42:52

## Thread

**1/**

Did manage to get ALSA to function without SNDRV_PCM_IOCTL_HW_REFINE and only with SNDRV_PCM_IOCTL_HW_PARAMS. My structures are different but aliased (snd_interval.interger -> .flag=4). Apparently setting the core values is enough for the driver.

Media (not lifted): `2072194202851549432_HMHoiZAWcAAjn6j_orig.png`

**2/**

Don't actually have to set {.flags,.rmask,.info} on my machine. Absolutely do have to set ".max=~0" for the intervals not being hardcoded. I only do double buffered, 48000Hz stereo, and just vary the frames/period sizing.
