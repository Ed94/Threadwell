---
title: "Eventually figure out enough to get aplay to actually play a wave file, had to find an explicitly stereo wav else it would refuse to just duplicate the mono channels."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2071415096304193820"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2071415096304193820"
date: 2026-06-29
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Eventually figure out enough to get aplay to actually play a wave file, had to find an explicitly stereo wav else it would refuse to just duplicate the mono channels."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2071415096304193820
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-06-29 02:06:58

## Thread

**1/** **@NOTimothyLottes** ^2071415096304193820

Eventually figure out enough to get aplay to actually play a wave file, had to find an explicitly stereo wav else it would refuse to just duplicate the mono channels. Basically the a'tools unfriendlyness mirrors that of ALSA. Still cannot understand 'boundary' ...

![](https://pbs.twimg.com/media/HL8km6eWsAEq6xb?format=png&name=orig)

**2/** **@NOTimothyLottes** ^2071445744389611593

No luck getting ALSA to play anything from my app. State is always 2 SNDRV_PCM_STATE_PREPARED, haven't been able to get it to run. If I try the start ioctl, then it errors with -EPIPE.
