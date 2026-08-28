---
title: "It isn’t the point of this project, but looking at the triangulations made me think about some GPU optimization esoterica."
type: archive
source: twitter
source_url: "https://x.com/ID_AA_Carmack/status/2072320234619355572"
author: "John Carmack"
handle: ID_AA_Carmack
post_id: "2072320234619355572"
date: 2026-07-01
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - ID_AA_Carmack
description: "It isn’t the point of this project, but looking at the triangulations made me think about some GPU optimization esoterica."
in_reply_to: ""
---

## Source

- URL: https://x.com/ID_AA_Carmack/status/2072320234619355572
- Author: John Carmack (@ID_AA_Carmack)
- Posted: 2026-07-01 14:03:40

## Thread

**1/** **@ID_AA_Carmack** ^2072320234619355572

It isn’t the point of this project, but looking at the triangulations made me think about some GPU optimization esoterica.

Everyone knows “triangle count” has an impact on performance. Graphics programmers also know that the ordering of the triangles can also make a significant difference, and integrate mesh optimization tools.

For the special case of planar figures like these, total triangle edge length can become the distinguishing performance characteristic. GPUs work with 2x2 blocks of pixels so they can generate derivatives for texture sampling and shaders. At triangle edges, they still usually have to do calculations for complete 2x2 blocks, regardless of whether 1,2,3, or 4 pixels in the block are actually needed. Long, skinny triangles can require over double the fragment shader invocations that area-maximizing triangles do.

Consider triangulating a circle: the obvious way is to make a single triangle fan, but you can reduce the total edge length by inscribing a polygon inside the circle and only fanning out from that to the circle. Slightly more vertex work, but less fragment work.

There probably isn’t any real world case where this would be a crucial optimization, but having an “optimization worldview” means always noticing the tradeoffs.

Branches: [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-marcospereeira-dont-you-think-gpus-are-going-to-be-running-the]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-sallubroz-love-this-way-of-thinking-performance-often-comes]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-NiclasJ-john-have-you-thought-about-to-apply-game-engine]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-0xV0LYX-underrated-part-of-gpu-optimization-triangle]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-samiannoesis-could-this-graphic-triangle-building-in-gpus-has]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-samiannoesis-inscribing-the-polygon-first-reduces-fragment]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-i_mika_el-yeah-triangle-count-gets-all-the-attention-did]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-sleep_deprivado-its-just-how-big-is-the-cell-list-for-the-mesh]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-EasyAi_Tools-thats-a-fascinating-edge-case-on-edge-lengths-i]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-KURAOpenclaw-triangle-count-still-matters-more-than-most]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-ElonBaldMusk-i-dont-have-fable-yet-for-me-to-understand-this]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-mourner-feels-unreal-to-see-my-library-get-retweeted-by]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-optozorax-also-these-triangles-are-terrible-for-fem-its]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-ParkerRedford-or-or-or-calculate-r-2-x-2-y-2-z-2-for-infinite]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-HeroicReplicas-apply-this-granular-factual-analytical-excellent]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-HostOfMeta-would-depend-on-the-hardware-target-too-no-say]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-MaxGraey-btw-for-a-large-number-of-small-triangles-1-3]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-zeuxcg-notably-this-is-also-a-problem-in-ray-tracing]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-IHateZuckSoMuch-i-saw-some-video-about-those-pixel-quads-being-a]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-nam_dau_tu-c-ch-s-p-x-p-tam-gi-c-ph-ng-n-y-l-m-m-nh-nh-l-i-l]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-lep1c2l0-earcut-does-have-an-optional-triangle-area]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-MycelialClay-post-bug-fix-version-the-original-poster-put-up]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-AwokeKnowing-tldr-carmack-says-to-convex-hull-your-letters-and]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-evidype-for-ui-work-this-lesson-never-dies-total-work]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-RedaOuVT-there-probably-isnt-any-real-world-case-where]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-galateacyc-triangulation-algorithms-are-ridiculously-finicky]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-01-fedyac-this-is-a-topic-covered-by-an-old-blog-post-from]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-02-marcocc-triangle-ordering-matters-more-than-most-realize]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-02-gaborvalasek-the-problem-with-mwt-total-edge-length-minimizing]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-03-swengsbelike-but-theyre-cutting-out-circles-inside-circles]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-03-1louder-fyi-im-stealing-this-having-an-optimization]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-04-MakeTechPtyLtd-hey-john-what-happened-to-your-local-ai-rack-did]], [[archive/threads/ID_AA_Carmack/2026-07-01-it-isnt-the-point-of-this-project-but-looking-at/2026-07-06-AIwithFuture-this-is-the-part-of-the-ai-story-that-gets]]
