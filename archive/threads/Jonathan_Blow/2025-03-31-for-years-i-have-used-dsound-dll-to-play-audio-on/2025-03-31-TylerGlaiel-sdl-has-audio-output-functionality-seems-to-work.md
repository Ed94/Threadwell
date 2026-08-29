---
title: "@Jonathan_Blow SDL has audio output functionality, seems to work pretty well from what I can tell."
type: archive
source: twitter
source_url: "https://x.com/TylerGlaiel/status/1906824305217835350"
author: "Tyler Glaiel"
handle: TylerGlaiel
post_id: "1906824305217835350"
date: 2025-03-31
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "@Jonathan_Blow SDL has audio output functionality, seems to work pretty well from what I can tell."
in_reply_to: ""
parent_post_id: "1906823282915262657"
---

## Source

- URL: https://x.com/TylerGlaiel/status/1906824305217835350
- Author: Tyler Glaiel (@TylerGlaiel)
- Posted: 2025-03-31 21:41:56

## Branch

**1/** **@TylerGlaiel** ^1906824305217835350

**@Jonathan_Blow**

SDL has audio output functionality, seems to work pretty well from what I can tell. I use FAudio on top of it (open source reimplementation of XAudio)

**2/** **@Jonathan_Blow** ^1906824662400831937

**@TylerGlaiel**

No Extra Layers Please

**3/** **@axnjaxn** ^1906906393782751361

**@Jonathan_Blow** **@TylerGlaiel**

I wondered if it would be possible to harvest whatever SDL3 uses underneath its extra layer, and within the header it calls out WASAPI, coreaudio, and ALSA, so perhaps they decided to build on top of the trash?

**4/** **@TylerGlaiel** ^1906907341033025796

**@axnjaxn** **@Jonathan_Blow**

SDL3 has a priority list of like 20 different underlying driver APIs since i guess windows is a bit fucked there. but it is fully open source

## Related

- Spine: [[archive/threads/Jonathan_Blow/2025-03-31-for-years-i-have-used-dsound-dll-to-play-audio-on]]
