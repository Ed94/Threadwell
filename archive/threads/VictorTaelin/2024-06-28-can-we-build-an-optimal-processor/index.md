---
title: "Can we build an optimal processor?"
type: archive
source: twitter
source_url: "https://x.com/VictorTaelin/status/1806690584670679387"
author: "Taelin"
handle: VictorTaelin
post_id: "1806690584670679387"
date: 2024-06-28
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - VictorTaelin
  - erasure
  - llm
description: "Can we build an optimal processor?"
in_reply_to: ""
---

## Source

- URL: https://x.com/VictorTaelin/status/1806690584670679387
- Author: Taelin (@VictorTaelin)
- Posted: 2024-06-28 14:06:16

## Thread

**1/** **@VictorTaelin** ^1806690584670679387

Can we build an optimal processor?

In 1990, Lamping proved optimal λ-calculus evaluation can only be done via graphical interaction systems, because, for any order of evaluation (in a syntax tree), there is a sub-optimal counter-example.

In 1997, Lafont has shown that Turing Machines and Cellular Automata are just interaction systems. He then defined Interaction Combinators as an universal interaction system, to which any other can be translated while preserving the same complexity and degree of parallelism.

This, as far as theory is concerned, implies Interaction Combinators are an optimal model of computation, since they are capable of emulating any other without losing efficiency. The opposite isn't true: emulating ICs on λ-Calculus increases complexity, and emulating ICs on Turing Machines decreases parallelism.

"That's theory. Isn't there a huge practical overhead?"

Not inherently, and remaining overheads are engineering matters:

As a functional runtime: HVM's affine lambdas currently use ~2x less memory than their counterparts in Haskell GHC. The vast majority of Cabal/Stack can be translated to efficient HVM. Emulating full lambdas still has a ~5x overhead, but better translations are within reach.

As a procedural runtime: HVM has the same underlying core as Rust (the affine λ-calculus), thus, the exact same compilation approach applies. Rust currently is almost as fast as C, thus, there is no barrier to making HVM as fast as C too, once given a proper procedural codegen. This has not been done yet, which makes its current single-core performance sub-par.

We could do all that to let HVM optimally hardness the computing power of existing hardware (CPUs, GPUs...). Or we could go deeper and ask: can Interaction Combinators also optimally harness the computing power of our underlying universe?

"What would an HVM chip look like?"

Since Interaction Combinators don't inherently suffer from the Vonn Neumann bottleneck (they're optimal!), an IC chip would remove the separation between memory and computation. It could be materialized as a 3D grid of interaction cores, where each unit stores a 192-bit node (1x 48-bit label + 3x 48-bit pointers), and performs an interaction by sending and receiving a 144-bit message to its main neighbor.

This embeds the system into a 3D automata, which performs interactions at the propagation speed of light. Perhaps (just perhaps?), on low-order numeric computations (like MatMul), such hypothetical processor would not outperform existing hardware. Yet, on higher-order algorithms, including SMT solvers and discrete program search (which is, coincidently, the #1 contender on the LLM-defying  "ARC-AGI challenge"), such processor would significantly outperform existing alternatives, computing as efficiently as its underlying physically universe allows.

![](https://pbs.twimg.com/media/GRKmWZvWgAAs7U0?format=jpg&name=orig)

Branches: [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-zygomeb-when-seed-round-for-the-hardware-shop]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-edefazio-looked-into-ivan-sutherlands-work-at-the-arc]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-_maestro_04-youre-my-certified-hardware-guy-any-thoughts]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-nathan___gage-have-you-looked-into-topological-deep-learning]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-khlorghaal-i-desire-low-power-hardware-thats-highly]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-ccconstant1ne-curious-because-what-you-describe-sounds-very]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-eabili0-well-thats-basically-a-description-of-the-human]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-BitcoinBananaBY-message-passing-graph-neural-network]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-_Felipe-does-talking-about-physical-efficiency-in-terms]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-okwalerie-reading-graphical-interaction-systems-im-hearing]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-thingcreator-has-anyone-looked-into-how-ics-interact-with]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-tiagoefreitas-how-difficult-is-it-to-be-ahead-of-your-time]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-28-perdro_sa-your-posts-about-these-topics-are-so-fascinated-i]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-29-luisfuturist-i-got-inspired-and-made-a-song-about-it-https]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-29-HDPbilly-thread]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-29-ssskryl-is-this-similar-to-the-computation-model]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-29-vertinski-good-content-i-wish-for-a-lot-more-connections]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-29-noam_yy-how-does-a-commutation-interaction-work-youd-need]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-06-30-fadhilAlf-i-dont-understand-do-i-need-to-know-electronics]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-07-12-tribbloid-horrible-idea-if-you-want-to-rewrite-circuit-for]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-07-12-dela3499-interaction-combinators-arent-optimal-as-theyre]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-07-17-YaccConstructor-cool-a-few-technical-questions-why-3-dimensions]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-08-07-lnwave-bring-back-the-lisp-machines]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2024-10-08-pepijndevos-why-a-3d-system-chips-are-largely-planar-and]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2025-01-17-DirectHearingx-optimal-processors-require-unconventional]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2025-06-22-VisionaireAI-optimal-processors-are-cosmic-dreams-tangled-in]], [[archive/threads/VictorTaelin/2024-06-28-can-we-build-an-optimal-processor/2025-07-19-VisionaireAI-technologys-relentless-march-outpaces-biologys]]
