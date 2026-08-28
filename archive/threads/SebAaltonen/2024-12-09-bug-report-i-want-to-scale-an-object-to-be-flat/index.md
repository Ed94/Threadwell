---
title: "Bug report: I want to scale an object to be flat."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1866131513852477814"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1866131513852477814"
date: 2024-12-09
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Bug report: I want to scale an object to be flat."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1866131513852477814
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2024-12-09 14:43:18

## Thread

**1/** **@SebAaltonen** ^1866131513852477814

Bug report: I want to scale an object to be flat. I set the X-axis scale to zero. Lighting breaks!

When the X-axis in the scale matrix is zero, that matrix can't be inverted. Divide by zero is not legal. So, we can't calculate the inverse-transpose matrix for normal transform.

**2/** **@BrookeHodgman** ^1866243051812954338

**@SebAaltonen**

When computing the normal-transformation matrix, you could detect this special case and emit a matrix that just results in 1,0,0,0 for all inputs 😎

**3/** **@SebAaltonen** ^1866270528694055205

**@BrookeHodgman**

Unfortunately a 3x3 matrix that does this doesn't exist. Also that's not correct either, you want either (-1,0,0) or (+1,0,0) output depending on which side the normal is.

**4/** **@EricLengyel** ^1866657604094833128

The 3x3 matrix you want does exist. It's got a one in the upper-left corner and zeros everywhere else. For an input normal of (x, y, z), the result will be (x, 0, 0), which will still point in the right direction. It just needs renormalized, which is to be expected.

**5/** **@BrookeHodgman** ^1866664013746102746

**@EricLengyel** **@SebAaltonen**

That can output 0,0,0 (and then normalise to NaN) for some inputs though, so isn't quite the same as above 😓

**6/** **@EricLengyel** ^1866668063334293551

It is provably the correct matrix to use for transforming normals when there's a zero scale in the x direction. Any surface having a normal with zero x component would no longer exist after the scale is applied, so a NaN normal actually makes sense and would only appear on degenerate triangles that get culled anyway. To avoid interpolating with a NaN normal at a vertex, the scale transform would need to be applied after interpolation occurs.

**7/** **@BrookeHodgman** ^1866670373972087037

**@EricLengyel** **@SebAaltonen**

Yeah it's correct in theory... But in practice (with interpolation like you mention or normal maps, etc) you often do see surfaces that have "wrong" normals so have to worry about handling those NaNs 😓
You don't want an unlucky normal map sample to result in a random black pixel

**8/** **@SebAaltonen** ^1866757644486414718

**@BrookeHodgman** **@EricLengyel**

Random NaN pixel would be even worse. It will propagate and ruin the whole image.

**9/** **@EricLengyel** ^1866767238734504032

**@SebAaltonen** **@BrookeHodgman**

A normal map would need to contain vectors tangent to the surface for this to happen. So just don’t allow it! It can’t occur if the normals are calculated from a height field anyway.

**10/** **@SebAaltonen** ^1866772316983578634

**@EricLengyel** **@BrookeHodgman**

You don't even need a normal map to see "backfacing" pixels. Interpolated normal makes it possible. Let's say you have a smoothed cube. Normal vectors on the same triangle have 90-degree angle between them. Let's say we are flattening such cube...

**11/** **@SebAaltonen** ^1866772609712656859

**@EricLengyel** **@BrookeHodgman**

If we flatten vertex normals, then we get triangles with (1,0,0) and (-1,0,0) normals and interpolating those will result in (0,0,0) in the midpoint. Cube could be slightly rotated so that these triangles are visible.

**12/** **@SebAaltonen** ^1866773052958142802

**@EricLengyel** **@BrookeHodgman**

If you flatten per pixel, then you will get a triangle that is facing (-1,0,0) halfway and facing (+1,0,0) halfway, and there's a possibility that the center pixel hits (0,0,0) exactly it's normal vector.x = 0.

**13/** **@SebAaltonen** ^1866773630199402991

**@EricLengyel** **@BrookeHodgman**

The same can happen in completely flat surfaces with normal map. The same slightly rotated cube, but with flat faces. Now the normal map makes some pixels have negative X normal (most are positive), and there can be some with normal.X=0, which causes problems.

**14/** **@SebAaltonen** ^1866774168869671329

**@EricLengyel** **@BrookeHodgman**

A simple example with planar surface. You have a normal map on the plane that has half-sphere bumps. If this surface is flattened in X direction, then bumps of course disappear, as bumps are flattened too. But if you rotate it slightly, then some of those bump pixels face -X.

**15/** **@SebAaltonen** ^1866774427310190975

**@EricLengyel** **@BrookeHodgman**

This kind of normal map

![](https://pbs.twimg.com/media/GegdbifW4AAeNfx?format=png&name=orig)

**16/** **@SebAaltonen** ^1866775636779655651

**@EricLengyel** **@BrookeHodgman**

The flattening matrix still works, but randomly some pixels have normal.x = 0 exactly, and those will have invalid normals after renormalize. Maybe we just nudge the math a bit to make them choose either +X or -X path.
