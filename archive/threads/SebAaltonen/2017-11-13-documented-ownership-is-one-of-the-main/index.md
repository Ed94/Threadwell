---
title: "@kingsamj @EricLengyel Documented ownership is one of the main advantages of unique_ptr over raw ptr."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/930214265750945794"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "930214265750945794"
date: 2017-11-13
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@kingsamj @EricLengyel Documented ownership is one of the main advantages of unique_ptr over raw ptr."
in_reply_to: "930210358614097921"
---

## Source

- URL: https://x.com/SebAaltonen/status/930214265750945794
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2017-11-13 23:22:18

## Thread

**1/** **@SebAaltonen** ^930214265750945794

**@kingsamj** **@EricLengyel**

Documented ownership is one of the main advantages of unique_ptr over raw ptr. Straightforward to understand who owns this object. Downside of unique_ptr is that destructor call needs a complete type. Forward declare isn't enough.

**2/** **@SimonMoos** ^930249760182808577

**@SebAaltonen** **@kingsamj** **@EricLengyel**

Do you then use raw pointers to indicate lack of ownership?

**3/** **@ScottMcMillan0** ^930264647441121281

**@SimonMoos** **@SebAaltonen** **@kingsamj** **@EricLengyel**

That is the convention I’ve generally employed. I.e. never pass raw with a comment like ‘this takes ownership’, pass as unique_ptr if that’s the case. Avoid shared_ptr.

**4/** **@SebAaltonen** ^930350438326644736

**@ScottMcMillan0** **@SimonMoos** **@kingsamj** **@EricLengyel**

Passing unique pointer as an function argument (or returning it) always means that you are transferring ownership (factory function or sink). In common case you pass data by value or reference, unless null is a valid input for function (then use raw pointer).

**5/** **@SebAaltonen** ^930351180852711424

**@ScottMcMillan0** **@SimonMoos** **@kingsamj** **@EricLengyel**

When raw ptr is stored to a structure, it means that this object doesn't own the memory. In a well designed system, an object with a raw ptr never outlives the data that it points to. For example iterators of a container use raw pointers to keep track of their location.

**6/** **@SebAaltonen** ^930351701168656384

**@ScottMcMillan0** **@SimonMoos** **@kingsamj** **@EricLengyel**

Also worth noting that often unique_ptr<T> members can be replaced by simple data members of type T. This is better for cache locality and removes allocations. If you don't need to transfer ownership, then why use a pointer in the first place?

Branches: [[archive/threads/SebAaltonen/2017-11-13-documented-ownership-is-one-of-the-main/2017-11-14-SimonMoos-thanks-very-helpful-to-know]]
