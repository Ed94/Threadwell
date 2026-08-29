---
title: "A strange notion that assumes that text is the only way to program computers."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/2027461617210827256"
author: "Jebrim"
handle: AgileJebrim
post_id: "2027461617210827256"
date: 2026-02-27
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "A strange notion that assumes that text is the only way to program computers."
in_reply_to: ""
---

## Source

- URL: https://x.com/AgileJebrim/status/2027461617210827256
- Author: Jebrim (@AgileJebrim)
- Posted: 2026-02-27 19:11:32

## Thread

**1/** **@AgileJebrim** ^2027461617210827256

A strange notion that assumes that text is the only way to program computers.

Surely we can do better to provide an alternative as graphics programmers that doesn’t rely on string parsing, a fairly fragile, error-prone, and expensive way of representing user intent to a machine.

![](https://pbs.twimg.com/media/HCL9mK9WQAA4qJJ?format=jpg&name=orig)

**2/** **@NyxXeres** ^2027531357245591796

**@AgileJebrim**

If it was anyone else I might agree, but Ryan specifically did work on alternatives to text based programming.

**3/** **@AgileJebrim** ^2027542254055776549

**@NyxXeres**

And yet he wrote this. Strange.

I’d still like to read about his efforts elsewhere though. Do you have anything to share?

**4/** **@rfleury** ^2027542644533170333

**@AgileJebrim** **@NyxXeres**

Worth an unblock just to show how pathetically dishonest and idiotic you’re being

https://youtu.be/GB_oTjVVgDc?si=CaATi2ZnXg85rOn8

**5/** **@AgileJebrim** ^2027545886209765630

**@rfleury** **@NyxXeres**

This looks familiar. I think I watched this a while ago. This is *not* at all what I’m talking about. The user is still typing text, there’s still the possibility for typing code errors, and there’s still a significant learning curve involved.

**6/** **@AgileJebrim** ^2027546439224603017

**@rfleury** **@NyxXeres**

Scratch is a lot closer in the right direction. It’s just not well designed with its underlying tech stack. You guys far too easily dismiss that approach.

**7/** **@AgileJebrim** ^2027549162204533025

There’s a big disregard in technical coding communities, including your own, for ease of use and software that “just works” out of the box, without any errors, and reliably without any responsive delays.

You’re still targeting experienced professionals rather than noobs. It reminds me of Linux distros that continually try to pull their users into the terminal, forever cementing their failure to gain widespread adoption among a wider audience.

Nothing about what you’re showing gives enough of an OOMPH! to justify the effort and learning curve for people to switch from their current tools.

**8/** **@rfleury** ^2027551263311991033

**@AgileJebrim** **@NyxXeres**

You have no idea what you’re talking about, and I can only assume you’re BS’ing, given the lack of public information about anything meaningful you’ve worked on. Goodbye.

**9/** **@AgileJebrim** ^2027563206042902687

Some information is publicly available out there if you bothered to look. I’ve mostly been in the flight simulation industry and have worked on a multitude of different simulators over the last 11 years. These are industry-leading training devices that have been used to train hobbyists, airline pilots, and even warfighters flying the F-35.

It also includes geospatial software to assist with mission planning and fire control. A lot of what I produce is sold directly to large corporations and governments.

I’ve also engaged in R&D pushing the bleeding edge of safety-critical GPGPU systems with a particular eye towards serving the needs of avionics and vision systems.

My resume includes Knife Edge Software, Lockheed Martin, and Collins Aerospace/RTX (part of the former Evans & Sutherland group). I always keep my current employer secret, but we work on sensor rendering technology (LWIR, MWIR, NVG, SAR, etc.) that we sell as a plugin to other sims.

On the side, I’ve also built highly affordable MMO tech and now have a small side business where I am building a special shader compiler that is designed to enable easy development of highly performant GPU-centric applications that can be trivially proven to meet safety-critical requirements (WCET determinism and no-fail) at a low cost. You will see more info released about that over time.

**10/** **@rfleury** ^2027566307911373020

**@AgileJebrim** **@NyxXeres**

>if you bothered to look

Holy

**11/** **@AgileJebrim** ^2028488091443355774

I have another more relevant comment to make about your article. Despite your naming convention of lane, this code is actually all scalar. Why would you multithread before you’re SIMDified it? The way you’re doing the summation here isn’t compatible with SIMD unless the autovectorizer gets lucky.

![](https://pbs.twimg.com/media/HCajKvaXwAAxYKI?format=jpg&name=orig)

**12/** **@rfleury** ^2028495224985800883

I never claimed it wasn’t scalar. The term “lane” is overloaded with its SIMD usage, but that is irrelevant, given that the subject of the article wasn’t SIMD. The summation was a simple example to demonstrate the concept, obviously if you needed a sum to be very fast, you’d SIMD it also.

>Why would you multi thread before you SIMD

Again, you wouldn’t in this case. You’d do both. There are many other problems where you need to go across cores before you SIMD.

>The way you’re doing the summation here isn’t compatible with SIMD

No it’s not, at all, even a little bit. I have no idea why you would say that. You can do both, but again, the subject of the post wasn’t SIMD.

**13/** **@AgileJebrim** ^2028496017021116792

I know you didn’t claim it. I’m simply saying you focus way more on multicore and not at all on SIMD. That’s silly and wasteful.

And it isn’t compatible with SIMD because a proper implementation would iterate += 16 at a time to sum batches of 16 per loop iteration. Your current code has a serial dependency by doing it 1 at a time.

**14/** **@AgileJebrim** ^2028496469376872776

**@rfleury** **@NyxXeres**

Index 0 needs to add to index 16, 32, etc.

Index 1 needs to add to index 17, 33, etc.

**15/** **@AgileJebrim** ^2028496926019076423

**@rfleury** **@NyxXeres**

Before you worry about wasting more cores than you need to, use your first core more effectively. Just as hardware engineers optimize things by reducing the distance between hardware components, the same principle should apply to your software. You should be SIMD by default.

**16/** **@AgileJebrim** ^2028497338428203331

Multicore + SIMD is a great combo. Make that your default. Then go all in and make GPGPU your default. You get much better memory bandwidth, far more registers, and the ability to micromanage what’s in your L1 cache.

You’re inching your way closer to my way of doing things. Just take the final leap! 😜
