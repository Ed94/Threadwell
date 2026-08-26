---
title: "I just do combinations of separate SPSC ring buffers with a known amount of input and output threads."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1873824152013959209"
author: "Jebrim"
handle: AgileJebrim
post_id: "1873824152013959209"
date: 2024-12-30
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - bmcnett
description: "I just do combinations of separate SPSC ring buffers with a known amount of input and output threads."
in_reply_to: ""
parent_post_id: "1873744231719956872"
---

## Source

- URL: https://x.com/AgileJebrim/status/1873824152013959209
- Author: Jebrim (@AgileJebrim)
- Posted: 2024-12-30 20:11:06

## Branch

**1/** **@AgileJebrim** ^1873824152013959209

I just do combinations of separate SPSC ring buffers with a known amount of input and output threads. The ratio of producers to consumers dictates how many of each ring buffer each thread gets assigned to it. They just iterate through each per pass.

Way more predictable execution times when done like this. No spin loops of unknown duration.

## Related

- Spine: [[archive/threads/bmcnett/2024-12-30-the-simplest-multi-producer-multi-consumer-ring]]
