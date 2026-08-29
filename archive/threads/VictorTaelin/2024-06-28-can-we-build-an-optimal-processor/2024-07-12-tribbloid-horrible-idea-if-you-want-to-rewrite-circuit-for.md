---
title: "@VictorTaelin horrible idea: if you want to rewrite circuit for performance, why not doing it directly on the lowest gate-level?"
type: archive
source: twitter
source_url: "https://x.com/tribbloid/status/1811804116877799564"
author: "Peng Cheng, asking λP2-λC"
handle: tribbloid
post_id: "1811804116877799564"
date: 2024-07-12
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - VictorTaelin
description: "@VictorTaelin horrible idea: if you want to rewrite circuit for performance, why not doing it directly on the lowest gate-level?"
in_reply_to: ""
parent_post_id: "1806690584670679387"
---

## Source

- URL: https://x.com/tribbloid/status/1811804116877799564
- Author: Peng Cheng, asking λP2-λC (@tribbloid)
- Posted: 2024-07-12 16:45:37

## Branch

**1/** **@tribbloid** ^1811804116877799564

**@VictorTaelin**

horrible idea: if you want to rewrite circuit for performance, why not doing it directly on the lowest gate-level?

mainstream adders (Kogge-Stone) and multipliers (Wallace) are quite suboptimal, but the only superhuman rewrite I knew is based on e-graph

https://arxiv.org/abs/2312.06004

**2/** **@VictorTaelin** ^1811807840383750429

**@tribbloid**

What do you mean is a terrible idea exactly? A processor with millions of interaction cores?

**3/** **@tribbloid** ^1811808888624181341

**@VictorTaelin**

sorry I mean "doing it on gate-level" may be a horrible idea

**4/** **@VictorTaelin** ^1811809058883522654

**@tribbloid**

but I don't get what you mean? what the alternative would be?

**5/** **@tribbloid** ^1811813448084312474

**@VictorTaelin**

IMHO most tools focus on optimising RTL then delegate to HLS

> (from arXiv) High-level and logic synthesis tools ... but rely on fixed architectures ...

if optimising gate-level directly (e.g. rewriting a ripple-carry adder into Kogge-Stone), then HLS will be slow in comparison

**6/** **@tribbloid** ^1811824453111939074

**@VictorTaelin**

correction: delegate to LS (which will be slow in comparison)

LS and HLS are not the same thing (excuse my English)

## Related

- Spine: [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor]]
