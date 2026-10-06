---
title: "@NOTimothyLottes Funny that they say \"actual fp32 compute\"."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/2106630618859639291"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "2106630618859639291"
date: 2026-10-04
archived: 2026-10-06
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Funny that they say \"actual fp32 compute\"."
in_reply_to: ""
parent_post_id: "2106566586819609002"
---

## Source

- URL: https://x.com/SebAaltonen/status/2106630618859639291
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2026-10-04 06:20:53

## Branch

**1/** **@SebAaltonen** ^2106630618859639291

**@NOTimothyLottes**

Funny that they say "actual fp32 compute". Meaning without the second ALU pipe, like it would be useless. Double ALU rate isn't useless, even if it requires pairing and even if it only makes games 20% faster on average. And they use the single ALU pipe math in their ALU/BW chart.

**2/** **@SebAaltonen** ^2106631423306195057

**@NOTimothyLottes**

The reason we don't see higher gain from the second ALU pipe is that there's so many shaders that are bound by samplers or memory. ALU/BW rate is already going down 42%, even with double ALU pipes, and that's the problem right there. Lots of BW bound shaders.

**3/** **@LeviathanGamer2** ^2106649813001314342

**@SebAaltonen** **@NOTimothyLottes**

Here is also the Dual-issue supporting instructions on RDNA3 onwards, which is quite limited:

![](https://pbs.twimg.com/media/HTxS1y8XMAEB2aD?format=jpg&name=orig)

**4/** **@LeviathanGamer2** ^2106650148780536074

**@SebAaltonen** **@NOTimothyLottes**

Here is CDNA5. So far driver side this is identical for RDNA5. They have a new encoding VOPD3 as well as expanded VOPD:

![](https://pbs.twimg.com/media/HTxTJGOWwAAC94j?format=jpg&name=orig)
![](https://pbs.twimg.com/media/HTxTJXEWcAEObSn?format=jpg&name=orig)

**5/** **@SebAaltonen** ^2106736298186944626

**@LeviathanGamer2** **@NOTimothyLottes**

Yeah. AMD chose manual dual-issue. Leans 100% on ILP. While Nvidia chose 100% TLP. Second pipeline runs different wave. Feels like history repeating (VLIW vs SIMT back in the day).

**6/** **@SebAaltonen** ^2106736928951304342

**@LeviathanGamer2** **@NOTimothyLottes**

But Nvidia’s approach to double FP ALU pipes didn’t provide more than 30% average gains in games either. Most game shaders are not heavily ALU bound. Or there’s not enough parallelism, especially below 4K resolution.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2026-10-04-thread-serious-talk-on-steamdeck-2-speculation]]
