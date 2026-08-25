---
title: "Often overlooked aspect of GPU perf scaling"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1883566551120670753"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1883566551120670753"
date: 2025-01-26
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Often overlooked aspect of GPU perf scaling"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1883566551120670753
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-01-26 17:23:55

## Thread

**1/** **@NOTimothyLottes** ^1883566551120670753

Often overlooked aspect of GPU perf scaling
Shaders run at two rates
(1.) Cold I$ and K$ rate [significantly slower]
(2.) Warm I$ and K$ rate
You actually need jobs with small wave count to be sharing the same I$ and K$ across waves (cannot be latency sensitive)

**2/** **@NOTimothyLottes** ^1883569276973707397

Big problem with mass amounts of artist graph authored material shaders paired with raster, 
(1.) More materials
(2.) GPU kicks work as wide as possible (due to limited ROP queue size)
Both amplify the amount of cold cache work

**3/** **@NOTimothyLottes** ^1883569959286313322

Very common to look even at full-screen passes and see quite long first waves/SIMD (cold caches), followed by later warm-cache steady state. As GPUs get huge, it pushes more and more waves into the cold-cache region. Scaling-TAAs do the same by reducing render resolution.

Branches: [[archive/threads/NOTimothyLottes/2025-01-26-often-overlooked-aspect-of-gpu-perf-scaling/2025-01-27-Varaquilex-a-visualization-of-said-cold-caches-on-a-cs]]

**4/** **@NOTimothyLottes** ^1883570605909590084

So quite literally the smaller the GPU (aka mobile), the more possible benefits from scaling-TAAs getting reduced resolution, because the cold-cache effects are minimized, etc. But with say the 5090, scaling-TAAs can drop whole GPU efficiency by a substantial amount

**5/** **@NOTimothyLottes** ^1883571920211529760

NVIDIA has load prefetch hints (load more lines than required for the load), and AMD should ideally start including the same for both K$ and D$, so one can at least reduce worst case latency. This doesn't solve bandwidth duplication of wide work distribution though.

**6/** **@NOTimothyLottes** ^1883572955529252878

There are a few different perf wins from decoupling shading from raster, one is the reduction of cold cache effects. One can loop through waves of work in the same material shader, without exit, without reload of constants, etc.

**7/** **@NOTimothyLottes** ^1883574057180021045

Decoupled shading moves a subset of the shading data [material lookup] from interpolated (and thus distributed duplication) to non-temporal streaming (no duplication).

**8/** **@NOTimothyLottes** ^1883574463771676674

Likewise if it's same-material same-wave, aka one wave is looping through a local collection of surface, the remaining non-material sampling (that is interpolated) has a higher likely hood of hitting in the cache [less ultimate duplication of data across the chip]

**9/** **@NOTimothyLottes** ^1883575590445576272

In modern times with scaling-TAAs and maximum negative mip-bias, by reducing render resolution and maximizing frame rate, one is also minimizing cache reuse. So instead of say shading all the near samples at the same time, each are now divided across perhaps 32 frames

**10/** **@NOTimothyLottes** ^1883576673381285955

Thus a massive mismatch between data layout and data usage. The data is stored (and compressed) localized and layered (multiple textures/material), but is increasingly being used in an effectively random access. Both scaling-TAAs and RT are guilty here.

**11/** **@NOTimothyLottes** ^1883579422676320293

Games that rely on a mix of {heavy deferred shading, scaling-TAAs (reduced render res), RT noise reduction, and frame generation} are scaling poorly (bad engineering) and scale as a function of increased {latency, artifacts}

**12/** **@NOTimothyLottes** ^1883579950051266839

Meanwhile games that are still engineered more like vintage games {high res, low try density, simple baked lightmap textures mostly, MSAA} are scaling relatively well getting high FPS and low latency

**13/** **@NOTimothyLottes** ^1883580512171942335

Ultimately all of this hints that it would be better if the per-frame workloads are closer to the vintage games (no-TAA, no frame-gen), and instead one amortizes shading into something that "bakes" in realtime amortized across many frames into the vintage style engine data

Branches: [[archive/threads/NOTimothyLottes/2025-01-26-often-overlooked-aspect-of-gpu-perf-scaling/2025-01-26-bmcnett-my-take-is-similar-but-i-also-feel-that-a-lot-of]]

**14/** **@NOTimothyLottes** ^1883587813092069667

All these "AI" spatial-temporal denoise-scaling-TAAs are ultimately just doing really expensive logic to try to reconstruct the surface material properties at high res and local lighting from a blurry/noisy mess then apply the local conditions to the material

**15/** **@NOTimothyLottes** ^1883588874582298925

Which is perhaps stupid given the games already easily know the exact high-res material properties, why try to "infer" them burning TOps of logic and heating your office.

**16/** **@NOTimothyLottes** ^1883590137445224708

Scaling-denoise-TAAs do hint thought that perhaps the academic methods games use for BPR and shading are quite lacking in terms of amortization of costs.

**17/** **@NOTimothyLottes** ^1883590627285409935

Frame-gen when it "works" ok is just an alpha blend between two states. Clearly an engine could be doing that too instead of reshading everything every frame. And an engine could choose when to do that vs something else to avoid artifacts, something a frame-gen cannot do.

**18/** **@NOTimothyLottes** ^1883591956598845661

Ultimately the industry will choose if to devolve into AI generated slop-ware where IHVs black box more and more of your engine and you get more and more trapped and lazy. Or break out and do something better and control your own destiny.

Branches: [[archive/threads/NOTimothyLottes/2025-01-26-often-overlooked-aspect-of-gpu-perf-scaling/2025-01-26-noop_dev-i-thought-framegen-was-just-an-offspring-of-mpeg2]]
