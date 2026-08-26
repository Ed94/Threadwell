---
title: "@NOTimothyLottes I'm not going to pretend I understand a lick of this, which is why I have a humble request, well 2 actually:"
type: archive
source: twitter
source_url: "https://x.com/RouaniJihad/status/1870960478572499239"
author: "🕹️G🅰MESTUFFS🎮"
handle: RouaniJihad
post_id: "1870960478572499239"
date: 2024-12-22
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes I'm not going to pretend I understand a lick of this, which is why I have a humble request, well 2 actually:"
in_reply_to: ""
parent_post_id: "1870942850684420564"
---

## Source

- URL: https://x.com/RouaniJihad/status/1870960478572499239
- Author: 🕹️G🅰MESTUFFS🎮 (@RouaniJihad)
- Posted: 2024-12-22 22:31:53

## Branch

**1/** **@RouaniJihad** ^1870960478572499239

**@NOTimothyLottes**

I'm not going to pretend I understand a lick of this, which is why I have a humble request, well 2 actually:
1- Is there a way for you to finish working on STP.
2- Can you create an open source denoiser for say, a real-time Path Tracer 👉👈
Reading this is enough as well... =]

**2/** **@NOTimothyLottes** ^1871178158155714646

**@RouaniJihad**

My recommendation: ask Unity to open source STP under a MIT license so any external person could finish it. And then both Unity and anyone else could benefit from it's long term evolution.

**3/** **@NOTimothyLottes** ^1871178888543687059

**@RouaniJihad**

One fundamental problem with bespoke high-tech solutions like these are that in many cases they become abandonware when all the original people involved in the projects no longer work at the company (which is the case here)

**4/** **@NOTimothyLottes** ^1871180562016387273

**@RouaniJihad**

There are very few people who could work on it, and after Unity shed it's high tech rendering staff during it's downsizing efforts to stay live during it's stock crash, who knows when they will have an environment that fosters that kind of R&D again

**5/** **@NOTimothyLottes** ^1871182399876559216

**@RouaniJihad**

As for STP it wasn't ever designed to denoise per say, it does get a little denoising as a side effect of temporal filtering though, but things like stochastic GI on disocclusions will show a mismatch in noise with other parts of the image that get good temporal feedback

**6/** **@NOTimothyLottes** ^1871183683459145777

**@RouaniJihad**

The cases where people have merged scaling TAAs and denoisers, they do so by augmenting the TAA with extra side channel information from the G-buffer {normals, albedo, etc} and then keep a lot more recurrent data in feedback across frames, this massively increases costs

**7/** **@NOTimothyLottes** ^1871184146795491786

**@RouaniJihad**

Traditionally those who have managed to improve temporal feedback in cases of {rendered mirror reflections, SSR, or even RT} have needed to generate a section reprojection vector of where the mirrored reflection was in the prior frame, this is something Unity doesn't have today

**8/** **@NOTimothyLottes** ^1871184992803672572

**@RouaniJihad**

There is another interesting option that a scaling-TAA typically tracks the amount of screen convergence, and one could pass that information back into an input denoiser before the TAA that denoises less where things have converged and a lot where things would be disoccluded

**9/** **@NOTimothyLottes** ^1871190322346377591

**@RouaniJihad**

Can watch videos like this https://www.youtube.com/watch?v=K3ZHzJ_bhaI ... and you start to see that no one has actually come to a great solution for screen-space denoise+scaling+TAA, even given the ML solutions ...

**10/** **@NOTimothyLottes** ^1871191321974817274

**@RouaniJihad**

Suggests maybe it would ultimately be better to push the RT usage back into the environment probe space and do the spatial temporal denoise there, and then use those probes to light the scene instead.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2024-12-22-fixing-atomicadd-benchmarking-amd-nv]]
