---
title: "@NOTimothyLottes Im pretty sure you cant do this properly for the physics workload, because it would mess with the convergence of the optimizer."
type: archive
source: twitter
source_url: "https://x.com/ISzlachtycz/status/1946605956785184781"
author: "Ihor_Szlachtycz 🇺🇦"
handle: ISzlachtycz
post_id: "1946605956785184781"
date: 2025-07-19
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Im pretty sure you cant do this properly for the physics workload, because it would mess with the convergence of the optimizer."
in_reply_to: ""
parent_post_id: "1946453750085808492"
---

## Source

- URL: https://x.com/ISzlachtycz/status/1946605956785184781
- Author: Ihor_Szlachtycz 🇺🇦 (@ISzlachtycz)
- Posted: 2025-07-19 16:20:00

## Branch

**1/** **@ISzlachtycz** ^1946605956785184781

**@NOTimothyLottes**

Im pretty sure you cant do this properly for the physics workload, because it would mess with the convergence of the optimizer. Processing color b would mess with the processing of color a, and add randomness to the order of resolving constraints.

**2/** **@NOTimothyLottes** ^1946609109375041541

**@ISzlachtycz**

So much lost in translation. The methods I'm suggesting don't change the answer, they change the ordering of execution of independent pairs while keeping dependent ordering the same.

**3/** **@NOTimothyLottes** ^1946609910432600507

**@ISzlachtycz**

Another extreme example, if you color first and take a sufficiently random sampling of pairs, you can hierarchy resolve the earlier color dependencies until the object you need to process is in the right update state too ...

**4/** **@NOTimothyLottes** ^1946610706909950118

**@ISzlachtycz**

Doing things this way requires versioning by color though (memory) and can sometimes involve some work duplication. But it allows a sufficiently large complex problem to get pipelined parallelization.

**5/** **@NOTimothyLottes** ^1946611382708834700

**@ISzlachtycz**

This family of ideas is how I did my hierarchical cone stepped ray macher in my GTC demo about a decade back. The core ideas involve moving a hierarchical dependent workload into a single dispatch without any barriers.

**6/** **@NOTimothyLottes** ^1946612166791946530

**@ISzlachtycz**

You guarantee correctness by risking some amount of work duplication if the dependency isn't satisfied by the time the answer is needed. But in practice it is possible to make it so that duplication is rare and massive optimization is guaranteed.

**7/** **@NOTimothyLottes** ^1946612579087839232

**@ISzlachtycz**

It also naturally adapts to highly irregular behavior and changing machine size, etc. while being robust to cores getting preempted (self healing, whatever is running is guaranteed to continue forward progress)

**8/** **@ISzlachtycz** ^1946613205779837126

**@NOTimothyLottes**

So if you have colors a and b, you process color a and b in parallel, but when you run into a situation where some constraint from color b needs results from color a to be completed, you just have it process those dependencies right there?

**9/** **@ISzlachtycz** ^1946613231071478069

**@NOTimothyLottes**

Then when color a processing gets to those nodes, you recompute them and restore them?

**10/** **@NOTimothyLottes** ^1946618143498973205

**@ISzlachtycz**

If version of the object at a specific finished prior colors isn't available, you just recursively build those dependencies so you can finish the job. But you save the versioned objects so others won't have to recompute in practice ...

**11/** **@ISzlachtycz** ^1946618734728065201

**@NOTimothyLottes**

Yeah makes sense. I guess you gotta keep some metadata around to know whether the object is computed or not, but i get the idea. Maybe sometimes it can be implicitly figured out. Thanks for the explanation :)

**12/** **@ISzlachtycz** ^1946618995697754615

**@NOTimothyLottes**

I guess you do run the risk of the island approach though, where the dependency chain can grow to be quite large. But i havent worked in large physics sims, so not sure how it would work in practice

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-07-19-peanut-gallery-vs-parallelizing-the-physics-solver]]
