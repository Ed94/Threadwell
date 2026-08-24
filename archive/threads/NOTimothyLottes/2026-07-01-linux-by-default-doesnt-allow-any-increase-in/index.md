---
title: "Linux by default doesn't allow any increase in scheduling priority."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2072135292115427728"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2072135292115427728"
date: 2026-07-01
archived: 2026-08-23
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Linux by default doesn't allow any increase in scheduling priority."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2072135292115427728
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-01 01:48:46

## Thread

**1/**

Linux by default doesn't allow any increase in scheduling priority. Users need to manually setup special user|group with elevated rights. Also system calls that try elevated scheduling don't clamp, instead they fail -EPREM if out of bounds. So all around a pain in the ass.

Media (not lifted): `2072135292115427728_HMGz-64W4AABeaH_orig.png`

**2/**

I'm a little lazy right now and don't feel like trying SteamOS big picture mode to see what the default ulimits are. Curious what they allow.

**3/**

Linux priority workarounds
(a.) Use getrlimit() to get {soft,hard} limits
(b.) Use setrlimit() to set 'soft=hard' limit
(c.) Then set priority or nice based on new soft limit

Media (not lifted): `2072147378480566273_HMG-UCRXIAEKbdj_orig.png` `2072147378480566273_HMG-zRxWwAAWtI4_orig.png`

**4/**

I don't do one-time global priority maximums, just in case someone sudo's higher priority hard limit dynamically it should pickup the new limit.

**5/**

Also while on setrlimit, I also bump up the RLIMIT_MEMLOCK to it's maximum just in case before the mlockall().

Media (not lifted): `2072149707107787035_HMHBGTPXwAA_axg_orig.png`
