---
title: "@onatt0 It would be interesting to size stuff so the limits align with instruction cache size limits."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1917657931375313017"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1917657931375313017"
date: 2025-04-30
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@onatt0 It would be interesting to size stuff so the limits align with instruction cache size limits."
in_reply_to: "1917656470444790255"
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1917657931375313017
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-04-30 19:10:53

> @NOTimothyLottes a much better encoding is possible
> next iteration is going to be
>
> 16bits*4words if you need multiple words(last word=15bits)
> 7bits*9chars if its a unique/short name(to not clutter the 16-bit dictionary-space)
>
> 64K*4 words should be enough for most cases

## Thread

**1/** **@NOTimothyLottes** ^1917657931375313017

**@onatt0**

It would be interesting to size stuff so the limits align with instruction cache size limits. Build something where the expectation is a hit in the I$ once it's warm after the context switch and move everything else to data complexity.

**2/** **@NOTimothyLottes** ^1917658709192306788

**@onatt0**

Same could apply for non-bulk data, ie the stuff you'd possibly want human readable annotation on. Make it sized to practical L2$ limits, or fix it to at most the shared L3$.
