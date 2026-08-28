---
title: "@FlohOfWoe @martin_cohen Sequential languages are still the bee's knees."
type: archive
source: twitter
source_url: "https://x.com/TheGingerBill/status/1211259156365266945"
author: "gingerBill"
handle: TheGingerBill
post_id: "1211259156365266945"
date: 2019-12-29
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - TheGingerBill
description: "@FlohOfWoe @martin_cohen Sequential languages are still the bee's knees."
in_reply_to: ""
---

## Source

- URL: https://x.com/TheGingerBill/status/1211259156365266945
- Author: gingerBill (@TheGingerBill)
- Posted: 2019-12-29 12:14:21

## Thread

**1/** **@TheGingerBill** ^1211259156365266945

**@FlohOfWoe** **@martin_cohen**

Sequential languages are still the bee's knees. I don't care how many people way it's "old fashioned" when it is still the easiest to read and write, and most importantly, easiest to reason about.

The "parallel paradigms" are usually completely unintuitive to reason about.

**2/** **@TheGingerBill** ^1211259575707557888

**@FlohOfWoe** **@martin_cohen**

In many regards, C is the virtual platform that hardware platforms target now, but that's probably a consequence of the kind of architectures CPUs use nowadays (i.e. von Neumann).

**3/** **@TheGingerBill** ^1211260016507936768

**@FlohOfWoe** **@martin_cohen**

The last paragraph in that article is bizarre to me since parallel programming isn't foreign to C-like abstractions either. The issue is that C targets "below the OS" rather than above it. If you had a more modern language that made assumptions such as an OS, the issue is gone.

**4/** **@TheGingerBill** ^1211260444075331585

**@FlohOfWoe** **@martin_cohen**

But "Parallel Programming" is such a bizarre term to me because it means so many different things. What kind of parallelism do you want? Do you want a particular subset such as concurrency? And which model do you want to follow? You cannot escape theory-ladenness.

**5/** **@TheGingerBill** ^1211261396996022273

**@FlohOfWoe** **@martin_cohen**

Sometimes a task queue is the best option, sometimes CSP style is good, sometimes the actor model good, etc.

An interesting problem with regards to programming language design. I don't think there is a silver bullet (sadly) for "parallel programming", but it will be C-like.

**6/** **@TheGingerBill** ^1211264388671430656

**@FlohOfWoe** **@martin_cohen**

My go-to approach in C is still a task queue which can signal where the tasks can signal when done and between other tasks. I'm not sure of the name of this model, but it's a pretty useful and simple one. But importantly, it is a model at the end of the day and it is flawed.
