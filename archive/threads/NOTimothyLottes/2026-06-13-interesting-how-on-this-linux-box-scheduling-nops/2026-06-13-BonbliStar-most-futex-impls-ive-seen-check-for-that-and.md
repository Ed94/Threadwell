---
title: "@NOTimothyLottes most futex impls i've seen check for that and early return before the syscall, but you likely already knew that"
type: archive
source: twitter
source_url: "https://x.com/BonbliStar/status/2065944487075975648"
author: "Bonbli ★"
handle: BonbliStar
post_id: "2065944487075975648"
date: 2026-06-13
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes most futex impls i've seen check for that and early return before the syscall, but you likely already knew that"
in_reply_to: ""
parent_post_id: "2065840191340707905"
---

## Source

- URL: https://x.com/BonbliStar/status/2065944487075975648
- Author: Bonbli ★ (@BonbliStar)
- Posted: 2026-06-13 23:48:43

## Branch

**1/** **@BonbliStar** ^2065944487075975648

**@NOTimothyLottes**

most futex impls i've seen check for that and early return before the syscall, but you likely already knew that

**2/** **@NOTimothyLottes** ^2065998673117376693

**@BonbliStar**

Yes, the comment was more the point of designing for the worst case, the limit of possibly blocking calls that interact with the scheduling.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2026-06-13-interesting-how-on-this-linux-box-scheduling-nops]]
