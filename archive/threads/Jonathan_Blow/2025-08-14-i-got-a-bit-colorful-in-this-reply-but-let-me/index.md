---
title: "I got a bit colorful in this reply, but let me describe why this drives me so crazy, especially now in 2025:"
type: archive
source: twitter
source_url: "https://x.com/Jonathan_Blow/status/1956008762461823353"
author: "Jonathan Blow"
handle: Jonathan_Blow
post_id: "1956008762461823353"
date: 2025-08-14
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "I got a bit colorful in this reply, but let me describe why this drives me so crazy, especially now in 2025:"
in_reply_to: ""
---

## Source

- URL: https://x.com/Jonathan_Blow/status/1956008762461823353
- Author: Jonathan Blow (@Jonathan_Blow)
- Posted: 2025-08-14 15:03:24

## Thread

**1/** **@Jonathan_Blow** ^1956008762461823353

I got a bit colorful in this reply, but let me describe why this drives me so crazy, especially now in 2025:

Now someone comes along to make their web app, and they are using React or something.

So now we have *at minimum* 4 layers of wrapping: React -> browser API -> SDL -> OS API.

Each layer adds inefficiency and bugs and wastes a large amount of programmer time.

This is just on *one browser*. Every single other web browser has to run the same React app in the same way, with some *different* stack of 4+ wrappers all acting on each other.

What is the goal of all these browsers doing all these heterogeneous things that sucks up all these programmer life years? Actually the goal is to ***provide no new functionality***, because not only does a browser API not provide anything that was not in the pre-browser APIs, they all have to be compatible with each other or web pages won't work.

Meanwhile every other system, that is not a browser, that also wants to provide a consistent API to its users, has to do the same thing, but different, because the provided APIs are different.

So if we are putting this huge amount of effort in to do all this redundant heterogeneous programming to solve the same problem dozens or hundreds of times, it must really be worth it, right? Like, we must be solving some super serious difficult rocket science problem?

No, keyboard and mouse input is very close to the simplest possible API. You have information about each event. That information is a small set of enums and flags. But everyone has trivially different numbers for their enums and flags because everyone wants trivially different numbers for their enums and flags. (If you get really crazy, you might want to identify which device an event came from, but almost no programmers do this).

So we do this immense amount of programming effort, slowness at runtime, bugs to users, etc, in order to map trivially different numbers back and forth.

If we are going to screw around forever making mess after mess for such a simple thing, we don't deserve to be able to do complex and nuanced things. And so it has come to be: we almost can't do complex and nuanced things at all, any more. But even if we could, we wouldn't have the time.

Multiply this by 1000 different systems, and you get today's software. 

I feel programmers in 2025 are just very low-IQ compared to how programmers are "supposed" to be. It's like there's a very simple maze on a piece of paper in front of us but we just can't figure out the line to draw through the maze. So we get out a crayon and scribble (incidentally making the maze bigger) but we have a big dumb idiot smile for a few minutes because we contributed to open source!!!! (Followed by years of painful toothache as we deal with the things we actually typed).

[BTW, jai adds to this problem -- we have our own set of trivially different numbers and flags. I hate it and I think it is stupid, but because I am spending my time and energy making a programming language, engine, and game, I don't have the bandwidth to solve the actual problem here, the solution to which seems to be political to at least a substantial degree.]

https://x.com/Jonathan_Blow/status/1955819306010468582

**2/** **@Jonathan_Blow** ^1956012404547932416

P.S. I also meant to point out that all these ugly wrappers don't even implement anything really, because we haven't even talked about how keyboard and mouse events actually get created in the first place, which is its own entire huge ugly horror show at this point...

Branches: [[archive/threads/Jonathan_Blow/2025-08-14-i-got-a-bit-colorful-in-this-reply-but-let-me/2025-08-14-TylerGlaiel-are-you-talking-about-sdl-here-or-the-web-browser]], [[archive/threads/Jonathan_Blow/2025-08-14-i-got-a-bit-colorful-in-this-reply-but-let-me/2025-08-14-hr_sasja-how-bad-can-it-be-poll-recognizes-new-press-key]], [[archive/threads/Jonathan_Blow/2025-08-14-i-got-a-bit-colorful-in-this-reply-but-let-me/2025-08-15-PierreJoye-for-most-cases-it-comes-down-to-ui-needs-2025-and]], [[archive/threads/Jonathan_Blow/2025-08-14-i-got-a-bit-colorful-in-this-reply-but-let-me/2025-08-15-etodanik-i-still-have-flashbacks-to-implementing-a-cef]], [[archive/threads/Jonathan_Blow/2025-08-14-i-got-a-bit-colorful-in-this-reply-but-let-me/2025-08-15-Mallchad-i-like-how-people-are-obsessed-with-minimal-apis]], [[archive/threads/Jonathan_Blow/2025-08-14-i-got-a-bit-colorful-in-this-reply-but-let-me/2025-08-19-PhilAndrew61181-i-feel-like-its-almost-screenshot-saturday-sdl-3]]
