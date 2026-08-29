---
title: "@AgileJebrim I have no meaningful GPU coding experience."
type: archive
source: twitter
source_url: "https://x.com/SpikyCaterpillr/status/2058630363509907942"
author: "Spikier Caterpillar"
handle: SpikyCaterpillr
post_id: "2058630363509907942"
date: 2026-05-24
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim I have no meaningful GPU coding experience."
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/SpikyCaterpillr/status/2058630363509907942
- Author: Spikier Caterpillar (@SpikyCaterpillr)
- Posted: 2026-05-24 19:25:00

## Branch

**1/** **@SpikyCaterpillr** ^2058630363509907942

**@AgileJebrim**

I have no meaningful GPU coding experience. That said, if it's a LARGE array in GPU memory, the obvious guess would be "tell several compute units to sum chunks of it in parallel, then add the outputs together". The optimum chunk size will vary by GPU and possibly other factors.

**2/** **@AgileJebrim** ^2058630786803229053

**@SpikyCaterpillr**

"tell several compute units to sum chunks of it in parallel, then add the outputs together"

Any idea how you’d structure it? How would you do this on multicore CPUs using SIMD?

**3/** **@SpikyCaterpillr** ^2058640615412224473

**@AgileJebrim**

First determine the desired chunk size (I assume compute units have limited addressable space, for one), then iterate over the large array calling starting a summer on each chunk. When I run out of cores or GPU memory, wait and sum what I've got before continuing down the array.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
