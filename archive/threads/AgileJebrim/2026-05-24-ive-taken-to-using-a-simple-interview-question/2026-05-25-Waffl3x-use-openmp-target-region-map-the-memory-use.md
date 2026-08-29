---
title: "Use OpenMP :^)"
type: archive
source: twitter
source_url: "https://x.com/Waffl3x/status/2058821469434523920"
author: "Waffl3x ❤️‍🩹 🩹 👁‍🗨"
handle: Waffl3x
post_id: "2058821469434523920"
date: 2026-05-25
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "Use OpenMP :^)"
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/Waffl3x/status/2058821469434523920
- Author: Waffl3x ❤️‍🩹 🩹 👁‍🗨 (@Waffl3x)
- Posted: 2026-05-25 08:04:24

## Branch

**1/** **@Waffl3x** ^2058821469434523920

Use OpenMP :^)
Target region, map the memory, use parallel for with a reduction clause, yell at my compiler vendor if it fails to vectorize.
Or just use Fortran (also with OpenMP).

Answer changes if you need non-overflowing semantics. I am honestly not sure how I would do it efficiently in a scenario that effectively needs a bigint.

I imagine you chunk it in such a way that lets you use native width ints for the largest proportion of the calculation possible

**2/** **@AgileJebrim** ^2058921496240627917

**@Waffl3x**

OpenMP is for CPUs and isn’t really designed for the realtime workflows we require. ISPC would be better and actually has hard guarantees about vectorization.

Our earlier tech was built on top of ISPC. Our next gen tech is in a custom shader language built for GPU-native apps.

**3/** **@AgileJebrim** ^2058921653338361857

**@Waffl3x**

The goal should be to avoid BIGINT and have the input values be defined as smaller bitwidths instead.

**4/** **@Waffl3x** ^2058961654243827959

**@AgileJebrim**

Mmm I can see it, also I suppose bigint isn't necessary anyway, 128bit is almost certainly goof enough for a sum... I hope.

**5/** **@AgileJebrim** ^2058964499680420089

**@Waffl3x**

https://x.com/agilejebrim/status/2058562643158352101?s=46&t=ZbNecpPBsBMrvteeaA6IcA

**6/** **@Waffl3x** ^2058969433499111811

**@AgileJebrim**

My mental model for this was off, it really does fit in a 32bit unsigned huh? OpenMP does this efficiently trivially I'm pretty sure, but that's just because it's such a simple case. So my answer really isn't useful for the interviewer.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
