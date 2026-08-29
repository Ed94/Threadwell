---
title: "Use a parallel reduction, not atomics from every thread."
type: archive
source: twitter
source_url: "https://x.com/ourtown2/status/2058459472557990030"
author: "Brian Crabtree"
handle: ourtown2
post_id: "2058459472557990030"
date: 2026-05-24
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "Use a parallel reduction, not atomics from every thread."
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/ourtown2/status/2058459472557990030
- Author: Brian Crabtree (@ourtown2)
- Posted: 2026-05-24 08:05:57

## Branch

**1/** **@ourtown2** ^2058459472557990030

Use a parallel reduction, not atomics from every thread.

Split the array into blocks. Each thread loads one or more elements, accumulates a local partial sum in registers, then the block reduces those partials using warp-level shuffles and shared memory. Each block writes one partial sum to an output array. Then launch a second reduction over that smaller partial array until only one value remains.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
