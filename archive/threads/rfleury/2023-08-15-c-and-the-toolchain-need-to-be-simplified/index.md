---
title: "C and the toolchain need to be simplified & stripped down, not tidied up."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1691290392204132353"
author: "Ryan Fleury"
handle: rfleury
post_id: "1691290392204132353"
date: 2023-08-15
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "C and the toolchain need to be simplified & stripped down, not tidied up."
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/1691290392204132353
- Author: Ryan Fleury (@rfleury)
- Posted: 2023-08-15 03:27:06

## Thread

**1/** **@rfleury** ^1691290392204132353

C and the toolchain need to be simplified & stripped down, not tidied up. Even the simplest of new systems languages have taken ~1 decade (1/5 of a career) to approximate C's practical utility at ~50%. They're still severely lacking in tooling, and they ~all piggyback off LLVM.

**2/** **@TheGingerBill** ^1691518907742334979

**@rfleury**

I am going to be blunt with you:

How many of these new systems languages have actually tried for more than a week? Because this two-penny's opinion is bad. A lot of C's utility is because it's 50 years old, and everything is built around it, for better or worse (mostly worse).

**3/** **@TheGingerBill** ^1691519060570189824

**@rfleury**

I agree with the piggyback off LLVM, and I regret my choices (which is why we are now moving towards the Tilde backend). This is why I tell anyone who wants to attempt to make a new language to stay away from LLVM as far as possible.

 DO NOT USE LLVM!

**4/** **@TheGingerBill** ^1691519416297558016

**@rfleury**

As for "C's practical utility at 50%", that's an extremely vague statement which means nothing.

I know for a fact that Odin for what people use it for is hell of a lot more practical than C and better to deal with. The problems are when interfacing with the C "ecosystem" itself.

**5/** **@rfleury** ^1691661423649370531

**@TheGingerBill**

“The problems are when you need to interact with reality”

**6/** **@hasen_95dx** ^1691692126617387479

**@rfleury** **@TheGingerBill**

The reality that C is broken?

**7/** **@rfleury** ^1691817295428116747

**@Hasen_Judi** **@TheGingerBill**

“Reality is broken”

**8/** **@TheGingerBill** ^1691825782090273215

**@rfleury** **@Hasen_Judi**

You're not helping yourself here, Ryan. The reality of the situation is not a problem. I've already done all of this for Odin.

> C and the toolchain need to be simplified & stripped down, not tidied up.

The toolchain is not the problem. C the language itself is not fixable.

**9/** **@TheGingerBill** ^1691826341497262160

**@rfleury** **@Hasen_Judi**

Having to interface with the C and even Objective-C ecosystems? Already done. Have a better type system to express what C types were actually representing? Done. Have constructs so that you don't even need to specify the vast majority of linker flags and objects separately? Done.

**10/** **@rfleury** ^1691826741000675514

**@TheGingerBill** **@Hasen_Judi**

I’m well aware you think you’ve solved the problem Bill.

**11/** **@TheGingerBill** ^1691827528359374928

**@rfleury** **@Hasen_Judi**

I don't think I've solved ALL of the problems. Most of them are just trade-offs, with loads of compromises and issues. 

I could literally lecture on all of the issues with Odin for days straight.

**12/** **@TheGingerBill** ^1691828062415925466

**@rfleury** **@Hasen_Judi**

But you are complaining without actually giving any concrete ideas, nor even concrete things about what is wrong. Be explicit. And don't just say you said it in another vague "thread".

This is all I am frustrated about. You are a very smart man, but are being extremely vague.

**13/** **@rfleury** ^1691830184025178477

**@TheGingerBill** **@Hasen_Judi**

I’m forced to compress and abstract over 100s of ideas because of the breadth of the problem space, of the discussion, and the Twitter character limit. If that ends up vague, that’s a valid criticism. I’ll write a post with a list of concrete project & spec descriptions. Deal?

**14/** **@TheGingerBill** ^1691830364098941251

**@rfleury** **@Hasen_Judi**

Deal! I would love to read such an article from you 🙂
