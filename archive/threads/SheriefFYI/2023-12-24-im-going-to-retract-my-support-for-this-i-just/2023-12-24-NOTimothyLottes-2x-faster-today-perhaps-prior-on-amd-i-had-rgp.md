---
title: "@SheriefFYI 2x faster today perhaps."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1738916459655336202"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1738916459655336202"
date: 2023-12-24
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SheriefFYI
description: "@SheriefFYI 2x faster today perhaps."
in_reply_to: ""
parent_post_id: "1738800602568638492"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1738916459655336202
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-12-24 13:36:06

## Branch

**1/** **@NOTimothyLottes** ^1738916459655336202

**@SheriefFYI**

2x faster today perhaps. Prior on AMD I had RGP captures of game with 3 separate DMAs. See 0.1ms of GFX idle for a semaphore signal, and 0.1 ms idle for semaphore wait (already signaled) -> 3=0.6 ms GFX idle time/frame. At 120Hz that's >7% of the frame lost, not acceptable IMO.

**2/** **@NOTimothyLottes** ^1738917893348159912

**@SheriefFYI**

... That was just for the transfers, the capture had a lot of dependent async-compute too, but at 200us idle/instance, all that had to be converted to non-async. Cutting waits from 100us to 50us {per signal or wait} wouldn't change the conclusion.

**3/** **@NOTimothyLottes** ^1738919198192017531

**@SheriefFYI**

If drivers had on-GPU syncs, then async would be useful for things like CS index culling into a ring-buffer feeding GFX. But you need fully pipelined syncs for that. Even if they got 50us to 1us, it's still perf death simply due to the idle during drain and fill.

## Related

- Spine: [[archive/threads/SheriefFYI/2023-12-24-im-going-to-retract-my-support-for-this-i-just]]
