---
title: "@AgileJebrim ptx, my ass: https://redplait.blogspot.com/2026/08/parser-of-ptx-instructions.html"
type: archive
source: twitter
source_url: "https://x.com/real_redp/status/2091228915142472141"
author: "red plait"
handle: real_redp
post_id: "2091228915142472141"
date: 2026-08-22
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim ptx, my ass: https://redplait.blogspot.com/2026/08/parser-of-ptx-instructions.html"
in_reply_to: ""
parent_post_id: "2090977998593827103"
---

## Source

- URL: https://x.com/real_redp/status/2091228915142472141
- Author: red plait (@real_redp)
- Posted: 2026-08-22 18:20:01

## Branch

**1/** **@real_redp** ^2091228915142472141

**@AgileJebrim**

ptx, my ass: https://redplait.blogspot.com/2026/08/parser-of-ptx-instructions.html

**2/** **@AgileJebrim** ^2091230269747397000

**@real_redp**

FWIW I target SPIR-V in part because it’s a binary format (ASCII asm sucks) and in part because it’s more portable than PTX.

**3/** **@AgileJebrim** ^2091230640842612865

**@real_redp**

The main advantage of PTX is that it gets you direct access to a lower level API into NVIDIA hardware than anything else available unless we manage to reverse engineer PSO binary caches (something I’m still debating attempting) to write directly in SASS.

**4/** **@real_redp** ^2091231795350044950

**@AgileJebrim**

he-he
I made tool to patch sass

**5/** **@AgileJebrim** ^2091233823228940511

**@real_redp**

Which generation? Is it available?

**6/** **@AgileJebrim** ^2091234694201331796

**@real_redp**

I see you have a disassembler. It looks to be CUDA-specific? I’d love to see you do one for Vulkan PSOs too, especially for Ampere.
https://github.com/redplait/denvdis/tree/master

**7/** **@AgileJebrim** ^2091235158682730697

**@real_redp**

Actually, I think this path might work as is combined with the Cubin extension in Vulkan.
“sed-like tool for inline patching of sass instructions within cubin files.”
Lots of possibilities! 🤔

How mature is this?

**8/** **@real_redp** ^2091235642898325872

**@AgileJebrim**

enough to do crazy things like https://redplait.blogspot.com/2026/07/optimization-of-sass-stall-counts.html

## Related

- Spine: [[archive/threads/AgileJebrim/2026-08-22-start-with-spir-v-or-ptx-instead]]
