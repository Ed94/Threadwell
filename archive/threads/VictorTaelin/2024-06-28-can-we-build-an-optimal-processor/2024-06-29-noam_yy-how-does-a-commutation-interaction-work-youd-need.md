---
title: "@VictorTaelin How does a commutation interaction work?"
type: archive
source: twitter
source_url: "https://x.com/noam_yy/status/1807177987177230724"
author: "Noam Y"
handle: noam_yy
post_id: "1807177987177230724"
date: 2024-06-29
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - VictorTaelin
description: "@VictorTaelin How does a commutation interaction work?"
in_reply_to: ""
parent_post_id: "1806690584670679387"
---

## Source

- URL: https://x.com/noam_yy/status/1807177987177230724
- Author: Noam Y (@noam_yy)
- Posted: 2024-06-29 22:23:02

## Branch

**1/** **@noam_yy** ^1807177987177230724

**@VictorTaelin**

How does a commutation interaction work?
You'd need some kind of alloc/free manager.

**2/** **@VictorTaelin** ^1811784231363711315

**@noam_yy**

Yes, remember that cores can communicate with any other via lightweight messaging (that should be central to the chip's design). Allocation should be done by sending an alloc request to increasingly distant cores until one is free.

**3/** **@noam_yy** ^1811785874662646023

**@VictorTaelin**

nice! this starts to feel a lot like some blockchain designs, which makes sense, a parallel computer and a distributed are very similiar.

## Related

- Spine: [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor]]
