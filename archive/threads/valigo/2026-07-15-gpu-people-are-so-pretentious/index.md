---
title: "GPU people are so pretentious."
type: archive
source: twitter
source_url: "https://x.com/valigo/status/2077379756270448823"
author: "Valentin Ignatev"
handle: valigo
post_id: "2077379756270448823"
date: 2026-07-15
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - valigo
description: "GPU people are so pretentious."
in_reply_to: ""
---

## Source

- URL: https://x.com/valigo/status/2077379756270448823
- Author: Valentin Ignatev (@valigo)
- Posted: 2026-07-15 13:08:24

## Thread

**1/** **@valigo** ^2077379756270448823

GPU people are so pretentious. They can't call their code just a program. It has to be something fancy, like shader, or, even worse, a kernel. So full of themselves!

**2/** **@NOTimothyLottes** ^2077382772650295346

**@valigo**

Some of us want to write programs for the GPU but IHVs don’t want to give access to externally compiled binaries in Vulkan.

**3/** **@valigo** ^2077383454170157205

**@NOTimothyLottes**

yeah... I guess you can get really close with foss amd drivers (not through vulkan though), but it's really fucked that gpus don't just give you an instruction set for purely market grab and politics reasons by OS vendors.

**4/** **@valigo** ^2077383834224488699

**@NOTimothyLottes**

Which is kinda funny, because CUDA is almost it, just a bit more high level

**5/** **@NOTimothyLottes** ^2077385030297399481

**@valigo**

Most advanced GPU programming for graphics/games is effectively held hostage beyond the brick wall of no 3rd party compiler access on Windows PC. But ISAs are mostly stable for many generations now, so it’s possible to target the variations. Just couldn’t hit future GPUs.

**6/** **@AgileJebrim** ^2077409130306760887

I think there just needs to be some reverse engineering done of the PSOs and to compile directly into them. None of this requires active involvement from the vendors. It’s just a bunch of grunt work for every target device and driver version for it, which might be fine in an environment with just a single target platform.
