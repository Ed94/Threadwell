---
title: "Go preserving struct field order gives more predictable control over layout, but Rust, i think, also provides explicit layout guarantees through #[repr(C)]."
type: archive
source: twitter
source_url: "https://x.com/VictoriqueM/status/2118353676192399673"
author: "Victoria"
handle: VictoriqueM
post_id: "2118353676192399673"
date: 2026-11-05
archived: 2026-11-16
draft: false
tags:
  - archive
  - twitter
  - valyala
description: "Go preserving struct field order gives more predictable control over layout, but Rust, i think, also provides explicit layout guarantees through #[repr(C)]."
in_reply_to: ""
parent_post_id: "2118349666911768669"
---

## Source

- URL: https://x.com/VictoriqueM/status/2118353676192399673
- Author: Victoria (@VictoriqueM)
- Posted: 2026-11-05 14:44:08

## Branch

**1/** **@VictoriqueM** ^2118353676192399673

Go preserving struct field order gives more predictable control over layout, but Rust, i think, also provides explicit layout guarantees through #[repr(C)].
 
so i guess it's more default layout semantics vs an inherent advantage in the generated machine code.

buuuut, Go's predictable memory layout is genuinely valuable for performance-sensitive code, cos it preserves struct field declaration order, giving us straightforward control over field placement, alignment and padding without requiring additional layout annotations, etc... 

Win Win

## Related

- Spine: [[archive/threads/valyala/2026-11-05-til-you-can-increase-hot-loop-performance-by-20x]]
