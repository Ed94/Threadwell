---
title: "@AgileJebrim Divide up the available memory between cores, each with out output slot and as many input slots as possible."
type: archive
source: twitter
source_url: "https://x.com/matt_timmermans/status/2058551271389356330"
author: "Matt Timmermans"
handle: matt_timmermans
post_id: "2058551271389356330"
date: 2026-05-24
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim Divide up the available memory between cores, each with out output slot and as many input slots as possible."
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/matt_timmermans/status/2058551271389356330
- Author: Matt Timmermans (@matt_timmermans)
- Posted: 2026-05-24 14:10:43

## Branch

**1/** **@matt_timmermans** ^2058551271389356330

**@AgileJebrim**

Divide up the available memory between cores, each with out output slot and as many input slots as possible.   Load memory, have each core accumulate its part, repeat.

Might be able to go faster with double-buffering so you can load and sum at the same time.

**2/** **@AgileJebrim** ^2058551683420913730

**@matt_timmermans**

“have each core accumulate its part”

Detail this.

**3/** **@matt_timmermans** ^2058554402332409962

**@AgileJebrim**

I'm not actually familiar enough to know why you asking for detail (I should NOT get your job :-), but each pass is essentially an image resize.  Separate input + output memory, organize input to reduce contention.  Only a few thousand output pixels, so that part not important.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
