---
title: "It's ARM based, so it's not like a GPU in the traditional sense, NVIDIA has made CPU/APUs AFAIK."
type: archive
source: twitter
source_url: "https://x.com/JesseStojan/status/2060540898149048338"
author: "Jesse S"
handle: JesseStojan
post_id: "2060540898149048338"
date: 2026-05-30
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "It's ARM based, so it's not like a GPU in the traditional sense, NVIDIA has made CPU/APUs AFAIK."
in_reply_to: ""
parent_post_id: "2060513369065754969"
---

## Source

- URL: https://x.com/JesseStojan/status/2060540898149048338
- Author: Jesse S (@JesseStojan)
- Posted: 2026-05-30 01:56:47

## Branch

**1/** **@JesseStojan** ^2060540898149048338

It's ARM based, so it's not like a GPU in the traditional sense, NVIDIA has made CPU/APUs AFAIK. So the difference is probably going to be unified memory like Apple and NVIDIA DGX, alongside others going that route. The gaming side and even the professional workstation side is nothing compared to their server side products.

**2/** **@AgileJebrim** ^2060543431538037055

**@JesseStojan**

We already develop for the Tegra-based Jetson, so that’s fine.

**3/** **@JesseStojan** ^2060559836023022012

**@AgileJebrim**

Nice, I've been focusing on CNC/CAE and simulation/analysis stuff, so it's a mix of CPU and whatever hardware is available, I'll utilize the iGPU to squeeze out every last drop of performance if I have to.

**4/** **@AgileJebrim** ^2060560952844485032

**@JesseStojan**

We’re really big on trying to eliminate offline steps entirely from the stack. Everything is real-time, including the dev tools. No static analysis.

**5/** **@AgileJebrim** ^2060561152082333950

**@JesseStojan**

Basically have a solidly proven compiler and interpreter such that everything else built on top of it just works.

**6/** **@JesseStojan** ^2060567168689836209

**@AgileJebrim**

No static analysis sounds pretty wild.  Though idk what you're working on aside from it being rendering related and you've been making your own programming language for it. I'm cool with both real-time and offline rendering though. Especially massive parallelism.

**7/** **@AgileJebrim** ^2060569318899773465

Well the compiler itself needs to be tested to death to ensure no varying performance instructions can be generated. But anything built on top will not, that’s the beauty that makes it stand apart from anything else on the market in SC.

We’re not just doing rendering. This can power a metaverse server, editor, or even a social media server like X, alongside a client for it. This can run the computer vision for autonomous vehicles and robotics.

Even the editor itself is being created on top of it and is a client-server application to allow for version control and real-time multi-user collaboration. We aren’t doing a text-based language, so traditional offline tools won’t work.

Quite literally rebuilding a new stack from the bottom up. Lots of work to do.

**8/** **@JesseStojan** ^2060571172887023876

**@AgileJebrim**

Niceee, yeah the SDK I've been working on has all the cross platform/architecture support for IPC, Rendering, Physics, etc.. the whole stack. Mostly freestanding C++ and Assembly. That'd be interesting to see what you're cooking up, I'd imagine a node based graph like Houdini?

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-30-i-dont-think-hardware-vendors-are-going-to]]
