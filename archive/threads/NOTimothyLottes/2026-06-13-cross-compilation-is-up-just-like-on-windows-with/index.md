---
title: "Cross compilation is up."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2065832746757341482"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2065832746757341482"
date: 2026-06-13
archived: 2026-08-23
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Cross compilation is up."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2065832746757341482
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-06-13 16:24:42

## Thread

**1/**

Cross compilation is up. Just like on windows with GCC I have to disable all warnings because there is no way to turn off “function called through a non-compatible type”. They obviously should have had warning IDs and an ID based disable.

Media (not lifted): `2065832746757341482_HKtP7aQXsAAtJ5X_orig.jpg` `2065832746757341482_HKtP7aTWEAAC_j4_orig.jpg`

Branches: [[archive/threads/NOTimothyLottes/2026-06-13-cross-compilation-is-up-just-like-on-windows-with/2026-06-13-tomcr2100-interesting-font-does-it-have-a-name]]

**2/**

Found my first of perhaps many Wine “fix me”s looks like they didn’t emulate NtQuerySystemInformation() for use to get the TSC time scalar. Also implies all PC devs do this wrong, else Valve would have had this implemented already.
