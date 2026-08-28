---
title: "TIL that this is correct syntax and that `finally` runs after the return of the function"
type: archive
source: twitter
source_url: "https://x.com/alexdotjs/status/1704472735219339585"
author: "Alex / KATT 🐱"
handle: alexdotjs
post_id: "1704472735219339585"
date: 2023-09-20
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - alexdotjs
description: "TIL that this is correct syntax and that `finally` runs after the return of the function"
in_reply_to: ""
---

## Source

- URL: https://x.com/alexdotjs/status/1704472735219339585
- Author: Alex / KATT 🐱 (@alexdotjs)
- Posted: 2023-09-20 12:29:02

## Thread

**1/** **@alexdotjs** ^1704472735219339585

TIL that this is correct syntax and that `finally` runs after the return of the function

#junior4lyfe

![](https://pbs.twimg.com/media/F6eAcpHWkAAp18v?format=png&name=orig)

**2/** **@ThePrimeagen** ^1704676599210127604

**@alexdotjs**

Try catch is a mistake

**3/** **@rfleury** ^1704715681831538787

**@ThePrimeagen** **@alexdotjs**

“Error data” is not special data, and doesn’t deserve special treatment via special language features. Error conditions are just conditions, and code needs to be prepared one way or another for all plausible conditions

**4/** **@eloytoro** ^1704801861570560417

**@rfleury** **@ThePrimeagen** **@alexdotjs**

How about panics

**5/** **@rfleury** ^1704841356181745924

**@eloytoro** **@ThePrimeagen** **@alexdotjs**

Panics are reasonable but are appropriate for a very small % of what people call “errors”

**6/** **@eloytoro** ^1704842606943899762

**@rfleury** **@ThePrimeagen** **@alexdotjs**

the problem is when there's no semantic difference between an exception and a panic, like in JS/Java/C++ etc
