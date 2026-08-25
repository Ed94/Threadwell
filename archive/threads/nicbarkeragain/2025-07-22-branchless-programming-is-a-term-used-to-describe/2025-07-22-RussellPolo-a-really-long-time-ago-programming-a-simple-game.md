---
title: "A really long time ago,  programming a simple game in basic on a 6502 based Commodore PET, I changed the logic from:"
type: archive
source: twitter
source_url: "https://x.com/RussellPolo/status/1947564413780680847"
author: "Russell Polo"
handle: RussellPolo
post_id: "1947564413780680847"
date: 2025-07-22
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - nicbarkeragain
description: "A really long time ago,  programming a simple game in basic on a 6502 based Commodore PET, I changed the logic from:"
in_reply_to: ""
parent_post_id: "1947506500194472221"
---

## Source

- URL: https://x.com/RussellPolo/status/1947564413780680847
- Author: Russell Polo (@RussellPolo)
- Posted: 2025-07-22 07:48:34

## Branch

**1/** **@RussellPolo** ^1947564413780680847

A really long time ago,  programming a simple game in basic on a 6502 based Commodore PET, I changed the logic from:

If <leftarrow> then pos=pos-1
If <rightarrow> then pos=pos+1
If...

To:
pos=pos+key2motion[keypress]

The result was a dramatic improvement.  Sluggish character movement became smooth, quick motion. The result wasn't as easy to understand,  but the performance result more than justified the confusing code. 

Ever since,  I've always looked for ways to avoid branching logic. These are the types of optimizations you could never expect from a compiler.

## Related

- Spine: [[archive/threads/nicbarkeragain/2025-07-22-branchless-programming-is-a-term-used-to-describe]]
