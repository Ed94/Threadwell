---
title: "@VictorTaelin In Rust I’ve ended up making a code garbage compactor."
type: archive
source: twitter
source_url: "https://x.com/software_is_art/status/2078221834059915275"
author: "Callum Galbreath"
handle: software_is_art
post_id: "2078221834059915275"
date: 2026-07-17
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - VictorTaelin
description: "@VictorTaelin In Rust I’ve ended up making a code garbage compactor."
in_reply_to: ""
parent_post_id: "2078110851123286452"
---

## Source

- URL: https://x.com/software_is_art/status/2078221834059915275
- Author: Callum Galbreath (@software_is_art)
- Posted: 2026-07-17 20:54:31

## Branch

**1/** **@software_is_art** ^2078221834059915275

**@VictorTaelin**

In Rust I’ve ended up making a code garbage compactor.

Before opening a PR the tool uses a bottom up module traversal technique that iteratively: 
1. Changes all pub members to pub(mod) 
2. Compiles
3. Build errors show what to keep / delete

## Related

- Spine: [[archive/threads/VictorTaelin/2026-07-17-read-this-and-your-next-model-will-be-10x-smarter]]
