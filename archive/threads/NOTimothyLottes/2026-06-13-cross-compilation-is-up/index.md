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
draft: false
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

![](https://pbs.twimg.com/media/HKtP7aQXsAAtJ5X?format=jpg&name=orig)

![](https://pbs.twimg.com/media/HKtP7aTWEAAC_j4?format=jpg&name=orig)
Branches: [[archive/threads/NOTimothyLottes/2026-06-13-cross-compilation-is-up/2026-06-13-tomcr2100-interesting-font-does-it-have-a-name]]

**2/**

Found my first of perhaps many Wine “fix me”s looks like they didn’t emulate NtQuerySystemInformation() for use to get the TSC time scalar. Also implies all PC devs do this wrong, else Valve would have had this implemented already.
