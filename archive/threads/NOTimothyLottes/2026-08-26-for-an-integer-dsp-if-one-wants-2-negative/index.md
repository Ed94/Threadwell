---
title: "For an integer DSP, if one wants 2 negative operand modifiers: that requires 2 carry ins."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2092760583405736322"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2092760583405736322"
date: 2026-08-26
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "For an integer DSP, if one wants 2 negative operand modifiers: that requires 2 carry ins."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2092760583405736322
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-08-26 23:46:19

## Thread

**1/** **@NOTimothyLottes** ^2092760583405736322

For an integer DSP, if one wants 2 negative operand modifiers: that requires 2 carry ins. 7 series DSP has one, and Ultrascale adds a full extra W MUX which provides a 4th input for the odder, with a RND term which and be optionally added in for a second carry.

**2/** **@NOTimothyLottes** ^2092761941408170463

7 series does not(Z)+not(X+Y+CIN)+1 where the NOTs and last +1 are runtime adjustable. So it has 2 carry ins BUT the CIN is trapped in the NOT instead of outside so it prevents two operand negation

**3/** **@NOTimothyLottes** ^2092762990521036839

When doing signed fixed point, it is nice to logically flip the neg and pos sides so one gets a positive maximum magnitude power of 2.

**4/** **@NOTimothyLottes** ^2092764192478482740

But when 0x8000… is your largest magnitude term, your multiply always does a sign flip by default, so  having NEG modifier on the MUL sub-product of and IMAD is necessary simply to avoid the sign flip.

**5/** **@NOTimothyLottes** ^2092765456339808439

Also when thinking in this inverted way, the IMAD is really more of an IMSB without the NEG modifiers. Yes: It’s a way of thinking that is alien to kids now stuck with brains in 1-s complement floating point. But state of the art for vintage simpler integer machines
