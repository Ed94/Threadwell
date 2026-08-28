---
title: "When Unity and Unreal package textures and generate mip maps, are the mip maps generated with the same 2x2 box filter that glGenerateMipmaps uses, or a high quality multi-tap resampling filter? Even a very costly resample should be cheaper than good GPU texture compression."
type: archive
source: twitter
source_url: "https://x.com/ID_AA_Carmack/status/1478077222841995265"
author: "John Carmack"
handle: ID_AA_Carmack
post_id: "1478077222841995265"
date: 2022-01-03
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - ID_AA_Carmack
description: "When Unity and Unreal package textures and generate mip maps, are the mip maps generated with the same 2x2 box filter that glGenerateMipmaps uses, or a high quality multi-tap resampling filter? Even a very costly resample should be cheaper than good GPU texture compression."
in_reply_to: ""
---

## Source

- URL: https://x.com/ID_AA_Carmack/status/1478077222841995265
- Author: John Carmack (@ID_AA_Carmack)
- Posted: 2022-01-03 18:54:05

## Thread

**1/** **@ID_AA_Carmack** ^1478077222841995265

When Unity and Unreal package textures and generate mip maps, are the mip maps generated with the same 2x2 box filter that glGenerateMipmaps uses, or a high quality multi-tap resampling filter? Even a very costly resample should be cheaper than good GPU texture compression.

**2/** **@cmuratori** ^1478450814838472707

**@ID_AA_Carmack**

Is there any way to use something other than a box filter and _not_ require trilinear filtering, though? The advantage of 2x2 box filtering MIPs is that for any 2D use (common in Unity), you no longer need trilinear filtering, because the transition is mathematically seamless.

**3/** **@ID_AA_Carmack** ^1478459632423161865

**@cmuratori**

What do you mean by 'mathematically seamless'? Any proper filter should be 'energy conserving', but the transition between mip levels, especially in 2D scaling, will always have a jarring pop without trilinear (which, unfortunately, is blending a too-blurry and a aliased image).

**4/** **@omershapira** ^1478464461388271622

**@ID_AA_Carmack** **@cmuratori**

I *think* what he means is a 2x2 box filter averages out the nyquist frequency, avoiding aliasing, so when zooming perpendicular to the image plane (“2D”), a realtime filtered pixel at the transition point will equal the prefiltered replacement.

**5/** **@ID_AA_Carmack** ^1478470219488190469

**@omershapira** **@cmuratori**

But that isn't what happens with bilinear-nearest filtering, because as soon as the step distance goes below 1 texel on either axis, it drops to the smaller mip level with a very obvious pop -- it avoids aliasing by being up to 2x blurrier (on each axis).

**6/** **@omershapira** ^1478473383364993025

**@ID_AA_Carmack** **@cmuratori**

define “below 1” :) The claim is that under a 2D axis-aligned zoom, *at* a distance of d=1, the box filter is the optimal (energy conserving) filtering, and when the sampler drops a mip level, it replaces the box-filtered 2x2 tile with the same precalculated value without a pop

**7/** **@omershapira** ^1478475334865633290

**@ID_AA_Carmack** **@cmuratori**

This is obviously not guaranteed to happen in practice (bilinear-nearest has a non-integer bias, and dxdy can be jittered), in which case a mip level will drop/rise and cause excessive filtering. Either way, I don’t consider being able to do it more than an anecdote.

**8/** **@cmuratori** ^1478505985878605824

**@omershapira** **@ID_AA_Carmack**

I actually wrote our 2D stuff this way, and unless I did something special that I don't remember doing, it "just works" and you can avoid trilinear everywhere - more importantly, you can _avoid having the other MIP resident_, which is important for low memory as well.

**9/** **@cmuratori** ^1478506351286358017

**@omershapira** **@ID_AA_Carmack**

I of course agree that for other scenarios you may prefer a sharpening filter instead and pay for the trilinear/aniso. But for a (wide) class of games, which are 2D, I would have to see more proof that a box filter isn't at least a reasonable choice.

**10/** **@cmuratori** ^1478506695781322753

**@omershapira** **@ID_AA_Carmack**

It is also important to recognize that many 2D sprites do not scale more than 4x in the first place, so the amount of improvement you get from a sharpening filter is further suspect. For certain art, maybe, but for a lot of art, the difference is negligible.
