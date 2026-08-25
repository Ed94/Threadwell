---
title: "Comparing matrix to quaternion code:"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1885175713638076657"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1885175713638076657"
date: 2025-01-31
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Comparing matrix to quaternion code:"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1885175713638076657
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-01-31 03:58:09

## Thread

**1/** **@NOTimothyLottes** ^1885175713638076657

Comparing matrix to quaternion code:
(A.) https://d3cw3dd2w32x2b.cloudfront.net/wp-content/uploads/2015/01/matrix-to-quat.pdf
(B.) https://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/index.htm (Alternative Method)

A with conditional moves is probably faster on CPU
B probably faster on GPU? (sqrt = 4 clk, copysign=BFI)
Anything better than those?

![](https://pbs.twimg.com/media/Gil71jfXEAAhOJa?format=png&name=orig)

**2/** **@NOTimothyLottes** ^1885182390978429048

The (B.) alternative method might be just 32 VALU clocks on AMD, wrote up the code below (but warning didn't test it yet).

![](https://pbs.twimg.com/media/GimC2pIXsAACvgi?format=png&name=orig)
