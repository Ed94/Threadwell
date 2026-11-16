---
title: "In plan9 a single process cannot make threads as you typically know them."
type: archive
source: twitter
source_url: "https://x.com/_rygo6/status/1987691022328246674"
author: "rygo6"
handle: _rygo6
post_id: "1987691022328246674"
date: 2025-11-10
archived: 2026-11-15
draft: false
tags:
  - archive
  - twitter
  - _rygo6
description: "In plan9 a single process cannot make threads as you typically know them."
in_reply_to: ""
---

## Source

- URL: https://x.com/_rygo6/status/1987691022328246674
- Author: rygo6 (@_rygo6)
- Posted: 2025-11-10 01:17:23

## Thread

**1/** **@_rygo6** ^1987691022328246674

In plan9 a single process cannot make threads as you typically know them. If you make a thread in plan9 it creates what is essentially the equivalent to an async method, or coroutine, or goroutine, or fiber by today's terminology. Which means in plan9, out-of-the-box, plain C innately works akin to how async programming works in every other language.

This I personally found interesting as since that time a lot of programming paradigms have ended up emulating this type of behavior by adding coroutines or async methods or other and relies heavily on this type of programming model now. Which plan9 had the foresight to see and innately make plain C with the OS threads API behave that way. If plan9 had caught on rather than Unix all the additional language features relating to coroutines, async, fibers etc. etc. would have been moot.

Which you might wonder, what if you did want an actual hardware thread? You could still do that, but only through creating another process. Which plan9 rfork was particularly made to be lightweight to enable making new processes. It also had more options to give fine-grained control over what exact memory was shared upon making a new thread. You had to explicitly make a chunk of memory shared for it to be available, then specify this shared memory to be available to the forked process. Shared memory chunks were of course represented as files. But the preferred way to share state was to create channels, bi-directional lockless queues, which would then have to be explicitly shared with the forked process, and were also represented as files. In this way plan9 innately solved much of the concurrency complications with plain C. By default, two hardware threads could not access the shared state of one another. You had to explicitly make a chunk of memory and specify which threads could access it. Or ideally you made a channel, and explicitly marked it as being available to specific forked child process. Channels also became a model adopted by later programming language features for dealing with concurrency which plan 9 simply did out-of-the-box with C. If plan9 caught on many of the concurrency features in languages invented since would have also been moot.

For brevity there was an option of rfork to simply make a whole process with full shared memory of the parent process, essentially operating like a modern OS thread, however this was more so the nuclear option and not preferred.

Personally, I'm thinking... this sort of model should probably be replicated for C in general. It solves some of the difficult issues of C concurrency purely through a different kind of underlying C API and changing of OS concepts. Most people since when they looked at similar complications automatically deferred to adding new language features and new concepts. When really maybe the better solution was to the re-think exactly how the underlying OS concepts and libraries should work.

Of note, plan9 from userpsace made a big step in making a lot of this programming model of C available in other OSs. Although I've not personally dug into trying to use that much. Now I am wondering... maybe that is the way to go for any attempt to improve upon C or should have been the way any attempt to improve programming should have gone. Not through adding new language features but through re-thinking how the underlying system library works. Maybe the whole premise of new language features and languages to evolve programming paradigms was facing the exact opposite direction than it should have. Maybe it should have been looking deeper for how to refactor, consolidate, delete and change the underlying system concepts and system library rather than just add new stuff on top. Programmers tend to fall into that trap of not understanding things at a deeper level and looking for solutions there, but instead just layering more on top.
