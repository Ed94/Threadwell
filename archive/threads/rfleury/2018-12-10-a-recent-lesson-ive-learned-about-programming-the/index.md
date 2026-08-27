---
title: "A recent lesson I've learned about #programming the hard way: Be *very* skeptical of mental models."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1072013399926616065"
author: "Ryan Fleury"
handle: rfleury
post_id: "1072013399926616065"
date: 2018-12-10
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "A recent lesson I've learned about #programming the hard way: Be *very* skeptical of mental models."
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/1072013399926616065
- Author: Ryan Fleury (@rfleury)
- Posted: 2018-12-10 06:21:26

## Thread

**1/** **@rfleury** ^1072013399926616065

A recent lesson I've learned about #programming the hard way: Be *very* skeptical of mental models. 1/7

**2/** **@rfleury** ^1072013400673140736

I had been building The Melodist's editor with the unconsciously-made assumption that the map editor should be working on the same entity data structures that the game does, simply because entities in the editor/game represent the same thing conceptually. 2/7

**3/** **@rfleury** ^1072013401558212610

However, the editor requires a much different set of functionality than the game, and it requires different data, different serializability, and different data transformations. 3/7

**4/** **@rfleury** ^1072013402527035392

After realizing this and splitting the problem into two, both problems became far simpler, and some features that would be extremely difficult to produce in the previous system became trivial. It all started with thinking about the *problem*, not the *mental model*. 4/7

**5/** **@rfleury** ^1072013403449769984

The statement "Think about the real, physical problem, not the mental model" is undoubtedly one I would have agreed with for at least a few years, but this problem proved that such a method of thinking doesn't happen automatically. 5/7

**6/** **@rfleury** ^1072013404330582016

Through this, I've learned to always try to critically think about the way I am thinking about a problem, instead of pretending that my mental model's perception of the problem *is* the problem. It isn't. 6/7

**7/** **@rfleury** ^1072013405232361473

Following from this, I claim that any particular programming ideology that encourages you to reason about the problem *through* your mental model is just no good, and doesn't help you write good software. 7/7
