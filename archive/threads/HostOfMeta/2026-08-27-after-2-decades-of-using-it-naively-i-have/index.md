---
title: "After 2 decades of using it naively, I have deconstructed the (×) cross product."
type: archive
source: twitter
source_url: "https://x.com/HostOfMeta/status/2093065798399176704"
author: "Jeremie Pelletier"
handle: HostOfMeta
post_id: "2093065798399176704"
date: 2026-08-27
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - HostOfMeta
description: "After 2 decades of using it naively, I have deconstructed the (×) cross product."
in_reply_to: ""
---

## Source

- URL: https://x.com/HostOfMeta/status/2093065798399176704
- Author: Jeremie Pelletier (@HostOfMeta)
- Posted: 2026-08-27 19:59:08

## Thread

**1/** **@HostOfMeta** ^2093065798399176704

After 2 decades of using it naively, I have deconstructed the (×) cross product. Only took learning geometric algebra. Goes like this:

u×v = ⋆(u∧v) = w

As in, it combines two operations: a lift and a drop. First the wedge creates a bivector out of (u) and (v), which turns the two vectors into an oriented plane. Then the dual multiplies by the antiscalar, which cancels out (u) and (v) while leaving an orthogonal (w) vector in place.

And explains why it only works in 3D (7D uses a different contraction, because this formula yields a 5D blade.)

**2/** **@HostOfMeta** ^2093066969188622765

Quick precision: the "cancels out" part only applies when (u) and (v) are the basis vectors e1 and e2, meaning their coefficients stay unitary as (1).

When these input vectors have non-unit coefficients, then the dual makes more of a selection operation because they play a role.
