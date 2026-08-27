---
title: "Implemented a simple linear estimator for distance field value."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1320266867852922880"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1320266867852922880"
date: 2020-10-25
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Implemented a simple linear estimator for distance field value."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1320266867852922880
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2020-10-25 07:32:05

## Thread

**1/** **@SebAaltonen** ^1320266867852922880

Implemented a simple linear estimator for distance field value. Stored difference to this estimate as pre-process step and zlib compressed it...

Results:
Uncompressed = 926 MB
zlib = 552 MB (59%)
zlib with pre-process = 129 MB (14%)

Similar trick works for heightmap compression

![](https://pbs.twimg.com/media/ElKD2eUXIAIv9V-?format=jpg&name=orig)
![](https://pbs.twimg.com/media/ElKGqGoW0AAxIGP?format=jpg&name=orig)

**2/** **@SebAaltonen** ^1320267261723222016

When compressing SDF data, you can use the eikonal equation as the estimator instead of a linear estimate. This is better. Didn't yet implement it.

https://en.wikipedia.org/wiki/Eikonal_equation

https://www.shadertoy.com/view/MtK3zD

**3/** **@SebAaltonen** ^1320268159811801089

For completeness, here's the abs_diff functions needed for the compressor and the decompressor.

![](https://pbs.twimg.com/media/ElKI0_dW0AI3ZPg?format=png&name=orig)

**4/** **@SebAaltonen** ^1320269116712886274

And the inverse preprocessing step you use after the zlib decompress:

![](https://pbs.twimg.com/media/ElKJqRyWMAAmmpk?format=jpg&name=orig)

**5/** **@SebAaltonen** ^1320269630896803840

The first (X=0, Y=0, Z=0) planes need different code. Here I simply don't preprocess them. For the first scanline you need linear 1d estimate (x-2, x-1 is good). For the first plane you need 2d estimate.
