---
title: "I don’t think hardware vendors are going to practically be able to ditch the CPU from system architectures any more than they’ll ditch the GPU, but I do think the GPU should become the master device driving decisions rather than just a slave accelerator for heterogeneous apps."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/2060513369065754969"
author: "Jebrim"
handle: AgileJebrim
post_id: "2060513369065754969"
date: 2026-05-30
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "I don’t think hardware vendors are going to practically be able to ditch the CPU from system architectures any more than they’ll ditch the GPU, but I do think the GPU should become the master device driving decisions rather than just a slave accelerator for heterogeneous apps."
in_reply_to: ""
---

## Source

- URL: https://x.com/AgileJebrim/status/2060513369065754969
- Author: Jebrim (@AgileJebrim)
- Posted: 2026-05-30 00:07:24

## Thread

**1/** **@AgileJebrim** ^2060513369065754969

I don’t think hardware vendors are going to practically be able to ditch the CPU from system architectures any more than they’ll ditch the GPU, but I do think the GPU should become the master device driving decisions rather than just a slave accelerator for heterogeneous apps.

We (Isochron) believe we have a method of doing something like that by creating a GPU-native RTOS. It however won’t boot directly into it (although that would be nice) as we still depend upon existing third party drivers for I/O, but the GPU RTOS would run in parallel alongside a CPU-based OS as a hard real-time coprocessor without interference from the CPU.

What’s key here is that all control logic is on the GPU itself and is what tells the CPU what to do, such as load data from disk or send packets out over the network.

Branches: [[archive/threads/AgileJebrim/2026-05-30-i-dont-think-hardware-vendors-are-going-to/2026-05-30-nate_the_sneak-why-you-guys-trying-to-rebuild-the-world-in-the]], [[archive/threads/AgileJebrim/2026-05-30-i-dont-think-hardware-vendors-are-going-to/2026-05-30-NOTimothyLottes-unfortunately-few-know-how-to-author-programs]], [[archive/threads/AgileJebrim/2026-05-30-i-dont-think-hardware-vendors-are-going-to/2026-05-30-JesseStojan-its-arm-based-so-its-not-like-a-gpu-in-the]], [[archive/threads/AgileJebrim/2026-05-30-i-dont-think-hardware-vendors-are-going-to/2026-05-30-loganb-seems-unrealistic-to-have-hard-real-time-in-a]], [[archive/threads/AgileJebrim/2026-05-30-i-dont-think-hardware-vendors-are-going-to/2026-05-30-olenbaranasalat-what-problem-are-you-solving-what-is-the-cpu]], [[archive/threads/AgileJebrim/2026-05-30-i-dont-think-hardware-vendors-are-going-to/2026-05-30-Sacb0y-i-dont-think-thats-a-good-idea-theres-some]], [[archive/threads/AgileJebrim/2026-05-30-i-dont-think-hardware-vendors-are-going-to/2026-05-31-xyzw_io-this-isochron-https-www-isochron-org-about]]
