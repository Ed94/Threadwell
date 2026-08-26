---
title: "Peanut gallery vs Parallelizing the Physics Solver"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1946452873656631650"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1946452873656631650"
date: 2025-07-19
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
  - physics
  - graph-coloring
  - pipelining
description: "Peanut gallery vs Parallelizing the Physics Solver"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1946452873656631650
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-07-19 06:11:43

## Thread

**1/** **@NOTimothyLottes** ^1946452873656631650

Peanut gallery vs Parallelizing the Physics Solver
(1.) Yeah always write your own low level primitives for CPU stuff. It's cool to see just how bad std+OS sync actually is visually in this presentation
(2.) Presentation never fully optimized! ...

![](https://pbs.twimg.com/media/GwMwA9dXYAAwYaO?format=jpg&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2025-07-19-peanut-gallery-vs-parallelizing-the-physics-solver/2025-07-19-bmcnett-i-remember-the-gpu-scheduler-ruining-the]]

**2/** **@NOTimothyLottes** ^1946453750085808492

The graph coloring splits into serialized batches of independent work, but this is the DX GPU way of doing stuff, ZERO pipelining (still huge idle gaps). Would be far better to split into pipelined (overlapped) batches ->
do(A)
do(B)
wait(A)
do(C)
wait(B)
do(D)
wait(C)
...

Branches: [[archive/threads/NOTimothyLottes/2025-07-19-peanut-gallery-vs-parallelizing-the-physics-solver/2025-07-19-jakubtomsu_-is-that-possible-when-you-have-a-linear]], [[archive/threads/NOTimothyLottes/2025-07-19-peanut-gallery-vs-parallelizing-the-physics-solver/2025-07-19-AgileJebrim-what-about-when-each-stage-depends-upon-the]], [[archive/threads/NOTimothyLottes/2025-07-19-peanut-gallery-vs-parallelizing-the-physics-solver/2025-07-19-ISzlachtycz-im-pretty-sure-you-cant-do-this-properly-for-the]]
