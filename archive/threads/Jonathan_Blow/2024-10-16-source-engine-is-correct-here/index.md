---
title: "Source engine is correct here."
type: archive
source: twitter
source_url: "https://x.com/Jonathan_Blow/status/1846414645340389700"
author: "Jonathan Blow"
handle: Jonathan_Blow
post_id: "1846414645340389700"
date: 2024-10-16
archived: 2026-09-08
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "Source engine is correct here."
in_reply_to: ""
---

## Source

- URL: https://x.com/Jonathan_Blow/status/1846414645340389700
- Author: Jonathan Blow (@Jonathan_Blow)
- Posted: 2024-10-16 04:55:30

## Thread

**1/** **@Jonathan_Blow** ^1846414645340389700

Source engine is correct here. (Same coordinates I use... there are Reasons!)

https://x.com/FreyaHolmer/status/1846322053760033220

**2/** **@Jonathan_Blow** ^1846422137138970912

Since people are asking about the reasons...

For one, the convention is that increasing angle makes a point or vector go around counterclockwise (via cos/sin). This means that 2D is inherently right-handed unless you want to rewrite all your trig functions. Also a right-handed XY plane is what everyone learned in school, which is great. As you keep adding dimensions, it makes sense to keep the same handedness of space. If adding Z suddenly makes things flip left-handed, what happens when you add W -- does it stay left-handed or do you flip it again? Why? 

If your spaces are completely the same handedness as you generalize and keep adding dimensions, then any two basis vectors are always the same handedness with respect to each other. If some spaces are opposite handedness of others, then you don't know!

With regard to what direction is forward, it again helps to think about generalizing to any number of dimensions. If you are in a 1-dimensional space, that dimension is the forward dimension. It doesn't make sense to even have concepts like left/right or up/down until you have more dimensions. So the forward direction is what you have when you perform no transform on the first vector in your basis.

Annoyingly of course, screenspace pixels in most operating systems are left-handed and uv texture space in most file and memory formats is left-handed because of this, which means you have to convert when you reference these things. (But it's not that everything is arbitrary and these things are "just as right" as you ... if you call cos,sin on an increasing angle and map it naively to screen pixels, it comes out backwards! Screen pixels are wrong given the math functions that we have!)

The conventions that have +Z or -Z as forward are confusing; they are trying to be intuitive because hey, screen X and Y go in certain directions, just add Z to that, but this does not extend to further dimensions and to non-graphics applications, whereas the philosophy I discussed above maps to *any* geometric problem in *any* number of dimensions. It is really screwed up when you are trying to do IK in an arbitrary object space and -Z is forward for some bizarre reason (as people who interface with busted-ass old modeling and animation tools have long had to put up with).

I often tend to follow the Geometric Algebra convention of naming my dimensions e1, e2, e3, ... instead of x, y, z, ... because this way you never run out of dimensions and you are never confused about which ones are in which order. Every combinatoric subspace of any of these e_n is right-handed and it's all very simple.

**3/** **@Jonathan_Blow** ^1846424206541566158

(in b4 someone claims that the results of cos,sin are just numbers and the mapping to right or left-handed rotation is arbitrary. Yeah in theory, but everyone expects these to go counterclockwise and you'll get really really confused if you decide to flip this sometimes and not other times.)

**4/** **@cmuratori** ^1846442818388349254

Also, if cosine and sine are "just numbers", you also wouldn't care about handedness, or where your axes point, because it's all arbitrary. So the point is if you are going to have a convention, you should pick one with the least surprise for people using standard functions.

**5/** **@marc_b_reynolds** ^1846446321990853117

**@cmuratori** **@Jonathan_Blow**

Another perspective is if you start with the 2D convention of positive X to right and positive Y is up then the standard convention directly falls out.  Even ignoring how trig functions were defined.  (Specifically from parallel and orthogonal projections)

**6/** **@cmuratori** ^1846463818911883359

**@marc_b_reynolds** **@Jonathan_Blow**

That is how I usually think about it myself. The "identity matrix camera" has to produce the standard math coordinate system, and then I derive everything else from that.

**7/** **@Huitzlopochtll** ^1846685927521112186

**@cmuratori** **@marc_b_reynolds** **@Jonathan_Blow**

maybe I misunderstand, but doesn't starting with the convention of x right and y up, result in z forwards, which is not the source engine way? or would it have to change for 3d? or do you think z forwards is better than x forwards?

**8/** **@marc_b_reynolds** ^1846781825915511243

**@Huitziofpain** **@cmuratori** **@Jonathan_Blow**

I was talking about so-called right-handed where positive angles are counter-clockwise in the plane.
