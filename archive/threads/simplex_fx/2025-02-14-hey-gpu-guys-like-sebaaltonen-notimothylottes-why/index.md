---
title: "Hey, gpu guys like @SebAaltonen @NOTimothyLottes why do rendering guys usually wrap 3d apis at low level in engines, creating some generic mid-low level API?"
type: archive
source: twitter
source_url: "https://x.com/simplex_fx/status/1890348863287943363"
author: "Simplex"
handle: simplex_fx
post_id: "1890348863287943363"
date: 2025-02-14
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - simplex_fx
description: "Hey, gpu guys like @SebAaltonen @NOTimothyLottes why do rendering guys usually wrap 3d apis at low level in engines, creating some generic mid-low level API?"
in_reply_to: ""
---

## Source

- URL: https://x.com/simplex_fx/status/1890348863287943363
- Author: Simplex (@simplex_fx)
- Posted: 2025-02-14 10:34:24

## Thread

**1/** @simplex_fx

Hey, gpu guys like @SebAaltonen @NOTimothyLottes why do rendering guys usually wrap 3d apis at low level in engines, creating some generic mid-low level API?

My 3d engine have a few super high level functions for stuff I actually do, and the rest is totally up to platform/api specific code. 

Unless you go with some super generic game engine (bad idea on it's own anyway), 3d engine should be also just specific to the use case.

Branches: [[archive/threads/simplex_fx/2025-02-14-hey-gpu-guys-like-sebaaltonen-notimothylottes-why/2025-02-14-count_mascetti-every-time-i-abstract-at-a-higher-level-i-end-up]], [[archive/threads/simplex_fx/2025-02-14-hey-gpu-guys-like-sebaaltonen-notimothylottes-why/2025-02-14-SebAaltonen-i-briefly-discussed-this-topic-in-my-siggraph]], [[archive/threads/simplex_fx/2025-02-14-hey-gpu-guys-like-sebaaltonen-notimothylottes-why/2025-02-14-matiasgoldberg-you-can-do-whatever-you-want-the-api-just-because]], [[archive/threads/simplex_fx/2025-02-14-hey-gpu-guys-like-sebaaltonen-notimothylottes-why/2025-02-14-NOTimothyLottes-yeah-its-a-common-problem-thin-wrapper-interfaces]], [[archive/threads/simplex_fx/2025-02-14-hey-gpu-guys-like-sebaaltonen-notimothylottes-why/2025-02-15-RyDawgE256-i-dont-disagree-but-the-reason-is-that-99-of]], [[archive/threads/simplex_fx/2025-02-14-hey-gpu-guys-like-sebaaltonen-notimothylottes-why/2025-02-15-matthewcraig42-usually-the-key-benefit-is-two-fold-making-the]], [[archive/threads/simplex_fx/2025-02-14-hey-gpu-guys-like-sebaaltonen-notimothylottes-why/2025-02-15-pagedeux-the-render-pipeline-is-basically-a-full-piece-of]], [[archive/threads/simplex_fx/2025-02-14-hey-gpu-guys-like-sebaaltonen-notimothylottes-why/2025-02-15-vanderschnarzen-i-have-exactly-that-my-abstraction-is-basically]]

**2/** @songohab

@simplex_fx @SebAaltonen @NOTimothyLottes

Exactly the question I was asking myself lol. Always felt like 3D apis SHOULD be specific. But I’m just a noob
