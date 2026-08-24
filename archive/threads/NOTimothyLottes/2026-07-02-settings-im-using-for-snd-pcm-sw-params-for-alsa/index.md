---
title: "Settings I'm using for snd_pcm_sw_params for ALSA, don't have docs for all of this, seems to work."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2072506103401754653"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2072506103401754653"
date: 2026-07-02
archived: 2026-08-23
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Settings I'm using for snd_pcm_sw_params for ALSA, don't have docs for all of this, seems to work."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2072506103401754653
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-02 02:22:15

## Thread

**1/**

Settings I'm using for snd_pcm_sw_params for ALSA, don't have docs for all of this, seems to work. I'm doing 64 frame period size on a double buffer right now without any thread priority, and not getting xruns, so not yet sure of bad behavior

![](https://pbs.twimg.com/media/HMMFAHiX0AAzY_R?format=png&name=orig)
**2/**

I put in a forced thread sleep between writes to force a xrun, and SNDRV_PCM_IOCTL_WRITEI_FRAMES kernel call then returns -32, in which case I run a SNDRV_PCM_IOCTL_PREPARE and then just get back to the write loop, seems to restore normal playback just fine.

**3/**

I reduced asound.h to this basically, the most minimal thing I found I needed. Now I also rename a few things (like structure names), and my IOCTL macros are slightly different in composition than standard.

![](https://pbs.twimg.com/media/HMMJjYPWAAAY1IE?format=png&name=orig)
**4/**

After getting this far, it actually looks quite easy, but the route to this was filled with garbage sifting because I couldn't easily find someone else who did this kind of minimalization. I'm only supporting 48KHz stereo 16-bit signed, with double buffering = keep it simple.
