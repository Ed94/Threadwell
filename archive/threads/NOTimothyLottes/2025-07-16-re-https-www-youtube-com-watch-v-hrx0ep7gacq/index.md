---
title: "Re  https://www.youtube.com/watch?v=hRX0Ep7gacQ - Actually I'm not at all surprised they used FSR1, because it's damn fast, this title was targeting 60Hz, and it has a boat load of fast dynamic and/or transparent stuff."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1945609535067947204"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1945609535067947204"
date: 2025-07-16
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Re  https://www.youtube.com/watch?v=hRX0Ep7gacQ - Actually I'm not at all surprised they used FSR1, because it's damn fast, this title was targeting 60Hz, and it has a boat load of fast dynamic and/or transparent stuff."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1945609535067947204
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-07-16 22:20:35

## Thread

**1/** **@NOTimothyLottes** ^1945609535067947204

Re  https://www.youtube.com/watch?v=hRX0Ep7gacQ - Actually I'm not at all surprised they used FSR1, because it's damn fast, this title was targeting 60Hz, and it has a boat load of fast dynamic and/or transparent stuff. So no ghosting issues. Instead of trashing them, I'd thank them ...

**2/** **@ThreatInteract** ^1946588727515709945

**@NOTimothyLottes**

1/2 
"It looks soft"
It's millions of times more clear than any DLSS game shown. Where was "soft" when CNN model would destroy games with extreme motion smudging?

4xMSAA (a proper implementation) 1080p integer scaled on a 4k display looks far better than 4k DLSS performance.

**3/** **@ThreatInteract** ^1946590260366114896

**@NOTimothyLottes**

2/2
@dark1x
is acting like because something is "old" that makes the use unjustified. Very few games with FSR1 used MLAA before the FSR1 pass, especially nothing as polished as SMAA so the approach is arguably new.

**4/** **@NOTimothyLottes** ^1946603002493603890

**@ThreatInteract** **@dark1x**

I can confirm that FSR1 does require anti-aliased input (something like an MLAA with continuous gradients). Otherwise it cannot correctly determine edge angle.

**5/** **@NOTimothyLottes** ^1946603734101872703

**@ThreatInteract** **@dark1x**

FSR1 is not well paired with say 4xMSAA because those long 4 steps in a near axis aligned edge look axis aligned to FSR1. It only has a 4x4 pixel box of analysis (and doesn't use the 4 corners)

**6/** **@NOTimothyLottes** ^1946604405752483945

**@ThreatInteract** **@dark1x**

If you want a good answer to scaling MSAA youd need to do a custom MSAA shader resolve that scales and is reading the original sample values. And NV hardware is fantastic at that too.

**7/** **@AgileJebrim** ^1946608828793204915

Or consider an area-based anti-aliasing approach, which is really good at maintaining conservation of energy and avoiding the flickering of small details. Michael Cosman at E&S patented such an approach back in the 90s. It looks like Michel A Rohner has his own similar approach here.

He also mentions you. :P

https://anti-aliasing.com

![](https://pbs.twimg.com/media/GwO-ac1W4AAv1mH?format=jpg&name=orig)

**8/** **@NOTimothyLottes** ^1946614628236026212

**@AgileJebrim** **@ThreatInteract** **@dark1x**

Oh yeah I love the area approaches. Few humans actually understand or have seen how good actual energy conservation looks, but once you try it, there is no going back.

**9/** **@NOTimothyLottes** ^1946615996111810944

**@AgileJebrim** **@ThreatInteract** **@dark1x**

In many of my engines I render a full 360 degree equal texel area warped octahedron with fixed axis. Then at end of frame I project a cylindrical wide angle projection from that, applying the camera rotation. This makes camera rotation energy preserving ...

**10/** **@NOTimothyLottes** ^1946616562888118449

**@AgileJebrim** **@ThreatInteract** **@dark1x**

... while it's a half step towards full energy preservation, that alone shows massive perceptual benefit. When you have a point renderer that does sub-pixel offsets, it's possible to approach energy preservation in translation too

**11/** **@NOTimothyLottes** ^1946617163629854992

**@AgileJebrim** **@ThreatInteract** **@dark1x**

A human with perfect 256-step sub-pixel granularity energy conserving AA can better predict and target using a lower resolution display than a high res display with say no-aa raster with SMAA. It's not even close.
