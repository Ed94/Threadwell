---
title: "I've long time talked about killing the graphics API."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1595091915472764928"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1595091915472764928"
date: 2022-11-22
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "I've long time talked about killing the graphics API."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1595091915472764928
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2022-11-22 16:28:42

## Thread

**1/** **@SebAaltonen** ^1595091915472764928

I've long time talked about killing the graphics API. First step: Kill descriptor APIs. Descriptors are just memory, you can put them in buffers, load them in shader and copy/update them in GPU timeline.

This new Khronos extension does exactly that:
https://www.khronos.org/blog/vk-ext-descriptor-buffer

Branches: [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics/2022-11-22-SebAaltonen-hopefully-in-the-future-the-existing-vulkan]], [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics/2022-11-22-PLT_cheater-killing-the-graphics-api-what-does-that-mean-how]], [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics/2022-11-22-danoli3-hooley-dooley]], [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics/2022-11-22-vingt_2-yes-please]], [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics/2022-11-22-AlenL-few-more-decades-and-will-finally-be-back-to]], [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics/2022-11-23-zhaijialong-this-extension-still-lacks-the-ability-to-create]], [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics/2022-11-23-ThisIsJBernard-finally-was-waiting-on-this-one-now-just-want]], [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics/2022-11-23-Venemo-afaik-that-is-only-fully-true-on-amd-gpus]], [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics/2022-11-23-JoaoBapt-one-of-the-biggest-roadblocks-when-i-was-trying]], [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics/2022-11-23-RandomPedroJ-when-i-started-with-modern-graphics-apis-i-e]], [[archive/threads/SebAaltonen/2022-11-22-ive-long-time-talked-about-killing-the-graphics/2022-11-23-SvetlinTotev-another-vulkan-w]]

**2/** **@NOTimothyLottes** ^1595158732706811905

**@SebAaltonen**

Yes, closer to what many of us wanted from VK from the beginning. Article missed this: DYNAMIC on AMD at least was good because it can be SGPR preload (removes an indirection at runtime).

**3/** **@NOTimothyLottes** ^1595159948669104128

**@SebAaltonen**

Unfortunatly though I'd expect some are going to abuse the API: use max descriptor size for everything all in one giant array. Will kill cache efficiency. Not sure if this new API supports the alternatives to fix that.

**4/** **@rianflo** ^1595161710905929728

**@NOTimothyLottes** **@SebAaltonen**

I am using VK_KHR_push_descriptor for now.
