---
title: "@BOENSAW Entities don’t have to go but having a mental framework where entities run functions is probably not helpful."
type: archive
source: twitter
source_url: "https://x.com/Jonathan_Blow/status/2036815488173703237"
author: "Jonathan Blow"
handle: Jonathan_Blow
post_id: "2036815488173703237"
date: 2026-03-25
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - BOENSAW
description: "@BOENSAW Entities don’t have to go but having a mental framework where entities run functions is probably not helpful."
in_reply_to: ""
parent_post_id: "2036653149948424230"
---

## Source

- URL: https://x.com/Jonathan_Blow/status/2036815488173703237
- Author: Jonathan Blow (@Jonathan_Blow)
- Posted: 2026-03-25 14:40:29

## Branch

**1/** **@Jonathan_Blow** ^2036815488173703237

**@BOENSAW**

Entities don’t have to go but having a mental framework where entities run functions is probably not helpful.

**2/** **@anicic_filip** ^2037079338512769397

**@Jonathan_Blow** **@BOENSAW**

Could you expand on that? 
I've seen:
- entities with no function pointers, use of switches by entity type, with logic ran per case
- entities with function pointers
- OOP child classes with method overrides.

Is this what you are describing as a mental framework?

**3/** **@Jonathan_Blow** ^2037294870939972085

**@anicic_filip** **@BOENSAW**

My game code has evolved toward "iterate over all entities of type X, do Y on them, at the place in the code where this needs to happen". The entity does not own the function, the game engine owns the function.

**4/** **@Jonathan_Blow** ^2037295493085319580

(So instead of having a generic tick function where you switch on entity type, and then a generic pre-tick because of course you need that, and pre-pre-tick, and post-tick, etc, you just have small bits of code where you iterate over things by type and do what that type needs. If you store the entities by type in the first place (which is a very efficient way to do it due to uniform size), then these iterations are much faster than iterating over randomly-typed entities in random order.

**5/** **@Jonathan_Blow** ^2037295938583314583

**@anicic_filip** **@BOENSAW**

A real-world example (but most loops have more in the body; this one is chosen for readability):

![](https://pbs.twimg.com/media/HEXt2j_bUAAxPLa?format=png&name=orig)

**6/** **@Jonathan_Blow** ^2037296285506822315

**@anicic_filip** **@BOENSAW**

The idea of a generic tick function for entities is really not great to begin with, because in a complex game you end up caring a great deal about what order things happen in, then you need to go to great pain to impose this order. Instead, you can just say "do A, then B, ..."

**7/** **@iquilezles** ^2037321785008668834

Once I saw a project where everything was entities with a .tick(), plus a gigantic priority table intended to orchestrate the mess. Because reasoning the flow was still too hard, developers had added yield() for_rand_number_of_frames everywhere, "to give other entities some time to run their tick()s". Naturally all actions took multiple frames to execute, and they still had flow/synch bugs everywhere anyways.

I advised them to burn thing down and move on to just an app loop with { do_thing_A(); do_thing_B(); ... do_thing_Z(); }. But they didn't. The project failed a year after under the weight of its own spaghetti design.

You could say the problem was that particular team of coders, not the design per-se. But, I mean, I've seen this story repeat with different teams repeat 3 or 4 times by now...

**8/** **@Jonathan_Blow** ^2037322309502185845

**@iquilezles** **@anicic_filip** **@BOENSAW**

Everyone wants to think they are in the Matrix and doing some super cool entity simulation reality engine. In reality it is just clumsy code failing to do something simple, at great cost in complexity, speed and reliability.

**9/** **@BOENSAW** ^2037340571690471473

**@Jonathan_Blow** **@iquilezles** **@anicic_filip**

I think part of the appeal is also hiding code so that it appears simpler because you can't see all of it at once. not that that's good, lol

## Related

- Spine: [[archive/threads/BOENSAW/2026-03-25-the-more-experienced-i-get-programming-games-the]]
