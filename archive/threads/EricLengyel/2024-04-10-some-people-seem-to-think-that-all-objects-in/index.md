---
title: "Some people seem to think that all objects in exterior algebra or geometric algebra are represented in code by big 16-component entities."
type: archive
source: twitter
source_url: "https://x.com/EricLengyel/status/1777895775428854186"
author: "Eric Lengyel"
handle: EricLengyel
post_id: "1777895775428854186"
date: 2024-04-10
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - EricLengyel
description: "Some people seem to think that all objects in exterior algebra or geometric algebra are represented in code by big 16-component entities."
in_reply_to: ""
---

## Source

- URL: https://x.com/EricLengyel/status/1777895775428854186
- Author: Eric Lengyel (@EricLengyel)
- Posted: 2024-04-10 03:05:59

## Thread

**1/** **@EricLengyel** ^1777895775428854186

Some people seem to think that all objects in exterior algebra or geometric algebra are represented in code by big 16-component entities. No decent implementation would do this, and if it's something you've seen, then you've been exposed to a very poor source of information.

**2/** **@EricLengyel** ^1777895776540299662

Points still have 3 components (or maybe 4 homogeneous components), lines have 6, and planes have 4. Quaternions have 4 components, dual quaternions (motors) have 8 components, and flectors have 8 components. Nothing ever uses more than 8. These are implemented as distinct types.

**3/** **@gamespotting** ^1777903028840124551

**@EricLengyel**

I remember when pondering what it’d take to implement a system for graphics, thinking a fully general element (of an R{3,2} conformal space) could have up to 32 components.. but most elements of interest for graphic’s applications would only have 4, 6, or 8 or something..

Branches: [[archive/threads/EricLengyel/2024-04-10-some-people-seem-to-think-that-all-objects-in/2024-04-10-gamespotting-degenerate-cases-where-a-0-value-in-one-component]]
