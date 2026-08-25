---
title: "Programming practices that increase total code volume lead to more bugs and less performance."
type: archive
source: twitter
source_url: "https://x.com/cmuratori/status/1691186899212472321"
author: "Casey Muratori"
handle: cmuratori
post_id: "1691186899212472321"
date: 2023-08-14
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - cmuratori
description: "Programming practices that increase total code volume lead to more bugs and less performance."
in_reply_to: ""
---

## Source

- URL: https://x.com/cmuratori/status/1691186899212472321
- Author: Casey Muratori (@cmuratori)
- Posted: 2023-08-14 20:35:52

## Thread

**1/** @cmuratori

Programming practices that increase total code volume lead to more bugs and less performance. It's not a tradeoff, it's a lose-lose. When you use significantly more code than is necessary to implement a feature, you provide an order of magnitude more code path combinations for bugs.

People think "delivering features" is somehow at odds with delivering reasonable performance. The opposite is true. Reliable code often tends to perform very well on modern CPUs. It's unreliable code that manages to cripple a modern CPU, because it is built out of massive stacks of unnecessary layers whose interactions have never been thought through by anyone.

Branches: [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-14-dmitriid-this-is-the-best-metaphor-not-ironically-also]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-14-Saniell_-funny-enough-when-you-write-oop-language-design]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-14-0xlac-the-answers-to-op-install-a-plugin-on-top-of-vs]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-14-matt_j2-my-approach-is-to-write-code-that-i-can-come-back]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-14-snlwtn-vs2022-on-mac-is-virtually-unusable]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-14-TanishqSingla_-not-to-mention-how-modern-software-shamelessly]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-14-KDmitriy99-it-cant-even-ctrl-a-after-some-update-a-few]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-14-TheBuzzSaw-just-today-in-vs-2022-the-semantic-analyzer]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-14-t3chn01200-performance-is-a-feature-change-my-mind]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-15-00jknight-i-largely-consider-clean-code-to-mean-that-the]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-15-DefenceForceOrg-i-do-have-both-vs2022-and-vs2019-on-my-machine]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-15-EduardKafe-developers-had-no-reason-to-uograde-their]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-15-unclebobmartin-generally-speaking-thats-a-good-principle-but-its]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-15-enjoyingthewind-is-there-a-good-reason-to-use-vs-instead-of-vscode]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-15-Bordonius-vscode-will-end-up-going-the-way-of-all-editors]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-15-Hannomalie1-does-more-code-automatically-mean-more-code-paths]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-16-SamvStachelski-strange-never-had-that-problem-with-that-waaaay]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-16-rudiservo-true-and-false-depends-on-the-project-and-the]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-16-DavidBBlack-agree-completely-another-aspect-is-the-importance]], [[archive/threads/cmuratori/2023-08-14-programming-practices-that-increase-total-code/2023-08-20-hasen_95dx-architecture-is-difficult-and-most-people-have-no]]

**2/** @ExodusPgame

@cmuratori

When I was into clean code and wrote code to be "future proof", what caused me to slowly snap out of it, was that adding new features became more and more difficult due of the code structure, which directly contradicted the promise.

Your videos accelerated the process.
