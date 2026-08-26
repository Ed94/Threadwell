---
title: "just saving my last conversation with Fable on this entire flattener debacle."
type: archive
source: twitter
source_url: "https://x.com/VictorTaelin/status/2085409601034371371"
author: "Taelin"
handle: VictorTaelin
post_id: "2085409601034371371"
date: 2026-08-06
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - VictorTaelin
  - pattern-matching
  - bend
  - llm
description: "just saving my last conversation with Fable on this entire flattener debacle."
in_reply_to: ""
---

## Source

- URL: https://x.com/VictorTaelin/status/2085409601034371371
- Author: Taelin (@VictorTaelin)
- Posted: 2026-08-06 16:56:08

## Thread

**1/** **@VictorTaelin** ^2085409601034371371

just saving my last conversation with Fable on this entire flattener debacle. I like it because it seems to be on the exact edge of what AI's still can't do (today)

the task was to implement an "elegant" pattern-match flattener for Bend's core. the one Fable had written was extremely contrived (like, 3x longer than it should) and I was trying to get it to find the simplest possible implementation.

note this problem is not new. converting pattern-matches into decision trees has been described in 1985. it is implemented in nearly every proof assistant. Fable knows how to build one.

yet, what I demanded it something *slightly* different. a minimal implementation on Bend's context, which has a few nuances, like being based on point-free λ-trees. these nuances were enough to put it out of its zone of comfort, and, despite being an extraordinary model, it still couldn't make the jump from the textbook algorithm it knows, to a general solution on Bend's context

that's why its code was so big. it was stuffing layers of duct taping, to compensate for the fact it couldn't see the general solution. 5 days, 15+ attempts, and the function barely got smaller. I even gave it a step-by-step derivation, but it STILL failed. ultimately, I just decided to write the algorithm myself. to its credit, my own solutions still had some gaps. I guess we're both equally stupid nowadays, but at least we managed to fix it together. below is this last conversation (summarized)

this is a bit embarrassing because I burned millions of tokens and wasted a lot of time on something I honestly could do in an hour. that's stupid, and a good argument that AI is (still) a tool that requires skill, and can be misused in dumb ways that tank your productivity and end up being detrimental rather than good

![](https://pbs.twimg.com/media/HPDc5vLWoAAXkOH?format=jpg&name=orig)

Branches: [[archive/threads/VictorTaelin/2026-08-06-just-saving-my-last-conversation-with-fable-on/2026-08-06-yacineMTB-i-think-the-ability-to-make-a-computer-program]]
