---
title: "Notably this is *also* a problem in ray tracing: long and thin triangles end up degrading BVH quality which makes traversal more expensive."
type: archive
source: twitter
source_url: "https://x.com/zeuxcg/status/2072367220873982042"
author: "Arseny Kapoulkine 🇺🇦"
handle: zeuxcg
post_id: "2072367220873982042"
date: 2026-07-01
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - ID_AA_Carmack
description: "Notably this is *also* a problem in ray tracing: long and thin triangles end up degrading BVH quality which makes traversal more expensive."
in_reply_to: ""
parent_post_id: "2072320234619355572"
---

## Source

- URL: https://x.com/zeuxcg/status/2072367220873982042
- Author: Arseny Kapoulkine 🇺🇦 (@zeuxcg)
- Posted: 2026-07-01 17:10:22

## Branch

**1/** **@zeuxcg** ^2072367220873982042

Notably this is *also* a problem in ray tracing: long and thin triangles end up degrading BVH quality which makes traversal more expensive. Plus a thin triangle suffers even more under rotation, as the node bounds are (usually) axis aligned.

This is all offset to some degree with "split BVH" (a long triangle gets placed into multiple smaller BVH nodes) but not all drivers implement that and this doesn't fully recover the cost.

## Related

- Spine: [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at]]
