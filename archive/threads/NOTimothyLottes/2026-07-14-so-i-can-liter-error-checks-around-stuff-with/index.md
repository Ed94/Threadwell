---
title: "Another round of getting optimized error checking."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2076888631508107561"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2076888631508107561"
date: 2026-07-14
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Another round of getting optimized error checking."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2076888631508107561
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-14 04:36:51

## Thread

**1/**

Another round of getting optimized error checking. Disassembly [after syscall] shows that it works. 
(1.) Volatile store __LINE__
(2.) Volatile store "error code"
(3.) TEST if error
(4.) Conditional forward branch on error [static prediction untaken]
AS_MINIMAL_AS_ONE_CAN_GET

![](https://pbs.twimg.com/media/HNKWJZqXwAADMnN?format=png&name=orig)

**2/**

A macro cheat sheet to try to explain how it works ...

![](https://pbs.twimg.com/media/HNKX5DhXIAE1BG6?format=png&name=orig)

**3/**

I have a collection of force inline wrappers that test returns from syscalls/functions for error and return the return. These all leverage builtin_expect so the compiler knows to make them fall through in the common case.

![](https://pbs.twimg.com/media/HNKY8qFXQAAF9Db?format=png&name=orig)

**4/**

Those force inlines call Err() on terminal error. The Err() function ensures the {__LINE__, error} stores are visible, then triggers the console drawing code to kill the app with printed error. Then it sleeps until the termination.

![](https://pbs.twimg.com/media/HNKZyFTXYAAETnU?format=png&name=orig)

**5/**

Compiler eventually screws up, but at least it gets the fast path correct, and the slow error path gets an extra call. Effectively it conditionally forward branches to a distant call to Err() instead of just branching to the Err().

**6/**

So I can liter error checks around stuff with little actual cost,
(1.) Two stores
(2.) A CMP or TEST
(3.) An ignored on no-error branch on the first execution! [this code almost never runs 2 times].
