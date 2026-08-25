---
title: "The first way people usually learn code compression is by pulling common things out into helper functions, but in my view the complexity of adding a new entry point is often overlooked, and things quickly turn into a mess."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/2061619837877780961"
author: "Ryan Fleury"
handle: rfleury
post_id: "2061619837877780961"
date: 2026-06-02
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "The first way people usually learn code compression is by pulling common things out into helper functions, but in my view the complexity of adding a new entry point is often overlooked, and things quickly turn into a mess."
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/2061619837877780961
- Author: Ryan Fleury (@rfleury)
- Posted: 2026-06-02 01:24:07

## Thread

**1/** @rfleury

The first way people usually learn code compression is by pulling common things out into helper functions, but in my view the complexity of adding a new entry point is often overlooked, and things quickly turn into a mess.

It’s a useful exercise to try compressing code without helper functions, and instead merging similar work by using loops, tables, and reordering. In my experience this leads to dramatically simpler architecture, and it’s a lot easier to keep the whole picture in your head.

Branches: [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-wizplum-what-about-polymorphism-and-inheritance]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-eron_wolf-i-like-giant-matching-functions-with-lots-of]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-jshurmer-very-well-said-it-would-be-useful-to-see-examples]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-Mallchad-ive-been-compressing-in-terms-of-section]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-polloimperial-i-got-a-mess-kind-of-working-fine-but-dirty-with]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-jrjnorton-do-you-have-an-example-or-a-before-and-after-by]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-gcoum-only-way-to-compress-is-dsl-vv-everything-else-is]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-0x6e616461-i-like-using-lambdas-or-local-functions-to]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-Arrghtv-i-completely-agree-adding-a-helper-function]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-SaladeTomate18-entry-point-you-mean-indirection]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-patrickgwsmith-i-like-this-as-it-maps-the-problem-with-input-on]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-vf42-never-thought-of-helper-f-ns-as-code-compression]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-MrModez-i-noticed-focusing-on-the-data-you-work-and-how]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-ChickenBurner2-oh-i-hate-helper-functions-especially-the-ones]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-alienorg-fewer-entry-points-fewer-surprises]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-anicic_filip-im-not-exactly-sure-what-do-you-mean-with-this]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-pbwinston-does-this-imply-if-you-took-an-external]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-sipubot-db]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-pegvvin-cant-tell-just-how-many-times-ive-pulled-out]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-guywald-100-agree-dry-can-be-extremely-overdone-llms-love]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-AlexAegis-yes-a-similar-problem-comes-when-you-follow]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-JoelStransky-ive-come-to-refer-to-declarative-as-just-fucking]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-ndwork-a-function-explicitly-limits-the-variables-that]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-katanadash-my-mental-model-for-this-are-you-putting-the-mess]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-02-Ravicale-ill-often-inline-every-helper-function-i-find]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-03-jeremdak-i-like-a-big-ass-on-my-functions]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-03-javiercbk-rad-debugger-is-easy-to-read-for-such-a-complex]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-03-0paperpal-will-love-to-read-a-long-article-on-this]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-03-partnano-do-you-have-a-code-example-of-how-you-would]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-03-p_mbanugo-interesting-i-was-just-reviewing-code-and]], [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code/2026-06-03-alecodex-can-you-share-an-open-source-project-that-follows]]

**2/** @rfleury

(It also naturally organizes work by computational requirements rather than abstract similarity, which simplifies code but also puts you in a much better position to make performance considerations)
