---
title: "If the plan in the long term is to be off LLVM, you’ll need all that code anyway so that is fairly fixed."
type: archive
source: twitter
source_url: "https://x.com/joe_sweeney/status/1871663107753292020"
author: "Joe"
handle: joe_sweeney
post_id: "1871663107753292020"
date: 2024-12-24
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "If the plan in the long term is to be off LLVM, you’ll need all that code anyway so that is fairly fixed."
in_reply_to: ""
parent_post_id: "1871638900554317934"
---

## Source

- URL: https://x.com/joe_sweeney/status/1871663107753292020
- Author: Joe (@joe_sweeney)
- Posted: 2024-12-24 21:03:53

## Branch

**1/** **@joe_sweeney** ^1871663107753292020

If the plan in the long term is to be off LLVM, you’ll need all that code anyway so that is fairly fixed. My naive impression is that if you want a good cohesive experience you probably need to control that backend no material what, which sucks because that complexity sucks. But you probably wouldn’t want to use someone else’s code gen even it existed.

For SIMD, I don’t envy your position but my recent experience using ISPC (Intel’s SPMD language) that feels like the future approach for most people writing SIMD code. I also think that an SPMD system should live in userspace and just take in compile time directives and then output intrinsics to the compiler. So then you are just on the hook for providing the user with access to the different CPU instructions then leave the design choices to userland.

People know which platforms they need to target so just give them the lowest level access so it is possible. Then they can use your other language features to make the cross platform SIMD code that makes sense for them (which seems like what real power users will do even if you provide another abstraction over SIMD).

To me the compiler’s job would just be to output the best instructions possible, so I would think saving your complexity budget for your own optimizing backends.

You can take this all with a grain of salt, just some thoughts.

## Related

- Spine: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the]]
