---
title: "New programming blog post about the complexity and performance trade-offs of maintaining entity memory contiguity in games."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1235037224976044034"
author: "Ryan Fleury"
handle: rfleury
post_id: "1235037224976044034"
date: 2020-03-04
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "New programming blog post about the complexity and performance trade-offs of maintaining entity memory contiguity in games."
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/1235037224976044034
- Author: Ryan Fleury (@rfleury)
- Posted: 2020-03-04 02:59:54

## Thread

**1/** **@rfleury** ^1235037224976044034

New programming blog post about the complexity and performance trade-offs of maintaining entity memory contiguity in games.

#programming #gamedev 

https://ryanfleury.net/blog_entity_memory_contiguity

**2/** **@simplex_fx** ^1235160069026844673

**@rfleury**

"This is also why, in my estimation, it is not a good idea for a game engine that supports many possible games to enforce this kind of design structure on gameplay code, because it constrains design ideas"

Could you elaborate on this? :)

**3/** **@rfleury** ^1235223001504698368

**@simplex_fx**

Yes—engines often are opinionated about entities, and enforce some of generic model in which entities are defined. This doesn't seem like a net win to me, since different games have different problems, and different entity structures lend themselves better to different problems.

**4/** **@simplex_fx** ^1235255274572742656

**@rfleury**

ECS has nothing to do with how entities are defined.

There could be generic micro components, and systems, but there could be big, and/or specialized ones too.

You could still have an entity archetype with just one big component.

**5/** **@rfleury** ^1235261483740565504

**@simplex_fx**

I didn't argue against any of that. I just said that ECS is designed to solve a specific problem, and therefore it's a specific solution. The blog post isn't about any of this.

**6/** **@simplex_fx** ^1235268864222670848

**@rfleury**

ECS is not designed to solve a specific problem. It just means, that you keep data, relations between data, and transformations on the data separated.

I don't see, how it constrains design ideas. 
But it could certainly allow drastic improvements in entity memory contiguity.
