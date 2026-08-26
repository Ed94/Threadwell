---
title: "@NOTimothyLottes Best guess from what they have said is they want unrestricted access to the command processor/ultra-threaded dispatch processor(micro-engine scheduler) to implement their own scheduling program(targeting specific CUs for example)."
type: archive
source: twitter
source_url: "https://x.com/LeviathanGamer2/status/1880503685534638343"
author: "LeviathanGamer"
handle: LeviathanGamer2
post_id: "1880503685534638343"
date: 2025-01-18
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Best guess from what they have said is they want unrestricted access to the command processor/ultra-threaded dispatch processor(micro-engine scheduler) to implement their own scheduling program(targeting specific CUs for example)."
in_reply_to: ""
parent_post_id: "1880479856632426572"
---

## Source

- URL: https://x.com/LeviathanGamer2/status/1880503685534638343
- Author: LeviathanGamer (@LeviathanGamer2)
- Posted: 2025-01-18 06:33:11

## Branch

**1/** **@LeviathanGamer2** ^1880503685534638343

**@NOTimothyLottes**

Best guess from what they have said is they want unrestricted access to the command processor/ultra-threaded dispatch processor(micro-engine scheduler) to implement their own scheduling program(targeting specific CUs for example).

**2/** **@NOTimothyLottes** ^1880606749671190680

**@LeviathanGamer2**

That is the part that is likely workaroundable (for example if programs are CU aware, then they can choose to exit and open up those CUs to another launch)

**3/** **@LeviathanGamer2** ^1880647971743932701

**@NOTimothyLottes**

I am assuming you mean ExecuteIndirect? As far as I am aware, you can't explicitly schedule to a target CU without disabling CUs. You are at the mercy of the driver, which might result in poor latency(mainly for a workload you might want to share across multiple GPUs).

**4/** **@NOTimothyLottes** ^1880679657315733597

**@LeviathanGamer2**

If you have persistent workgroups, that have fully filled the GPU, when you launch work, nothing happens until waves choose to exit, so CU aware waves can choose to exit, and the HW will restrict its launch to the newly open CUs I believe

**5/** **@NOTimothyLottes** ^1880680467122536572

**@LeviathanGamer2**

Also besides adjusting schedule priority and avoiding TDRs, there is little reason to launch at all. Just reuse existing waves with fixed VGPR counts.

**6/** **@NOTimothyLottes** ^1880682699016540277

**@LeviathanGamer2**

From a latency perspective the worst option one has is to "launch work" in response to something. The best option is to already be running on the machine and respond to something you'd polled from a memory partition that is set to bypass cache (which AMD already exposes on PC)

**7/** **@LeviathanGamer2** ^1880693145513722176

**@NOTimothyLottes**

Yeah, I think the use case would be passing work from 1 GPU to another GPU, and you would want to launch immediately and try to have low LDS/Cache conflicts while also having the highest priority, so you would want a specific CU for that. Still, that is spitballing an edge case.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-01-18-good-landmine-to-step-on-amd-vs-hotz]]
