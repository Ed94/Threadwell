---
title: "@mike_acton Am I right in thinking this is running the entire Pico8 program at every pixel and then discarding all but the specific pixel it cares about? This is..."
type: archive
source: twitter
source_url: "https://x.com/tom_forsyth/status/1673486875947053056"
author: "Tom Forsyth (TODO: fix my heart or die)"
handle: tom_forsyth
post_id: "1673486875947053056"
date: 2023-06-27
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - mike_acton
description: "@mike_acton Am I right in thinking this is running the entire Pico8 program at every pixel and then discarding all but the specific pixel it cares about? This is..."
in_reply_to: ""
parent_post_id: "1673485333084913664"
---

## Source

- URL: https://x.com/tom_forsyth/status/1673486875947053056
- Author: Tom Forsyth (TODO: fix my heart or die) (@tom_forsyth)
- Posted: 2023-06-27 00:22:17

## Branch

**1/** **@tom_forsyth** ^1673486875947053056

**@mike_acton**

Am I right in thinking this is running the entire Pico8 program at every pixel and then discarding all but the specific pixel it cares about? This is... so wrong :-)

**2/** **@mike_acton** ^1673488140429033472

**@tom_forsyth**

Yes and no. It's doing that for an area that matches the draw area of the pico8 (128x128). Then the actual render view is just a texture lookup. I have a few things I could do to reduce it further, but webgpu doesn't have this constraint so not bothering.

**3/** **@tom_forsyth** ^1673489657894690816

**@mike_acton**

I did once contemplate writing a ZX Spectrum emulator like this. It is unclear if there is quite enough horsepower to do this at full speed. Maybe if it transpiled the Z80 code rather than emulating it?

## Related

- Spine: [[archive/threads/mike_acton/2023-06-26-since-2darray-is-working-on-a-pico8-to-burst-lua]]
