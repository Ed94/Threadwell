---
title: "@simplex_fx Context: It's a mostly experimental engine meant to be a workspace for research."
type: archive
source: twitter
source_url: "https://x.com/BrrtrnP/status/1887236840194998670"
author: "PBrrtrn"
handle: BrrtrnP
post_id: "1887236840194998670"
date: 2025-02-05
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - simplex_fx
description: "@simplex_fx Context: It's a mostly experimental engine meant to be a workspace for research."
in_reply_to: ""
parent_post_id: "1887224326350635382"
---

## Source

- URL: https://x.com/BrrtrnP/status/1887236840194998670
- Author: PBrrtrn (@BrrtrnP)
- Posted: 2025-02-05 20:28:20

## Branch

**1/** **@BrrtrnP** ^1887236840194998670

**@simplex_fx**

Context: It's a mostly experimental engine meant to be a workspace for research. As such there's a heavy focus on devices that support latest capabilities. Don't think people are expected to pick Spartan up and make a game to put on Steam.

**2/** **@simplex_fx** ^1887238637596909575

Meanwhile, people run bleeding edge AI research on 7-11yo GPUs...

not supporting 8yo hw is just retarded masturbation, not research.

Also
"Spartan Engine is one of the most advanced one-man game engines out there, pushing the limits of real-time approaches."

I assume, he meant the limits for entry here :D

**3/** **@BrrtrnP** ^1887241495268499862

**@simplex_fx**

Way I see it, it's not so much about the specific GPUs you want to support, but rather about the cost/benefit of portability.

**4/** **@simplex_fx** ^1887256960594034899

**@BrrtrnP**

I mean, maybe checking for actual gpu caps would make more sense, and just maybe fucking disable features, based on that.

or vulkan version, if you are lazy

**5/** **@GustavSterbrant** ^1887259761294594524

**@simplex_fx** **@BrrtrnP**

It does that. But you’re too lazy to ask about it or to read the code. Instead you jump on the insult train immediately, while calling other people lazy. Not a great look.

**6/** **@simplex_fx** ^1887260479594332463

**@GustavSterbrant** **@BrrtrnP**

it literally compares fucking strings too.

**7/** **@GustavSterbrant** ^1887260618526478339

**@simplex_fx** **@BrrtrnP**

Yes and? Oh yeah I forgot you’re like an Amish person but for coding.

**8/** **@simplex_fx** ^1887260914757607829

**@GustavSterbrant** **@BrrtrnP**

maybe it's a fucking retarded thing to figure out gpu caps based on vendor string?

go back sucking off your pal

**9/** **@GustavSterbrant** ^1887261419856343342

**@simplex_fx** **@BrrtrnP**

He’s not. I asked him if he checks capabilities and he said his engine does that first, this is just for the warning. But you jumped to conclusions thinking it’s so easy to write a Vulkan renderer from scratch.

**10/** **@AgileJebrim** ^1887261780059009035

**@GustavSterbrant** **@simplex_fx** **@BrrtrnP**

It is easy to write a Vulkan renderer from scratch.

**11/** **@GustavSterbrant** ^1887261914969063450

**@AgileJebrim** **@simplex_fx** **@BrrtrnP**

Not even remotely.

**12/** **@GustavSterbrant** ^1887262512258924686

**@AgileJebrim** **@simplex_fx** **@BrrtrnP**

What you are talking about is an extremely narrow, compute only ray marcher. That’s not a renderer, that’s a laboration. A renderer is capable of handling content, materials, shaders etc. Be efficient with uploading memory, visibility, submitting frames and synchronization.

**13/** **@NOTimothyLottes** ^1887284591754440819

**@GustavSterbrant** **@AgileJebrim** **@simplex_fx** **@BrrtrnP**

In my generation the now vintage machines didn't really have enough memory to handle the associated code complexity we have today, and well one can still author things in that way on modern machines, which makes it still approachable for one person :)

**14/** **@simplex_fx** ^1887287012287226246

**@NOTimothyLottes** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

Not that vintage, if you worked on WinCE 4-5-6 crap. Most didn’t even had fpus 😅

**15/** **@NOTimothyLottes** ^1887288475671576874

**@simplex_fx** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

My dad tried to force me off games by throwing away the Atari and C64, so I had cut my teeth mostly on ASM on a 8086 at first.

**16/** **@simplex_fx** ^1887289402415579625

**@NOTimothyLottes** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

We were too poor, never got hands on PC.

First pc was then top of the line 166mhz pentium, not sure how my father managed to buy it, it was ultra expensive.
Considering it was in mid 90s eastern europe, I suspect something semi-illegal at minimum😅

**17/** **@simplex_fx** ^1887291056959443001

**@NOTimothyLottes** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

All the c64 had was basic-assisted asm 😅😅

I was furious when I saw shit like PLOT xy on an Atari or something 😅 We had to hit mem addresses with a hammer until it looked good (or froze the computer, probably destroying a day of work)

**18/** **@simplex_fx** ^1887294440026616229

**@NOTimothyLottes** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

Tbh perfect graphics api to me is still that.

Unified memory, and mostly just dropping shit into random mem addresses instead of calling fuckton of api crap

**19/** **@NOTimothyLottes** ^1887297722815783269

**@simplex_fx** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

I know of at least one other game dev (besides myself) doing compute-only (no vertex/pixel) all GPU-side game logic. And minus init-time setup, the runtime is mostly exactly as you described, API-free.

**20/** **@simplex_fx** ^1887302551155941632

**@NOTimothyLottes** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

I still see too many problems related input and sound. Mostly latency related ones.

**21/** **@NOTimothyLottes** ^1887304954836099411

**@simplex_fx** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

It is substantially lower input latency. More so if the majority of render logic can be view-independent. You read input on GPU then only right before updating player+camera before view-dependent render. Below is how I do it ...

![](https://pbs.twimg.com/media/GjEM3AMWUAAmFo0?format=png&name=orig)
![](https://pbs.twimg.com/media/GjENxwBXkAA9grx?format=png&name=orig)

**22/** **@simplex_fx** ^1887306831485190594

**@NOTimothyLottes** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

I mean gameplay vs input not cam vs input

**23/** **@NOTimothyLottes** ^1887308171569459242

**@simplex_fx** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

Gameplay logic is done on the GPU too.
No CPU involvement.
So yeah, it is about as real low latency as possible.

**24/** **@simplex_fx** ^1887308790103437322

**@NOTimothyLottes** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

Ok but input devices don’t grow on the gpu.

Not to mention sound card and nic

**25/** **@NOTimothyLottes** ^1887310996022112697

**@simplex_fx** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

Incoming UDP packets (I prefer fixed size) can be fed to the GPU using a similar method. Modern GPUs from AMD/NV have quite capable scalar cores which run in parallel with the vector ones, and GPU scalar cores might even be lower power ...

**26/** **@simplex_fx** ^1887311684047397364

**@NOTimothyLottes** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

I mean, is there some direct nic-gpu stuff?

I recently maybe saw something in an AI related context, not sure of that’s a thing, or how that works.

Kinda like nvme->gpu stuff?

My problem is more like the other way, aka fetching data from gpu

**27/** **@NOTimothyLottes** ^1887316887219925286

**@simplex_fx** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

It would be nice if one could setup shared memory mappings between devices [storage/sound/NIC/etc] and then completely bypass the CPU, but today's OS/driver/HW engineering fail continues.

**28/** **@NOTimothyLottes** ^1887319803834077606

**@simplex_fx** **@GustavSterbrant** **@AgileJebrim** **@BrrtrnP**

At a minimum IHVs could provide a way to shader store to the DRAM used by the HDMI out audio ring buffer, and also have HW write the [in/out] position to L2|DRAM so it is shader read accessible. Then also you'd need pinned allocations and quality of service on GPU runtime

## Related

- Spine: [[archive/threads/simplex_fx/2025-02-05-i-mean-1050-and-1060-are-just-top20-gpus-in]]
