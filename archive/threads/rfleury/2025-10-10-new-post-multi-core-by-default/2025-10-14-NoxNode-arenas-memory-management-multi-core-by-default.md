---
title: "@rfleury Arenas : Memory management"
type: archive
source: twitter
source_url: "https://x.com/NoxNode/status/1977914042518843663"
author: "NoxNode"
handle: NoxNode
post_id: "1977914042518843663"
date: 2025-10-14
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury Arenas : Memory management"
in_reply_to: ""
parent_post_id: "1976458516325073141"
---

## Source

- URL: https://x.com/NoxNode/status/1977914042518843663
- Author: NoxNode (@NoxNode)
- Posted: 2025-10-14 01:47:10

## Branch

**1/** **@NoxNode** ^1977914042518843663

**@rfleury**

Arenas : Memory management
Multi-Core By Default : Concurrency
?? : Networking

Is there a simple but high value technique (like this and arenas) but for networking?
Thanks for the article btw, very eye-opening.

**2/** **@rfleury** ^1977926206453690421

I don’t work on networked programs very much, but honestly you can infer my general approach from many of my articles. In my post on deterministic simulation and refresh rates, I show how I split a game simulation thread from the UI/render thread. That same general architecture works if you move the game simulation thread onto a different machine, although obviously specifics change. But that architecture would “slice” the problem correctly for networking.

https://www.rfleury.com/p/main-loops-refresh-rates-and-determinism

**3/** **@NoxNode** ^1978024508196782514

**@rfleury**

I think more so than architecture slicing, I'm looking for a simple and powerful way of making unreliable messages handled by default in the same way this technique makes code multi-core by default. Glenn Fielder has good relevant articles, but I feel like it can be even simpler.

## Related

- Spine: [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default]]
