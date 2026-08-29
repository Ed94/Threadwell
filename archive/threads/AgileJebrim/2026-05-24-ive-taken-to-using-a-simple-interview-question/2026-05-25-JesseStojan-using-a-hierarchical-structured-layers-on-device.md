---
title: "@AgileJebrim Using a hierarchical/structured layers on-device parallel reduction of cascading (multi-pass) kernels."
type: archive
source: twitter
source_url: "https://x.com/JesseStojan/status/2058768097939472658"
author: "Jesse S"
handle: JesseStojan
post_id: "2058768097939472658"
date: 2026-05-25
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim Using a hierarchical/structured layers on-device parallel reduction of cascading (multi-pass) kernels."
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/JesseStojan/status/2058768097939472658
- Author: Jesse S (@JesseStojan)
- Posted: 2026-05-25 04:32:19

## Branch

**1/** **@JesseStojan** ^2058768097939472658

**@AgileJebrim**

Using a hierarchical/structured layers on-device parallel reduction of cascading (multi-pass) kernels.
E.g. `hip/cub::DeviceReduce::Sum(...)`/`sycl::Reduction(...)` with more steps.
(I saw you say 16M × uint8 in the replies, but it was one of the first questions in my head lol)

**2/** **@AgileJebrim** ^2058769061480206761

**@JesseStojan**

Cool. Provide more details please.

**3/** **@AgileJebrim** ^2058769188873732484

**@JesseStojan**

You’re implementing the low level details, no reusing an existing function.

**4/** **@JesseStojan** ^2058785099756265546

**@AgileJebrim**

Well in that case, 1st kernel pass, each workgroup strides through the global array, sums the values, tree reduction in shared memory, writes the partial sum to a (uint32/64) partials[blockN] buffer. 2nd kernel pass reduces the partials[] down to the final sum.

**5/** **@AgileJebrim** ^2058788993848766932

**@JesseStojan**

Tell me more about this step labeled “sums the values”

**6/** **@JesseStojan** ^2058803240313979237

**@AgileJebrim**

Each thread sums many values using a stride (num_workgroups × threads_per_workgroup). Within each iteration, neighboring threads in a (subgroup/warp/wavefront) access consecutive addresses, enabling coalesced wide bursts (one transaction per subgroup).

**7/** **@AgileJebrim** ^2058922041076592962

**@JesseStojan**

Do you think you can write a short for loop snippet for this in a shader language?

**8/** **@JesseStojan** ^2058930323946152157

**@AgileJebrim**

Yeah, though just fair heads up, I'm not seeking employment lol, I'm just a nerd for rendering/CGI and massively parallel computing.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
