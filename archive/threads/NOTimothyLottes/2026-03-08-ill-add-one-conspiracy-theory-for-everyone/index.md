---
title: "I'll add one conspiracy theory for everyone listening: After STP's source was out there, DLSS4 'transformer' magically gained 'sharpness' but I don't believe it was from the ML model change at all, instead I think they just introduced the same error feedback mechanism in STP ..."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2030722033286328426"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2030722033286328426"
date: 2026-03-08
archived: 2026-08-23
status: draft
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "I'll add one conspiracy theory for everyone listening: After STP's source was out there, DLSS4 'transformer' magically gained 'sharpness' but I don't believe it was from the ML model change at all, instead I think they just introduced the same error feedback mechanism in STP ..."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2030722033286328426
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-03-08 19:07:16

## Thread

**1/**

I'll add one conspiracy theory for everyone listening: After STP's source was out there, DLSS4 'transformer' magically gained 'sharpness' but I don't believe it was from the ML model change at all, instead I think they just introduced the same error feedback mechanism in STP ...

Branches: [[2026-03-08-gindi4711-did-they-not-just-use-more-historical-frames-to]]

**2/**

Specifically STP samples feedback at the position of the input pixels, and uses that difference as an error term estimating the amount of blur introduced, one can subtract out some amount of that 'error' to sharpen ...

**3/**

Of course that idea isn't strictly new either, fluid sims with advection use similar logic to sharpen. So I'm just another human building on the masters of the past. One can start to go beyond sharpening with this technique and get into local contrast adaption too ...

**4/**

One of the marketing points of DLSS4 was 'sharpness' but it didn't actually resolve details to a higher frequency than prior, instead it just gets to a higher contrast, and then they con the consumer with that ...

**5/**

Another trick one can employ, and something I used often as a pro photographer, was to deliberately thin or thicken features with sub-pixel precision during enlargement. Meaning you can take a 'feature' and thin it below source nyquist. And people go 'wow' it's detailed ...

**6/**

So for instance one can take a input (lower-resolution) feature and simultaneously increase it's contrast while reducing it's thickness (when enlarged) in an energy preserving way. Can use signal bounds to estimate how much contrast and thus thin-ness one can push the feature ...

**7/**

This gets easier with color signals because you can take the minimum bounds of the three channels, this is actually exactly what CAS does (just applied in a context without enlargement) ...

**8/**

Anyway all this stuff is easy to artistically shape analytically in shader code, and never needed any kind of ML to be implemented (in fact ML would be slow, because it cannot do max/min style logic!!!).
