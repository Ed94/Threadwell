---
title: "@NOTimothyLottes @SheriefFYI What’s the best way of doing that if rebar is not supported? Say on WebGL / DX11?"
type: archive
source: twitter
source_url: "https://x.com/Meetem4/status/1737448166683713602"
author: "Meetem"
handle: Meetem4
post_id: "1737448166683713602"
date: 2023-12-20
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SheriefFYI
description: "@NOTimothyLottes @SheriefFYI What’s the best way of doing that if rebar is not supported? Say on WebGL / DX11?"
in_reply_to: ""
parent_post_id: "1737162074172637506"
---

## Source

- URL: https://x.com/Meetem4/status/1737448166683713602
- Author: Meetem (@Meetem4)
- Posted: 2023-12-20 12:21:37

## Branch

**1/** **@Meetem4** ^1737448166683713602

**@NOTimothyLottes** **@SheriefFYI**

What’s the best way of doing that if rebar is not supported? Say on WebGL / DX11?

**2/** **@NOTimothyLottes** ^1737478162009801189

**@Meetem4** **@SheriefFYI**

For DX11, use Vulkan instead. On pre-large-bar, AMD still supported the 256 MiB device_local+host_visible, NV one has to fallback to slower bus crossing just host_visible buffer.

**3/** **@NOTimothyLottes** ^1737479360867688545

**@Meetem4** **@SheriefFYI**

As for Web* - Root problem is more like the idea that if someone has a broken arm, that all arms should be broken too, so until the controlling parties can be convinced that it is ok to support both people with broken arms and non-broken arms, good luck

**4/** **@Meetem4** ^1737515940055527782

**@NOTimothyLottes** **@SheriefFYI**

Thank you. Does large bar require support for ReBAR, so 30xx gpus?

**5/** **@NOTimothyLottes** ^1737519841341321657

**@Meetem4** **@SheriefFYI**

Probably more complex, as in dependent on {motherboard chipset, BIOS/UEFI settings, GPU chipset that the IHVs greenlight enable which might be driver dependent}?

**6/** **@Meetem4** ^1737528676198039713

**@NOTimothyLottes** **@SheriefFYI**

Thank you very much, I'm extemely appreciate that!

## Related

- Spine: [[archive/threads/SheriefFYI/2023-12-19-always-always-always-use-an-async-copy-queue]]
