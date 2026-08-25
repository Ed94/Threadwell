---
title: "@NOTimothyLottes so you're preallocating every type of descriptor to a max count and aliasing them with various qualifiers/attributes? all that in a single memory layout?"
type: archive
source: twitter
source_url: "https://x.com/VPCOMPRESSB/status/1953820468697317627"
author: "/i:'mɪər/"
handle: VPCOMPRESSB
post_id: "1953820468697317627"
date: 2025-08-08
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes so you're preallocating every type of descriptor to a max count and aliasing them with various qualifiers/attributes? all that in a single memory layout?"
in_reply_to: ""
parent_post_id: "1736154923408953499"
---

## Source

- URL: https://x.com/VPCOMPRESSB/status/1953820468697317627
- Author: /i:'mɪər/ (@VPCOMPRESSB)
- Posted: 2025-08-08 14:07:54

## Branch

**1/** @VPCOMPRESSB

@NOTimothyLottes

so you're preallocating every type of descriptor to a max count and aliasing them with various qualifiers/attributes? all that in a single memory layout?

if this is the case, the program identifier makes sense. you can just swap out the code, leaving the data untouched.

**2/** @NOTimothyLottes

@VPCOMPRESSB

I use the layout aliasing to choose things like {read-only K$ reads, vs read-write texture cache access} for buffers, for making sure GLC=1 (write through to coherent cache domain) is enabled for stores (image and buffer), as well as selecting the texel format for image access :)

**3/** @VPCOMPRESSB

i revisited last night.

e.g.

i heard that a single shader doesn't like using multiple images due to resource contention.

i assume your code is laid in stages. each stage corresponds to a specific image. barriers are emplaced between stages. essentially, in a single shader, you'd imitate multiple shaders that are pipelined.

aliasing supports this even further, with explicit intentions for resources.

**4/** @NOTimothyLottes

@VPCOMPRESSB

On modern desktop GPUs it is very efficient to have everything bound all the time (bind everything once/frame). On AMD on use the descriptor is loaded into SGPRs. You only pay for what is used. And ideally group descriptors used together near so they share same cache lines.

**5/** @NOTimothyLottes

@VPCOMPRESSB

Merging independent shaders is then easy. Merging dependent shaders is more complex. You can both do it an unsafe way or a safe way (too long for one tweet)...

**6/** @NOTimothyLottes

@VPCOMPRESSB

The unsafe way: launch a N+M sized 1D dispatch. Bank on having enough work in N such that when the dependent M starts that enough of N is finished in practice. This can work when early M depends on only early N workgroups.

**7/** @NOTimothyLottes

@VPCOMPRESSB

There are various safe ways. For instance  if the dependent work isn't done, one can conditionally duplicate the work. Or conditionally use a fallback. Or only use the pre task if it had finished to accelerate the second, for example hierarchical empty space skipping ...

**8/** @NOTimothyLottes

@VPCOMPRESSB

The challenge of course is that the  obvious stuff like spin waiting isn't safe because of bad API and driver design : no forward progress guarantee (on preemption, etc)

**9/** @NOTimothyLottes

@VPCOMPRESSB

Quite literally they just need to put in a guarantee that workgroups with lower coords in scan order are launched first and restored first in a partial preemption restore. Then you could safely spin on work in a prior numbered workgroup

## Related

- Spine: [[archive/threads/NOTimothyLottes/2023-12-16-inspecting-my-old-vk-engines]]
