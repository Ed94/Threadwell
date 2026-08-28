---
title: "@EricLengyel So in the case of two vectors, the result of the geometric product would be a mixed grade bivector+scalar, right?"
type: archive
source: twitter
source_url: "https://x.com/NateMorrical/status/2019958137093284129"
author: "Nate Morrical"
handle: NateMorrical
post_id: "2019958137093284129"
date: 2026-02-07
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - EricLengyel
description: "@EricLengyel So in the case of two vectors, the result of the geometric product would be a mixed grade bivector+scalar, right?"
in_reply_to: ""
parent_post_id: "2019901780549861535"
---

## Source

- URL: https://x.com/NateMorrical/status/2019958137093284129
- Author: Nate Morrical (@NateMorrical)
- Posted: 2026-02-07 02:15:23

## Branch

**1/** **@NateMorrical** ^2019958137093284129

**@EricLengyel**

So in the case of two vectors, the result of the geometric product would be a mixed grade bivector+scalar, right?

I lack a good geometric intuition for the geometric product... Though I have had what appear like geometric products pop up in arithmetic from time to time.

**2/** **@EricLengyel** ^2019981553431113787

**@NateMorrical**

Yep! That’s what the last equation says.

**3/** **@NateMorrical** ^2020179654301347975

**@EricLengyel**

Currently this equation appears like a pointless coroutine.

I could invent a seemingly equally useful "geometric division" operator which returns (a \wedge b) + (a • b)^{-1}. 

Surely there's more to the geometric product than just a shorthand convenience?

**4/** **@NateMorrical** ^2020183354373746849

**@EricLengyel**

I'm poking at this because they almost look like homogeneous magnitudes.

If the left wedge was replaced with a weight expansion, and the right stays a bulk contraction, then I can implement a ray-plane intersection t with it that seems to preserve front / back face information.

**5/** **@EricLengyel** ^2020205603013161098

**@NateMorrical**

I'm not aware of any connection there. But I will note that the antiwedge product g ∨ l between a plane and a line gives you an intersection point for which the sign of the e₄ component tells you whether the ray hit the front or back of the plane.

**6/** **@NateMorrical** ^2020280784154952136

**@EricLengyel**

The idea here is related. 

If you take a ray r = [e1,e2,e3 | e4, e423, e431, e412] to be a mixed grade origin + antivector "direction" object, then g∨r + g∧r gives a homogeneous magnitude which once unitized appears like a ray-plane intersection t.

**7/** **@NateMorrical** ^2020281726392741902

**@EricLengyel**

The object r can be made an "anti-r" of sorts such that the plane measures the origin as a numerator and the rays direction measures the plane as a denominator. 

It simplifies to an addition between a dot and an antidot, which reminded me a bit of the geometric product.

**8/** **@EricLengyel** ^2020285746033381650

**@NateMorrical**

But g ∨ r contains both scalar and bivector parts.

**9/** **@NateMorrical** ^2020340030900965660

**@EricLengyel**

Sorry, I meant g∨(r_\bulk) + g∧(r_\weight). 

This is assuming a projective metric/antimetric. Relating back to bulk contractions / weight expansions.

**10/** **@NateMorrical** ^2020368563534725193

**@EricLengyel**

In retrospect there's a bit more nuance to it. 

Linalg ray vs plane t = -(g.n • r.o + g.d)/(r.ω•g.n)=(g.n • r.o)/(r.ω•g.n)+(g.d•r.w)/(r.ω•g.n)

Ie a sum of two inner products followed by a signed unitization.

In PGA, dual t = g•r / g°r + g°r/g°r = ± ||g•r + g°r||

**11/** **@NateMorrical** ^2020372185786057057

**@EricLengyel**

g•r=g∨𝕣^☆=g∨[e321|e423,e431,e412]^☆=-g∨[e1,e2,e3|e4]
g°r=g∧𝕣^★=g∧[e1,e2,e3]^★=g∧[0|e423,e431,e412]

So ||g•r + g°r|| = || g∨𝕣^☆ + g∧𝕣^★||

(Assuming I have that all right ...)

**12/** **@NateMorrical** ^2020373138639581327

**@EricLengyel**

From here I used symmetry between expansions and contractions to simplify. Twitter's char limit isn't great for writing that out.

TLDR, I was seeing this "sum of two inner products, then project" pattern, which reminded me of the geometric product.

**13/** **@NateMorrical** ^2020598208179970199

**@EricLengyel**

Revisiting this idea this morning, I believe this is another flaw in my logic:

g•𝕣 = g⊺𝐆𝕣 ≠ g∨𝕣^★. The inner product filters out off-diagonal terms from the interior product.

So g•r = 0, because 𝐆 filters out all but e1,e2,e3, and g has none of these.

**14/** **@EricLengyel** ^2020741046381187537

Yeah, the dot product between two things of different grades is always zero. I don't think the formulation of a "ray" that you're using is the right approach. Normally, you'd just intersect a line and a plane, and the e₄ component of the resulting point ends up being the value you need to divide by.

**15/** **@NateMorrical** ^2020882239572357358

**@EricLengyel**

This increases arithmetic complexity converting the ray to plucker coordinates.

Conventionally we dot the origin with the plane, then divide by the dot between the direction and the plane.

**16/** **@NateMorrical** ^2020884910278574565

**@EricLengyel**

By using the first and third blocks of the metric, this seems to avoid increasing arithmetic. But it's not elegant. 

The "plane" must become mixed grade iiic, so the ray origin/direction pairs with seven unique "plane" bases. 

This is what we do in real RT code. t=(o•g)/(d•g)

**17/** **@NateMorrical** ^2020888592957198742

**@EricLengyel**

I understand the philosophy of PGA isn't necessarily about compute performance. 

But it's a real reason I can't use it in practice. I usually can't afford it.

**18/** **@EricLengyel** ^2020940405043495372

I understand where you're coming from, and in the case of a ray intersecting a single plane, it's probably best to just stick with a point and direction instead of combining them into a line. If you did make a line, I think the final calculation would simplify to the same thing if you expressed the line in terms of the point and direction that made it. Performance is important, and that's why I point out that GA is slower than conventional methods at several places in my book.

**19/** **@NateMorrical** ^2030131930029773034

**@EricLengyel**

Gave this another go today. 

Let a ray r = o+v, where o is the origin as a point and v is the direction as a zero-offset trivector. Then g to be a plane.

Then o = ½(r+r̃) and v = ½(r-r̃).

So s = g∧½(r+r̃) + g◦½(r-r̃) and the intersection between r and g is t = (s_•)/(s_◦)

**20/** **@NateMorrical** ^2030133863201263696

**@EricLengyel**

Err, s = g∨½(r+r̃) + g◦½(r-r̃)

First term is a scalar where origin meets plane. Second is antiscalar where the dual of the direction joins the plane.

The ½ can be dropped as it's a common constant to both sides.

g∨(r+r̃) + g◦(r-r̃) is what made me go "geometric product?"

**21/** **@EricLengyel** ^2030532837095670099

**@NateMorrical**

Since the antiwedge product and antidot product are being taken with different values, I don't think there's a connection with the geometric antiproduct.

**22/** **@NateMorrical** ^2031159959019516382

**@EricLengyel**

Iiic, a geo product decomposes vector multiplication into a projection plus a rejection.

The scalar here is the projection of the origin onto the plane.

The antiscalar seems a bit like +/- rejection of the direction.

So it still seems related to me, if only indirectly.

## Related

- Spine: [[archive/threads/EricLengyel/2026-02-06-when-a-is-a-vector-and-b-is-any-multivector-the]]
