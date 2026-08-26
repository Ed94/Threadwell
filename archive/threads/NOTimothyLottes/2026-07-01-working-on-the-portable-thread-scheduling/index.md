---
title: "Working on the portable thread scheduling priority interface."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2072134509089144888"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2072134509089144888"
date: 2026-07-01
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Working on the portable thread scheduling priority interface."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2072134509089144888
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-01 01:45:40

## Thread

**1/** **@NOTimothyLottes** ^2072134509089144888

Working on the portable thread scheduling priority interface. Windows is a bit nicer by default, one can increase the scheduling priority without admin and there is a AvSetMmThreadCharacteristics() / AvSetMmThreadPriority() hack for "Pro Audio" scheduling needs.

**2/** **@NOTimothyLottes** ^2072135292115427728

Linux by default doesn't allow any increase in scheduling priority. Users need to manually setup special user|group with elevated rights. Also system calls that try elevated scheduling don't clamp, instead they fail -EPREM if out of bounds. So all around a pain in the ass.

![](https://pbs.twimg.com/media/HMGz-64W4AABeaH?format=png&name=orig)

**3/** **@NOTimothyLottes** ^2072136089070961073

I'm a little lazy right now and don't feel like trying SteamOS big picture mode to see what the default ulimits are. Curious what they allow.

**4/** **@NOTimothyLottes** ^2072147378480566273

Linux priority workarounds
(a.) Use getrlimit() to get {soft,hard} limits
(b.) Use setrlimit() to set 'soft=hard' limit
(c.) Then set priority or nice based on new soft limit

![](https://pbs.twimg.com/media/HMG-UCRXIAEKbdj?format=png&name=orig)
![](https://pbs.twimg.com/media/HMG-zRxWwAAWtI4?format=png&name=orig)

**5/** **@NOTimothyLottes** ^2072147765157638479

I don't do one-time global priority maximums, just in case someone sudo's higher priority hard limit dynamically it should pickup the new limit.

**6/** **@NOTimothyLottes** ^2072149707107787035

Also while on setrlimit, I also bump up the RLIMIT_MEMLOCK to it's maximum just in case before the mlockall().

![](https://pbs.twimg.com/media/HMHBGTPXwAA_axg?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2026-07-01-working-on-the-portable-thread-scheduling/2026-07-01-mrsteyk1-on-my-install-the-limit-is-8m-even-vkcubes-usage]]
