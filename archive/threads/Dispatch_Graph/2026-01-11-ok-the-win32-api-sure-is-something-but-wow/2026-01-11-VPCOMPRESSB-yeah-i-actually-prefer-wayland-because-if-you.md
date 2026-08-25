---
title: "yeah."
type: archive
source: twitter
source_url: "https://x.com/VPCOMPRESSB/status/2010385913541546282"
author: "/i:'mɪər/"
handle: VPCOMPRESSB
post_id: "2010385913541546282"
date: 2026-01-11
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - Dispatch_Graph
description: "yeah."
in_reply_to: ""
parent_post_id: "2010303501851877740"
---

## Source

- URL: https://x.com/VPCOMPRESSB/status/2010385913541546282
- Author: /i:'mɪər/ (@VPCOMPRESSB)
- Posted: 2026-01-11 16:18:47

## Branch

**1/** @VPCOMPRESSB

yeah. i actually prefer Wayland because if you implement something super simple, you get something super simple back (e.g., if i create a window, i get the bare minimum window - no decorations, no resizing, no keyboard or mouse input). with Win32, i'd have fight it and move through its weeds to force it to make something simple.
another problem with Win32 is that it modularizes too much, and make everything seem irrelevant from each other. in Wayland, it's all unified, where if just learn 1 pattern from 1 thing, you can apply that pattern to everything else, from windows to input (e.g., all interfaces are just a simple server-client messaging model). basically, you can take a step back and look at everything as a whole, and clearly see a pattern.

**2/** @NOTimothyLottes

@VPCOMPRESSB @Dispatch_Graph You didn't get the true Wayland experience until you try interfacing to Wayland without the Wayland user-space library. Meaning do it with just the kernel calls required. Then you will have taken the gold off the poop, and understood how bad it actually is.

**3/** @NOTimothyLottes

@VPCOMPRESSB @Dispatch_Graph WIN32 base system DLLs are a substantially cleaner interface. I only do non-decorated full-screen (foreground or background) window. Majority of WIN32 code fits on screen grab with mostly comments. I'm not a fan of their "WndProc" but at least it is simple.

![](https://pbs.twimg.com/media/G-Zd9wLWUAE9kZj?format=png&name=orig)

**4/** @NOTimothyLottes

@VPCOMPRESSB @Dispatch_Graph Some like to hate on X11, but for what it was designed to do (support both local and remote displays), it is at least very well documented and actually quite easy to roll an interface for with just Linux kernel calls (no external libraries). Docs here: https://x.org/releases/X11R7.7/doc/xproto/x11protocol.html

**5/** @NOTimothyLottes

@VPCOMPRESSB @Dispatch_Graph Duckduckgo Wayland protocol and you get this garbage as documentation (below). Nothing there actually explains how it works, it's just high-level OOP obfustication speak. My vomit translator cannot even process this stuff.

![](https://pbs.twimg.com/media/G-Zjy3uXgAETWbE?format=jpg&name=orig)

**6/** @NOTimothyLottes

@VPCOMPRESSB @Dispatch_Graph Lets continue. It's built over unix domain sockets and doesn't support remote rendering. Haha, WFT. Just because they want to transfer file descriptors between processes for "bulk data". Wayland looses network displays and is SLOWER (fail): https://www.dedoimedo.com/computers/plasma-6-4-performance-wayland-x11-power-cpu-kernel.html

![](https://pbs.twimg.com/media/G-Zk_VHW0AAFoC_?format=png&name=orig)
![](https://pbs.twimg.com/media/G-Zla8PXYAAdRoE?format=png&name=orig)
![](https://pbs.twimg.com/media/G-ZmyPCWQAAKtYR?format=png&name=orig)

**7/** @NOTimothyLottes

@VPCOMPRESSB @Dispatch_Graph Don't understand why Linux people had to take what was working, X11, and instead of just improving it, they had to make something that {removed the remote desktop, made it slower, and forces an OOP garbage design}. There is nothing good here.

**8/** @NOTimothyLottes

@VPCOMPRESSB @Dispatch_Graph Another great thing about X11, is that it was trivial to both write and use your own window manager, using the same stable system for DECADES. I had a 350 line minwm.c window manager. Dead easy.

![](https://pbs.twimg.com/media/G-ZrxUJXwAAINS7?format=png&name=orig)

**9/** @NOTimothyLottes

@VPCOMPRESSB @Dispatch_Graph Unix was about KISS (keep it simple stupid) then Linux user-space people transformed that into MISC {make it stupid complex}. Seen this trend with Audio, from OSS to ALSA, and so on.

**10/** @NOTimothyLottes

@VPCOMPRESSB @Dispatch_Graph I worked in the {SunOS,Solaris,HPUX,SGI,AXI,etc} workstation era and started on Linux before ELF and before pthreads. Meaning I build things based on fork() [instead of pthreads] and SHM (shared page mappings) when doing local-only interfaces (no high kernel call granularity).

**11/** @NOTimothyLottes

@VPCOMPRESSB @Dispatch_Graph If Linux people wanted to replace X11 with a local only interface, at a minimum it should have been simple SHM for the majority, and then only go outside SHM when needing to say kick a doorbell (make wake another process), etc.

**12/** @o__boga

@NOTimothyLottes @VPCOMPRESSB @Dispatch_Graph Obfuscation is the secret for its "security!"!

**13/** @VPCOMPRESSB

@NOTimothyLottes @Dispatch_Graph i've never actually used X11. this is much easier.

![](https://pbs.twimg.com/media/G-a43PTXMAAIaEO?format=png&name=orig)

## Related

- Spine: [[archive/threads/Dispatch_Graph/2026-01-11-ok-the-win32-api-sure-is-something-but-wow]]
