---
title: "Yuck, starting on WDM/KS audio interface for WIN32, much more painful than ALSA."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2072804183992922296"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2072804183992922296"
date: 2026-07-02
archived: 2026-08-23
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Yuck, starting on WDM/KS audio interface for WIN32, much more painful than ALSA."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2072804183992922296
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-02 22:06:42

## Thread

**1/**

Yuck, starting on WDM/KS audio interface for WIN32, much more painful than ALSA. But I've been here before. Starting with the include bloat ... the real question is if I'm going to need to file more Wine bugs.

Media (not lifted): `2072804183992922296_HMQT-ALWoAAABEe_orig.png` `2072804183992922296_HMQUVgpXYAA3h6r_orig.png`

**2/**

Wine has a lot of problems with SetConsoleMode() I had to include an extra ENABLE_WRAP_AT_EOL_OUTPUT, and then force a newline right after ASCI ESC[H else it would screw up (and it still does at the end with the ??). But at least the debug is usable now.

Media (not lifted): `2072825642354123190_HMQnWmJXcAAOiSS_orig.png`

**3/**

But of course instant bad news, I cannot open the WinMM DRV_QUERYDEVICEINTERFACE, it returned ~0 (INVALID_HANDLE_VALUE). So I'm dead in the water in Wine again. Honestly getting sick of filing bugs in Wine, all the important stuff I do is broken. So what, no games use WDM/KS?

Media (not lifted): `2072826861449629746_HMQoTiQWkAAbwj1_orig.png`

**4/**

https://forum.winehq.org/viewtopic.php?t=10225 - Looks like I'm 16 years late to the answer, if they didn't get in WDM/KS in 16 years, certainly it won't happen. Still surprised that all PC games are using the higher level garbage-ware sound APIs on Windows.
