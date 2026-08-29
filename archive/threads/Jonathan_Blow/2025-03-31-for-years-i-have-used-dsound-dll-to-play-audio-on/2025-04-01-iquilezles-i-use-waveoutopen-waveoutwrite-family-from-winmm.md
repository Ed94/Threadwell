---
title: "I use waveOutOpen()/waveOutWrite() family, from winmm.dll."
type: archive
source: twitter
source_url: "https://x.com/iquilezles/status/1906981591802601841"
author: "inigo quilez"
handle: iquilezles
post_id: "1906981591802601841"
date: 2025-04-01
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "I use waveOutOpen()/waveOutWrite() family, from winmm.dll."
in_reply_to: ""
parent_post_id: "1906823282915262657"
---

## Source

- URL: https://x.com/iquilezles/status/1906981591802601841
- Author: inigo quilez (@iquilezles)
- Posted: 2025-04-01 08:06:56

## Branch

**1/** **@iquilezles** ^1906981591802601841

I use waveOutOpen()/waveOutWrite() family, from winmm.dll.

I often precompute all sounds, but you presumably are mixing on a circular buffer, so I imagine you can waveOutWrite() one or two buffer windows while you prep the next.

All this assuming they haven't killed winmm.dll.... ???

## Related

- Spine: [[archive/threads/Jonathan_Blow/2025-03-31-for-years-i-have-used-dsound-dll-to-play-audio-on]]
