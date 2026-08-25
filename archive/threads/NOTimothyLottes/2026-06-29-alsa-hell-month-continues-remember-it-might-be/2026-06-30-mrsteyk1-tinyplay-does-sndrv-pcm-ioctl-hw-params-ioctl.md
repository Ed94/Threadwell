---
title: "@NOTimothyLottes tinyplay does SNDRV_PCM_IOCTL_HW_PARAMS ioctl (referenced in the article alongside REFINE)"
type: archive
source: twitter
source_url: "https://x.com/mrsteyk1/status/2071774178374812018"
author: "mrsteyk"
handle: mrsteyk1
post_id: "2071774178374812018"
date: 2026-06-30
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes tinyplay does SNDRV_PCM_IOCTL_HW_PARAMS ioctl (referenced in the article alongside REFINE)"
in_reply_to: ""
parent_post_id: "2071725181576319370"
---

## Source

- URL: https://x.com/mrsteyk1/status/2071774178374812018
- Author: mrsteyk (@mrsteyk1)
- Posted: 2026-06-30 01:53:50

## Branch

**1/**

@NOTimothyLottes tinyplay does SNDRV_PCM_IOCTL_HW_PARAMS ioctl (referenced in the article alongside REFINE)

![](https://pbs.twimg.com/media/HMBrjrxbkAAID_C?format=png&name=orig)

**2/**

@mrsteyk1 I believe the method the ALSA people wanted users to go by was to first REFINE to grab the full PCM limits, then iteratively make changes (via REFINE ioctl) until it converges to one configuration, at which point the HW_PARAMS ioctl is used to finalize that config.

**3/**

@mrsteyk1 Maybe it works sometimes to just use HW_PARAMs directly, but I have not got that working. I also cannot seem to get the refinement process to work either. And I don't get error returns, so still no idea what is wrong yet.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2026-06-29-alsa-hell-month-continues-remember-it-might-be]]
