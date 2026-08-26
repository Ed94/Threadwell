---
title: "I’ve never looked at a real-world optimizer."
type: archive
source: twitter
source_url: "https://x.com/LubaRaphael/status/1872174154872475966"
author: "Raphael Luba"
handle: LubaRaphael
post_id: "1872174154872475966"
date: 2024-12-26
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "I’ve never looked at a real-world optimizer."
in_reply_to: ""
parent_post_id: "1871638900554317934"
---

## Source

- URL: https://x.com/LubaRaphael/status/1872174154872475966
- Author: Raphael Luba (@LubaRaphael)
- Posted: 2024-12-26 06:54:36

## Branch

**1/** **@LubaRaphael** ^1872174154872475966

I’ve never looked at a real-world optimizer. Are they really table-driven so that they would use the same structure as our x64 assembler to figure out instructions and optimizations?
Or are they instead built from a basic operation-to-instruction mapping (like the current x64 backend) plus a thousand rules like "if I detect this kind of pattern, replace it with this instruction sequence"?
If it is the latter, they would use different structures anyways and we could factor out the assembler without impacting the optimizer very much.

## Related

- Spine: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the]]
