---
title: "Me and my @plasticdemo team, escaping a wave of green aliens."
type: archive
source: twitter
source_url: "https://x.com/bonzajplc/status/2100543801626390926"
author: "bonzaj/plastic"
handle: bonzajplc
post_id: "2100543801626390926"
date: 2026-09-17
archived: 2026-09-21
draft: false
tags:
  - archive
  - twitter
  - bonzajplc
description: "Me and my @plasticdemo team, escaping a wave of green aliens."
in_reply_to: ""
---

## Source

- URL: https://x.com/bonzajplc/status/2100543801626390926
- Author: bonzaj/plastic (@bonzajplc)
- Posted: 2026-09-17 11:14:03

## Thread

**1/** **@bonzajplc** ^2100543801626390926

Me and my @plasticdemo team, escaping a wave of green aliens. 

Here's a showcase of a massive deterministic GPU simulation working in multiplayer . 

Big immersive worlds are possible to run fluently online (we are in 400 km range). 

Everyone is simulating exactly the same world.

<video controls src="https://video.twimg.com/amplify_video/2100543524747751425/vid/avc1/1920x1080/OA--pTX-jKfxpBUL.mp4?tag=29"></video>

**2/** **@bendzzArt** ^2100567899106914717

**@bonzajplc** **@plasticdemo**

how do you handle desyncs? Players desync all the time and affect the sim right?

**3/** **@bonzajplc** ^2100571740015337813

**@bendzzArt** **@plasticdemo**

No :). Generally we need to be 100% sure that the player will not desync

**4/** **@AgileJebrim** ^2100600800896598170

**@bonzajplc** **@bendzzArt** **@plasticdemo**

Oh that’s not workable at scale then lol. You need to rework your network protocol to utilize an eventual consistency UDP approach where you just constantly stream snapshots of current local state.

**5/** **@AgileJebrim** ^2100600901962551569

**@bonzajplc** **@bendzzArt** **@plasticdemo**

Be completely unreliable where it’s perfectly fine that any packet drops.

**6/** **@bonzajplc** ^2100602329728708682

**@AgileJebrim** **@bendzzArt** **@plasticdemo**

really hard with deterministic approach. The simulation cannot progress if you won't agree that everyone has sent their actions. It's probably not scallable to 1000's of unrealiable players. it's good for party of friends.

**7/** **@AgileJebrim** ^2100602970580697111

**@bonzajplc** **@bendzzArt** **@plasticdemo**

So where is the scale of the GPU being applied if not to the players? An enormous numbers of NPCs?

Next question: Is there an authoritative server involved or is this entirely peer-to-peer?

**8/** **@bonzajplc** ^2100609118717321547

**@AgileJebrim** **@bendzzArt** **@plasticdemo**

There is still a server. NPCs, physics, fluids, world destruction. Dynamic multiplayer world

**9/** **@AgileJebrim** ^2100611262203769111

**@bonzajplc** **@bendzzArt** **@plasticdemo**

Is the server running the code on a GPU too?

That’s very expensive hosting for only 4 players. That’s why I encourage an architecture that can scale to a massive number of players. You can then subdivide the hosting costs among many more users.

**10/** **@AgileJebrim** ^2100611667801313390

**@bonzajplc** **@bendzzArt** **@plasticdemo**

I guess the main reason you’re using the deterministic approach is to avoid sending all that vast dynamic state data across the network. Certainly an advantage on the bandwidth cost front.

**11/** **@59thProfile** ^2100622133105705370

**@AgileJebrim** **@bonzajplc** **@bendzzArt** **@plasticdemo**

right, only need to send inputs!

**12/** **@AgileJebrim** ^2100623336095023274

**@59thProfile** **@bonzajplc** **@bendzzArt** **@plasticdemo**

Yep. Fine for RTSes or anything with small player counts and many entities. He could stuff multiple independent running matches into a single server node and that might make it economical.

**13/** **@59thProfile** ^2100625981266399498

**@AgileJebrim** **@bonzajplc** **@bendzzArt** **@plasticdemo**

multiple, as in thousands probably

**14/** **@AgileJebrim** ^2100626906219421721

**@59thProfile** **@bonzajplc** **@bendzzArt** **@plasticdemo**

Tens of thousands. :P

**15/** **@59thProfile** ^2100631876733944223

**@AgileJebrim** **@bonzajplc** **@bendzzArt** **@plasticdemo**

yeah and if you do it right (i think bonzaj is missing something here) desync should be impossible and can potentially be used as anti-cheat primitive

**16/** **@AgileJebrim** ^2100634824293618129

**@59thProfile** **@bonzajplc** **@bendzzArt** **@plasticdemo**

Since his server is just a relay, he’s got no way to send someone the current state of the game newly connected or reconnected unless he either replays every packet that’s ever occurred or more likely just have one player forward a snapshot of their current state of the game.

**17/** **@AgileJebrim** ^2100635000584470582

**@59thProfile** **@bonzajplc** **@bendzzArt** **@plasticdemo**

The game is also only as fast as the slowest player’s connection if he’s doing it like I think he is. That’s not good.

**18/** **@bonzajplc** ^2100646208037433519

**@AgileJebrim** **@59thProfile** **@bendzzArt** **@plasticdemo**

Yeah, that’s why I look into consoles :)

**19/** **@AgileJebrim** ^2100646372349190392

**@bonzajplc** **@59thProfile** **@bendzzArt** **@plasticdemo**

Doesn’t do much good if they’re on WiFi and constantly disconnecting.

**20/** **@NOTimothyLottes** ^2100648916634984482

**@AgileJebrim** **@bonzajplc** **@59thProfile** **@bendzzArt** **@plasticdemo**

When it’s massive destruction, I can seen the appeal of deterministic sim. Now if the sim can run faster than real-time you can handle disconnection. Clients that dont make the sim frame’s time cut have to take a predicted future state for the sim frame ….

**21/** **@NOTimothyLottes** ^2100650025999093837

**@AgileJebrim** **@bonzajplc** **@59thProfile** **@bendzzArt** **@plasticdemo**

Reconnect, the server give the corrected past, run faster than real-time until time syncs again, with all the workarounds that requires. Same with late connection, you’ve see the game in fast forward until the timelines meet. At least you only sync action and not effect.

**22/** **@59thProfile** ^2100652524583723029

**@NOTimothyLottes** **@AgileJebrim** **@bonzajplc** **@bendzzArt** **@plasticdemo**

Server doesn’t have to do anything you could just relay the client

**23/** **@NOTimothyLottes** ^2100658236483330316

**@59thProfile** **@AgileJebrim** **@bonzajplc** **@bendzzArt** **@plasticdemo**

In my example the server is relaying the authoritive actions for the frame (or series of past frames). Assuming no P2P in the architecture. Note Im assuming the server is also running the sim to correct for clients behaviors on forward extrapolation state that players see.

**24/** **@NOTimothyLottes** ^2100659503112892821

**@59thProfile** **@AgileJebrim** **@bonzajplc** **@bendzzArt** **@plasticdemo**

Im working on something with non deterministic massive destruction. But locally relative sync of state between peers. So effectively the opposite design. But seeing full deterministic in the video, is quite inspiring.

**25/** **@bonzajplc** ^2100666022152003834

Maintaining that is quite a challange. yesterday I Introduced a change that breaks determinism randomly on one of the tests. The problem is that it triggered today after 10 other merges from the team. 

Also I know now that driver updates can also break determinism. By that I mean between players. We can detect that their startup hashes (based on a test that coverages most of the features) is different and warn them that they may desync, but it's quite nasty design

**26/** **@NOTimothyLottes** ^2100667343441436815

**@bonzajplc** **@59thProfile** **@AgileJebrim** **@bendzzArt** **@plasticdemo**

Haha, driver updates as in compiler changes to float ordering and factoring … if I went deterministic, I’d go to integer maths. But I did most of my learnings pre floating point, so integer is easy in the brain.

**27/** **@NOTimothyLottes** ^2100667901661356378

**@bonzajplc** **@59thProfile** **@AgileJebrim** **@bendzzArt** **@plasticdemo**

You could do screwy things like alias to int and zero the LSB bit periodically to force some amount of float sanity in the compiler (because the AND cannot be moved relative to neighboring ops).
