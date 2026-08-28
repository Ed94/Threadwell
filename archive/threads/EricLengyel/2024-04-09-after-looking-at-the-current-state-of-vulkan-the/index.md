---
title: "After looking at the current state of Vulkan (the API, driver support, stability, etc.), I have concluded that I'm better off sticking with OpenGL for the time being when it comes to making a PC game."
type: archive
source: twitter
source_url: "https://x.com/EricLengyel/status/1777833385676968429"
author: "Eric Lengyel"
handle: EricLengyel
post_id: "1777833385676968429"
date: 2024-04-09
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - EricLengyel
description: "After looking at the current state of Vulkan (the API, driver support, stability, etc.), I have concluded that I'm better off sticking with OpenGL for the time being when it comes to making a PC game."
in_reply_to: ""
---

## Source

- URL: https://x.com/EricLengyel/status/1777833385676968429
- Author: Eric Lengyel (@EricLengyel)
- Posted: 2024-04-09 22:58:04

## Thread

**1/** **@EricLengyel** ^1777833385676968429

After looking at the current state of Vulkan (the API, driver support, stability, etc.), I have concluded that I'm better off sticking with OpenGL for the time being when it comes to making a PC game.

**2/** **@SebAaltonen** ^1777950713215324609

**@EricLengyel**

Vulkan has extremely good documentation. I haven't found any stability issues on PC either. But it's critical to use validation layer during development and enable sync validation too. Otherwise you end up doing bad stuff by accident crashing the drivers easily.

**3/** **@SebAaltonen** ^1777951183065190794

**@EricLengyel**

Unless you are targeting very old Intel iGPUs, there shouldn't be driver issues on PC either. Android is of course a completely different ballgame. If you need to target Android 8 or earlier, then Vulkan is a bad idea.

**4/** **@EricLengyel** ^1777953111933604051

**@SebAaltonen**

With Vulkan, I would be targeting Windows PC only with a min GPU around GF 1060.

One thing turning me off right now is lack of AMD support for VK_EXT_shader_object. (Has this changed?)

I saw a couple problems with Vulkan on Intel ARC hardware, but that was a couple years ago.

**5/** **@SebAaltonen** ^1777954235725795328

**@EricLengyel**

Since we are developing for Android, I wouldn't even dream about fancy extensions like VK_EXT_shader_object. Stock Vulkan 1.1 is the best you can do on Android.  

Why do you need that extension? Something you can't do without it?

**6/** **@EricLengyel** ^1777954857997234610

**@SebAaltonen**

I can get by without that extension, but it would make things a lot easier for me. I would definitely be using dynamic rendering to its fullest because that's how the hardware actually works (and I have a lot of state combinations that are not known up front).

**7/** **@SebAaltonen** ^1777955612309049782

**@EricLengyel**

Vulkan 1.3 is widely used on PC and it adds a lot of dynamic state. Much better than 1.1 in that regard. But Vulkan 1.3 support on Android is still too small for shipping.

**8/** **@SebAaltonen** ^1777956086215008627

**@EricLengyel**

Pre-1.3 Vulkan is PITA for PSO management, since all render state is practically inside the PSO. Except viewport rectangle and stencil rectangle. Those support dynamic state even in 1.0.

**9/** **@EricLengyel** ^1777960415907217696

**@SebAaltonen**

You're talking to the guy who made those dynamic in 1.0. (You mean viewport and scissor rectangles.)

**10/** **@tloch14** ^1778014039571869800

**@EricLengyel** **@SebAaltonen**

I want to hear that story.
