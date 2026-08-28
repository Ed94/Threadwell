---
title: "@EricLengyel My problem with the anti wedge product is that it needs an arbitrary pseudoscalar to be defined."
type: archive
source: twitter
source_url: "https://x.com/Atridas87/status/1209737702091956224"
author: "Atridas"
handle: Atridas87
post_id: "1209737702091956224"
date: 2019-12-25
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - EricLengyel
description: "@EricLengyel My problem with the anti wedge product is that it needs an arbitrary pseudoscalar to be defined."
in_reply_to: ""
parent_post_id: "1209615020947980288"
---

## Source

- URL: https://x.com/Atridas87/status/1209737702091956224
- Author: Atridas (@Atridas87)
- Posted: 2019-12-25 07:28:38

## Branch

**1/** **@Atridas87** ^1209737702091956224

**@EricLengyel**

My problem with the anti wedge product is that it needs an arbitrary pseudoscalar to be defined. It has a "handedness", while the contraction does not.

**2/** **@Atridas87** ^1209738708108414983

**@EricLengyel**

And dual quaternions: they are equivalent to rotors* in the conformal model. I won't say I understand them fully yet, but I've come close and I believe that to be the best path there.

*One with "only" rotation and translation.

**3/** **@EricLengyel** ^1209944360000712704

**@Atridas87**

That's the problem. Treating dual quaternions as if they're rotors is the reason why lots of things are backwards, and it's wrong. Twitter is not the proper place to elaborate.

**4/** **@Atridas87** ^1209949583842926593

**@EricLengyel**

Well, they perform two rotations: one around an arbitrary line in 3d space and a second around a line in the horizon perpendicular to that axis.

**5/** **@EricLengyel** ^1209962875814440961

**@Atridas87**

Rotors are composed of reflections through vectors, and as a result, can only rotate about the origin. What you're talking about is composed of reflections through *planes*, and that is what makes it possible to rotate about a line and perform translations in projective space.

**6/** **@EricLengyel** ^1209963383803367424

**@Atridas87**

This is the crux of the problem. Everyone makes dual quaternions by using the geometric product to concatenate two reflections through vectors. But what they really want is to use the *anti* geometric product to concatenate two reflections through antivectors.

**7/** **@Atridas87** ^1209964624281513984

**@EricLengyel**

When I come back to the problem I'll think about that.
In the conformal model you can decompose a translation to the reflection to a free vector + the reflection to the point at infinity. I don't know what neither of those means yet, so I'll 🤐

**8/** **@Atridas87** ^1209964899801145345

**@EricLengyel**

At the moment what I do is to interpret geometrically the logarithm of the rotor as the plane of rotation.

**9/** **@EricLengyel** ^1209942706077569024

**@Atridas87**

The antiwedge product is not a replacement for the contraction, which is an interior product. Contraction is an antiwedge product between one thing and the complement of another, and IMO, it makes more sense to look at it that way:

![](https://pbs.twimg.com/media/EMqUejIU8AAXSB1?format=png&name=orig)

**10/** **@Atridas87** ^1209948090024759298

**@EricLengyel**

In the algebra of subspaces, the wedge product does addition and the contraction substraction.
The antiwedge does the intersection if and only if the pseudoscalar is the union. To me, that's another category, less "fundamental", but useful nevertheless.

**11/** **@Atridas87** ^1209948875823472640

**@EricLengyel**

The antiwedge can be defined in terms of the wedge (the formula I learned from your book) or the contraction (the formula you just wrote rearranged).
It still needs an arbitrary pseudoscalar* that acts as a union of both blades to work.

*a blade actually works!

## Related

- Spine: [[archive/threads/EricLengyel/2019-12-24-1-8-every-operation-in-grassmann-geometric]]
