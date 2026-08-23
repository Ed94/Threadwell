---
title: "CRT emulation on LCDs can be hard."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1688491417109196800"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1688491417109196800"
date: 2023-08-07
archived: 2026-08-23
status: draft
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "CRT emulation on LCDs can be hard."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1688491417109196800
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-08-07 10:04:59

## Thread

**1/**

CRT emulation on LCDs can be hard. For example it's often easy to generate a pattern that causes a LCD hardware bug. NOT joking. Here is an example on the Steam Deck. The pattern in the window affects the scan (Deck scan is rotated) outside the window.

Media (not lifted): `1688491417109196800_F265_JZXsAAInpa_orig.jpg` `1688491417109196800_F265_hLXkAAnfek_orig.jpg`

Branches: [[2023-08-10-BlurBusters-very-interesting-crosstalk-from-voltage-inversion]]

**2/**

The actual pattern is this (it's a 2x1 pixel checker of {G,RB}).

Media (not lifted): `1688492237775142912_F266epnW4AAdCiK_orig.png`

**3/**

The theory: Deck's 90deg scan results in {(bottom)R, G, B (top)} sub-pixel components. So could alternate {G,RB} only per pixel in a checker pattern to generate a new sub-pixel pattern at a different resolution. In this case trying for 640x400 virtual resolution.

Media (not lifted): `1688493686554849280_F267UYuXAAAO50A_orig.png`

**4/**

For virtual pixel, shift energy into masked virtual phosphor. So 50% brightness red, would be {100%, 0%} for {in, out} of phosphor pixels. Over 50% one starts to increase non-phosphor pixels until some maximum so mask is still visible, but brightness isn't too compromised.

**5/**

Of course this is done in linear, so it's energy conserving in theory. But when the panel fails, it breaks down and doesn't work. I see this problem on a bunch of different devices. My personal AMD laptop has the exact same fail case (but rotated differently).
