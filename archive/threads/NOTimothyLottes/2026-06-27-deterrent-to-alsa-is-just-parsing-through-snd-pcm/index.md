---
title: "Deterrent to ALSA is just parsing through snd_pcm_open() source."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2070734717825986566"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2070734717825986566"
date: 2026-06-27
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Deterrent to ALSA is just parsing through snd_pcm_open() source."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2070734717825986566
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-06-27 05:03:23

## Thread

**1/**

Deterrent to ALSA is just parsing through snd_pcm_open() source. It's death by boiler plate and complexity. Tinyalsa isn't much better. Likely easier to think about this from perspective of devices that can be open()ed from /dev/snd. On my machine doesn't seem to hot plug

![](https://pbs.twimg.com/media/HLy5-C9XMAAfs_w?format=png&name=orig)
**2/**

Assuming 'p'&'c' are PLAYBACK & CAPTURE, so opening different devices (instead of both in one device). Then just have user provide a device, or have the API war-dial open() constructing possible devices to probe what is available 'pcmC{c}D{d}{p|c}'. Easier than listing files.

![](https://pbs.twimg.com/media/HLy6SApX0AApPub?format=png&name=orig)