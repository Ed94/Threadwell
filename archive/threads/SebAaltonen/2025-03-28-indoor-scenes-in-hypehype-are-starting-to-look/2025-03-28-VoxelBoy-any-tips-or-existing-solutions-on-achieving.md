---
title: "@SebAaltonen Any tips or existing solutions on achieving something similar in Unity? (in terms of indoor lighting)"
type: archive
source: twitter
source_url: "https://x.com/VoxelBoy/status/1905551799790006590"
author: "Yilmaz Kiymaz"
handle: VoxelBoy
post_id: "1905551799790006590"
date: 2025-03-28
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen Any tips or existing solutions on achieving something similar in Unity? (in terms of indoor lighting)"
in_reply_to: ""
parent_post_id: "1905523331496828964"
---

## Source

- URL: https://x.com/VoxelBoy/status/1905551799790006590
- Author: Yilmaz Kiymaz (@VoxelBoy)
- Posted: 2025-03-28 09:25:27

## Branch

**1/** **@VoxelBoy** ^1905551799790006590

**@SebAaltonen**

Any tips or existing solutions on achieving something similar in Unity? (in terms of indoor lighting)

**2/** **@BenSimsTech** ^1905565847059661090

**@VoxelBoy** **@SebAaltonen**

In Unity I do it this way: Custom EnvProbe component, capture gbuffer albedo normal and depth into cubemap on load. Pick 1 probe per frame and relight similar to deferred lighting using current sun/sky etc. Convolve to SH for diffuse and GGX for spec. Combine during deferred pass

**3/** **@BenSimsTech** ^1905566465274892341

**@VoxelBoy** **@SebAaltonen**

This is a custom pipeline though. You'll need a decent amount of graphics code/shaders to get it working, will be very hard to retrofit into HDRP, might be feasible in URP/BiRP. I'm still working on it, may switch to octmaps instead of cubemaps. Unity is still very behind with GI

**4/** **@VoxelBoy** ^1905573689317339393

**@BenSimsTech** **@SebAaltonen**

Also, with your custom render pipeline, how easy would you say it is to exceed URP performance if what’s being used are the most basic features such as Lit shader + lightmaps? Is there a lot of cruft in URP that causes overhead in your opinion?

**5/** **@BenSimsTech** ^1905585393078251755

**@VoxelBoy** **@SebAaltonen**

URP is reasonably lightweight, depends what you're targeting though. For low-end mobile/mobile VR there's a few uneccessary copies/blits etc for things like color grading, depth reads, MSAA resolves etc. Lights are only culled on per-object basis which can waste performance too.

**6/** **@Alecazam123** ^1905622046685757524

**@BenSimsTech** **@VoxelBoy** **@SebAaltonen**

I don’t think msaa is worth it on TBDR.  Too much bandwidth shuffling tiles on/off.  And avoiding swapping out say depth is tough.

**7/** **@NOTimothyLottes** ^1905628963482825079

**@Alecazam123** **@BenSimsTech** **@VoxelBoy** **@SebAaltonen**

MSAA+tiler makes sense if no post, assuming one does inline 4 sample tonemap before box summation (HW resolve). Have to super sample alpha test and set coverage mask, and super-sample depth for soft particle blend. Neither should require depth export if HW is good

**8/** **@Alecazam123** ^1905629412651139223

**@NOTimothyLottes** **@BenSimsTech** **@VoxelBoy** **@SebAaltonen**

Gpu occlusion needs hierZ.  Just not worth it IMHO.

**9/** **@NOTimothyLottes** ^1905637476334469247

**@Alecazam123** **@BenSimsTech** **@VoxelBoy** **@SebAaltonen**

Good HW in theory with wave ops on a full-screen triangle could read the MSAA depth and do an inline down-sample for the wave tile without ever needing to export MSAA depth, hierZ done with last frame's reduced depth and speculation should work for HZB occlusion

**10/** **@NOTimothyLottes** ^1905638036160811329

**@Alecazam123** **@BenSimsTech** **@VoxelBoy** **@SebAaltonen**

On a tiler you don't do mid-frame readback feeding any kind of geometry because the tiler geo passes are too latent (do all VS for the view for tile chunking, then PS)

**11/** **@NOTimothyLottes** ^1905638813818372537

**@Alecazam123** **@BenSimsTech** **@VoxelBoy** **@SebAaltonen**

The MSAA alternative I was pushing for at Unity for "general purpose" deferred g-buffer stuff was 1:2x2 nearest scaling mixed with 8x area STP (scaling-TAA), and hopefully eventually CS based index culling (to keep triangle, and thus chucker DRAM round trip bandwidth low)

**12/** **@Alecazam123** ^1905640027402764799

**@NOTimothyLottes** **@BenSimsTech** **@VoxelBoy** **@SebAaltonen**

Still a lot of limitations on depth/stencil and color msaa resolves and iOS.  Hw only has it all around A13.  Nice sample shaders for tonemap prior to resolve.   Still think TAA is the most flexible/affordable.   Plus msaa lowers tile size from 32x32@1x to 16x16@4x.

**13/** **@NOTimothyLottes** ^1905642771387457570

**@Alecazam123** **@BenSimsTech** **@VoxelBoy** **@SebAaltonen**

MSAA/TAA doesn't change the problem with mid-frame CPU read back. Id still probably go with a mix of vintage precomputed clustered visibility (ratchet and clank style) and model LOD for the static geo of a tri based mobile engine

## Related

- Spine: [[archive/threads/SebAaltonen/2025-03-28-indoor-scenes-in-hypehype-are-starting-to-look]]
