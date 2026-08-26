---
title: "@iquilezles I'd say ALWAYS look at the generated assembly when you care about optimizations."
type: archive
source: twitter
source_url: "https://x.com/and_coder/status/1888420888032559405"
author: "Dmitry Andreev"
handle: and_coder
post_id: "1888420888032559405"
date: 2025-02-09
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - iquilezles
description: "@iquilezles I'd say ALWAYS look at the generated assembly when you care about optimizations."
in_reply_to: ""
parent_post_id: "1888409333182218691"
---

## Source

- URL: https://x.com/and_coder/status/1888420888032559405
- Author: Dmitry Andreev (@and_coder)
- Posted: 2025-02-09 02:53:19

## Branch

**1/** **@and_coder** ^1888420888032559405

**@iquilezles**

I'd say ALWAYS look at the generated assembly when you care about optimizations. I've seen NVidia compilers still generated branches even with the ternary operator if arguments are expressions. To be sure have float a = ..., float b = ..., and then float c = (x < 0.5) ? a : b;

## Related

- Spine: [[archive/threads/iquilezles/2025-02-09-hey-dont-optimize-conditional-moves-with-mix-step]]
