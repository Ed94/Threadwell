---
title: "@nicbarkeragain 100% agree"
type: archive
source: twitter
source_url: "https://x.com/agriffini/status/2120027255615451588"
author: "Andrea Griffini"
handle: agriffini
post_id: "2120027255615451588"
date: 2026-11-10
archived: 2026-11-15
draft: false
tags:
  - archive
  - twitter
  - nicbarkeragain
description: "@nicbarkeragain 100% agree"
in_reply_to: ""
parent_post_id: "2119934264489963758"
---

## Source

- URL: https://x.com/agriffini/status/2120027255615451588
- Author: Andrea Griffini (@agriffini)
- Posted: 2026-11-10 05:34:20

## Branch

**1/** **@agriffini** ^2120027255615451588

**@nicbarkeragain**

100% agree

Function overloading itself is dangerous if used too much. We've a code base that uses it way too much and it's pure hell.
In particular it mixes very bad with implicit conversion: basically when you look at the code you've no idea what's going to happen.

**2/** **@nicbarkeragain** ^2120030204483809651

**@agriffini**

yeah I've seen C++ codebases where a super unexpected chain of 4 implicit conversions happen, and you end up with something completely cooked like passing a string to an int argument with no compiler error 😅

**3/** **@agriffini** ^2120036375319777756

**@nicbarkeragain**

Exactly.

In that project of ours you bump into foo(x,y,z), look up for definition and find out it calls foo(x, z, w), that calls foo(z, w, x) where w.t (that by the way was the original `y`) is used to do something trivial.

Mix in implicit conversions and you get the picture.

**4/** **@nicbarkeragain** ^2120041147271930119

**@agriffini**

Yeah I’ve found them very useful in small specific situations, like reducing boilerplate using libraries that have their own string container implementation, much easier to add a simple implicit conversion to your own string type. Gotta practise restraint though haha

## Related

- Spine: [[archive/threads/nicbarkeragain/2026-11-09-happy-to-admit-that-using-a-minimal-subset-of-c]]
