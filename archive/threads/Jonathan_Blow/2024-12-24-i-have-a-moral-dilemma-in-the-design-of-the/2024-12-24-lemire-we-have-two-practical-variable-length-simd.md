---
title: "We have two practical variable-length SIMD instruction sets: SVE/SVE2 and RISC-V."
type: archive
source: twitter
source_url: "https://x.com/lemire/status/1871649811981639834"
author: "Daniel Lemire"
handle: lemire
post_id: "1871649811981639834"
date: 2024-12-24
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "We have two practical variable-length SIMD instruction sets: SVE/SVE2 and RISC-V."
in_reply_to: ""
parent_post_id: "1871638900554317934"
---

## Source

- URL: https://x.com/lemire/status/1871649811981639834
- Author: Daniel Lemire (@lemire)
- Posted: 2024-12-24 20:11:03

## Branch

**1/** **@lemire** ^1871649811981639834

We have two practical variable-length SIMD instruction sets: SVE/SVE2 and RISC-V.

I don’t know anyone doing useful mainstream work with SVE/SVE2. It runs on AWS/Graviton… but… anyone using it?  There might be some niche HPC application.

RISC-V might get more mileage in the coming years. Maybe.

I think that the only mainstream software library to support both RISC-V and x64/ARM is the simdutf library (see GitHub). So you can see the intrinsics at play there. It works.

This being said, there is no sign that variable-length is the future…

There are downsides:

1. You often design and test your software with specific registers in mind. What happens when you code is used on different register sizes?

2. With fixed-length registers, you can have fixed-bit masks (e.g., result of a comparison) which maps nicely to and from general purpose registers. Not so with variable length. This makes algorithmic designs harder.

Folks like @geofflangdale and @FUZxxl probably share my skepticism of variable-length designs.

Now: don’t get me wrong… RISC-V is damn sexy. Maybe it is the future. Who knows?

@pshufb may know more about RISC-V.

**2/** **@Jonathan_Blow** ^1871653212622651509

This all makes sense but what about “actually just do everything as scalars and we will schedule it however we schedule it,” which I think is what won in GPUs? Is there a reason to believe that would not win eventually in CPUs?

And for fixed length … people cannot even agree on the length right now … which makes it even more of a hassle.

**3/** **@corsix** ^1871673285098062096

**@Jonathan_Blow** **@lemire** **@rflaherty71**

“actually just do everything as scalars and we will schedule it however we schedule it” — whilst true on some GPUs, not true on all GPU-adjacent things, and even where it _is_ true, if you’re really pushing performance, you need to care about it being scheduled as 32-wide SIMD

**4/** **@Jonathan_Blow** ^1871977920534827033

**@corsix** **@lemire** **@rflaherty71**

If someone writes a program using 4-wide intrinsics, is that really going to help very much at targeting 32-wide? I think the code just has to be written differently.

**5/** **@Jonathan_Blow** ^1871978586389057974

**@corsix** **@lemire** **@rflaherty71**

It’s a weird spot right now because as far as I know, AVX-512 is still kinda failed on Intel CPUs (??), so anyone who actually wants reliable improvement has to stay at 256 and below… is that going to help someone run much better on a tenstorrent chip? Seems dubious.

## Related

- Spine: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the]]
