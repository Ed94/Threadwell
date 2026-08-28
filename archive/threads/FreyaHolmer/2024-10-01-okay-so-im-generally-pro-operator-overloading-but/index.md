---
title: "okay so I'm generally pro-operator-overloading but even I will admit it's a little silly that m*(q*v) can be a matrix multiplied by the result of a quaternion rotation of a vector v interpreted as a column vector"
type: archive
source: twitter
source_url: "https://x.com/FreyaHolmer/status/1841087879759495670"
author: "Freya Holmér"
handle: FreyaHolmer
post_id: "1841087879759495670"
date: 2024-10-01
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - FreyaHolmer
description: "okay so I'm generally pro-operator-overloading but even I will admit it's a little silly that m*(q*v) can be a matrix multiplied by the result of a quaternion rotation of a vector v interpreted as a column vector"
in_reply_to: ""
---

## Source

- URL: https://x.com/FreyaHolmer/status/1841087879759495670
- Author: Freya Holmér (@FreyaHolmer)
- Posted: 2024-10-01 12:08:50

## Thread

**1/** **@FreyaHolmer** ^1841087879759495670

okay so I'm generally pro-operator-overloading but even I will admit it's a little silly that m*(q*v) can be a matrix multiplied by the result of a quaternion rotation of a vector v interpreted as a column vector

**2/** **@FreyaHolmer** ^1841087881542091238

I think q*v is the most egregious one, because it's decidedly NOT what is happening math side

it's more like
★(q(★v)q*)

where ★ is the hodge dual, swapping the {x,y,z} basis with a {yz,zx,xy} basis, and * is the conjugate, negating the bivector part

**3/** **@EricLengyel** ^1841213433976668166

**@FreyaHolmer**

Why the Hodge dual here?

**4/** **@Chrispykins** ^1841221790661820676

**@EricLengyel** **@FreyaHolmer**

v is a real vector. Typically when encoding a real vector as a quat, you turn the real components into imaginary components and leave the scalar part 0.

The imaginary components are isomorphic to bivectors in R³, so the ★ changes the vector components into bivector components.

**5/** **@EricLengyel** ^1841225875494486260

That's not necessary. The product qvq* correctly transforms any vector v, and the product qbq* correctly transforms any bivector b. Since we're talking about {x,y,z} and {yz,zx,xy} bases and vectors/bivectors here, we're clearly aware of the larger exterior algebra and the geometric product, and not just the quaternion product, so there's no reason to take complements to convert vectors to/from bivectors.

**6/** **@FreyaHolmer** ^1841254247888793699

**@EricLengyel** **@Chrispykins**

oh wait is ★(q(★v)q*) the same as qvq*, even if we assume only the geometric product as the one canonical product?

I kind of just assumed they were different, since q(★v) is in the even subalgebra, while qv is in the odd subalgebra with a vector and trivector part, I think

**7/** **@EricLengyel** ^1841261355585913075

**@FreyaHolmer** **@Chrispykins**

Yes, qvq* and ★(q(★v)q*) produce the same answer under the geometric product. This is true because q corresponds to an orthogonal transformation, and thus vectors and antivectors (bivectors in 3D) transform identically.

**8/** **@EricLengyel** ^1841261454298845644

**@FreyaHolmer** **@Chrispykins**

q(★v) has a bivector part and a scalar part, and qv has a vector part and a trivector part. They're just complements of each other such that ★(qv) = q(★v), and the component values are the same.

**9/** **@FreyaHolmer** ^1841261925596111047

**@EricLengyel** **@Chrispykins**

ah neat, I didn't know that! I never even thought to test it, thanks c:

**10/** **@EricLengyel** ^1841267369647485057

Btw, in the ordinary 3D algebra that we're talking about right now, the Hodge dual and complement are equivalent, and they are each their own inverses. But be aware that the equivalence doesn't hold in algebras where the metric is not the identity matrix, and their inverses have grade-dependent sign changes in even numbers of dimensions. The Hodge dual doesn't even have an inverse in PGA due to the degenerate metric, so you'd have to use complements in your original formula instead, which technically ought to say ★⁻¹(q(★v)q*). The Hodge dual is one of four related duals described in my book, and it's equivalent to what I call the "right bulk dual" (with the other three being the "left bulk dual", the "right weight dual", and the "left weight dual"). </rambling>
