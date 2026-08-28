---
title: "my god they're maybe finally adding reflection to C++26"
type: archive
source: twitter
source_url: "https://x.com/TylerGlaiel/status/1723970493307552093"
author: "Tyler Glaiel"
handle: TylerGlaiel
post_id: "1723970493307552093"
date: 2023-11-13
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - TylerGlaiel
description: "my god they're maybe finally adding reflection to C++26"
in_reply_to: ""
---

## Source

- URL: https://x.com/TylerGlaiel/status/1723970493307552093
- Author: Tyler Glaiel (@TylerGlaiel)
- Posted: 2023-11-13 07:46:10

## Thread

**1/** **@TylerGlaiel** ^1723970493307552093

my god they're maybe finally adding reflection to C++26

https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2996r0.html

**2/** **@cmuratori** ^1724152404596404631

**@TylerGlaiel**

I can only imagine the fifteen ways they will have managed to make it completely unusable in any scenario where you might actually want reflection.

**3/** **@anicic_filip** ^1724251440422539551

**@cmuratori** **@TylerGlaiel**

What do you normally use for reflection of data in C++ to your game/editor tools?

**4/** **@cmuratori** ^1724252283523707159

**@anicic_filip** **@TylerGlaiel**

A program I wrote.

**5/** **@anicic_filip** ^1724253524467282244

**@cmuratori** **@TylerGlaiel**

Any public alternatives that are decent for small projects, that you tried before?

**6/** **@cmuratori** ^1724256203574833485

**@anicic_filip** **@TylerGlaiel**

I have not tried it, but @rfleury and @AllenWebster4th did one called MetaDesk at one point: https://dion.systems/metadesk.html

**7/** **@rfleury** ^1724257454224236925

**@cmuratori** **@anicic_filip** **@TylerGlaiel** **@AllenWebster4th**

I still use Metadesk for metacode (it is a simpler, metaprogram-/handwriting-tuned JSON-superset text format). My metaprogram just ingests both Metadesk files and my C files, and I can parse/generate whatever I want.

I wrote on one way I use it here:
https://www.rfleury.com/p/table-driven-code-generation

**8/** **@rfleury** ^1724258277989757390

**@cmuratori** **@anicic_filip** **@TylerGlaiel** **@AllenWebster4th**

You can also just use macros to encode stuff directly into your C, or nest & extend C within your metacode language, but I found separate metacode was simpler and mostly without extra hassle, and my metaprogram constructs don't need to be C-like or live within C constructs.

**9/** **@rfleury** ^1724258628725862688

**@cmuratori** **@anicic_filip** **@TylerGlaiel** **@AllenWebster4th**

But yeah, there are loads of options - you just need programs that parse and output text, then you just author the stuff you want in the parsed text. There is no reason why auto-gen'd reflection data needs to exist in your C++ compiler, and frankly it's best if it doesn't.

**10/** **@rfleury** ^1724259422174904802

**@cmuratori** **@anicic_filip** **@TylerGlaiel** **@AllenWebster4th**

(I know Casey knows all of this, but figured I'd add info from my Metadesk-perspective for those reading this thread)

Branches: [[archive/threads/TylerGlaiel/2023-11-13-my-god-theyre-maybe-finally-adding-reflection-to/2023-11-14-anicic_filip-thank-you-for-the-breakdown-ryan-much-appreciated]]
