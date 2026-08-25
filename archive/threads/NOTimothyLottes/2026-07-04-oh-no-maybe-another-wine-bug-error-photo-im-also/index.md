---
title: "Oh no, maybe another Wine bug (error photo)? I'm also getting an \"AUDCLNT_E_DEVICE_IN_USE\" (0x8889000A) when http://x.com is open (which would imply pipewire owning the audio device)."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2073531564655260153"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2073531564655260153"
date: 2026-07-04
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Oh no, maybe another Wine bug (error photo)? I'm also getting an \"AUDCLNT_E_DEVICE_IN_USE\" (0x8889000A) when http://x.com is open (which would imply pipewire owning the audio device)."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2073531564655260153
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-04 22:17:04

## Thread

**1/**

Oh no, maybe another Wine bug (error photo)? I'm also getting an "AUDCLNT_E_DEVICE_IN_USE" (0x8889000A) when http://x.com is open (which would imply pipewire owning the audio device). So still holding out hope that Wine actually tried to emulate exclusive mode ...

![](https://pbs.twimg.com/media/HMapMOaXIAEqXQe?format=png&name=orig)

**2/**

... haha what a joke. Nope, actually at another Wine bug, when my other Linux digital twin can open the audio device with exclusive access, the wine'd version cannot. So I'm back to another actual WINE bug where they return AUDCLNT_E_DEVICE_IN_USE to avoid needing to implement

**3/**

Nothing smells more like the 4th of july, than rain and grepping wine source to track down wine bugs. Does look like they just didn't implement EXCLUSIVE mode. Because I'm passing "*duration == *period" ...

![](https://pbs.twimg.com/media/HMavfcGXUAAC7xf?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2026-07-04-oh-no-maybe-another-wine-bug-error-photo-im-also/2026-07-05-mrsteyk1-once-upon-a-time-wine-didnt-implement-a]]

**4/**

Wine's IAudioClient::GetDevicePeriod() returns 53333 for minimum (which is 256 samples at 48KHz - really crappy) and 100000 for default (which is 480 samples at 48Khz - even worse), neither which work with EXCLUSIVE mode. Man Wine sucks, nothing but constant show stopping bugs.
