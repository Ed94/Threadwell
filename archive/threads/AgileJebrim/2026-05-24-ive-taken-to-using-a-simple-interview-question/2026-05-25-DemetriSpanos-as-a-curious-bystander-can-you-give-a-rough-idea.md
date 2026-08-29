---
title: "@AgileJebrim As a curious bystander: can you give a rough idea how suboptimal it is to do \"the naive thing\"?"
type: archive
source: twitter
source_url: "https://x.com/DemetriSpanos/status/2058774747068891207"
author: "Demetri Spanos"
handle: DemetriSpanos
post_id: "2058774747068891207"
date: 2026-05-25
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim As a curious bystander: can you give a rough idea how suboptimal it is to do \"the naive thing\"?"
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/DemetriSpanos/status/2058774747068891207
- Author: Demetri Spanos (@DemetriSpanos)
- Posted: 2026-05-25 04:58:44

## Branch

**1/** **@DemetriSpanos** ^2058774747068891207

**@AgileJebrim**

As a curious bystander: can you give a rough idea how suboptimal it is to do "the naive thing"?

I mean one launch independently accumulating a vec4 per lane (Nx4M matrix yields 1xM array of vec4) and then a second launch to accumulate the 1xM in one lane?

2x suboptimal? worse?

**2/** **@AgileJebrim** ^2058776867981648367

Accumulating a partial sum in a vec4 per lane is a great approach. I think you’re the first one here to suggest it that didn’t attempt to prematurely reduce the vec4 every iteration.

There’s a significantly faster, albeit more involved way to reduce all of those parallel results than running a single lane in a second pass though. If you have 2000+ lanes across the hardware and 4 per lane, you’re looking at a serial accumulation in a single lane taking 8000+ steps on a half clock rate processor. You could do that in a small handful (~less than a dozen off the top of my head) instead.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
