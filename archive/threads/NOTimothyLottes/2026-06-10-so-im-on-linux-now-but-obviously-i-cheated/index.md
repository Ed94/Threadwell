---
title: "So I'm on Linux now, but obviously I cheated, because this is a SteamOS machine (pre-installed)."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2064858927829745887"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2064858927829745887"
date: 2026-06-10
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "So I'm on Linux now, but obviously I cheated, because this is a SteamOS machine (pre-installed)."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2064858927829745887
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-06-10 23:55:06

## Thread

**1/** @NOTimothyLottes

So I'm on Linux now, but obviously I cheated, because this is a SteamOS machine (pre-installed). Need to re-learn enough to be able to make responsible choices on a new install. First up what init system to do? {openrc, runit, s6, or dinit}.

Branches: [[archive/threads/NOTimothyLottes/2026-06-10-so-im-on-linux-now-but-obviously-i-cheated/2026-06-11-RouaniJihad-my-patience-is-this-thin-with-win11-right-now-but]], [[archive/threads/NOTimothyLottes/2026-06-10-so-im-on-linux-now-but-obviously-i-cheated/2026-06-11-NOTimothyLottes-dinit-is-out-no-c-for-me-so-runit-wins-by-default]], [[archive/threads/NOTimothyLottes/2026-06-10-so-im-on-linux-now-but-obviously-i-cheated/2026-06-11-mcnabbd-fascinating-to-me-how-this-challenge-would-have]]

**2/** @NOTimothyLottes

Going to give artix-lxqt-runit variation a try. Mostly just a stop gap to see if I can actually get a bloated Linux system installed before a more serious effort with BuildRoot. First de-windows victim computer will be an AMD powered APU.

**3/** @NOTimothyLottes

Looks like the workaround for my locked UEFI secure boot Enabled on the second machine was to "Set Supervisor Password", afterwords I could disable secure boot and APM, but still no way to enable legacy BIOS "Boot Mode".

**4/** @NOTimothyLottes

Somewhat surprised, Artix using the graphical install just worked out of the box (AMD APU). Got confused post install when 'top' shows 'Xorg' instead of 'XLibre' but the package manager says XLibre is installed.
