---
title: "When writing graphics applications and demos, I've found loading in complex geometry without introducing any ridiculous dependencies (I'm looking at you, Assimp) is a pain and normally results in me writing some crappy special-case parser for OBJ so that I can throw some..."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1144107248215609344"
author: "Ryan Fleury"
handle: rfleury
post_id: "1144107248215609344"
date: 2019-06-27
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "When writing graphics applications and demos, I've found loading in complex geometry without introducing any ridiculous dependencies (I'm looking at you, Assimp) is a pain and normally results in me writing some crappy special-case parser for OBJ so that I can throw some..."
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/1144107248215609344
- Author: Ryan Fleury (@rfleury)
- Posted: 2019-06-27 04:56:39

## Thread

**1/** **@rfleury** ^1144107248215609344

When writing graphics applications and demos, I've found loading in complex geometry without introducing any ridiculous dependencies (I'm looking at you, Assimp) is a pain and normally results in me writing some crappy special-case parser for OBJ so that I can throw some... (1/5)

**2/** **@rfleury** ^1144107248911884288

...static geometry into my application easily. This sucks, so I decided to write a single-header OBJ loader in C (also probably close to C++ compatible, but I didn't check). It's not really complete (no material support yet), but does auto-triangulization, sub-models, (2/5)

**3/** **@rfleury** ^1144107249620672512

polygon groups, and works within a fixed-size parsing buffer. The high-level API that it provides (the LoadOBJ function) uses the CRT to load in the file and allocate a huge parsing buffer, but the lower level ParseOBJ function just works on the memory that is passed to it. (3/5)

**4/** **@rfleury** ^1144107250363117569

Documentation, bug fixes, and support will get better as I fix it up a bit, but here's a link to the WIP version for those interested:

https://gist.github.com/ryanfleury/0062f2ffdec07bcda8a4a0ef5c7f8f37

(4/5)

**5/** **@rfleury** ^1144107251134865408

Here's proof that it loads Sponza out of the box (with a lack of proper material support right now)!

(5/5)

![](https://pbs.twimg.com/media/D-CvSEKXUAAaWzD?format=jpg&name=orig)
