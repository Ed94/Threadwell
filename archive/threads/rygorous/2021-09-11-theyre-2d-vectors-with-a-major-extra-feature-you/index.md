---
title: "@ladyaeva They're 2D vectors with a major extra feature: you can multiply two vectors to get a third, and this multiplication is just like multiplication in the reals: it's commutative (a*b=b*a), invertible unless you're multiplying by 0, and also has a nice geometric interpretation."
type: archive
source: twitter
source_url: "https://x.com/rygorous/status/1436788358768828417"
author: "Fabian Giesen"
handle: rygorous
post_id: "1436788358768828417"
date: 2021-09-11
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - rygorous
description: "@ladyaeva They're 2D vectors with a major extra feature: you can multiply two vectors to get a third, and this multiplication is just like multiplication in the reals: it's commutative (a*b=b*a), invertible unless you're multiplying by 0, and also has a nice geometric interpretation."
in_reply_to: "1436618444477190148"
---

## Source

- URL: https://x.com/rygorous/status/1436788358768828417
- Author: Fabian Giesen (@rygorous)
- Posted: 2021-09-11 20:26:53

## Thread

**1/** **@rygorous** ^1436788358768828417

**@ladyaeva**

They're 2D vectors with a major extra feature: you can multiply two vectors to get a third, and this multiplication is just like multiplication in the reals: it's commutative (a*b=b*a), invertible unless you're multiplying by 0, and also has a nice geometric interpretation.

**2/** **@rygorous** ^1436789164813402113

**@ladyaeva**

This is the part that makes them special; you can get real vector spaces in any dimension, but spaces where you can also define a nice product are hard to come by.

**3/** **@rygorous** ^1436789973630390274

**@ladyaeva**

There's nothing nice for 3D, for example. You can take  the cross product, which is vector*vector -> vector (so right "types" at least), but a x b =- b x a so it's anti-commutative, and in particular a x a = 0 for any a so it's also not invertible.

**4/** **@EricLengyel** ^1437160350961438723

**@rygorous** **@ladyaeva**

The incorrect belief that vector × vector -> vector, that the result of a cross product has the same type as its operands, is the source of over a century of misunderstanding and incomplete mathematics.

**5/** **@EricLengyel** ^1437160587016892416

**@rygorous** **@ladyaeva**

You can try to stuff its three components into the same type as a vector, but you can't escape the fact that the result of a cross product has different properties.

**6/** **@rygorous** ^1437173844716834820

**@EricLengyel** **@ladyaeva**

_This_ of all places is the thread (see https://x.com/ladyaeva/status/1436763466619097099) where you decide to parachute in with your pet peeve about how cross products are wrong, actually? Come on.

**7/** **@rygorous** ^1437174450911285248

**@EricLengyel** **@ladyaeva**

Yes, bivectors are a better way to understand this, but cross products are everywhere, be it textbooks, tutorials, papers or classes, and "um actually you're doing it wrong" is not the way to rectify that situation.

**8/** **@ZPostFacto** ^1437186294400962560

**@rygorous** **@EricLengyel** **@ladyaeva**

"Wrong" seems to me to be drastically overstating the case.  "Incomplete" maybe.

I feel the same way on this stuff as I do about Hamiltonian mechanics.  It's more elegant in a certain sense, perhaps it is accessing some deeper truth (?).  And yet is is undeniably less intuitive.

**9/** **@ZPostFacto** ^1437187241265164293

**@rygorous** **@EricLengyel** **@ladyaeva**

Intuitiveness has real value; it's not clear to me that teaching things in a more elegant but less intuitive manner is the correct tradeoff, for most people.

Even though I think the Deeper Ways are interesting & valuable.

There are only so many hours in the day to learn stuff.

**10/** **@EricLengyel** ^1437223683089518592

**@ZPostFacto** **@rygorous** **@ladyaeva**

So a question on my mind is whether someone who was never taught that vector × vector = vector would still find it less intuitive to learn that more things than just scalars and vectors exist, and vector × vector = bivector. (That's what you're getting at, right?)

**11/** **@EricLengyel** ^1437224384360431617

**@ZPostFacto** **@rygorous** **@ladyaeva**

Would somebody who was taught the graded exterior algebra with wedge and antiwedge products from the beginning, only later being exposed to the cross product, find the cross product to be an unintuitive hack?

**12/** **@ZPostFacto** ^1437231042734137349

**@EricLengyel** **@rygorous** **@ladyaeva**

I think I has to do with how concrete the concepts are.

E.g. in both Lagrangian and Hamiltonian dynamics, energy plays a central role.  It's just a much more abstract quantity than force.

"Vector perpendicular to the argument vectors" is a very concrete thing.

**13/** **@ZPostFacto** ^1437231332170428416

**@EricLengyel** **@rygorous** **@ladyaeva**

And I think good pedagogy always goes from concrete to abstract, and from specific to general.

**14/** **@ZPostFacto** ^1437232576322629637

**@EricLengyel** **@rygorous** **@ladyaeva**

So if somebody had always been taught the more abstract way from the beginning, yeah they might find it intuitive.  But imo that's basically just a bad way to teach.  It asks people to leap across a big conceptual chasm.  Many won't make it.  And most don't need it.

**15/** **@rygorous** ^1437237573995282435

**@ZPostFacto** **@EricLengyel**

The way I view it is that certainly in programming and engineering, most people are consumers not producers of math. When they have a problem, they look up a formula (or go on StackOverflow), maybe massage it a bit with some algebra, and plug their numbers in. That's it.

**16/** **@rygorous** ^1437238342026809345

**@ZPostFacto** **@EricLengyel**

"I don't actually know how this really works under the hood and I don't care as long as it does" is totally valid. E.g. there's lots of people who learn the Z-transform by rote, know how to work with, know nothing about formal power series or complex analysis, and don't ned to.

**17/** **@rygorous** ^1437238864498757633

**@ZPostFacto** **@EricLengyel**

"You're not understanding this right" is less than useless when you're in that position. Indeed I don't understand this right, I don't understand it at all, but I should still be able to function within it.

**18/** **@rygorous** ^1437239562615463939

**@ZPostFacto** **@EricLengyel**

For better or for worse, and for all the conceptual baggage they come with, cross products are everywhere, and they're treated as vectors. You're going to find them in textbooks, formula collections, as ∇ ×, in the code you got from SO to set up a look-at matrix, everywhere.

**19/** **@rygorous** ^1437239917600395267

**@ZPostFacto** **@EricLengyel**

The world you live in doesn't have everything stated as blades. You don't get around knowing what × is or how it works, even when you don't agree with it.

**20/** **@rygorous** ^1437240600604991488

**@ZPostFacto** **@EricLengyel**

If you don't particularly care about the theory, couldn't care less about whether it's beautiful or elegant or not, but do want to just grab code or formulas and have them work, GA does very little for you and mostly places extra barriers between you and getting what you want.

**21/** **@EricLengyel** ^1437260942908092416

**@rygorous** **@ZPostFacto**

I disagree, mostly. In my experience, specific parts of GA are extremely practical in 3D apps. I use them like crazy for common calculations that would otherwise be more complex / obfuscated. However, I agree that some other parts gain you very little and could even hurt.

**22/** **@EricLengyel** ^1437261490155753477

**@rygorous** **@ZPostFacto**

In my opinion, *almost all* of the existing learning resources for GA are terrible, focus on the wrong things, and are written by people who don't have a full grasp of it. I'm in the midst of trying to change this by providing the big picture and approaching GA with pragmatism.
