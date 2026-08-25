---
title: "My gamedev head just wants a sort of game mechanic lego for conveying a simd operation frame."
type: archive
source: twitter
source_url: "https://x.com/Ed__dev/status/1944930386984734925"
author: "Ed_"
handle: Ed__dev
post_id: "1944930386984734925"
date: 2025-07-15
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - nicbarkeragain
description: "My gamedev head just wants a sort of game mechanic lego for conveying a simd operation frame."
in_reply_to: ""
parent_post_id: "1944913662499516737"
---

## Source

- URL: https://x.com/Ed__dev/status/1944930386984734925
- Author: Ed_ (@Ed__dev)
- Posted: 2025-07-15 01:21:53

## Branch

**1/** **@Ed__dev** ^1944930386984734925

My gamedev head just wants a sort of game mechanic lego for conveying a simd operation frame. We have carts to give the operation rail and we'll have it vend us the result in the storage bin. All these bins are slices. Everything inside the rail could behave like a shader's frame where you're only allowed to-do simd ops...
So far that I can tell if its in an iterator, the iterator is almost always going to be succeeded after this op occurs so it can be optionally incremented implicitly or manually.  
This may have been done already I haven't done that much studies on this.

![](https://pbs.twimg.com/media/Gv3H3-IWkAAmiVO?format=png&name=orig)

**2/** **@Ed__dev** ^1944933144714457233

You could do more composition by having calls to procs, but it would be the async/await situation where now that proc must be a rail proc for the specific width. 
All operations within the procs must end up being simd, but the slices from arbitrary pointers can come from any struct in memory.

**3/** @Ed__dev

@nicbarkeragain

![](https://pbs.twimg.com/media/Gv3L4JqXAAA22Q4?format=png&name=orig)

**4/** **@Ed__dev** ^1944936495766294767

**@nicbarkeragain**

You could probably do mixin of different simd widths within one rail block but I don't know how that would start to get messy so maybe provide some sort of layout struct like the shaders to specify what the rail expects width wise for a set of bound vars.

**5/** **@Ed__dev** ^1944945740247392259

The nuance is that I know I want to feed these things a very specific width for a range of ops during hot-paths in a pipeline of an program. Its annoying to deal with this width and striding it. Shaders deal with this concept for you to a great degree. These array data layouts for operating on this array data should all be specificable at comp-time so you just need a way to triage that to compositional definitions. Specifying them constantly for every single var's access to their elements is annoying and add complexity to parsing what's going on visually.

Specifically, since at many times any user is doing some weird strides/offsets on data to process, you want to specify on simd/rail blocks runtime offset vars that will be utilized with so they may be in a proc's args but then the rail knows that offset int is for a set of bound slices offset math in a layout definition for the rail/simd block.
This would make the block scope's math data arrays look like shader math, because all the slice specification for the SIMDs was dealt with via specifying some type forum on the simd slices. 

This is equivalent to what structs did for C on doing data offset math on single data instructions.

**6/** **@Ed__dev** ^1944947063931781184

**@nicbarkeragain**

Figuring it out for simd will probably lead to systems langs being able to triage shader compilation and loading of those SPOs to the gpu in in the same lang syntax and you'd just have specific rules for compute, vertex, and frag shader railing blocks.

**7/** **@Ed__dev** ^1944997289308655624

**@nicbarkeragain**

Last dumb example I'll muse about. Def would be fun to try prototyping something like this...

![](https://pbs.twimg.com/media/Gv4EmPLWAAADJDi?format=jpg&name=orig)

## Related

- Spine: [[archive/threads/nicbarkeragain/2025-07-15-i-cant-help-but-have-this-feeling-that-were]]
