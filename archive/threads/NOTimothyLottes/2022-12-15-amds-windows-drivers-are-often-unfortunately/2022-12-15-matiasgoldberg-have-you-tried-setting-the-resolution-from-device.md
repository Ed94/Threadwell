---
title: "@NOTimothyLottes Have you tried setting the resolution from Device Manager-> Monitor Name-> Properties ?"
type: archive
source: twitter
source_url: "https://x.com/matiasgoldberg/status/1603482063436406788"
author: "Matías N. Goldberg"
handle: matiasgoldberg
post_id: "1603482063436406788"
date: 2022-12-15
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Have you tried setting the resolution from Device Manager-> Monitor Name-> Properties ?"
in_reply_to: ""
parent_post_id: "1603479655574642688"
---

## Source

- URL: https://x.com/matiasgoldberg/status/1603482063436406788
- Author: Matías N. Goldberg (@matiasgoldberg)
- Posted: 2022-12-15 20:08:09

## Branch

**1/** **@matiasgoldberg** ^1603482063436406788

**@NOTimothyLottes**

Have you tried setting the resolution from Device Manager-> Monitor Name-> Properties ?

Via normal ways Windows/Amd decides to always use 1080p signal and upscale.

But on that old dialog it actually respects the resolution/hz I set

**2/** **@NOTimothyLottes** ^1603484063230316544

**@matiasgoldberg**

I get 'Generic PnP Monitor' there and no properity that seems to apply towards setting frequency limits or modes.

**3/** **@matiasgoldberg** ^1603491500171616281

**@NOTimothyLottes**

OK I was trying to recall from memory. I am at computer now.

Go to Advanced Display -> Display Properties for <X>

Then Adapter -> List All Modes

Select one you DON'T want -> OK -> Apply;
then List All Modes again, select the one you want -> OK -> Apply

![](https://pbs.twimg.com/media/FkC-_hpWYB82qEx?format=png&name=orig)
![](https://pbs.twimg.com/media/FkC_BJhWYBQwma-?format=jpg&name=orig)

**4/** **@NOTimothyLottes** ^1603492205229924374

**@matiasgoldberg**

The mode I'm building isn't standard, so it never shows up in the list. But thanks for the tip anyway.

**5/** **@NOTimothyLottes** ^1603493252417609740

**@matiasgoldberg**

Even using the "Custom Resolution Utility" to override and place in the correct display V&H ranges into the display registry data, with a reboot, still won't fix the problem with AMD's drivers. It still just won't accept the mode. This is latest AMD driver too.

![](https://pbs.twimg.com/media/FkC_wsCWYBUIMFF?format=png&name=orig)

**6/** **@NOTimothyLottes** ^1603494786010341379

**@matiasgoldberg**

Related, one of the amazing things possible on even current NVIDIA drivers is to run 240p 120Hz modes on standard old 31KHz VGA CRTs for perfect scanlines for vintage gaming. Also won't work on AMD due to this driver bug. Same trick as used on MiSTer here: https://www.retrorgb.com/mister-240p-120hz-on-a-vga-crt-monitor.html

**7/** **@NOTimothyLottes** ^1603522358475726849

**@matiasgoldberg**

Ok here we go. Lets see how long it takes to get a one line fix in an AMD public driver. Bug filed same as a standard user would file a bug, here on the AMD forums: https://community.amd.com/t5/drivers-software/amd-driver-quot-custom-resolutions-quot-broken-please-fix-it-s-a/m-p/567137/highlight/true#M165847

## Related

- Spine: [[archive/threads/NOTimothyLottes/2022-12-15-amds-windows-drivers-are-often-unfortunately]]
