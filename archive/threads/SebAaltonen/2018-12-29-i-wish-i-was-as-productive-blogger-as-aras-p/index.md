---
title: "I wish I was as productive blogger as @aras_p."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1078805212712841216"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1078805212712841216"
date: 2018-12-29
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "I wish I was as productive blogger as @aras_p."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1078805212712841216
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2018-12-29 00:09:40

## Thread

**1/** **@SebAaltonen** ^1078805212712841216

I wish I was as productive blogger as @aras_p. His latest blog post was pure gold. Somebody with lots of gamedev/perf experience needs to write a blog post titled: ”Raw loops NOT considered a bad practice”.

**2/** **@olson_dan** ^1079067708098920449

**@SebAaltonen** **@aras_p**

Raw loops are not great, ranged-based loops are significantly better but not thought out well enough in C++ (yet?)

**3/** **@ChristerEricson** ^1079110360043466752

**@olson_dan** **@SebAaltonen** **@aras_p**

The problem isn't "range-based" (loops or otherwise). It's that everything "modern" in C++ is implemented as a library instead of natively. So you get: terrible syntax, obscure errors, slow compiles, bad code gen, unpredictable code gen, an inconsistently designed language, etc.

**4/** **@olson_dan** ^1079205956033032192

**@ChristerEricson** **@SebAaltonen** **@aras_p**

Range based loops are a first class feature, not implemented as a library.  There is some possibility that they are slower in debug due to shit implementation, but the conceptual overhead is significantly smaller than "raw" loops.

**5/** **@olson_dan** ^1079206464843960321

**@ChristerEricson** **@SebAaltonen** **@aras_p**

It is of course trivially demonstrable that not everything in scare-quotes "modern" C++ is implemented as a library and your point is kind of lost when I was discussing one of those exact things.

**6/** **@KageKirin** ^1079266185407942657

**@olson_dan** **@ChristerEricson** **@SebAaltonen** **@aras_p**

Maybe confusion with std::for_each, which is implemented as template monster.

**7/** **@hugoamnov** ^1079473906447253504

**@KageKirin** **@olson_dan** **@ChristerEricson** **@SebAaltonen** **@aras_p**

Nah the confusion is due to the fact that the blog post in the OP is about the c++20 ranges, and those definitely suffer from the problems listed by @ChristerEricson but OP also mentions raw loops vs range-based, which don't.

**8/** **@SebAaltonen** ^1079485510215786496

**@hugoamnov** **@KageKirin** **@olson_dan** **@ChristerEricson** **@aras_p**

C++ range based for is a raw loop. You write a raw loop body for it. Non raw loops = std algorithms, such as for_each, remove_if, transform, find_if, partition, etc.

**9/** **@SebAaltonen** ^1079486865802186753

**@hugoamnov** **@KageKirin** **@olson_dan** **@ChristerEricson** **@aras_p**

Raw loop is any loop where you have a C++ loop body and write that loop body yourself. ”No raw loops” policy means that you instead use std algorithms to transform your data. Or the new C++20 ranges library.
