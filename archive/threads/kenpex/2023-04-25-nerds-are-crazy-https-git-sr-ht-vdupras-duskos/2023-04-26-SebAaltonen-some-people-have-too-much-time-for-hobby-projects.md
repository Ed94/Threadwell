---
title: "@kenpex Some people have too much time for hobby projects."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1651168030557077504"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1651168030557077504"
date: 2023-04-26
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - kenpex
description: "@kenpex Some people have too much time for hobby projects."
in_reply_to: ""
parent_post_id: "1650678968255913985"
---

## Source

- URL: https://x.com/SebAaltonen/status/1651168030557077504
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2023-04-26 10:15:10

## Branch

**1/**

@kenpex Some people have too much time for hobby projects.

**2/**

@SebAaltonen @kenpex Where else can someone learn Forth nowadays?

Would place Forth knowledge above C++ in an interview, shows an understanding of a live coded programmable compiler bootstrapped from assembly.

These are the people you want to help break tradition. They see the schlep, if you will.

**3/**

@Lambda_Coder @SebAaltonen I wouldn't. Forth today is hyper-niche, and even the programming model it teaches you about is. Lastly, the best way to learn forth is probably to make your own forth.

**4/**

@kenpex @SebAaltonen What of the distinction between Forth the syntactic language and the semantic programming model?

The way I see modern software, an insane amount of tooling and scaffolding is maintained to achieve what Forth and Lisp had emerging from their architecture. And usually not reusable

**5/**

@kenpex @SebAaltonen The fact that the model is obscure should turn it into a superpower.

I'd agree for an existing company it would be a risk, but for a startup its how you end up running circles around the competition.

Not forth/lisp themselves, but adapting their models with modern hindsights.

**6/**

@Lambda_Coder @SebAaltonen I doubt it. I doubt that languages or paradigms make any difference in practice (never saw any study showing significant advantages). And the lisp paradigm is in my opinion, niche for reasonable reasons. In general, the lack of strong semantics is a liability, not a strength.

**7/**

@kenpex @SebAaltonen What if there existed a way to get the live coding, programmable programming of Lisp/Forth, scale it to support AAA game engines, and keep most modern PLT developments in the process?

I agree languages and paradigms are compile-time concerns and as such make the runtime complex.

**8/**

@kenpex @SebAaltonen Its no different than a game engine moving from one scene to the next; a few layers of abstraction deeper.

Level designers would go insane having to reboot the editor between each change, yet when it comes to code it seems a perfectly normal thing to do.

I want this to change.

**9/**

@kenpex @SebAaltonen I also appreciate how weird and niche this position is.

It's one of these situations where the thing is already executing in my mind, but translating this to software and everyday terms is another story.

**10/**

@Lambda_Coder @SebAaltonen Live-coding is indeed (and provably so, there is science) a superpower, but does not have much to do with language semantics. It's tooling and "tradition". Lisps are usually VM-based, REPLs etc, but you can do that with C or whatever, and similarly, you can "offline" compile lisp

**11/**

@kenpex @SebAaltonen I would say it's deeply connected to language design, in that doing it elsewhere is more complex and yields less power.
Lisp has the most powerful REPL for this reason, but then it needs more semantic info to use it safely in a stateful simulation. Needs Erlang's supervision too.

**12/**

@kenpex @SebAaltonen The runtime architecture I'm interested in keeps track of its systems, generates the wires between them, handles snapshots and replay logging from non-deterministic inputs, supervises and restores crashed systems and is aware of frame boundaries to know when live coding is safe.

**13/**

@kenpex @SebAaltonen Too often in Lisp I crash something at the REPL, or lose track of a connected socket, or whatever else happening which causes me to reboot the entire runtime tower, and I see every second waiting to get back to the previous state as wasted time where the mental context fades away

## Related

- Spine: [[archive/threads/kenpex/2023-04-25-nerds-are-crazy-https-git-sr-ht-vdupras-duskos]]
