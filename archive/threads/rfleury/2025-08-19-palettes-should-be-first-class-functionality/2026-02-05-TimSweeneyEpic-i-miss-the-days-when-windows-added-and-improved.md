---
title: "@rfleury I miss the days when Windows added and improved UI controls and apps rushed to adopt them."
type: archive
source: twitter
source_url: "https://x.com/TimSweeneyEpic/status/2019288689571221523"
author: "Tim Sweeney"
handle: TimSweeneyEpic
post_id: "2019288689571221523"
date: 2026-02-05
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury I miss the days when Windows added and improved UI controls and apps rushed to adopt them."
in_reply_to: ""
parent_post_id: "1957853922191638708"
---

## Source

- URL: https://x.com/TimSweeneyEpic/status/2019288689571221523
- Author: Tim Sweeney (@TimSweeneyEpic)
- Posted: 2026-02-05 05:55:14

## Branch

**1/** **@TimSweeneyEpic** ^2019288689571221523

**@rfleury**

I miss the days when Windows added and improved UI controls and apps rushed to adopt them. Because this stopped a couple decades ago, every framework had to take over and build their own, and it’s only through hoc reimplementation that features propagate among apps.

**2/** **@rfleury** ^2019295435379339449

I couldn’t agree more. Unfortunately I think a lack of trust in Windows led to a lack of coupling with the platform (especially since Windows was just one option for the hardware). It became more appealing to build custom layers, and abstract over the underlying platform, so that you weren’t locked in (even though you still wanted to ship on Windows as one option).

I think this lack of trust came from many things, including seemingly unrelated ones—notably UI API design (the newer “modern” APIs vastly overcomplicate what the old basic C-style ones made comparatively simple—*not* to suggest they were perfect), a lack of keeping up with the bleeding edge in both UI design and distribution (writing a Windows program misses new UI design ideas e.g. unified palettes, and all of the distribution magic you get from e.g. web—it’s possible a different OS strategy may have changed that), platform stewardship (bloat, anti-user policies), and so on.

**3/** **@rfleury** ^2019297702853636176

This is really undesirable, because the platform is really the right layer for implementing this kind of thing. Each program has fewer responsibilities, so things Just Work, you win code dedup (in a way that programs - even if they use common libraries - can't), you get tighter cross-program integration, and everything is consistent to the user. Maybe a future platform can do this right for longer!

## Related

- Spine: [[archive/threads/rfleury/2025-08-19-palettes-should-be-first-class-functionality]]
