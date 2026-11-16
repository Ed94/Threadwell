---
title: "@valyala A bit off topic, but have you ever considered to rewrite Victoria* products to Rust?"
type: archive
source: twitter
source_url: "https://x.com/DmytroKrasun/status/2118354404059513331"
author: "Dmytro Krasun"
handle: DmytroKrasun
post_id: "2118354404059513331"
date: 2026-11-05
archived: 2026-11-16
draft: false
tags:
  - archive
  - twitter
  - valyala
description: "@valyala A bit off topic, but have you ever considered to rewrite Victoria* products to Rust?"
in_reply_to: ""
parent_post_id: "2118349666911768669"
---

## Source

- URL: https://x.com/DmytroKrasun/status/2118354404059513331
- Author: Dmytro Krasun (@DmytroKrasun)
- Posted: 2026-11-05 14:47:01

## Branch

**1/** **@DmytroKrasun** ^2118354404059513331

**@valyala**

A bit off topic, but have you ever considered to rewrite Victoria* products to Rust?

**2/** **@valyala** ^2118366895862661191

There is no practical sense in rewriting VictoriaMetrics from Go to Rust:

- Rust code is harder to write, read and maintain than Go code. This slows down development pace.

- Rust compiler takes much more time for compiling the source code than Go compiler (minutes vs seconds). This slows down development pace.

- While Rust code can be faster than the corresponding Go code, it doesn't matter for 99% of the codebase of typical application such as VictoriaMetrics. As for the rest of 1% of the source code sitting in hot paths, there are no issues in optimising it in Go.

## Related

- Spine: [[archive/threads/valyala/2026-11-05-til-you-can-increase-hot-loop-performance-by-20x]]
