---
title: "Back in 1993, I was taking a number theory class, and there was a semester-long factorization contest that we could participate in."
type: archive
source: twitter
source_url: "https://x.com/EricLengyel/status/1389106103179378689"
author: "Eric Lengyel"
handle: EricLengyel
post_id: "1389106103179378689"
date: 2021-05-03
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - EricLengyel
description: "Back in 1993, I was taking a number theory class, and there was a semester-long factorization contest that we could participate in."
in_reply_to: ""
---

## Source

- URL: https://x.com/EricLengyel/status/1389106103179378689
- Author: Eric Lengyel (@EricLengyel)
- Posted: 2021-05-03 06:34:37

## Thread

**1/** **@EricLengyel** ^1389106103179378689

Back in 1993, I was taking a number theory class, and there was a semester-long factorization contest that we could participate in. I implemented a distributed multiple polynomial quadratic sieve (MPQS) for the Mac, and I needed a cluster of computers to run it on.

**2/** **@EricLengyel** ^1389106104240525319

The computer lab in the math building had a bunch of Mac Centris 650s on an AppleTalk network. But they were running some kind of secure software that didn't give you access to the Finder, only specific software, so I couldn't pop in a disk and run my own programs.

**3/** **@EricLengyel** ^1389106107696631808

You can see in this picture that the Centris had two little buttons on the front. One was a reset button, and the other generated a non-maskable interrupt (NMI). If Macsbug was installed, the NMI button froze everything and dropped you into the system debugger.

![](https://pbs.twimg.com/media/E0cP-6yVgAERsOJ?format=jpg&name=orig)

**4/** **@EricLengyel** ^1389106109265235970

If no debugger was installed, then the NMI button brought up a small system monitor window. It was extremely basic and didn't do much more than let you look at raw memory and, importantly, let you poke new byte values into memory at arbitrary addresses.

**5/** **@EricLengyel** ^1389106110389391362

On my own computer, I wrote a tiny program that would display the system file picker and execute whatever file was chosen. I printed out the machine code for that program and brought it with me to the lab. It was only a few dozen 8-bit hex values.

**6/** **@EricLengyel** ^1389106111450468352

I could enter that program in the system monitor, but I needed a way to run it. The Mac had several hooks (function pointers) at fixed low-memory addresses, and one of them was a callback that would be repeatedly invoked as the user was dragging something in the GUI.

**7/** **@EricLengyel** ^1389106112436195330

So I put my program's address into that hook, exited the monitor, and dragged a scroll bar indicator somewhere. Bam! The system file picker appears. I navigate to the Finder program, select it, and click Open. The Finder launches, and I have full access to the computer.

**8/** **@EricLengyel** ^1389106113618989057

I repeated this on about 15 computers and loaded my MPQS program on each of them. About half the lab was now running a distributed factorization algorithm controlled by a central host over the network, and the whole thing actually got results!

**9/** **@EricLengyel** ^1389106114583678980

On these computers, I could factor a general number with around 70 decimal digits in a reasonable amount of time (like overnight). And yes, I won the contest.

Branches: [[archive/threads/EricLengyel/2021-05-03-back-in-1993-i-was-taking-a-number-theory-class/2021-05-04-JonathanShafter-you-sir-are-my-hero]], [[archive/threads/EricLengyel/2021-05-03-back-in-1993-i-was-taking-a-number-theory-class/2021-05-04-StevenB337-thread]], [[archive/threads/EricLengyel/2021-05-03-back-in-1993-i-was-taking-a-number-theory-class/2021-05-04-JEdwardPrice1-awesome]], [[archive/threads/EricLengyel/2021-05-03-back-in-1993-i-was-taking-a-number-theory-class/2021-05-04-thinkx-macsbug-was-freaking-work-of-genius-imho]], [[archive/threads/EricLengyel/2021-05-03-back-in-1993-i-was-taking-a-number-theory-class/2021-05-04-vapejuicepen-they-let-you-win-the-contest-cuz-they-felt-sry-4]], [[archive/threads/EricLengyel/2021-05-03-back-in-1993-i-was-taking-a-number-theory-class/2021-05-04-otaria123-please-unroll]], [[archive/threads/EricLengyel/2021-05-03-back-in-1993-i-was-taking-a-number-theory-class/2021-05-04-riptusk331-did-the-computer-lab-catch-on]], [[archive/threads/EricLengyel/2021-05-03-back-in-1993-i-was-taking-a-number-theory-class/2021-05-07-udsd007-serious-applause-and-kudos]]
