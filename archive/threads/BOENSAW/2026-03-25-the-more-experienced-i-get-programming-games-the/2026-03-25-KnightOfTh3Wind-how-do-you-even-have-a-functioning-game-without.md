---
title: "@BOENSAW How do you even have a functioning game without entities"
type: archive
source: twitter
source_url: "https://x.com/KnightOfTh3Wind/status/2036777757875581351"
author: "Knight Errant"
handle: KnightOfTh3Wind
post_id: "2036777757875581351"
date: 2026-03-25
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - BOENSAW
description: "@BOENSAW How do you even have a functioning game without entities"
in_reply_to: ""
parent_post_id: "2036653149948424230"
---

## Source

- URL: https://x.com/KnightOfTh3Wind/status/2036777757875581351
- Author: Knight Errant (@KnightOfTh3Wind)
- Posted: 2026-03-25 12:10:33

## Branch

**1/** **@KnightOfTh3Wind** ^2036777757875581351

**@BOENSAW**

How do you even have a functioning game without entities

**2/** **@BOENSAW** ^2036779389757894720

**@KnightOfTh3Wind**

I'm just guessing, but over time I've realized less and less things actually need to be compartmentalized into boxes and can just be managed as a part of global state

**3/** **@SagelessRanger** ^2036781762752205009

**@BOENSAW** **@KnightOfTh3Wind**

Can you make this expand on this idea this sounds very interesting and potentially more clear to manage

**4/** **@BOENSAW** ^2036786837029863443

**@SagelessRanger** **@KnightOfTh3Wind**

Take a cutscene for a simple example. A naive approach might be something like "npc object spawns a textbox object and sends text from its text variable". Doesn't sound so bad but what if two NPCs activate at once, what if the textbox or npc gets destroyed somehow... error prone

**5/** **@BOENSAW** ^2036787552238342282

**@SagelessRanger** **@KnightOfTh3Wind**

Something more along this line of thinking would be like "interaction system detects conditions to begin the cutscene state which reads from a script and draws textboxes automatically". less interdependence, no reliance on external objects, no way to muddy the state

## Related

- Spine: [[archive/threads/BOENSAW/2026-03-25-the-more-experienced-i-get-programming-games-the]]
