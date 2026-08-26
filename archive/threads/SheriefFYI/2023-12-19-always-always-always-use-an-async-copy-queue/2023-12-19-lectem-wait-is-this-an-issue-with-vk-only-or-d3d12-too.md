---
title: "@NOTimothyLottes @SheriefFYI Wait, is this an issue with VK only or D3D12 too?"
type: archive
source: twitter
source_url: "https://x.com/lectem/status/1737171397477106038"
author: "Clément Grégoire"
handle: lectem
post_id: "1737171397477106038"
date: 2023-12-19
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SheriefFYI
description: "@NOTimothyLottes @SheriefFYI Wait, is this an issue with VK only or D3D12 too?"
in_reply_to: ""
parent_post_id: "1737161181524095352"
---

## Source

- URL: https://x.com/lectem/status/1737171397477106038
- Author: Clément Grégoire (@lectem)
- Posted: 2023-12-19 18:01:50

## Branch

**1/** **@lectem** ^1737171397477106038

**@NOTimothyLottes** **@SheriefFYI**

Wait, is this an issue with VK only or D3D12 too?

**2/** **@SheriefFYI** ^1737171797991190978

**@lectem** **@NOTimothyLottes**

both, it’s part of WDDM architecture.

**3/** **@lectem** ^1737172605260443945

**@SheriefFYI** **@NOTimothyLottes**

Oh damn, I was under the impression that it was not really expensive as Unreal does use them quite a bit and I never saw issues with that...
How big of an issue can it be?

**4/** **@SheriefFYI** ^1737173083008487777

**@lectem** **@NOTimothyLottes**

depends on how long your wait is usually. if the fence is signaled early enough the wait can become a no-op.

**5/** **@lectem** ^1737173826050392448

**@SheriefFYI** **@NOTimothyLottes**

In the scenario I've measured it was basicly copies or compute done at the beginning of frame so the gfx queue was definitely waiting and signal was after work.
Didn't really measure but it didn't seem that big of an issue. Maybe because it was at beginning / end of cmd exec?

**6/** **@lectem** ^1737174096947954046

**@SheriefFYI** **@NOTimothyLottes**

Or by early enough do you mean that if the wait is short (under millisec or something ) it's OK?

**7/** **@SheriefFYI** ^1737174479967568185

**@lectem** **@NOTimothyLottes**

please measure and then we can talk.

**8/** **@lectem** ^1737175062585696506

**@SheriefFYI** **@NOTimothyLottes**

I'll try to find a few captures during the week.

## Related

- Spine: [[archive/threads/SheriefFYI/2023-12-19-always-always-always-use-an-async-copy-queue]]
