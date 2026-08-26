---
title: "New post: \"Multi-Core By Default\""
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1976458516325073141"
author: "Ryan Fleury"
handle: rfleury
post_id: "1976458516325073141"
date: 2025-10-10
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "New post: \"Multi-Core By Default\""
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/1976458516325073141
- Author: Ryan Fleury (@rfleury)
- Posted: 2025-10-10 01:23:25

## Thread

**1/** **@rfleury** ^1976458516325073141

New post: "Multi-Core By Default"

On multi-core programming, not as a special-case technique, but as a new dimension in all code.

![](https://pbs.twimg.com/media/G23KVYlaAAAqLc7?format=png&name=orig)

Branches: [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-heyotetsuo-thats-nice-but-its-funny-if-you-think-people-can]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-harrytrewartha-might-be-interesting-to-see-an-implementation-of]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-VPCOMPRESSB-seems-like-spmd-and-logistics-logic-could]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-flaratt_ljos-holy-shit-this-is-such-a-cool-idea-ive-never]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-nihil2501-are-people-more-commonly-doing-this-style-in-game]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-Noga_Navon-i-mean-it-is-getting-hard-getting-a-single-core]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-Nlitened-shouldnt-single-core-array-summation-be-faster]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-wookash_podcast-do-you-suggest-to-do-it-right-after-main-and]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-_naisstep-with-go-this-is-very-easy]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-BonbliStar-i-used-to-use-this-technique-in-love2d-with-lua]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-joe_sweeney-excellent-post-ive-written-plenty-of-shaders-but]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-the_8th_mage-can-you-say-more-about-this-and-other-cores-can]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-andrew_saraev-thanks-for-sharing-this-ryan-amazing-how-simple]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-py_thri-damn-this-is-highly-illuminating-best-thing-about]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-frogtoss-i-have-not-run-across-this-interesting-pattern-in]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-carl_feynman-my-company-sells-stuff-to-make-this-easy]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-the_8th_mage-it-seems-like-theres-some-problems-with-load]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-RicanSamurai-great-article-and-the-other-previous-linked]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-aepau2-a-similar-style-is-somewhat-common-in-the-linux]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-10-_dtx___-is-this-influenced-by-csp-c-a-r-hoare-saw-the]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-11-Karyuutensei-i-read-your-post-and-it-reminds-me-a-lot-of-how-i]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-11-Karyuutensei-also-interesting-is-the-notion-of-persistent]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-11-preshing-thats-a-very-cool-way-to-exploit-parallelism-in]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-11-truthdotphd-imagine-your-code-as-a-bustling-kitchen-each]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-14-NoxNode-arenas-memory-management-multi-core-by-default]], [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default/2025-10-23-Cappuccino423-cool-idea-i-added-a-similar-model-to-my-language]]

**2/** **@rfleury** ^1976458517935685934

https://www.rfleury.com/p/multi-core-by-default

**3/** **@Colonthreee** ^1976459817024922050

**@rfleury**

What about turning singlethreaded code multithreaded post compile, so we get multithreading by default without all the technobabble?

**4/** **@rfleury** ^1976460285281214609

**@Colonthreee**

Underspecified

**5/** **@Colonthreee** ^1976467661346439362

**@rfleury**

It would be possible to divide workloads efficiently post-compile (or at the compile-step), so that we can benefit from the hardware advances without having to explicitly write it in code. There must be more "streamlined" solutions to this.

**6/** **@rfleury** ^1976468528304918831

**@Colonthreee**

Okay then go do it

**7/** **@Colonthreee** ^1976469056971825527

**@rfleury**

I have been trying to make something like this work for about a year now, but it's impossible to convince investors, and I have very little money to dedicate development time to this, so unless that changes it will most likely be up to someone else...

**8/** **@BretHatin** ^1976616116563972151

**@Colonthreee** **@rfleury**

interaction nets? hvm has raised money, maybe you can follow their footsteps.
