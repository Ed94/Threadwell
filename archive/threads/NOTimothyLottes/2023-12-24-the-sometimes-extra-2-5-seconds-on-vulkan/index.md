---
title: "The sometimes extra ~2.5 seconds on Vulkan initialization on my win10 AMD laptop is in vkCreateInstance()."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1738941410676547997"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1738941410676547997"
date: 2023-12-24
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "The sometimes extra ~2.5 seconds on Vulkan initialization on my win10 AMD laptop is in vkCreateInstance()."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1738941410676547997
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-12-24 15:15:14

## Thread

**1/** **@NOTimothyLottes** ^1738941410676547997

The sometimes extra ~2.5 seconds on Vulkan initialization on my win10 AMD laptop is in vkCreateInstance(). Dominates all other load costs at this point when starting from warm caches. Kicking extra threads has relatively low cost, so things like window creation get pipelined

![](https://pbs.twimg.com/media/GCH0hXUWUAAPRak?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2023-12-24-the-sometimes-extra-2-5-seconds-on-vulkan/2023-12-24-matiasgoldberg-it-takes-how-long-maybe-its-taking-a-long-time]], [[archive/threads/NOTimothyLottes/2023-12-24-the-sometimes-extra-2-5-seconds-on-vulkan/2023-12-25-matias__eduardo-thats-insane]]

**2/** **@NOTimothyLottes** ^1738942198089965923

VkImportMemoryHostPointerInfoEXT change finished. On launch I map the Kart file, then kick a copy of the Kart to the start of the 'single GPU buffer' followed by optional image init from offsets in the GPU copy. The map stays for GPU write back to the Kart file.

**3/** **@NOTimothyLottes** ^1738943024653066639

I do still have a background page walker running at launch to try to pre-warm pages ahead of usage. And this also applies to the memory mapped Kart file. The net of all this is the minimal possible work at startup given the constraints of the current OS/APIs.
