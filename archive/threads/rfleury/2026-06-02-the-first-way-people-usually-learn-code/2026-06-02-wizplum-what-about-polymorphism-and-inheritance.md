---
title: "@rfleury What about polymorphism and inheritance?"
type: archive
source: twitter
source_url: "https://x.com/wizplum/status/2061622209383379247"
author: "wizplum"
handle: wizplum
post_id: "2061622209383379247"
date: 2026-06-02
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury What about polymorphism and inheritance?"
in_reply_to: ""
parent_post_id: "2061619837877780961"
---

## Source

- URL: https://x.com/wizplum/status/2061622209383379247
- Author: wizplum (@wizplum)
- Posted: 2026-06-02 01:33:32

## Branch

**1/** @wizplum

@rfleury

What about polymorphism and inheritance?

**2/** @rfleury

@wizplum

Largely useless and terrible

**3/** @SaladeTomate18

@rfleury @wizplum

You still need callback for buttons OnClick.

I assume that's why you said largely (99%) and not always (100%)

**4/** @rfleury

@SaladeTomate18 @wizplum

No, you don’t. You shouldn’t even have that concept. It’s not a good design.

**5/** @SaladeTomate18

@rfleury @wizplum

How would you handle it ?

It is totally not my domain so I am just repeating basic patterns I've seen in many UI libraries.

Thinking about it on the spot all I see is using IDs on buttons and a big switch.

**6/** @rfleury

@SaladeTomate18 @wizplum

Check this out

https://youtu.be/Z1qyvQsjK5Y

**7/** @SaladeTomate18

@rfleury @wizplum

Already watched it years ago 😅

I thought we were talking specifically retained UI. Not Immediate ones.

I do have some friends that worked on AAA with IM UI and they told me performance was not good compared to retained mode (could be just bad code ofc)

**8/** @rfleury

@SaladeTomate18 @wizplum

Even with retained mode you do not need callbacks. But no, your friends are incorrect. There is nothing in principle about IM UI that makes it less performant than RM. In many cases it’s quite the opposite.

## Related

- Spine: [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code]]
