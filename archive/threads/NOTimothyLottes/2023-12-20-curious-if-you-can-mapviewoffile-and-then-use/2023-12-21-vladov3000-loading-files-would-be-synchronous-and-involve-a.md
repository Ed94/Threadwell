---
title: "@NOTimothyLottes Loading files would be synchronous and involve a bunch of faults, so how would it be worth it compared to the syscall overhead?"
type: archive
source: twitter
source_url: "https://x.com/vladov3000/status/1737631747750109607"
author: "vlad vladov"
handle: vladov3000
post_id: "1737631747750109607"
date: 2023-12-21
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Loading files would be synchronous and involve a bunch of faults, so how would it be worth it compared to the syscall overhead?"
in_reply_to: ""
parent_post_id: "1737618231450579351"
---

## Source

- URL: https://x.com/vladov3000/status/1737631747750109607
- Author: vlad vladov (@vladov3000)
- Posted: 2023-12-21 00:31:06

## Branch

**1/** **@vladov3000** ^1737631747750109607

**@NOTimothyLottes**

Loading files would be synchronous and involve a bunch of faults, so how would it be worth it compared to the syscall overhead?

**2/** **@NOTimothyLottes** ^1737632532357636356

**@vladov3000**

It would have to pre-fault the pages and lock the pages to have a GPU mapping of it. It would be worth it to not have to use some other mechanism for the GPU program to feed the CPU information about what to copy out of GPU memory into a file.

**3/** **@vladov3000** ^1737649307736821760

**@NOTimothyLottes**

I see.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2023-12-20-curious-if-you-can-mapviewoffile-and-then-use]]
