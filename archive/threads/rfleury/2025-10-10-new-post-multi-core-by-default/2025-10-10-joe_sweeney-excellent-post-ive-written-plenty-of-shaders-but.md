---
title: "Excellent post, I've written plenty of shaders but never thought to write CPU code in the same way."
type: archive
source: twitter
source_url: "https://x.com/joe_sweeney/status/1976626608392863987"
author: "Joe"
handle: joe_sweeney
post_id: "1976626608392863987"
date: 2025-10-10
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "Excellent post, I've written plenty of shaders but never thought to write CPU code in the same way."
in_reply_to: ""
parent_post_id: "1976458516325073141"
---

## Source

- URL: https://x.com/joe_sweeney/status/1976626608392863987
- Author: Joe (@joe_sweeney)
- Posted: 2025-10-10 12:31:22

## Branch

**1/** **@joe_sweeney** ^1976626608392863987

Excellent post, I've written plenty of shaders but never thought to write CPU code in the same way.

Have you tried porting old code to this method and is it simple? Or is it best to just rewrite systems in this style from scratch, while allowing previous code to remain single threaded?

**2/** **@rfleury** ^1976628953352994908

Yes. I recently rewrote the PDB -> RDI converter in this style, which was originally using a job system (kicking off jobs, then waiting on them).

It requires a thorough pass over the code. Many codepaths will simply translate over, but in some cases, you will need to do a more careful rewrite of an algorithm to distribute work more uniformly (I mention the radix sort thing as one example).

So it really depends on what you’re starting with. If you’re starting with single threaded code, it’s actually really easy to get started, since you just put an if(LaneIdx() == 0) and begin pulling things out as you can.

## Related

- Spine: [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default]]
