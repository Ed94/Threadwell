---
title: "@NOTimothyLottes Did this still synchronize all threads before starting the child kernel or could some workgroups begin before others caught up and started their own children? And vice-versa for returning back to the parent."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/2121255478319604151"
author: "Jebrim"
handle: AgileJebrim
post_id: "2121255478319604151"
date: 2026-11-13
archived: 2026-11-13
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Did this still synchronize all threads before starting the child kernel or could some workgroups begin before others caught up and started their own children? And vice-versa for returning back to the parent."
in_reply_to: ""
parent_post_id: "2121253265018949886"
---

## Source

- URL: https://x.com/AgileJebrim/status/2121255478319604151
- Author: Jebrim (@AgileJebrim)
- Posted: 2026-11-13 14:54:51

## Branch

**1/** **@AgileJebrim** ^2121255478319604151

**@NOTimothyLottes**

Did this still synchronize all threads before starting the child kernel or could some workgroups begin before others caught up and started their own children? And vice-versa for returning back to the parent.

**2/** **@NOTimothyLottes** ^2121269655331352625

**@AgileJebrim**

You can just read the CDP docs they go into detail. I think they have an old CDP and a new CDP2 at this point, but the new stuff is off my radar completely as I just use persistent threads for my own stuff.

**3/** **@AgileJebrim** ^2121312823133213071

**@NOTimothyLottes**

I meant your non-atomic approach. The contract would thus be different if global sync guarantees were no longer required. I know how much you like pipelining.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2026-11-13-thankfully-a-friend-sent-this-to-me-otherwise-id]]
