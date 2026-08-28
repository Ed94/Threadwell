---
title: "@AllenWebster4th IMO the real reason to avoid `malloc` nowadays (for any device with virtual addressing) is to avoid the internal lock contention."
type: archive
source: twitter
source_url: "https://x.com/RandyPGaul/status/1594772462289715201"
author: "Randy Gaul"
handle: RandyPGaul
post_id: "1594772462289715201"
date: 2022-11-21
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - RandyPGaul
description: "@AllenWebster4th IMO the real reason to avoid `malloc` nowadays (for any device with virtual addressing) is to avoid the internal lock contention."
in_reply_to: ""
---

## Source

- URL: https://x.com/RandyPGaul/status/1594772462289715201
- Author: Randy Gaul (@RandyPGaul)
- Posted: 2022-11-21 19:19:19

## Thread

**1/** **@RandyPGaul** ^1594772462289715201

**@AllenWebster4th**

IMO the real reason to avoid `malloc` nowadays (for any device with virtual addressing) is to avoid the internal lock contention. Arena doesn't really help much here beyond preventing fragmentation within pages, which imo is still not that great of a benefit.

**2/** **@rfleury** ^1594778888861020160

**@RandyPGaul** **@AllenWebster4th**

Unfortunately there is a huge lack of precision in the terms. Arenas—or at least what I mean by arenas—are growing linear/stack allocators with explicit handles. They don’t have any locking mechanism. This can dramatically *help* with synchronization.

**3/** **@rfleury** ^1594780740532985856

**@RandyPGaul** **@AllenWebster4th**

(Specifically because the natural usage pattern is to not allow, generally, one arena to cross the boundary between two threads, unless you’re explicitly making an interlocked synchronized data structure or something of the sort)

**4/** **@RandyPGaul** ^1594782194647855104

**@rfleury** **@AllenWebster4th**

Yeah if it’s thread local then you got it. But that’s a pretty strong limitation for “general use”.

Main thing of interest to me is framing contention as the primary concern as opposed to fragmentation

**5/** **@RandyPGaul** ^1594783978875392000

**@rfleury** **@AllenWebster4th**

Example cute_tiled.h https://github.com/RandyGaul/cute_headers/blob/master/cute_tiled.h a SFH lib for parsing JSON maps created by https://www.mapeditor.org/ uses an arena allocator. I actually really regret it. Complicates code unnecessarily and provides almost no practical benefit to anyone using the lib.

**6/** **@rfleury** ^1594788957728174080

**@RandyPGaul** **@AllenWebster4th**

This is why I think there is some misunderstanding regarding the terminology. Thread-local allocation isn’t prohibitive for general use, it’s what you want by default, with minimal (and explicit) cross-thread communication.

**7/** **@rfleury** ^1594789248385056770

**@RandyPGaul** **@AllenWebster4th**

Furthermore, I haven’t looked at your library much, but in the Metadesk library—a very similar problem—we also use arenas, and our experience was entirely different. On the surface, it looks like we have very different ideas about what arenas are and what they mean to the caller.

**8/** **@RandyPGaul** ^1594798522024734720

**@rfleury** **@AllenWebster4th**

What’s different in your experience? Just curious for discussion’s sake, not trying to prod or anything 😊

**9/** **@rfleury** ^1594815318819737601

**@RandyPGaul** **@AllenWebster4th**

Twitter is low bandwidth so it’s impossible to be anything but low detail, but basically everything — arenas have helped simplify APIs, simplify allocation, improve performance, and eliminate bugs. I can’t be much more precise but a lot of the reasoning is embedded in the API.

**10/** **@RandyPGaul** ^1594830594307166209

**@rfleury** **@AllenWebster4th**

I see you used it in your API. API aside, in terms of threading MD is single-threaded internally, yes? I'd be curious to see a use-case example from customer PoV where the arenas lowered threading contention

**11/** **@RandyPGaul** ^1594832245264896000

**@rfleury** **@AllenWebster4th**

Usually for parser/loader kind of tasks I see them happen once at startup and never again, so lock contention on malloc usually a non-existent priority. Maybe MD is used differently than this?

**12/** **@rfleury** ^1594854847500922881

**@RandyPGaul** **@AllenWebster4th**

Metadesk’s implementation is single threaded in the sense that it contains no synchronization, but this is because it’s strictly organized as stateless, data-in-data-out transforms. Multithreading occurs by bucketing these transforms (and their arenas) on different threads.

**13/** **@rfleury** ^1594855461047914496

**@RandyPGaul** **@AllenWebster4th**

Arenas do not solve contention, but they don’t promote usage patterns that introduce unnecessary contention. They’re useful building blocks in bucketing allocations and work, which is exactly what you need for minimizing contention.

**14/** **@RandyPGaul** ^1594872404408696832

**@rfleury** **@AllenWebster4th**

Makes sense thanks for explaining!
