---
title: "What separates an engineer from a developer is keeping the USER’s problem front and center in every architectural design decision."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/2097298982703649017"
author: "Jebrim"
handle: AgileJebrim
post_id: "2097298982703649017"
date: 2026-09-08
archived: 2026-11-16
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "What separates an engineer from a developer is keeping the USER’s problem front and center in every architectural design decision."
in_reply_to: ""
---

## Source

- URL: https://x.com/AgileJebrim/status/2097298982703649017
- Author: Jebrim (@AgileJebrim)
- Posted: 2026-09-08 12:20:18

## Thread

**1/** **@AgileJebrim** ^2097298982703649017

What separates an engineer from a developer is keeping the USER’s problem front and center in every architectural design decision. NFR-driven constraints matter. Bidirectional traceability matters.

And yet I keep hearing people spend hours debating the pros and cons of this language feature, that coding style, and that framework platform, all completely divorced from how they enable devs to offer customers the highest quality solutions for the lowest price.

The end user doesn’t care if you used const by default, a borrow checker, or advanced metaprogramming tools. How do these trace back to providing an affordable quality attribute that they do care about?

If you’re not choosing/designing your software stack with the quality of the user experience front and center, you’re just wasting time and needlessly adding cost, making yourself less competitive against others offering similar functionality but with better quality execution.

For the particular constraints I choose to prioritize within my projects, everything revolves first and foremost around eliminating lag/stutter for the end user, followed by secondary priorities of lowering both dev costs and hardware operating costs of using the software. Higher quality, lower costs.

EVERY design tradeoff decision made for delivering on a functional requirement revolves around whether I can deliver on these 3 things that drive the nonfunctional requirements. If a particular design decision and implementation cannot trace itself back to both a functional and nonfunctional requirement, then it’s both a waste of time and counterproductive.

I pursue portable isochronous data parallel execution with static resource allocation because that’s the logical conclusion analyzing these NFRs lead to. They’re not optional if one wants to achieve the goals set forth for offering the best quality of service for the lowest price, regardless of the specific functional nature of the project in question.

If it helps for your software product to be interactive and immediately responsive to user input, then it can benefit from my approach. This isn’t just for my own niche problem domain.

The tools don’t currently exist for making it cheap and easy to rapidly produce such software; thus we’ve gotta make them ourselves. To lower the cost of such tools, we should make them publicly available and treat them as a product too.

Minimally, in a buyer’s market, product cost = (dev cost / number of customers) + profit margin.

Maximally, in a seller’s market, product cost = value add (cost of customer’s alternatives - their savings & profit by choosing us).

This latter is why custom pricing exists for B2B sales; we must be cheaper and less risky than the cost of them either rolling their own or going with a competitor. It unfortunately does have a scaling problem, so we do want to choose a bit of both. Different customers value real-time guarantees and low costs differently. We’re also constrained by the reality of most user software running on general purpose multitasking operating systems running third party software, which cannot perfectly guarantee isochrony.

This thus all leads to us offering multiple tiered products. Serve the customers for which our NFRs are a cheaper nice-to-have, but not hard guarantees, gaining scale and lowering costs in the process, whilst simultaneously targeting the safety/mission-critical market for which our value add is non-optional and demands a safety-certified real-time environment with the most premium quality.

Every internal debate revolves around how to deliver on all of these aforementioned goals. They must be front and center in every discussion until this problem of providing a solution for the cheap and rapid production of guaranteed hard real-time (stutter-free) software on cheap hardware is solved. Only after that can we (and our future customers) focus on the functionality of the end user software itself, regardless of the domain in question.

Branches: [[archive/threads/AgileJebrim/2026-09-08-what-separates-an-engineer-from-a-developer-is/2026-09-08-ExodusPgame-are-you-planning-a-closed-or-open-beta-anytime]], [[archive/threads/AgileJebrim/2026-09-08-what-separates-an-engineer-from-a-developer-is/2026-09-09-stikves-that-is-a-maturity-developers-will-have-to-learn]]

**2/** **@AgileJebrim** ^2097301188068692290

There is a major tradeoff that this approach comes with, which is that all software wanting to be stutter-free must be rewritten from scratch, likely also including all the legacy data that it depends upon. This is a real greater short-term cost that business customers must account for. Those who do choose us will however over the long-term have the potential to disrupt existing industries and compete against the legacy big players that decide not to proactively lead.

I expect developers working on new greenfield projects without existing legacy content to hold them back will likely be our primary customers.

**3/** **@SebAaltonen** ^2097360487700738543

**@AgileJebrim**

That's the core issue with high performance code. Only seasoned experts are able to write it. Requires architectural planning and rigor. Hard to scale to large teams. In gamedev, code isn't the product. Code has to be good enough to ship. There's always more important stuff.

**4/** **@AgileJebrim** ^2097371437296230681

**@SebAaltonen**

Part of lowering dev costs is providing the tools that automate achieving these quality attributes to then avoid needing high levels of skill among both the programmers and content creators. The tools should prevent them from shooting themselves in the foot on performance.
